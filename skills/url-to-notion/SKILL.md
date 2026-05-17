---
name: url-to-notion
description: 根据 URL 抓取文章全文，裁剪后保存到 Notion「整理笔记」数据库。自动处理 JS 渲染页面（少数派等），使用 Notion Files API 直接上传图片（无需外部图床），生成标签和摘要。触发词：保存文章到 Notion、裁剪文章、保存到整理笔记、url-to-notion。
version: 1.0.0
metadata:
  homepage: https://github.com/victor-skills#url-to-notion
---

# URL to Notion

根据 URL 抓取文章全文，裁剪精华内容，保存到 Notion「整理笔记」数据库。

## 核心流程

### 1. 抓取文章内容

**通用方法：** 优先使用 `opencli web` 抓取（适配多种网站，支持 JS 渲染）

```bash
~/.npm-global/bin/opencli web article "<URL>" -f json > /tmp/article_<id>.json
```

如果 `opencli web` 抓取失败或返回内容为空，回退到 `agent-browser`：

```bash
agent-browser open "<URL>"
agent-browser wait --load networkidle
agent-browser wait 3000
agent-browser get text body --json
```

**X/Twitter 特殊处理（统一流程）：**

使用 `opencli twitter` 系列命令统一处理 X 推文和 X Article，支持文本 + 图片/附件全量下载。

**步骤 1：抓取文本内容**
```bash
# 普通推文 / X Article 均使用 article 命令
~/.npm-global/bin/opencli twitter article "<X URL>" -f json > /tmp/x_<id>.json
```

- 普通推文：内容在返回的 `content` 字段（Markdown 格式）
- X Article：内容在 `content` 字段（含标题、完整正文 Markdown）
- 从返回结果中提取：`title`, `author`, `content`, `url`

**步骤 2：下载所有图片/附件**
```bash
~/.npm-global/bin/opencli twitter download --tweet-url "<X URL>" -f json --output /tmp/x_dl_<id>
```

- 自动下载推文/文章中的所有图片（含封面 + 内嵌截图）
- 文件保存在 `/tmp/x_dl_<id>/tweets/` 目录下，命名 `tweet_1.jpg`, `tweet_2.png` 等
- 返回 JSON 列表，每项含 `index`, `type`, `status`, `size`
- 支持普通推文（1-4 张图）和 X Article（多张内嵌截图）

> ⚠️ 此命令需要 opencli 已配置 Twitter 登录态（browser profile）。

**步骤 3：上传图片到 Notion**
```bash
python3 << 'PYEOF'
import json, subprocess, os, time

NOTION_KEY = open(os.path.expanduser("~/.config/notion/api_key")).read().strip()
IMG_DIR = "/tmp/x_dl_<id>/tweets"
file_ids = []

for f in sorted(os.listdir(IMG_DIR)):
    if not f.lower().endswith(('.jpg','.jpeg','.png','.gif','.webp')):
        continue
    fpath = os.path.join(IMG_DIR, f)
    mime = subprocess.run(["file","--mime-type","-b",fpath], capture_output=True, text=True).stdout.strip()
    
    # Create upload object
    r = subprocess.run(["curl","-s","-X","POST",
        "https://api.notion.com/v1/file_uploads",
        "-H",f"Authorization: Bearer {NOTION_KEY}",
        "-H","Notion-Version: 2025-09-03",
        "-H","Content-Type: application/json",
        "-d",json.dumps({"filename":f,"content_type":mime})],
        capture_output=True, text=True)
    file_id = json.loads(r.stdout)["id"]
    
    # Send file
    subprocess.run(["curl","-s","-X","POST",
        f"https://api.notion.com/v1/file_uploads/{file_id}/send",
        "-H",f"Authorization: Bearer {NOTION_KEY}",
        "-H","Notion-Version: 2025-09-03",
        "-F",f"file=@{fpath};filename={f}"], capture_output=True)
    
    file_ids.append((f, file_id))
    print(f"Uploaded: {f} -> {file_id}")
    time.sleep(0.4)

# Save for later use
json.dump(file_ids, open("/tmp/x_dl_<id>/file_ids.json","w"))
print(json.dumps(file_ids))
PYEOF
```

**步骤 4：写入 Notion 页面**

先创建页面（属性 + 封面），再添加正文内容和图片。

- 封面：使用第一张图片（`tweet_1.jpg` 通常是封面）
- 正文：将 `content` 字段解析为 Markdown，转换为 Notion blocks
- 图片插入：用 `after` 参数将剩余图片插入到正文中合适位置（如每个 section 之后）

> 图片插入策略：
> - 第一张图片 (`tweet_1.jpg`) 作为页面封面
> - 剩余图片均匀分布在正文各 section 之后，或放在文末「附录：原文截图」section 中
> - 使用 `PATCH /v1/blocks/{page_id}/children` + `"after": "<block_id>"` 插入

### 2. 提取图片 URL

从页面中提取正文区域的图片：

```bash
agent-browser eval '
  const imgs = Array.from(document.querySelectorAll("img"))
    .map(img => img.src || img.dataset?.src || "")
    .filter(src => src && src.startsWith("http") && src.includes("cdn"))
    .slice(0, 30);
  JSON.stringify(imgs);
'
```

### 3. 下载图片（处理防盗链）

很多 CDN 有 Referer 防盗链，需要用 `Referer` 头下载：

```bash
mkdir -p /tmp/sspai_<article_id>
curl -sL -H "Referer: https://sspai.com/" -o /tmp/sspai_<id>/img01.jpeg "<image_url>"
```

### 4. 上传图片到 Notion（Files API）

Notion 2025 年新增 Files API，可直接上传图片到 Notion 托管的存储，无需外部图床。

**单文件上传流程（适用于 < 5MB 的图片）：**

```bash
NOTION_KEY=$(cat ~/.config/notion/api_key)
FILE_PATH="/tmp/sspai_<id>/img01.png"
FILE_NAME="img01.png"

# 步骤 1：创建上传对象
FILE_ID=$(curl -s -X POST "https://api.notion.com/v1/file_uploads" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d "{\"filename\": \"$FILE_NAME\", \"content_type\": \"image/png\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# 步骤 2：上传文件二进制数据
curl -s -X POST "https://api.notion.com/v1/file_uploads/$FILE_ID/send" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -F "file=@$FILE_PATH;filename=$FILE_NAME"

echo "File ID: $FILE_ID"
```

**批量上传脚本：**

```bash
NOTION_KEY=$(cat ~/.config/notion/api_key)
declare -A FILE_IDS
for f in /tmp/sspai_<id>/img*; do
  name=$(basename "$f")
  mime=$(file --mime-type -b "$f")
  
  # Create upload
  file_id=$(curl -s -X POST "https://api.notion.com/v1/file_uploads" \
    -H "Authorization: Bearer $NOTION_KEY" \
    -H "Notion-Version: 2025-09-03" \
    -H "Content-Type: application/json" \
    -d "{\"filename\": \"$name\", \"content_type\": \"$mime\"}" \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
  
  # Send file
  curl -s -X POST "https://api.notion.com/v1/file_uploads/$file_id/send" \
    -H "Authorization: Bearer $NOTION_KEY" \
    -H "Notion-Version: 2025-09-03" \
    -F "file=@$f;filename=$name" > /dev/null
  
  FILE_IDS[$name]=$file_id
  echo "Uploaded: $name -> $file_id"
  
  # Rate limit: Notion ~3 req/s
  sleep 0.4
done
```

**使用 Python 库（更简洁）：**

```bash
pip3 install notion-upload  # 首次需安装

python3 << 'EOF'
from notion_upload import notion_upload
import json

api_key = open("$HOME/.config/notion/api_key").read().strip()
files = ["/tmp/sspai_<id>/img01.png", "/tmp/sspai_<id>/img02.png"]
file_ids = []

for f in files:
    name = f.split("/")[-1]
    up = notion_upload(f, name, api_key)
    file_id = up.upload()
    file_ids.append(file_id)
    print(f"Uploaded {name} -> {file_id}")

# 输出 JSON 供后续使用
print(json.dumps(file_ids))
EOF
```

### 5. 创建 Notion 页面

目标数据库：`整理笔记`
- `database_id`: `05c87b65-e76b-4789-a38c-5c84809d300f`
- `data_source_id`: `d42aae33-7fc9-4fa5-9b57-7c30d6c7d1b3`

固定属性：
| 属性 | 值 |
|------|-----|
| 卡片类型 | 文献笔记 |
| 文献类型 | 文章 |
| 标签 | 根据内容自动生成 3-5 个（参考下方标签库） |
| 🚩 领域 | **必须设置**，根据文章内容匹配领域数据库（见下方领域映射表） |

**🚩 领域映射表（领域 database_id: `ac9e08fc-67f9-423f-a141-49ac44be6bf2`）：**

| 领域名称 | page_id | 匹配关键词 |
|---------|---------|----------|
| AI人工智能探索 | `ed5986fc-f0ad-40ce-8f42-f024f9fdc682` | AI、人工智能、机器学习、大模型、LLM、Agent、智能体、深度学习、神经网络、ChatGPT、OpenAI、AI工具、AI编程 |
| 软件工程 | `d910d18f-7f98-4cf1-be83-92d8becd4aa2` | 开发、编程、软件工程、架构、DevOps、测试、代码、技术栈、前端、后端、全栈、API、数据库 |
| 产品设计 | `db72e064-5347-4be9-9f3e-27e3d3a007eb` | 产品设计、UX、UI、交互设计、用户体验、产品管理、PRD、设计系统、可用性测试 |
| 知识管理 | `d67f2535-eed2-4b20-a507-66dda792dcbe` | 知识管理、笔记、第二大脑、PKM、Obsidian、Notion、Roam、卡片笔记、学习方法、记忆、阅读方法 |
| 工具最佳实践 | `3c546c15-556f-44ba-b777-2ac60b2673bf` | 工具推荐、效率工具、工作流、自动化、最佳实践、技巧、教程、how-to、工具评测 |
| 💰投资 | `3570f06d-1a7f-8003-a5d9-fe0483f9cea1` | 投资、股票、基金、加密货币、理财、财务规划、市场分析、价值投资 |
| 🔗 Web3 与区块链 | `3570f06d-1a7f-815a-b3e6-ce1389389ca6` | Web3、区块链、DeFi、NFT、智能合约、去中心化、DAO、以太坊、比特币 |
| 阅读 | `2740f06d-1a7f-801f-9007-c6478d6f80f9` | 书评、读书笔记、阅读推荐、书单、文学、小说、非虚构阅读 |
| 摄影 | `2190f06d-1a7f-8066-ad5e-feed0decb336` | 摄影、相机、拍照技巧、后期处理、摄影器材、构图、光影 |
| 生活 | `b0dccc25-90b3-4567-9966-0b5284fb3907` | 生活方式、健康、健身、旅行、美食、家居、情感、心理、冥想、正念、习惯、个人成长 |

**选择规则：**
1. 根据文章主题选择**最匹配的 1 个领域**（优先选择匹配度最高的）
2. 如果文章跨多个领域，选择占比最大的那个
3. 如果无法匹配到任何领域，选择「生活」作为默认
4. 领域通过 relation 字段设置：`"🚩 领域": {"relation": [{"id": "<domain_page_id>"}]}`

```bash
NOTION_KEY=$(cat ~/.config/notion/api_key)
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "05c87b65-e76b-4789-a38c-5c84809d300f"},
    "properties": {
      "Name": {"title": [{"text": {"content": "<文章标题>"}}]},
      "URL": {"url": "<原始URL>"},
      "为什么收集此笔记": {"rich_text": [{"text": {"content": "<1-2句话说明为什么收集这篇笔记>"}}]},
      "总结": {"rich_text": [{"text": {"content": "<1-2段核心内容摘要>"}}]},
      "卡片类型": {"select": {"name": "文献笔记"}},
      "文献类型": {"select": {"name": "文章"}},
      "标签": {"multi_select": [{"name": "标签1"}, {"name": "标签2"}, {"name": "标签3"}]},
      "🚩 领域": {"relation": [{"id": "<匹配的领域page_id>"}]}
    }
  }'
```

### 6. 添加正文内容

用 `PATCH /v1/blocks/{page_id}/children` 添加内容块。每批不超过 100 个 blocks。

```bash
curl -s -X PATCH "https://api.notion.com/v1/blocks/<page_id>/children" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"children": [...]}'
```

**翻译规则：**
- 原文为英文、繁体中文或其他语言时 → 翻译为简体中文
- 原文为简体中文时 → 直接保留
- 翻译必须忠实原文，不增删观点、不改语气、不添加个人解读
- 专有名词（人名、产品名、技术术语）可保留英文原文或在首次出现时加括号标注
- 代码块、引用、表格等技术性内容保持原文格式

**内容裁剪原则：**
- ⚠️ 核心规则：不要修改、重写、改写原文内容。保留原文的段落、句式、语气
- 仅做「结构性裁剪」：删除导航栏、侧边栏、评论、页脚、广告、SEO 标签、作者头像等非正文元素
- 如果原文是非中文（英文、繁体中文等），翻译为简体中文。翻译时忠实原文，不增删观点
- 如果原文已经是简体中文，直接保留，不做翻译
- 保留核心图片（封面 + 正文配图，通常 5-10 张），使用 Notion Files API 上传图片后用 `file_upload` ID 引用
- 保留原文链接和作者信息
- 末尾可添加简短的「核心要点速查」（3-5 条），但正文内容必须是原文的忠实呈现

**Block 类型参考：**
- 标题：`heading_1`, `heading_2`, `heading_3`
- 段落：`paragraph`
- 列表：`bulleted_list_item`, `numbered_list_item`
- 图片：`{"type":"image","image":{"type":"file_upload","file_upload":{"id":"<file_id>"}}}`
- 分割线：`{"type":"divider","divider":{}}`
- Callout：`{"type":"callout","callout":{"rich_text":[...],"icon":{"emoji":"📝"}}}`

## 标签库

根据文章内容从已有标签中选择 3-5 个。常用标签分类：

### 通用
- 生产力、效率、工具、工作流、最佳实践、时间管理、知识管理、第二大脑、笔记

### 技术
- AI、人工智能、大模型、LLM、AI编程、AI辅助编程、Agent、智能体、OpenAI、ChatGPT、编程、开发、软件工程、软件开发、前端、全栈能力、Node.js、TypeScript、JavaScript、Python

### 内容源
- 少数派、RSS、资讯、公众号文章、YouTube视频、B站视频、博客、资讯文章

### 方法论
- 方法论、设计思想、思维方式、思考工具、产品设计、设计原则

### 产品/商业
- 产品、产品经理、商业模式、商业分析、创业、副业、独立开发、Side Project、SaaS、产品方案

### 生活方式
- 旅行、旅行、出行、旅游、自驾游、摄影、健身、健康、极简生活、穿搭、投资、基金

### 管理/成长
- 管理、团队管理、项目管理、自我提升、习惯养成、自律、沟通

**选择规则：**
1. 优先选择与文章主题最匹配的 2-3 个标签
2. 如果文章来自特定平台（少数派/公众号/博客），加上对应的来源标签
3. 如果涉及 AI/技术，加上对应的技术标签
4. 总数控制在 3-5 个

## 错误处理

### CDN 防盗链（Referer 限制）
症状：下载图片时失败或返回 403。
解法：下载图片时带上原文域名的 Referer 头，然后通过 Notion Files API 上传到 Notion 托管存储。

### Notion Files API
- **单文件限制**：5MB（`enforce_max_size=True`），图片通常远小于此限制
- **API 版本**：必须使用 `Notion-Version: 2025-09-03`（文件上传专属版本）
- **流程**：创建上传对象 → 发送文件 → 在 block 中引用 file_upload ID
- **Rate limit**：~3 req/s，上传多张图片时需 `sleep 0.4` 间隔
- **支持格式**：image/jpeg, image/png, image/gif, image/webp, image/svg+xml, image/heic, image/tiff, image/avif, image/bmp, image/apng, image/vnd.microsoft.icon

### Files API 上传失败
- 400 错误：检查 filename 和 content_type 是否正确
- 401 错误：检查 NOTION_KEY 是否有效
- 413 错误：文件超过 5MB 限制，需压缩或使用 multi_part 模式
- multi_part 模式：文件 > 20MB 时自动启用，需分片上传 + complete 信号

### Notion API 限制
- Block 创建：Rate limit ~3 req/s，Payload limit 100 blocks per request, 500KB
- 图片 block 中使用 file_upload 类型时，文件必须先通过 Files API 上传

### 页面抓取失败
- `web_fetch` 对 JS 渲染页面无效，必须用 `agent-browser`
- 少数派、知乎等都需要浏览器渲染
- 等待 `networkidle` 后再抓取内容

### X/Twitter 抓取失败
- 优先使用 `opencli twitter article <URL> -f json` 获取内容
- 备用方案：`opencli twitter download --tweet-url <URL>` 下载图片/附件
- 如果 opencli 未登录 Twitter：回退到 fxtwitter API（`https://api.fxtwitter.com/<user>/status/<id>`），但只能获取文本，图片需手动提取
- X Article 的内嵌图片是私有媒体，只有通过 opencli browser 登录态才能下载

### opencli twitter download 注意事项
- 文件保存在 `--output` 目录下的 `tweets/` 子目录中
- 命名规则：`tweet_1.jpg`, `tweet_2.png` 等（按顺序编号）
- 第一张通常是封面图
- 返回的 JSON 含 `index`, `type` (image/video), `status`, `size` 字段
- 下载图片时必须带 `Referer: https://x.com/` 头，否则 CDN 返回 403

## 操作完成后返回结果

**每次操作完成后，必须向用户返回新增的 Notion 页面链接。**

从创建页面 API 响应中提取 `url` 字段（Notion API 返回 `page.url`），格式如下：

```
✅ 已保存到 Notion 整理笔记

- **标题**：{文章标题}
- **作者**：{作者}
- **领域**：{领域名称}
- **标签**：{标签1}、{标签2}、{标签3}
- **页面**：{page_url}

（如有图片/附件，补充说明处理情况）
```

> ⚠️ 如果创建页面时 API 响应没有 `url` 字段，手动拼接：`https://www.notion.so/{title-slug}-{page_id_no_dashes}`
> 其中 `page_id_no_dashes` 是页面 ID 去掉连字符的格式。

## 快速参考

```bash
# 环境变量
NOTION_KEY=$(cat ~/.config/notion/api_key)

# Notion Files API
FILES_API_URL="https://api.notion.com/v1/file_uploads"
FILES_API_VERSION="2025-09-03"

# 数据库
整理笔记 database_id: 05c87b65-e76b-4789-a38c-5c84809d300f
整理笔记 data_source_id: d42aae33-7fc9-4fa5-9b57-7c30d6c7d1b3

# Image block with file_upload
IMAGE_BLOCK='{"type":"image","image":{"type":"file_upload","file_upload":{"id":"<file_id>"}}}'

# X 推文/X Article 统一处理流程
# 1. opencli twitter article <URL> -f json > /tmp/x_<id>.json  (文本)
# 2. opencli twitter download --tweet-url <URL> -f json --output /tmp/x_dl_<id>  (图片)
# 3. Python 脚本批量上传 Notion Files API
# 4. 第一张作封面，其余用 after 参数插入正文
```

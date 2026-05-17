---
name: music-notes
description: 深度音乐研究 Agent。接收歌曲名、艺人、Apple Music/Spotify/YouTube 链接、歌词片段或听感,自动识别歌曲/专辑/歌手并进行深度研究,生成高质量音乐研究笔记,写入 Notion 音乐数据库(使用类型字段区分)。触发词:音乐研究、研究这首歌、music research、分析这首歌、记录音乐、专辑研究、歌手研究。
version: 1.0.0
metadata:
  homepage: https://github.com/victor-skills#music-research
---

# Music Research - 深度音乐研究技能

接收歌曲名、艺人、音乐链接或听感,自动识别歌曲/专辑/歌手并进行深度研究,生成高质量音乐研究笔记,写入 Notion 音乐数据库。

## 核心流程

```
输入(歌名/链接/歌词/听感/专辑名/歌手名)
    ↓
识别类型(单曲 / 专辑 / 歌手)
    ↓
深度研究(根据类型选择研究方向)
    ↓
生成音乐研究笔记(高质量 Markdown 格式)
    ↓
写入 Notion 音乐数据库(创建页面 + 正文内容块,设置类型字段)
```

## 数据库信息

- **Notion 音乐数据库** databaseId: `3550f06d1a7f800ea4adf722d176a2e0`
- **Data Source ID**(用于查询):`3550f06d-1a7f-80df-bb22-000b73a97e67`
- **领域数据库** databaseId: `ac9e08fc-67f9-423f-a141-49ac44be6bf2`

## Step 0: 识别输入类型

根据用户输入判断是要创建哪种类型的页面:

| 类型 | 触发场景 | 示例 |
|------|---------|------|
| **单曲** | 输入歌曲名、歌曲链接、歌词片段 | "Kiss Goodbye"、Apple Music 单曲链接 |
| **专辑** | 输入专辑名、提到"专辑"、专辑链接 | "盖世英雄"、"分析这张专辑" |
| **歌手** | 输入歌手名、提到"歌手"、艺人链接 | "周杰伦"、"介绍一下这个歌手" |

**类型判断规则**:
- 如果用户明确提到"专辑"或"歌手",按用户意图
- 如果是单曲链接(Apple Music 包含 `?i=` 参数),判定为单曲
- 如果是专辑链接(Apple Music 不含 `?i=` 参数),判定为专辑
- 默认情况下,输入歌曲名 → 单曲

## Step 1: 识别内容

根据输入类型搜索确认信息:

### 单曲识别

```bash
# 搜索歌曲
web_search "<歌曲名/关键词> 歌手 专辑"

# 如果是链接,从 URL 提取信息
web_fetch --url "<URL>" --maxChars 10000
```

必须确认:
- 歌曲名(准确名称)
- 原唱/主要艺人
- 作词人(如有公开信息)
- 作曲人(如有公开信息)
- 专辑名
- 发行日期(或年份)
- 流派/曲风(最多 3 个)
- 语言(中文/英文/日文/韩文/其他)

### 经典歌词提取

研究阶段搜索歌词来源:
```bash
# 搜索歌词
web_search "<歌曲名> <艺人> 歌词 genius"
web_search "<歌曲名> <艺人> lyrics"

# 从 Genius 提取
web_fetch --url "https://genius.com/<artist>-<song>-lyrics" --maxChars 10000
```

提取 **2-4 句最经典/最有代表性的歌词**,选择标准:
- 最抓耳/最有记忆点的 hook 句
- 最能体现歌曲主题或情感的核心句
- 文学性最强、意境最美的句子
- 流传最广、最常被引用的句子

⚠️ 不要复制整段歌词,只选最精华的几句。

### 专辑识别

必须确认:
- 专辑名(准确名称)
- 主要艺人/歌手
- 发行日期
- 唱片公司
- 流派/曲风
- 曲目数量
- 制作人(如有公开信息)

### 歌手识别

必须确认:
- 歌手名/艺名
- 出生地/国籍
- 出道年份
- 代表作品
- 主要流派
- 重要奖项

## Step 2: 深度研究

### 单曲研究维度

根据歌曲特点,从以下维度中**动态选择**最值得研究的方向:

| 维度 | 适用场景 |
|------|---------|
| 创作背景 | 有故事可讲(演唱会即兴、个人经历触发) |
| 艺人阶段 | 该歌曲在艺人职业生涯中的位置 |
| 制作过程 | 制作人、录音室、DAW、合成器、鼓机 |
| 编曲逻辑 | 和声进行、乐器编排、结构 |
| Groove/节奏 | 节奏设计、律动感、节奏密度 |
| 声音设计 | 合成器音色、texture、空间感 |
| 低频设计 | Bassline 设计、低频处理 |
| Stereo Image | 立体声场、空间感、混音宽度 |
| 人声处理 | 和声编排、人声效果链、真假音 |
| Mixing/Mastering | 混音理念、母带处理特点 |
| Sample 来源 | Sampled 曲目、翻唱、采样历史 |
| 流派演化 | 该歌曲在音乐流派演化链上的位置 |
| 社会/文化背景 | 时代背景、文化运动、社会意义 |
| 社区讨论 | Reddit/YouTube/论坛经典讨论 |
| 乐评观点 | Pitchfork/RS/RYM 等评分或评价 |
| 历史定位 | 对后续音乐的影响、历史意义 |
| Live 演出变化 | 不同 live 版本的改编 |
| Remix/Demo | 官方 Remix、Demo 版本对比 |
| 歌词分析 | 歌词文学性、核心意象、叙事结构 |

### 专辑研究维度

| 维度 | 适用场景 |
|------|---------|
| 专辑概念 | 专辑整体主题、概念设计 |
| 制作过程 | 制作周期、录音室、制作团队 |
| 曲目编排 | 曲目顺序设计、起承转合 |
| 音乐风格演化 | 与艺人前作的对比、风格变化 |
| 商业表现 | 销量、排行榜、奖项 |
| 文化影响 | 对行业的影响、粉丝反应 |
| 视觉设计 | 封面设计、MV、视觉概念 |

### 歌手研究维度

| 维度 | 适用场景 |
|------|---------|
| 音乐生涯 | 出道历程、重要转折点 |
| 音乐风格 | 流派演变、风格特点 |
| 代表作品 | 最知名作品分析 |
| 制作能力 | 创作/制作/编曲能力 |
| 商业成就 | 销量、巡演、商业价值 |
| 文化影响 | 对行业的影响、历史地位 |
| 个人经历 | 影响音乐创作的人生经历 |

### 按流派的研究侧重

| 流派 | 重点研究方向 |
|------|------------|
| Hip-Hop | Sample 来源 / Flow / 制作人体系 / Beat 制作 |
| Ambient/Drone | Texture / 空间感 / 声音设计 / 氛围营造 |
| City Pop | 时代背景 / 编曲 / 日本经济泡沫期文化 |
| Indie Folk | 歌词叙事 / 情绪结构 / 原声编曲 |
| Electronic | Groove / Sound Design / Synth / Mixing |
| 华语流行 | 旋律写作 / 歌词文学性 / 经典歌词分析 / 制作水准 / 市场影响 |
| R&B | Groove / 和声复杂度 / Vocal Run / 制作细节 |
| 摇滚 | 吉他编配 / 律动 / 现场能量 / 乐队动态 |

### 调研来源(优先级)

1. **官方**:Apple Music、唱片公司资料、官方采访、MV
2. **数据库**:Discogs、Genius、RateYourMusic、WhoSampled
3. **媒体**:Pitchfork、Rolling Stone、NME、The Fader
4. **社区**:Reddit、YouTube 评论、豆瓣音乐、音乐论坛

## Step 3: 生成研究笔记

输出像**乐评人/音乐制作人/Digging DJ/文化评论者**写的研究笔记,而不是 AI 百科摘要。

### 输出原则

- **长短不一,自由结构**,自然分段,有重点偏移
- 某部分特别值得分析 → 深入展开
- 某部分信息很少 → 不要硬编
- 信息密度高,有洞察,有专业性
- 有历史视角、制作视角、文化视角

### 必须回答的问题(根据情况选择)

- 这首歌为什么成立?
- 为什么它会打动人?
- 为什么它容易被循环播放?
- 它真正独特的地方是什么?
- 它属于哪条音乐演化链?
- 它为什么不是「普通好听」?

### 禁止

- 空泛夸奖(「氛围感」「高级」「空灵」「很 Chill」)
- AI 式抒情
- 套话
- 重复百科
- 整段歌词复制(只选 2-4 句经典歌词)
- 在正文中重复写基本信息(歌曲名、艺人、专辑、发行日期、作词/作曲、流派、语言等)- 这些已写入页面属性

### 特别关注(如果存在)

- Sample / 经典 Live / Remix / Demo / 制作幕后
- DAW / 合成器 / 鼓机
- 社区经典讨论
- 争议(列出不同说法)
- 无法确认的信息(明确标注)

### 笔记格式模板(仅供参考,不必严格遵循)

#### 单曲模板

> ⚠️ **重要:正文中不要重复写基本信息**(歌曲名、艺人、专辑、发行日期、作词/作曲、流派、语言等)。这些信息已经写入页面属性,正文只写研究内容。

```markdown
## 📝 创作背景
(如果值得写)

## 🎛️ 制作与编曲分析
(根据歌曲类型选择重点方向深入)

## 🌍 文化与历史意义
(如果值得写)

## 💬 社区讨论与评价
(如果有经典讨论或乐评)

## 🎯 为什么成立
(总结这首歌为什么独特、为什么打动人)

## 📜 经典歌词
(2-4 句最经典/最有代表性的歌词)

---
(外部链接:Apple Music、网易云等)
```

#### 专辑模板

> ⚠️ **重要:正文中不要重复写基本信息**(专辑名、艺人、发行日期、流派等)。这些信息已经写入页面属性。

```markdown
## 📝 专辑概述
(专辑概念、整体风格定位)

## 🎛️ 制作与曲目分析
(制作过程、曲目编排、代表曲目分析)

## 🌍 文化与商业影响
(销量、奖项、行业影响)

## 🎯 历史地位
(在艺人作品序列中的位置、对后续音乐的影响)

---
(曲目列表)

(外部链接:Apple Music、网易云等)
```

#### 歌手模板

> ⚠️ **重要:正文中不要重复写基本信息**(歌手名、出生地、出道年份等)。这些信息已经写入页面属性。

```markdown
## 📝 音乐生涯概述
(出道历程、重要转折点)

## 🎛️ 音乐风格与创作特点
(风格演变、创作能力、代表作品分析)

## 🌍 商业成就与文化影响
(销量、巡演、行业地位)

## 🎯 历史地位
(对华语流行音乐的贡献、影响力)

---
(代表作品列表)

(外部链接:Apple Music、网易云、官网等)
```

## Step 4: 写入 Notion

### 4.1 搜索并下载封面

**优先使用互联网搜索获取真实专辑/单曲封面图**，而非生成图片。流程：

```bash
# 步骤 1：搜索封面图
web_search "<歌曲名/专辑名> <艺人名> cover album art"

# 步骤 2：从搜索结果中提取封面图 URL（优先 Apple Music / Spotify / 豆瓣音乐 的封面）
# 常见封面来源：
#   - Apple Music: https://is1-ssl.mzstatic.com/image/thumb/Music.../cover.jpg
#   - Spotify: https://i.scdn.co/image/ab67616d0000b273...
#   - 豆瓣音乐: https://img9.doubanio.com/view/.../cover.jpg
#   - QQ音乐/网易云等

# 步骤 3：下载封面到本地（curl 获取原始图片）
curl -sL "<封面图URL>" -o /tmp/cover-<slug>.jpg

# 步骤 4：检查文件有效性（确保是真实图片且大小合理）
file /tmp/cover-<slug>.jpg   # 应显示 JPEG/PNG image data
ls -la /tmp/cover-<slug>.jpg # 应 > 10KB

# 如果下载失败或文件无效，使用 opencli gemini image 作为备用方案：
~/.npm-global/bin/opencli gemini image "<提示词>" --rt 16:9 --op /tmp
```

**封面来源优先级**：
1. Apple Music 原始封面（最高质量）
2. Spotify 专辑封面
3. 豆瓣音乐封面
4. 其他音乐平台封面
5. 备用：opencli gemini image 生成

### 4.2 封面上传（Notion Files API）

**所有封面图片必须通过 Notion Files API 上传到 Notion 托管存储**，禁止使用 external URL 或 R2 链接作为 Notion 图片来源。

```bash
NOTION_KEY=$(cat ~/.config/notion/api_key)
COVER_PATH="/tmp/cover-<slug>.jpg"  # 或 .png，根据实际文件类型
COVER_NAME="cover-<slug>.jpg"

# 步骤 1：创建上传对象
FILE_ID=$(curl -s -X POST "https://api.notion.com/v1/file_uploads" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d "{\"filename\": \"$COVER_NAME\", \"content_type\": \"image/jpeg\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# 步骤 2：上传文件（HTTP 200 即表示上传成功）
curl -s -X POST "https://api.notion.com/v1/file_uploads/$FILE_ID/send" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -F "file=@$COVER_PATH;filename=$COVER_NAME" > /dev/null

# 步骤 3：获取封面 URL
COVER_URL=$(curl -s "https://api.notion.com/v1/file_uploads/$FILE_ID" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('url', ''))")

echo "Cover URL: $COVER_URL"
```

- **API 版本**：必须使用 `Notion-Version: 2025-09-03`（文件上传专属版本）
- **单文件限制**：5MB
- 上传成功后查询 file_upload 对象获取 `url`，用于后续设置页面 cover
- 如果 URL 为空，可等待几秒后重试查询
- **MIME 类型匹配**：上传前用 `file --mime-type` 检测真实类型，`content_type` 字段必须匹配（.jpg → image/jpeg, .png → image/png）

### 4.3 创建页面(带 icon + cover)

根据类型创建不同属性的页面:

#### 单曲页面

```bash
NOTION_KEY=$(cat ~/.config/notion/api_key)
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "3550f06d1a7f800ea4adf722d176a2e0"},
    "icon": {"type": "emoji", "emoji": "🎵"},
    "cover": {"type": "file_upload", "file_upload": {"id": "<Notion Files API 返回的 FILE_ID>"}},
    "properties": {
      "名称": {"title": [{"text": {"content": "<歌曲名>"}}]},
      "类型": {"select": {"name": "单曲"}},
      "原唱": {"rich_text": [{"text": {"content": "<艺人名>"}}]},
      "🏷️ 作词人": {"rich_text": [{"text": {"content": "<作词人>"}}]},
      "🎼 作曲人": {"rich_text": [{"text": {"content": "<作曲人>"}}]},
      "📀 专辑": {"rich_text": [{"text": {"content": "<专辑名>"}}]},
      "📝 语言": {"select": {"name": "<中文|英文|日文|韩文|其他>"}},
      "发行时间": {"date": {"start": "<YYYY-MM-DD>"}},
      "网易云链接": {"url": "<https://music.163.com/song?id=xxx>"},
      "🎵 流派/曲风": {"multi_select": [{"name": "<流派1>"}, {"name": "<流派2>"}]}
    }
  }'
```

#### 专辑页面

```bash
NOTION_KEY=$(cat ~/.config/notion/api_key)
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "3550f06d1a7f800ea4adf722d176a2e0"},
    "icon": {"type": "emoji", "emoji": "💿"},
    "cover": {"type": "file_upload", "file_upload": {"id": "<Notion Files API 返回的 FILE_ID>"}},
    "properties": {
      "名称": {"title": [{"text": {"content": "<专辑名>"}}]},
      "类型": {"select": {"name": "专辑"}},
      "原唱": {"rich_text": [{"text": {"content": "<歌手名>"}}]},
      "🎵 流派/曲风": {"multi_select": [{"name": "<流派1>"}, {"name": "<流派2>"}]},
      "发行时间": {"date": {"start": "<YYYY-MM-DD>"}}
    }
  }'
```

#### 歌手页面

```bash
NOTION_KEY=$(cat ~/.config/notion/api_key)
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "3550f06d1a7f800ea4adf722d176a2e0"},
    "icon": {"type": "emoji", "emoji": "🎤"},
    "cover": {"type": "file_upload", "file_upload": {"id": "<Notion Files API 返回的 FILE_ID>"}},
    "properties": {
      "名称": {"title": [{"text": {"content": "<歌手名>"}}]},
      "类型": {"select": {"name": "歌手"}},
      "🎵 流派/曲风": {"multi_select": [{"name": "<流派1>"}, {"name": "<流派2>"}]}
    }
  }'
```

> ⚠️ **注意**：创建页面时直接使用 Notion Files API 返回的 `FILE_ID`，不要先查询 URL 再用 external 类型。`file_upload` 类型的 cover 字段只需要 `{"id": "<file_id>"}`。

**Icon 选择指南(emoji 优先):**

**按类型选择 icon**:
| 类型 | 推荐 icon |
|------|----------|
| 单曲 | 🎵 🎶 🎧 |
| 专辑 | 💿 📀 🎼 |
| 歌手 | 🎤 🎹 🎸 |

**按流派选择 icon(单曲)**:
| 流派/风格 | 推荐 icon |
|-----------|----------|
| 流行 | 🎵 🎶 |
| 摇滚 | 🎸 🔥 |
| 民谣 | 🎸 🌿 |
| R&B | 🎤 💜 |
| 嘻哈 | 🎤 🔊 |
| 电子 | 🎛️ ⚡ |
| 抒情 | 🎹 💫 |
| 中国风 | 🏮 🎋 |
| 古典 | 🎻 🎼 |
| 爵士 | 🎷 🌙 |

如果歌曲有特定意象(如海洋、星空、城市),也可选择对应 emoji。

### 4.3 添加正文内容

> 正文只写研究内容。基本信息已在页面属性中设置,**不要重复写入正文**。
> 根据页面类型(单曲/专辑/歌手),正文内容侧重不同:
> - **单曲**:创作背景、编曲分析、文化意义、为什么成立、经典歌词
> - **专辑**:专辑概述、曲目分析、制作过程、历史地位
> - **歌手**:音乐生涯、风格特点、代表作品、历史地位

将研究笔记内容转换为 Notion blocks,用 `PATCH /v1/blocks/{page_id}/children` 添加:

- 标题 → `heading_1`, `heading_2`
- 段落 → `paragraph`
- 列表项 → `bulleted_list_item`
- 引用 → `quote`
- 分割线 → `divider`
- 加粗 → `"annotations": {"bold": true}`
- 代码 → `"annotations": {"code": true}`

每批不超过 100 个 blocks,Rate limit ~3 req/s,批量间 `sleep 0.4`。

### 经典歌词写入 Notion

单曲页面正文末尾(研究内容之后、分割线之前),添加经典歌词区块:

```python
# 经典歌词区块: 使用 heading_2 + quote blocks
# 每句歌词一个独立的 quote block,保持简洁
{
    "object": "block",
    "type": "heading_2",
    "heading_2": {
        "rich_text": [{"type": "text", "text": {"content": "📜 经典歌词"}}]
    }
},
{
    "object": "block",
    "type": "quote",
    "quote": {
        "rich_text": [{"type": "text", "text": {"content": "歌词第一句"}}]
    }
},
{
    "object": "block",
    "type": "quote",
    "quote": {
        "rich_text": [{"type": "text", "text": {"content": "歌词第二句"}}]
    }
}
```

⚠️ 只选 2-4 句最经典的歌词,每句一个 `quote` block,不要整段粘贴。

## 错误处理

| 问题 | 处理 |
|------|------|
| 歌曲/专辑/歌手无法识别 | 告知用户,请提供更准确的信息 |
| 部分信息缺失 | 标记「无法确认」,不要编造 |
| 有多个同名内容 | 列出可能的选项让用户确认 |
| Notion API 429 | 等待后重试 |
| 网易云链接找不到 | 留空或跳过该字段 |
| 封面生成失败 | 跳过封面生成,页面不设 cover |

## 快速参考

```bash
# 环境变量
NOTION_KEY=$(cat ~/.config/notion/api_key)

# Notion API
NOTION_API="https://api.notion.com/v1"
NOTION_VERSION="2022-06-28"  # 页面/数据库操作
NOTION_FILES_VERSION="2025-09-03"  # 文件上传专属版本

# 数据库
音乐 databaseId: 3550f06d1a7f800ea4adf722d176a2e0
音乐 data_source_id: 3550f06d-1a7f-80df-bb22-000b73a97e67

# Notion Files API(音乐封面上传)
FILES_API_URL="https://api.notion.com/v1/file_uploads"

# 封面生成
~/.npm-global/bin/opencli gemini image "<prompt>" --rt 16:9 --op /tmp

# 类型选项
单曲 / 专辑 / 歌手

# 流派选项
民谣 / 嘻哈 / 乡村 / 古典 / R&B / 流行 / 摇滚 / 抒情 / 中国风
```

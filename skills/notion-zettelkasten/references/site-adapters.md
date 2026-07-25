# 网站适配规则

## 通用抓取

优先使用 `opencli web read`（支持 JS 渲染，会同时下载页面图片到本地 `images/` 目录）：

```bash
mkdir -p /tmp/article_<id>
opencli web read --url "<URL>" --output /tmp/article_<id>
# 输出通常在 /tmp/article_<id>/<title>/<title>.md
# 图片在 /tmp/article_<id>/<title>/images/
```

微信公众号、需要登录或重 JS 的站点，统一用 `opencli web read`；curl 直接抓大概率返回验证页。

回退方案：`agent-browser`：

```bash
agent-browser open "<URL>"
agent-browser wait --load networkidle
agent-browser wait 3000
agent-browser get text body --json
```

## X/Twitter 特殊处理

统一使用 `opencli twitter` 系列，不要额外包 `timeout`（部分环境没有该命令，会导致整条命令失败）。

### 1. 抓取文本
```bash
opencli twitter article "<X URL>" -f json > /tmp/x_<id>.json
```
- 普通推文 / 线程在 `content` 字段（Markdown）
- X Article 含标题 + 完整正文
- 失败时回退 fxtwitter API：
  ```bash
  curl -sL "https://api.fxtwitter.com/<username>/status/<tweet_id>" -o /tmp/fx_<id>.json
  ```
  - 普通推文正文在 `.tweet.text`
  - X Article 正文在 `.tweet.article.content.blocks[]`

### 2. 下载图片/附件
```bash
opencli twitter download --tweet-url "<X URL>" -f json --output /tmp/x_dl_<id>
```
- 文件保存在 `/tmp/x_dl_<id>/tweets/` 目录
- 命名：`tweet_1.jpg`, `tweet_2.png`...
- 需要 opencli 已配置 Twitter 登录态

**如果 opencli download 不可用或未登录**：用 fxtwitter API 取媒体 URL：
- 普通推文媒体：`.tweet.media.all[].url`
- X Article 媒体：`.tweet.article.media_entities[].media_info.original_img_url`
- 这些 URL 来自 `pbs.twimg.com`，本地可能不可达，直接在 Notion 中使用 `external` image block

### 3. 写入页面
- 第一张图片作封面（`external` URL）
- 剩余图片按原文顺序插入正文（`external` image block）
- X Article 可通过 `atomic` block + `entityMap` 精确还原图片位置（详见 `references/site-adapters.md` 或 SKILL.md 功能 12）

## 少数派（sspai）

需要浏览器渲染 + Referer 防盗链：
```bash
curl -sL -H "Referer: https://sspai.com/" -o /tmp/sspai_<id>/img01.jpeg "<image_url>"
```

## 知乎

需要浏览器渲染，图片需带 Referer 头下载。

## 微信公众号（mp.weixin.qq.com）

微信公众号文章需要**浏览器渲染**，且图片有防盗链，需要专门处理：

### 1. 抓取 HTML（统一用 opencli web）

微信公众号对 curl 做了限制：直接 curl 经常返回验证页或只有少量内容，**必须先用浏览器渲染后再抓取**。

**统一使用 `opencli web read`**：

```bash
mkdir -p /tmp/wechat_<id>
opencli web read --url "<WECHAT_URL>" --output /tmp/wechat_<id>
# 输出：/tmp/wechat_<id>/<title>/<title>.md
# 图片：/tmp/wechat_<id>/<title>/images/
```

- 返回 Markdown 文件，正文已按原始段落结构保留
- 图片已下载到本地 `images/` 目录，可直接上传 Notion Files API
- 如需原始 HTML（例如要精确提取 `data-src` 或 `#js_content` 结构），回退 `agent-browser`

**备用：`agent-browser`**（仅在 `opencli web read` 失败或不可用时使用）：

```bash
agent-browser open "<WECHAT_URL>"
agent-browser wait 3000
agent-browser get html body --json > /tmp/wechat_<id>_raw.json
```

然后提取 `data.html` 字段保存为 HTML 文件：

```python
import json
with open('/tmp/wechat_<id>_raw.json') as f:
    d = json.load(f)
html = d['data']['html']
with open('/tmp/wechat_<id>.html', 'w') as f:
    f.write(html)
```

**curl 仅作最后尝试**：少数情况下 curl 能直接拿到内容，但大部分文章会被微信拦截，不建议依赖。

### 2. 解析结构

拿到 HTML 后：
- 标题优先取 `h1.rich_media_title`， fallback 到 `h2.rich_media_title`
- 正文从 `#js_content` 提取
- 图片 URL 在 `<img data-src="...">`（不在 `src`）
- 每个 `data-src` 必须保留完整 URL（含 `?wx_fmt=...&from=appmsg`），否则下载失败
- 文本按原始顺序逐个输出为 paragraph，**不要过度合并相邻短段落**，避免结构丢失
- 第一个图片通常作为封面，其余按原文顺序插入正文

解析示例见 `references/scripts/wechat-parser.py`。

### 3. 下载图片

微信公众号图片必须带 `Referer` 头，否则返回空：

```bash
curl -sL --max-time 15 \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  -H "Referer: <WECHAT_URL>" \
  "<IMAGE_URL_WITH_QUERY>" -o /tmp/wechat_<id>/img_00.png
```

### 4. 上传到 Notion

微信图片不能直接用 `external` URL（Notion 无法通过防盗链），必须：
1. 本地下载
2. 通过 Notion Files API 上传为 `file_upload`
3. 在 children blocks 中使用 `file_upload` 类型 image

### 5. 常见失败与处理

| 现象 | 原因 | 处理 |
|------|------|------|
| curl 返回验证页 / 内容极少 | 微信反爬 | 统一用 `opencli web read` 渲染，失败时回退 `agent-browser` |
| 标题为空 | 只匹配了 `h2` 而实际在 `h1` | 同时尝试 `h1.rich_media_title` 和 `h2.rich_media_title` |
| 图片下载为空 | URL 被截断或缺少 Referer | 使用完整 `data-src` + `Referer: <文章URL>` |
| 正文结构丢失 | 过度合并段落 | 每个文本节点独立成段，只合并同一段内的连续短句 |
| children 过多 | 微信长文图片多 | 超过 100 blocks 时优先保留文字，按比例丢弃尾部图片 |

## 页面抓取失败处理

1. `web_fetch` 对 JS 渲染页面无效 → 用 `opencli web read` 或 `agent-browser`
2. 微信公众号、少数派、知乎等需要浏览器渲染
3. 等待 `networkidle` 后再抓取

## X 抓取失败处理

1. 优先 `opencli twitter article`
2. 备用 `opencli twitter download` 下载图片
3. 如果 opencli 未登录 → 回退 fxtwitter API（仅文本）
4. X Article 内嵌图片需 browser 登录态

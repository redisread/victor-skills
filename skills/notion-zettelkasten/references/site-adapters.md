# 网站适配规则

## 通用抓取

优先使用 `opencli web`（支持 JS 渲染）：

```bash
opencli web article "<URL>" -f json > /tmp/article_<id>.json
```

回退方案：`agent-browser`：

```bash
agent-browser open "<URL>"
agent-browser wait --load networkidle
agent-browser wait 3000
agent-browser get text body --json
```

## X/Twitter 特殊处理

统一使用 `opencli twitter` 系列：

### 1. 抓取文本
```bash
opencli twitter article "<X URL>" -f json > /tmp/x_<id>.json
```
- 普通推文在 `content` 字段（Markdown）
- X Article 含标题 + 完整正文

### 2. 下载图片/附件
```bash
opencli twitter download --tweet-url "<X URL>" -f json --output /tmp/x_dl_<id>
```
- 文件保存在 `/tmp/x_dl_<id>/tweets/` 目录
- 命名：`tweet_1.jpg`, `tweet_2.png`...
- 需要 opencli 已配置 Twitter 登录态

### 3. 上传图片到 Notion
使用 Python 脚本批量上传（详见 [references/image-upload.md](image-upload.md)）

### 4. 写入页面
- 第一张图片作封面
- 剩余图片用 `after` 参数插入正文

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

**统一使用 `opencli web`**：

```bash
opencli web article "<WECHAT_URL>" -f json > /tmp/wechat_<id>.json
```

- 返回的 JSON 中，正文通常在 `.content`（Markdown/HTML）或 `.html`
- 如需原始 HTML，优先从 `.html` 字段读取；没有时再用 `.content` 反推

**备用：`agent-browser`**（仅在 `opencli web` 失败或不可用时使用）：

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
| curl 返回验证页 / 内容极少 | 微信反爬 | 统一用 `opencli web` 渲染，失败时回退 `agent-browser` |
| 标题为空 | 只匹配了 `h2` 而实际在 `h1` | 同时尝试 `h1.rich_media_title` 和 `h2.rich_media_title` |
| 图片下载为空 | URL 被截断或缺少 Referer | 使用完整 `data-src` + `Referer: <文章URL>` |
| 正文结构丢失 | 过度合并段落 | 每个文本节点独立成段，只合并同一段内的连续短句 |
| children 过多 | 微信长文图片多 | 超过 100 blocks 时优先保留文字，按比例丢弃尾部图片 |

## 页面抓取失败处理

1. `web_fetch` 对 JS 渲染页面无效 → 用 `agent-browser`
2. 少数派、知乎等需要浏览器渲染
3. 等待 `networkidle` 后再抓取

## X 抓取失败处理

1. 优先 `opencli twitter article`
2. 备用 `opencli twitter download` 下载图片
3. 如果 opencli 未登录 → 回退 fxtwitter API（仅文本）
4. X Article 内嵌图片需 browser 登录态

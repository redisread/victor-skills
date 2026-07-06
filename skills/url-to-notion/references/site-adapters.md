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

## 页面抓取失败处理

1. `web_fetch` 对 JS 渲染页面无效 → 用 `agent-browser`
2. 少数派、知乎等需要浏览器渲染
3. 等待 `networkidle` 后再抓取

## X 抓取失败处理

1. 优先 `opencli twitter article`
2. 备用 `opencli twitter download` 下载图片
3. 如果 opencli 未登录 → 回退 fxtwitter API（仅文本）
4. X Article 内嵌图片需 browser 登录态

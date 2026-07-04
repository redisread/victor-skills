---
name: url-to-notion
description: 根据 URL 抓取文章全文，裁剪后保存到 Notion「整理笔记」数据库。自动处理 JS 渲染页面（少数派等），使用 Notion Files API 直接上传图片（无需外部图床），生成标签和摘要。触发词：保存文章到 Notion、裁剪文章、保存到整理笔记、url-to-notion。
version: 1.1.0
metadata:
  homepage: https://github.com/victor-skills#url-to-notion
---

# URL to Notion

抓取文章全文，裁剪精华内容，保存到 Notion「整理笔记」数据库。

## 核心流程

```
抓取内容 → 提取图片 → 下载图片 → 上传到 Notion → 创建页面 → 添加正文
```

## 数据库信息

| 名称 | 值 |
|------|-----|
| 整理笔记 database_id | `05c87b65-e76b-4789-a38c-5c84809d300f` |
| 整理笔记 data_source_id | `d42aae33-7fc9-4fa5-9b57-7c30d6c7d1b3` |

## Step 1: 抓取内容

按网站类型选择抓取方式（详见 [references/site-adapters.md](references/site-adapters.md)）：
- **通用**：`opencli web article` → 回退 `agent-browser`
- **X/Twitter**：`opencli twitter article` + `opencli twitter download`
- **少数派/知乎**：需浏览器渲染 + Referer 防盗链

## Step 2: 提取与下载图片

从页面提取正文图片 URL，带 Referer 头下载（处理防盗链）。

## Step 3: 上传图片到 Notion

使用 Notion Files API 批量上传（详见 [references/image-upload.md](references/image-upload.md)）：
- 创建上传对象 → 发送文件 → 获取 file_upload ID
- Rate limit ~3 req/s，批量间 `sleep 0.4`

## Step 4: 创建 Notion 页面

1. 创建页面：设置标题、作者、领域、标签、封面
2. 添加正文：Markdown → Notion blocks
3. 插入图片：用 `after` 参数分布到正文中

标签选择规则见 [references/tag-rules.md](references/tag-rules.md)。

## 验证

- [ ] 页面已创建，URL 可访问
- [ ] 标题、作者、标签已设置
- [ ] 正文内容已裁剪（非全文复制）
- [ ] 图片已正确上传和显示

## 返回结果

```
✅ 已保存到 Notion 整理笔记
- **标题**：{标题}
- **作者**：{作者}
- **领域**：{领域}
- **标签**：{标签}
- **页面**：{page_url}
```

## 快速参考

```bash
NOTION_KEY=$(cat ~/.config/notion/api_key)
FILES_API_URL="https://api.notion.com/v1/file_uploads"
FILES_API_VERSION="2025-09-03"
```

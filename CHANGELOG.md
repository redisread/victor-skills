# Changelog

本文件记录 victor-skills 项目所有技能和 Agent 的版本变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/)，版本号遵循 [SemVer](https://semver.org/)。

---

## Skills

### article-images-gen

#### [1.0.5] - 2026-05-06
- 更新插图密度选择提示

#### [1.0.4] - 早期版本
- 初始版本，支持 Gemini / Grok / ChatGPT 图片生成

---

### blog-push

#### [1.1.0] - 2026-06-20
- 技能库整理：拆分 references 文档，精简主 SKILL.md

#### [1.0.0] - 早期版本
- 初始版本，支持 posts/daily/weekly 三种内容类型发布

---

### hackernews-digest

#### [1.1.0] - 2026-06-20
- 技能库整理：优化 SKILL.md 结构
- CR 修复：移除假 hash、统一 API 版本、修复搜索边界

#### [1.0.0] - 早期版本
- 初始版本，获取 HN Top 10 并生成摘要

---

### music-notes

#### [1.1.0] - 2026-06-20
- 技能库整理：拆分 references（notion-api.md、research-dimensions.md）
- 新增 smart-search 流程

#### [1.0.0] - 早期版本
- 初始版本（原名 music-research），后重命名为 music-notes

---

### r2-uploader

#### [1.1.0] - 2026-06-20
- 技能库整理：优化 SKILL.md 结构
- CR 修复：统一 API 版本

#### [1.0.0] - 早期版本
- 初始版本，支持单文件/远程 URL/批量上传到 Cloudflare R2

---

### tool-save-to-notion

#### [1.1.0] - 2026-06-20
- 技能库整理：拆分 references（extraction-rules.md、icon-guide.md、notion-api.md）
- 修复 YAML frontmatter 解析错误

#### [1.0.0] - 早期版本
- 初始版本，自动提取工具信息并保存到 Notion 工具箱

---

### tool-share

#### [1.1.0] - 2026-06-20
- 技能库整理：新增 references/article-template.md

#### [1.0.0] - 早期版本
- 初始版本，调研工具信息并生成分享文章

---

### url-to-notion

#### [1.1.0] - 2026-06-20
- 技能库整理：拆分 references（image-upload.md、site-adapters.md、tag-rules.md）
- CR 修复：统一 API 版本

#### [1.0.0] - 早期版本
- 初始版本，抓取 URL 文章内容并裁剪保存到 Notion

---

## Agents

### para-notes-agent

#### [1.0.0] - 2026-07-06
- 初始版本，基于 Apple Notes 的 PARA 笔记管理
- 模型升级为 sonnet（原 qwen3.6-plus）
- 补齐 version 和 metadata 字段

---

### quality-info-reviewer

#### [1.2.0] - 2026-07-06
- 输出格式新增「内容摘要」段（150-300 字）

#### [1.1.0] - 早期版本
- 新增 Twitter/X 递归加载被引用推文逻辑

#### [1.0.0] - 早期版本
- 初始版本，10 条标准信息质量评估

---

### weekly-tool-digest-agent

#### [1.1.0] - 2026-07-06
- 初始版本，查询 Notion 工具箱数据库生成周报

---

## 已废弃/移除的技能

以下技能已从项目中移除（2026-06-20 技能库整理）：

- `bloomscroll-style-writer` — 滚动风格写作
- `jike-digest` — 即刻内容摘要
- `reddit-daily-digest` — Reddit 每日摘要
- `reddit-digest` — Reddit 摘要（被 hackernews-digest 替代）
- `x-following-digest` — Twitter/X 关注摘要

### notion-zettelkasten

#### [1.1.6] - 2026-07-25
- 优化 X/Twitter 保存流程：明确优先用 `opencli twitter article` + `opencli twitter download`，移除失效的 `timeout` 包装
- 补充 X/Twitter 图片处理：opencli 下载的媒体用 `file_upload`，fxtwitter 返回的 `pbs.twimg.com` URL 用 `external`
- 完善 X/Twitter 回退路径：普通推文用 `.tweet.text`/`.tweet.media`，X Article 用 `.tweet.article.*`
- 微信公众号抓取统一改为 `opencli web read --url ... --output ...`，移除无效的 `opencli web article` 命令，明确输出 Markdown 与本地 `images/` 目录

#### [1.1.5] - 2026-07-25
- 功能 13（URL 保存到工具箱）新增大页面/入口型站点摘要规则，提取核心功能点与适用场景，不再硬编码具体站点类型
- 功能 12（URL 保存到文献笔记）内联 Markdown 格式必须转成 Notion `rich_text`：`[文字](URL)` → 可点击链接，`**加粗**` → bold，`*斜体*` → italic
- 通用网站抓取统一优先使用 `opencli web read`（支持 JS 渲染、自动下载图片），微信公众号等强反爬站点不再依赖裸 `curl`
- 清理 Codewiki 相关描述：Codewiki 不再作为通用分类或站点类型出现在工具箱提取与适配规则中

#### [1.1.4] - 2026-07-22
- 功能 12（URL 保存到文献笔记）优化图片插入位置：优先按原始结构穿插，无精确位置时按段落均匀分布
- 新增 X Article（fxtwitter）精确位置解析：通过 `atomic` block + `entityMap` 中的 `MEDIA` 实体定位图片
- 认证指引补充：默认从 `~/.config/notion/env.sh` 加载 `NOTION_API_TOKEN`

#### [1.1.0] - 2026-07-06
- 合并 url-to-notion 和 tool-save-to-notion 触发词，统一由 notion-zettelkasten 管理

---

### user-experience-design

#### [1.0.0] - 2026-07-19
- 初始版本，收录自 Steven 的用户体验设计方法框架
- 基于《体验经济》8 条核心思想：体验式营销、CEM、数字化、定制化、顾客损失、记忆点、游戏化、主题化
- 输出结构：体验目标 → 顾客损失清单 → 主题构思 → 记忆点/定制化 → 落地清单

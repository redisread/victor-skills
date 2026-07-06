# Notion Zettelkasten Database Schemas

> Auto-generated: 2026-07-06

## Database IDs

| Name | ID |
|------|-----|
| 文献笔记 | `05c87b65-e76b-4789-a38c-5c84809d300f` |
| 工具箱 | `6f7bb9cc-ac01-41c5-9856-fb1568d197ae` |
| 领域 | `ac9e08fc-67f9-423f-a141-49ac44be6bf2` |
| 永久笔记 | `1bf7d20f-9d37-48a6-bb18-78e3513698f5` |
| 灵感笔记 | `22b9457a-b762-4c74-a41e-7be43ad0aa52` |

---

## 1. 文献笔记

**ID:** `05c87b65-e76b-4789-a38c-5c84809d300f`
**Description:** 外部内容摘录：网页、文章、书籍、视频等。知识管理的输入端。

### Properties

| Name | ID | Type | Details |
|------|-----|------|---------|
| Name | `title` | title | 文献标题 |
| URL | `%3CgI~` | url | 原文链接 |
| 总结 | `Z%3Fd_` | rich_text | 内容摘要 |
| 为什么收集此笔记 | `WE%7Ci` | rich_text | 收集原因 |
| 状态 | `%3DQlu` | status | 处理状态 |
| 是否需要review | `%3EjzV` | checkbox | 标记是否需要回顾 |
| 文献类型 | `%40TKk` | select | 文章/书籍/视频等 |
| 标签 | `ZtNX` | multi_select | 分类标签 |
| 🚩 领域 | `nsmb` | relation | → 领域 (`ac9e08fc`) |
| 关联永久笔记 | `%3B%60ZW` | relation | → 永久笔记 (`1bf7d20f`) |
| 关联文献笔记 | `%5BCO%7B` | relation | → 自身（同库自关联） |
| 关联项目 | `%3Ekn%7C` | relation | → 项目看板 (`ace1543c`) |
| 卡片完成时间 | `Ef%3Af` | date | 完成提炼的时间 |
| 创建时间 | `q%3AIC` | created_time | 自动记录 |
| 更新时间 | `XjaJ` | last_edited_time | 自动记录 |

### 状态选项

| 名称 | ID | Color | Group |
|------|-----|-------|-------|
| 未开始 | `0b343f85-0690-4ca4-8aaf-b82aa5d7619c` | default | To-do |
| 处理中 | `fe82c0df-285a-4727-b857-fc59003f49b2` | blue | In progress |
| 完成 | `636fd67a-6ed3-4480-80c7-30b4dceaf316` | green | Complete |
| 归档 | `uUuw` | orange | Complete |

### 文献类型选项

| 名称 | ID | Color |
|------|-----|-------|
| 文章 | `ko~` | yellow |
| 书籍 | `` `dQS `` | brown |
| 笔记 | `7fc4d5a8-8bc9-46f0-85b4-3bca4583136a` | gray |
| 视频 | `;uRi` | pink |
| 想法 | `251a4ece-af73-40a4-a134-0243aeacc89d` | purple |
| 音频 | `XTZW` | blue |
| 工具调研 | `030cbb0f-a682-46d7-9105-2eaa7313f06b` | default |
| openclaw摘要 | `7ec687ae-8c18-4cc7-89da-195716da0a96` | green |

### 标签选项（部分常用）

AI, 知识管理, 最佳实践, 博客, 生产力, 美团, 大模型, 方法论, 笔记, 仓储, 开发, 卡片盒笔记法, Apple, 生活, Notion, 商业模式, Java, 投资, 旅行, 资讯, web3, 产品, CloudFlare, Redis, 推荐系统, 设计思想, 管理, MySQL, SpringBoot, 极简主义, JVM, ChatGPT, 效率, Agent, Claude, 架构, 写作, Claude Code, 提示词工程, 第二大脑, Vibe Coding ...

---

## 2. 灵感笔记

**ID:** `22b9457a-b762-4c74-a41e-7be43ad0aa52`
**Description:** 个人思考、灵感、突发想法。成熟后可转化为永久笔记。

### Properties

| Name | ID | Type | Details |
|------|-----|------|---------|
| Name | `title` | title | 灵感标题 |
| 总结 | `JB%7BP` | rich_text | 简要描述 |
| 状态 | `iDCr` | status | 处理状态 |
| 标签 | `t%5DQ%60` | multi_select | 分类标签 |
| 🚩 领域 | `zYF%3A` | relation | → 领域 (`ac9e08fc`) |
| 关联笔记 | `DQ_W` | relation | → 文献笔记 (`05c87b65`) |
| 转化为 | `BLFt` | relation | → 永久笔记 (`1bf7d20f`) |
| 创建时间 | `ujr%5D` | created_time | 自动记录 |
| 更新时间 | `%3FcYz` | last_edited_time | 自动记录 |

### 状态选项

| 名称 | ID | Color |
|------|-----|-------|
| 草稿 | `91fd0ca3-0a41-4c9f-b1fe-e758db52be44` | gray |
| 发展中 | `54f6328a-207d-4f73-aaf3-91cb32e9cabc` | blue |
| 待转化 | `965d3767-cc79-4656-8577-95c811889129` | yellow |
| 已转化 | `38d5d240-9770-4686-ac37-76218bddf017` | green |

### 标签选项（部分常用）

AI, 知识管理, LLM, 第二大脑, AI编程, 最佳实践, 工作流, 代码审查, 效率工具, Notion, 投资, 金融, Agent, 商业模式, 产品设计, 写作, 方法论, Claude, AI辅助编程, 自我提升, 开发工具, Claude Code, 软件工程, 大模型 ...

---

## 3. 永久笔记

**ID:** `1bf7d20f-9d37-48a6-bb18-78e3513698f5`
**Description:** 经过深度加工、具有长期复用价值的知识单元。

### Properties

| Name | ID | Type | Details |
|------|-----|------|---------|
| Name | `title` | title | 笔记标题 |
| 总结 | `Z%3Fd_` | rich_text | 核心观点 |
| 状态 | `%3DQlu` | status | 处理状态 |
| 标签 | `ZtNX` | multi_select | 分类标签 |
| 🚩 领域 | `Aot%7D` | relation | → 领域 (`ac9e08fc`) |
| 关联永久笔记 | `XvYq` | relation | → 自身（双向链接） |
| 关联文献笔记 | `frlr` | relation | → 文献笔记 (`05c87b65`) |
| 关联灵感笔记 | `pUwr` | relation | → 灵感笔记 |
| 关联项目 | `` `pR%7C `` | relation | → 项目看板 (`ace1543c`) |
| 创建时间 | `q%3AIC` | created_time | 自动记录 |
| 更新时间 | `XjaJ` | last_edited_time | 自动记录 |

### 状态选项

| 名称 | ID | Color | Group |
|------|-----|-------|-------|
| 未开始 | `0b343f85-0690-4ca4-8aaf-b82aa5d7619c` | default | To-do |
| 处理中 | `fe82c0df-285a-4727-b857-fc59003f49b2` | blue | In progress |
| 持续更新 | `aLEt` | brown | In progress |
| 归档 | `~|py` | yellow | Complete |
| 完成 | `636fd67a-6ed3-4480-80c7-30b4dceaf316` | green | Complete |
| 再次回顾 | `dKW;` | blue | Complete |

---

## 4. 工具箱

**ID:** `6f7bb9cc-ac01-41c5-9856-fb1568d197ae`
**Description:** 所有工具收集地。

### Properties

| Name | ID | Type | Details |
|------|-----|------|---------|
| Name | `title` | title | 工具名称 |
| URL | `_%7C%3C` | url | 工具链接 |
| 简介 | `uJ%5D%7D` | rich_text | 工具描述 |
| 类型单选 | `%3B~np` | select | 工具分类 |
| 类型 | `%3CHOu` | multi_select | 工具分类（多选） |
| 标签 | `HT%5Ef` | multi_select | 分类标签 |
| ⭐ 置顶 | `R%7BwI` | checkbox | 是否置顶 |
| 创建时间 | `tyHb` | created_time | 自动记录 |
| 更新时间 | `Ha@q` | last_edited_time | 自动记录 |

### 类型单选选项

| 名称 | ID | Color |
|------|-----|-------|
| 网站 | `75a9cd52-c105-4e25-80e4-1593608844ad` | blue |
| 工具包 | `db5f5a5c-fa5d-4235-b04f-cc4bea518753` | yellow |
| 软件 | `b1ff97de-ede7-4056-906e-4ac13f4329c4` | green |
| 浏览器插件 | `b3691d0f-ff32-4c50-a303-97e0cd09af2f` | red |
| Prompt | `af1b8729-e3bf-46ce-a701-a6f1b8d85362` | purple |

---

## 5. 领域

**ID:** `ac9e08fc-67f9-423f-a141-49ac44be6bf2`
**Description:** 笔记内容下的分类。

### Properties

| Name | ID | Type | Details |
|------|-----|------|---------|
| Name | `title` | title | 领域名称 |
| 简介 | `%5C_pu` | rich_text | 领域描述 |
| 是否归档 | `aXPn` | checkbox | 是否归档 |
| 关联永久笔记 | `%3DC%7B%3A` | relation | → 永久笔记 (`1bf7d20f`) |
| 关联灵感笔记 | `XuEh` | relation | → 灵感笔记 |
| 关联文献笔记 | `%5BQDS` | relation | → 文献笔记 (`05c87b65`) |
| 创建时间 | `yI%5Dj` | created_time | 自动记录 |
| 更新时间 | `eoqH` | last_edited_time | 自动记录 |

---

## Cross-Database Relations

```
文献笔记 ←→ 永久笔记 (关联永久笔记 / 关联文献笔记)
文献笔记 ←→ 领域     (🚩 领域 / 关联文献笔记)
文献笔记 ←→ 项目看板 (关联项目 / 关联文献笔记)
灵感笔记 ←→ 永久笔记 (转化为 / 关联灵感笔记)
灵感笔记 ←→ 文献笔记 (关联笔记)
灵感笔记 ←→ 领域     (🚩 领域 / 关联灵感笔记)
永久笔记 ←→ 领域     (🚩 领域 / 关联永久笔记)
永久笔记 ←→ 项目看板 (关联项目 / 关联永久笔记)
永久笔记 ←→ 永久笔记 (关联永久笔记, 自关联)
```

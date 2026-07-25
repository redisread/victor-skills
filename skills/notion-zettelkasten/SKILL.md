---
name: notion-zettelkasten
description: "Notion 卡片盒笔记系统（Zettelkasten）管理工具。支持查询和创建文献笔记、灵感笔记、永久笔记（含正文），查询/创建/删除工具箱，URL保存工具到工具箱，查询领域，URL保存文章到文献笔记。触发词：文献笔记、灵感笔记、永久笔记、卡片笔记、工具箱、领域查询、记笔记、记灵感、收集文献、保存文章、保存工具、url-to-notion、zettelkasten、保存文章到 Notion、裁剪文章、保存到整理笔记、保存这个工具、添加到工具箱、收藏这个链接、save this tool、add to toolbox。当用户提到 Notion 笔记的查询、创建、删除或 URL 保存时使用。"
version: 1.1.6
metadata:
  homepage: https://github.com/victor-skills#notion-zettelkasten

---

# Notion Zettelkasten 技能

管理 Notion 卡片盒笔记系统的查询和创建操作。通过 Notion REST API（curl + jq）实现。

数据库结构和属性 ID 详见：`references/database-schemas.md`

## 认证

```bash
# 环境变量 NOTION_API_TOKEN 必须已设置
# 默认从 ~/.config/notion/env.sh 加载：
source ~/.config/notion/env.sh

# 如该文件不存在或为空，提示用户设置：
export NOTION_API_TOKEN="ntn_xxx..."
```

通用请求头：

```bash
NOTION_HEADERS=(-H "Authorization: Bearer $NOTION_API_TOKEN" -H "Notion-Version: 2022-06-28" -H "Content-Type: application/json")
```

## 数据库 ID 速查

| 数据库 | ID |
|--------|-----|
| 文献笔记 | `05c87b65-e76b-4789-a38c-5c84809d300f` |
| 灵感笔记 | `22b9457a-b762-4c74-a41e-7be43ad0aa52` |
| 永久笔记 | `1bf7d20f-9d37-48a6-bb18-78e3513698f5` |
| 工具箱 | `6f7bb9cc-ac01-41c5-9856-fb1568d197ae` |
| 领域 | `ac9e08fc-67f9-423f-a141-49ac44be6bf2` |

---

## 功能 1：查询文献笔记（最近1天/1周）

查询最近新建的文献笔记，支持按天或周筛选。

```bash
# 最近1天
curl -s -X POST "https://api.notion.com/v1/databases/05c87b65-e76b-4789-a38c-5c84809d300f/query" \
  "${NOTION_HEADERS[@]}" \
  -d '{
    "filter": {
      "timestamp": "created_time",
      "created_time": {"after": "'$(date -u -v-1d +%Y-%m-%dT%H:%M:%SZ)'"}
    },
    "sorts": [{"timestamp": "created_time", "direction": "descending"}],
    "page_size": 20
  }' | jq '[.results[] | {id, title: .properties.Name.title[0].plain_text, url: .properties.URL.url, status: .properties["状态"].status.name, type: .properties["文献类型"].select.name, created: .properties["创建时间"].created_time, summary: ((.properties["总结"].rich_text // [])[0].plain_text // "无摘要")}]'

# 最近1周（将 -v-1d 改为 -v-7d）
curl -s -X POST "https://api.notion.com/v1/databases/05c87b65-e76b-4789-a38c-5c84809d300f/query" \
  "${NOTION_HEADERS[@]}" \
  -d '{
    "filter": {
      "timestamp": "created_time",
      "created_time": {"after": "'$(date -u -v-7d +%Y-%m-%dT%H:%M:%SZ)'"}
    },
    "sorts": [{"timestamp": "created_time", "direction": "descending"}],
    "page_size": 50
  }' | jq '[.results[] | {id, title: .properties.Name.title[0].plain_text, url: .properties.URL.url, status: .properties["状态"].status.name, type: .properties["文献类型"].select.name, created: .properties["创建时间"].created_time}]'
```

**输出格式：** 表格展示标题、URL、状态、文献类型、创建时间、摘要。

---

## 功能 2：查询灵感笔记（最近1天/1周）

```bash
# 最近1天
curl -s -X POST "https://api.notion.com/v1/databases/22b9457a-b762-4c74-a41e-7be43ad0aa52/query" \
  "${NOTION_HEADERS[@]}" \
  -d '{
    "filter": {
      "timestamp": "created_time",
      "created_time": {"after": "'$(date -u -v-1d +%Y-%m-%dT%H:%M:%SZ)'"}
    },
    "sorts": [{"timestamp": "created_time", "direction": "descending"}],
    "page_size": 20
  }' | jq '[.results[] | {id, title: .properties.Name.title[0].plain_text, status: .properties["状态"].status.name, summary: ((.properties["总结"].rich_text // [])[0].plain_text // "无摘要"), created: .properties["创建时间"].created_time}]'

# 最近1周（将 -v-1d 改为 -v-7d）
```

**输出格式：** 表格展示标题、状态、摘要、创建时间。

---

## 功能 3：随机查询一条笔记（文献/灵感）

从文献笔记或灵感笔记中随机选一条展示。

```bash
# 随机一条文献笔记（用 bash $RANDOM 生成随机索引）
IDX=$((RANDOM % 100))
curl -s -X POST "https://api.notion.com/v1/databases/05c87b65-e76b-4789-a38c-5c84809d300f/query" \
  "${NOTION_HEADERS[@]}" \
  -d '{"page_size": 100}' | jq --argjson idx "$IDX" \
  '[.results[] | {id, title: .properties.Name.title[0].plain_text, url: .properties.URL.url, status: .properties["状态"].status.name, type: .properties["文献类型"].select.name, summary: ((.properties["总结"].rich_text // [])[0].plain_text // "无摘要")}] | .[$idx] // .[0]'

# 随机一条灵感笔记（同理，改数据库 ID 和字段映射）
IDX=$((RANDOM % 100))
curl -s -X POST "https://api.notion.com/v1/databases/22b9457a-b762-4c74-a41e-7be43ad0aa52/query" \
  "${NOTION_HEADERS[@]}" \
  -d '{"page_size": 100}' | jq --argjson idx "$IDX" \
  '[.results[] | {id, title: .properties.Name.title[0].plain_text, status: .properties["状态"].status.name, summary: ((.properties["总结"].rich_text // [])[0].plain_text // "无摘要")}] | .[$idx] // .[0]'
```

**输出格式：** 单条笔记的完整信息（标题、URL/状态、摘要、类型）。

---

## 功能 4：查询工具箱（最近1周新建）

```bash
curl -s -X POST "https://api.notion.com/v1/databases/6f7bb9cc-ac01-41c5-9856-fb1568d197ae/query" \
  "${NOTION_HEADERS[@]}" \
  -d '{
    "filter": {
      "timestamp": "created_time",
      "created_time": {"after": "'$(date -u -v-7d +%Y-%m-%dT%H:%M:%SZ)'"}
    },
    "sorts": [{"timestamp": "created_time", "direction": "descending"}],
    "page_size": 50
  }' | jq '[.results[] | {id, title: .properties.Name.title[0].plain_text, url: .properties.URL.url, type: .properties["类型单选"].select.name, intro: ((.properties["简介"].rich_text // [])[0].plain_text // "无简介"), created: .properties["创建时间"].created_time}]'
```

**输出格式：** 表格展示工具名称、URL、类型、简介、创建时间。

---

## 功能 5：创建文献笔记

创建一篇新的文献笔记（含正文内容）。需要用户提供：标题（必填）、URL、摘要、文献类型、标签、领域。

**⚠️ 正文是核心**：创建笔记时必须包含正文内容（children blocks），不能只创建空页面。

```bash
# 变量说明：
# TITLE - 文献标题（必填）
# URL - 原文链接（可选）
# SUMMARY - 内容摘要（必填，将同时写入属性字段和正文）
# BODY - 正文内容（必填，用户提供的核心笔记内容）
# DOC_TYPE - 文献类型：文章/书籍/笔记/视频/想法/音频/工具调研/openclaw摘要（可选）
# TAGS - 标签数组（可选）
# DOMAIN_ID - 领域ID（可选，先通过功能8查询）

curl -s -X POST "https://api.notion.com/v1/pages" \
  "${NOTION_HEADERS[@]}" \
  -d '{
    "parent": {"database_id": "05c87b65-e76b-4789-a38c-5c84809d300f"},
    "properties": {
      "Name": {"title": [{"text": {"content": "'"$TITLE"'"}}]},
      "URL": {"url": "'"$URL"'"},
      "总结": {"rich_text": [{"text": {"content": "'"$SUMMARY"'"}}]},
      "文献类型": {"select": {"name": "'"$DOC_TYPE"'"'}},
      "状态": {"status": {"name": "未开始"}},
      "标签": {"multi_select": ['"$TAGS"']},
      "🚩 领域": {"relation": [{"id": "'"$DOMAIN_ID"'"}]}
    },
    "children": [
      {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": "📝 摘要"}}]}},
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "'"$SUMMARY"'"}}]}},
      {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": "📖 正文笔记"}}]}},
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "'"$BODY"'"}}]}},
      {"object": "block", "type": "divider", "divider": {}},
      {"object": "block", "type": "callout", "callout": {"rich_text": [{"type": "text", "text": {"content": "来源：'"$URL"'"}}], "icon": {"type": "emoji", "emoji": "🔗"}}}
    ]
  }' | jq '{id, title: .properties.Name.title[0].plain_text, url: .url, created: .created_time}'
```

**正文结构：**
1. `📝 摘要` — 简短概括（来自 SUMMARY）
2. `📖 正文笔记` — 用户提供的核心笔记内容（来自 BODY）
3. 分割线 + `🔗 来源` callout — 标注原文链接

**注意：**
- BODY 是必填的，没有正文的文献笔记没有价值
- 如果正文超过 2000 字符，需要拆分成多个 paragraph block
- 只包含用户提供的字段，可选字段未提供时从请求中移除
- 标签格式：`{"name": "AI"}, {"name": "知识管理"}`

---

## 功能 6：创建灵感笔记

**⚠️ 正文是核心**：创建时必须包含正文内容。

```bash
# 变量说明：
# TITLE - 灵感标题（必填）
# SUMMARY - 简要描述（必填）
# BODY - 详细想法/灵感来源/展开思考（必填）
# TAGS - 标签数组（可选）
# DOMAIN_ID - 领域ID（可选）

curl -s -X POST "https://api.notion.com/v1/pages" \
  "${NOTION_HEADERS[@]}" \
  -d '{
    "parent": {"database_id": "22b9457a-b762-4c74-a41e-7be43ad0aa52"},
    "properties": {
      "Name": {"title": [{"text": {"content": "'"$TITLE"'"}}]},
      "总结": {"rich_text": [{"text": {"content": "'"$SUMMARY"'"}}]},
      "状态": {"status": {"name": "草稿"}},
      "标签": {"multi_select": ['"$TAGS"']},
      "🚩 领域": {"relation": [{"id": "'"$DOMAIN_ID"'"}]}
    },
    "children": [
      {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": "💡 灵感概述"}}]}},
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "'"$SUMMARY"'"}}]}},
      {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": "🧠 详细思考"}}]}},
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "'"$BODY"'"}}]}},
      {"object": "block", "type": "divider", "divider": {}},
      {"object": "block", "type": "callout", "callout": {"rich_text": [{"type": "text", "text": {"content": "状态：草稿 → 待发展为永久笔记或关联到项目"}}], "icon": {"type": "emoji", "emoji": "🌱"}}}
    ]
  }' | jq '{id, title: .properties.Name.title[0].plain_text, url: .url, created: .created_time}'
```

**正文结构：**
1. `💡 灵感概述` — 一句话概括（来自 SUMMARY）
2. `🧠 详细思考` — 展开的想法、灵感来源、联想（来自 BODY）
3. 分割线 + `🌱` callout — 提示后续动作

**默认状态：** 草稿

---

## 功能 7：创建永久笔记

**⚠️ 正文是核心**：永久笔记必须是完整的、独立的知识单元，正文不可为空。

```bash
# 变量说明：
# TITLE - 笔记标题（必填，使用观点作为标题）
# SUMMARY - 核心观点（必填，一句话提炼）
# BODY - 正文论述（必填，完整的观点阐述、论据、例子）
# TAGS - 标签数组（可选）
# DOMAIN_ID - 领域ID（可选）

curl -s -X POST "https://api.notion.com/v1/pages" \
  "${NOTION_HEADERS[@]}" \
  -d '{
    "parent": {"database_id": "1bf7d20f-9d37-48a6-bb18-78e3513698f5"},
    "properties": {
      "Name": {"title": [{"text": {"content": "'"$TITLE"'"}}]},
      "总结": {"rich_text": [{"text": {"content": "'"$SUMMARY"'"}}]},
      "状态": {"status": {"name": "未开始"}},
      "标签": {"multi_select": ['"$TAGS"']},
      "🚩 领域": {"relation": [{"id": "'"$DOMAIN_ID"'"}]}
    },
    "children": [
      {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": "🎯 核心观点"}}]}},
      {"object": "block", "type": "callout", "callout": {"rich_text": [{"type": "text", "text": {"content": "'"$SUMMARY"'"}}], "icon": {"type": "emoji", "emoji": "💎"}}},
      {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": "📝 论述"}}]}},
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "'"$BODY"'"}}]}},
      {"object": "block", "type": "divider", "divider": {}},
      {"object": "block", "type": "callout", "callout": {"rich_text": [{"type": "text", "text": {"content": "这是一个原子性知识单元，应能独立成立。检查：是否只表达了一个观点？是否有足够论据？"}}], "icon": {"type": "emoji", "emoji": "✅"}}}
    ]
  }' | jq '{id, title: .properties.Name.title[0].plain_text, url: .url, created: .created_time}'
```

**正文结构：**
1. `🎯 核心观点` — 一句话 callout（来自 SUMMARY）
2. `📝 论述` — 完整的观点阐述、论据、实例（来自 BODY）
3. 分割线 + `✅` callout — 自检提示

**默认状态：** 未开始

**永久笔记原则：**
- 一个笔记一个观点（原子性）
- 用自己的话写，不是摘抄
- 能独立理解，不依赖上下文

---

## 功能 8：查询全部领域

列出系统中所有领域，用于创建笔记时选择关联领域。

```bash
curl -s -X POST "https://api.notion.com/v1/databases/ac9e08fc-67f9-423f-a141-49ac44be6bf2/query" \
  "${NOTION_HEADERS[@]}" \
  -d '{
    "sorts": [{"property": "Name", "direction": "ascending"}],
    "page_size": 100
  }' | jq '[.results[] | {id, name: .properties.Name.title[0].plain_text, intro: (.properties["简介"].rich_text[0].plain_text // "无简介"), archived: .properties["是否归档"].checkbox}]'
```

**输出格式：** 列表展示领域名称、简介、是否归档、ID（用于关联）。

---

## 功能 9：创建领域

```bash
# 变量说明：
# NAME - 领域名称（必填）
# INTRO - 领域简介（必填，将写入属性字段和正文）
# BODY - 详细描述（可选，包含/排除范围、关键主题等）

curl -s -X POST "https://api.notion.com/v1/pages" \
  "${NOTION_HEADERS[@]}" \
  -d '{
    "parent": {"database_id": "ac9e08fc-67f9-423f-a141-49ac44be6bf2"},
    "properties": {
      "Name": {"title": [{"text": {"content": "'"$NAME"'"}}]},
      "简介": {"rich_text": [{"text": {"content": "'"$INTRO"'"}}]}
    },
    "children": [
      {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": "📋 领域简介"}}]}},
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "'"$INTRO"'"}}]}},
      {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": "📂 覆盖范围"}}]}},
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "'"$BODY"'"}}]}}
    ]
  }' | jq '{id, name: .properties.Name.title[0].plain_text, url: .url, created: .created_time}'
```

**正文结构：**
1. `📋 领域简介` — 简短概括（来自 INTRO）
2. `📂 覆盖范围` — 包含/排除范围、关键主题（来自 BODY）

---

## 功能 10：创建工具箱工具（去重校验）

创建前先按 URL 查重，避免重复添加。

### Step 1：URL 去重检查

```bash
# 用用户提供的 URL 查询工具箱是否已存在
curl -s -X POST "https://api.notion.com/v1/databases/6f7bb9cc-ac01-41c5-9856-fb1568d197ae/query" \
  "${NOTION_HEADERS[@]}" \
  -d '{
    "filter": {
      "property": "URL",
      "url": {"equals": "'"$TOOL_URL"'"}
    }
  }' | jq '{found: (.results | length > 0), existing: [.results[] | {id, title: .properties.Name.title[0].plain_text, url: .properties.URL.url}]}'
```

- 如果 `found: true` → 告知用户工具已存在，展示已有条目，**终止操作**
- 如果 `found: false` → 继续 Step 2

### Step 2：创建工具

```bash
# 变量说明：
# TOOL_NAME - 工具名称（必填）
# TOOL_URL - 工具链接（必填）
# TOOL_INTRO - 工具简介（必填，将写入属性字段和正文）
# TOOL_TYPE - 类型单选：网站/工具包/软件/浏览器插件/Prompt（可选）
# TOOL_TAGS - 标签数组（可选）
# TOOL_BODY - 正文内容（可选，包含使用方法、适用场景等）

curl -s -X POST "https://api.notion.com/v1/pages" \
  "${NOTION_HEADERS[@]}" \
  -d '{
    "parent": {"database_id": "6f7bb9cc-ac01-41c5-9856-fb1568d197ae"},
    "properties": {
      "Name": {"title": [{"text": {"content": "'"$TOOL_NAME"'"}}]},
      "URL": {"url": "'"$TOOL_URL"'"},
      "简介": {"rich_text": [{"text": {"content": "'"$TOOL_INTRO"'"}}]},
      "类型单选": {"select": {"name": "'"$TOOL_TYPE"'"'}},
      "标签": {"multi_select": ['"$TOOL_TAGS"']}
    },
    "children": [
      {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": "📋 简介"}}]}},
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "'"$TOOL_INTRO"'"}}]}},
      {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": "🛠️ 使用方法"}}]}},
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "'"$TOOL_BODY"'"}}]}},
      {"object": "block", "type": "divider", "divider": {}},
      {"object": "block", "type": "callout", "callout": {"rich_text": [{"type": "text", "text": {"content": "链接：'"$TOOL_URL"'"}}], "icon": {"type": "emoji", "emoji": "🔗"}}}
    ]
  }' | jq '{id, title: .properties.Name.title[0].plain_text, url: .url, created: .created_time}'
```

**正文结构：**
1. `📋 简介` — 简短描述（来自 TOOL_INTRO）
2. `🛠️ 使用方法` — 使用指南、适用场景（来自 TOOL_BODY）
3. 分割线 + `🔗` callout — 工具链接

**注意：** 可选字段未提供时从请求中移除。

---

## 功能 11：删除工具箱工具（需确认）

**⚠️ 破坏性操作，必须向用户确认后执行。**

### Step 1：搜索工具

先按名称或 URL 搜索，展示匹配结果让用户确认。

```bash
# 按名称搜索（使用 Notion search API）
curl -s -X POST "https://api.notion.com/v1/search" \
  "${NOTION_HEADERS[@]}" \
  -d '{
    "query": "'"$SEARCH_TERM"'",
    "filter": {"property": "object", "value": "page"},
    "page_size": 10
  }' | jq '[.results[] | select(.parent.database_id == "6f7bb9cc-ac01-41c5-9856-fb1568d197ae") | {id, title: .properties.Name.title[0].plain_text, url: .properties.URL.url}]'
```

### Step 2：确认后删除

用户确认要删除的工具后，执行 trash 操作：

```bash
# PAGE_ID - 用户确认要删除的工具页面 ID
curl -s -X PATCH "https://api.notion.com/v1/pages/$PAGE_ID" \
  "${NOTION_HEADERS[@]}" \
  -d '{"in_trash": true}' | jq '{id, trashed: .in_trash}'
```

**操作规范：**
1. 展示搜索结果，列出匹配的工具名称和 URL
2. 明确告知用户「此操作将把工具移到回收站，可以恢复」
3. 等用户明确确认后再执行
4. 多个匹配时让用户选择具体删除哪一个

---

## 功能 12：URL 保存到文献笔记

根据 URL 抓取网页内容（含图片），保存到文献笔记数据库。支持文章、X/Twitter、少数派等。

### 核心流程

```
抓取内容 → 提取图片URL → 下载图片 → 上传到Notion → 语言检测+翻译 → 创建页面（含封面+正文+图片+领域）
```

**⚠️ 正文规则：**
- **不添加任何额外内容**：不要 `📝 摘要`、`📖 正文` 等标题，不要概述，不要总结
- 直接将原文完整内容写入正文 blocks，逐段对应
- **如果原文是英文 → 逐段翻译为简体中文后写入**，保持段落数量和顺序不变
- 如果原文是中文 → 直接写入正文
- **翻译要求：忠实原文完整内容，不做摘要不删减，保留段落结构，技术术语可保留英文并括号标注中文**
- 图片插入到正文中对应位置（如有），或集中放在正文末尾
- 单段超过 1990 字符时拆分为多个 paragraph block
- **Markdown 内联格式必须转成 Notion rich_text**：`[文字](URL)` → 可点击链接，`**加粗**` → bold，`*斜体*` → italic。不要把 Markdown 源码当纯文本写进 Notion（详见 [references/markdown-to-notion-rich-text.md](references/markdown-to-notion-rich-text.md)）
- **注意：翻译工作由 Claude 在构建 children blocks 时直接完成。不需要调用外部翻译 API。Claude 读取提取的英文内容后，直接输出翻译后的中文段落，然后写入 Notion blocks。**

### Step 1：抓取内容

按网站类型选择抓取方式（详见 [references/site-adapters.md](references/site-adapters.md)）：

<<<<<<< HEAD
**通用网站（优先 `opencli web read`，默认下载图片）：**

```bash
mkdir -p /tmp/article_<id>
opencli web read --url "<URL>" --output /tmp/article_<id> -f json > /tmp/article_meta_<id>.json
```

- 输出目录下生成 `.md` 正文文件和 `images/` 目录
- 图片已下载到本地，可直接作为 `file_upload` 上传
- 返回的 JSON 元数据含 `title`, `author`, `publish_time`, `saved`（Markdown 文件路径）

微信公众号、少数派、知乎等需要 JS 渲染的站点，统一用 `opencli web read`；curl 直接抓大概率返回验证页或内容残缺。

**回退方案（按优先级）：**
1. `agent-browser open "<URL>"` + `get html body --json` / `get text body --json`
2. `curl -sL --max-time 15 -H "User-Agent: Mozilla/5.0" "<URL>"` — 仅适用于非 JS 渲染页面，图片需单独下载

**X/Twitter：**
```bash
# 优先 opencli twitter（不要包 timeout，部分环境没有该命令）
opencli twitter article "<X URL>" -f json > /tmp/x_article.json

# 抓取图片/附件（需要 opencli 已登录 Twitter）
opencli twitter download --tweet-url "<X URL>" -f json --output /tmp/x_dl
```

- `opencli twitter article` 返回列表，普通推文/线程在 `content`，X Article 含 `title` + 完整正文
- `opencli twitter download` 把媒体存到 `/tmp/x_dl/tweets/`，本地可直接读取

**图片回退：`opencli web read`**

当 `opencli twitter download` 失败、未登录或没有返回媒体时，用浏览器渲染再试一次：

```bash
opencli web read --url "<X URL>" --output /tmp/x_web_<id> -f json
```

- 输出目录下生成 `.md` 和 `images/`
- 下载到的本地图片走 `file_upload`

**文本/图片回退：fxtwitter API**（opencli 完全不可用时）：

```bash
curl -sL "https://api.fxtwitter.com/<username>/status/<tweet_id>" -o /tmp/fx_article.json
```

- 普通推文：正文在 `.tweet.text`，媒体在 `.tweet.media.all[].url`
- X Article：正文在 `.tweet.article.content.blocks[]`；封面图在 `.tweet.article.cover_media.media_info.original_img_url`；内容图片在 `.tweet.article.media_entities[].media_info.original_img_url`；图片位置通过 `atomic` block + `entityMap` 中的 `MEDIA` 实体关联到 `media_id`

**微信公众号：**

微信公众号文章需要浏览器渲染，curl 经常被拦截。推荐用 `agent-browser` 获取渲染后的 HTML，再按 `references/site-adapters.md` 的「微信公众号」章节解析。
解析脚本：`references/scripts/wechat-parser.py`。微信图片有防盗链，需下载后通过 Files API 上传为 `file_upload`。

**记录图片位置（强烈建议）：**

不同来源对图片位置的表达能力不同。尽量在抓取阶段就把图片和它附近的文本段落关联起来，供 Step 5 使用：

| 来源 | 可获取的位置信息 | 处理方式 |
|------|----------------|---------|
| HTML 网页 | `<img>` 出现在第 N 个段落之后 | 给该图片标注 `block_index = N` |
| X Article (fxtwitter) | `atomic` block + `entityMap` 中的 `MEDIA` 实体，可映射到 media_id | 按文本块顺序计算 `block_index`，精确插入 |
| agent-browser / opencli web | 可能返回带图片位置的 JSON | 优先使用解析器给出的索引 |

图片对象建议统一为：

```python
{"url": "...", "file_id": "...", "block_index": 5}  # block_index 可选，越小位置越靠前
```

**X/Twitter 图片处理：**

- `opencli twitter download` 下载到本地的媒体 → 使用 `file_upload` image block
- fxtwitter 返回的 `pbs.twimg.com` URL → 本地可能不可达，使用 `external` image block，让 Notion 直接加载
- 第一张图片作封面；其余按原文顺序（或 `block_index`）插入正文

**图片类型选择策略：**

| 场景 | 方式 | 说明 |
|------|------|------|
| 普通网站图片 | `file_upload` | `opencli web read` 已下载到 `images/`；或手动下载后上传 |
| X/Twitter 图片 | `file_upload` / `external` | opencli 下载的本地媒体用 `file_upload`；fxtwitter 的 `pbs.twimg.com` URL 用 `external` |
| 需要防盗链的图片 | `external` + Referer | 少数派/知乎等，如果 Notion 无法访问则跳过 |

**少数派/知乎：** 需浏览器渲染 + Referer 防盗链头。

### Step 2：提取图片 URL

从抓取的 HTML 或 JSON 中提取图片 URL：

```python
import re, json

# 从 HTML 提取
imgs = re.findall(r'<img[^>]*src=["\']([^"\']+)["\']', raw_html)

# 从 X/Twitter fxtwitter JSON 提取
# cover_media 和 media_entities 中包含图片信息

# 解析相对路径为绝对路径
base_url = "/".join(source_url.split("/")[:3])
resolved = []
for img in imgs[:10]:  # 限制数量
    if img.startswith("http"):
        resolved.append(img)
    elif img.startswith("/"):
        resolved.append(base_url + img)
    else:
        resolved.append(source_url.rsplit("/", 1)[0] + "/" + img)
```

### Step 3：下载图片

```bash
mkdir -p /tmp/notion_images

# 带 Referer 下载（处理防盗链）
curl -sL --max-time 10 -H "Referer: <source_site>" -o /tmp/notion_images/img_00.png "<image_url>"

# 验证下载成功（文件大小 > 100 bytes）
```

### Step 4：上传图片到 Notion Files API

使用 Notion Files API（版本 `2025-09-03`），详见 [references/image-upload.md](references/image-upload.md)：

```python
import json, subprocess, os, time, mimetypes

NOTION_KEY = os.environ.get("NOTION_API_TOKEN", "")
FILES_API_VERSION = "2025-09-03"

uploaded_images = []

for img_path in sorted(os.listdir(IMG_DIR)):
    if not img_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
        continue

    fpath = os.path.join(IMG_DIR, img_path)
    mime = mimetypes.guess_type(fpath)[0] or "image/png"

    # Step 4a: 创建上传对象
    r = subprocess.run(["curl", "-s", "-X", "POST",
        "https://api.notion.com/v1/file_uploads",
        "-H", f"Authorization: Bearer {NOTION_KEY}",
        "-H", f"Notion-Version: {FILES_API_VERSION}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps({"filename": img_path, "content_type": mime})],
        capture_output=True, text=True)
    file_id = json.loads(r.stdout)["id"]

    # Step 4b: 发送文件数据
    subprocess.run(["curl", "-s", "-X", "POST",
        f"https://api.notion.com/v1/file_uploads/{file_id}/send",
        "-H", f"Authorization: Bearer {NOTION_KEY}",
        "-H", f"Notion-Version: {FILES_API_VERSION}",
        "-F", f"file=@{fpath};filename={img_path}"])

    uploaded_images.append({"file_id": file_id, "name": img_path})
    time.sleep(0.5)  # Rate limit: ~2 req/s
```

### Step 4.5：语言检测 + 英文翻译（必须执行）

提取的正文如果是英文，**必须翻译为简体中文后写入 Notion**。**翻译是强制步骤，不可跳过。**

**翻译要求：**
- 逐段翻译，保持原文段落结构和顺序
- 技术术语保留英文原文或标注（如 "Agent（智能体）"）
- 代码片段、URL、专有名词不翻译
- 列表、编号结构保持原样
- 翻译质量要求：准确、自然、可读，不要机翻感

```python
import re

def detect_language(text):
    """检测文本主要语言"""
    # 简单检测：统计中文字符占比
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    total_chars = len(text.strip())
    if total_chars == 0:
        return "unknown"
    ratio = chinese_chars / total_chars
    return "zh" if ratio > 0.1 else "en"

# 检测语言
lang = detect_language(full_text)
print(f"Detected language: {lang}")

if lang == "en":
    # 逐段翻译（由 Claude 执行翻译）
    # 将原文按段落拆分，逐段翻译
    paragraphs = [p.strip() for p in full_text.split('\n\n') if p.strip()]
    translated_paragraphs = []
    for para in paragraphs:
        # 翻译规则：
        # 1. 保留代码块不翻译
        # 2. 保留 URL 不翻译
        # 3. 技术术语可保留英文并括号标注中文
        # 4. 保持段落结构不变
        translated = translate_to_chinese(para)  # 由 Claude 执行
        translated_paragraphs.append(translated)

    # 使用翻译后的段落作为正文
    body_paragraphs = translated_paragraphs
else:
    # 中文原文直接使用
    body_paragraphs = [p.strip() for p in full_text.split('\n\n') if p.strip()]
```

**注意：** 翻译工作由 Claude 在构建 children blocks 时直接完成。不需要调用外部翻译 API。Claude 读取提取的英文内容后，直接输出翻译后的中文段落，然后写入 Notion blocks。

**翻译示例：**

原文：
> Nobody starts with a perfect workflow. In the beginning, you usually only have a rough sense of the problem, a few strong intuitions, and some obvious constraints.

翻译后：
> 没有人一开始就有完美的工作流。起初，你通常只对问题有一个粗略的感知、一些强烈的直觉，以及一些明显的约束条件。

**翻译示例：**

原文：
> Nobody starts with a perfect workflow. In the beginning, you usually only have a rough sense of the problem, a few strong intuitions, and some obvious constraints.

翻译后：
> 没有人一开始就有完美的工作流。起初，你通常只对问题有一个粗略的感知、一些强烈的直觉，以及一些明显的约束条件。

**翻译规则：**
1. 保留代码块不翻译
2. 保留 URL 不翻译
3. 技术术语可保留英文并括号标注中文（如 "Agent（智能体）"）
4. 保持段落结构不变
5. 翻译质量要求：准确、自然、可读，不要机翻感

### Step 5：创建文献笔记页面（含封面 + 正文 + 图片 blocks + 领域）

```python
# === 封面处理 ===
# 第一张图片设为页面封面（cover），不插入正文
cover_block = None
inline_images = uploaded_images[1:]  # 剩余图片插入正文

if uploaded_images:
    first_img = uploaded_images[0]
    # 优先使用 file_upload 类型（已上传到 Notion）
    cover_block = {
        "type": "file_upload",
        "file_upload": {"id": first_img["file_id"]}
    }
    # 如果是 external URL（如 X/Twitter 图片），用 external 类型
    if first_img.get("url"):
        cover_block = {
            "type": "external",
            "external": {"url": first_img["url"]}
        }

# === 领域处理 ===
# 创建前先用功能 8 查询领域列表，让用户选择关联领域
# 或根据标签/内容自动推荐（如标签含 "AI" → 推荐 "AI" 领域）
domain_id = ""  # 用户选择的领域 ID，为空则不设置

# === 构建 children blocks ===
# ⚠️ 直接保存原文翻译内容，不添加摘要/概述/正文标题等额外内容
children = []

# 添加原文段落（英文已翻译为中文，中文直接使用）
# 每段不超过 1990 字符（Notion 上限 2000，留余量防止编码问题）
for para in text_paragraphs:
    if len(para) <= 1990:
        children.append({
            "object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": para}}]}
        })
    else:
        # 超长段落拆分为多个 block
        for i in range(0, len(para), 1990):
            chunk = para[i:i+1990]
            children.append({
                "object": "block", "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": chunk}}]}
            })

# 插入图片 blocks：按原始结构穿插，而不是全部堆在末尾
# 优先使用来源解析器提供的 block_index；没有时按段落数均匀分布
children = interleave_paragraphs_and_images(
    paragraphs=text_paragraphs,
    images=inline_images,
    max_blocks=98  # 预留 divider + callout
)

# 来源 callout
children.append({"object": "block", "type": "divider", "divider": {}})
children.append({"object": "block", "type": "callout", "callout": {
    "rich_text": [{"type": "text", "text": {"content": f"来源：{source_url}"}}],
    "icon": {"type": "emoji", "emoji": "🔗"}
}})

# 注意: children 总数不超过 100 个 block（Notion API 限制）
```

**图片穿插函数示例：**

```python
def interleave_paragraphs_and_images(paragraphs, images, max_blocks=98):
    """
    把图片按原始结构穿插到段落之间。

    - 如果 image 字典里有 'block_index'，表示解析器已给出在原文中的位置，直接按索引插入。
    - 否则按段落数均匀分布：每 ceil(N_paragraphs / N_images) 个段落后放一张图。
    - 若总 blocks 超过 max_blocks，优先保留文字段落，按比例丢弃尾部图片。
    """
    text_blocks = []
    for para in paragraphs:
        if len(para) <= 1990:
            text_blocks.append({"object": "block", "type": "paragraph",
                                "paragraph": {"rich_text": [{"type": "text", "text": {"content": para}}]}})
        else:
            for i in range(0, len(para), 1990):
                text_blocks.append({"object": "block", "type": "paragraph",
                                    "paragraph": {"rich_text": [{"type": "text", "text": {"content": para[i:i+1990]}}]}})

    # 按 block_index 排序，无索引的排最后
    positioned = [(img.get("block_index", float("inf")), img) for img in images]
    positioned.sort(key=lambda x: x[0])

    children = []
    img_idx = 0
    n_text = len(text_blocks)
    n_images = len(positioned)
    # 均匀分布的步长
    step = max(1, n_text // max(n_images, 1)) if n_images > 0 else n_text

    for text_idx, block in enumerate(text_blocks):
        children.append(block)
        # 有 block_index 的图片：在当前文本块之后插入所有 block_index 落在此处的图片
        while img_idx < n_images:
            idx, img = positioned[img_idx]
            # 已提供明确位置且 <= 当前文本索引，插入
            if idx != float("inf") and idx <= text_idx:
                children.append(image_block(img))
                img_idx += 1
            else:
                break
        # 无 block_index 的图片：按均匀步长插入
        if img_idx < n_images and positioned[img_idx][0] == float("inf"):
            if (text_idx + 1) % step == 0:
                children.append(image_block(positioned[img_idx][1]))
                img_idx += 1

    # 若还有剩余图片（原文末尾）
    while img_idx < n_images:
        children.append(image_block(positioned[img_idx][1]))
        img_idx += 1

    # 超限保护：优先保留文字段落
    if len(children) > max_blocks:
        text_part = [b for b in children if b["type"] != "image"]
        image_part = [b for b in children if b["type"] == "image"]
        keep_images = min(len(image_part), max_blocks - len(text_part))
        children = text_part + image_part[:keep_images]

    return children


def image_block(img):
    """根据 img 字典构建 Notion image block（支持 file_upload / external）。"""
    if img.get("file_id"):
        return {"object": "block", "type": "image",
                "image": {"type": "file_upload", "file_upload": {"id": img["file_id"]}}}
    return {"object": "block", "type": "image",
            "image": {"type": "external", "external": {"url": img["url"]}}}
```

**图片插入策略：**
- `file_upload` 类型图片可直接包含在创建页面的 `children` 中
- `external` 类型图片（如 X/Twitter pbs.twimg.com）也可包含在 `children` 中，Notion 会从 URL 加载
- **优先按原始结构插入**：HTML 解析时记录 `<img>` 所在的段落位置；JSON 解析时使用解析器提供的 `block_index`
- **无精确位置时均匀分布**：不要把所有图片放到正文末尾
- 超出 `max_blocks` 时优先保留文字段落，按比例丢弃尾部图片
- 不要先创建页面再追加图片（容易产生重复），在创建时一次性包含所有 blocks
```

**创建页面（含封面 + 领域）：**
```bash
curl -s -X POST "https://api.notion.com/v1/pages" \
  "${NOTION_HEADERS[@]}" \
  -d '{
    "parent": {"database_id": "05c87b65-e76b-4789-a38c-5c84809d300f"},
    "cover": <cover_block 或省略>,
    "properties": {
      "Name": {"title": [{"text": {"content": "<标题>"}}]},
      "URL": {"url": "<来源URL>"},
      "总结": {"rich_text": [{"text": {"content": "<摘要>"}}]},
      "文献类型": {"select": {"name": "文章"}},
      "状态": {"status": {"name": "处理中"}},
      "标签": {"multi_select": [{"name": "AI"}, {"name": "..."}]},
      "🚩 领域": {"relation": [{"id": "<domain_id>"}]}
    },
    "children": <上面构建的 children 数组>
  }'
```

### 标签选择

参考 [references/tag-rules.md](references/tag-rules.md)：
1. 优先选 2-3 个最相关标签
2. 特定平台加来源标签（少数派/公众号/博客/X）
3. AI/技术类加技术标签
4. 总数控制 3-5 个

### 关键限制

| 限制 | 值 | 处理方式 |
|------|-----|---------|
| 单次创建最多 blocks | 100 | 超过时分批用 PATCH 追加 |
| 单文件最大 | 5MB | 大图压缩或跳过 |
| Files API rate limit | ~2 req/s | 每次上传间隔 0.5s |
| rich_text 最大长度 | 2000 字符 | 长文本拆分为多个 block |
| 支持图片格式 | png, jpg, gif, webp, svg | 其他格式跳过 |

### 返回结果

```
✅ 已保存到 Notion 文献笔记
- **标题**：{标题}
- **来源**：{URL}
- **标签**：{标签}
- **图片**：{N} 张已上传
- **页面**：{page_url}
```

---

## 功能 13：URL 保存到工具箱

根据 URL 自动提取工具信息，保存到工具箱数据库。包含正文（最佳实践/使用方法）。

### 核心流程

```
接收 URL → URL 去重 → 提取页面信息 → 选择图标 → 生成正文 → 创建页面
```

### Step 1：URL 去重检查

```bash
# 先检查该 URL 是否已在工具箱中
curl -s -X POST "https://api.notion.com/v1/databases/6f7bb9cc-ac01-41c5-9856-fb1568d197ae/query" \
  "${NOTION_HEADERS[@]}" \
  -d '{
    "filter": {
      "property": "URL",
      "url": {"equals": "'"$TOOL_URL"'"}
    }
  }' | jq '{found: (.results | length > 0), existing: [.results[] | {id, title: .properties.Name.title[0].plain_text}]}'
```

- 如果 `found: true` → 告知用户工具已存在，**终止操作**
- 如果 `found: false` → 继续 Step 2

### Step 2：提取页面信息

优先使用 `opencli web read` 抓取页面（支持 JS 渲染，自动下载图片）：

```bash
mkdir -p /tmp/tool_<id>
opencli web read --url "$TOOL_URL" --output /tmp/tool_<id>
```

按域名规则提取（详见 [references/extraction-rules.md](references/extraction-rules.md) 和 [references/site-adapters.md](references/site-adapters.md)）：

| 来源 | 提取内容 |
|------|---------|
| GitHub | 仓库名、简介、topics、语言 |
| Chrome Web Store | 扩展名、描述 → 类型：浏览器插件 |
| npm/PyPI | 包名、description → 类型：工具包 |
| 官网/SaaS | 站名、hero 描述 → 类型：网站 |

**大页面/入口型站点处理**：
- 如果抓取到的 Markdown 超过 20KB（例如代码库百科、文档聚合站），不要全文写入工具箱。
- 只提取：一句话简介 + 使用方式 + 适用场景 + 核心功能。
- 正文里**跳过图片、视频、架构图**，只保留文字和链接。
- 工具箱卡片的目标是可快速判断“这个工具是什么、怎么用”，不是归档原文。

### Step 3：选择图标

根据工具特征选择 emoji（详见 [references/icon-guide.md](references/icon-guide.md)）：

| 场景 | 图标 |
|------|------|
| Python 项目 | 🐍 |
| AI/LLM/Agent | 🤖 |
| 设计工具 | 🎨 |
| 开发工具 | 🛠️ |
| 默认 | 💻 |

### Step 4：生成正文内容

根据工具类型自动生成「最佳实践」正文：

| 工具类型 | 正文重点 |
|---------|---------|
| 软件 | 安装配置 → 快捷键 → 工作流集成 → 效率技巧 |
| 网站 | 使用场景 → 核心功能 → 付费方案 → 替代方案 |
| 浏览器插件 | 安装方式 → 使用技巧 → 隐私设置 → 冲突排查 |
| Prompt | 使用场景 → 优化技巧 → 变量设置 → 效果对比 |
| 工具包 | 安装命令 → 基础用法 → 进阶配置 → 版本兼容 |

生成正文时：
- 优先使用 `opencli web read` 抓取到的真实内容，不要编造功能点；
- 如果内容里有 Markdown 链接 `[文字](URL)` 或 `**加粗**`，必须转成 Notion rich_text 格式（参考 [references/markdown-to-notion-rich-text.md](references/markdown-to-notion-rich-text.md)）；
- 入口型/百科型页面只做摘要，不要堆全文。

### Step 5：创建页面（含封面和图标）

```bash
curl -s -X POST "https://api.notion.com/v1/pages" \
  "${NOTION_HEADERS[@]}" \
  -d '{
    "parent": {"database_id": "6f7bb9cc-ac01-41c5-9856-fb1568d197ae"},
    "icon": {"type": "emoji", "emoji": "'"$ICON"'"},
    "cover": {"type": "external", "external": {"url": "'"$COVER_URL"'"}},
    "properties": {
      "Name": {"title": [{"text": {"content": "'"$TOOL_NAME"'"}}]},
      "URL": {"url": "'"$TOOL_URL"'"},
      "简介": {"rich_text": [{"text": {"content": "'"$TOOL_DESC"'"}}]},
      "类型单选": {"select": {"name": "'"$TOOL_TYPE"'"'}},
      "标签": {"multi_select": ['"$TOOL_TAGS"']}
    },
    "children": [
      {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "🎯 最佳实践"}}]}},
      {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": "适用场景"}}]}},
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "'"$USAGE_SCENARIOS"'"}}]}},
      {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": "快速开始"}}]}},
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "'"$QUICK_START"'"}}]}},
      {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": "核心技巧"}}]}},
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "'"$TIPS"'"}}]}},
      {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": "注意事项"}}]}},
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "'"$CAUTIONS"'"}}]}},
      {"object": "block", "type": "divider", "divider": {}},
      {"object": "block", "type": "callout", "callout": {"rich_text": [{"type": "text", "text": {"content": "链接：'"$TOOL_URL"'"}}], "icon": {"type": "emoji", "emoji": "🔗"}}}
    ]
  }' | jq '{id, title: .properties.Name.title[0].plain_text, url: .url, created: .created_time}'
```

**正文结构（5 段式最佳实践）：**
1. `🎯 最佳实践` — 大标题
2. `适用场景` — 什么时候用
3. `快速开始` — 3-5 步上手
4. `核心技巧` — 3-5 个提效要点
5. `注意事项` — 常见坑和限制
6. 分割线 + `🔗` callout — 工具链接

### 返回结果

```
✅ 已保存到 Notion 工具箱
📌 名称：{name}
🔗 URL: {url}
📁 类型：{type}
🏷️ 标签：{tags}
🎨 图标：{icon}
🔗 在 Notion 中查看: {page_url}
```

---

## 测试数据记录

以下 URL 已通过功能 12 测试，验证了不同网站类型的抓取和保存流程：

| # | URL 类型 | URL | 抓取方式 | 语言 | 封面 | 领域 | 正文翻译 | 状态 |
|---|---------|-----|---------|------|------|------|---------|------|
| 1 | X Article | `https://x.com/WendyWug/status/2073947768507515046` | `opencli twitter article <tweet_id>` | 英文→中文 | ✅ external | ✅ AI | ✅ 逐段翻译 | ✅ |
| 2 | X 推文 Thread | `https://x.com/web3annie/status/2073781889387925709` | `opencli twitter thread <tweet_id>` | 中文 | ❌ 无图片 | ✅ AI | — 中文直存 | ✅ |
| 3 | 少数派文章 | `https://sspai.com/post/111702` | `curl` + HTML 解析 | 中文 | ✅ file_upload | ✅ AI | — 中文直存 | ✅ |
| 4 | 网页文章 | `https://simplemarkdowneditor.com/pub/IbaCrTjLJT?key=uQOQ2NPO3TTUSXyYDjyLf` | `opencli web read --url <URL>` | 英文→中文 | ❌ 无图片 | ✅ AI | ✅ 逐段翻译 | ✅ |

**抓取方式选择策略：**

| 来源类型 | 首选工具 | 回退方案 | 图片处理 |
|---------|---------|---------|---------|
| 普通网页 | `curl` + HTML 解析 | `opencli web read --url` | 下载到本地 → `file_upload` |
| X Article | `opencli twitter article <tweet_id>` | — | 无图片（opencli 不提取 Article 图片） |
| X 推文 Thread | `opencli twitter thread <tweet_id>` | — | `media_urls` 字段可获取 |
| 少数派 | `curl` + Referer 防盗链 | `opencli web read` | 下载需带 Referer → `file_upload` |
| 知乎 | `opencli web read` | — | 需 Referer，可能被限制 |

**已知限制：**
- `opencli twitter article` 不支持提取 X Article 内嵌图片（Draft.js entityMap 中的图片被丢弃）
- `opencli twitter download --tweet-url` 对 Article 类型返回 EMPTY_RESULT
- X 图片 URL（pbs.twimg.com）本地环境可能不可达，需用 `external` 类型或 fxtwitter API 辅助
- sspai 图片下载必须带 `Referer: https://sspai.com/` 头
- 单个 `rich_text` content 上限 2000 字符，超长需拆分（实测用 1990 字符截断更安全）
- 每次创建页面 `children` 上限 100 个 blocks

---

## 操作规范

1. **创建操作前确认**：创建笔记/领域/工具前，向用户确认内容无误再执行
2. **正文必填**：创建文献笔记、灵感笔记、永久笔记、领域、工具时，**正文（children blocks）不可为空**。如果用户未提供正文内容，必须主动询问
3. **字段按需传入**：用户未提供的可选字段不要包含在请求体中
4. **标签处理**：用户输入逗号分隔的标签字符串，转换为 `[{"name": "tag1"}, {"name": "tag2"}]` 格式
5. **领域关联**：创建笔记时如需关联领域，先用功能 8 查询领域列表，让用户选择
6. **结果展示**：查询结果以表格形式展示，创建结果返回 Notion 页面链接
7. **时间计算**：macOS 使用 `date -u -v-Nd`，Linux 使用 `date -u -d 'N days ago'`
8. **错误处理**：检查 HTTP 状态码，429 时等待 Retry-After 秒后重试
9. **工具箱去重**：创建工具前必须先按 URL 查重（功能 10/13），重复则终止
10. **删除需确认**：删除工具（功能 11）必须先展示搜索结果，等用户明确确认后再执行
11. **URL 保存**：抓取内容后先向用户展示标题和摘要，确认后再写入 Notion（功能 12/13）
12. **图片上传限速**：批量上传图片时每次间隔 0.4 秒，避免触发 rate limit
13. **正文超长处理**：单个 rich_text content 上限 2000 字符，超长内容需拆分为多个 paragraph block
14. **英文翻译**：功能 12 保存文献笔记时，如果原文是英文，必须逐段翻译为简体中文后写入正文。翻译要求：忠实原文完整内容，不做摘要不删减，保留段落结构，技术术语可保留英文并括号标注中文
15. **封面设置**：功能 12 保存文献笔记时，第一张图片设为页面 cover 属性，不重复插入正文

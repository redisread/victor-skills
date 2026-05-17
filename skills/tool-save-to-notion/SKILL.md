---
name: tool-save-to-notion
description: "Save tool links to Notion Toolbox. Use this skill whenever user provides ANY tool URL (GitHub, official website, product page, AI tool, browser extension, software, online service) and wants to save it to Notion. This skill automatically extracts tool info (name, type, tags, description) from the page and saves it as a structured database entry. Common triggers: 保存这个工具, 添加到工具箱, 收藏这个链接, save this tool, add to toolbox."
version: 1.0.0
metadata:
  homepage: https://github.com/victor-skills#tool-save-to-notion
---

# tool-save-to-notion

自动将工具链接保存到 Notion 工具箱数据库，包含图标、封面和最佳实践指南。

## 何时使用

当用户提供以下任一链接时**立即使用此技能**：
- GitHub 仓库链接
- 工具/产品官方网站
- AI 工具页面
- 浏览器插件商店页面
- 在线服务/网页工具
- 软件包页面 (npm, PyPI 等)
- 任何用户说"保存"、"收藏"、"添加到工具箱"的链接

## 工具箱数据库

**Database ID:** `6f7bb9cc-ac01-41c5-9856-fb1568d197ae`
**描述:** 所有工具收集地

### 数据库字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| **Name** | title | ✅ | 工具名称 |
| **类型** | multi_select | ✅ | 工具分类（见下方类型选择指南） |
| **标签** | multi_select | ✅ | 技术标签（平台、功能、技术栈等） |
| **URL** | url | ✅ | 原始链接 |
| **简介** | rich_text | ✅ | 1-2 句话描述 |
| **⭐ 置顶** | checkbox | ❌ | 是否置顶（默认 false） |
| **创建时间** | created_time | 自动 | Notion 自动记录 |
| **更新时间** | last_edited_time | 自动 | Notion 自动记录 |

---

## 执行流程

### 步骤 1: 接收 URL

用户可能这样说：
- "保存这个工具：https://github.com/user/repo"
- "把这个添加到我的工具箱"
- "收藏：https://example.com"
- "save this: https://..."

### 步骤 2: 提取页面信息

使用 WebFetch 访问 URL，提取关键信息：

```
需要提取：
1. 工具名称 (Name) - 页面标题或 og:title
2. 描述 (Description) - meta description 或页面简介
3. 关键词 - meta keywords, 页面内容中的技术名词
4. 页面类型 - 根据域名判断类型
5. 封面图 URL (Cover) - og:image 或 twitter:image（可选，用于 Notion 页面封面）
```

**WebFetch 示例：**
```
访问 https://github.com/user/repo
提取：
- 标题：仓库名称
- 描述：仓库简介
- 主题：GitHub topics
- 语言：主要编程语言
```

### 步骤 3: 生成最佳实践内容

根据工具类型和描述，自动生成该工具的最佳实践建议：

**最佳实践生成规则：**

| 工具类型 | 最佳实践重点 |
|---------|-------------|
| **软件** | 安装配置、快捷键、工作流集成、效率技巧 |
| **网站** | 使用场景、核心功能、付费方案、替代方案 |
| **浏览器插件** | 安装方式、使用技巧、隐私设置、冲突排查 |
| **Prompt** | 使用场景、优化技巧、变量设置、效果对比 |
| **工具包** | 安装命令、基础用法、进阶配置、版本兼容 |

**最佳实践内容结构：**
1. **适用场景** - 这个工具最适合解决什么问题
2. **快速开始** - 3-5 步上手指南
3. **核心技巧** - 3-5 个提升效率的要点
4. **注意事项** - 常见坑点或限制
5. **相关资源** - 文档链接、社区、教程

### 步骤 4: 选择图标

根据工具类型自动选择 emoji 图标：

| 类型 | 默认图标 | 特殊情况 |
|------|---------|---------|
| **软件** | 💻 | AI工具用🤖，设计工具用🎨，开发工具用🛠️ |
| **网站** | 🌐 | AI服务用🤖，学习平台用📚，云服务用☁️ |
| **浏览器插件** | 🔌 | 生产力用⚡，安全用🔒，AI用🤖 |
| **Prompt** | 📝 | 代码用💻，创意用✨，分析用🔍 |
| **工具包** | 📦 | Python用🐍，JS用📜，AI/ML用🧠 |

**图标选择优先级：**
1. 工具明确特征（如 Python 项目优先用 🐍）
2. 功能领域（如 AI 用 🤖，设计用 🎨）
3. 类型默认图标

### 步骤 5: 调用 Notion API 保存

使用以下 API 调用（同时设置图标、封面和正文内容）：

```bash
curl -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2021-05-13" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {
      "database_id": "6f7bb9cc-ac01-41c5-9856-fb1568d197ae"
    },
    "icon": {
      "type": "emoji",
      "emoji": "🤖"
    },
    "cover": {
      "type": "external",
      "external": {
        "url": "https://example.com/cover-image.jpg"
      }
    },
    "children": [
      {
        "object": "block",
        "type": "image",
        "image": {
          "type": "external",
          "external": {"url": "https://example.com/cover-image.jpg"}
        }
      },
      {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
          "rich_text": [{"type": "text", "text": {"content": "🎯 最佳实践"}}]
        }
      },
      {
        "object": "block",
        "type": "heading_3",
        "heading_3": {
          "rich_text": [{"type": "text", "text": {"content": "适用场景"}}]
        }
      },
      {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
          "rich_text": [{"type": "text", "text": {"content": "描述适用场景..."}}]
        }
      },
      {
        "object": "block",
        "type": "heading_3",
        "heading_3": {
          "rich_text": [{"type": "text", "text": {"content": "快速开始"}}]
        }
      },
      {
        "object": "block",
        "type": "numbered_list_item",
        "numbered_list_item": {
          "rich_text": [{"type": "text", "text": {"content": "步骤 1..."}}]
        }
      },
      {
        "object": "block",
        "type": "heading_3",
        "heading_3": {
          "rich_text": [{"type": "text", "text": {"content": "核心技巧"}}]
        }
      },
      {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
          "rich_text": [{"type": "text", "text": {"content": "技巧 1..."}}]
        }
      },
      {
        "object": "block",
        "type": "heading_3",
        "heading_3": {
          "rich_text": [{"type": "text", "text": {"content": "注意事项"}}]
        }
      },
      {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
          "rich_text": [{"type": "text", "text": {"content": "注意事项..."}}]
        }
      },
      {
        "object": "block",
        "type": "heading_3",
        "heading_3": {
          "rich_text": [{"type": "text", "text": {"content": "相关资源"}}]
        }
      },
      {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
          "rich_text": [
            {"type": "text", "text": {"content": "官方文档: "}},
            {"type": "text", "text": {"content": "https://docs.example.com", "link": {"url": "https://docs.example.com"}}}
          ]
        }
      }
    ],
    "properties": {
      "Name": {
        "title": [{"text": {"content": "工具名称"}}]
      },
      "类型": {
        "multi_select": [{"name": "类型"}]
      },
      "标签": {
        "multi_select": [{"name": "标签 1"}, {"name": "标签 2"}]
      },
      "URL": {
        "url": "https://example.com"
      },
      "简介": {
        "rich_text": [{"text": {"content": "工具简介..."}}]
      },
      "⭐ 置顶": {
        "checkbox": false
      }
    }
  }'
```

**注意：**
- `icon` 字段使用 emoji 类型，根据工具类型自动选择
- `cover` 字段是可选的。如果提取到封面图，添加该字段；如果没有封面图，省略该字段
- `children` 包含封面图片 + 最佳实践结构化内容
- 必须在创建页面时使用 `children` 参数，后续追加 blocks 需要使用不同的 API

### 步骤 6: 返回结果

保存成功后，告诉用户：

```
✅ 已保存到 Notion 工具箱

📌 名称：{Name}
🔗 URL: {URL}
📁 类型：{类型}
🏷️ 标签：{标签列表}
📝 简介：{简介}
🎨 图标：{emoji}
🖼️ 封面：顶部封面 + 正文图片
📖 最佳实践：已生成（适用场景、快速开始、核心技巧、注意事项、相关资源）

🔗 [在 Notion 中查看]({notion_url})
```

---

## 类型选择指南

**⚠️ 重要：类型只能从以下 5 个选项中选择（单选）：**

| 类型 | 适用场景 | 示例 |
|------|----------|------|
| **软件** | 桌面应用、移动应用、独立客户端 | VS Code、Figma 桌面版、Notion App |
| **网站** | 在线服务、Web 应用、SaaS 平台 | claude.ai、notion.so、GitHub |
| **浏览器插件** | Chrome/Edge/Safari 扩展程序 | Chrome Web Store 中的插件 |
| **Prompt** | Prompt 模板、提示词集合、AI 指令 | Prompt 库、提示词工具 |
| **工具包** | SDK、库、框架、CLI 工具、工具集 | npm 包、Python 库、GitHub 工具集 |

### 类型判断逻辑

```
1. 是浏览器插件吗？ → 浏览器插件
2. 是 Prompt 相关吗？ → Prompt
3. 是库/SDK/框架/CLI 吗？ → 工具包
4. 是独立桌面/移动应用吗？ → 软件
5. 其他所有 Web 服务 → 网站
```

**注意：类型是单选，不是多选！** 每个工具只能选择一个最匹配的类型。

---

## 标签提取策略

从页面内容中提取标签，优先级：

1. **显式标签** - 页面明确标注的 topics/tags
2. **技术栈** - React, Vue, Python, TypeScript, Node.js 等
3. **平台** - Mac, Windows, Chrome, VS Code, iOS 等
4. **功能** - AI, 效率，设计，开发工具，数据分析等
5. **来源** - GitHub, 开源，独立开发, SaaS 等

**标签示例：**
- 技术：`React`, `TypeScript`, `Python`, `Next.js`
- 平台：`Mac`, `Chrome`, `VS Code`, `Web`
- 功能：`AI`, `效率`, `设计`, `开发工具`, `API`
- 来源：`GitHub`, `开源`, `独立开发`, `SaaS`

**提示：** 标签应该简洁，每个标签不超过 10 个字符。

---

## 封面图提取策略

从页面内容中提取封面图，按以下优先级：

### 提取优先级

1. **Open Graph Image (og:image)** - 首选
   ```html
   <meta property="og:image" content="https://example.com/image.jpg" />
   ```
   - 质量最高，通常是网站专门准备的分享图片
   - 尺寸一般符合 Notion 封面要求（建议 ≥ 600x300）

2. **Twitter Card Image** - 备选
   ```html
   <meta name="twitter:image" content="https://example.com/image.jpg" />
   ```

3. **GitHub 仓库特殊处理** - GitHub 专用
   - 使用 GitHub 默认 OG 图片：`https://opengraph.githubassets.com/1/{owner}/{repo}`

4. **无合适图片** - 不设封面
   - 某些网站（如即刻）不提供 og:image 或 twitter:image
   - 跳过封面设置，Notion 页面正常创建但没有封面和正文图片

### 封面图验证

- **最小尺寸**: 600x300 像素（Notion 推荐）
- **支持格式**: JPEG, PNG, GIF, WebP
- **协议要求**: 必须是 HTTPS 链接
- **相对路径处理**: 如果是相对路径，需要拼接为绝对 URL

### Notion Cover 字段格式

```json
"cover": {
  "type": "external",
  "external": {
    "url": "https://example.com/cover-image.jpg"
  }
}
```

**注意**: `cover` 字段是可选的。如果提取到合适的封面图则添加，否则省略。

---

## 错误处理

### 常见错误及解决方案

| 错误 | 原因 | 解决方法 |
|------|------|----------|
| 401 Unauthorized | API key 无效或过期 | 检查 settings.json 中的 NOTION_API_KEY |
| 403 Forbidden | Integration 无写入权限 | 确认数据库已连接 Integration |
| 400 Bad Request | 请求格式错误 | 检查 JSON 格式和字段类型 |
| 404 Not Found | 数据库 ID 错误 | 确认 database_id 正确 |

### 错误响应处理

如果 API 调用失败：
1. 显示错误信息
2. 提供可能的原因
3. 建议用户检查 Notion 设置

```
❌ 保存失败

错误信息：{error_message}

可能的原因：
1. API key 无效或过期
2. Integration 没有数据库写入权限
3. 数据库 ID 不正确

请检查：
- settings.json 中的 NOTION_API_KEY 是否正确
- 数据库是否已连接到 Integration
```

---

## 完整示例

### 示例 1: GitHub 仓库（工具包）带最佳实践

**用户输入：**
```
保存这个工具：https://github.com/datawhalechina/hello-agents
```

**执行步骤：**

1. **访问页面** - 通过 GitHub API 获取仓库信息
2. **提取内容：**
   - 名称："hello-agents"
   - 描述："📚 《从零开始构建智能体》——从零开始的智能体原理与实践教程"
   - 类型："工具包"（Python 教程项目）
   - 标签：["GitHub", "Python", "AI", "Agent", "LLM", "教程", "开源"]
   - 图标：🐍（Python 项目）
   - 封面图：`https://opengraph.githubassets.com/1/datawhalechina/hello-agents`
3. **生成最佳实践：**
   - 适用场景：学习 Agent 开发、LLM 应用构建
   - 快速开始：克隆仓库 → 安装依赖 → 运行示例
   - 核心技巧：按章节顺序学习、动手实践每个示例
   - 注意事项：需要 Python 基础、部分示例需要 API key
   - 相关资源：官方文档、Datawhale 社区
4. **调用 API 保存**

**返回结果：**
```
✅ 已保存到 Notion 工具箱

📌 名称：hello-agents
🔗 URL: https://github.com/datawhalechina/hello-agents
📁 类型：工具包
🏷️ 标签：GitHub, Python, AI, Agent, LLM, 教程, 开源
📝 简介：📚 《从零开始构建智能体》——从零开始的智能体原理与实践教程
🎨 图标：🐍
🖼️ 封面：顶部封面 + 正文图片
📖 最佳实践：已生成（适用场景、快速开始、核心技巧、注意事项、相关资源）

🔗 [在 Notion 中查看](https://www.notion.so/hello-agents-xxxx)
```

### 示例 2: AI 工具网站

**用户输入：**
```
把这个加到工具箱：https://claude.ai
```

**返回结果：**
```
✅ 已保存到 Notion 工具箱

📌 名称：Claude
🔗 URL: https://claude.ai
📁 类型：网站
🏷️ 标签：AI, 聊天机器人, 大模型, SaaS
📝 简介：Anthropic 开发的 AI 助手
🎨 图标：🤖
🖼️ 封面：顶部封面 + 正文图片
📖 最佳实践：已生成

🔗 [在 Notion 中查看](https://www.notion.so/Claude-xxxx)
```

### 示例 3: Chrome 插件

**用户输入：**
```
保存这个 Chrome 插件：https://chromewebstore.google.com/detail/xxx
```

**返回结果：**
```
✅ 已保存到 Notion 工具箱

📌 名称：xxx
🔗 URL: https://chromewebstore.google.com/detail/xxx
📁 类型：浏览器插件
🏷️ 标签：Chrome, 生产力, AI
📝 简介：xxx 插件描述
🎨 图标：🔌
🖼️ 封面：顶部封面 + 正文图片
📖 最佳实践：已生成

🔗 [在 Notion 中查看](https://www.notion.so/xxx-xxxx)
```

---

## 环境变量

确保 `settings.json` 中配置了：

```json
{
  "env": {
    "NOTION_API_KEY": "ntn_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  }
}
```

## ⚠️ 重要：数据库权限设置

在保存工具到 Notion 之前，**必须将数据库共享给 integration**：

1. 打开 Notion 中的"工具箱"数据库
2. 点击右上角的 **"···"** (更多按钮)
3. 选择 **"Connect to"** 或 **"Add connections"**
4. 选择你的 integration 名称（例如 "openclaw"）
5. 确认连接

或者：
1. 打开 https://www.notion.so/my-integrations
2. 点击你的 integration
3. 点击 **"Add to workspace"** 或 **"Connected workspaces"**
4. 确保选择了正确的工作区
5. 然后在 Notion 中打开数据库，点击右上角 **"Share"**
6. 在 Search people 中搜索你的 integration 名称并添加

---

## 快速参考

### API 调用完整模板

```bash
curl -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2021-05-13" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "6f7bb9cc-ac01-41c5-9856-fb1568d197ae"},
    "icon": {"type": "emoji", "emoji": "🤖"},
    "cover": {
      "type": "external",
      "external": {"url": "https://.../cover-image.jpg"}
    },
    "children": [
      {
        "object": "block",
        "type": "image",
        "image": {
          "type": "external",
          "external": {"url": "https://.../cover-image.jpg"}
        }
      },
      {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
          "rich_text": [{"type": "text", "text": {"content": "🎯 最佳实践"}}]
        }
      },
      {
        "object": "block",
        "type": "heading_3",
        "heading_3": {
          "rich_text": [{"type": "text", "text": {"content": "适用场景"}}]
        }
      },
      {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
          "rich_text": [{"type": "text", "text": {"content": "..."}}]
        }
      }
    ],
    "properties": {
      "Name": {"title": [{"text": {"content": "名称"}}]},
      "URL": {"url": "https://..."},
      "简介": {"rich_text": [{"text": {"content": "描述"}}]},
      "类型": {"multi_select": [{"name": "软件"}]},
      "标签": {"multi_select": [{"name": "标签 1"}]},
      "⭐ 置顶": {"checkbox": false}
    }
  }'
```

**注意：** API 版本使用 `2021-05-13` 以支持 `children` 参数。

### 类型列表（仅限这 5 个）

**软件** | **网站** | **浏览器插件** | **Prompt** | **工具包**

### 图标选择速查

| 场景 | 推荐图标 |
|------|---------|
| Python 项目 | 🐍 |
| JavaScript/Node | 📜 |
| AI/LLM/Agent | 🤖 |
| 设计工具 | 🎨 |
| 开发工具 | 🛠️ |
| 学习/教程 | 📚 |
| 云服务 | ☁️ |
| 安全/隐私 | 🔒 |
| 生产力 | ⚡ |
| 数据分析 | 📊 |
| 默认 | 💻 |

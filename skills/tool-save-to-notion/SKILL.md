---
name: tool-save-to-notion
description: "Save tool links to Notion Toolbox. Use this skill whenever user provides ANY tool URL (GitHub, official website, product page, AI tool, browser extension, software, online service) and wants to save it to Notion. This skill automatically extracts tool info (name, type, tags, description) from the page and saves it as a structured database entry. Common triggers: 保存这个工具, 添加到工具箱, 收藏这个链接, save this tool, add to toolbox."
version: 1.1.0
metadata:
  homepage: https://github.com/victor-skills#tool-save-to-notion
---

# tool-save-to-notion

自动将工具链接保存到 Notion 工具箱数据库，包含图标、封面和最佳实践指南。

## 何时使用

用户提供以下任一链接时立即触发：
- GitHub 仓库、工具官网、AI 工具页面
- 浏览器插件商店、在线服务/网页工具
- npm/PyPI 等包页面
- 任何用户说"保存"、"收藏"、"添加到工具箱"的链接

## 核心流程

```
接收 URL → 提取页面信息 → 选择图标 → 生成最佳实践 → 调用 Notion API 保存
```

## Step 1: 提取页面信息

使用 WebFetch 访问 URL，按域名规则提取（详见 [references/extraction-rules.md](references/extraction-rules.md)）：
1. 工具名称、描述、关键词
2. 页面类型（按域名 + 内容特征判定）
3. 封面图 URL（可选）

## Step 2: 选择图标

根据工具特征选择 emoji（详见 [references/icon-guide.md](references/icon-guide.md)）：
1. 明确特征优先（Python → 🐍）
2. 功能领域次之（AI → 🤖）
3. 类型默认兜底

## Step 3: 生成最佳实践

根据工具类型自动生成正文内容：
- 适用场景 → 快速开始 → 核心技巧 → 注意事项 → 相关资源

各类型重点详见 [references/notion-api.md](references/notion-api.md)。

## Step 4: 保存到 Notion

调用 Notion API 创建页面（属性 + 封面 + 正文 + icon）。
API 模板和字段定义见 [references/notion-api.md](references/notion-api.md)。

## 验证

- [ ] 页面已创建，URL 可访问
- [ ] 类型、标签已正确设置
- [ ] 最佳实践内容已生成
- [ ] 图标和封面已设置

## 返回结果

```
✅ 已保存到 Notion 工具箱
📌 名称：{name}
🔗 URL: {url}
📁 类型：{type}
🏷️ 标签：{tags}
🎨 图标：{icon}
🔗 [在 Notion 中查看]({page_url})
```

## 类型列表（仅限 5 个）

软件 | 网站 | 浏览器插件 | Prompt | 工具包

# Notion API 参考

## 数据库信息

| 名称 | 值 |
|------|-----|
| 工具箱 Database ID | `6f7bb9cc-ac01-41c5-9856-fb1568d197ae` |
| API 版本 | `2021-05-13`（支持 children 参数） |

## 数据库字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| Name | title | ✅ | 工具名称 |
| 类型 | multi_select | ✅ | 软件/网站/浏览器插件/Prompt/工具包 |
| 标签 | multi_select | ✅ | 技术标签 |
| URL | url | ✅ | 原始链接 |
| 简介 | rich_text | ✅ | 1-2 句话描述 |
| ⭐ 置顶 | checkbox | ❌ | 默认 false |
| 创建时间 | created_time | 自动 | — |
| 更新时间 | last_edited_time | 自动 | — |

## 创建页面 API

```bash
curl -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2021-05-13" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "6f7bb9cc-ac01-41c5-9856-fb1568d197ae"},
    "icon": {"type": "emoji", "emoji": "🤖"},
    "cover": {"type": "external", "external": {"url": "https://..."}},
    "children": [
      {"object": "block", "type": "image", "image": {"type": "external", "external": {"url": "https://..."}}},
      {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "🎯 最佳实践"}}]}},
      {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": "适用场景"}}]}},
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "..."}}]}}
    ],
    "properties": {
      "Name": {"title": [{"text": {"content": "名称"}}]},
      "URL": {"url": "https://..."},
      "简介": {"rich_text": [{"text": {"content": "描述"}}]},
      "类型": {"multi_select": [{"name": "软件"}]},
      "标签": {"multi_select": [{"name": "标签1"}]},
      "⭐ 置顶": {"checkbox": false}
    }
  }'
```

## 最佳实践内容结构

根据工具类型自动生成：

| 工具类型 | 最佳实践重点 |
|---------|-------------|
| 软件 | 安装配置、快捷键、工作流集成、效率技巧 |
| 网站 | 使用场景、核心功能、付费方案、替代方案 |
| 浏览器插件 | 安装方式、使用技巧、隐私设置、冲突排查 |
| Prompt | 使用场景、优化技巧、变量设置、效果对比 |
| 工具包 | 安装命令、基础用法、进阶配置、版本兼容 |

正文结构：适用场景 → 快速开始（3-5 步）→ 核心技巧（3-5 个）→ 注意事项 → 相关资源

## 数据库权限

保存前必须将数据库共享给 integration：
1. 打开 Notion 工具箱数据库
2. 点击右上角 ··· → Connect to → 选择 integration
3. 或在 https://www.notion.so/my-integrations 配置

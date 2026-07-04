# Notion API 参考

## 数据库信息

| 名称 | ID |
|------|-----|
| 音乐数据库 databaseId | `3550f06d1a7f800ea4adf722d176a2e0` |
| 音乐 Data Source ID | `3550f06d-1a7f-80df-bb22-000b73a97e67` |
| 领域数据库 databaseId | `ac9e08fc-67f9-423f-a141-49ac44be6bf2` |

## API 版本

- 页面/数据库操作：`Notion-Version: 2022-06-28`
- 文件上传专属：`Notion-Version: 2025-09-03`

## 创建页面 API

```bash
NOTION_KEY=$(cat ~/.config/notion/api_key)
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "3550f06d1a7f800ea4adf722d176a2e0"},
    "icon": {"type": "emoji", "emoji": "💿"},
    "cover": {"type": "file_upload", "file_upload": {"id": "<FILE_ID>"}},
    "properties": {
      "名称": {"title": [{"text": {"content": "<名称>"}}]},
      "类型": {"select": {"name": "专辑"}},
      "原唱": {"rich_text": [{"text": {"content": "<歌手>"}}]},
      "🎵 流派/曲风": {"multi_select": [{"name": "<流派>"}]},
      "发行时间": {"date": {"start": "<YYYY-MM-DD>"}}
    }
  }'
```

## 添加正文内容

使用 `PATCH /v1/blocks/{page_id}/children` 添加 Notion blocks：
- 标题 → `heading_1`, `heading_2`
- 段落 → `paragraph`
- 列表项 → `bulleted_list_item`
- 引用 → `quote`
- 分割线 → `divider`

每批不超过 100 个 blocks，Rate limit ~3 req/s，批量间 `sleep 0.4`。

## 经典歌词区块

单曲页面正文末尾添加经典歌词（2-4 句，每句一个 `quote` block）：

```json
{
  "object": "block",
  "type": "heading_2",
  "heading_2": {"rich_text": [{"type": "text", "text": {"content": "📜 经典歌词"}}]}
}
```

## Notion Files API（封面上传）

```bash
FILES_API_URL="https://api.notion.com/v1/file_uploads"
NOTION_KEY=$(cat ~/.config/notion/api_key)

# 1. 创建上传对象
curl -s -X POST "$FILES_API_URL" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d "{\"filename\":\"cover.jpg\",\"content_type\":\"image/jpeg\"}"

# 2. 发送文件（使用返回的 file_upload ID）
curl -s -X POST "$FILES_API_URL/{file_id}/send" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -F "file=@/path/to/cover.jpg;filename=cover.jpg"
```

## Icon 选择指南

### 按类型
| 类型 | 推荐 icon |
|------|----------|
| 单曲 | 🎵 🎶 🎧 |
| 专辑 | 💿 📀 🎼 |
| 歌手 | 🎤 🎹 🎸 |

### 按流派（单曲）
| 流派 | 推荐 icon |
|------|----------|
| 流行 | 🎵 🎶 |
| 摇滚 | 🎸 🔥 |
| 民谣 | 🎸 🌿 |
| R&B | 🎤 💜 |
| 嘻哈 | 🎤 🔊 |
| 电子 | 🎛️ ⚡ |
| 抒情 | 🎹 💫 |
| 中国风 | 🏮 🎋 |
| 古典 | 🎻 🎼 |
| 爵士 | 🎷 🌙 |

## 类型选项
单曲 / 专辑 / 歌手

## 流派选项
民谣 / 嘻哈 / 乡村 / 古典 / R&B / 流行 / 摇滚 / 抒情 / 中国风

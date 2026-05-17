# Reddit Daily Digest Output Format

## Notion 格式规范

### 页面结构（从上到下）

1. **heading_1**: `📰 Reddit r/{subreddit} 每日速递 - {date}`
2. **callout** (💡): 日期 + 精选数量 + 数据来源
3. **paragraph**: `📌 **文章速览：**`
4. **bulleted_list_item** × N: 每篇 `**{标题}**：{一句话摘要}`
5. **divider**
6. 对每篇文章：
   - **heading_2**: `文章 {N}`
   - **paragraph**: 带链接的标题
   - **paragraph**: 元信息
   - **callout** (📋): 一句话摘要
   - **callout** (🎯): 核心要点
   - **callout** (💡): 可实践建议
   - **callout** (✨): 创作灵感
   - **divider**
   - **callout** (🐦): Twitter/X 文案
   - **callout** (📱): 即刻文案
   - **paragraph**: 带链接的 `查看 Reddit 原文`
   - **divider**
7. **callout** (📊): 今日统计

## 社交媒体文案规则

**仅保留 Twitter/X 和 即刻两个平台，均为简体中文。**

**Twitter/X**: 1-2 短段落，hook 开头，少量 emoji，结尾带链接
**即刻**: 简洁技术总结，3-5 条 bullet 或短段落 + 链接

## Notion API 链接格式

```python
# 正确格式（使用 text.link.url）
{"text": {"content": "文本", "link": {"url": "https://..."}}}

# 错误格式（顶层 href 会被忽略）
{"text": {"content": "文本"}, "href": "https://..."}  # ❌
```

## Notion 文献库字段

- **Name**: `Reddit r/{subreddit} 每日速递 - {date}`
- **URL**: `https://www.reddit.com/r/{subreddit}/`
- **文献类型**: `资讯文章`
- **🚩 领域**: 关联到 `AI人工智能探索` (ed5986fc-f0ad-40ce-8f42-f024f9fdc682)
- **标签**: `AI`, `AI编程`, `Reddit`, `资讯`, `Vibe Coding`
- **摘要**: `今日精选 {N} 篇 r/{subreddit} 高价值帖子摘要`

---
name: reddit-daily-digest
description: >
  抓取指定 subreddit 最近 24 小时帖子，分析筛选高质量内容，按《Reddit r/vibecoding 每日速递》格式
  生成 Notion 页面写入文献库。
  触发词：reddit 每日速递、subreddit 日报、Reddit digest、Reddit daily、Reddit 每日摘要、
  抓取 subreddit、reddit 热点总结
version: 1.0.0
metadata:
  homepage: https://github.com/victor-skills#reddit-daily-digest
---

# Reddit Daily Digest

抓取指定 subreddit 最近帖子，筛选高质量内容，生成社交媒体文案，写入 Notion 文献库。

## 核心流程

### 1. 确定参数

默认 subreddit: `vibecoding`，可通过用户指令指定。

```bash
SUBREDDIT="${1:-vibecoding}"
DATE=$(date +%Y-%m-%d)
WORK_DIR="/Users/victor/Desktop/Inbox/temp/reddit_${SUBREDDIT}_${DATE}"
mkdir -p "$WORK_DIR"
```

### 2. 抓取帖子列表

使用 `opencli reddit` 获取帖子（new 排序，limit 100 覆盖 24 小时）：

```bash
~/.npm-global/bin/opencli reddit subreddit "$SUBREDDIT" --sort new --limit 100 -f json > "$WORK_DIR/posts_list.json"
```

### 3. 抓取每篇帖子详情和评论

遍历帖子列表，用 `opencli reddit read` 获取详情：

```bash
~/.npm-global/bin/opencli reddit read "$post_id" --sort top --limit 50 --depth 3 --max-length 3000 -f json > "$WORK_DIR/post_${post_id}.json"
# 每次请求间 sleep 2-3s 避免限流
```

可用 `scripts/fetch_posts.sh` 自动化批量抓取。

### 3.5 解析帖子创建时间

⚠️ `opencli reddit` 返回的 `time` 字段为 Unix 时间戳，需转换为北京时间（UTC+8）显示。

**Python 转换示例：**

```python
import datetime

def format_time(unix_ts):
    """Unix 时间戳 → 北京时间字符串"""
    if not unix_ts:
        return "未知"
    dt = datetime.datetime.fromtimestamp(unix_ts, tz=datetime.timezone(datetime.timedelta(hours=8)))
    return dt.strftime("%Y-%m-%d %H:%M CST")
```

从帖子列表 JSON 中直接读取 `time` 字段转换，无需额外请求：
```python
for p in posts:
    created_time = format_time(p.get('time'))
```

将 `created_time` 存入对应文章数据。

### 4. 质量筛选

**⚠️ 必须先按时间过滤，再评分选取。**

第一步：时间过滤——仅保留最近 24 小时内的帖子：

```python
import datetime

now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))
cutoff = now - datetime.timedelta(hours=24)

recent_posts = []
for p in posts:
    ts = p.get('time', 0)
    if ts:
        dt = datetime.datetime.fromtimestamp(ts, tz=datetime.timezone(datetime.timedelta(hours=8)))
        if dt >= cutoff:
            recent_posts.append(p)
```

第二步：在过滤后的帖子中评分选取（score = upvotes + comments × 0.5），取前 8 篇。

质量判定标准（满足至少 2 项）：

- **Upvotes >= 50**（或排名前 30%）
- **Comments >= 10**
- **内容深度**: 正文 > 200 字符或包含代码/教程
- **主题相关性**: AI 编程、开发工具、独立开发等
- **新颖性**: 独特视角、项目展示、经验教训

排除：纯 meme、低质量灌水、重复帖、NSFW。

### 5. 分析生成内容

对每篇精选文章提取：

- 📋 一句话摘要（15-30 字，概括核心内容）
- 🎯 核心要点 (3-5 条)
- 💡 可实践建议 (2-4 条)
- ✨ 创作灵感 (2-3 条)
- 两个平台的社交媒体文案（**Twitter/X**、**即刻**，均为简体中文）

### 6. 写入 Notion 文献库

数据库 ID: `8f68db8a-3a48-4541-a3a7-4978eb9453e2`

**⚠️ Notion API 关键注意事项：**

1. **链接必须使用 `text.link.url` 格式**，顶层 `href` 会被忽略：
   ```python
   {"text": {"content": "点击这里", "link": {"url": "https://..."}}}
   ```

2. **加粗使用 `annotations.bold = true`**：
   ```python
   {"text": {"content": "加粗文字"}, "annotations": {"bold": True}}
   ```

3. **Markdown 转换函数 `rt(text)` 规则**：
   - `**bold**` → content="bold", annotations.bold=True
   - `[text](url)` → content="text", text.link={"url": "url"}
   - `[**text**](url)` → 需先剥离 ** 再创建链接（content="text", text.link=...）

**页面结构（从上到下）：**

1. **heading_1**: `📰 Reddit r/{subreddit} 每日速递 - {date}`
2. **callout** (💡): 日期 + 精选数量 + 数据来源
3. **paragraph**: `📌 **文章速览：**`
4. **bulleted_list_item** × N: 每篇 `**{标题}**：{一句话摘要}（{创建时间}）`
5. **divider**
6. 对每篇文章：
   - **heading_2**: `文章 {N}`
   - **paragraph**: 带链接的标题（`text.link.url` 格式，可点击跳转）
   - **paragraph**: 元信息（`🔥 {upvotes} 票 | 💬 {comments} 条评论 | 🕐 {创建时间}`）
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

**步骤 A**: 创建页面（带前 50 blocks）
**步骤 B**: 分批追加剩余 blocks（每批 50）
**步骤 C**: 返回页面链接

### 7. 清理

删除中间 JSON 文件和临时脚本。

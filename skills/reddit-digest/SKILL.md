---
name: reddit-digest
description: |
  抓取指定单个 Subreddit 最近 24 小时热门 Post，逐一获取详情与评论，生成摘要、核心要点、可实践建议、灵感启发及社交媒体分享文案，输出为每日精选 Markdown 文档。
  当用户说"帮我抓取/总结 Reddit r/xxx"、"生成 Reddit 每日摘要"、"reddit digest"时使用。
---

# Reddit Subreddit 每日摘要

## 配置

优先级：命令行参数 > 环境变量 > 默认值

| 参数 | 环境变量 | 默认值 |
|------|---------|--------|
| `--base-dir` | `REDDIT_DIGEST_BASE_DIR` | `/Users/victor/Desktop/resource/daily-info/reddit` |
| `--subreddit` | `REDDIT_DIGEST_SUBREDDIT` | `ClaudeAI` |

输出路径：`{BASE_DIR}/{YYYYMMDD}/{subreddit_name}/{subreddit_name}-{YYYYMMDD}.md`
临时目录：`{BASE_DIR}/{YYYYMMDD}/{subreddit_name}/temp/`

## 依赖

- **autocli**：获取热门列表和 Post 详情
- **scripts/fetch_post_details.py**：批量并发获取所有 Post 详情，保存到临时目录

## 执行流程

### Step 1: 初始化

确定 `BASE_DIR` 和 `SUBREDDIT`，创建输出目录和临时目录：

```bash
mkdir -p {BASE_DIR}/{YYYYMMDD}/{subreddit_name}/temp
```

### Step 2: 批量获取 Post 列表与详情

一条命令完成列表获取 + 批量详情抓取：

```bash
autocli reddit subreddit {subreddit_name} --limit 50 --sort top --time day --format json | \
  python3 {SKILL_DIR}/scripts/fetch_post_details.py --temp-dir {TEMP_DIR}
```

脚本**串行**调用 `autocli reddit read {url} -f json` 逐条抓取（autocli 基于浏览器，并发会导致 tab 冲突，默认 workers=1），每条 Post 保存为：

```
{TEMP_DIR}/{rank:02d}-{sanitized_title}.json
```

每个文件结构：

```json
{
  "rank": 1,
  "meta": { "author", "comments", "title", "upvotes", "url" },
  "content": [ { "author", "score", "text", "type" }, ... ],
  "error": null
}
```

`content` 字段：`type=POST` 为原文，`type=L0` 为顶层评论，`type=L1` 为回复。

**容错**：抓取失败时 `error` 字段记录原因，仅用 `meta` 元数据生成简要摘要。

### Step 3: 分析每个 Post

逐一读取 `{TEMP_DIR}/*.json`，按 rank 顺序分析，筛选并剔除低价值 Post。

输出文档结构与筛选规则见 [references/output-template.md](references/output-template.md)。

### Step 4: 汇总输出

将所有分析结果按 rank 排序合并，写入最终文档。所有内容**使用简体中文撰写**。

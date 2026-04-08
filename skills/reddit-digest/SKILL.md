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
- **agent-browser**：容错备用

## 执行流程

### Step 1: 初始化

1. 确定 `BASE_DIR` 和 `SUBREDDIT`
2. 若 `{BASE_DIR}/{YYYYMMDD}/{subreddit_name}/` 不存在则创建
3. `mkdir -p {TEMP_DIR}`

### Step 2: 获取 Post 列表

```bash
autocli reddit subreddit {subreddit_name} --limit 50 --sort top --time day --format json
```

返回字段：`author`, `comments`, `title`, `upvotes`, `url`

### Step 3: 逐一获取 Post 详情

```bash
autocli reddit read {post_url} -f json
```

返回字段：`author`, `score`, `text`, `type`（'POST'=原文，'L0'=评论）

**容错顺序**：autocli read → autocli 动态判断 → agent-browser → 仅用列表元数据生成简要摘要

### Step 4: 分析每个 Post

将分析结果写入 `{TEMP_DIR}/{rank}-{sanitized_title}.md`，筛选并剔除低价值 Post。

输出文档结构与筛选规则见 [references/output-template.md](references/output-template.md)。

### Step 5: 汇总输出

读取所有临时文件，按 rank 排序合并，写入最终文档。所有内容**使用简体中文撰写**。

---
name: hackernews-digest
description: |
  获取 Hacker News 热门文章并生成每日摘要。对每篇文章进行总结、提炼核心要点、给出可实践建议、灵感启发，以及生成社交媒体分享文案（即刻 + 小红书 + Twitter/X）。
  触发场景：用户提到 "HN 摘要"、"Hacker News 日报"、"hackernews digest"、"今日 HN"、"HN 热门"、"技术日报" 等。即使用户只说 "看看今天 HN 有什么"，也应触发此技能。
version: 1.1.0
metadata:
  homepage: https://github.com/victor-skills#hackernews-digest
---

# Hacker News 每日摘要

获取 Hacker News Top 10 热门文章，并行抓取原文，生成摘要、核心要点、可实践建议、灵感启发及社交媒体分享文案。

## 配置

| 方式 | 优先级 | 示例 |
|------|--------|------|
| `--base-dir` 参数 | 最高 | `--base-dir /tmp/hn` |
| `HN_DIGEST_BASE_DIR` 环境变量 | 中 | `export HN_DIGEST_BASE_DIR=...` |
| 默认值 | 最低 | `~/Desktop/resource/daily-info/hacknews` |

路径规则：
- 临时目录：`{BASE_DIR}/{YYYYMMDD}/temp/`
- 最终文档：`{BASE_DIR}/{YYYYMMDD}/hackernews-daily-{YYYYMMDD}.md`

## 核心流程

```
初始化 → 获取 Top 10 → 并行抓取分析 → 汇总生成文档
```

## Step 1: 初始化

1. 确定 `BASE_DIR`（参数 > 环境变量 > 默认值）
2. 获取日期，计算 `TEMP_DIR` 和 `OUTPUT_DIR`
3. 清理已存在文件
4. `mkdir -p {TEMP_DIR}`

## Step 2: 获取热门文章

```bash
autocli hackernews top --limit 10 --format json
```

## Step 3: 并行抓取与分析

为每篇文章创建并行 Agent：
1. WebFetch 抓取原文
2. 按模板生成分析
3. 写入 `{TEMP_DIR}/{rank}-{title}.md`

每篇文章输出：摘要 → 核心要点 → 可实践建议 → 灵感启发 → 社交媒体文案（即刻 + 小红书 + Twitter/X）。

## Step 4: 汇总生成文档

按 rank 排序合并，添加 front matter 和今日总结。

## 注意事项

- **并行化**：10 篇文章必须并行抓取
- **容错**：URL 不可访问时，用 autocli 动态判断，仍不行用 agent-browser
- **语言**：中文撰写
- **文案风格**：即刻轻松有态度、小红书吸睛有干货、Twitter 简洁专业

## 验证

- [ ] 10 篇文章全部抓取成功（或标注失败原因）
- [ ] 每篇包含摘要 + 核心要点 + 可实践建议 + 社交媒体文案
- [ ] 最终文档已生成，front matter 完整

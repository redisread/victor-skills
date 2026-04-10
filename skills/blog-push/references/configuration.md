# 环境变量配置与 Front Matter 参考

## 环境变量

在 `~/.zshrc` 或 `~/.bashrc` 中配置：

```bash
export HUGO_BLOG_DIR=/Users/victor/Desktop/project/github/HUGO_blog
export HUGO_POSTS_DIR=content/zh/posts          # 可选，默认值
export HUGO_DAILY_DIR=content/zh/daily          # 可选，默认值
export HUGO_WEEKLY_DIR=content/zh/weekly        # 可选，默认值
export HUGO_TEMPLATE_PATH=archetypes/default.md # 可选，默认值
export HUGO_DAILY_TEMPLATE=archetypes/daily.md  # 可选，默认值
export HUGO_WEEKLY_TEMPLATE=archetypes/weekly.md # 可选，默认值
```

优先级：**命令行参数 > 环境变量 > 默认值**

| 环境变量 | 默认值 |
|---------|--------|
| `HUGO_BLOG_DIR` | `.`（当前目录） |
| `HUGO_POSTS_DIR` | `content/zh/posts` |
| `HUGO_DAILY_DIR` | `content/zh/daily` |
| `HUGO_WEEKLY_DIR` | `content/zh/weekly` |
| `HUGO_TEMPLATE_PATH` | `archetypes/default.md` |
| `HUGO_DAILY_TEMPLATE` | `archetypes/daily.md` |
| `HUGO_WEEKLY_TEMPLATE` | `archetypes/weekly.md` |

## Front Matter 模板

### posts 类型（`archetypes/default.md`）

```yaml
---
title: "{{ 文章标题 }}"
subtitle:
date: {{ 自动生成 }}
publishDate: {{ 自动生成 }}
aliases:
description:
image: {{ 封面图（如果有） }}
draft: false
hideToc: false
enableToc: true
enableTocContent: false
tocPosition: inner
author: VictorHong
authorEmoji: 🪶
authorImageUrl:
tocLevels: ["h1","h2", "h3", "h4"]
libraries: [katex, mathjax, mermaid, chart, flowchartjs, msc, viz, wavedrom]
tags: []
series: []
categories: []
---
```

### daily 类型（`archetypes/daily.md`）

```yaml
---
title: "{{ 文章标题 }}"
date: {{ 自动生成 }}
publishDate: {{ 自动生成 }}
description:
tags:
  - AI
  - Daily Digest
categories:
  - AI
image:
---
```

### weekly 类型（`archetypes/weekly.md`）

```yaml
---
title: "{{ 年 }}-{{ 月 }} Weekly Log"
date: {{ 自动生成 }}
publishDate: {{ 自动生成 }}
description:
tags:
  - weekly
series:
categories:
  - weekly
image:
---
```

## 智能内容分析

脚本自动检测并添加 `libraries` 字段：

- **数学公式**（`$...$` 或 `$$...$$`）→ 添加 `katex`
- **Mermaid 图表**（`` ```mermaid ``）→ 添加 `mermaid`
- **图表内容**（`` ```chart/flowchart ``）→ 添加 `chart, flowchartjs`

智能分类建议关键词：
- **技术**: 代码、编程、开发、架构、API、数据库、Docker、Git
- **AI**: AI、机器学习、LLM、大模型、Claude、GPT、Prompt
- **生活**: 读书、电影、旅行、咖啡、美食、运动
- **思考**: 思考、方法论、职业规划、成长、效率、复盘

## 完整参数说明

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--type` | `-t` | `posts`/`daily`/`weekly` | `posts` |
| `--md` | `-m` | Markdown 文件路径 | 必需 |
| `--cover` | `-c` | 封面图片路径 | 可选 |
| `--category` | `-cat` | 分类目录（posts 必需） | - |
| `--name` | `-n` | 自定义文章名称 | 使用文件名 |
| `--draft` | `-d` | 标记为草稿 | false |
| `--tags` | - | 自定义标签（逗号分隔） | - |
| `--more-marker` | - | 在第一段后插入 `<!--more-->` 截断标记 | false |
| `--git-push` | - | 发布后自动 git add/commit/push | false |
| `--shortcodes` | - | 显示 Shortcodes 指南 | - |
| `--check-config` | - | 显示当前配置信息 | - |
| `--list-categories` | `-l` | 显示分类目录（posts） | - |
| `--list` | - | 显示现有文章（daily/weekly）| - |
| `--blog-dir` | - | 博客根目录（覆盖环境变量） | - |
| `--posts-dir` | - | 目标目录路径 | - |
| `--template` | - | 模板文件路径 | - |

## 注意事项

- 目标文章已存在时，脚本会警告并覆盖
- 原 Markdown 的 front matter 会被移除并由脚本重新生成
- 指定 `--category` 时会覆盖智能分类建议
- `--tags` 指定的标签会与智能建议标签合并去重
- `--posts-dir` 和 `--template` 支持相对路径（相对于 `--blog-dir`）或绝对路径
- `--more-marker`：若文章已包含 `<!--more-->` 则跳过，不重复插入
- `--git-push`：commit message 格式为 `新增: {文章名}`；push 失败会打印错误但不中断流程

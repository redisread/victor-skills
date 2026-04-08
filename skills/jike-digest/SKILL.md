---
name: jike-digest
description: |
  抓取指定即刻 Topic 最近 20 条内容，筛选有价值的 post，生成摘要、可实践建议、灵感启发，输出为每日精选 Markdown 文档。
  当用户说"帮我总结即刻 topic"、"即刻日报"、"jike digest"、"jike 摘要"、"即刻每日精选"、"抓取即刻 {topic_id}"时使用。
---

# 即刻 Topic 每日摘要

## 配置

优先级：命令行参数 > 环境变量 > 默认值

| 参数 | 环境变量 | 默认值 |
|------|---------|--------|
| `--topic-id` | `JIKE_TOPIC_ID` | （必填，无默认值） |
| `--base-dir` | `JIKE_DIGEST_BASE_DIR` | `/Users/victor/Desktop/resource/daily-info/jike` |

若 `topic-id` 未提供且无环境变量，报错并提示用户。

常用 Topic ID：

| Topic | ID |
|-------|----|
| AI 探索站 | 63579abb6724cc583b9bba9a |
| 产品经理的日常 | 563a2995306dab1300a32227 |
| 大产品小细节 | 57079a1526b0ab12002c29da |
| 副业探索小分队 | 65544021a2935ec6b005bcd2 |
| 薅羊毛小分队 | 5523d164e4b0466c6563cd30 |
| 科技圈大小事 | 597ae4ac096cde0012cf6c06 |

输出路径：`{BASE_DIR}/{YYYYMMDD}/jike-{topic_name}-{YYYYMMDD}.md`

## 依赖

- **autocli**：获取 Topic 内容

## 执行流程

### Step 1: 初始化

1. 确定 `TOPIC_ID` 和 `BASE_DIR`
2. 若 `{BASE_DIR}/{YYYYMMDD}/` 已存在则清空与当前 topic 相关文件
3. `mkdir -p {BASE_DIR}/{YYYYMMDD}`

### Step 2: 获取内容

```bash
autocli jike topic {topic_id} --limit 20 -f json
```

### Step 3: 筛选与分析

剔除低价值内容，对保留的 post 逐条生成分析。输出格式见 [references/output-template.md](references/output-template.md)。

### Step 4: 写入文档

将分析结果按模板写入输出文件，**使用简体中文撰写**，保持即刻社区轻松有态度的风格。

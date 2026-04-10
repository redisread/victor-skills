---
name: blog-push
description: Hugo 博客文章发布工具。支持三种内容类型：posts（博客文章）、daily（日报）、weekly（周报）。使用场景：(1) 用户需要发布博客文章到 Hugo，(2) "发布文章"、"publish blog"、"创建博客"、"发布日报"、"发布周报"，(3) 将完成的 Markdown 文档移动到对应目录。支持查看分类、选择目录、自动生成 front matter、处理封面图、草稿管理、环境变量配置、从任意目录执行。
---

# Hugo 博客文章发布技能

将 Markdown 文档发布到 Hugo 博客，支持 **posts**、**daily**、**weekly** 三种内容类型，可从任意目录执行。

## 快速开始

**1. 配置环境变量（一次性设置）**

```bash
# ~/.zshrc 中添加
export HUGO_BLOG_DIR=/Users/victor/Desktop/project/github/HUGO_blog
```

详细配置参考：[references/configuration.md](references/configuration.md)

**2. 检查配置**

```bash
python3 scripts/publish_blog.py --check-config
```

## 常用命令

### 查看分类/现有文章

```bash
# posts 类型 — 查看可用分类
python3 scripts/publish_blog.py --type posts --list-categories

# daily/weekly 类型 — 查看现有文章
python3 scripts/publish_blog.py --type daily --list
python3 scripts/publish_blog.py --type weekly --list
```

### 发布文章

```bash
# posts（需指定分类）
python3 scripts/publish_blog.py \
  --md ./my-article.md \
  --type posts \
  --category 技术

# daily / weekly（直接发布）
python3 scripts/publish_blog.py --md ./ai-news.md --type daily
python3 scripts/publish_blog.py --md ./weekly-log.md --type weekly
```

### 带封面图发布

```bash
python3 scripts/publish_blog.py \
  --md ./my-article.md \
  --cover ./cover.png \
  --type posts \
  --category AI
```

封面图会复制到文章目录，命名为 `{文章名}-cover.{扩展名}`。

### 其他常用选项

```bash
# 发布为草稿
python3 scripts/publish_blog.py --md ./draft.md --type daily --draft

# 自定义文章名和标签
python3 scripts/publish_blog.py \
  --md ./article.md \
  --type posts \
  --category AI \
  --name "我的自定义标题" \
  --tags "AI,Python,机器学习"

# 查看 Shortcodes 指南
python3 scripts/publish_blog.py --shortcodes
```

## 智能功能

脚本自动分析内容并增强 front matter：
- 检测数学公式（`$...$`）→ 自动添加 `katex` 库
- 检测 Mermaid 图表 → 自动添加 `mermaid` 库
- 根据内容关键词智能建议分类和标签（可被 `--category` / `--tags` 覆盖）

## 发布后步骤

```bash
cd $HUGO_BLOG_DIR
hugo server -D        # 本地预览：http://localhost:1313
hugo                  # 构建
git add . && git commit -m "发布：文章标题" && git push
```

## 参考文档

- **[references/configuration.md](references/configuration.md)** — 环境变量详情、Front Matter 模板、完整参数说明、注意事项
- **[references/shortcodes.md](references/shortcodes.md)** — zzo 主题 Shortcodes 完整使用示例（boxmd、alert、expand、tabs、img、button 等）

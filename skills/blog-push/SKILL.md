---
name: blog-push
description: Hugo 博客文章智能发布工具。用于"发布博客"、"推送到blog"、"post to blog"、"发布文章"、"发布日报"、"发布周报"等场景。Claude 主导完成：自动读取博客配置、智能分析内容提取标题/分类/标签、生成 front matter、添加 <!--more--> 截断标记、复制封面图、调用脚本写入文件、git push 一键发布。支持 posts/daily/weekly 三种内容类型，从任意目录执行。
version: 1.0.0
metadata:
  homepage: https://github.com/victor-skills#blog-push
---

# Hugo 博客文章发布

Claude(openclaw) 主导完成整个发布流程，无需用户手动填写参数。

## 发布流程

### 第 1 步：读取博客配置

优先从以下位置自动获取博客路径：
1. 环境变量 `$HUGO_BLOG_DIR`
2. 用户 MEMORY.md / USER.md 中记录的博客路径
3. 询问用户

```bash
echo $HUGO_BLOG_DIR   # 检查环境变量
```

### 第 2 步：智能分析文章内容

从用户提供的 Markdown 内容中自动提取：

- **标题**：从 front matter `title` 字段或正文一级标题提取
- **内容类型**：根据标题/内容判断是 posts / daily / weekly
  - `daily`：包含日期格式标题（如"2026-04-10 AI日报"）或明显的日报内容
  - `weekly`：包含周报/Weekly字样
  - `posts`：默认的博客文章
- **分类（category）**：查看博客目录下已有分类，结合内容智能选择
- **标签（tags）**：根据内容关键词提取，最多 5 个
- **封面图**：用户是否附带了图片路径

### 第 3 步：生成发布命令

根据分析结果，构造并执行脚本命令：

```bash
# posts 类型
python3 <skill_dir>/scripts/publish_blog.py \
  --md <文章路径> \
  --type posts \
  --category <分类> \
  --name "<标题>" \
  --tags "<tag1>,<tag2>" \
  --git-push \
  [--cover <封面图路径>] \
  [--draft]

# daily 类型
python3 <skill_dir>/scripts/publish_blog.py \
  --md <文章路径> \
  --type daily \
  --git-push

# weekly 类型
python3 <skill_dir>/scripts/publish_blog.py \
  --md <文章路径> \
  --type weekly \
  --git-push
```

`--git-push` 会在写入文件后自动执行 `git add / commit / push`。

> **脚本路径**：skill 安装后路径通常为 `~/.claude/skills/blog-push/scripts/publish_blog.py`，或使用项目内相对路径。

### 第 4 步：返回结果

告知用户：
- ✅ 文章写入路径
- ✅ git commit 信息
- ✅ push 结果（成功/失败原因）

---

## 直接调用模式（手动指定参数）

如果用户明确提供了参数，直接拼接命令执行，无需走 AI 分析流程：

```bash
python3 scripts/publish_blog.py --check-config          # 检查配置
python3 scripts/publish_blog.py --type posts --list-categories
python3 scripts/publish_blog.py --type daily --list
```

完整参数说明见：[references/configuration.md](references/configuration.md)

---

## 参考文档

- **[references/configuration.md](references/configuration.md)** — 环境变量、Front Matter 模板、完整参数说明
- **[references/shortcodes.md](references/shortcodes.md)** — zzo 主题 Shortcodes 参考（boxmd、alert、expand、tabs、notice 等）

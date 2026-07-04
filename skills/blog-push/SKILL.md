---
name: blog-push
description: Hugo 博客文章智能发布工具。用于"发布博客"、"推送到blog"、"post to blog"、"发布文章"、"发布日报"、"发布周报"等场景。Claude 主导完成：自动读取博客配置、智能分析内容提取标题/分类/标签、生成 front matter、添加 <!--more--> 截断标记、复制封面图、调用脚本写入文件、git push 一键发布。支持 posts/daily/weekly 三种内容类型，从任意目录执行。
version: 1.1.0
metadata:
  homepage: https://github.com/victor-skills#blog-push
---

# Hugo 博客文章发布

Claude 主导完成整个发布流程，无需用户手动填写参数。

## 核心流程

```
读取配置 → 分析内容 → 构造命令 → 执行发布
```

## Step 1: 读取博客配置

按优先级获取博客路径：
1. 环境变量 `$HUGO_BLOG_DIR`
2. MEMORY.md / USER.md 中记录的路径
3. 询问用户

## Step 2: 分析内容

从 Markdown 内容自动提取：
- **标题**：front matter 或正文一级标题
- **类型**：posts / daily / weekly（根据标题内容判断）
- **分类+标签**：查看已有分类，智能匹配
- **封面图**：用户附带的图片路径

## Step 3: 执行发布

```bash
# posts 类型
python3 <skill_dir>/scripts/publish_blog.py \
  --md <文章路径> --type posts \
  --category <分类> --name "<标题>" --tags "<tag1>,<tag2>" \
  --git-push [--cover <封面图路径>]

# daily / weekly 类型
python3 <skill_dir>/scripts/publish_blog.py \
  --md <文章路径> --type daily|weekly --git-push
```

`--git-push` 自动执行 `git add / commit / push`。

## Step 4: 返回结果

- ✅ 文章写入路径
- ✅ git commit 信息
- ✅ push 结果

## 参数说明

完整参数和 Front Matter 模板见 [references/configuration.md](references/configuration.md)。
zzo 主题 Shortcodes 见 [references/shortcodes.md](references/shortcodes.md)。

## 验证

- [ ] 文件已写入博客目录
- [ ] front matter 完整（title, date, tags, categories）
- [ ] `<!--more-->` 已添加
- [ ] git push 成功

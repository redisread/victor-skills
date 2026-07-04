---
name: article-images-gen
description: 文案插图专家，为文章生成手绘风格插图。风格：手绘、简约、整洁、留白、构图平衡、色调统一。Use when user asks to generate illustrations for articles, "为文章配图", "生成插图", or needs hand-drawn style images for content.
version: 1.0.5
metadata:
  homepage: https://github.com/victor-skills#article-images-gen
---

# Article Images Generator (文案插图专家)

专为文章生成手绘风格插图，使用 `opencli gemini image`（主）和 `opencli grok image`（降级）。

## 调用脚本

```bash
# 全自动生成配图（分析 → 大纲 → 提示词 → 图片 → 插入文章）
bun scripts/illustrator.ts path/to/article.md [--density <level>] [--output-dir <path>]

# 单张图片
bun scripts/main.ts --prompt "your prompt" [--image output.png]

# 批量 prompt
bun scripts/main.ts --promptfiles prompt1.md,prompt2.md
```

密度选项：`minimal` (1-2张) | `balanced` (3-4张) | `per-section`（推荐）| `rich` (5+张)

## 工作流程

1. **分析文案**：识别章节结构、核心论点、适合插图的位置
2. **生成大纲**：保存 `{outputDir}/outline.md`
3. **生成提示词**：保存 `{outputDir}/prompts/NN-hand-drawn-{slug}.md`
4. **生成图片**：Gemini（主）→ Grok（降级），保存到 `{outputDir}/`
5. **更新文章**：在对应章节后插入图片引用

## 生成策略

- **首选**：`opencli gemini image`（16:9 横版）
- **降级**：Gemini 失败时自动切换 `opencli grok image`
- **超时**：单次最长 300 秒

## 输出目录

固定输出到 `/tmp/imageGen/{YYYYMMDD}/{articleName}/`

## 验证

- [ ] 大纲和提示词文件已生成
- [ ] 图片数量符合密度要求
- [ ] 文章已更新图片引用

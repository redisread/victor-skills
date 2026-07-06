---
name: article-images-gen
description: "文案插图专家，为文章生成图片生成提示词（prompt）。风格：手绘、简约、整洁、留白、构图平衡、色调统一。Use when user asks to generate image prompts for articles, \"为文章配图\", \"生成插图提示词\", \"生成配图prompt\" or needs hand-drawn style image prompts for content. 输出标准化提示词供 opencli-assistant 后续生成图片。"
version: 2.0.0
metadata:
  homepage: https://github.com/victor-skills#article-images-gen
---

# Article Images Prompt Generator (文案插图提示词专家)

专为文章生成高质量图片生成提示词（prompt），专注于手绘风格插图。提示词可直接供 @opencli-assistant 使用 `opencli gemini image` / `opencli chatgpt image` / `opencli grok image` 生成图片。

## 调用脚本

```bash
# 全自动生成配图提示词（分析 → 大纲 → 提示词）
bun scripts/prompt-generator.ts path/to/article.md [--density <level>] [--output-dir <path>]

# 单张图片提示词
bun scripts/prompt-generator.ts --prompt "your description" [--output-dir <path>]

# 批量生成（从 prompt 文件列表）
bun scripts/prompt-generator.ts --promptfiles prompt1.md,prompt2.md [--output-dir <path>]
```

密度选项：`minimal` (1-2张) | `balanced` (3-4张) | `per-section`（推荐）| `rich` (5+张)

## 输出格式

每个提示词文件包含标准化的图片生成参数，可直接被 opencli-assistant 使用：

```markdown
---
illustration_id: 1
style: hand-drawn
article_section: "章节标题"
purpose: "配图目的"
---

## 提示词（Prompt）

Hand-drawn minimalist illustration: [主题描述]. Simple, clean, lots of white space, balanced composition, unified color tone, no text, no words, no letters.

## 生成参数

| 参数 | 值 |
|------|-----|
| 服务 | gemini（主）/ chatgpt（备选）/ grok（兜底） |
| 比例 | 16:9 |
| 风格 | 手绘、简约、留白 |
| 主色调 | [根据内容自动推断] |
| 辅助色 | [根据内容自动推断] |

## 执行命令

```bash
opencli gemini image "[提示词内容]" --rt 16:9 --op /tmp/imageGen/output -f json --timeout 300
```

## 备选命令

```bash
# 如果 gemini 失败
opencli chatgpt image "[提示词内容]" --rt 16:9 --op /tmp/imageGen/output -f json --timeout 300

# 兜底方案
opencli grok image "[提示词内容]" --out /tmp/imageGen/output -f json --timeout 300 --count 1
```
```

## 工作流程

1. **分析文案**：识别章节结构、核心论点、适合插图的位置
2. **生成大纲**：保存 `{outputDir}/outline.md`
3. **生成提示词**：保存 `{outputDir}/prompts/NN-hand-drawn-{slug}.md`
4. **输出标准化参数**：每个提示词包含完整生成参数和执行命令

## 提示词生成策略

- **分析内容**：提取关键词、引用、主题色彩
- **自动推断色调**：
  - 科技/AI/代码 → 蓝色/紫色系 + 青色/绿色系
  - 温暖/故事 → 橙色/黄色系 + 红色/粉色调
  - 自然/生态 → 绿色/青色系 + 黄色/橙色调
  - 商业/金融 → 深蓝/灰色系 + 金色/橙色调
- **风格统一**：手绘、简约、留白、无文字
- **构图**：16:9 横版，适合文章配图

## 输出目录

固定输出到 `/tmp/imageGen/{YYYYMMDD}/{articleName}/`

## 与 opencli-assistant 联动

1. SkillExpert 生成提示词文件 → 保存到输出目录
2. opencli-assistant 读取提示词 → 执行 `opencli gemini image` 生成图片
3. 生成失败时自动降级：`gemini` → `chatgpt` → `grok`

## 验证

- [ ] 大纲和提示词文件已生成
- [ ] 提示词数量符合密度要求
- [ ] 每个提示词包含完整的生成参数和执行命令
- [ ] 提示词可直接被 opencli-assistant 使用

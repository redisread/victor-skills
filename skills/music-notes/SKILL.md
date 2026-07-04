---
name: music-notes
description: 深度音乐研究 Agent。接收歌曲名、艺人、Apple Music/Spotify/YouTube 链接、歌词片段或听感，自动识别歌曲/专辑/歌手并进行深度研究，生成高质量音乐研究笔记，写入 Notion 音乐数据库（使用类型字段区分）。触发词：音乐研究、研究这首歌、music research、分析这首歌、记录音乐、专辑研究、歌手研究。
version: 1.1.0
metadata:
  homepage: https://github.com/victor-skills#music-notes
---

# Music Research - 深度音乐研究

接收歌曲名、艺人、音乐链接或听感，自动识别类型并深度研究，写入 Notion 音乐数据库。

## 核心流程

```
输入 → 识别类型(单曲/专辑/歌手) → smart-search 搜集信息 → 提取关键信息 → 深度研究 → 生成笔记 → 写入 Notion
```

## Step 1: 识别输入类型

| 类型 | 触发场景 |
|------|---------|
| 单曲 | 歌曲名、单曲链接（Apple Music 含 `?i=`）、歌词片段 |
| 专辑 | 专辑名、提到"专辑"、专辑链接 |
| 歌手 | 歌手名、提到"歌手"、艺人链接 |

默认：输入歌曲名 → 单曲。

## Step 2: 搜集音乐信息

调用 `smart-search` skill 搜索，策略：
1. `opencli list -f yaml` 预检可用源
2. 中文内容优先 `doubao`，英文优先 `grok`/`gemini`
3. 不足时补充专用源（豆瓣音乐、Genius）

搜索关键词模板见 [references/research-dimensions.md](references/research-dimensions.md)。

## Step 3: 提取关键信息

从搜索结果中提取对应类型的必须字段（详见 [references/research-dimensions.md](references/research-dimensions.md)）。
信息不足时明确告知用户，不编造。

## Step 4: 深度研究

根据类型选择研究维度（详见 [references/research-dimensions.md](references/research-dimensions.md)），动态选取最值得分析的方向。

单曲正文末尾添加「📜 经典歌词」区块（2-4 句，每句一个 quote block）。

## Step 5: 写入 Notion

1. 封面图：`opencli gemini image` 生成 → Notion Files API 上传
2. 创建页面：设置属性 + 封面 + icon
3. 添加正文：Markdown → Notion blocks

API 调用详情、Icon 选择、类型/流派选项见 [references/notion-api.md](references/notion-api.md)。

## 验证

- [ ] 页面已创建，URL 可访问
- [ ] 类型字段正确（单曲/专辑/歌手）
- [ ] 正文包含研究内容，不重复属性信息
- [ ] 单曲包含经典歌词区块

## 错误处理

| 问题 | 处理 |
|------|------|
| 无法识别 | 告知用户，请提供更准确信息 |
| 部分信息缺失 | 标记「无法确认」，不编造 |
| 同名内容冲突 | 列出选项让用户确认 |
| Notion API 429 | 等待后重试 |
| 封面生成失败 | 跳过封面，页面不设 cover |

---
name: x-following-digest
version: 2.0.0
description: "获取 Twitter/X Following 最近 24 小时精选推文（含 RT 转发），自动获取原帖完整内容，生成摘要分析和社交媒体文案。当用户提到 '获取 following 推文'、'following 推文摘要'、'推特关注列表 digest' 或类似请求时触发使用。"
metadata:
  homepage: https://github.com/victor-skills#x-following-digest
---

# X Following Digest

获取 Twitter/X 关注列表（Following）最近 24 小时的精选推文，进行智能筛选和深度分析。**v2.0 更新：不再排除 RT 内容，自动获取转发的原帖完整内容。**

## 触发场景

- "获取我 following 的推文摘要"
- "分析关注列表的推文"
- "生成 Twitter following digest"
- "获取推特关注列表的精选内容"
- "following 推文分析"
- "X 关注列表每日精选"

## 工作流程

### 1. 获取推文数据

使用 autocli 获取 following 的最近 300 条推文：

```bash
autocli twitter timeline --type following --limit 300 -f json
```

### 2. 筛选最近 24 小时推文

使用当前时间（UTC）筛选出 created_at 在最近 24 小时内的推文。

获取当前时间的命令：
```bash
date -u +"%a %b %d %H:%M:%S %z %Y"
```

Twitter 时间格式示例：`Sat Apr 11 00:15:15 +0000 2026`

筛选逻辑：
- 解析每条推文的 `created_at` 字段
- 只保留距离当前时间不超过 24 小时的推文
- 保持原始 JSON 结构不变

### 3. 保存原始数据

将筛选后的推文保存到：

```
${X_DIGEST_BASE_DIR}/x/${DATE}/xFollowingRaw-${TIMESTAMP}.json
```

- `X_DIGEST_BASE_DIR`: 基础目录，默认为 `/Users/victor/Desktop/resource/daily-info/`
- `DATE`: 当前日期，格式 `YYYYMMDD`（如 20260411）
- `TIMESTAMP`: 当前执行时间戳，格式 `YYYYMMDDHHMMSS`

### 4. 智能内容筛选与 RT 原帖获取

#### 4.1 内容筛选

从筛选后的推文中识别高质量内容：

**排除标准：**
- 纯新闻短讯（只陈述事实，无观点）
- 广告/推广内容
- 少于 50 个字符的碎碎念
- 纯表情符号或图片无文字内容
- 过于个人化的日常分享（如"今天吃了什么"）

**高质量内容特征：**
- 有独特观点或见解
- 分享经验、教程或技术内容
- 引发深度讨论的话题
- 有价值的学习资源
- 行业洞察或分析
- **RT 转发的内容（不再排除，会自动获取原帖详情）**

#### 4.2 RT 转发内容处理

对于 RT（转发）类型的推文，**不再排除**，而是自动获取原帖的完整内容：

**识别 RT 推文：**
- 推文文本以 `RT @username:` 开头

**RT 原帖内容获取：**
1. 首先尝试使用 `autocli twitter thread <tweet-id> -f json` 获取完整 thread
2. 如果 thread 获取失败，尝试使用 `autocli twitter article <tweet-id> -f json` 获取 X 文章
3. 每次获取超时时间为 30 秒

**扩展 JSON 结构：**

```json
{
  "author": "ylecun",
  "created_at": "Sat Apr 11 04:12:07 +0000 2026",
  "id": "2042817948771922398",
  "text": "RT @SenMarkKelly: In the middle of a historic mission...",
  "url": "https://x.com/ylecun/status/2042817948771922398",
  "is_retweet": true,
  "retweeted_content": {
    "original_author": "SenMarkKelly",
    "original_tweet_id": "2042817948771922398",
    "preview_text": "原帖预览文本...",
    "original_url": "https://x.com/SenMarkKelly/status/2042817948771922398",
    "thread_content": [...],        // 如果成功获取 thread，为数组；否则为 null
    "article_content": {...},       // 如果成功获取 article，为对象；否则为 null
    "fetch_status": "thread_success",  // pending | thread_success | article_success | fetch_failed
    "fetch_error": null             // 错误信息（如果有）
  }
}
```

**获取状态说明：**
- `pending`: 尚未尝试获取
- `thread_success`: 成功获取 thread 内容（推文串）
- `article_success`: 成功获取 article 内容（X 文章）
- `fetch_failed`: 获取失败（超时或其他错误）

**注意：** 由于 Twitter/X 的访问限制，autocli 的 thread/article 命令可能无法成功获取。分析时会基于：
1. 优先使用成功获取的 thread_content 或 article_content
2. 如果获取失败，基于 preview_text 和可见部分进行分析

### 5. 生成深度分析报告

**分析步骤：**

1. 读取原始 JSON 文件（推荐使用 `-enriched.json` 增强版本，包含 RT 原帖内容）
2. 对每条推文进行深度分析
3. 生成最终的 Markdown 报告

**使用分析脚本：**

```bash
# 筛选高质量推文并获取 RT 原帖内容
python3 ${SKILL_DIR}/scripts/analyze.py ${RAW_FILE} ${OUTPUT_DIR}/temp-analysis.md
```

增强后的 JSON 文件会自动保存为 `${RAW_FILE%-enriched.json}-enriched.json`

**RT 推文特殊处理：**

对于 RT 转发推文，分析报告应包含：
- **转发信息**: 谁转发了这条推文
- **原帖作者**: @original_author
- **原帖链接**: 原帖完整 URL
- **获取状态**: thread_success / article_success / fetch_failed
- **原帖内容**:
  - 如果成功获取 `thread_content`：展示 thread 的内容摘要
  - 如果成功获取 `article_content`：展示 X 文章内容摘要
  - 如果获取失败：基于 `preview_text` 进行分析

**分析维度（使用简体中文）：**

1. **推文原文**
   - 保留原始文本
   - 如为英文，在后面追加简体中文翻译
   - 对于 RT 推文，同时展示原帖完整内容

2. **核心观点**
   - 提炼推文的核心论点或主旨
   - 用 1-2 句话概括
   - 对于 thread/article，总结主要论点和结论

3. **引用/转发内容**（如适用）
   - 原文引用内容（双语）
   - 引用来源链接
   - 对于 RT，提供原帖作者链接

4. **可实践建议**
   - 基于推文内容的具体行动建议
   - 可操作、可落地的步骤

5. **创作灵感**
   - 从推文延伸出的创意想法
   - 相关主题或角度的启发

6. **社交媒体分享文案**
   - **即刻**: 适合即刻平台的转发文案（简短、有观点，带 emoji）
   - **小红书**: 适合小红书的文案（emoji 丰富、口语化、亲切）
   - **推特**: 适合 Twitter/X 的英文文案（简洁、有 hook）

7. **原文链接**
   - 必须携带推文 URL
   - 对于 RT，同时提供原帖链接

### 6. 输出最终报告

将所有分析结果保存为 Markdown 文件：

```
${X_DIGEST_BASE_DIR}/x/${DATE}/xFollowingDigest-${TIMESTAMP}.md
```

**报告结构：**

```markdown
# X Following Digest - ${DATE}

生成时间：${生成时间}
筛选范围：最近 24 小时
精选推文数：${数量}
转发推文数：${RT 数量}
RT 原帖获取成功：${成功数量}

---

## 推文 1

**作者:** @{username}
**发布时间:** ${created_at}
**互动数据:** ${likes} likes, ${replies} replies, ${retweets} retweets

**原文:**
[推文内容]

**翻译:** [如原文为英文]

**核心观点:**
[核心观点摘要]

---

## 推文 2 - RT 转发

**转发者:** @{retweeter}
**发布时间:** ${created_at}

**🔄 原帖信息:**
- **原帖作者:** @{original_author}
- **原帖链接:** [原帖 URL]
- **获取状态:** thread_fetched/article_fetched/fetch_failed

**原帖内容:**
[如果是 thread，展示 thread 的内容摘要]
[如果是 article，展示文章内容摘要]

**翻译:** [如需要]

**核心观点:**
[核心观点摘要]

**可实践建议:**
- [建议 1]
- [建议 2]

**创作灵感:**
[灵感内容]

**社交媒体文案:**
- 🟠 即刻：[即刻文案]
- 🔴 小红书：[小红书文案]
- 🔵 推特：[Twitter 文案]

**原文链接:** [推文 URL]

---

## 汇总统计

- 总推文数：X
- 精选推文数：Y
- 转发推文数：Z
- RT 原帖获取成功：W
- 筛选率：P%
```

## 执行命令

### 方式一：全自动执行（推荐）

运行完整工作流：

```bash
bash ${SKILL_DIR}/scripts/run.sh
```

然后使用 Claude 完成分析：

```
请分析刚获取的推文数据 ${OUTPUT_DIR}/xFollowingRaw-${TIMESTAMP}-enriched.json 并生成最终报告
```

### 方式二：分步执行

**Step 1: 获取数据**
```bash
bash ${SKILL_DIR}/scripts/run.sh
```

**Step 2: 筛选高质量推文**
```bash
python3 ${SKILL_DIR}/scripts/analyze.py ${RAW_FILE}
```

**Step 3: 生成深度分析**
使用 Claude 分析筛选后的推文，生成最终报告并保存到 `${OUTPUT_DIR}/xFollowingDigest-${TIMESTAMP}.md`

## 配置说明

### 环境变量

- `X_DIGEST_BASE_DIR`: 输出基础目录（默认：`/Users/victor/Desktop/resource/daily-info/`）
- `X_RAW_LIMIT`: 获取推文数量（默认：300）

### 依赖工具

- `autocli`: 用于获取 Twitter/X 数据
- `date`: 用于时间处理
- `python3`: 用于 JSON 处理和筛选

### autocli 命令参考

```bash
# 获取推文时间线
autocli twitter timeline --type following --limit 300 -f json

# 获取推文 thread（原帖 + 回复）
autocli twitter thread <tweet-id> -f json --limit 50

# 获取 X 文章（长内容）
autocli twitter article <tweet-id> -f json
```

## 输出文件说明

| 文件名 | 说明 |
|--------|------|
| `xFollowingRaw-YYYYMMDDHHMMSS.json` | 筛选后的原始推文数据（最近 24 小时） |
| `xFollowingRaw-YYYYMMDDHHMMSS-enriched.json` | 增强数据，包含 RT 原帖内容和获取状态 |
| `xFollowingDigest-YYYYMMDDHHMMSS.md` | 最终的深度分析报告 |

## 示例工作流程

```bash
# 1. 运行脚本获取数据
bash skills/x-following-digest/scripts/run.sh

# 输出:
# 🐦 X Following Digest
# =====================
# 生成时间：2026-04-11 12:30:45 UTC
# 输出目录：/Users/victor/Desktop/resource/daily-info/x/20260411
#
# 📥 Step 1: 获取 Following 推文 (limit: 300)...
# ✅ 获取完成，共 300 条推文
#    原始数据：/Users/victor/Desktop/resource/daily-info/x/20260411/xFollowingRaw-20260411123045.json
#
# ⏰ Step 2: 筛选最近 24 小时的推文...
# ✅ 筛选完成，最近 24 小时共 45 条推文
#
# ✨ Step 3: 筛选高质量推文并获取 RT 原帖内容...
# ✅ 增强数据已保存：.../xFollowingRaw-20260411123045-enriched.json
#
# 📊 基础数据处理完成！

# 2. 使用 Claude 分析
# 在 Claude Code 中输入:
请分析文件 /Users/victor/Desktop/resource/daily-info/x/20260411/xFollowingRaw-20260411123045-enriched.json 中的推文，
筛选高质量内容并生成深度分析报告，保存到 /Users/victor/Desktop/resource/daily-info/x/20260411/xFollowingDigest-20260411123045.md
```

## 更新日志

### v2.0.0 (2026-04-11)

- **不再排除 RT 内容**：RT 转发内容现在会被保留并分析
- **自动获取原帖**：使用 `autocli twitter thread` 和 `autocli twitter article` 自动获取 RT 原帖的完整内容
- **扩展 JSON 结构**：`retweeted_content` 新增 `thread_content`、`article_content`、`fetch_status` 字段
- **改进分析报告**：RT 推文分析现在包含原帖完整内容和获取状态

### v1.0.0

- 初始版本

---
name: bloomscroll-style-writer
description: Generate personal reflection articles in the Bloomscroll newsletter style (mymind). Warm, self-deprecating, first-person voice with curated content sections. Each section has a 💭 title, personal reflection, and gentle humor. Trigger words: Bloomscroll风格, 个人随笔, 知识随笔, weekly digest, 写随笔.
version: 1.0.0
metadata:
  homepage: https://github.com/victor-skills#bloomscroll-style-writer
---

# Bloomscroll Style Writer

Generate articles in the style of mymind's **Bloomscroll** newsletter — warm, personal, self-deprecating reflections on curated topics.

## Notion 整理笔记 Quick Reference

| Key | Value |
|-----|-------|
| Database ID | `05c87b65-e76b-4789-a38c-5c84809d300f` |
| API Key | `~/.config/notion/api_key` |
| API Version | `2025-09-03` |
| Default Filter | 排除 `状态 = 归档` |
| 领域映射 | 参考 `~/.agents/skills/url-to-notion/SKILL.md` 中的领域映射表 |

**Notion 限制：**
- `POST /v1/blocks/{id}/children` 端点可能返回 `invalid_request_url` — 使用 `POST /v1/pages` 带 `children` 字段一次性创建
- 图片使用 `external` 类型（R2 URL），`file_upload` 类型有时上传状态卡在 `pending`
- R2 域名：`https://cos.jiahongw.com/covers/`

## Style DNA

### Core Voice

| Dimension | Rule |
|-----------|------|
| Perspective | First-person ("I", "my") — never corporate or brand voice |
| Tone | Like a thoughtful friend sharing what's on their mind |
| Humor | Self-deprecating, gentle, observant (not punchline-driven) |
| Vulnerability | Admit failures, contradictions, human foibles openly |
| Authority | Soft — "It seems to me...", "based purely on anecdotal evidence" |
| Warmth | Genuine care, never condescending or preachy |

### Structural Template

```
Hi [name],

⟡ [Optional: edition marker or theme line, italic]

[One-sentence hook: "Here's what's on my mind about [topic]."]

💭 [Section Title — personal, not formal]
[Optional: image]
[2-4 paragraphs of personal reflection]

💭 [Section Title]
[Optional: image]
[2-4 paragraphs of personal reflection]

[repeat 3-6 sections total]

---

[Italic sign-off: "Until next time, [warm closing]."]
```

### Section Formula

Each 💭 section follows this pattern:

1. **Introduce the thing** — what is it? (1 sentence)
2. **Why it moved me** — personal connection, emotion, or observation (1-2 sentences)
3. **Self-aware twist** — humor, contradiction, or honest admission (1 sentence)
4. **Gentle close** — reflection that doesn't preach (1 sentence)

## Writing Rules

### Do

- Use short paragraphs (2-4 sentences max)
- Write like you're talking to one person, not an audience
- Include specific numbers for comedic effect ("2,347 notes, read maybe 20 times")
- Admit when you fail at the thing you're writing about
- Connect personal experience to broader human patterns
- End sections with a feeling, not a lesson
- Use italics for asides and the sign-off

### Don't

- No listsicles ("5 ways to...")
- No corporate speak ("In today's fast-paced world...")
- No expert positioning ("As a knowledge management expert...")
- No call-to-action buttons or marketing language
- No exclamation marks in section titles
- No "In conclusion" or summary sections
- Don't resolve everything neatly — leave some ambiguity

### Signature Phrases (Use Sparingly)

- "It seems to me..."
- "This is based purely on anecdotal evidence"
- "I should probably [do the thing], so..."
- "Like a [metaphor] that [ironic twist]"
- "Here's what's on my mind about..."
- "Until next time, [warm closing]"

## Content Curation Pattern

When writing about multiple items:

- Mix media types (books, videos, podcasts, art, ideas)
- Each item gets a personal angle, not a summary
- Thread a loose theme through all sections (mindfulness, creativity, etc.)
- End with 2-3 lighter "also saved this week" links for fun

## Image Placement

Images should appear:
- After the 💭 title, before the text
- Hand-drawn or doodle style preferred
- No text in images
- 16:9 aspect ratio
- Warm, pastel color palette

## Full Example

See this article for reference:

```
Hi Victor,

Here's what's on my mind about notes.

💭 我的笔记坟墓

[illustration: pile of notes and notebooks]

我大约有 2,347 条笔记。读过它们的次数，大概不超过 20 次。
这个数字是我刚刚在 Notion 里搜到的，但请不要问我为什么搜
这个数字——因为我自己也不知道为什么是 2,347。

Tiago Forte 说建立"第二大脑"的核心是 CODE 方法：Capture,
Organize, Distill, Express。我完美地执行了前两步。Capture
和 Organize。Capture 一切。Organize 到各种标签、数据库、
关联字段里。然后……就没了。

Distill 和 Express 像是我办了健身卡但从来不去的理由一样——
我知道应该做，但我总有更好的借口。

💭 工具收集症候群

[illustration: person moving trash cans]

过去一年里，我尝试过的笔记工具包括：Notion（主力）、Apple
Notes、Obsidian、Logseq、Roam Research、Bear、Craft，甚至
Notion 本身的不同模板我都换过七八套。

每次换工具的时候，我都告诉自己：这次一定会坚持。

结果只是把我的混乱从一个平台迁移到另一个平台。就像搬家时
把垃圾打包带走，换了个更好看的垃圾桶。

---

Until next time, take care of your notes.
(And maybe actually read them once in a while.)
```

## Workflow

When asked to write in this style:

### Phase 1: Gather Reference Material (Required)

**Always search the user's Notion for relevant content** to ground the article in their actual collected knowledge.

**Step 1: Use the global search API** (database queries may return 0 results due to permission issues)

```bash
# Search Notion for relevant pages by topic/keyword
python3 << 'PYEOF'
import requests, os, json

NOTION_KEY = open(os.path.expanduser("~/.config/notion/api_key")).read().strip()

# Search by multiple related keywords
keywords = ["旅行", "travel", "trip", "徒步", "攻略"]  # adapt to topic
for kw in keywords:
    resp = requests.post(
        "https://api.notion.com/v1/search",
        headers={"Authorization": f"Bearer {NOTION_KEY}", "Notion-Version": "2025-09-03", "Content-Type": "application/json"},
        json={"query": kw, "filter": {"property": "object", "value": "page"}, "page_size": 10}
    )
    results = resp.json()
    for r in results.get("results", []):
        title = r.get("properties", {}).get("Name", {}).get("title", [{}])[0].get("plain_text", "No title")
        page_id = r["id"].replace("-", "")
        print(f"• {title} (id: {page_id})")
PYEOF
```

**Step 2: Read full content of the most relevant pages**

```bash
# Read blocks from a specific page
python3 -c "
import requests, os
NOTION_KEY = open(os.path.expanduser('~/.config/notion/api_key')).read().strip()
PAGE_ID = '<page-id-without-dashes>'
resp = requests.get(f'https://api.notion.com/v1/blocks/{PAGE_ID}/children?page_size=100',
    headers={'Authorization': f'Bearer {NOTION_KEY}', 'Notion-Version': '2025-09-03'})
for b in resp.json()['results']:
    t = b['type']
    if t in ('paragraph','heading_1','heading_2','heading_3','quote'):
        texts = b[t].get('rich_text', [])
        text = ''.join(x['plain_text'] for x in texts)
        if text: print(text)
"
```

**What to extract from Notion notes:**
- Key insights, quotes, or observations the user has saved
- Interesting tools, books, videos, or ideas they've collected
- Specific details (names, numbers, dates) to weave into reflections
- Personal context from their saved notes that can become article material

### Phase 2: Synthesize & Plan

1. **Identify the topic** and personal angle based on the gathered notes
2. **Select 3-5 reference notes** to weave into the article — use specific details, not summaries
3. **Generate 3-5 section titles** with 💭 prefix, each anchored to a real note or insight
4. **Map sections to notes**: which Notion content inspires which section?

### Phase 3: Write

5. **Write each section** following the formula (introduce → why it moved me → self-aware twist → gentle close)
6. **Weave in specific details** from the Notion notes — names, numbers, quotes, tool names
7. **Add opening and closing** (Hi [name] + warm sign-off)
8. **Optionally generate illustrations** using `opencli gemini image` with doodle style prompts

### Phase 4: Publish (Optional)

9. **Publish** to Notion, email, or social platforms per user request

### Illustration Generation

When generating images for articles:

```bash
opencli gemini image "[simple prompt, no complex descriptions]" --rt 16:9 --op /Users/victor/Desktop/Inbox/temp
```

Keep prompts very short (5-8 words max). Avoid complex descriptions.

⚠️ **If Gemini returns "no-images"** (happens occasionally):
- Retry with an even simpler prompt (3-5 words)
- If still failing, proceed without images and use `[图片：描述]` placeholders
- Images can be added later when the service is available

### Publishing to Notion

When saving to Notion「整理笔记」:
- Use external image URLs (R2) for reliability
- Set icon: 💭 (emoji)
- Set cover: external URL
- 文献类型: 想法 or 笔记
- 卡片类型: 永久笔记
- 🚩 领域: match content topic
- Include all images as inline blocks between text sections

## Quality Checklist

Before delivering:

- [ ] Reads like a friend wrote it, not a blog
- [ ] Contains at least one self-deprecating moment
- [ ] No sections longer than 4 paragraphs
- [ ] Ends with warmth, not a lesson
- [ ] Title is personal, not SEO-optimized
- [ ] At least one specific number used for humor
- [ ] Sign-off matches the warm, casual tone

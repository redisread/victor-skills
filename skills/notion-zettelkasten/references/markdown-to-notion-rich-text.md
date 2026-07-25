# Markdown 内联格式 → Notion rich_text

保存文章或工具箱卡片时，抓取到的 Markdown 文本里经常包含 `**加粗**`、`*斜体*` 和 `[链接文字](URL)`。如果直接当纯文本写入 Notion，这些格式会原样暴露，阅读和点击体验都很差。

建议在构建 Notion `rich_text` 数组前先做一次 inline 解析。

## 解析规则

| Markdown | Notion rich_text |
|----------|-----------------|
| `**文字**` | `annotations.bold = true` |
| `*文字*` | `annotations.italic = true` |
| `[文字](URL)` | `text.link.url = URL` |

说明：
- 链接的可见文字写入 `text.content`，URL 写入 `text.link.url`；
- 加粗和斜体可以叠加在普通文字段上；
- 单个 `text.content` 长度超过 1900 字符时，需要在保持标注的前提下拆成多个 `text` 对象；
- 拆分优先在句号、换行处切断，不要切断链接或加粗标记。

## Python 参考实现

```python
import re

_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
_ITALIC_RE = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")


def _split_italic(s):
    out, idx = [], 0
    for m in _ITALIC_RE.finditer(s):
        if m.start() > idx:
            out.append({"type": "text", "text": {"content": s[idx:m.start()]}})
        out.append({"type": "text", "text": {"content": m.group(1)}, "annotations": {"italic": True}})
        idx = m.end()
    if idx < len(s):
        out.append({"type": "text", "text": {"content": s[idx:]}})
    return out


def _split_bold_italic(s):
    out, idx = [], 0
    for m in _BOLD_RE.finditer(s):
        if m.start() > idx:
            out.extend(_split_italic(s[idx:m.start()]))
        out.append({"type": "text", "text": {"content": m.group(1)}, "annotations": {"bold": True}})
        idx = m.end()
    if idx < len(s):
        out.extend(_split_italic(s[idx:]))
    return out


def _split_segment(seg, max_len=1900):
    content = seg["text"]["content"]
    if len(content) <= max_len:
        return [seg]
    chunks = []
    base = {"type": "text", "text": {"content": ""}}
    if "annotations" in seg:
        base["annotations"] = dict(seg["annotations"])
    if "link" in seg["text"]:
        base["text"]["link"] = dict(seg["text"]["link"])
    while len(content) > max_len:
        cut = content.rfind("。", max_len // 2, max_len)
        if cut == -1:
            cut = content.rfind("\n", max_len // 2, max_len)
        if cut == -1:
            cut = max_len
        piece = dict(base)
        piece["text"] = dict(base["text"])
        piece["text"]["content"] = content[:cut]
        chunks.append(piece)
        content = content[cut:].lstrip()
    last = dict(base)
    last["text"] = dict(base["text"])
    last["text"]["content"] = content
    chunks.append(last)
    return chunks


def make_rich_text(content):
    """把一段 Markdown 文本转成 Notion rich_text 数组。"""
    parts, idx = [], 0
    for m in _LINK_RE.finditer(content):
        if m.start() > idx:
            parts.extend(_split_bold_italic(content[idx:m.start()]))
        parts.append({
            "type": "text",
            "text": {"content": m.group(1), "link": {"url": m.group(2)}}
        })
        idx = m.end()
    if idx < len(content):
        parts.extend(_split_bold_italic(content[idx:]))

    out = []
    for seg in parts:
        out.extend(_split_segment(seg))
    return out
```

## 使用示例

```python
paragraph = {
    "object": "block",
    "type": "paragraph",
    "paragraph": {"rich_text": make_rich_text("这是一个 **[链接](https://example.com)** 和 **加粗** 文字。")}
}
```

## 注意事项

- 该实现只处理最常见的三种 inline 标记；嵌套情况（如链接文字里再加粗）暂不支持；
- 如果原文使用 HTML `<strong>` / `<a>`，建议先统一转换成 Markdown 再调用；
- 工具箱卡片的正文也适用同样规则，但工具箱通常不需要保留图片 block。

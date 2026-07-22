#!/usr/bin/env python3
"""
微信公众号文章解析器。

输入：微信文章 HTML 文件路径或 URL
输出：JSON（标题、来源 URL、段落/图片顺序列表）

用法：
    python3 wechat-parser.py <html_file> [--url <source_url>]
    python3 wechat-parser.py --url https://mp.weixin.qq.com/s/...

输出示例：
{
  "title": "文章标题",
  "source_url": "https://mp.weixin.qq.com/s/...",
  "elements": [
    {"type": "img", "url": "https://mmbiz.qpic.cn/..."},
    {"type": "text", "content": "段落内容"},
    ...
  ]
}
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

try:
    from bs4 import BeautifulSoup, NavigableString
except ImportError:
    print("Error: beautifulsoup4 is required. Install: pip install beautifulsoup4", file=sys.stderr)
    sys.exit(1)


def fetch_html(url: str, timeout: int = 20) -> str:
    """用 curl 抓取微信文章 HTML。"""
    cmd = [
        "curl", "-sL", "--max-time", str(timeout),
        "-H", "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Failed to fetch {url}: {result.stderr}")
    return result.stdout


def extract_elements(content_div):
    """按文档顺序提取文本段落和图片 URL。"""
    elements = []

    def walk(node):
        for child in node.children:
            if isinstance(child, NavigableString):
                text = str(child).strip()
                if text:
                    elements.append({"type": "text", "content": text})
                continue

            if child.name == "img":
                src = child.get("data-src") or child.get("src")
                if src:
                    elements.append({"type": "img", "url": src})
                continue

            # 段落、标题、列表项作为文本叶节点
            if child.name in ("p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "blockquote"):
                text = child.get_text(strip=True)
                if text:
                    elements.append({"type": "text", "content": text})
                # 段落内可能还有内联图片
                for img in child.find_all("img"):
                    src = img.get("data-src") or img.get("src")
                    if src:
                        elements.append({"type": "img", "url": src})
                continue

            # 容器标签继续递归
            if child.name in ("section", "div", "span", "a", "strong", "em", "b", "i"):
                walk(child)
                continue

            # 其他标签：取文本兜底
            text = child.get_text(strip=True)
            if text:
                elements.append({"type": "text", "content": text})

    walk(content_div)
    return elements


def parse_wechat(html: str, source_url: str = "") -> dict:
    soup = BeautifulSoup(html, "html.parser")

    # 标题：优先 h1，fallback h2
    title_tag = soup.select_one("h1.rich_media_title") or soup.select_one("h2.rich_media_title")
    title = title_tag.get_text(strip=True) if title_tag else "无标题"

    content_div = soup.find("div", id="js_content")
    if not content_div:
        raise ValueError("Cannot find #js_content in WeChat HTML")

    elements = extract_elements(content_div)

    # 合并同一自然段内的连续短文本节点（可选：避免把一句话拆成多个 block）
    merged = []
    buf = ""
    for el in elements:
        if el["type"] == "text":
            if len(buf) + len(el["content"]) + 2 < 300:
                buf = (buf + "\n\n" + el["content"]).strip() if buf else el["content"]
            else:
                if buf:
                    merged.append({"type": "text", "content": buf})
                buf = el["content"]
        else:
            if buf:
                merged.append({"type": "text", "content": buf})
                buf = ""
            merged.append(el)
    if buf:
        merged.append({"type": "text", "content": buf})

    return {
        "title": title,
        "source_url": source_url,
        "elements": merged,
    }


def main():
    parser = argparse.ArgumentParser(description="Parse WeChat article HTML")
    parser.add_argument("html_file", nargs="?", help="Path to WeChat HTML file")
    parser.add_argument("--url", default="", help="Original source URL")
    args = parser.parse_args()

    if args.html_file:
        html = Path(args.html_file).read_text(encoding="utf-8")
    elif args.url:
        html = fetch_html(args.url)
    else:
        parser.print_help()
        sys.exit(1)

    result = parse_wechat(html, args.url)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

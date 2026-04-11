#!/usr/bin/env python3
"""
X Following Digest - 推文分析脚本
用于筛选高质量推文、标记 RT 转发并生成分析报告
"""

import json
import sys
import os
import re
import subprocess
from datetime import datetime
from typing import List, Dict, Any, Optional


def load_tweets(file_path: str) -> List[Dict[str, Any]]:
    """加载推文数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def is_retweet(tweet: Dict[str, Any]) -> bool:
    """判断是否为 RT 转发推文"""
    text = tweet.get('text', '')
    return text.startswith('RT @')


def fetch_original_content(tweet_id: str, output_dir: str) -> Dict[str, Any]:
    """
    获取 RT 原帖的完整内容

    尝试两种方式：
    1. 先尝试获取 thread（推文串）
    2. 如果 thread 失败或为空，尝试获取 article（X 文章）

    Args:
        tweet_id: 推文 ID
        output_dir: 临时文件输出目录

    Returns:
        {
            "thread_content": [...],  # 如果成功获取 thread
            "article_content": "...",  # 如果成功获取 article
            "fetch_status": "thread_success" | "article_success" | "fetch_failed",
            "error": "错误信息（如果有）"
        }
    """
    result = {
        "thread_content": None,
        "article_content": None,
        "fetch_status": "fetch_failed",
        "error": None
    }

    # 尝试获取 thread
    thread_file = os.path.join(output_dir, f"thread_{tweet_id}.json")
    try:
        cmd = ["autocli", "twitter", "thread", tweet_id, "-f", "json", "--limit", "50"]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if proc.returncode == 0 and proc.stdout.strip():
            thread_data = json.loads(proc.stdout)
            if thread_data and isinstance(thread_data, list) and len(thread_data) > 0:
                result["thread_content"] = thread_data
                result["fetch_status"] = "thread_success"
                print(f"✅ 成功获取 thread: {tweet_id} ({len(thread_data)} 条推文)", file=sys.stderr)
                return result
    except subprocess.TimeoutExpired:
        result["error"] = "thread 获取超时"
    except json.JSONDecodeError as e:
        result["error"] = f"thread JSON 解析失败：{e}"
    except Exception as e:
        result["error"] = f"thread 获取失败：{e}"

    # 尝试获取 article
    article_file = os.path.join(output_dir, f"article_{tweet_id}.json")
    try:
        cmd = ["autocli", "twitter", "article", tweet_id, "-f", "json"]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if proc.returncode == 0 and proc.stdout.strip():
            article_data = json.loads(proc.stdout)
            if article_data:
                result["article_content"] = article_data
                result["fetch_status"] = "article_success"
                print(f"✅ 成功获取 article: {tweet_id}", file=sys.stderr)
                return result
    except subprocess.TimeoutExpired:
        result["error"] = "article 获取超时"
    except json.JSONDecodeError as e:
        result["error"] = f"article JSON 解析失败：{e}"
    except Exception as e:
        result["error"] = f"article 获取失败：{e}"

    print(f"❌ 获取原帖失败 {tweet_id}: {result['error'] or '未知错误'}", file=sys.stderr)
    return result


def extract_retweet_info(tweet: Dict[str, Any]) -> Optional[Dict[str, str]]:
    """
    从 RT 推文中提取原帖信息
    返回：{"original_author": "...", "preview_text": "..."}
    """
    text = tweet.get('text', '')

    # 匹配 RT @username: content
    match = re.match(r'RT @([^:]+):\s*(.+)', text, re.DOTALL)
    if match:
        return {
            "original_author": match.group(1),
            "preview_text": match.group(2)[:300]  # 预览前 300 字符
        }
    return None


def get_tweet_id_from_url(url: str) -> Optional[str]:
    """从推文 URL 中提取 tweet ID"""
    match = re.search(r'/status/(\d+)', url)
    if match:
        return match.group(1)
    return None


def enrich_retweet_content(tweet: Dict[str, Any], output_dir: str = None) -> Dict[str, Any]:
    """
    为 RT 推文添加元数据和完整原帖内容

    功能：
    1. 标记为 RT
    2. 提取原帖作者、预览文本
    3. 自动获取完整的原帖内容（thread 或 article）

    Args:
        tweet: 推文数据
        output_dir: 临时文件输出目录，用于存放获取的原帖数据

    Returns:
        增强后的推文数据
    """
    if not is_retweet(tweet):
        return tweet

    # 标记为 RT
    tweet['is_retweet'] = True

    # 提取 RT 信息
    rt_info = extract_retweet_info(tweet)
    if not rt_info:
        return tweet

    # 获取 tweet ID
    tweet_id = get_tweet_id_from_url(tweet.get('url', ''))

    # 构建 retweeted_content 结构
    tweet['retweeted_content'] = {
        "original_author": rt_info["original_author"],
        "original_tweet_id": tweet_id,
        "preview_text": rt_info["preview_text"],
        "original_url": f"https://x.com/{rt_info['original_author']}/status/{tweet_id}" if tweet_id else None,
        "thread_content": None,      # thread 内容（数组）
        "article_content": None,     # article 内容（对象）
        "fetch_status": "pending",   # pending | thread_success | article_success | fetch_failed
        "fetch_error": None          # 错误信息
    }

    # 如果有 output_dir，尝试获取完整原帖内容
    if output_dir and tweet_id:
        fetch_result = fetch_original_content(tweet_id, output_dir)
        tweet['retweeted_content']['thread_content'] = fetch_result.get('thread_content')
        tweet['retweeted_content']['article_content'] = fetch_result.get('article_content')
        tweet['retweeted_content']['fetch_status'] = fetch_result.get('fetch_status')
        tweet['retweeted_content']['fetch_error'] = fetch_result.get('error')

    return tweet


def is_high_quality_tweet(tweet: Dict[str, Any]) -> bool:
    """
    判断是否为高质量推文

    排除标准:
    - 纯新闻短讯（只陈述事实，无观点）
    - 广告/推广内容
    - 少于 50 个字符的碎碎念（RT 除外）
    - 纯表情符号或图片无文字内容
    - 过于个人化的日常分享
    """
    # RT 推文直接保留（将基于预览文本分析）
    if is_retweet(tweet):
        return True

    text = tweet.get('text', '').strip()

    # 基本长度检查（非 RT）
    if len(text) < 50:
        return False

    # 排除纯 URL 或短链接
    if text.startswith('http') and len(text) < 60:
        return False

    # 排除纯表情符号
    if all(ord(c) > 127 or c.isspace() for c in text.replace('https://', '').replace('http://', '')):
        return False

    # 排除明显的广告关键词
    ad_keywords = ['限时优惠', '点击链接', '立即购买', '优惠码', '折扣',
                   'promo code', 'discount', 'sale', 'buy now', 'limited time',
                   ' sponsored ', '广告', '推广', 'affiliate']
    text_lower = text.lower()
    for keyword in ad_keywords:
        if keyword.lower() in text_lower:
            return False

    # 排除过于个人化的日常分享关键词
    personal_keywords = ['吃饭了', '睡觉了', '起床了', '今天天气', '今天吃',
                         '今天穿', '今天去', '刚刚在', '现在在', '好困', '好饿',
                         'good morning', 'good night', 'having lunch', 'having dinner',
                         'just woke up', 'going to bed', 'i\'m eating', 'i\'m at']
    for keyword in personal_keywords:
        if keyword.lower() in text_lower:
            return False

    # 排除纯新闻短讯特征（通常是客观陈述，无主语或观点）
    news_patterns = ['据报道', '消息称', ' announced ', ' announced\n', ' announced:',
                     'breaking:', 'breaking news', 'just in:', 'update:']
    if len(text) < 100:
        for pattern in news_patterns:
            if pattern.lower() in text_lower:
                return False

    return True


def filter_high_quality_tweets(tweets: List[Dict[str, Any]], output_dir: str = None) -> List[Dict[str, Any]]:
    """筛选高质量推文，并为 RT 添加元数据"""
    filtered = []
    rt_count = 0

    for tweet in tweets:
        if is_high_quality_tweet(tweet):
            if is_retweet(tweet):
                rt_count += 1
                tweet = enrich_retweet_content(tweet, output_dir)
            filtered.append(tweet)

    if rt_count > 0:
        print(f"🔄 包含 {rt_count} 条 RT 推文（将获取原帖完整内容）", file=sys.stderr)

    return filtered


def format_tweet_for_analysis(tweet: Dict[str, Any]) -> str:
    """格式化推文用于分析"""
    author = tweet.get('author', 'unknown')
    text = tweet.get('text', '')
    url = tweet.get('url', '')
    created_at = tweet.get('created_at', '')
    likes = tweet.get('likes', 0)
    replies = tweet.get('replies', 0)
    retweets = tweet.get('retweets', 0)
    views = tweet.get('views', 0)

    # 如果是 RT，显示原帖信息
    rt_section = ""
    if tweet.get('is_retweet'):
        rt_content = tweet.get('retweeted_content', {})
        original_author = rt_content.get('original_author', 'unknown')
        original_url = rt_content.get('original_url', '')
        preview = rt_content.get('preview_text', '')
        fetch_status = rt_content.get('fetch_status', 'unknown')

        rt_section = f"""
🔄 [RT 转发]
原帖作者：@{original_author}
原帖预览：{preview}...
原帖链接：{original_url}
获取状态：{fetch_status}"""

        # 如果有 thread 内容，展示 thread
        thread_content = rt_content.get('thread_content')
        if thread_content:
            rt_section += f"\n\n📝 原帖 Thread ({len(thread_content)} 条推文):\n"
            for i, thread_tweet in enumerate(thread_content[:5], 1):  # 最多展示 5 条
                thread_text = thread_tweet.get('text', '')
                rt_section += f"  {i}. {thread_text}\n"
            if len(thread_content) > 5:
                rt_section += f"  ... 还有 {len(thread_content) - 5} 条\n"

        # 如果有 article 内容，展示 article
        article_content = rt_content.get('article_content')
        if article_content:
            rt_section += "\n\n📄 原帖 Article:\n"
            if isinstance(article_content, dict):
                article_text = article_content.get('content', '') or article_content.get('text', '')
                rt_section += f"  {article_text[:500]}...\n" if article_text else "  无法获取文章内容\n"
            elif isinstance(article_content, str):
                rt_section += f"  {article_content[:500]}...\n"

    return f"""---
作者：@{author}
发布时间：{created_at}
互动数据：{likes} likes, {replies} replies, {retweets} retweets, {views} views
原文:
{text}
链接：{url}{rt_section}
---"""


def generate_markdown_report(
    tweets: List[Dict[str, Any]],
    date_str: str,
    timestamp_str: str
) -> str:
    """生成 Markdown 报告头部"""

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 统计 RT 数量
    rt_count = sum(1 for t in tweets if t.get('is_retweet'))

    # 统计 RT 原帖获取成功数量
    rt_fetched = sum(1 for t in tweets if t.get('is_retweet') and t.get('retweeted_content', {}).get('fetch_status') in ['thread_success', 'article_success'])

    header = f"""# X Following Digest - {date_str}

生成时间：{current_time}
筛选范围：最近 24 小时
精选推文数：{len(tweets)}
转发推文数：{rt_count}
RT 原帖获取成功：{rt_fetched}

---

"""
    return header


def save_enriched_json(tweets: List[Dict[str, Any]], output_file: str):
    """保存增强后的 JSON 数据（包含 RT 元数据）"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(tweets, f, ensure_ascii=False, indent=2)
    print(f"✅ 增强数据已保存：{output_file}", file=sys.stderr)


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze.py <tweets.json> [output.md]", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    # 从文件路径提取日期
    file_name = os.path.basename(input_file)
    date_str = "Unknown"
    if file_name.startswith('xFollowingRaw-'):
        date_str = file_name[14:22]  # 提取 YYYYMMDD

    # 获取当前时间戳
    timestamp_str = datetime.now().strftime("%Y%m%d%H%M%S")

    # 创建输出目录用于存放临时文件
    output_dir = os.path.dirname(input_file) if output_file else os.path.dirname(input_file)
    if not output_dir:
        output_dir = "."

    print(f"📊 分析推文数据：{input_file}", file=sys.stderr)

    # 加载推文
    try:
        tweets = load_tweets(input_file)
    except Exception as e:
        print(f"❌ 加载推文失败：{e}", file=sys.stderr)
        sys.exit(1)

    total_count = len(tweets)
    print(f"📥 加载完成，共 {total_count} 条推文", file=sys.stderr)

    # 筛选高质量推文
    quality_tweets = filter_high_quality_tweets(tweets, output_dir)
    quality_count = len(quality_tweets)
    print(f"✨ 筛选出 {quality_count} 条高质量推文 (排除 {total_count - quality_count} 条)", file=sys.stderr)

    if quality_count == 0:
        print("⚠️  没有高质量推文需要分析", file=sys.stderr)
        sys.exit(0)

    # 保存增强后的 JSON 数据
    enriched_json_file = input_file.replace('.json', '-enriched.json')
    save_enriched_json(quality_tweets, enriched_json_file)

    # 生成报告
    report = generate_markdown_report(quality_tweets, date_str, timestamp_str)

    # 输出推文内容供 Claude 分析
    tweets_content = []
    for i, tweet in enumerate(quality_tweets, 1):
        tweets_content.append(f"## 推文 {i}\n\n{format_tweet_for_analysis(tweet)}\n")

    full_report = report + "\n\n".join(tweets_content)

    # 输出到文件或 stdout
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_report)
        print(f"✅ 报告已保存：{output_file}", file=sys.stderr)
    else:
        print(full_report)

    # 输出统计信息到 stderr
    rt_count = sum(1 for t in quality_tweets if t.get('is_retweet'))
    rt_fetched = sum(1 for t in quality_tweets if t.get('is_retweet') and t.get('retweeted_content', {}).get('fetch_status') in ['thread_success', 'article_success'])

    print(f"\n📈 统计:", file=sys.stderr)
    print(f"   - 总推文数：{total_count}", file=sys.stderr)
    print(f"   - 高质量推文：{quality_count}", file=sys.stderr)
    print(f"   - 转发推文：{rt_count}", file=sys.stderr)
    print(f"   - RT 原帖获取成功：{rt_fetched}", file=sys.stderr)
    print(f"   - 筛选率：{quality_count/total_count*100:.1f}%", file=sys.stderr)
    print(f"\n💾 输出文件:", file=sys.stderr)
    print(f"   - 增强数据：{enriched_json_file}", file=sys.stderr)
    if output_file:
        print(f"   - 分析报告：{output_file}", file=sys.stderr)


if __name__ == '__main__':
    main()

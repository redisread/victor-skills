#!/usr/bin/env python3
"""
Save tool information to Notion Toolbox database.
Usage: python save-to-notion.py --url "https://example.com" --name "Tool Name" --type "网站" --tags "AI,效率" --description "Tool description"

Features:
- Auto-extract cover image from og:image, twitter:image, or GitHub
- Auto-select emoji icon based on tool type and features
- Generate best practices content (适用场景, 快速开始, 核心技巧, 注意事项, 相关资源)
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
import re
from html.parser import HTMLParser

NOTION_API_KEY = os.environ.get('NOTION_API_KEY', '')
DATABASE_ID = '6f7bb9cc-ac01-41c5-9856-fb1568d197ae'
NOTION_API_URL = 'https://api.notion.com/v1/pages'

# Valid types (exactly 5 options)
VALID_TYPES = {'软件', '网站', '浏览器插件', 'Prompt', '工具包'}
NOTION_VERSION = '2021-05-13'  # Supports children parameter at creation time

# Icon mapping based on tool type and features
ICON_MAP = {
    # By type
    '软件': '💻',
    '网站': '🌐',
    '浏览器插件': '🔌',
    'Prompt': '📝',
    '工具包': '📦',
    # By technology/feature
    'python': '🐍',
    'javascript': '📜',
    'typescript': '📘',
    'ai': '🤖',
    'llm': '🤖',
    'agent': '🤖',
    'design': '🎨',
    'dev': '🛠️',
    'learn': '📚',
    'cloud': '☁️',
    'security': '🔒',
    'productivity': '⚡',
    'data': '📊',
}


class MetaParser(HTMLParser):
    """Parse meta tags from HTML to extract og:image and twitter:image."""

    def __init__(self):
        super().__init__()
        self.og_image = None
        self.twitter_image = None
        self.title = None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'meta':
            # Open Graph Image
            if attrs_dict.get('property') == 'og:image':
                self.og_image = attrs_dict.get('content', '')
            # Twitter Card Image
            if attrs_dict.get('name') == 'twitter:image':
                self.twitter_image = attrs_dict.get('content', '')
        elif tag == 'title':
            pass  # Title content comes in handle_data

    def handle_data(self, data):
        if self.lasttag == 'title' and not self.title:
            self.title = data.strip()


def select_icon(tool_type, tags, description):
    """Select appropriate emoji icon based on tool type and features.
    
    Priority:
    1. Explicit technology/feature match in tags/description
    2. Tool type default
    3. Generic fallback
    """
    text_to_check = ' '.join(tags).lower() + ' ' + description.lower()
    
    # Check for technology matches first (highest priority)
    tech_priority = ['python', 'javascript', 'ai', 'llm', 'agent', 'design', 'dev']
    for tech in tech_priority:
        if tech in text_to_check:
            return ICON_MAP.get(tech, ICON_MAP.get(tool_type, '💻'))
    
    # Fall back to type-based icon
    return ICON_MAP.get(tool_type, '💻')


def generate_best_practices(name, tool_type, description, url):
    """Generate best practices content based on tool type.
    
    Returns a list of Notion block objects.
    """
    blocks = []
    
    # Section header
    blocks.append({
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": "🎯 最佳实践"}}]
        }
    })
    
    # 1. 适用场景
    blocks.append({
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": [{"type": "text", "text": {"content": "适用场景"}}]
        }
    })
    
    use_cases = {
        '软件': f"{name} 适合需要本地运行的场景，可作为日常开发/工作流的核心工具。",
        '网站': f"{name} 适合在线快速访问，无需安装即可使用的场景。",
        '浏览器插件': f"{name} 适合增强浏览器功能，提升网页浏览效率的场景。",
        'Prompt': f"{name} 适合需要快速调用 AI 能力，标准化输出质量的场景。",
        '工具包': f"{name} 适合集成到项目中，快速实现特定功能的开发场景。"
    }
    blocks.append({
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": use_cases.get(tool_type, description)}}]
        }
    })
    
    # 2. 快速开始
    blocks.append({
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": [{"type": "text", "text": {"content": "快速开始"}}]
        }
    })
    
    quick_starts = {
        '软件': [
            "访问官网下载对应系统的安装包",
            "安装并完成初始配置",
            "熟悉核心界面和基础操作",
            "尝试完成一个简单任务",
            "根据需要调整设置和快捷键"
        ],
        '网站': [
            "访问网站并注册/登录账号",
            "浏览功能介绍或新手引导",
            "尝试核心功能（上传/创建/查询等）",
            "了解付费方案和限制",
            "收藏网址或添加到书签"
        ],
        '浏览器插件': [
            "在 Chrome Web Store 或对应商店搜索安装",
            "点击添加到浏览器并确认权限",
            "点击插件图标查看功能面板",
            "根据需要配置插件选项",
            "测试插件在目标网站上的效果"
        ],
        'Prompt': [
            "复制 Prompt 模板到剪贴板",
            "在 AI 工具（ChatGPT/Claude 等）中粘贴",
            "根据实际需求修改变量/参数",
            "发送并观察输出效果",
            "根据结果迭代优化 Prompt"
        ],
        '工具包': [
            "查看官方文档了解安装方式",
            "通过包管理器安装（pip/npm 等）",
            "阅读 README 和快速开始指南",
            "复制示例代码到本地运行",
            "根据项目需求修改和扩展"
        ]
    }
    
    for step in quick_starts.get(tool_type, ["访问工具链接", "了解基本功能", "尝试使用"]):
        blocks.append({
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": step}}]
            }
        })
    
    # 3. 核心技巧
    blocks.append({
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": [{"type": "text", "text": {"content": "核心技巧"}}]
        }
    })
    
    tips = {
        '软件': [
            "学习快捷键可以大幅提升效率",
            "定期备份配置文件防止丢失",
            "关注官方更新获取新功能",
            "探索插件/扩展生态",
            "加入用户社区获取使用技巧"
        ],
        '网站': [
            "善用浏览器书签或收藏功能",
            "了解免费额度限制，合理规划使用",
            "关注官方博客获取更新动态",
            "尝试 API 接口实现自动化",
            "备份重要数据到本地"
        ],
        '浏览器插件': [
            "检查插件权限，避免过度授权",
            "注意插件冲突，必要时禁用排查",
            "定期更新获取安全补丁",
            "使用插件管理器批量管理",
            "关注隐私政策，敏感场景谨慎使用"
        ],
        'Prompt': [
            "使用变量占位符提高复用性",
            "添加角色设定引导输出风格",
            "通过示例（few-shot）提升准确性",
            "迭代优化，记录有效版本",
            "建立个人 Prompt 库分类管理"
        ],
        '工具包': [
            "锁定版本号避免破坏性更新",
            "阅读源码了解实现细节",
            "关注 GitHub Issues 获取解决方案",
            "编写封装代码提高复用性",
            "贡献代码或文档回馈社区"
        ]
    }
    
    for tip in tips.get(tool_type, ["阅读官方文档", "查看示例代码", "加入社区交流"]):
        blocks.append({
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": tip}}]
            }
        })
    
    # 4. 注意事项
    blocks.append({
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": [{"type": "text", "text": {"content": "注意事项"}}]
        }
    })
    
    warnings = {
        '软件': "注意系统兼容性要求，部分软件可能需要特定版本的操作系统或运行时环境。建议从官方渠道下载，避免使用来路不明的安装包。",
        '网站': "注意数据隐私和服务条款，敏感信息谨慎上传。免费服务可能有功能限制或广告，重要业务建议了解付费方案。",
        '浏览器插件': "插件会访问浏览器数据，请从官方商店安装并定期检查权限。过多插件可能影响浏览器性能，建议只保留必要的。",
        'Prompt': "Prompt 效果因模型版本而异，建议标注适用的 AI 模型。复杂任务建议分步骤进行，避免单次 Prompt 过长导致理解偏差。",
        '工具包': "注意依赖版本兼容性，升级前查看 CHANGELOG。生产环境使用需评估维护成本和社区活跃度，避免使用无人维护的包。"
    }
    
    blocks.append({
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": warnings.get(tool_type, "请仔细阅读官方文档，了解工具的使用限制和最佳实践。")}}]
        }
    })
    
    # 5. 相关资源
    blocks.append({
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": [{"type": "text", "text": {"content": "相关资源"}}]
        }
    })
    
    # Add original URL
    blocks.append({
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [
                {"type": "text", "text": {"content": "官方网站: "}},
                {"type": "text", "text": {"content": url, "link": {"url": url}}}
            ]
        }
    })
    
    # Add GitHub link if it's a GitHub repo
    if 'github.com' in url:
        blocks.append({
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {"type": "text", "text": {"content": "GitHub 仓库: "}},
                    {"type": "text", "text": {"content": url, "link": {"url": url}}}
                ]
            }
        })
    
    return blocks


def extract_cover_image(url):
    """Extract cover image URL from web page.

    Priority:
    1. og:image (Open Graph)
    2. twitter:image (Twitter Card)
    3. GitHub special handling (opengraph.githubassets.com)

    Returns None if no suitable image found.
    """

    try:
        # Fetch page HTML
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (compatible; NotionTool/1.0)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')

        # Parse meta tags
        parser = MetaParser()
        parser.feed(html)

        # Priority 1 & 2: og:image or twitter:image
        cover_url = parser.og_image or parser.twitter_image

        if cover_url:
            # Convert relative URL to absolute
            if cover_url.startswith('/'):
                from urllib.parse import urlparse
                parsed = urlparse(url)
                cover_url = f'{parsed.scheme}://{parsed.netloc}{cover_url}'
            elif cover_url.startswith('//'):
                cover_url = f'https:{cover_url}'

            return cover_url

        # Priority 3: GitHub special handling
        if 'github.com' in url:
            match = re.search(r'github\.com/([^/]+/[^/]+)', url)
            if match:
                repo_path = match.group(1)
                return f'https://opengraph.githubassets.com/1/{repo_path}'

    except Exception:
        pass

    return None


def save_to_notion(name, tool_type, tags, url, description, starred=False, cover_image_url=None, icon_emoji=None):
    """Save tool info to Notion database with icon and best practices."""

    if not NOTION_API_KEY:
        return {'success': False, 'error': 'NOTION_API_KEY environment variable not set'}

    # Validate type
    if tool_type not in VALID_TYPES:
        return {'success': False, 'error': f'Invalid type. Must be one of: {", ".join(VALID_TYPES)}'}

    # Auto-select icon if not provided
    if not icon_emoji:
        icon_emoji = select_icon(tool_type, tags, description)

    # Build properties
    properties = {
        'Name': {
            'title': [{'text': {'content': name}}]
        },
        'URL': {
            'url': url
        }
    }

    # Add type (类型) - single select
    properties['类型'] = {
        'multi_select': [{'name': tool_type}]
    }

    # Add tags (标签)
    if tags:
        properties['标签'] = {
            'multi_select': [{'name': t.strip()} for t in tags]
        }

    # Add description (简介)
    if description:
        properties['简介'] = {
            'rich_text': [{'text': {'content': description}}]
        }

    # Add starred (⭐ 置顶)
    properties['⭐ 置顶'] = {'checkbox': starred}

    # Build request
    data = {
        'parent': {'database_id': DATABASE_ID},
        'icon': {
            'type': 'emoji',
            'emoji': icon_emoji
        },
        'properties': properties
    }

    # Build children blocks (cover image + best practices)
    children_blocks = []
    
    # Add cover image if available
    if cover_image_url:
        data['cover'] = {
            'type': 'external',
            'external': {
                'url': cover_image_url
            }
        }
        children_blocks.append({
            'object': 'block',
            'type': 'image',
            'image': {
                'type': 'external',
                'external': {'url': cover_image_url}
            }
        })
    
    # Generate and add best practices content
    best_practices_blocks = generate_best_practices(name, tool_type, description, url)
    children_blocks.extend(best_practices_blocks)
    
    data['children'] = children_blocks

    try:
        req = urllib.request.Request(
            NOTION_API_URL,
            data=json.dumps(data).encode('utf-8'),
            headers={
                'Authorization': f'Bearer {NOTION_API_KEY}',
                'Notion-Version': NOTION_VERSION,
                'Content-Type': 'application/json'
            },
            method='POST'
        )

        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return {
                'success': True,
                'id': result.get('id'),
                'url': result.get('url'),
                'icon': icon_emoji,
                'properties': result.get('properties')
            }

    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else ''
        return {'success': False, 'error': f'HTTP {e.code}: {error_body}'}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def main():
    parser = argparse.ArgumentParser(description='Save tool to Notion Toolbox')
    parser.add_argument('--url', required=True, help='Tool URL')
    parser.add_argument('--name', required=True, help='Tool name')
    parser.add_argument('--type', required=True, choices=list(VALID_TYPES), help='Tool type (single select)')
    parser.add_argument('--tags', nargs='+', default=[], help='Tags')
    parser.add_argument('--description', default='', help='Description')
    parser.add_argument('--starred', action='store_true', help='Starred')
    parser.add_argument('--cover', default=None, help='Cover image URL (optional, will auto-extract if not provided)')
    parser.add_argument('--icon', default=None, help='Emoji icon (optional, will auto-select if not provided)')

    args = parser.parse_args()

    # Auto-extract cover image if not provided
    cover_image_url = args.cover
    if not cover_image_url:
        cover_image_url = extract_cover_image(args.url)

    result = save_to_notion(
        name=args.name,
        tool_type=args.type,
        tags=args.tags,
        url=args.url,
        description=args.description,
        starred=args.starred,
        cover_image_url=cover_image_url,
        icon_emoji=args.icon
    )

    if result['success']:
        output = {
            'success': True,
            'url': result['url'],
            'id': result['id'],
            'icon': result['icon'],
            'has_cover': cover_image_url is not None,
            'has_best_practices': True
        }
        print(json.dumps(output))
        sys.exit(0)
    else:
        print(json.dumps({'success': False, 'error': result['error']}))
        sys.exit(1)


if __name__ == '__main__':
    main()
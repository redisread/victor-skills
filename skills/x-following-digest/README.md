# X Following Digest

获取 Twitter/X Following 最近 24 小时精选推文，生成摘要分析和社交媒体文案。

## 功能特点

- 🐦 自动获取 Following 最近 300 条推文
- ⏰ 智能筛选最近 24 小时内容
- ✨ 高质量内容过滤（排除广告、新闻短讯、碎碎念）
- 🔄 **RT 转发元数据提取** - 自动识别 RT 并提取原帖作者、预览文本、链接
- 📝 生成深度分析报告
- 💡 提取可实践建议和创作灵感
- 📱 自动生成社交媒体文案（即刻/小红书/推特）

## RT 转发内容处理

对于 RT（转发）推文，技能会：

1. **识别 RT 推文** - 检测 `RT @username:` 格式的转发
2. **提取元数据** - 自动提取原帖作者、预览文本（前300字符）、原帖链接
3. **补充 JSON 数据** - 添加 `retweeted_content` 字段存储元数据

**RT 数据扩展示例：**

```json
{
  "author": "ylecun",
  "text": "RT @SenMarkKelly: ...",
  "is_retweet": true,
  "retweeted_content": {
    "original_author": "SenMarkKelly",
    "original_tweet_id": "2042817948771922398",
    "preview_text": "In the middle of a historic mission...",
    "original_url": "https://x.com/SenMarkKelly/status/2042817948771922398",
    "note": "基于预览文本分析。如需完整原帖，请运行: autocli twitter thread {tweet_id} -f json"
  }
}
```

**获取完整原帖（可选）：**

如需获取 RT 原帖的完整内容，可手动运行：

```bash
# 获取原帖 thread
autocli twitter thread <tweet-id> -f json --limit 10

# 获取 X 文章
autocli twitter article <tweet-id> -f json
```

*注意：由于 Twitter/X 的访问限制，autocli 的 thread/article 命令可能无法成功。分析时主要基于 RT 中的预览文本进行。*

## 安装

```bash
npx skills add ./skills/x-following-digest
```

## 使用方法

### 快速开始

在 Claude Code 中输入：

```
获取 following 推文分析
```

或

```
生成 Twitter following digest
```

### 手动执行

**Step 1: 获取原始数据**

```bash
bash skills/x-following-digest/scripts/run.sh
```

**Step 2: 生成分析报告**

在 Claude Code 中输入：

```
请分析刚获取的增强数据文件 /Users/victor/Desktop/resource/daily-info/x/YYYYMMDD/xFollowingRaw-xxx-enriched.json
```

或直接使用技能：

```
@x-following-digest 分析推文 /Users/victor/Desktop/resource/daily-info/x/YYYYMMDD/xFollowingRaw-xxx-enriched.json
```

### 分析脚本选项

```bash
# 筛选高质量推文并添加 RT 元数据
python3 skills/x-following-digest/scripts/analyze.py tweets.json

# 同时生成分析报告模板
python3 skills/x-following-digest/scripts/analyze.py tweets.json output.md
```

## 输出文件

| 文件 | 说明 |
|------|------|
| `xFollowingRaw-YYYYMMDDHHMMSS.json` | 筛选后的原始推文数据 |
| `xFollowingRaw-YYYYMMDDHHMMSS-enriched.json` | **增强数据（含 RT 元数据）** |
| `xFollowingDigest-YYYYMMDDHHMMSS.md` | 深度分析报告（由 Claude 生成） |

**输出示例：**

```
/Users/victor/Desktop/resource/daily-info/x/20260411/
├── xFollowingRaw-20260411041329.json          # 原始筛选数据 (210KB)
├── xFollowingRaw-20260411041329-enriched.json # 增强数据 (186KB)
└── xFollowingDigest-20260411044500.md         # 分析报告 (10KB)
```

## 目录结构

```
x-following-digest/
├── SKILL.md              # 技能定义文件
├── README.md             # 本文件
└── scripts/
    ├── run.sh            # 主执行脚本
    └── analyze.py        # 推文分析脚本（支持 RT 原帖获取）
```

## 环境变量

- `X_DIGEST_BASE_DIR`: 输出基础目录（默认: `/Users/victor/Desktop/resource/daily-info/`）
- `X_RAW_LIMIT`: 获取推文数量（默认: 300）

## 依赖

- `autocli`: 获取 Twitter/X 数据、thread、article
- `python3`: JSON 处理和分析

## 报告内容

每条精选推文包含：

- 📋 **推文原文**（英文含翻译）
- 🔄 **RT 转发信息**（如适用）
  - 原帖作者和链接
  - 原帖预览文本
- 💭 **核心观点**（提炼总结）
- ✅ **可实践建议**
- 💡 **创作灵感**
- 📱 **社交媒体分享文案**
  - 即刻版本（简短、有观点）
  - 小红书版本（emoji 丰富、口语化）
  - 推特版本（英文 hook）
- 🔗 **原文链接**

## 测试示例

本次测试生成的报告：

- **原始数据**: 298 条推文
- **高质量筛选**: 197 条（筛选率 66.1%）
- **RT 推文**: 52 条（基于预览文本分析）
- **报告文件**: `/Users/victor/Desktop/resource/daily-info/x/20260411/xFollowingDigest-20260411044500.md`

## License

MIT

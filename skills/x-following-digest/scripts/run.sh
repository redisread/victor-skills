#!/bin/bash

# X Following Digest - 主执行脚本
# 获取 Twitter Following 最近 24 小时精选推文并生成分析报告

set -e

# 配置
X_DIGEST_BASE_DIR="${X_DIGEST_BASE_DIR:-/Users/victor/Desktop/resource/daily-info/}"
X_RAW_LIMIT="${X_RAW_LIMIT:-300}"

# 获取当前时间信息
CURRENT_DATE=$(date -u +"%Y%m%d")
CURRENT_DATETIME=$(date -u +"%Y%m%d%H%M%S")
CURRENT_ISO=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
CURRENT_TIMESTAMP=$(date -u +"%s")

# 创建输出目录
OUTPUT_DIR="${X_DIGEST_BASE_DIR}/x/${CURRENT_DATE}"
mkdir -p "$OUTPUT_DIR"

echo "🐦 X Following Digest"
echo "====================="
echo "生成时间: $CURRENT_ISO"
echo "输出目录: $OUTPUT_DIR"
echo ""

# Step 1: 获取推文数据
echo "📥 Step 1: 获取 Following 推文 (limit: $X_RAW_LIMIT)..."

RAW_FILE="${OUTPUT_DIR}/xFollowingRaw-${CURRENT_DATETIME}.json"

# 使用 autocli 获取推文
if ! command -v autocli &> /dev/null; then
    echo "❌ 错误: autocli 未安装，请先安装 autocli"
    exit 1
fi

autocli twitter timeline --type following --limit "$X_RAW_LIMIT" -f json > "$RAW_FILE"

if [ ! -f "$RAW_FILE" ] || [ ! -s "$RAW_FILE" ]; then
    echo "❌ 错误: 未能获取推文数据"
    exit 1
fi

TOTAL_TWEETS=$(cat "$RAW_FILE" | grep -c '"id":' || echo "0")
echo "✅ 获取完成，共 $TOTAL_TWEETS 条推文"
echo "   原始数据: $RAW_FILE"
echo ""

# Step 2: 筛选最近 24 小时的推文
echo "⏰ Step 2: 筛选最近 24 小时的推文..."

# 计算 24 小时前的时间戳（秒）
ONE_DAY_AGO=$((CURRENT_TIMESTAMP - 86400))

# 创建筛选后的文件
FILTERED_FILE="${OUTPUT_DIR}/.filtered-${CURRENT_DATETIME}.json"

# 使用 Python 进行时间筛选（更可靠）
python3 << PYTHON_EOF
import json
from datetime import datetime
import sys

# 读取原始数据
with open("$RAW_FILE", 'r', encoding='utf-8') as f:
    try:
        tweets = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析错误: {e}")
        sys.exit(1)

# 当前时间和24小时前
current_ts = $CURRENT_TIMESTAMP
one_day_ago = $ONE_DAY_AGO

# Twitter 时间格式: "Sat Apr 11 00:15:15 +0000 2026"
def parse_twitter_time(time_str):
    try:
        dt = datetime.strptime(time_str, '%a %b %d %H:%M:%S +0000 %Y')
        return int(dt.timestamp())
    except:
        return 0

# 筛选最近24小时的推文
filtered_tweets = []
for tweet in tweets:
    created_at = tweet.get('created_at', '')
    tweet_ts = parse_twitter_time(created_at)

    if tweet_ts >= one_day_ago:
        filtered_tweets.append(tweet)

# 保存筛选结果
with open("$FILTERED_FILE", 'w', encoding='utf-8') as f:
    json.dump(filtered_tweets, f, ensure_ascii=False, indent=2)

print(f"✅ 筛选完成，最近 24 小时共 {len(filtered_tweets)} 条推文")
PYTHON_EOF

if [ ! -f "$FILTERED_FILE" ] || [ ! -s "$FILTERED_FILE" ]; then
    echo "⚠️  最近 24 小时没有推文，结束执行"
    exit 0
fi

FILTERED_COUNT=$(cat "$FILTERED_FILE" | python3 -c "import json,sys; print(len(json.load(sys.stdin)))")
echo ""

# Step 3: 更新原始数据文件为筛选后的数据
mv "$FILTERED_FILE" "$RAW_FILE"
echo "✅ 原始数据已更新为筛选后的内容 ($FILTERED_COUNT 条)"
echo ""

# Step 4: 筛选高质量推文并获取 RT 原帖内容
echo "✨ Step 3: 筛选高质量推文并获取 RT 原帖内容..."
echo "   这可能需要一些时间（取决于 RT 数量和原帖获取情况）..."
echo ""

ENHANCED_FILE="${OUTPUT_DIR}/xFollowingRaw-${CURRENT_DATETIME}-enriched.json"
ANALYSIS_TEMP="${OUTPUT_DIR}/.analysis-temp-${CURRENT_DATETIME}.md"

# 传递输出目录给 analyze.py，以便它可以在那里存放临时文件
python3 "${SKILL_DIR}/scripts/analyze.py" "$RAW_FILE" "$ANALYSIS_TEMP"

echo ""
echo "📊 基础数据处理完成！"
echo ""
echo "====================="
echo "数据文件:"
echo "  - 原始筛选数据: $RAW_FILE"
echo "  - 增强数据(含RT原帖): $ENHANCED_FILE"
echo ""
echo "下一步:"
echo "  在 Claude Code 中输入以下指令生成最终分析报告:"
echo ""
echo "  @x-following-digest 分析推文 $ENHANCED_FILE"
echo ""
echo "  或手动分析:"
echo "  请分析文件 $ENHANCED_FILE 中的推文，生成深度分析报告"
echo "====================="

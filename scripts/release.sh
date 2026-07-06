#!/usr/bin/env bash
# release.sh — 技能/Agent 发版脚本
# 用法: ./scripts/release.sh <name> <new-version> [changelog-entry]
#
# 示例:
#   ./scripts/release.sh blog-push 1.2.0 "新增草稿模式支持"
#   ./scripts/release.sh quality-info-reviewer 1.3.0 "优化 Twitter 加载逻辑"
#
# 自动完成:
#   1. 更新 SKILL.md / agent .md 的 version 字段
#   2. 在 CHANGELOG.md 追加版本条目
#   3. 更新 README.md 版本表
#   4. git add + commit + tag (<name>@<version>)

set -euo pipefail

# ── 参数校验 ─────────────────────────────────────────────────────────────────
if [[ $# -lt 2 ]]; then
  echo "用法: $0 <name> <new-version> [changelog-entry]"
  echo "示例: $0 blog-push 1.2.0 \"新增草稿模式支持\""
  exit 1
fi

NAME="$1"
NEW_VERSION="$2"
CHANGELOG_ENTRY="${3:-}"

# 验证版本号格式（SemVer）
if ! echo "$NEW_VERSION" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+$'; then
  echo "❌ 版本号格式错误: $NEW_VERSION（需为 MAJOR.MINOR.PATCH，如 1.2.3）"
  exit 1
fi

# ── 定位文件 ─────────────────────────────────────────────────────────────────
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

SKILL_FILE="skills/$NAME/SKILL.md"
AGENT_FILE=".claude/agents/$NAME.md"
FILE=""
TYPE=""

if [[ -f "$SKILL_FILE" ]]; then
  FILE="$SKILL_FILE"
  TYPE="skill"
elif [[ -f "$AGENT_FILE" ]]; then
  FILE="$AGENT_FILE"
  TYPE="agent"
else
  echo "❌ 找不到 $NAME：$SKILL_FILE 和 $AGENT_FILE 均不存在"
  exit 1
fi

echo "📦 类型: $TYPE"
echo "📄 文件: $FILE"

# ── 读取旧版本 ────────────────────────────────────────────────────────────────
OLD_VERSION=$(grep '^version:' "$FILE" | head -1 | sed 's/version: *//')

if [[ -z "$OLD_VERSION" ]]; then
  echo "⚠️  文件中无 version 字段，将新增"
else
  echo "🔄 版本: $OLD_VERSION → $NEW_VERSION"
fi

# ── 1. 更新版本字段 ──────────────────────────────────────────────────────────
if grep -q '^version:' "$FILE"; then
  sed -i '' "s/^version: .*/version: $NEW_VERSION/" "$FILE"
else
  # 在 frontmatter 的 description 行后插入 version
  sed -i '' "/^description:/a\\
version: $NEW_VERSION" "$FILE"
fi

echo "✅ 版本字段已更新"

# ── 2. 更新 CHANGELOG.md ─────────────────────────────────────────────────────
TODAY=$(date +%Y-%m-%d)
SECTION="### $NAME"
NEW_ENTRY="#### [$NEW_VERSION] - $TODAY"

if [[ -n "$CHANGELOG_ENTRY" ]]; then
  ENTRY_BODY="- $CHANGELOG_ENTRY"
else
  ENTRY_BODY="- 版本更新"
fi

CHANGELOG_FILE="CHANGELOG.md"

if [[ ! -f "$CHANGELOG_FILE" ]]; then
  echo "⚠️  CHANGELOG.md 不存在，跳过更新"
else
  # 在对应技能的 Section 下插入新版本条目
  # 找到 ### $NAME 后面的第一个 #### 行之前插入
  if grep -q "^### $NAME" "$CHANGELOG_FILE"; then
    # 在该 section 的第一个 #### 前插入新版本
    sed -i '' "/^### $NAME/,/^#### /{
      /^#### /i\\
$NEW_ENTRY\\
$ENTRY_BODY\\
    }" "$CHANGELOG_FILE"
  else
    # Section 不存在，追加到文件末尾（在对应 Skills/Agents 分类下）
    if [[ "$TYPE" == "skill" ]]; then
      echo -e "\n$SECTION\n\n$NEW_ENTRY\n$ENTRY_BODY" >> "$CHANGELOG_FILE"
    else
      echo -e "\n$SECTION\n\n$NEW_ENTRY\n$ENTRY_BODY" >> "$CHANGELOG_FILE"
    fi
  fi
  echo "✅ CHANGELOG.md 已更新"
fi

# ── 3. 更新 README.md 版本列 ─────────────────────────────────────────────────
README_FILE="README.md"

if [[ -f "$README_FILE" ]]; then
  # 匹配 | `name` | x.x.x | 格式并替换版本号
  if grep -q "| \`$NAME\` |" "$README_FILE"; then
    sed -i '' "s/| \`$NAME\` | [0-9][0-9.]* |/| \`$NAME\` | $NEW_VERSION |/" "$README_FILE"
    echo "✅ README.md 版本号已更新"
  else
    echo "⚠️  README.md 中未找到 $NAME 条目，跳过"
  fi
fi

# ── 4. Git commit + tag ──────────────────────────────────────────────────────
TAG="$NAME@$NEW_VERSION"

git add "$FILE" "$CHANGELOG_FILE" "$README_FILE" 2>/dev/null || true

COMMIT_MSG="release($NAME): $NEW_VERSION"
if [[ -n "$CHANGELOG_ENTRY" ]]; then
  COMMIT_MSG="$COMMIT_MSG - $CHANGELOG_ENTRY"
fi

git commit -m "$COMMIT_MSG"
git tag "$TAG"

echo ""
echo "🎉 发版完成！"
echo "   Tag: $TAG"
echo "   Commit: $(git rev-parse --short HEAD)"
echo ""
echo "推送到远程:"
echo "   git push origin $(git branch --show-current)"
echo "   git push origin $TAG"

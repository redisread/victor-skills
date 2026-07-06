#!/usr/bin/env bash
set -e

# 版本一致性校验脚本
# 检查所有 skill 和 agent 的版本号是否与 README.md 一致

errors=0

# 检查所有技能的版本是否在 README 中正确记录
for skill_dir in skills/*/; do
  skill_file="$skill_dir/SKILL.md"
  if [[ -f "$skill_file" ]]; then
    name=$(grep '^name:' "$skill_file" | sed 's/name: *//')
    version=$(grep '^version:' "$skill_file" | sed 's/version: *//')

    # 检查 README 中是否有该技能的条目
    if ! grep -q "| \`$name\` |" README.md; then
      echo "⚠️  $name: README.md 中未找到对应条目"
      errors=$((errors+1))
    else
      # 检查版本号是否一致
      readme_version=$(grep "| \`$name\` |" README.md | sed 's/.*| `'"$name"'` | \([0-9.]*\) |.*/\1/')
      if [[ "$readme_version" != "$version" ]]; then
        echo "❌ $name: README 版本 ($readme_version) 与 SKILL.md ($version) 不一致"
        errors=$((errors+1))
      fi
    fi
  fi
done

# 检查 Agent
for agent_file in .claude/agents/*.md; do
  if [[ -f "$agent_file" ]]; then
    name=$(grep '^name:' "$agent_file" | sed 's/name: *//')
    version=$(grep '^version:' "$agent_file" | sed 's/version: *//')

    if [[ -n "$name" && -n "$version" ]]; then
      if ! grep -q "| \`$name\` |" README.md; then
        echo "⚠️  Agent $name: README.md 中未找到对应条目"
        errors=$((errors+1))
      else
        readme_version=$(grep "| \`$name\` |" README.md | sed 's/.*| `'"$name"'` | \([0-9.]*\) |.*/\1/')
        if [[ "$readme_version" != "$version" ]]; then
          echo "❌ Agent $name: README 版本 ($readme_version) 与 agent 定义 ($version) 不一致"
          errors=$((errors+1))
        fi
      fi
    fi
  fi
done

if [[ $errors -gt 0 ]]; then
  echo ""
  echo "❌ 版本检查失败，发现 $errors 个不一致。请同步更新 README.md 中的版本号。"
  exit 1
fi

echo "✅ 所有技能/Agent 版本与 README.md 一致"
exit 0

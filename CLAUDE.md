# victor-skills 开发指南

## 项目概述

Victor 的 Claude Code Skill 集合，用于提升日常开发效率。使用 skill.sh 进行管理

## 技能命名规范

- 技能目录名称无强制前缀要求，建议使用有意义的名称
- 例如：`log-query`、`pr-review`、`victor-log-query`

## 技能文件结构

每个技能目录包含：

```
skills/<name>/
└── SKILL.md          # 技能定义（必须）
```

### SKILL.md Frontmatter 格式

```yaml
---
name: <name>
version: 1.0.0
description: "技能简短描述"
---
```

## 常用命令

安装 & 更新技能包：
```bash
npx skills add ./skills
```
安装 & 更新某个技能
```bash
npx skills add ./skills --skill xxx
```

注意：默认安装 ClaudeCode (project 级别) 即可

## 发布流程

1. 发布前确保 README.md 已更新


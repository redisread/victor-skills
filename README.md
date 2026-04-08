# victor-skills
Victor 的 Claude Code Skill 集合，用于提升日常开发效率。使用 skill.sh 进行管理

## 快速安装&更新

```bash
npx skills add ./skills
```

## 技能列表

| 技能 | 描述 |
|------|------|
| `hackernews-digest` | 获取 Hacker News 热门文章并生成每日摘要，包含核心要点、可实践建议、灵感启发及社交媒体分享文案 |

## 目录结构

```
victor-skills/
├── skills/                    # 各技能实现
│   └── <skill-name>/
│       └── SKILL.md           # 技能定义文件
├── CLAUDE.md                  # Claude 开发指南
├── CHANGELOG.md               # 版本变更记录
└── README.md
```

## 开发新技能

1. 在 `skills/` 下创建新目录，命名无强制前缀要求
2. 创建 `SKILL.md` 定义技能行为（frontmatter 需包含 `name`、`version`、`description`）
3. 更新本 `README.md` 的技能列表


## 许可证

MIT

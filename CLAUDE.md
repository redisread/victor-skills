# Claude 开发指南

## 原则

- 使用中文回复


## 目录结构

```
victor-skills/
├── skills/                    # 各技能实现
│   └── <skill-name>/
│       └── SKILL.md           # 技能定义文件
├── .claude/agents/            # 自定义 Agent 定义
├── docs/                      # 项目参考文档
├── CLAUDE.md                  # Claude 开发指南
└── README.md
```

## 开发新技能

1. 在 `skills/` 下创建新目录，命名无强制前缀要求
2. 创建 `SKILL.md` 定义技能行为（frontmatter 需包含 `name`、`description`）
3. 更新本 `README.md` 的技能列表


## 安装/更新 技能

默认安装和更新到当前项目，除非指定其他目录。

优先更新单个技能(非交互式):
```bash
npx skills add ./skills/<skill-name> -y --agent claude-code --target .
```

更新全部技能(非交互式):
```bash
npx skills add ./skills -y --agent claude-code --target .
```



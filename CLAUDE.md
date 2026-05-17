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
2. 创建 `SKILL.md` 定义技能行为（frontmatter 需包含 `name`、`description`、`version`、`metadata`）
3. 更新本 `README.md` 的技能列表

## SKILL.md 规范

### frontmatter 字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 技能唯一标识（kebab-case） |
| `description` | string | 是 | 技能行为描述，包含触发关键词 |
| `version` | string | 是 | 语义化版本号，如 `1.0.0` |
| `metadata` | object | 是 | 扩展元数据 |

### metadata 结构

```yaml
metadata:
  author: <作者或维护者>
  homepage: <技能主页或文档链接（可选）>
  triggers: <触发关键词列表（可选）>
```

### version 约定

- 遵循 [SemVer](https://semver.org/)：`MAJOR.MINOR.PATCH`
- `MAJOR`：工作流或接口不兼容变更
- `MINOR`：新增功能或行为改进，向后兼容
- `PATCH`：修复 bug、文案调整、脚本优化
- 初始版本从 `1.0.0` 开始


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



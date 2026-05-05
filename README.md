# victor-skills

Victor 的 Claude Code Skill 集合，用于提升日常开发效率。使用 skill.sh 进行管理。

## 快速安装 & 更新

```bash
npx skills add ./skills
```

## 技能列表

| 技能 | 描述 |
|------|------|
| `apple-notes` | Apple Notes 备忘录管理，支持创建、查看、编辑、搜索、移动和导出笔记 |
| `article-images-gen` | 文案插图专家，为文章生成手绘风格插图 |
| `blog-push` | Hugo 博客文章智能发布工具 |
| `hackernews-digest` | 获取 Hacker News 热门文章并生成每日摘要 |
| `jike-digest` | 抓取即刻 Topic 热门内容，生成每日精选摘要 |
| `neat-freak` | 会话结束后的知识库洁癖级整理与同步 |
| `r2-uploader` | 上传文件到 Cloudflare R2 对象存储，返回公开访问 URL |
| `reddit-digest` | 抓取 Subreddit 热门 Post，生成深度摘要与解读 |
| `tool-save-to-notion` | 将工具链接保存到 Notion 工具箱 |
| `x-following-digest` | 获取 Twitter/X Following 最近 24 小时精选推文摘要 |

## 目录结构

```
victor-skills/
├── skills/                    # 各技能实现
│   └── <skill-name>/
│       └── SKILL.md           # 技能定义文件
├── docs/                      # 项目参考文档
├── CLAUDE.md                  # Claude 开发指南
└── README.md
```

## 开发新技能

1. 在 `skills/` 下创建新目录，命名无强制前缀要求
2. 创建 `SKILL.md` 定义技能行为（frontmatter 需包含 `name`、`description`）
3. 更新本 `README.md` 的技能列表

## 许可证

MIT

# victor-skills

Victor 的 Claude Code Skill 集合，用于提升日常开发效率。

## Agent 列表

| Agent | 版本 | 描述 |
|-------|------|------|
| `para-notes-agent` | 1.0.0 | PARA 笔记管理专家，基于 Apple Notes 整理、分类、清理笔记 |
| `quality-info-reviewer` | 1.2.0 | 高质量信息审查员，按 10 条标准评估 URL 或文本，判定是否值得读 |
| `weekly-tool-digest-agent` | 1.1.0 | 工具箱周报生成器，查询 Notion 工具箱最近一周新增工具并生成结构化汇总报告 |

## 技能列表

### 知识管理

| 技能 | 版本 | 描述 |
|------|------|------|
| `notion-zettelkasten` | 1.1.6 | Notion 卡片盒笔记系统（Zettelkasten）管理工具，支持文献笔记、灵感笔记、永久笔记的查询与创建，工具箱与领域管理，URL保存文章和工具 |

### 内容保存（已合并到 notion-zettelkasten）

以下技能已合并到 notion-zettelkasten，不再单独维护：

- ~~`url-to-notion`~~ → 功能 12：URL 保存到文献笔记
- ~~`tool-save-to-notion`~~ → 功能 13：URL 保存到工具箱

### 内容创作

| 技能 | 版本 | 描述 |
|------|------|------|
| `raft-article-illustrator` | 6.1.0 | 极简手绘风格插图提示词——用类比而非图解，输出中文提示词可直接用于 Midjourney / Gemini / DALL-E |
| `raft-essay` | 1.6.0 | 撰写工程哲学风格的长文，聚焦 AI Agent 协作与人机边界 |

### 产品设计

| 技能 | 版本 | 描述 |
|------|------|------|
| `user-experience-design` | 1.0.0 | 用户体验设计方法框架（基于《体验经济》）——顾客损失清单、主题化、峰终定律、游戏化，先跑体验目标再落地 UI（by Steven） |

### 发布部署

| 技能 | 版本 | 描述 |
|------|------|------|
| `blog-push` | 1.1.0 | Hugo 博客文章智能发布工具 |

### 工具基础设施

| 技能 | 版本 | 描述 |
|------|------|------|
| `r2-uploader` | 1.2.0 | 上传文件到 Cloudflare R2 对象存储（默认 REST API，wrangler 兜底） |

## 外部依赖技能

以下技能不是本仓库维护的，而是从远程 GitHub 仓库引用的外部依赖。仓库只记录依赖来源（见 `skills-lock.json`），不复制技能本体，安装从上游拉取。

| 技能 | 来源 | 描述 |
|------|------|------|
| `book-to-skill` | [virgiliojr94/book-to-skill](https://github.com/virgiliojr94/book-to-skill) | 把书籍/文档（PDF、EPUB、DOCX 等）蒸馏成结构化 Agent Skill |

**恢复外部依赖**（在新环境/机器上，先 clone 本仓库再执行）：

```bash
npx skills experimental_install
```

该命令读取 `skills-lock.json`（只含 `sourceType: github` 的外部依赖条目），从上游仓库重新拉取并安装。

**添加新的外部依赖**：

```bash
npx skills add <owner/repo> --skill <skill-name> --agent claude-code -y
```

安装后 `skills-lock.json` 会自动记录该技能的 `sourceType: github` 条目。提交 lock 文件即完成「收纳依赖」，技能本体不进入本仓库。

## 许可证

MIT

## 版本管理

每个技能/Agent 独立版本，遵循 [SemVer](https://semver.org/)。完整变更记录见 [CHANGELOG.md](./CHANGELOG.md)。

发版流程：

```bash
# 使用发布脚本（自动更新 SKILL.md、CHANGELOG、README、打 tag）
./scripts/release.sh <skill-name> <new-version>
```
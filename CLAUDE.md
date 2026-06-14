# CLAUDE.md

这个仓库维护 Victor 的 Claude Code Skills 和少量自定义 Agent。默认用中文沟通，改动要小、可安装、可复现。

## Repo Layout

```text
skills/<skill-name>/SKILL.md       单个 skill 定义
skills/<skill-name>/README.md      可选：复杂 skill 的补充说明
skills/<skill-name>/references/    可选：长参考资料
.claude/agents/                    自定义 Agent 定义
docs/                              项目参考文档
README.md                          skill/agent 列表
```

## Skill Authoring Rules

每个 `SKILL.md` 必须有 YAML frontmatter：

```yaml
---
name: kebab-case-name
description: 简洁说明能力、触发词、适用边界
version: 1.0.0
metadata:
  homepage: https://github.com/redisread/victor-skills#skill-name
---
```

正文建议结构：

1. 适用场景
2. 前置条件或依赖
3. 操作流程
4. 验证方式
5. 常见错误/降级方案

复杂内容不要塞进主 `SKILL.md`。把长示例、适配器细节、错误码表放到 `references/`，并在主文件中用相对链接指向。

## Description Quality

`description` 决定 skill 是否会被触发，必须包含：

- 主要能力
- 明确触发词
- 典型输入形式
- 不适用边界（必要时）

避免空泛描述，例如“帮助用户处理内容”。应该写成“当用户要求保存文章到 Notion、裁剪网页、url-to-notion 或提供 URL 并要求入库时使用”。

## Versioning

遵循 SemVer：

- `MAJOR`: 工作流、依赖、输出格式不兼容
- `MINOR`: 新能力或兼容性增强
- `PATCH`: 文案、错误处理、示例或小修复

修改 skill 行为时同步更新 `version`；只改仓库级文档可以不改 skill 版本。

## Local Install / Smoke Test

单个 skill：

```bash
npx skills add ./skills/<skill-name> -y --agent claude-code --target .
```

全部 skills：

```bash
npx skills add ./skills -y --agent claude-code --target .
```

全局稳定版安装：

```bash
npx skills add redisread/victor-skills --skill <skill-name> --agent claude-code -y -g
```

改动后至少做：

```bash
find skills -name SKILL.md -maxdepth 3
sed -n '1,40p' skills/<skill-name>/SKILL.md
npx skills add ./skills/<skill-name> -y --agent claude-code --target .
```

如果 skill 包含脚本或 CLI 调用，还要运行一个最小真实案例或 dry-run，并在交付时说明结果。

## README Rules

新增、重命名、删除 skill 或 agent 时必须同步 `README.md`：

- Agent 列表
- 技能列表
- 简短描述

README 是对人看的目录；`SKILL.md` 是对 Agent 的执行说明。不要让两者描述互相矛盾。

## Safety

- 不要提交 token、cookie、`.env`、Notion/Cloudflare/GitHub 凭据。
- 如果示例需要密钥，用 `$ENV_NAME` 占位。
- 不要把个人 Chrome、本机路径或私有数据库内容写进通用 skill。
- 逆向接口、第三方登录、自动发布类 skill 必须写清楚用户授权边界。

## Review Checklist

PR/交付前检查：

- `SKILL.md` frontmatter 完整且 YAML 可读
- `name` 与目录名一致，使用 kebab-case
- `description` 足够触发，但不过度泛化
- 版本号按 SemVer 更新
- README 列表同步
- 本地安装命令通过
- 没有泄露凭据、本机隐私路径或过期命令

## Common Gotchas

- `npx skills add ./skills` 会安装全部 skill，调试单个 skill 时优先指定目录。
- 复杂 skill 的主文件越长，触发后上下文成本越高；主文件保留流程，长资料放 `references/`。
- 修改触发词后要实际观察是否更容易误触发；必要时收窄 description。

# URL 保存工具箱 — 信息提取规则

> 适用场景：功能 13「URL 保存到工具箱」。用户提供 URL 后，抓取页面并按以下规则提取工具名称、描述、类型、标签和封面图。

## 提取目标

访问 URL 后提取以下字段（对应工具箱数据库属性）：

| 字段 | 来源 | 必填 |
|------|------|------|
| 工具名称 | 页面标题 / og:title | ✅ |
| 描述 | meta description / 页面简介 | ✅ |
| 标签 | meta keywords、页面技术名词 | 可选 |
| 类型 | 根据域名和页面特征判断 | 可选 |
| 封面图 URL | og:image / twitter:image | 可选 |

## 按域名规则

### GitHub
- 标题：仓库名称（`repo`）
- 描述：仓库简介
- 标签：GitHub topics + 主要语言
- 类型：工具包（默认）/ 软件（有 release 时）
- 封面：`https://opengraph.githubassets.com/1/{owner}/{repo}`

### Chrome Web Store
- 标题：扩展名称
- 描述：简短描述
- 类型：浏览器插件
- 封面：商店页面主图

### npm / PyPI
- 标题：包名
- 描述：package.json 中的 description
- 类型：工具包
- 标签：从 README 提取技术关键词

### 官网 / SaaS
- 标题：站点名称
- 描述：hero section 或 meta description
- 类型：网站（默认）/ 软件（有桌面客户端时）
- 封面：og:image

## 类型判定优先级

1. URL 域名特征（chromewebstore → 浏览器插件）
2. 页面内容特征（有 `pip install` → 工具包）
3. 用户明确指定
4. 默认：网站

## 标签生成规则

标签写入工具箱的 `标签` 属性（multi_select），最多 5 个：

1. **平台/语言** — 从技术栈提取（Python、Chrome、Node、AI …）
2. **功能类别** — 从页面描述提取（生产力、开发、设计、写作 …）
3. **来源标签** — 如 GitHub 仓库可加 `开源`

## 不适用

本文件仅用于功能 13「URL 保存到工具箱」。文献笔记的 URL 保存（功能 12）使用独立的抓取和翻译流程，见 SKILL.md 功能 12 章节。

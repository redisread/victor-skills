# URL 信息提取规则

## 提取目标

访问 URL 后提取：
1. **工具名称** — 页面标题或 og:title
2. **描述** — meta description 或页面简介
3. **关键词** — meta keywords、页面技术名词
4. **页面类型** — 根据域名判断
5. **封面图 URL** — og:image 或 twitter:image（可选）

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
- 从页面提取技术关键词（最多 5 个）
- 包含平台/语言标签（如 Python、Chrome、AI）
- 包含功能标签（如 生产力、AI、开发）

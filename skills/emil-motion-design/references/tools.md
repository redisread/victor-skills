# Emil 推荐的工具与库

来自 Emil Kowalski 的公开推文、博客、课程侧记。可作为选型参考。

## 动效框架

### Motion（原 Framer Motion）

- **定位**：主力动效库
- **优点**：spring 物理、可中断动画、layout animation、AnimatePresence
- **缺点**：**"quite heavy"**——简单项目他不推荐引入，用 CSS transitions 更好
- **杀手 feature**：`useSpring` 拯救「生硬的鼠标绑定动效」
- **`AnimatePresence` mode='popLayout'**：删除元素时其他元素平滑重排

### CSS Transitions vs Keyframes

**Emil 的偏好**：CSS transitions > keyframes。

- Transitions **可中断可重定向**（用户反悔时能立即回退）
- Keyframes 一旦触发就跑完（除非手动 abort）
- 生产 UI 应该默认用 transitions

### View Transitions API

- 浏览器原生 morph 状态
- 现代 Chromium 系支持，Safari 逐步跟进
- 未来会取代大量 Framer Motion 场景

### Intersection Observer

- 简单场景替代 Motion 的 `useInView`
- 无需引入动效库，原生够用

## 动效工具

| 工具 | 用途 |
|------|------|
| **easing.dev** | 自定义 cubic-bezier 可视化 |
| **easings.co** | 同上 |
| **bezier-easing** | JS 端曲线插值库（Motion 底层用） |

## UI 库 / 组件

Emil 自己或推荐的高质量组件：

| 组件 | 作者 | 用途 |
|------|------|------|
| **Sonner** | Emil | Toast |
| **Vaul** | Emil（⚠️ unmaintained） | Drawer |
| **NumberFlow** | @barvian（Emil 推荐） | 数字动画 |
| **input-otp** | Emil 推荐 | 一次性密码输入 |
| **Liveline** | Emil 推荐 | 实时图表 |
| **Leva** | Emil 推荐 | 可定制 GUI（原型/调试用） |
| **cmdk** | Emil 推荐 | 命令菜单 |

## Primitive / 无样式基础

| 库 | 作用 |
|------|------|
| **Radix** | a11y + focus 管理 primitive，Vaul 就是基于 Radix Dialog |
| **Base UI** | 新一代 primitive（Radix 团队新项目） |
| **shadcn/ui** | 已内置很多 origin-aware 修复，装完即用 |

## Emil 日常应用（都是「小而美」）

不是动效直接工具，但反映他的审美取向：

| App | 用途 |
|-----|------|
| **Cleanshot** | 截图 |
| **Eagle** | 灵感收集 |
| **Obsidian** | 笔记 |
| **Things** | To-do |
| **Cron** | 日历 |
| **Raycast** | 启动器（**反面案例：故意无动画**，高频操作不该动画） |

## AI / Coding Agents

| 工具 | 用途 |
|------|------|
| **Claude Code** | Emil 主力 coding agent |
| **Codex** | 备选 |
| **Cursor** | 推荐其 Thermo-Nuclear Code Quality Review skill |
| **Anthropic 的 skill-creator skill** | 打包 skill 用 |

## 调试动画

Emil 分享的调试路径：

1. **Safari devtools → 手机连电脑真机测试**
   - Mac 用 USB 连 iPhone，Safari 里能直连调试手机页面
   - 真机才能测出 iOS 系统级动画干扰
2. **Xcode Simulator** — 替代方案（没实机时）
3. **逐帧 / 慢动作播放动画**
   - Chrome DevTools Performance 面板录制
   - Motion 有 `useMotionValue` + console.log 可以逐帧看数值
4. **`prefers-reduced-motion` 测试**
   - macOS：System Settings → Accessibility → Display → Reduce Motion
   - 所有动画都要在开这个开关的情况下测一遍

## Skills 生态（他自己开源的）

**GitHub**: https://github.com/emilkowalski/skills（18.2k stars）

**安装**：
```bash
npx skills@latest add emilkowalski/skills
```

**已发布的 skills**：

| Skill | 用途 |
|-------|------|
| `/animations` | 完整动画方法论包 |
| `/emil-design-eng` | 综合设计工程 skill（>100k 字符） |
| `/review-animations` | 审查现有项目动画 |
| `/improve-animations` | 用最强模型审 + 便宜模型执行 |
| `/find-animation-opportunities` | 发现值得加动画的地方 |
| `/animation-vocabulary` | 词汇表 skill |
| `/apple-design` | 从 Apple WWDC 提炼的 17 条原则 |

**核心主张**：*AI doesn't replace such expertise, it amplifies what you can get out of it.*

如果本 skill 不够用，可以直接 `npx skills add emilkowalski/skills/animations` 获取 Emil 原版更详细的方法论。

---
name: emil-motion-design
description: Web UI 动效与微交互设计方法框架，基于 Emil Kowalski（Linear / 前 Vercel 设计工程师，Sonner/Vaul 作者）公开分享的原则、模式与词汇。当用户要设计/审查 Web UI 动画（toast、drawer、popover、按钮反馈、页面切换、列表 stagger 等）、决定动画时长和 easing、审计现有项目动画质量、写代码需要精确动效词汇时使用；触发词包括「UI 动效」「Web 动画」「微交互」「动画审计」「toast 动效」「drawer 动效」「origin-aware」「easing 选择」「animation timing」「stagger」「purposeful animation」「emil kowalski」。不适用于游戏/影视动画、SVG 手绘动画、3D 场景动画、纯装饰性 marketing hero 动画。
version: 1.0.0
metadata:
  homepage: https://github.com/redisread/victor-skills#emil-motion-design
  source: 基于 Emil Kowalski 公开分享（emilkowal.ski / animations.dev / X @emilkowalski / Sonner / Vaul）
---

# emil-motion-design

> Web UI 动效设计的工程哲学。把动画从「装饰品」升级为「服务功能的工具」。核心信念是：**动画必须有目的、必须够快、必须来自触发点、必须可中断**。任何 UI 动画的第一个问题不是「怎么让它更炫」，而是「它到底该不该存在」。

## 使用时机

**必用**（在这些场景之前先跑本 skill）：
- 给一个 Web 组件设计新动效（modal、drawer、toast、popover、dropdown、command menu 等）
- 决定某个交互的动画时长、easing、方向
- 审计现有项目的动画质量（判断哪些该删、哪些该改、哪些缺失）
- 需要用精确词汇跟 AI/协作者描述动画意图（如 stagger / origin-aware / crossfade）

**可选**：写代码时查一次时长表 / easing 表，参考 `references/timing-easing.md`；实现具体模式时查 `references/patterns.md`。

**不适用**：游戏/影视动画（浏览器渲染优化模型不同）、纯装饰的 marketing hero 动画（可以更 loose）、SVG 手绘/3D 动画（超出方法论范围）。

## 输入 → 输出

**输入**至少给到：
- 要设计/审查的 UI 触点（一句话描述）
- 使用频率（高频每天多次 / 中频 / 低频只用几次）
- 交互触发方式（点击 / 键盘 / hover / 滚动 / 拖拽）

**输出**（按需选择）：
- **设计新动效**：动画目的 → 时长 → easing → transform-origin → 可中断性 → 代码骨架
- **审计现有动效**：按 8 类审计维度给出问题清单 + before/after 建议
- **快速决策**：直接从流程图给出时长和 easing

## 5 条核心原则（Purposeful Motion 五问）

设计任何 UI 动画前，按顺序问自己 5 个问题。任何一个答不出来，先把答案想清楚再动手。

### 原则 1：这个动画的目的是什么？

> "The best animation is no animation."

动画只应该服务这几个目的之一：**帮助理解状态变化 / 增强响应感 / 建立空间一致性 / 制造有意的惊喜**。

- 答不出目的 → 删掉，什么都不加
- 目的仅仅是「让它看起来更活」→ 也删掉
- 键盘触发的操作（快捷键、Enter 确认等）→ **永远不加动画**（Raycast 反例：越无动画越快）

### 原则 2：这个交互频率多高？

> High-frequency animations should be short or non-existent.

- 高频（每天几十次以上）→ 动画必须极短（100–150ms）或直接删除 transition
- 中频（每天几次）→ 标准时长（150–250ms）
- 低频（一天最多一次）→ 可以有惊喜性（200–300ms，可加 spring/overshoot）
- 悬停过渡（每小时几十次）→ **考虑完全移除 transition**

**300ms 是 UI 动画的硬上限**（marketing 页可以突破）。Vaul drawer 是罕见的例外（500ms，因为是全屏 modal 且模仿 iOS Sheet）。

### 原则 3：Easing 用哪个？

**默认走这个决策树**（详见 `references/timing-easing.md`）：

```
元素进入/退出视口？
  ├─ 是 → ease-out 或自定义 cubic-bezier（快开慢收，给响应感）
  └─ 否，屏幕内 A→B 移动？
      ├─ 是 → ease-in-out（模拟汽车加减速）
      └─ spinner/marquee → linear
```

- **永远不用 ease-in** 做进入/退出（开头慢显得迟钝）
- **CSS 内置曲线力度都不够**，重要动画写自定义 cubic-bezier
- 基础 hover 背景色变化 → `ease`（内置足够）

### 原则 4：动画从哪里长出来？（Origin-aware）

> Popover/dropdown 默认从中心展开 = 凭空出现感。真正好的做法是从触发按钮那个位置展开。

- Radix / Base UI 都暴露了 `--radix-*-transform-origin` 或 `--transform-origin` CSS 变量
- shadcn/ui 已经内置了这个修复
- 也别从 `scale(0)` 起始，从 `scale(0.9)` 或 `0.93` 开始（元素永远保留可见形状，不「凭空出现」）

### 原则 5：这个动画能被中断吗？

> "CSS transitions are interruptible; keyframes aren't."

- 用户随时可能重新触发、反悔、快速切换状态——动画必须能就地重定向
- **优先用 CSS transitions**（transform / opacity），不用 keyframes
- 需要更精细控制的中断用 Motion / Framer Motion 的 spring
- 拖拽/swipe 类交互 → **momentum-based**，速度阈值触发消除，不是简单的距离阈值

## 8 类审计维度（Emil Audit）

改自 emilkowalski/skills 的 `improve-animations` skill。审查一个项目的动画时，按这 8 类逐一扫描：

1. **Purpose & Frequency** — 每个动画有目的吗？频率合理吗？（本 skill 原则 1、2）
2. **Easing & Duration** — 时长在阈值内吗？easing 选对了吗？（原则 3）
3. **Physicality** — origin 对吗？scale 起始值对吗？有物理感吗？（原则 4）
4. **Interruptibility** — 能被打断/重定向吗？（原则 5）
5. **Performance** — 只动 transform/opacity 吗？有 layout thrashing 吗？
6. **Accessibility** — 尊重 `prefers-reduced-motion` 吗？动效不阻塞信息传达？
7. **Cohesion** — 整个产品的动画节奏一致吗？相似交互用一致的 easing/时长？
8. **Missed Opportunities** — 哪些高价值触点缺动画？哪些状态变化太突兀？

输出**优先级发现表**（不是全部同优先级），格式见 `references/audit-template.md`。

## 常用模式速查

10 条即用模式，详细代码见 `references/patterns.md`：

| # | 模式 | 一句话 |
|---|-----|-------|
| 1 | Button press feedback | `:active { transform: scale(0.97) }` — 让界面「在听」 |
| 2 | Never scale(0) | 从 `scale(0.9)` 起，元素永不消失 |
| 3 | Origin-aware popover | 用 `--radix-*-transform-origin` 从触发点展开 |
| 4 | Tooltip group delay | 首个延迟，组内切换无延迟 |
| 5 | Hover 去 transition | 高频悬停即时响应 |
| 6 | Stagger ≤50ms | 元素间延迟不超过 50ms，不然显慢 |
| 7 | popLayout on remove | AnimatePresence popLayout 让删除后平滑重排 |
| 8 | Blur 兜底 | `filter: blur(2px)` 掩盖不完美过渡 |
| 9 | Parent hover, child animate | 分离触发器和效果解决 flickering |
| 10 | Clip-path reveal | 硬件加速的形状揭示 |

## 输出模板

**新动效设计**（例：给一个 dropdown 加动效）：

```markdown
### 目的
帮助用户理解 dropdown 从触发按钮展开的空间关系（原则 1）

### 频率
中频（一天点几次） → 标准时长

### 参数
- 时长：200ms（enter）/ 150ms（exit）
- Easing：ease-out（enter）/ ease-in-out（exit）自定义 cubic-bezier(0.2, 0, 0, 1)
- Transform-origin：--radix-dropdown-menu-content-transform-origin
- Enter：scale(0.95) → scale(1) + opacity 0 → 1
- Exit：scale(1) → scale(0.95) + opacity 1 → 0

### 可中断
CSS transitions on transform/opacity（用户 hover 出去时立即回退）

### 无障碍
@media (prefers-reduced-motion: reduce) { transition-duration: 0.01ms }
```

**审计报告**（详见 `references/audit-template.md`）。

## 交付前的自检清单

- [ ] 我能一句话说清这个动画的**目的**吗？如果不能——删掉
- [ ] 时长 ≤ 300ms 吗？（UI 硬阈值）
- [ ] Easing 是 ease-out 或 cubic-bezier 吗？（不是 ease-in）
- [ ] 有 origin 处理吗？（不是默认 center）
- [ ] 动画能被中断吗？（CSS transitions or spring）
- [ ] 只动了 transform / opacity 吗？（不动 width/height/top/left）
- [ ] 有 `prefers-reduced-motion` 兜底吗？
- [ ] 如果是高频交互——考虑过完全删除动画吗？

## 与其他技能/角色的配合

- **本 skill → frontend-design**：先跑动效原则确定 timing/easing/motion 意图，再让 frontend-design 落地视觉细节
- **本 skill → `user-experience-design`**（Steven）：体验目标 + 记忆点 → 决定哪些触点值得投入动效资源
- **本 skill 的审计模式 → PR review**：让 Claude 用 8 维度审当前 diff 的动效改动

## 反模式（避免这样用本 skill）

- 把 8 类审计维度做成打分表，追求高分（会导致过度动画）
- 拿到「必须 300ms 内」就把所有动画统一设 300ms（要根据频率梯度选）
- 把 spring 用在功能性图表（银行 App 的资产曲线）——那类要「no animation」
- 用 origin-aware 但没接上 CSS 变量（Radix/Base UI 提供了，别自己算）
- 把 keyframes 当 transitions 用——用户反悔时动画不能中断

## 补充参考

- `references/timing-easing.md` — 时长表 + easing 决策树 + spring 参数
- `references/patterns.md` — 10 条动画模式的完整代码
- `references/vocabulary.md` — 80+ 动画词汇表（跟 AI / 协作者精确沟通用）
- `references/components.md` — Sonner + Vaul 完整设计复盘（造类似组件时抄决策链）
- `references/audit-template.md` — 8 维度审计报告模板 + 输出格式
- `references/tools.md` — Emil 推荐的动效工具/库/调试方法

## 来源

本 skill 基于 Emil Kowalski（@emilkowalski，Linear / 前 Vercel 设计工程师）的公开分享汇编：
- 博客 https://emilkowal.ski/ui（9 篇动效文章）
- 动画词汇表 https://animations.dev/vocabulary
- Skills 仓库 https://github.com/emilkowalski/skills（`improve-animations` 等 6 个 skill）
- 开源组件 Sonner / Vaul 的设计复盘

不含付费课程 animations.dev/motion 正文内容。⚠️ **Vaul 已被作者标注为 unmaintained**（"I might come back to it at some point, but not in the near future"）——生产选型时考虑替代方案（如 Base UI Dialog）。

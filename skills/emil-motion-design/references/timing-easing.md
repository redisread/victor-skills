# Timing & Easing 决策参考

Emil Kowalski 的动效时间/曲线体系。所有数字都来自他公开分享和 Sonner/Vaul 实现。

## Timing 表（UI 动画）

| 场景 | 时长 | 说明 |
|------|------|------|
| 微交互（按钮 press feedback、hover 状态） | **100–150ms** | 高频，尽可能短 |
| 标准 UI（dropdown、popover、tooltip enter） | **150–250ms** | 大多数场景默认区间 |
| 模态 / 抽屉 enter | **200–300ms** | 单一大动作，可以稍长 |
| Sonner toast enter | 400ms | Toast 是「有意让你注意到」，可以突破 300ms |
| Vaul drawer（iOS 风格全屏 modal） | 500ms | 主要 modal 而非高频交互，模仿 iOS Sheet |
| 元素间 stagger 延迟 | **≤50ms** | 超过 50ms 感知就慢了 |
| Tooltip 首次打开延迟 | 有（防误触） | 组内切换：0ms（`data-instant` 属性） |
| Marketing hero / 页面加载 | 可以更长 | 不受 UI 300ms 限制 |
| **UI 动画硬上限** | **300ms** | 超过 300ms 感知就 sluggish |

**感知加速小技巧**：转得更快的 spinner 让整个应用看起来加载更快（同样的等待时间下）。

## Easing 决策流程

```
┌─────────────────────────────────────────┐
│ 元素进入 / 退出视口？                    │
├────┬─────────────────────────────────────┤
│ 是 │ ease-out（默认）或自定义 cubic-bezier
│    │ （快开慢收，enter/exit 都用）
├────┴─────────────────────────────────────┤
│ 否，屏幕内 A→B 位置移动？                │
├────┬─────────────────────────────────────┤
│ 是 │ ease-in-out（模拟汽车加减速）
├────┴─────────────────────────────────────┤
│ 是 spinner / marquee？                   │
├────┬─────────────────────────────────────┤
│ 是 │ linear（唯一合法使用 linear 的场景）
├────┴─────────────────────────────────────┤
│ 是 hover 上的简单背景色变化？            │
├────┬─────────────────────────────────────┤
│ 是 │ ease（CSS 内置足够）
├────┴─────────────────────────────────────┤
│ 其他 / 重要动画                          │
├────┬─────────────────────────────────────┤
│    │ 自定义 cubic-bezier > CSS 内置
│    │ 工具：easing.dev / easings.co
└────┴─────────────────────────────────────┘
```

### 硬规则

- **永远不用 `ease-in`** 做 enter/exit：开头慢让界面感觉迟钝
- **CSS 内置曲线力度都不够**——重要动画写自定义 cubic-bezier
- **enter 和 exit 用不同 easing 可能更好**——enter 用 ease-out，exit 用 ease-in-out

## 推荐 cubic-bezier

来自 Emil 的组件源码：

```css
/* Vaul drawer 用的（来自 Ionic Framework，接近 iOS 感觉） */
transition-timing-function: cubic-bezier(0.32, 0.72, 0, 1);

/* 通用 ease-out，比 CSS 内置的更 punchy */
transition-timing-function: cubic-bezier(0.2, 0, 0, 1);

/* enter 用 ease-out，exit 用 ease-in-out */
&[data-state='open']  { transition-timing-function: cubic-bezier(0.2, 0, 0, 1); }
&[data-state='closed'] { transition-timing-function: cubic-bezier(0.4, 0, 0.6, 1); }
```

## Spring 参数指南

Spring 是**物理驱动**动画，不是固定时长——最适合装饰性动画、按钮反馈、拖拽物理。

| 参数 | 效果 |
|------|------|
| **Stiffness / Tension** | 越高越 snappy（快速抵达终点） |
| **Damping** | 越低越 bouncy（overshoot 明显） |
| **Mass** | 越重越慢（惯性大） |
| **Velocity** | 中断时保留速度和方向 |

### 什么时候不该用 spring

- **功能性图表**（银行 App 的账户曲线、监控 dashboard）→ 弹簧会让数字显得不可信，用 `no animation` 或 linear 更好
- **纯 marketing loading state** → 会分散注意力

### Motion (原 Framer Motion) 常用 spring 配方

```jsx
// 按钮弹起
{ type: 'spring', stiffness: 400, damping: 30 }

// iOS 风格 sheet
{ type: 'spring', stiffness: 300, damping: 35, mass: 1 }

// 拖拽后回弹
{ type: 'spring', stiffness: 500, damping: 40 }
```

## 关键 CSS 属性小抄

- `will-change: transform` — 消除 1px 末尾偏移，提升为 GPU 独立层。**不要滥用**（GPU 内存代价）
- `transform-origin` — origin-aware 动画的核心；配合 CSS 变量最灵活
- `filter: blur(2px)` — 缓动和时长都调不好时的兜底
- `tabular-nums` — 数字列不跳位（价格、时间等）
- `clip-path: inset(...)` — 硬件加速的 reveal / mask
- `@starting-style` — 未来简化 enter 动画（浏览器支持逐步完善）

## `prefers-reduced-motion` 兜底

**所有生产动画都必须支持**。最小实现：

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

更精细的做法：保留信息传递必需的动画（如 loading spinner 仍要转），只关掉装饰性的（enter/exit 缩放等）。

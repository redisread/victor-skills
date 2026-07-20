# 组件设计复盘：Sonner + Vaul

Emil Kowalski 两个代表作的完整决策链，用于造类似组件时抄决策 / 拆思路。

---

## Sonner — Toast 组件

**GitHub**: github.com/emilkowalski/sonner
**Docs**: https://sonner.emilkowal.ski
**License**: MIT

### 命名与定位

- **命名**：Sonner，法语「to ring」——**牺牲可发现性换独特/优雅**
- **定位**：`opinionated toast component for React`
- **护城河**：DX + 美感。作者原话：*People simply like beautiful things.*

### 动效核心决策

| 决策点 | 选择 | 原因 |
|--------|------|------|
| 时长 | 400ms enter | Toast 是「有意让用户注意到」，可以突破 UI 300ms 上限 |
| 起始位置 | `translateY(100%)` → `translateY(0)` | 从屏幕外滑入，符合空间直觉 |
| Easing | `ease`（默认）| 简单方向性动画，内置足够 |
| 实现方式 | **CSS transitions**，不用 keyframes | **可中断可重定向**（用户 hover / 快速关闭时能立即回退） |

### 堆叠动画

多个 toast 同时存在时的位置和缩放规则：

```
第 N 个 toast (index=0 最前):
  y = -index * gap
  scale = 1 - index * 0.05
  height = 前排 toast 的高度 (统一)
```

关键点：**堆叠时把所有 toast 强制设为最前方 toast 的高度**——不然堆叠会视觉抖动。

### Swipe to Dismiss

- **momentum-based** 不是简单距离阈值：速度 > `0.11` 或距离 > `SWIPE_THRESHOLD` 即消除
- 用 **pointer capture** 保证鼠标/手指移出 toast 仍能拖
- 释放时如果速度大 → 惯性甩出；速度小距离不够 → 弹回

### 暂停与冻结

- **Hover 冻结计时器**——鼠标停在 toast 上时不会消失
- **`document.hidden` 时冻结**——切标签页回来 toast 还在（用 `useIsDocumentHidden` hook 检测）

### API 设计

**Observer Pattern**（无 hooks/context 依赖）：

```tsx
// 任何地方都能触发，不需要 provider 包裹调用者
import { toast } from 'sonner'

toast('Hello')
toast.success('Done')
toast.error('Failed')
toast.loading('Uploading...')

// promise 三态自动化
toast.promise(uploadFile(), {
  loading: 'Uploading...',
  success: (data) => `Uploaded ${data.name}`,
  error: 'Upload failed',
})
```

**完整调用形式（8 种）**：`toast()` / `.success` / `.error` / `.loading` / `.promise` / `.action` / `.cancel` / `.custom` / `.headless`

### 常用 options

| Option | 默认 | 说明 |
|--------|------|------|
| `description` | - | 副标题 |
| `closeButton` | `false` | 右上关闭按钮 |
| `duration` | `4000ms` | 自动关闭时长 |
| `position` | `bottom-right` | 位置 |
| `dismissible` | `true` | 是否可关 |
| `icon` | - | 自定义图标 |
| `action` | - | JSX；`event.preventDefault()` 阻止关闭 |
| `cancel` | - | 同上 |
| `id` | - | 复用相同 id 更新已有 toast |
| `onDismiss` / `onAutoClose` | - | 回调 |

**未文档化的隐藏变体**：`toast.warning` / `toast.info` / `toast.message`（存在但不在文档）。

---

## Vaul — Drawer 组件

**GitHub**: github.com/emilkowalski/vaul
**Docs**: https://vaul.emilkowal.ski
**License**: MIT
**Stars**: 8.5k / 362 forks / v1.1.2（2024-12-14）

### ⚠️ 维护状态提醒

作者已标注 **unmaintained**：

> "I might come back to it at some point, but not in the near future."

**生产选型建议**：
- 关键项目考虑 fork 或用 Base UI Dialog 手工实现拖拽
- Emil 自己在 Linear 应该没继续维护 Vaul（爱好项目）

### 定位

- **原型**：iOS Apple Sheet
- **基础**：**Radix Dialog primitive**（继承 a11y + focus 管理，不重复造轮子）
- **技术栈**: TypeScript 96.5%

### 组件结构

```
Drawer.Root
  ├─ Drawer.Trigger
  └─ Drawer.Portal
       ├─ Drawer.Overlay
       └─ Drawer.Content
            ├─ Drawer.Title
            ├─ Drawer.Description
            ├─ Drawer.Handle
            └─ Drawer.Close
```

### Root Props（完整表）

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `defaultOpen` | boolean | - | 非受控初始状态 |
| `open` | boolean | - | 受控状态 |
| `onOpenChange` | function | - | 状态变化回调 |
| `modal` | boolean | **true** | modal 模式 |
| `container` | HTMLElement | `document.body` | Portal 容器 |
| `direction` | `bottom` \| `top` \| `left` \| `right` | **bottom** | 出现方向 |
| `onAnimationEnd` | function | - | 动画结束回调 |
| `dismissible` | boolean | **true** | 允许 swipe/click backdrop 关闭 |
| `handleOnly` | boolean | **false** | 只有 handle 可拖 |
| `repositionInputs` | boolean | **true** | 键盘出现时重新定位输入框 |
| `snapPoints` | array | - | 多档吸附点 |
| `activeSnapPoint` | any | - | 当前档 |
| `setActiveSnapPoint` | function | - | 设置档 |
| `fadeFromIndex` | number | - | 从第几档开始淡入 backdrop |
| `snapToSequentialPoint` | boolean | - | 顺序吸附 |

其他子组件（Trigger / Overlay / Content / Close / Title / Description）都只有 `asChild` prop（默认 false，用于组合原生元素）。Handle 和 Portal 无 prop。

### 动效核心决策

| 决策点 | 选择 | 原因 |
|--------|------|------|
| 缓动曲线 | `cubic-bezier(0.32, 0.72, 0, 1)` | 来自 Ionic Framework，接近 iOS 感觉 |
| 时长 | **500ms** | 突破 UI 300ms 上限——因为是主要 modal 而非高频交互 |
| 起始位置 | `translateY(100%)` | 从底部滑入 |
| 实现方式 | CSS transitions + JS 控制拖拽 | 平衡「可中断」和「精确物理」 |

### 拖拽物理

- **Momentum-based**：轻甩即关闭（阈值：速度而非距离）
- **顶部阻尼**：拖过顶部继续向上时 "the more you drag, the less the drawer will move"（弹性衰减）
- **多点触控**：**首次触摸后忽略其他手指**（防止 pinch/双指干扰）
- **Snap points**：多个 checkpoint，释放吸附最近点，也支持甩过多个点

### 滚动交互（关键坑）

**问题**：drawer 内容可滚动，用户在滚动到顶时继续拖 = drawer 该关闭还是继续滚？

**解法**：
- `shouldDrag` 函数：只在**内容滚到顶时**允许拖 drawer 关闭
- **100ms 超时**防误触：滚动刚停 100ms 内不切换到拖 drawer 模式

### 性能坑（大列表）

**踩过的坑**：Vaul 用 CSS 变量传递拖拽位置到子元素——但 >20 项列表时，父元素 CSS 变量变化会触发**子元素全部 style recalc**，卡到不能用。

**改法**：**直接在元素上设 `transform`**，绕过 CSS 变量继承路径。

### Backdrop 变形（scaleBackground）

Vaul 有个杀手 feature：`scaleBackground` prop 抓 `[vaul-drawer-wrapper]` 元素应用 transform + border-radius，制造**「body 变成 sheet 卡片」**的错觉（iOS iPhone 上 Safari 分享 sheet 就是这效果）。

### 输入框适配

- **Visual Viewport API** 监听键盘 resize
- 键盘弹起时自动调整抽屉高度和位置
- 已知 trade-off：`resize` 事件延迟明显（Safari 特别慢）

---

## 通用组件设计信条

从 Sonner 和 Vaul 提炼的元原则，可以应用到任何 React 组件设计：

### 1. API 尽量像现有 primitive

- Sonner API 像 `react-hot-toast`（`toast()` 一个函数入口）
- Vaul API 像 Radix Dialog（`.Root` / `.Trigger` / `.Content` 结构）

**为什么**：降低学习成本，用户几乎不用查文档。

### 2. 站在肩膀上

- Vaul 用 Radix Dialog 做底层（focus trap / a11y / portal 全免费）
- 不重复造轮子，把精力花在自己的差异化（拖拽物理、iOS 感觉）

### 3. 交互式文档

- Sonner 和 Vaul 都自建演示站（不用 Storybook，而是手工做的 landing page）
- **文档本身就是最好的营销**——看到就想装

### 4. 美感是被低估的差异化杠杆

> People simply like beautiful things.

- 组件市场竞争激烈，功能上很难拉开差距
- **视觉+动效的第一印象**决定了大多数人是否深度试用
- Sonner/Vaul 的成功都归功于「看起来就想用」

### 5. 中断优先（Interruptible First）

- CSS transitions 优于 keyframes（可中断）
- 用户随时会反悔、重新触发——**动画必须能就地回退**
- 拖拽/swipe **momentum-based**，不是简单阈值

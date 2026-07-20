# 10 条动画模式（Patterns）

来自 Emil Kowalski 的博客与推文，每条都带完整代码。用作即插即用的动画模板。

---

## 1. Button Press Feedback（按钮按压反馈）

即时反馈让界面感觉「在听」——用户点下去就有响应。

```css
.button {
  transition: transform 100ms cubic-bezier(0.2, 0, 0, 1);
}
.button:active {
  transform: scale(0.97);
}
```

**加分做法**：结合微小的 blur 掩盖不完美：

```css
.button:active {
  transform: scale(0.97);
  filter: blur(0.5px);
}
```

**注意**：键盘触发（快捷键、Enter 确认）不适用——键盘用户看不到 `:active` 反馈也无所谓。

---

## 2. Never scale(0)（永不从 0 开始）

从 `scale(0)` → `scale(1)` 会给「凭空出现」的感觉。改用 `scale(0.9)` 或 `0.93`。

**反例**：
```css
/* ❌ 元素凭空出现 */
@keyframes pop-in {
  from { transform: scale(0); opacity: 0; }
  to   { transform: scale(1); opacity: 1; }
}
```

**正例**：
```css
/* ✅ 像瘪了的气球，永远保有可见形状 */
@keyframes pop-in {
  from { transform: scale(0.9); opacity: 0; }
  to   { transform: scale(1);   opacity: 1; }
}
```

**原理**：现实世界中没有东西从零大小突然变到有大小——从 0.9 起始像「充气」，从 0 起始像「凭空生成」。

---

## 3. Origin-Aware Popover / Dropdown

Popover 默认从中心展开 = 「appears out of nowhere」感。**从触发按钮那个位置展开**才符合空间直觉。

### Radix 用法

```css
[data-radix-popper-content-wrapper] {
  transform-origin: var(--radix-dropdown-menu-content-transform-origin);
  animation: fade-scale-in 150ms cubic-bezier(0.2, 0, 0, 1);
}

@keyframes fade-scale-in {
  from { opacity: 0; transform: scale(0.95); }
  to   { opacity: 1; transform: scale(1); }
}
```

### Base UI 用法

用 `var(--transform-origin)` 替换。

### shadcn/ui

**已经内置这个修复**，安装即用。

---

## 4. Tooltip Group Delay（分组延迟）

第一个 tooltip 有延迟（防误触），**组内切换到其他 tooltip 时无延迟、无动画**。

```tsx
// Radix 的 TooltipProvider
<TooltipProvider
  delayDuration={500}       // 首次打开延迟
  skipDelayDuration={0}     // 打开后跨 tooltip 无延迟
>
  {/* ...多个 Tooltip.Root */}
</TooltipProvider>
```

对应 CSS：

```css
.tooltip[data-instant] {
  transition-duration: 0ms !important;
  animation-duration: 0ms !important;
}
```

---

## 5. Hover 去 transition（高频即时响应）

高频悬停过渡（一天几百次）让界面感觉更慢——**移除 transition，让 hover 瞬时响应**。

```css
/* ❌ 高频 hover 加 transition 反而慢 */
.nav-link {
  transition: color 200ms;
}
.nav-link:hover { color: var(--accent); }

/* ✅ 高频 hover 即时响应 */
.nav-link {
  color: var(--fg);
}
.nav-link:hover { color: var(--accent); }
```

**判断依据**：如果这个 hover 用户一天会触发几十次以上——去掉 transition。低频 hover（比如设置里的选项 hover）可以保留。

---

## 6. Stagger ≤50ms

多元素同时出现时给每个加小延迟制造 cascade 效果。**元素间延迟不能超过 ~50ms**——超过会让整个流程显得慢。

```css
.list-item {
  animation: slide-up 200ms cubic-bezier(0.2, 0, 0, 1) both;
}
.list-item:nth-child(1) { animation-delay: 0ms; }
.list-item:nth-child(2) { animation-delay: 30ms; }
.list-item:nth-child(3) { animation-delay: 60ms; }
.list-item:nth-child(4) { animation-delay: 90ms; }
/* ... */

@keyframes slide-up {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

或用 CSS 变量 + `--index`：

```css
.list-item {
  animation-delay: calc(var(--index) * 30ms);
}
```

**大列表提醒**：不要在 20+ 项列表上用 stagger，用户等最后一个出来的时间太长。改成 first-5 stagger + 其余 instant。

---

## 7. popLayout on Remove（平滑重排删除）

用 Framer Motion（现 Motion）的 `AnimatePresence` + `popLayout` mode，删除元素时其他元素平滑移动到新位置。

```tsx
import { AnimatePresence, motion } from 'framer-motion'

<AnimatePresence mode="popLayout">
  {items.map(item => (
    <motion.div
      key={item.id}
      layout                                  // 关键：启用 layout animation
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
      transition={{ duration: 0.2 }}
    >
      {item.content}
    </motion.div>
  ))}
</AnimatePresence>
```

**没 Motion 时的替代**：CSS `@starting-style` + `transition-behavior: allow-discrete`（现代浏览器）。

---

## 8. Blur 兜底（Bridge the Gap）

缓动和时长都调不好时——**加 blur** 掩盖不完美过渡。

```css
@keyframes swap {
  0%   { opacity: 1; filter: blur(0); }
  50%  { opacity: 0.5; filter: blur(4px); }
  100% { opacity: 1; filter: blur(0); }
}
```

**原理**：blur "bridges the visual gap between old and new states"——大脑对模糊的中间态更宽容，不再挑剔像素级的错位。

**注意**：blur 有性能成本，只在关键过渡用，别当默认。

---

## 9. Parent Hover, Child Animate（防闪烁）

Hover 动画应用到父元素本身会 flickering（动画改变父元素尺寸 → 鼠标脱离 → 又缩回 → 又 hover…）。

**解法**：父元素监听 hover，动画应用到子元素。

```css
/* ❌ Flickering */
.card {
  transition: transform 200ms;
}
.card:hover {
  transform: scale(1.05);
}

/* ✅ 稳定 */
.card:hover .card-inner {
  transform: scale(1.05);
}
.card-inner {
  transition: transform 200ms;
}
```

---

## 10. Clip-Path Reveal（硬件加速的形状揭示）

用 `clip-path` 做揭示动画——硬件加速、可以任意形状，不像 `width/height` 会触发 layout。

```css
/* 从左往右揭示 */
.reveal {
  clip-path: inset(0 100% 0 0);
  transition: clip-path 400ms cubic-bezier(0.2, 0, 0, 1);
}
.reveal.visible {
  clip-path: inset(0 0 0 0);
}

/* 圆形展开（材料设计经典） */
.ripple {
  clip-path: circle(0% at 50% 50%);
  transition: clip-path 300ms cubic-bezier(0.2, 0, 0, 1);
}
.ripple.active {
  clip-path: circle(150% at 50% 50%);
}
```

**适用场景**：图片对比 slider、tab 切换下划线、hero 揭示、button ripple。

---

## 附：性能红线

以下操作**只用 transform / opacity / filter**，不要动画这些属性：

| 属性 | 后果 |
|------|------|
| `width`, `height` | 触发 layout thrashing |
| `top`, `left`, `right`, `bottom` | 触发 layout thrashing |
| `margin`, `padding` | 触发 layout thrashing |
| `border-width` | 触发 layout thrashing |
| `background-color` | 触发 paint（可接受但慢） |

**改用**：
- 尺寸变化 → `transform: scale()`
- 位置变化 → `transform: translate()`
- 显隐变化 → `opacity`
- 尺寸 reveal → `clip-path`

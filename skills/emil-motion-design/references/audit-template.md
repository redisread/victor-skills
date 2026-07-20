# 8 维度动画审计模板

改自 emilkowalski/skills 的 `improve-animations` skill 输出格式。

## 审计流程

1. **扫描**：把项目里的所有动画列出来（`transition`、`animation`、`framer-motion` / `motion` 的 `motion.*` 组件、`react-spring`、`useSpring`、CSS keyframes）
2. **分类**：按下方 8 维度分类每个动画的问题
3. **优先级**：给每个问题打优先级（Critical / High / Medium / Low）
4. **建议**：每条问题给出 before / after 具体代码

## 优先级标准

| 优先级 | 判定 |
|--------|------|
| **Critical** | 影响可用性（比如键盘触发有动画阻塞、无 reduced-motion 兜底） |
| **High** | 明显违反核心原则（超 300ms、ease-in、scale(0) 起始、高频动画） |
| **Medium** | 精修问题（origin 没处理、stagger 过 50ms、能用 blur 但没用） |
| **Low** | 打磨机会（可以加动画但没加的地方） |

## 8 维度扫描清单

### 1. Purpose & Frequency

- [ ] 每个动画都能说清楚**目的**吗？（帮理解 / 增强响应 / 空间一致 / 有意惊喜）
- [ ] 高频交互（一天几十次以上）动画是不是太长？考虑删掉
- [ ] 键盘触发的操作是否**误加了动画**？（应该没有）
- [ ] 装饰性动画是否偷偷进入功能性场景？（例：银行账户曲线用了 spring）

### 2. Easing & Duration

- [ ] 所有动画时长 ≤ 300ms 吗？（marketing 除外）
- [ ] 用了 `ease-in` 做 enter/exit 吗？（应该没有）
- [ ] 是否统一用 `ease-out` 或自定义 cubic-bezier？
- [ ] Spinner / marquee 是否用 linear？
- [ ] 屏幕内 A→B 移动用 ease-in-out 吗？

### 3. Physicality

- [ ] Popover / dropdown 用了 origin-aware（`--radix-*-transform-origin`）吗？
- [ ] 从 `scale(0)` 起始吗？（应该 `scale(0.9)` 或 `0.93`）
- [ ] 元素消失是否有可见的过程？（不是「凭空消失」）
- [ ] 拖拽 / swipe 是 momentum-based 吗？

### 4. Interruptibility

- [ ] 用的是 CSS transitions 还是 keyframes？（可中断的场景应该用 transitions）
- [ ] 用户快速反悔操作时动画能立即回退吗？（手动测试）
- [ ] Framer Motion / Motion 用 spring 而不是硬 tween 吗？（可中断场景）

### 5. Performance

- [ ] 动画只用 `transform` / `opacity` / `filter` 吗？
- [ ] 有没有动画 `width` / `height` / `top` / `left`（layout thrashing）？
- [ ] 大列表（20+ 项）有 stagger 或 layout animation 吗？（可能卡）
- [ ] 有没有滥用 `will-change`（GPU 内存）？

### 6. Accessibility

- [ ] **所有生产动画都有 `prefers-reduced-motion` 兜底吗？**
- [ ] 动画时长不阻塞信息传达吗？（loading 不能太慢）
- [ ] 关键状态变化即使没动画也能感知吗？（颜色 / 图标 / 文字）
- [ ] 拖拽交互有键盘替代吗？

### 7. Cohesion

- [ ] 全站相似交互用一致的时长和 easing 吗？
- [ ] Toast、Modal、Drawer 之间的动效风格协调吗？
- [ ] 深浅色模式下动画质感一致吗？
- [ ] 移动端 / 桌面端时长有区分吗（触屏可以稍长）？

### 8. Missed Opportunities

- [ ] 有没有值得加动画的**状态变化被瞬变**了？（列表加删、tab 切换、accordion）
- [ ] 空状态 / 加载状态 / 错误状态是否有区分性动画？
- [ ] 有没有可以做**惊喜时刻**的低频操作？（首次成功、里程碑）
- [ ] Marketing 页 hero 有独特记忆点吗？

## 输出报告模板

```markdown
# 动画审计报告 — [项目名]

审计日期：YYYY-MM-DD
审计维度：Purpose, Easing, Physicality, Interruptibility, Performance, A11y, Cohesion, Opportunities

## 摘要

- 扫描到 **N** 个动画
- Critical: **X** / High: **Y** / Medium: **Z** / Low: **W**
- Top 3 阻塞项：[三行]

---

## Critical 问题

### C1. [问题标题]

**位置**：src/components/Dropdown.tsx:42
**维度**：Accessibility
**问题**：无 `prefers-reduced-motion` 兜底

**Before**：
```css
.dropdown {
  transition: transform 200ms ease-out;
}
```

**After**：
```css
.dropdown {
  transition: transform 200ms ease-out;
}
@media (prefers-reduced-motion: reduce) {
  .dropdown { transition-duration: 0.01ms; }
}
```

**Feel Check**：无障碍用户不再受动画影响，视觉正常用户体验不变。

---

## High 问题

### H1. [问题标题]

...（同格式）

---

## Medium 问题

### M1. [问题标题]

...（同格式）

---

## Low / Opportunities

### O1. [机会标题]

**位置**：src/pages/dashboard.tsx（列表加载）
**建议**：加 stagger 300ms 内完成（每项 40ms 延迟）
**理由**：首屏 dashboard 感受更"有序"，符合 CEO 说的"peak moment"设计

---

## Cohesion 观察

- [ ] Toast 用 400ms，Drawer 用 500ms，Dropdown 用 250ms —— 差异合理（频率梯度）
- [ ] 但 Modal 用 200ms 太短，建议改 300ms 与 Drawer 感觉靠近
- [ ] 全站有 3 种 easing 曲线在用，建议收敛到 2 种：`cubic-bezier(0.2, 0, 0, 1)` 和 `cubic-bezier(0.4, 0, 0.6, 1)`

---

## 附：动画清单

| 位置 | 类型 | 时长 | Easing | 目的 | 维度问题 |
|------|------|------|--------|------|----------|
| Button:active | transform scale | 100ms | ease-out | 反馈 | 无 |
| Dropdown enter | transform+opacity | 200ms | ease-out | 空间感 | 缺 origin-aware |
| ... | | | | | |
```

## 使用建议

- **先扫，再判优先级，最后写建议**——不要边扫边写建议（会遗漏）
- **每条建议给具体代码**，不要只描述「需要优化」
- **Feel Check** 那一行很重要——描述改完后**人的感觉**是什么，验证时能对上
- 如果扫出 50+ 条，只推 Top 10（Critical + High），Medium/Low 归到附录

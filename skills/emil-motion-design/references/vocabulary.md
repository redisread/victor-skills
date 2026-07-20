# 动画词汇表（80+ 术语）

来源：animations.dev/vocabulary（Emil Kowalski 整理）。

用途：跟 AI / 协作者 / PM 精确描述动画意图。Emil 的核心观点：**Vocabulary is a side-effect of domain expertise. Having the right words = getting the right output from AI.**

---

## 进入 / 退出（Entrances & Exits）

| 词汇 | 定义 |
|------|------|
| **Fade in / out** | 透明度变化 |
| **Slide in** | 从屏幕外进入 |
| **Scale in** | 从小到全尺寸，常配合淡入 |
| **Pop in** | 带轻微 overshoot / bounce |
| **Reveal** | 通过 clip-path / mask 逐步揭示 |
| **Enter / Exit** | 元素添加 / 移除时播放的动画 |

## 时序（Sequencing & Timing）

| 词汇 | 定义 |
|------|------|
| **Keyframes** | 定义 0% / 50% / 100% 帧，浏览器填间 |
| **Interpolation / Tween** | 生成中间帧 |
| **Stagger** | 元素依次动画，形成级联效果 |
| **Orchestration** | 多个动画协调 |
| **Delay** / **Duration** | 延迟 / 时长 |
| **Fill mode** | `forwards` 等，动画结束保持终态 |
| **Stepped animation** | 离散步进（如倒计时、逐帧动画） |

## 变换（Movement & Transforms）

| 词汇 | 定义 |
|------|------|
| **Translate** | 位移 |
| **Scale** | 缩放 |
| **Rotate** | 旋转 |
| **Skew** | 斜切 |
| **3D tilt / Flip** | rotateX / rotateY |
| **Perspective** | 3D 效果强度 |
| **Transform origin** | 变换锚点 |
| **Origin-aware animation** | 从触发器位置展开（非默认 center） |

## 状态过渡（Transitions Between States）

| 词汇 | 定义 |
|------|------|
| **Crossfade** | 一个淡出、一个淡入 |
| **Continuity transition** | 前后连贯保持定位感 |
| **Morph** | 平滑形变（如 Dynamic Island） |
| **Shared element transition** | 元素跨位置迁移（缩略图 → 卡片） |
| **Layout animation** | 尺寸/位置改变时动画而非瞬变 |
| **Accordion / Collapse** | 高度展开/折叠 |
| **Direction-aware transition** | 前进/后退方向反转 |

## 滚动（Scroll）

| 词汇 | 定义 |
|------|------|
| **Scroll reveal** | 进入视口时触发动画 |
| **Scroll-driven animation** | 进度绑定滚动位置 |
| **Parallax** | 前景后景不同速度 |
| **Page transition** | 路由切换动画 |
| **View transition** | 浏览器原生 morph 状态（View Transitions API） |

## 反馈 / 交互（Feedback & Interaction）

| 词汇 | 定义 |
|------|------|
| **Hover effect** | 悬停效果 |
| **Press / Tap feedback** | 按下反馈，subtle scale-down |
| **Hold to confirm** | 按住进度条 |
| **Drag** | 抓取移动，常带动量 |
| **Drag to reorder** | 列表拖排 |
| **Swipe to dismiss** | 拖走关闭 |
| **Rubber-banding** | iOS 边界回弹 |
| **Shake / Wiggle** | 错误提示 |
| **Ripple** | 波纹扩散 |

## Easing

| 词汇 | 定义 |
|------|------|
| **Easing** | 加速/减速节奏 |
| **Ease-out** | 快到慢；**UI 默认** |
| **Ease-in** | 慢到快；**通常避免** |
| **Ease-in-out** | 慢-快-慢，A→B 移动 |
| **Linear** | 匀速，只用于 spinner / marquee |
| **Cubic-bezier** | 自定义曲线 |
| **Asymmetric easing** | 加/减速不同速率 |

## 弹簧（Spring Animations）

| 词汇 | 定义 |
|------|------|
| **Spring** | 物理驱动（tension/mass/damping），非固定时长 |
| **Stiffness / Tension** | 越高越 snappy |
| **Damping** | 越低越 bouncy |
| **Mass** | 越重越慢 |
| **Bounce** | overshoot 再稳定 |
| **Perceptual duration** | 感知完成时间 |
| **Momentum** | 拖拽后惯性 |
| **Velocity** | 速度/方向，中断时保留 |
| **Interruptible animation** | 中途可重定向 |

## 循环 / 背景动效（Looping & Ambient）

| 词汇 | 定义 |
|------|------|
| **Marquee** | 无限循环滚动 |
| **Loop** | n 次或无限 |
| **Alternate (yoyo)** | 前后交替 |
| **Orbit** | 元素绕另一个 |
| **Pulse** | 温和缩放/透明度循环 |
| **Float** | 温和上下飘 |
| **Idle animation** | 等待时微动 |

## 精修 / 效果（Polish & Effects）

| 词汇 | 定义 |
|------|------|
| **Blur** | 软化或掩盖不完美 |
| **Clip-path** | 形状 reveal / mask / slider |
| **Mask** | 形状/渐变揭示 |
| **Before/after slider** | 拖分隔线切换两图 |
| **Line drawing** | SVG 路径自绘 |
| **Text morph** | 逐字符变化 |
| **Skeleton / Shimmer** | 加载占位 |
| **Number ticker** | 数字翻滚 |
| **Tabular numbers** | 等宽数字 |
| **Typewriter** | 逐字符出现 |

## 性能（Performance）

| 词汇 | 定义 |
|------|------|
| **Frame rate (FPS)** | 60fps 基线，120fps 新设备 |
| **Jank** | 掉帧可见卡顿 |
| **Dropped frame** | 错过绘制截止时间 |
| **Compositing** | GPU 移动/淡化图层，无需重排/重绘 |
| **will-change** | 提前把元素提升为独立层 |
| **Layout thrashing** | width/height/top/left 触发布局重算 |

## 原则（Principles to Know）

| 词汇 | 定义 |
|------|------|
| **Purposeful animation** | 动画服务功能，不只是装饰 |
| **Anticipation** | 主动作前小 wind-up（迪士尼动画原理） |
| **Follow-through** | 主动作后余韵，增加质感 |
| **Squash & stretch** | 变形传达重量/速度/柔韧 |
| **Perceived performance** | 让界面感觉更快 |
| **Frequency of use** | 高频动画更短更隐 |
| **Spatial consistency** | 元素跨状态保持身份/位置 |
| **Hardware acceleration** | 只动 transform/opacity 让 GPU 顺畅 |
| **Reduced motion** | 尊重 `prefers-reduced-motion` |

---

## 词汇使用示例

跟 AI 说「让这个 dropdown 更好看」→ AI 输出平庸。

跟 AI 说这样 →

> "Make this dropdown open with an **origin-aware** animation from the trigger button. Use **ease-out** cubic-bezier(0.2, 0, 0, 1), duration 200ms. Add a subtle **stagger** on the menu items with 30ms delay between each. Make sure it's **interruptible**—user closing mid-animation should reverse smoothly. Respect **prefers-reduced-motion**."

AI 输出立刻精准很多倍。这是 Emil 强调的「vocabulary = domain expertise = better AI leverage」。

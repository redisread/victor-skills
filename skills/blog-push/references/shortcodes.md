# Hugo Shortcodes 参考（zzo 主题）

## 盒子（Box / Boxmd）

支持 Markdown 语法的盒子：
```markdown
{{< boxmd >}}
This is **boxmd** — 支持 Markdown 语法
{{< /boxmd >}}
```

简单盒子（不渲染 Markdown）：
```markdown
{{< box >}}
This is **box** shortcode
{{< /box >}}
```

## 彩色提示框（Alert）

```markdown
{{< alert theme="info" >}}**信息** 内容{{< /alert >}}
{{< alert theme="warning" >}}**警告** 内容{{< /alert >}}
{{< alert theme="success" >}}**成功** 内容{{< /alert >}}
{{< alert theme="danger" >}}**危险** 内容{{< /alert >}}
```

## 展开栏（Expand）

```markdown
{{< expand "点击展开" >}}
折叠的内容（支持 Markdown）
{{< /expand >}}
```

## 选项卡（Tabs / Codes）

代码对比：
```markdown
{{< codes java javascript >}}
  {{< code >}}
  ```java
  System.out.println("Hello World!");
  ```
  {{< /code >}}
  {{< code >}}
  ```javascript
  console.log("Hello World!");
  ```
  {{< /code >}}
{{< /codes >}}
```

内容对比：
```markdown
{{< tabs Windows MacOS Ubuntu >}}
  {{< tab >}}
### Windows section
Windows 内容
  {{< /tab >}}
  {{< tab >}}
### MacOS section
MacOS 内容
  {{< /tab >}}
  {{< tab >}}
### Ubuntu section
Ubuntu 内容
  {{< /tab >}}
{{< /tabs >}}
```

> ⚠️ 每个 tab 的内容必须不同，否则 id hash 冲突导致 tab 无法切换。

## 图片（Image）

```markdown
{{< img src="https://example.com/image.jpg"
       title="图片标题"
       caption="图片描述"
       alt="alt 文本"
       width="700px"
       position="center" >}}
```

显示 front matter 封面图：
```markdown
{{< featuredImage >}}
```

## 按钮（Button）

```markdown
{{< button href="https://example.com" >}}访问博客{{< /button >}}
{{< button href="https://example.com" width="100px" height="36px" color="primary" >}}访问{{< /button >}}
```

## 彩色注意框（Notice）

与 `alert` 类似，样式略有不同：
```markdown
{{< notice success >}}success text{{< /notice >}}
{{< notice info >}}info text{{< /notice >}}
{{< notice warning >}}warning text{{< /notice >}}
{{< notice error >}}error text{{< /notice >}}
```

## 使用场景速查

| Shortcode | 适用场景 |
|-----------|----------|
| `boxmd` | 支持 Markdown 的提示框 |
| `box` | 简单提示框 |
| `alert` | 四色警示框（info/warning/success/danger）|
| `notice` | 四色注意框（info/warning/success/error）|
| `expand` | 折叠长内容 |
| `codes` / `tabs` | 多平台/多语言代码对比 |
| `img` | 需要标题和说明的图片 |
| `button` | 行动号召按钮 |
| `featuredImage` | 显示封面图 |

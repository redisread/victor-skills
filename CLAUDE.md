## 核心操作指引 
- 邮箱相关操作使用 gog 技能进行操作，我的邮箱是 wujiahong2013@gmail.com
- 获取 X（推特）相关数据 使用 autocli（指令参考 autocli twitter -h）
- 发布微信公众号文章, 使用 baoyu-post-to-wechat （Browser 方式）
- 发布 X Article ，使用 baoyu-post-to-x
- 发布 X tweet/thread 使用 autocli（指令参考 autocli twitter post -h）
- 发布 即刻(jike) 使用 autocli（指令参考  autocli jike create <text> ）
- 临时文件和无关文件、图片等存储在 /tmp/目录

## Notion 操作

- 操作 Notion 时请参考 `docs/notion_database_reference.md` 文件。
- 使用 /notion 操作 
- **创建笔记时必须设置 🚩 领域 属性**（关联到合适的领域页面）
- **创建新页面时必须同时设置 icon 和 cover**：
  - **icon**：优先使用 emoji（如 🧠📚🤖），也可用 external 图片链接
  - **cover**：使用 R2 存储的图片链接（上传到 R2 后返回 URL 设置为封面），推荐尺寸 1200x630
  - 封面图片生成或获取后，先上传到 R2（`wrangler r2 object put hugo-blog/agent/YYYYMMDD/filename.png --file <local-path> --remote`），再用返回的 `https://cos.jiahongw.com/...` 链接设置封面

## Apple Notes 操作

- 操作 Apple Notes 时请参考 `docs/apple_notes_reference.md` 文件。
- 使用 /apple-notes 操作
- 使用 PARA 方法管理 Apple Notes 备忘录


## 封面制作和画图参考指引 
- 使用 opencli gemini 命令进行绘图、图片生成或者生成封面，不要使用其他工具，使用示例: `opencli gemini image "小猪"`。（如果要参考可使用 `opencli gemini -h`


## 项目规范

所有 skill 保存在 skills 目录下  ，使用副本格式而不是软连接格式，和系统的技能保持一致 .






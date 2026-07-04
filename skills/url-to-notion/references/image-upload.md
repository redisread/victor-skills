# 图片上传参考

## Notion Files API

Notion 2025 年新增 Files API，可直接上传图片到 Notion 托管存储。

### 单文件上传流程（< 5MB）

```python
import json, subprocess, os

NOTION_KEY = open(os.path.expanduser("~/.config/notion/api_key")).read().strip()

# 1. 创建上传对象
r = subprocess.run(["curl", "-s", "-X", "POST",
    "https://api.notion.com/v1/file_uploads",
    "-H", f"Authorization: Bearer {NOTION_KEY}",
    "-H", "Notion-Version: 2025-09-03",
    "-H", "Content-Type: application/json",
    "-d", json.dumps({"filename": f, "content_type": mime})],
    capture_output=True, text=True)
file_id = json.loads(r.stdout)["id"]

# 2. 发送文件
subprocess.run(["curl", "-s", "-X", "POST",
    f"https://api.notion.com/v1/file_uploads/{file_id}/send",
    "-H", f"Authorization: Bearer {NOTION_KEY}",
    "-H", "Notion-Version: 2025-09-03",
    "-F", f"file=@{fpath};filename={f}"])
```

### 批量上传

```python
import time
file_ids = []
for f in sorted(os.listdir(IMG_DIR)):
    if not f.lower().endswith(('.jpg','.jpeg','.png','.gif','.webp')):
        continue
    # ... 上传单文件 ...
    file_ids.append((f, file_id))
    time.sleep(0.4)  # Rate limit ~3 req/s
```

### 在 block 中引用

```json
{
  "type": "image",
  "image": {
    "type": "file_upload",
    "file_upload": {"id": "<file_id>"}
  }
}
```

### 插入到正文指定位置

使用 `PATCH /v1/blocks/{page_id}/children` + `"after": "<block_id>"` 参数。

## API 限制

| 限制 | 值 |
|------|-----|
| 单文件最大 | 5MB（enforce_max_size=True） |
| API 版本 | `Notion-Version: 2025-09-03` |
| Rate limit | ~3 req/s |
| 每批 blocks | 100 个，500KB |
| 支持格式 | jpeg, png, gif, webp, svg, heic, tiff, avif, bmp, apng, ico |

## 错误处理

| 错误 | 原因 | 解法 |
|------|------|------|
| 400 | filename/content_type 错误 | 检查 MIME 类型 |
| 401 | NOTION_KEY 无效 | 检查密钥 |
| 413 | 文件超 5MB | 压缩或 multi_part |
| CDN 403 | Referer 防盗链 | 带 Referer 头下载 |

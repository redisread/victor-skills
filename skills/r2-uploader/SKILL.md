---
name: r2-uploader
description: 使用 Cloudflare R2 REST API 或 wrangler CLI 上传文件到 R2 对象存储，返回公开访问 URL。支持单文件上传、从远程 URL 直接上传、批量上传。默认走 REST API，wrangler 仅作兜底。当用户说"上传到 R2"、"传到 Cloudflare"、"存到 R2"、"上传图片/文件/附件"并提到 R2 或 wrangler 时使用。触发词：上传、R2、Cloudflare、存储、wrangler、bucket、对象存储、CDN 上传。
version: 1.2.0
metadata:
  homepage: https://github.com/victor-skills#r2-uploader
---

# R2 文件上传

使用 Cloudflare R2 REST API 上传文件到 R2 对象存储，自动回退到 wrangler CLI。

## 环境变量

| 变量 | 说明 |
|------|------|
| `$R2_BUCKET` | R2 存储桶名称（必填） |
| `$R2_DOMAIN` | 自定义域名（可选） |
| `$CLOUDFLARE_API_TOKEN` | Cloudflare API Token（必填，REST API 走这个；从 `~/.config/cloudflare/env.sh` 加载） |
| `$R2_ACCOUNT_ID` | Cloudflare Account ID（必填，REST API 走这个） |

## 核心流程

```
定位文件 → 生成路径 → 优先 REST API → 失败则 wrangler 兜底 → 返回 URL
```

## Step 1: 定位文件

按优先级搜索常见目录（避免无边界搜索整个 home）：

```bash
# 优先搜索常见目录
find ~/Downloads ~/Desktop ~/Documents /tmp -maxdepth 3 -name "<filename>" -type f 2>/dev/null | head -5

# 未找到时扩大范围（仍限深度）
find ~ -maxdepth 5 -name "<filename>" -type f 2>/dev/null | head -5
```

## Step 2: 生成路径

```bash
R2_PATH="agent/$(date +%Y%m%d)/$(basename "<file>")"
```

## Step 3: 上传（优先 REST API）

**优先 REST API**（稳且不依赖 wrangler 鉴权）：

```bash
source ~/.config/cloudflare/env.sh 2>/dev/null  # 加载 CLOUDFLARE_API_TOKEN
ACCOUNT_ID="${R2_ACCOUNT_ID:-}"  # 可选
ENCODED_KEY=$(python3 -c "import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1], safe='/'))" "$R2_PATH")
MIME=$(file --mime-type -b "<file-path>")

curl -fsS -X PUT \
  "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/r2/buckets/$R2_BUCKET/objects/$ENCODED_KEY" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: $MIME" \
  --data-binary "@<file-path>"
```

**REST API 返回非 0 退出码时**，自动回退到 wrangler CLI：

```bash
wrangler r2 object put "$R2_BUCKET/$R2_PATH" --file "<file-path>" --remote 2>&1
```

> ⚠️ wrangler `--remote` 在 Account API Token 模式下可能报 `Authentication failed (status: 400) [code: 9106]`；若报错，先用 REST API 重传一次（不要带 `--remote`，那是写入本地 MinIO）。

## Step 4: 返回 URL

```bash
# 有自定义域名
echo "https://$R2_DOMAIN/$R2_PATH"

# 无自定义域名
echo "https://pub-<account-id>.r2.dev/$R2_PATH"
```

## 从 URL 直接上传

```bash
TMP="/tmp/r2-upload-$(date +%s)"
curl -fsSL "<url>" -o "$TMP"
ACCOUNT_ID="${R2_ACCOUNT_ID:-}"
ENCODED_KEY=$(python3 -c "import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1], safe='/'))" "$R2_PATH")
MIME=$(file --mime-type -b "$TMP")

curl -fsS -X PUT \
  "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/r2/buckets/$R2_BUCKET/objects/$ENCODED_KEY" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: $MIME" \
  --data-binary "@$TMP"
rm "$TMP"
```

## 管理命令

```bash
# 删除对象
ENCODED_KEY=$(python3 -c "import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1], safe='/'))" "<path>")
curl -fsS -X DELETE \
  "https://api.cloudflare.com/client/v4/accounts/$R2_ACCOUNT_ID/r2/buckets/$R2_BUCKET/objects/$ENCODED_KEY" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN"

# 列出 buckets（wrangler 即可）
wrangler r2 bucket list
```

## 高级功能

批量上传、并发上传、错误处理详见 [references/advanced.md](references/advanced.md)。

## 验证

- [ ] 文件已上传到 R2（REST API 返回 `{"success": true}`）
- [ ] 返回的 URL 可公开访问（HTTP 200 + `Content-Type: image/png|jpeg|...`）
- [ ] CF 缓存命中后仍能拿到新内容（必要时手动 `curl -X DELETE` 删除缓存）

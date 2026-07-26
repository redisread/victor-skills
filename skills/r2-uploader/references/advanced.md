# 高级用法

## 目录

- [批量上传](#批量上传)
- [并发上传](#并发上传)
- [REST API 单文件模板](#rest-api-单文件模板)

---

## 批量上传

### 上传当前目录所有图片（REST API）

```bash
source ~/.config/cloudflare/env.sh 2>/dev/null
ACCOUNT_ID="${R2_ACCOUNT_ID:-}"

for file in *.jpg *.png *.gif *.webp; do
  [ -f "$file" ] || continue
  R2_PATH="agent/$(date +%Y%m%d)/$file"
  ENCODED_KEY=$(python3 -c "import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1], safe='/'))" "$R2_PATH")
  MIME=$(file --mime-type -b "$file")
  curl -fsS -X PUT \
    "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/r2/buckets/$R2_BUCKET/objects/$ENCODED_KEY" \
    -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
    -H "Content-Type: $MIME" \
    --data-binary "@$file" && echo "✓ $file"
done
```

### 上传指定目录所有文件（REST API）

```bash
DIR="/path/to/dir"
for file in "$DIR"/*; do
  [ -f "$file" ] || continue
  R2_PATH="agent/$(date +%Y%m%d)/$(basename "$file")"
  ENCODED_KEY=$(python3 -c "import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1], safe='/'))" "$R2_PATH")
  MIME=$(file --mime-type -b "$file")
  curl -fsS -X PUT \
    "https://api.cloudflare.com/client/v4/accounts/$R2_ACCOUNT_ID/r2/buckets/$R2_BUCKET/objects/$ENCODED_KEY" \
    -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
    -H "Content-Type: $MIME" \
    --data-binary "@$file" && echo "✓ $(basename "$file")"
done
```

---

## 并发上传

REST API 是 HTTP 调用，可并发：

```bash
find . -name "*.jpg" -print0 | xargs -0 -P 4 -I FILE bash -c '
  source ~/.config/cloudflare/env.sh 2>/dev/null
  R2_PATH="agent/$(date +%Y%m%d)/$(basename FILE)"
  ENCODED_KEY=$(python3 -c "import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1], safe=\"/\"))" "$R2_PATH")
  MIME=$(file --mime-type -b FILE)
  curl -fsS -X PUT \
    "https://api.cloudflare.com/client/v4/accounts/${R2_ACCOUNT_ID}/r2/buckets/$R2_BUCKET/objects/$ENCODED_KEY" \
    -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
    -H "Content-Type: $MIME" \
    --data-binary "@FILE"
'
```

参数说明：
- `-P 4`: 同时 4 个并发上传
- `-print0` / `-0`: 正确处理含空格的文件名
- `bash -c`: 让 `FILE` 在子 shell 中展开

---

## REST API 单文件模板

如果不想用 skill 里的 `Step 3`，可直接复制：

```bash
source ~/.config/cloudflare/env.sh 2>/dev/null

upload_to_r2() {
  local file="$1"
  local key="$2"  # 例: posts/life/20260726/cover.png
  local bucket="${R2_BUCKET:?R2_BUCKET not set}"
  local account="${R2_ACCOUNT_ID:?R2_ACCOUNT_ID not set}"
  local token="${CLOUDFLARE_API_TOKEN:?CLOUDFLARE_API_TOKEN not set}"
  local mime=$(file --mime-type -b "$file")
  local encoded=$(python3 -c "import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1], safe='/'))" "$key")

  curl -fsS -X PUT \
    "https://api.cloudflare.com/client/v4/accounts/$account/r2/buckets/$bucket/objects/$encoded" \
    -H "Authorization: Bearer $token" \
    -H "Content-Type: $mime" \
    --data-binary "@$file"
}

# 用法
upload_to_r2 "/path/to/local.png" "posts/life/$(date +%Y%m%d)/local.png"
```
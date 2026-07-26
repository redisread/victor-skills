# 错误处理指南

## 目录

- [诊断流程](#诊断流程)
- [错误码对照表](#错误码对照表)
- [REST API 重试机制](#rest-api-重试机制)
- [wrangler 兜底重试机制](#wrangler-兜底重试机制)
- [特殊路径处理](#特殊路径处理)
- [Cloudflare 缓存陷阱](#cloudflare-缓存陷阱)

---

## 诊断流程

上传失败时按顺序排查：

```bash
# 1. REST API 凭证
source ~/.config/cloudflare/env.sh && echo "TOKEN: ${CLOUDFLARE_API_TOKEN:0:10}..."
test -n "$R2_ACCOUNT_ID" && echo "ACCOUNT: $R2_ACCOUNT_ID"

# 2. wrangler 登录状态
wrangler whoami

# 3. bucket 存在
wrangler r2 bucket list | grep "<bucket>"

# 4. 文件可读
ls -la "<file-path>"
```

---

## 错误码对照表

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `401 Unauthorized` (REST API) | `CLOUDFLARE_API_TOKEN` 缺失或无 R2 写权限 | `source ~/.config/cloudflare/env.sh`；到 Cloudflare 控制台给 token 加 `Account / R2 / Edit` 权限 |
| `400 Bad Request` (REST API) | 路径未编码、Content-Type 错误 | `urllib.parse.quote(key, safe='/')`；用 `file --mime-type -b` 取实际 MIME |
| `Authentication failed (status: 400) [code: 9106]` (wrangler) | Account API Token 模式下 `wrangler r2 object put --remote` 不通过 | **不要带 `--remote`**（会写到本地 MinIO）或直接走 REST API |
| `The file does not exist` | 路径错误或空格问题 | `find` 查找正确路径 → 改用临时文件上传 |
| `Bucket not found` | bucket 不存在 | `wrangler r2 bucket create <name>` |
| `Network error` / `Timeout` | 网络问题 | 检查网络 → 启用重试机制 |
| `Permission denied` | 文件权限不足 | `chmod +r "<file>"` |

---

## REST API 重试机制

```bash
# 最多重试 3 次，每次间隔 2 秒
source ~/.config/cloudflare/env.sh 2>/dev/null
for i in 1 2 3; do
  ENCODED_KEY=$(python3 -c "import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1], safe='/'))" "$R2_PATH")
  MIME=$(file --mime-type -b "<file>")
  RESP=$(curl -fsS -X PUT \
    "https://api.cloudflare.com/client/v4/accounts/$R2_ACCOUNT_ID/r2/buckets/$R2_BUCKET/objects/$ENCODED_KEY" \
    -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
    -H "Content-Type: $MIME" \
    --data-binary "@<file>" 2>&1) && \
    { echo "✓ 上传成功"; break; }
  echo "⚠ 第 $i 次失败，2秒后重试..."
  sleep 2
done
```

---

## wrangler 兜底重试机制

REST API 都失败时回退（注意 `--remote` 9106 问题）：

```bash
for i in 1 2 3; do
  wrangler r2 object put "$R2_BUCKET/$R2_PATH" --file "<file>" --remote 2>&1 && \
    { echo "✓ 上传成功"; break; }
  echo "⚠ 第 $i 次失败，2秒后重试..."
  sleep 2
done
```

---

## 特殊路径处理

含空格或中文的路径在 REST API 写入前需编码（`urllib.parse.quote(..., safe='/'）`），skill 里的命令已处理。wrangler CLI 下用临时文件绕过：

```bash
TMP_FILE="/tmp/r2-upload-$(date +%s)"
cp "<source-path>" "$TMP_FILE"
wrangler r2 object put "$R2_BUCKET/$R2_PATH" --file "$TMP_FILE" --remote
rm "$TMP_FILE"
```

---

## Cloudflare 缓存陷阱

上传成功后 `https://cos.jiahongw.com/<key>` 可能仍返回旧的 404 或 27150 字节 HTML（缓存的 404 页面）。

诊断：

```bash
curl -sI "https://cos.jiahongw.com/<key>" 2>&1 | grep -iE "cf-cache-status|age"
# HIT + age > 0 → 缓存命中
```

解决（手动失效缓存）：

```bash
ENCODED_KEY=$(python3 -c "import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1], safe='/'))" "<key>")
curl -fsS -X DELETE \
  "https://api.cloudflare.com/client/v4/accounts/$R2_ACCOUNT_ID/r2/buckets/$R2_BUCKET/objects/$ENCODED_KEY" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN"
# 然后重新 PUT 一次（Cloudflare 边缘缓存会在下次访问时重新拉 R2）
```

#!/usr/bin/env bash
# Fetch all recent posts from a subreddit using opencli reddit
# Usage: fetch_posts.sh <subreddit> <output_dir> [limit]
set -euo pipefail

SUBREDDIT="${1:?Usage: fetch_posts.sh <subreddit> <output_dir> [limit]}"
OUTPUT_DIR="${2:?output_dir required}"
LIMIT="${3:-100}"
OPENCLI="${OPENCLI:-$HOME/.npm-global/bin/opencli}"

mkdir -p "$OUTPUT_DIR"

echo "📥 Fetching up to $LIMIT recent posts from r/$SUBREDDIT..."

# Fetch subreddit posts (new sort, JSON format)
$OPENCLI reddit subreddit "$SUBREDDIT" --sort new --limit "$LIMIT" -f json > "$OUTPUT_DIR/posts_list.json" 2>/dev/null

# Count posts
POST_COUNT=$(python3 -c "import json; data=json.load(open('$OUTPUT_DIR/posts_list.json')); print(len(data))" 2>/dev/null || echo "0")
echo "📋 Got $POST_COUNT posts"

# Fetch details for each post
IDX=0
while IFS=$'\t' read -r title author upvotes comments url post_id created_utc; do
  if [ -z "$post_id" ] || [ "$post_id" = "null" ]; then
    # Extract post ID from URL
    post_id=$(echo "$url" | grep -oP 'comments/\K[a-z0-9]+' || echo "")
  fi
  if [ -z "$post_id" ]; then
    echo "⚠️  Skipping post with no ID: $title"
    continue
  fi
  
  IDX=$((IDX + 1))
  echo "📖 [$IDX/$POST_COUNT] Fetching: $title"
  
  # Fetch post details and comments
  $OPENCLI reddit read "$post_id" --sort top --limit 20 --depth 2 --max-length 2000 -f json > "$OUTPUT_DIR/post_${post_id}.json" 2>/dev/null || echo "{}" > "$OUTPUT_DIR/post_${post_id}.json"
  
  sleep 1
done < <(python3 -c "
import json, sys
data = json.load(open('$OUTPUT_DIR/posts_list.json'))
for p in data:
    pid = p.get('id', '') or p.get('post_id', '') or ''
    title = p.get('title', '')
    author = p.get('author', '') or p.get('username', '') or ''
    upvotes = str(p.get('upvotes', p.get('score', 0)))
    comments = str(p.get('comments', p.get('num_comments', 0)))
    url = p.get('url', p.get('permalink', ''))
    created = str(p.get('created_utc', p.get('created', '')))
    print(f'{title}\t{author}\t{upvotes}\t{comments}\t{url}\t{pid}\t{created}')
" 2>/dev/null)

echo "✅ Fetched $IDX posts to $OUTPUT_DIR"
echo "$OUTPUT_DIR"

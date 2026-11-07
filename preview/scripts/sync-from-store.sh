#!/usr/bin/env bash
# Copy manuscript from the Project store into this repo, then rebuild the TOC manifest.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
STORE="${BOOK_STORE:-/cursor/stores/self/book}"

mkdir -p "$ROOT/preview/chapters" "$ROOT/book/chapters" "$ROOT/book/outline"
cp -f "$STORE"/chapters/ch-*.md "$ROOT/preview/chapters/"
cp -f "$STORE"/chapters/ch-*.md "$ROOT/book/chapters/"
cp -f "$STORE"/outline/00-complete-outline.md "$ROOT/preview/chapters/"
cp -f "$STORE"/outline/00-complete-outline.md "$ROOT/book/outline/"
node "$ROOT/preview/scripts/build-manifest.mjs"
echo "Synced chapters from $STORE"

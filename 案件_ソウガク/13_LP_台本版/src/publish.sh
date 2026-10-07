#!/usr/bin/env bash
# ソウガクLPの公開（ビルド → 公開前チェック → 公開ブランチへ反映 → 実サイトで一致を確認）
#   bash src/publish.sh "コミットメッセージ"
# 実サイト https://online-tutor.navolio.net/ は公開ブランチ codex/online-tutor-pages から表示される。
# 開発ブランチへ push しただけではサイトに出ないので、公開するときは必ずこれを使う。
set -euo pipefail

MSG="${1:?コミットメッセージを指定してください}"
BRANCH=codex/online-tutor-pages
SITE=https://online-tutor.navolio.net
SRC="$(cd "$(dirname "$0")" && pwd)"
LP="$(dirname "$SRC")"
REPO="$(git -C "$LP" rev-parse --show-toplevel)"

echo "== 1. ビルド"
(cd "$SRC" && python3 build_pages.py && rm -rf __pycache__)

echo "== 2. 公開前チェック"
NODE_PATH="${NODE_PATH:-$(npm root -g)}" node "$SRC/check_pages.cjs"

echo "== 3. 公開ブランチへ反映"
WT="$(mktemp -d)"
trap 'git -C "$REPO" worktree remove --force "$WT" >/dev/null 2>&1 || true' EXIT
git -C "$REPO" fetch -q origin "$BRANCH"
git -C "$REPO" worktree add -q --detach "$WT" "origin/$BRANCH"
PAGES=(index.html $(cd "$LP" && ls -d lp*/index.html))
for f in "${PAGES[@]}" style.css parts.css disclosure.html operator.html privacy.html; do
  mkdir -p "$WT/$(dirname "$f")"
  cp "$LP/$f" "$WT/$f"
done
cp -r "$LP/images/." "$WT/images/"
git -C "$WT" add -A
if git -C "$WT" diff --cached --quiet; then
  echo "公開ブランチに変更なし"
else
  git -C "$WT" commit -q -m "$MSG"
  git -C "$WT" push -q origin "HEAD:$BRANCH"
  git -C "$WT" log --oneline -1
fi

echo "== 4. 実サイトで一致を確認（最大4分）"
for i in $(seq 1 24); do
  ok=1
  for f in "${PAGES[@]}"; do
    a=$(curl -s "$SITE/$f?t=$RANDOM$i" | md5sum | cut -c1-32)
    b=$(md5sum < "$LP/$f" | cut -c1-32)
    [ "$a" = "$b" ] || ok=0
  done
  if [ $ok = 1 ]; then echo "実サイト反映OK（${PAGES[*]}）"; exit 0; fi
  sleep 10
done
echo "実サイトがまだ古いままです。GitHub Pages のデプロイ状況を確認してください。" >&2
exit 1

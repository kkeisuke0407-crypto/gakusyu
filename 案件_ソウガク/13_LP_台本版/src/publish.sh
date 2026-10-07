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

# 生成済みページが元データと食い違ったまま開発ブランチに残らないよう、変わっていればコミットして push する
GEN=$(cd "$LP" && ls index.html lp*/index.html)
if [ -n "$(cd "$LP" && git status --porcelain -- $GEN)" ]; then
  (cd "$LP" && git add -- $GEN && git commit -q -m "生成済みページを元データから再生成" && git push -q origin HEAD && git log --oneline -1)
fi

echo "== 2. 公開前チェック"
NODE_PATH="${NODE_PATH:-$(npm root -g)}" node "$SRC/check_pages.cjs"

echo "== 3. 公開ブランチへ反映"
WT="$(mktemp -d)"
trap 'git -C "$REPO" worktree remove --force "$WT" >/dev/null 2>&1 || true' EXIT
git -C "$REPO" fetch -q origin "$BRANCH"
git -C "$REPO" worktree add -q --detach "$WT" "origin/$BRANCH"
PAGES=(index.html $(cd "$LP" && ls -d lp*/index.html))
# 公開するのは、ページと法務ページから実際に参照されている CSS・画像だけ（publish_files.py が一覧を出す）。
# それ以外（旧ページの残り・使わなくなった画像・メモ・JSON）は公開ブランチから消す。CNAME だけは残す。
FILES="$(python3 "$SRC/publish_files.py")"
git -C "$WT" ls-files -z | grep -zv '^CNAME$' | xargs -0 -r git -C "$WT" rm -q --
while IFS= read -r f; do mkdir -p "$WT/$(dirname "$f")"; cp "$LP/$f" "$WT/$f"; done <<< "$FILES"
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

"""公開するファイルの一覧を出す（publish.sh から呼ぶ）。
ページ（index.html・lp*/index.html）と法務ページから、実際に参照されている
CSS・画像・HTML をたどって集める。参照されていないファイルは公開しない。
参照先がローカルに無ければ終了コード1。
  python3 publish_files.py  → 13_LP_台本版/ からの相対パスを1行ずつ出力
"""
import os
import re
import sys

LP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START = ["index.html", "disclosure.html", "operator.html", "privacy.html"] + sorted(
    d + "/index.html" for d in os.listdir(LP) if re.fullmatch(r"lp\d+", d))
# 引用符・url() の中にある、ローカルのファイルへの参照（http・data: は対象外）
REF = re.compile(r"""(?:["'(]|,\s*)([^"'()\s,]+?\.(?:webp|png|jpe?g|svg|gif|ico|css|html|js))(?=[?#"')\s,])""")

seen, missing, todo = set(), [], [p for p in START if os.path.exists(os.path.join(LP, p))]
while todo:
    f = todo.pop()
    if f in seen:
        continue
    seen.add(f)
    if not f.endswith((".html", ".css")):
        continue
    text = open(os.path.join(LP, f), encoding="utf-8").read()
    for ref in REF.findall(text):
        if re.match(r"(?:[a-z]+:|//|#)", ref):
            continue
        p = os.path.normpath(os.path.join(os.path.dirname(f), ref)).replace(os.sep, "/")
        if p.startswith(".."):
            continue
        if os.path.isfile(os.path.join(LP, p)):
            todo.append(p)
        else:
            missing.append(f"{f} → {ref}")

if missing:
    print("参照先のファイルがありません:\n  " + "\n  ".join(sorted(set(missing))), file=sys.stderr)
    sys.exit(1)
print("\n".join(sorted(seen)))

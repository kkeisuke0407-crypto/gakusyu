# -*- coding: utf-8 -*-
"""LP02 v2 検証スクリプト。

v2以降は index.html を正本とする。
旧v1の「説明記事を生成して体験談ブロックを後付けする」生成処理は廃止。
このスクリプトは、LP02が体験談駆動の構造を保っているかを検証する。

Usage:
    python3 build_lp02.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
html = (HERE / "index.html").read_text(encoding="utf-8")

checks = {
    "FV CTA -> #sogaku": 'href="#sogaku"' in html,
    "sogaku anchor": 'id="sogaku"' in html,
    "trial anchor": 'id="trial"' in html,
    "mt-talk": html.count('class="mt-talk"') >= 1,
    "mt-story >= 4": html.count('class="mt-story"') >= 4,
    "mt-review >= 4": html.count('class="mt-review"') >= 4,
    "mt-voice": html.count('class="mt-voice"') >= 1,
    "mt-spec": html.count('class="mt-spec"') >= 1,
    "no mt-imgslot": "mt-imgslot" not in html,
    "no competitor names": not any(x in html for x in [
        "家庭教師のランナー", "家庭教師のトライ", "家庭教師のサクシード",
        "キズキ", "メガスタ"
    ]),
    "no 300x250 felmat banner": "t.felmat.net/fmimg" not in html,
    "felmat CTA": "https://t.felmat.net/fmcl?ak=C12158L.1.I1680104.D1416296" in html,
    "sticky starts after sogaku CTA": "document.querySelector('#cta-sogaku')" in html,
    "noindex": '<meta name="robots" content="noindex, nofollow">' in html,
}

failed = [name for name, ok in checks.items() if not ok]
for name, ok in checks.items():
    print(("OK  " if ok else "NG  ") + name)

if failed:
    raise SystemExit("FAILED: " + ", ".join(failed))

print("LP02 v2 validation: OK")

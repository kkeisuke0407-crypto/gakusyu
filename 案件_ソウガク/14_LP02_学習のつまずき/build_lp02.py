# -*- coding: utf-8 -*-
"""LP02 current structure validator.

index.html is the source of truth.
This script does not regenerate the page.

Usage:
    python3 build_lp02.py                 # 構成・パーツのルールを確認
    python3 build_lp02.py <LP01 index>    # ＋ 下半分（無料体験〜追従ボタン）がLP01と1文字も違わないか確認
"""
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
html = (HERE / "index.html").read_text(encoding="utf-8")

service_pos = html.find('id="service"')
assert service_pos > 0, "service anchor missing"

pre = html[:service_pos]
post = html[service_pos:]

# HTML comments may contain the word ソウガク, so strip comments before visible-copy checks.
pre_visible = re.sub(r'<!--.*?-->', '', pre, flags=re.S)

checks = {
    "FV anonymous CTA": 'href="#service"' in pre_visible,
    "no Sogaku name before reveal": "ソウガク" not in pre_visible,
    "need answer: homework/concentration": "宿題が進まないなら" in pre_visible,
    "need answer: subject-specific": "漢字・算数で止まるなら" in pre_visible,
    "need answer: parent role": "親が先生役を続けなくてもいい" in pre_visible,
    "need answer: school difficulty": "学校に行きづらい時期" in pre_visible,
    "reveal Sogaku after service anchor": "ソウガク" in post,
    "3 proof stories after reveal": post.count('class="mt-story"') >= 4,
    "assessment only explanatory": html.count("アセスメント") <= 1,
    "no image placeholders": "mt-imgslot" not in html,
    "no competitors": not any(x in html for x in ["ランナー","家庭教師のトライ","サクシード","キズキ","メガスタ"]),
    "felmat CTA": "https://t.felmat.net/fmcl?ak=C12158L.1.I1680104.D1416296" in html,
    "sticky after first Sogaku CTA": "document.querySelector('#cta-sogaku')" in html,
    "noindex": '<meta name="robots" content="noindex, nofollow">' in html,
}

# hozon「体験談ランキング型LP パーツ集」のルール
talk = re.search(r'<div class="mt-talk">(.*?)\n  </div>', html, re.S).group(1)
rows = talk.count('class="mt-talk__row')
spec = html[html.index('class="mt-spec"'):]
spec = spec[:spec.index('\n  </div>')]
no_sticky = re.sub(r'<div class="mt-sticky">.*?</div></div>', '', html, flags=re.S)
checks.update({
    "parts: mt-talk 4-6 bubbles, image icons": 4 <= rows <= 6 and talk.count('mt-talk__icon"><img') == rows,
    "parts: mt-summary only once (top)": html.count('class="mt-summary"') == 1,
    "parts: no mt-conclusion (no comparison table)": "mt-conclusion" not in html,
    "parts: every mt-check has a foot line": html.count('class="mt-check"') == html.count('mt-check__foot'),
    "parts: every big button has ＼ひとこと／": all('mt-cta__micro' in c for c in re.findall(r'<div class="mt-cta"[^>]*>.*?</div>', no_sticky, re.S)),
    "parts: mt-oneline is one line (no <br>)": not re.search(r'class="mt-oneline"><span>[^<]*<br>', html),
    "parts: mt-bridge once, ＼name／": html.count('class="mt-bridge"') == 1 and "＼<span>ソウガク</span>／" in html,
    "parts: #cta-sogaku inside mt-spec": 'id="cta-sogaku"' in spec,
    "all ASP links are the same felmat URL": set(re.findall(r'href="(https://t\.felmat[^"]+)"', html)) == {"https://t.felmat.net/fmcl?ak=C12158L.1.I1680104.D1416296&amp;pb="},
    "no 300x250 felmat banner": "t.felmat.net/fmimg" not in html,
})

# 下半分がLP01と同じか（LP01 = branch claude/amazing-thompson-2rqmiv の 案件_ソウガク/13_LP_台本版/index.html）
if len(sys.argv) > 1:
    L = Path(sys.argv[1]).read_text(encoding="utf-8").split("\n")
    for a, b in [(263, 297), (299, 326), (328, 338), (340, 358), (360, 374), (376, 382), (385, 385), (387, 391)]:
        checks[f"LP01 lines {a}-{b} unchanged"] = "\n".join(L[a - 1:b]) in html

for name, ok in checks.items():
    print(("OK  " if ok else "NG  ") + name)

failed = [name for name, ok in checks.items() if not ok]
if failed:
    raise SystemExit("FAILED: " + ", ".join(failed))

print("LP02 structure validation: OK")

# -*- coding: utf-8 -*-
"""LP02 current structure validator.

index.html is the source of truth.
This script does not regenerate the page.
"""
from pathlib import Path
import re

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

for name, ok in checks.items():
    print(("OK  " if ok else "NG  ") + name)

failed = [name for name, ok in checks.items() if not ok]
if failed:
    raise SystemExit("FAILED: " + ", ".join(failed))

print("LP02 structure validation: OK")

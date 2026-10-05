# -*- coding: utf-8 -*-
"""LP02 current structure validator.

index.html is the source of truth.
This script does not regenerate the page.

構成：FVの会話 → 検索ニーズに2セクションで答える → 家だけでは行き詰まる4つ（ボタンなし）
      → #service（mt-bridge）で初めてソウガクを発表 → ここから下はLP01（王道LP）の
      第1位ソウガク〜体験談〜無料体験〜最後をそのまま（第2位・第3位・比較表・ランキングなし）

Usage:
    python3 build_lp02.py                 # 構成・パーツのルールを確認
    python3 build_lp02.py <LP01 index>    # ＋ #service より下がLP01と1文字も違わないか確認
                                          #   LP01 = branch claude/amazing-thompson-2rqmiv の 案件_ソウガク/13_LP_台本版/index.html
"""
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
html = (HERE / "index.html").read_text(encoding="utf-8")
visible = lambda s: re.sub(r'<!--.*?-->|<script.*?</script>', '', s, flags=re.S)

service_pos = html.find('id="service"')
assert service_pos > 0, "service anchor missing"
pre, post = html[:service_pos], html[service_pos:]
pre_visible = visible(pre)
FELMAT = "https://t.felmat.net/fmcl?ak=C12158L.1.I1680104.D1416296&amp;pb="

talk = re.search(r'<div class="mt-talk">(.*?)\n  </div>', pre, re.S).group(1)
rows = talk.count('class="mt-talk__row')
after_talk = pre[pre.index(talk) + len(talk):]
bridge_part = pre[pre.rindex('class="mt-h2"'):]
no_sticky = re.sub(r'<div class="mt-sticky">.*?</div></div>', '', html, flags=re.S)

checks = {
    # 構成
    "FV: mt-talk directly under the eyecatch": re.search(r'01_fv_evening-desk\.webp[^\n]*\n\n  <div class="mt-talk">', pre) is not None,
    "FV: 'see the service first' button right after the talk": re.match(r'\s*<p class="mt-small">[^\n]*</p>\n\n  <div class="mt-cta"><p class="mt-cta__micro">＼先にサービスを見たい方はこちら／</p><a class="mt-cta__btn" href="#service">', after_talk.split('</div>', 1)[1]) is not None,
    "no Sogaku name before reveal": "ソウガク" not in pre_visible,
    "need answers: exactly 2 H2 sections before reveal": pre.count('class="mt-h2"') == 2,
    "bridge: 4 pains (mt-check) and no button before reveal": bridge_part.count('<li>') >= 4 and 'mt-check' in bridge_part
    and 'class="mt-cta"' not in bridge_part[bridge_part.index('class="mt-check"'):],
    "reveal: mt-bridge ＼ソウガク／ once": html.count('class="mt-bridge"') == 1 and "＼<span>ソウガク</span>／" in html,
    "no ranking / competitors (visible)": not any(x in visible(html) for x in ["第1位", "第2位", "第3位", "ランナー", "トライ", "サクシード", "キズキ", "メガスタ", "3選"]),
    "no image placeholders": "mt-imgslot" not in html,
    "all ASP links are the same felmat URL": set(re.findall(r'href="(https://t\.felmat[^"]+)"', html)) == {FELMAT},
    "sticky after the first Sogaku button (#cta-rank1)": "document.querySelector('#cta-rank1')" in html and 'id="cta-rank1"' in post,
    "noindex": '<meta name="robots" content="noindex, nofollow">' in html,
    # hozon「体験談ランキング型LP パーツ集」のルール（新しく書いた部分）
    "parts: mt-talk 4-6 bubbles, image icons": 4 <= rows <= 6 and talk.count('mt-talk__icon"><img') == rows,
    "parts: every mt-check has a foot line": html.count('class="mt-check"') == html.count('mt-check__foot'),
    "parts: every big button has ＼ひとこと／": all('mt-cta__micro' in c for c in re.findall(r'<div class="mt-cta"[^>]*>.*?</div>', no_sticky, re.S)),
    "parts: mt-oneline is one line (no <br>)": not re.search(r'class="mt-oneline"><span>[^<]*<br>', html),
    "parts: no mt-conclusion (no comparison table)": "mt-conclusion" not in html,
    "parts: every H2 before reveal has a door image": all(re.match(r'[^\n]*\n  <figure class="mt-img"', pre[m.end():]) for m in re.finditer(r'<h2 class="mt-h2"', pre)),
}

# #service より下がLP01と同じか
if len(sys.argv) > 1:
    L = Path(sys.argv[1]).read_text(encoding="utf-8").split("\n")
    a = next(i for i, l in enumerate(L) if '広告主バナー（felmat 発行コードのまま' in l)
    b = next(i for i, l in enumerate(L) if 'ソウガクの無料体験を詳しく見る' in l)
    c = next(i for i, l in enumerate(L) if '12〜15 体験談パート' in l)
    checks["LP01 第1位ソウガク block unchanged"] = "\n".join(L[a:b + 1]) in post
    checks["LP01 体験談〜最後 unchanged"] = html.endswith("\n".join(L[c:]))

for name, ok in checks.items():
    print(("OK  " if ok else "NG  ") + name)

failed = [name for name, ok in checks.items() if not ok]
if failed:
    raise SystemExit("FAILED: " + ", ".join(failed))

print("LP02 structure validation: OK")

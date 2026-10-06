"""ソウガクLPの組み立て（王道LP＝index.html、LP02＝lp02/index.html）

比較表から下は王道LPと共通の部品（parts/common_*.html）をそのまま使う。
王道LP側を直すときは parts/ の共通部品を直して、このスクリプトを実行すれば両方に反映される。
  python3 build_pages.py
"""
import os, re
from build import render

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # 13_LP_台本版
P = lambda name: open(os.path.join(HERE, "parts", name), encoding="utf-8").read()

PAGES = {
    # 王道LP：FV → 比較表 → 3つのポイント → ランキング以降
    "index.html": dict(
        title="【2026年】発達障害・グレーゾーンの子向けオンライン家庭教師ランキングTOP3｜3社を比較",
        desc="発達障害・グレーゾーンの子に対応したオンライン家庭教師3社（ソウガク・ティントル・家庭教師のコーチング1）を、先生・授業時間・料金・保護者サポート・無料体験で比較。各社の料金と無料体験もまとめました。",
        parts=["lp01_top.html", "lp01_compare_h2.html", "common_compare.html", "lp01_points.html", "common_after.html"],
        prefix="", lp02_only=False),
    # LP02：家庭教師→オンライン家庭教師 導線（台本 LP02_台本_v1＝v2）。比較表より上だけ独自、「3つのポイント」は除外
    "lp02/index.html": dict(
        title="発達特性のあるお子さまの家庭教師は「1対1」だけで選ばない｜訪問型とオンラインを比較",
        desc="発達障害・グレーゾーンのお子さまの家庭教師選び。特性を理解してくれる先生の見分け方、訪問型とオンラインの違い、オンライン家庭教師の選び方を整理し、サービスを比較しました。",
        parts=["lp02_top.html", "lp02_compare_h2.html", "common_compare.html", "common_after.html"],
        prefix="../", lp02_only=True),
}

def lp02_only(t, keep):
    """共通部品の中の <!--LP02-ONLY-->〜<!--/LP02-ONLY--> は LP02 にだけ出す（王道LPは変えない）"""
    pat = r"[ \t]*<!--LP02-ONLY-->\n(.*?)[ \t]*<!--/LP02-ONLY-->\n"
    return re.sub(pat, (lambda m: m.group(1)) if keep else "", t, flags=re.S)

def add_prefix(t, prefix):
    """サブフォルダのページ用に、相対パス（画像・CSS・運営者ページなど）の頭に ../ を付ける"""
    if not prefix:
        return t
    def fix(m):
        attr, q, url = m.group(1), m.group(2), m.group(3)
        if re.match(r"^(https?:|#|/|mailto:|tel:|data:|\.\./)", url):
            return m.group(0)
        return f"{attr}={q}{prefix}{url}"
    return re.sub(r'\b(src|href|srcset)=(["\'])([^"\']+)', fix, t)

for out, d in PAGES.items():
    head = P("head.html").replace("{{TITLE}}", d["title"]).replace("{{DESC}}", d["desc"])
    t = render(head + "".join(P(x) for x in d["parts"]))
    t = lp02_only(t, d["lp02_only"])
    t = add_prefix(t, d["prefix"])
    path = os.path.join(ROOT, out)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(t)
    print("wrote", out, len(t))

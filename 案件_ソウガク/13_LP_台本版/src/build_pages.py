"""ソウガクLPの組み立て（王道LP＝index.html、サブLP＝lp02/・lp03/ …）

比較表から下は王道LPと共通の部品（parts/common_*.html）をそのまま使う。
王道LP側を直すときは parts/ の共通部品を直して、このスクリプトを実行すれば全ページに反映される。
共通部品の中の出し分け：<!--OUDOU-ONLY-->〜 は王道LPだけ、<!--SUB-ONLY-->〜 はサブLP（sub=True）だけに出す。
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
        desc="発達障害・グレーゾーンの子に対応したオンライン家庭教師3社（ソウガク・ティントル・家庭教師のコーチング1）を、発達特性への対応・先生・授業時間・料金・保護者サポート・無料体験の6項目で比較。各社の料金と無料体験もまとめました。",
        parts=["lp01_top.html", "common_compare.html", "lp01_points.html", "common_after.html"],
        prefix="", sub=False),
    # LP02：家庭教師→オンライン家庭教師 導線（台本 LP02_台本_v1＝v2）。比較表より上だけ独自、「3つのポイント」は除外
    "lp02/index.html": dict(
        title="発達特性のあるお子さまの家庭教師は「1対1」だけで選ばない｜訪問型とオンラインを比較",
        desc="発達障害・グレーゾーンのお子さまの家庭教師選び。特性を理解してくれる先生の見分け方、訪問型とオンラインの違いを整理し、オンライン家庭教師3社を比較しました。",
        parts=["lp02_top.html", "common_compare.html", "common_after.html"],
        prefix="../", sub=True),
    # LP03：勉強法・宿題 → 個別支援 導線（台本 LP03_台本_v1）。比較表より上だけ独自、「3つのポイント」は除外
    "lp03/index.html": dict(
        title="「勉強しない」を「やる気」だけで片づけない｜発達特性のある子の勉強・宿題が進まないとき",
        desc="発達障害・グレーゾーンの子が勉強しない、宿題が進まないときに。やる気だけの問題と考えず、どこで止まっているかを整理し、家庭教師の選び方まで紹介します。オンライン家庭教師3社の比較もまとめました。",
        parts=["lp03_top.html", "common_compare.html", "common_after.html"],
        prefix="../", sub=True),
    # LP04：教科・読み書き/LD → 個別支援 導線（台本 LP04_台本_v1）。比較の見出しより上だけ独自、「3つのポイント」は除外
    "lp04/index.html": dict(
        title="苦手な教科は「練習不足」だけで片づけない｜発達特性のある子の読み書き・算数・英語のつまずき",
        desc="発達障害・グレーゾーンのお子さんの漢字・読み書き・算数・英語が苦手なとき、読む・書く・覚える・考えるのどこで止まっているかで最初に変えることが変わります。家庭での工夫と、苦手な教科を見てもらうときの選び方、オンライン家庭教師の比較をまとめました。",
        parts=["lp04_top.html", "common_compare.html", "common_after.html"],
        prefix="../", sub=True),
    # LP05：塾・個別指導 → オンライン家庭教師 導線（台本 LP05_台本_v1）。比較の見出しより上だけ独自、「3つのポイント」は除外
    "lp05/index.html": dict(
        title="発達特性のある子の塾は「個別指導」だけで選ばない｜塾選びで確認したい4つと、オンライン家庭教師との違い",
        desc="発達障害・グレーゾーンのお子さんの塾選び。個別指導といっても人数や進め方は教室ごとに違います。塾を選ぶ前に確認したい4つ、集団塾・個別指導塾・オンライン家庭教師の違い、オンライン家庭教師3社の比較をまとめました。",
        parts=["lp05_top.html", "common_compare.html", "common_after.html"],
        prefix="../", sub=True),
    # LP06：通信教育・教材 → 個別支援 導線（台本 LP06_台本_v1）。比較の見出しより上だけ独自、「3つのポイント」は除外
    "lp06/index.html": dict(
        title="通信教育は「教材の良さ」だけで選ばない｜発達特性のある子の通信教育の選び方と向き・不向き",
        desc="発達障害・グレーゾーンのお子さんの通信教育選び。教材の内容だけでなく、始められるか・分からないときに進めるか・続けられるか・親がつきっきりにならないかを見て選びます。通信教育が合いやすい子、人に見てもらう方が進めやすい子と、オンライン家庭教師3社の比較をまとめました。",
        parts=["lp06_top.html", "common_compare.html", "common_after.html"],
        prefix="../", sub=True),
    # LP07：受験 × 家庭教師 → オンライン家庭教師 導線（台本 LP07_台本_v1）。比較の見出しより上だけ独自、「3つのポイント」は除外
    "lp07/index.html": dict(
        title="発達特性のある子の受験で家庭教師を選ぶなら「合格実績」だけで決めない｜確認したい4つ",
        desc="発達障害・グレーゾーンのお子さんの受験に向けた家庭教師選び。合格実績だけでなく、特性に合わせた教え方・志望校への対応・残り期間に合わせた優先順位・先生との相性を確認します。オンライン家庭教師3社の比較もまとめました。",
        parts=["lp07_top.html", "common_compare.html", "common_after.html"],
        prefix="../", sub=True),
    # LP08：不登校 × 家庭教師 → オンライン家庭教師 導線（台本 LP08_台本_v1）。比較の見出しより上だけ独自、「3つのポイント」は除外
    "lp08/index.html": dict(
        title="発達特性があり、不登校の子のために家庭教師を選ぶなら「勉強を教えてくれるか」だけで決めない｜4つの確認ポイント",
        desc="学校に行きづらい日が続く、発達障害・グレーゾーンのお子さんの家庭教師選び。短い時間から始められるか、発達特性やつまずき方に合わせてもらえるか、急かさずに関わってくれるかを入会前に確かめられるか、授業後の様子を親にも共有してくれるかを確認します。オンライン家庭教師3社の比較もまとめました。",
        parts=["lp08_top.html", "common_compare.html", "common_after.html"],
        prefix="../", sub=True),
}

def page_only(t, sub):
    """共通部品の中の <!--SUB-ONLY-->〜<!--/SUB-ONLY--> はサブLPにだけ、<!--OUDOU-ONLY-->〜<!--/OUDOU-ONLY--> は王道LPにだけ出す"""
    for tag, show in (("SUB-ONLY", sub), ("OUDOU-ONLY", not sub)):
        pat = r"[ \t]*<!--%s-->\n(.*?)[ \t]*<!--/%s-->\n" % (tag, tag)
        t = re.sub(pat, (lambda m: m.group(1)) if show else "", t, flags=re.S)
    return t

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
    t = page_only(t, d["sub"])
    t = add_prefix(t, d["prefix"])
    path = os.path.join(ROOT, out)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(t)
    print("wrote", out, len(t))

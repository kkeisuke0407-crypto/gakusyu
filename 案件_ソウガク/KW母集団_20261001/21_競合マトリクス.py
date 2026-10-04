# -*- coding: utf-8 -*-
"""競合ブランド × 検討語の掛け合わせを作り、KWPに投入する準備をする（評価しない・除外しない）。

  1. competitor_matrix.csv : ブランド検索形 × 修飾語（全組み合わせ）。KWP Historical Metrics の実測値を付ける
  2. seeds_round3.json     : KWP KeywordSeed（ブランド単体＋修飾語グループごとに 5〜10 語）
  3. holes_round3.txt      : Googleサジェスト用（全ブランドの主要検索形 × 主要修飾語）
生成した組み合わせはそのまま最終KWにはしない。KWPで数値が返ったものだけを CompetitorMatrix として統合する（14で実施）。
使い方: python 21_競合マトリクス.py        （生成のみ）
        python 21_競合マトリクス.py hist   （生成＋Historical Metrics 取得）
"""
import csv
import json
import sys
import time

import lib_soug as L

sys.stdout.reconfigure(encoding="utf-8")
ROUND = 3
MODS = {
    "評判・第三者評価": ["口コミ", "評判", "レビュー", "体験談", "感想", "評価"],
    "料金・契約": ["料金", "費用", "月謝", "値段", "価格", "入会金", "教材費", "高い", "安い"],
    "比較・選択": ["比較", "違い", "どっち", "おすすめ", "他社", "ランキング"],
    "不安・ネガティブ確認": ["デメリット", "メリット", "怪しい", "最悪", "失敗", "後悔", "合わない", "向いてない",
                       "やめたい", "辞めたい", "退会", "解約"],
    "申込直前": ["無料体験", "体験", "体験授業", "無料相談", "資料請求", "申し込み", "入会"],
    "発達特性との相性": ["発達障害", "発達障がい", "グレーゾーン", "ADHD", "ASD", "自閉症", "LD", "学習障害", "境界知能", "不登校"],
    "対象・用途": ["小学生", "中学生", "高校生", "高校受験", "中学受験", "大学受験"],
    # 主要競合のSERP（関連検索・PAA・上位タイトル）とサジェストで見つかった修飾語（round3 で追加）
    "追加：SERP・サジェスト由来": ["評判 悪い", "やばい", "知恵袋", "2ch", "料金表", "授業料", "夏期講習", "意味ない",
                             "バイト", "求人"],
    # 取得済み KeywordSeed（1,177リクエスト）の返却語で見つかった修飾語（Historical Metrics だけで実測）
    "追加：KWP KeywordSeed由来": ["クチコミ", "やめとけ", "合格実績", "時間割", "キャンペーン", "割引", "コース", "春期講習",
                             "冬期講習", "電話番号", "ホームページ", "株式会社", "講師", "とは"],
}
TRAIT_X = ["口コミ", "評判", "料金"]          # 例：トライ 発達障害 口コミ（主検索形だけ）
SUGGEST_MODS = ["", "口コミ", "評判", "料金", "発達障害"]


def brands():
    rows = list(csv.DictReader((L.HERE / "competitor_brands.csv").open(encoding="utf-8-sig")))
    out = {}
    for r in rows:
        if r["use_in_matrix"] == "1":
            out.setdefault(r["brand_name"], []).append(r["brand_alias"])
    return out


def build():
    matrix, groups, sugg = [], [], []
    for b, forms in brands().items():
        for i, f in enumerate(forms):
            groups.append(dict(group=f"競合:{b}|ブランド単体|{f}", keywords=[f]))
            for g, mods in MODS.items():
                kws = [f"{f} {m}" for m in mods]
                for k, m in zip(kws, mods):
                    matrix.append(dict(brand_name=b, brand_form=f, modifier_group=g, modifier=m, keyword=k))
                for j in range(0, len(kws), 6 if len(kws) > 10 else 10):   # 5〜10語ずつ
                    part = kws[j:j + (6 if len(kws) > 10 else 10)]
                    groups.append(dict(group=f"競合:{b}|{g}|{f}" + (f"#{j // 6 + 1}" if len(kws) > 10 else ""),
                                       keywords=part))
            if i == 0:
                for x in TRAIT_X:
                    kws = [f"{f} {t} {x}" for t in MODS["発達特性との相性"]]
                    for k, t in zip(kws, MODS["発達特性との相性"]):
                        matrix.append(dict(brand_name=b, brand_form=f, modifier_group=f"発達特性×{x}",
                                           modifier=f"{t} {x}", keyword=k))
                    groups.append(dict(group=f"競合:{b}|発達特性×{x}|{f}", keywords=kws))
                sugg += [f"{f} {m}".strip() for m in SUGGEST_MODS]
    return matrix, groups, sugg


def hist(matrix):
    sys.path.insert(0, r"C:\Users\user\Documents\google-ads-operations\kwp-mcp\src")
    from kwp_mcp.config import Settings
    from kwp_mcp.server import Context
    planner = Context(Settings.load()).planner
    path = L.HERE / "raw" / "hist_competitor_matrix.jsonl"
    have = {json.loads(l)["keyword"] for l in path.open(encoding="utf-8")} if path.exists() else set()
    todo = [k for k in dict.fromkeys(m["keyword"] for m in matrix) if k not in have]
    with path.open("a", encoding="utf-8") as f:
        for i in range(0, len(todo), 700):
            chunk = todo[i:i + 700]
            res = planner.get_historical_metrics(customer_id="6661622672", keywords=chunk, country="JP", language="ja",
                                                 network="GOOGLE_SEARCH", include_average_cpc=True)
            got = {r.original_keyword: r for r in res["records"]}
            for k in chunk:
                r = got.get(k)
                gm = r.google_metrics if r else None
                m = dict(avg_monthly_searches=gm.avg_monthly_searches, competition=gm.competition,
                         competition_index=gm.competition_index, low_bid=gm.low_top_of_page_bid,
                         high_bid=gm.high_top_of_page_bid,
                         monthly=[(x.year, x.month_number, x.monthly_searches) for x in gm.monthly_search_volumes]
                         ) if gm else {}
                f.write(json.dumps(dict(keyword=k, matched=(r.text if r and hasattr(r, "text") else ""), metrics=m,
                                        fetched_at=time.strftime("%Y-%m-%d %H:%M:%S")), ensure_ascii=False) + "\n")
            print(f"  hist {i + len(chunk)}/{len(todo)}", flush=True)
            time.sleep(2)


def main():
    matrix, groups, sugg = build()
    if len(sys.argv) > 1 and sys.argv[1] == "hist":
        hist(matrix)
    h = {}
    p = L.HERE / "raw" / "hist_competitor_matrix.jsonl"
    if p.exists():
        h = {j["keyword"]: j["metrics"] for j in map(json.loads, p.open(encoding="utf-8"))}
    with (L.HERE / "competitor_matrix.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(matrix[0].keys()) + ["kwp_measured", "average_monthly_searches"])
        w.writeheader()
        for m in matrix:
            mm = h.get(m["keyword"])
            w.writerow(dict(m, kwp_measured="" if mm is None else ("値あり" if mm else "値なし"),
                            average_monthly_searches="" if not mm else mm.get("avg_monthly_searches", "")))
    seeds = L.HERE / f"seeds_round{ROUND}.json"
    seeds.write_text(json.dumps({"keyword_groups": groups}, ensure_ascii=False, indent=1), encoding="utf-8")
    (L.HERE / f"holes_round{ROUND}.txt").write_text("\n".join(dict.fromkeys(sugg)) + "\n", encoding="utf-8")
    print(f"マトリクス {len(matrix):,} / KeywordSeed {len(groups):,} / サジェスト語 {len(set(sugg))}")


if __name__ == "__main__":
    main()

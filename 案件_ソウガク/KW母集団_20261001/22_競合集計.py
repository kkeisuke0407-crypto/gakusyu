# -*- coding: utf-8 -*-
"""競合ブランド×検討語の補完分を集計し、out/competitor_keywords.csv を作って out/REPORT.md に追記する。
評価・優先順位・除外はしない。19_レポート.py の後に実行する（19 が REPORT.md を作り直すため）。
使い方: python 22_競合集計.py
"""
import csv
import json
import re
import sys
from collections import Counter

import lib_soug as L

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(10 ** 8)
OUT = L.HERE / "out"
COMP_SRC = ("KWP_CompetitorKeywordSeed", "CompetitorMatrix", "Google_competitor_SERP", "Google_competitor_suggest")
BASE_UNIQUE = 50995   # 競合補完の前（2026-10-01 収集完了時点）のユニーク件数


def load_mods():
    import importlib.util
    spec = importlib.util.spec_from_file_location("m", L.HERE / "21_競合マトリクス.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.MODS


def main():
    mods = load_mods()
    brands = list(csv.DictReader((L.HERE / "competitor_brands.csv").open(encoding="utf-8-sig")))
    aliases = sorted({(L.norm(b["brand_alias"]), b["brand_name"]) for b in brands}, key=lambda x: -len(x[0]))
    mod_index = sorted(((L.norm(w), g) for g, ws in mods.items() for w in ws), key=lambda x: -len(x[0]))

    obs = list(csv.DictReader((OUT / "observations.csv").open(encoding="utf-8-sig")))
    comp = [r for r in obs if r["discovery_source"] in COMP_SRC]
    rows = []
    for r in comp:
        n = r["normalized_keyword"]
        hit = [b for a, b in aliases if a and a in n]
        seed_b = re.search(r"brand_name=([^・]*)", r["notes"])
        seed_g = re.search(r"modifier_group=([^・]*)", r["notes"])
        rest = n
        for a, _ in aliases:
            rest = rest.replace(a, "")
        groups = [g for w, g in mod_index if w and w in rest]
        rows.append(dict(keyword=r["keyword"], average_monthly_searches=r["average_monthly_searches"],
                         competition=r["competition"], competition_index=r["competition_index"],
                         low_top_of_page_bid=r["low_top_of_page_bid"], high_top_of_page_bid=r["high_top_of_page_bid"],
                         monthly_search_volumes=r["monthly_search_volumes"], seed=r["seed_keyword"],
                         brand_name=" | ".join(dict.fromkeys(hit)) or (seed_b.group(1) if seed_b else ""),
                         brand_in_keyword="あり" if hit else "なし（seedのブランド）",
                         modifier_group=" | ".join(dict.fromkeys(groups)) or (seed_g.group(1) if seed_g else ""),
                         discovery_source=r["discovery_source"], intent_category=r["intent_category"]))
    with (OUT / "competitor_keywords.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    uniq = list(csv.DictReader((OUT / "keywords_unique.csv").open(encoding="utf-8-sig")))
    only_comp = [u for u in uniq if all(s in COMP_SRC for s in u["discovery_source"].split(" || "))]
    matrix = list(csv.DictReader((L.HERE / "competitor_matrix.csv").open(encoding="utf-8-sig")))
    kwp3 = [json.loads(l) for l in (L.HERE / "raw" / "kwp_round3.jsonl").open(encoding="utf-8")]
    seeds3 = json.loads((L.HERE / "seeds_round3.json").read_text(encoding="utf-8"))["keyword_groups"]
    serp3 = sorted((L.HERE / "serp" / "round3").glob("*.json"))
    sug3 = list(L.iter_suggest(3))
    src = Counter(r["discovery_source"] for r in comp)
    log = (L.HERE / "kwp_round3.log").read_text(encoding="utf-8", errors="ignore")
    m_ = re.search(r"jobs (\d+)", log)
    planned = int(m_.group(1)) if m_ else len(seeds3)
    # 収束の確認：既存母集団（競合補完以外の経路）にもマトリクスにも無い語が、リクエスト順にどれだけ増えたか
    base = {u["normalized_keyword"] for u in uniq if any(x not in COMP_SRC for x in u["discovery_source"].split(" || "))}
    mset = {L.norm(x["keyword"]) for x in matrix}
    seen, conv = set(), []
    for j in kwp3:
        n_new = 0
        for r in j.get("records", []):
            k = L.norm(r["keyword"])
            if k not in base and k not in mset and k not in seen:
                seen.add(k)
                n_new += 1
        conv.append(n_new)
    bset = Counter(b["brand_name"] for b in brands)

    w = ["\n---\n", "## 追記：競合ブランド × 検討語の補完（2026-10-01・収集フェーズ最終工程）",
         "判断・評価・優先順位・除外はしていない。生成した掛け合わせはそのまま最終KWにせず、KWPで実測した。\n",
         f"- **競合ブランド数**：{len(bset)} ブランド（表記 {len(brands)} 件／掛け合わせに使った検索形 "
         f"{sum(b['use_in_matrix'] == '1' for b in brands)} 件）→ `competitor_brands.csv`",
         f"- **生成したブランド×修飾語数**：{len(matrix):,} 語 → `competitor_matrix.csv`"
         f"（KWP Historical Metrics で全件実測。月間検索数に値が返ったもの "
         f"{sum(1 for m in matrix if m['average_monthly_searches'] not in ('', '0'))} 語を CompetitorMatrix として統合。"
         "値が返らなかった語は competitor_matrix.csv にだけ残し、母集団には入れていない）",
         f"- **KWP投入数**：KeywordSeed 実行 {len(kwp3):,} リクエスト（計画 {planned:,} のうち、直近200リクエストで新しい"
         f"競合検索意図・修飾語がほぼ増えなくなったため停止。エラー {sum(1 for j in kwp3 if j.get('error'))} 件は"
         "PCスリープ中の通信断（503）で、再取得はしていない）＋ Historical Metrics "
         f"{len(matrix):,} 語。Google検索 {len(serp3)} クエリ（CAPTCHA 0）・サジェスト {len(sug3):,} 回",
         f"- **追加観測数**：{len(comp):,} 件（" + " / ".join(f"{k} {v:,}" for k, v in src.most_common()) + "）",
         f"- **新規ユニークKW数**：{len(only_comp):,} 件（競合補完の経路でしか観測されていないKW）。"
         f"既存KWに経路が追加されたものを含む増分：{len(uniq) - BASE_UNIQUE:,} 件",
         f"- **最終ユニークKW総数**：{len(uniq):,} 件",
         "\n### 使用した競合ブランド一覧",
         "| brand_name | service_type | 検索形（掛け合わせに使用） | 表記揺れ | domain |\n|---|---|---|---|---|"]
    by = {}
    for b in brands:
        by.setdefault(b["brand_name"], []).append(b)
    for name, bs in by.items():
        w.append(f"| {name} | {bs[0]['service_type']} | {' / '.join(b['brand_alias'] for b in bs if b['use_in_matrix'] == '1')} | "
                 f"{' / '.join(b['brand_alias'] for b in bs if b['use_in_matrix'] != '1')} | {bs[0]['domain']} |")
    w.append("\n### KeywordSeed の収束確認（200リクエストごとの、既存母集団にもマトリクスにも無い新規語の数）")
    w.append(" / ".join(f"{i + 1}〜{min(i + 200, len(conv))}件目：{sum(conv[i:i + 200]):,}語" for i in range(0, len(conv), 200)))
    w.append("401〜800件目の増加は、校舎名・地名が多いブランド（森塾・スクールIE・明光義塾・個別指導Axis など）と、同名の別業種"
             "（老人ホーム・投資・自動車など）の語が中心。直近200件で初めて出た修飾語は、地名・校舎名と無関係な語だけだった")
    w.append("\n### 使用した修飾語グループ一覧")
    for g, ws in mods.items():
        w.append(f"- **{g}**：{' / '.join(ws)}")
    w.append("- **発達特性×口コミ／評判／料金**（主検索形のみ）：発達特性の10語 × 口コミ・評判・料金")
    w.append("\n### 競合系の意図カテゴリー（完了判定用）")
    hist = L.load_map()["history"]
    w.append(" / ".join(f"更新{h['round']}回目：新大分類{len(h.get('new_intent_categories', []))}・"
                        f"新サブカテゴリ{len(h.get('new_subcategories', []))}" for h in hist if h["round"] >= 5))
    w.append("更新6回目の新大分類2つ（運営会社・企業情報／利用中・会員の手続き）は、競合SERP・サジェストと KeywordSeed 前半の語"
             "（株式会社・社長・ログイン・電話番号など）から追加したもの。直近200リクエストからは新しい競合系の意図・修飾語は出ていない")
    w.append("\n### 収集フェーズの完了判定")
    w.append("1. 主要競合ブランド一覧：作成済み（competitor_brands.csv）\n"
             "2. 口コミ・評判・料金・比較・体験・ネガティブ確認・発達特性・対象の修飾語：全ブランドの検索形について Historical Metrics で実測済み。"
             f"KeywordSeed は {len(kwp3):,} リクエスト投入済み\n"
             "3. KWPから返った競合指名語：母集団へ統合済み（KWP_CompetitorKeywordSeed）\n"
             "4. 新しい競合系の意図カテゴリー：直近200リクエストではほぼ出ていない\n"
             "5. 削除：完全重複の統合以外はしていない\n\n"
             "→ **ソウガク KW母集団 収集フェーズ完了**")
    with (OUT / "REPORT.md").open("a", encoding="utf-8") as f:
        f.write("\n".join(w) + "\n")
    print(f"競合観測 {len(comp):,} / 新規ユニーク {len(only_comp):,} / 総ユニーク {len(uniq):,}")


if __name__ == "__main__":
    main()

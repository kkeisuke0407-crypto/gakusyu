# -*- coding: utf-8 -*-
"""out/REPORT.md：依頼書の11項目だけを出す（おすすめKW・出稿候補・高CV候補・低CPC候補は出さない）。
使い方: python 19_レポート.py
"""
import csv
import glob
import json
import sys
from collections import Counter, defaultdict

import lib_soug as L

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(10 ** 8)
OUT = L.HERE / "out"


def main():
    obs = list(csv.DictReader((OUT / "observations.csv").open(encoding="utf-8-sig")))
    uniq = list(csv.DictReader((OUT / "keywords_unique.csv").open(encoding="utf-8-sig")))
    pre = [r for r in obs if r["keyword"].strip()]
    norm_u = {r["normalized_keyword"] for r in uniq}
    src = Counter(r["discovery_source"] for r in obs)

    cat = Counter()
    for r in uniq:
        for c in r["intent_category"].split(" | "):
            cat[c] += 1
    m = L.load_map()
    names = list(m["intent_categories"].keys())

    kwp = [json.loads(l) for p in sorted((L.HERE / "raw").glob("kwp_round*.jsonl")) for l in p.open(encoding="utf-8")]
    by_type = defaultdict(list)
    for j in kwp:
        by_type[j["seed_type"]].append(j)

    serp = []
    for f in sorted(glob.glob(str(L.HERE / "serp" / "round*" / "*.json"))):
        d = json.loads(open(f, encoding="utf-8").read())
        serp.append((d.get("round"), d.get("q")))
    captcha = [json.loads(l) for l in (L.HERE / "serp" / "captcha_log.jsonl").open(encoding="utf-8")] \
        if (L.HERE / "serp" / "captcha_log.jsonl").exists() else []
    planned2 = [l.strip() for l in (L.HERE / "serp_queries_round2.txt").open(encoding="utf-8") if l.strip()]
    done_q = {q for _, q in serp}
    not_run = [q for q in planned2 if q not in done_q]

    cov = list(csv.DictReader((L.HERE / "coverage.csv").open(encoding="utf-8-sig")))
    zero = [r for r in cov if int(r["discovered_keywords_count"]) == 0]

    w = []
    w.append("# ソウガク KW母集団 収集レポート（2026-10-01）\n")
    w.append("判断・評価・優先順位・出稿可否は含まない。分類は意図マップ語彙によるデータ整理のみ（1KWに複数の大分類が付く）。\n")
    w.append("## 1. 総取得数")
    w.append(f"- {len(obs):,} 観測（`out/observations.csv`、1観測1行）")
    w.append("- 内訳: " + " / ".join(f"{k} {v:,}" for k, v in src.most_common()))
    w.append("\n## 2. 重複除去前の件数")
    w.append(f"- {len(pre):,} 件（keyword が空でない観測行）")
    w.append("\n## 3. 重複除去後のユニーク件数")
    w.append(f"- {len(uniq):,} 件（`out/keywords_unique.csv`、keyword の完全一致のみ統合。表記揺れ・語順違いは別行）")
    w.append(f"- 参考：normalized_keyword（NFKC＋空白除去＋小文字化）単位では {len(norm_u):,} 種類")
    w.append("\n## 4. 主要な意図カテゴリー一覧")
    for n in names:
        spec = m["intent_categories"][n]
        w.append(f"- {n}（意図マップ更新{spec['round']}回目で追加／該当サブカテゴリ: {', '.join(spec['any_axes'])}）")
    w.append(f"- 未分類（どの大分類にも当たらないもの）")
    w.append("\n## 5. 意図カテゴリー別件数（ユニークKW基準・複数該当あり）")
    w.append("| 意図カテゴリー | 件数 |\n|---|---:|")
    for n in names + ["未分類"]:
        w.append(f"| {n} | {cat.get(n, 0):,} |")

    w.append("\n## 6. 使用したKeywordSeed一覧")
    for j in by_type["KeywordSeed"]:
        w.append(f"- round{j['round']}｜{j['seed_group']}｜{' / '.join(j['keywords'])}｜取得{j.get('record_count', 0)}件"
                 + ("｜エラー" if j.get("error") else ""))
    w.append("\n## 7. 使用したURLSeed一覧")
    for t in ("UrlSeed", "KeywordAndUrlSeed"):
        w.append(f"\n### {t}（{len(by_type[t])}件）")
        for j in by_type[t]:
            kw = f"｜KW: {' / '.join(j['keywords'])}" if j.get("keywords") else ""
            w.append(f"- round{j['round']}｜{j['url']}｜{j['seed_group']}{kw}｜取得{j.get('record_count', 0)}件")
    w.append("\n## 8. 使用したSiteSeed一覧")
    for j in by_type["SiteSeed"]:
        w.append(f"- round{j['round']}｜{j['site']}｜取得{j.get('record_count', 0)}件")
    w.append("\n## 9. 使用したGoogle検索クエリ一覧")
    for rnd, q in serp:
        w.append(f"- round{rnd}｜{q}")
    w.append(f"- サジェスト：各周回のSERPクエリ・関連検索・穴埋め語（`holes_round2.txt`）について「語」「語＋空白」で取得（`suggest/round*.jsonl`）")

    w.append("\n## 10. 周回ごとの新規カテゴリー数")
    w.append("意図マップの更新回ごとに集計（1回目＝依頼書の初期版、2回目＝1周目の取得データ、3・4回目＝1周目＋2周目途中までの統合データの未分類読解、5回目＝穴埋め周回の取得データ）。\n")
    w.append("| 意図マップ更新 | 根拠データ | 新しい大分類 | 新しいサブカテゴリ | 追加語 |\n|---|---|---:|---:|---:|")
    for h in m["history"]:
        if h["round"] == 1:
            w.append(f"| 1回目 | 依頼書（初期マップ） | {len(names and [n for n in names if m['intent_categories'][n]['round'] == 1])} | "
                     f"{sum(1 for a in m['axes'].values() for c in a.values() if c.get('round') == 1)} | — |")
        else:
            w.append(f"| {h['round']}回目 | {h.get('source', '')[:80]} | {len(h.get('new_intent_categories', []))} | "
                     f"{len(h.get('new_subcategories', []))} | {h.get('new_terms', 0)} |")

    w.append("\n## 11. まだ探索不足の可能性がある領域")
    w.append(f"- **SERPを取れていないクエリ（CAPTCHAで停止 {len(captcha)} 回）**：2周目予定{len(planned2)}件のうち未取得 {len(not_run)} 件。"
             "サジェスト・KWPで代替したが、PAA・上位ページ見出しは未取得："
             + " / ".join(not_run))
    zero_kw = [j for j in by_type["KeywordSeed"] if not j.get("record_count")]
    w.append("- **KWPが候補を返さなかったseed**（健康・医療系の語で0件になる）：" +
             " / ".join(f"{j['seed_group']}（{' / '.join(j['keywords'])}）" for j in zero_kw))
    zero_done = [r for r in zero if r["serp_searched"] != "0" or r["kwp_keyword_seeded"] != "0"]
    zero_todo = [r for r in zero if r["serp_searched"] == "0" and r["kwp_keyword_seeded"] == "0"]
    w.append(f"- **coverage.csv で発見KWが0件の組み合わせ {len(zero)} / {len(cov)} 件**"
             f"（うち穴埋めでSERP・KWPに投入済みでも0件 {len(zero_done)} 件／意図マップ更新4・5回目で増えたサブカテゴリのため未投入 {len(zero_todo)} 件）。"
             "ASD（自閉症・アスペルガー）を含む組み合わせは、KWPが自閉症・アスペルガーで候補を返さないため、検索がないのか計測できていないのかを区別できていない：")
    by_pair = defaultdict(list)
    for r in zero:
        axes = "×".join(c.split("/", 1)[0] for c in r["combination"].split(" × "))
        by_pair[axes].append(r["combination"])
    for k, v in sorted(by_pair.items(), key=lambda kv: -len(kv[1])):
        w.append(f"  - {k}（{len(v)}件）：" + " / ".join(x.replace("発達特性/", "").replace("子どもの属性/", "")
                                                      .replace("解決手段/", "").replace("学習課題/", "")
                                                      .replace("検討行動/", "").replace("保護者の悩み/", "")
                                                      .replace("シチュエーション・出来事/", "") for x in v[:40])
                 + (" …" if len(v) > 40 else ""))
    un = Counter(r["discovery_source"].split(" || ")[0] for r in uniq if r["intent_category"] == "未分類")
    w.append(f"- **未分類 {sum(un.values()):,} 件**（" + " / ".join(f"{k} {v:,}" for k, v in un.most_common())
             + "）。読解した範囲では、URLSeed由来の無関係語（メール・保険・VR・公務員試験など）と競合サイトの構造見出し"
               "（アクセス・地域選択・プライバシーポリシー等）が中心")
    w.append("- **URLSeedは443件で投入を停止**（方針変更）。未投入の下層ページ・KeywordAndUrlSeed・SiteSeedは、薄い意図の代表URLと主要競合10サイトだけに絞った")
    (OUT / "REPORT.md").write_text("\n".join(w) + "\n", encoding="utf-8")
    print("REPORT.md", len(w), "行")


if __name__ == "__main__":
    main()

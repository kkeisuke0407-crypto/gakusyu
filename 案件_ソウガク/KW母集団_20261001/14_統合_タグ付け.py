# -*- coding: utf-8 -*-
"""全ソースを統合して observations.csv（重複除去前）と keywords_unique.csv（完全一致のみ統合）を作る。

・評価・優先度・除外は一切しない。分類（タグ）は意図マップの語彙によるデータ整理だけ。分類不能は「未分類」。
・NO DATA は空欄（0にしない）。表記揺れ・語順違いは別行（normalized_keyword を別列で持つ）。
・Google由来の検索語（関連検索・サジェスト）とPAA自然文は、KWP Historical Metrics で数値を付ける（数値が出ない語は空欄）。
出力: out/observations.csv, out/keywords_unique.csv
"""
from __future__ import annotations

import csv
import json
import sys
import time
import warnings
from collections import defaultdict
from pathlib import Path

import lib_soug as L

warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")
OUT = L.HERE / "out"
OUT.mkdir(exist_ok=True)
COMP_ROUND = 3   # 競合ブランド×検討語の補完周回
COLS = ["keyword", "normalized_keyword", "average_monthly_searches", "competition", "competition_index",
        "low_top_of_page_bid", "high_top_of_page_bid", "monthly_search_volumes", "discovery_source", "seed_type",
        "seed_keyword", "seed_url", "intent_category", "intent_subcategory", "target_attribute",
        "condition_or_trait", "problem_or_need", "solution_type", "decision_stage", "source_url",
        "source_page_title", "search_query_used", "notes"]


def blank(v):
    return "" if v is None else v


def monthly_str(m):
    ms = sorted((x for x in m or [] if x[1] and x[2] is not None), key=lambda x: (x[0], x[1]))
    return "|".join(f"{y}-{mo:02d}:{v}" for y, mo, v in ms)


def metric_cols(m: dict | None) -> dict:
    m = m or {}
    return dict(average_monthly_searches=blank(m.get("avg_monthly_searches")),
                competition=blank(m.get("competition")), competition_index=blank(m.get("competition_index")),
                low_top_of_page_bid=blank(m.get("low_bid")), high_top_of_page_bid=blank(m.get("high_bid")),
                monthly_search_volumes=monthly_str(m.get("monthly")))


def tag_cols(text: str) -> dict:
    t = L.tag(text)
    return {k: " | ".join(t[k]) for k in ("intent_category", "intent_subcategory", "target_attribute",
                                          "condition_or_trait", "problem_or_need", "solution_type", "decision_stage")}


def hist_metrics(keywords: list[str]) -> dict:
    """Google由来の検索語に KWP の数値を付ける（キャッシュ: raw/hist_google_terms.jsonl）"""
    path = L.HERE / "raw" / "hist_google_terms.jsonl"
    have = {}
    if path.exists():
        for line in path.open(encoding="utf-8"):
            j = json.loads(line)
            have[j["keyword"]] = j["metrics"]
    todo = [k for k in dict.fromkeys(keywords) if k and k not in have and len(k) <= 80]
    if todo:
        sys.path.insert(0, r"C:\Users\user\Documents\google-ads-operations\kwp-mcp\src")
        from kwp_mcp.config import Settings
        from kwp_mcp.server import Context
        planner = Context(Settings.load()).planner
        with path.open("a", encoding="utf-8") as f:
            for i in range(0, len(todo), 700):
                chunk = todo[i:i + 700]
                res = planner.get_historical_metrics(customer_id="6661622672", keywords=chunk, country="JP",
                                                     language="ja", network="GOOGLE_SEARCH", include_average_cpc=True)
                got = {r.original_keyword: r for r in res["records"]}
                for k in chunk:
                    r = got.get(k)
                    gm = r.google_metrics if r else None
                    m = dict(avg_monthly_searches=gm.avg_monthly_searches, competition=gm.competition,
                             competition_index=gm.competition_index, low_bid=gm.low_top_of_page_bid,
                             high_bid=gm.high_top_of_page_bid,
                             monthly=[(x.year, x.month_number, x.monthly_searches) for x in gm.monthly_search_volumes]
                             ) if gm else {}
                    have[k] = m
                    f.write(json.dumps(dict(keyword=k, metrics=m, fetched_at=time.strftime("%Y-%m-%d %H:%M:%S")),
                                       ensure_ascii=False) + "\n")
                time.sleep(2)
    return have


def main():
    rows = []
    resolver = L.url_resolver()

    # ---- KWP（4種seed） ----
    for j in L.iter_kwp():
        comp = (j.get("seed_group") or "").startswith("競合:")
        if comp:   # 競合ブランド×検討語の KeywordSeed（seed_group = 競合:ブランド|修飾語グループ|検索形）
            b, g, *_ = j["seed_group"][3:].split("|") + [""]
        for r in j.get("records", []):
            rows.append(dict(keyword=r["keyword"], **metric_cols(r["metrics"]),
                             discovery_source="KWP_CompetitorKeywordSeed" if comp else f"KWP_{j['seed_type']}",
                             seed_type=j["seed_type"],
                             seed_keyword=" / ".join(j.get("keywords") or []), seed_url=j.get("url") or j.get("site") or "",
                             source_url="", source_page_title="", search_query_used="",
                             notes=(f"brand_name={b}・modifier_group={g}・" if comp else "")
                                   + f"round{j['round']}・seed_group={j.get('seed_group', '')}・取得{j.get('fetched_at', '')}"))

    # ---- Google SERP（自然検索・広告タイトル、PAA、関連検索） ----
    google_terms = []
    for d in L.iter_serp():
        q, rnd = d.get("q", ""), d.get("round")
        gs = "Google_competitor_SERP" if rnd == COMP_ROUND else None
        for kind in ("organic", "ads"):
            for rank, r in enumerate(d.get(kind, []), 1):
                real = resolver.get(r.get("url", ""), r.get("url", ""))
                rows.append(dict(keyword=r.get("title", ""), discovery_source=gs or "Google_SERP", seed_type="Google検索",
                                 seed_keyword=q, seed_url="", source_url=real, source_page_title=r.get("title", ""),
                                 search_query_used=q,
                                 notes=f"round{rnd}・{'広告' if kind == 'ads' else '自然検索'}{rank}位・"
                                       f"snippet={(r.get('snippet') or r.get('text') or '')[:200]}"))
        for p in d.get("paa", []):
            if p != q:
                rows.append(dict(keyword=p, discovery_source=gs or "Google_PAA", seed_type="Google検索_PAA" if gs else "Google検索", seed_keyword=q,
                                 seed_url="", source_url="", source_page_title="", search_query_used=q,
                                 notes=f"round{rnd}"))
                google_terms.append(p)
        for t in d.get("related", []):
            rows.append(dict(keyword=t, discovery_source=gs or "Google_related_search", seed_type="Google検索_関連検索" if gs else "Google検索",
                             seed_keyword=q, seed_url="", source_url="", source_page_title="", search_query_used=q,
                             notes=f"round{rnd}"))
            google_terms.append(t)
    for s in L.iter_suggest():
        for t in s.get("suggestions", []):
            rows.append(dict(keyword=t, discovery_source="Google_competitor_suggest" if s["round"] == COMP_ROUND
                             else "Google_suggest", seed_type="Googleサジェスト",
                             seed_keyword=s["input"], seed_url="", source_url="", source_page_title="",
                             search_query_used=s["input"], notes=f"round{s['round']}"))
            google_terms.append(t)

    # ---- 競合・関連ページ（title / H1 / H2 / H3 / FAQ） ----
    for p in L.iter_pages():
        if p.get("status") != 200:
            continue
        for field in ("title", "h1", "h2", "h3", "faq"):
            vals = p.get(field) or []
            for v in ([vals] if isinstance(vals, str) else vals):
                if v:
                    rows.append(dict(keyword=v, discovery_source="Google_competitor", seed_type=f"page_{field}",
                                     seed_keyword="", seed_url="", source_url=p["url"],
                                     source_page_title=p.get("title", ""), search_query_used="",
                                     notes=f"round{p['round']}"))

    # ---- 自然文（Q&Aタイトル等。PAAとFAQは上で入っているので重ならない種類だけ） ----
    for n in L.iter_natural():
        if n["source"] == "Q&A_title":
            rows.append(dict(keyword=n["query"], discovery_source="Google_SERP", seed_type="Q&Aタイトル",
                             seed_keyword=n.get("parent_query", ""), seed_url="", source_url=n.get("source_url", ""),
                             source_page_title=n["query"], search_query_used=n.get("parent_query", ""),
                             notes=f"round{n['discovered_round']}・自然文"))

    # ---- 競合ブランド×検討語マトリクス：KWP Historical Metrics で値（月間検索数>0）が返った組み合わせだけ ----
    mpath = L.HERE / "raw" / "hist_competitor_matrix.jsonl"
    if mpath.exists():
        info = {m["keyword"]: m for m in csv.DictReader((L.HERE / "competitor_matrix.csv").open(encoding="utf-8-sig"))}
        for j in map(json.loads, mpath.open(encoding="utf-8")):
            m = j["metrics"] or {}
            if not m.get("avg_monthly_searches"):
                continue
            i = info.get(j["keyword"], {})
            rows.append(dict(keyword=j["keyword"], **metric_cols(m), discovery_source="CompetitorMatrix",
                             seed_type="ブランド×修飾語（Historical Metrics）", seed_keyword=i.get("brand_form", ""),
                             seed_url="", source_url="", source_page_title="", search_query_used="",
                             notes=f"brand_name={i.get('brand_name', '')}・modifier_group={i.get('modifier_group', '')}・"
                                   f"round{COMP_ROUND}・取得{j.get('fetched_at', '')}"))

    # ---- Google由来の検索語に KWP の数値を付ける ----
    hm = hist_metrics(google_terms)
    for r in rows:
        if r["discovery_source"] in ("Google_related_search", "Google_suggest", "Google_PAA",
                                     "Google_competitor_suggest") or r.get("seed_type") in ("Google検索_PAA", "Google検索_関連検索"):
            r.update(metric_cols(hm.get(r["keyword"])))
        for c in COLS:
            r.setdefault(c, "")
        r["normalized_keyword"] = L.norm(r["keyword"])
        r.update(tag_cols(r["keyword"]))

    with (OUT / "observations.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)

    # ---- ユニーク（keyword の完全一致のみ統合。経路はすべて連結して保持） ----
    uniq: dict[str, dict] = {}
    agg = defaultdict(lambda: defaultdict(list))
    for r in rows:
        k = r["keyword"]
        if k not in uniq:
            uniq[k] = dict(r)
        else:
            for c in ("average_monthly_searches", "competition", "competition_index", "low_top_of_page_bid",
                      "high_top_of_page_bid", "monthly_search_volumes"):
                if uniq[k][c] == "" and r[c] != "":
                    uniq[k][c] = r[c]
        for c in ("discovery_source", "seed_type", "seed_keyword", "seed_url", "source_url", "source_page_title",
                  "search_query_used"):
            if r[c] and r[c] not in agg[k][c]:
                agg[k][c].append(r[c])
    for k, u in uniq.items():
        for c, vals in agg[k].items():
            u[c] = " || ".join(vals[:50]) + (f" || …他{len(vals) - 50}" if len(vals) > 50 else "")
        u["notes"] = f"観測{sum(1 for _ in [])}"
    counts = defaultdict(int)
    for r in rows:
        counts[r["keyword"]] += 1
    for k, u in uniq.items():
        u["notes"] = f"観測回数{counts[k]}"
    with (OUT / "keywords_unique.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(uniq.values())
    print(f"observations {len(rows):,} / unique {len(uniq):,}")


if __name__ == "__main__":
    main()

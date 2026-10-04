# -*- coding: utf-8 -*-
"""coverage.csv：意図マップの主要軸の掛け合わせごとに、どこまで探索したかを記録する（件数の評価はしない）。

主要な掛け合わせ（全直積は作らない）
  発達特性 × 解決手段 / 学習課題 / 子どもの属性 / 検討行動 / 保護者の悩み / シチュエーション
  子どもの属性 × 解決手段 / 学習課題
  解決手段 × 検討行動
  発達特性 × 子どもの属性(小中高・受験生・不登校) × 解決手段(家庭教師・オンライン・塾)
列：combination, serp_searched, kwp_keyword_seeded, kwp_url_seeded, discovered_keywords_count, last_round
使い方: python 15_カバレッジ.py
"""
from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from itertools import product

import lib_soug as L

sys.stdout.reconfigure(encoding="utf-8")

PAIRS = [("発達特性", "解決手段"), ("発達特性", "学習課題"), ("発達特性", "子どもの属性"), ("発達特性", "検討行動"),
         ("発達特性", "保護者の悩み"), ("発達特性", "シチュエーション・出来事"), ("子どもの属性", "解決手段"),
         ("子どもの属性", "学習課題"), ("解決手段", "検討行動")]
TRIPLE_ATTR = ["小学生", "中学生", "高校生", "受験生", "不登校"]
TRIPLE_SOL = ["家庭教師", "オンライン家庭教師・オンライン塾", "塾・個別指導"]


def combos(m: dict) -> list[tuple[str, ...]]:
    out = []
    for a, b in PAIRS:
        for ca, cb in product(m["axes"][a], m["axes"][b]):
            out.append((f"{a}/{ca}", f"{b}/{cb}"))
    for t, at, s in product(m["axes"]["発達特性"], TRIPLE_ATTR, TRIPLE_SOL):
        out.append((f"発達特性/{t}", f"子どもの属性/{at}", f"解決手段/{s}"))
    return out


def keyset(text: str) -> set[str]:
    return set(L.tag(text)["intent_subcategory"])


def main():
    m = L.load_map()
    combo_list = combos(m)
    serp = defaultdict(int)
    kws = defaultdict(int)
    urls = defaultdict(int)
    found = defaultdict(set)
    last = defaultdict(int)

    def mark(store, ks, rnd, value=None):
        for c in combo_list:
            if set(c) <= ks:
                key = " × ".join(c)
                if value is None:
                    store[key] += 1
                else:
                    store[key].add(value)
                last[key] = max(last[key], rnd)

    for rnd in L.rounds_available():
        for d in L.iter_serp(rnd):
            mark(serp, keyset(d.get("q", "")), rnd)
        for j in L.iter_kwp(rnd):
            if j["seed_type"] in ("KeywordSeed", "KeywordAndUrlSeed"):
                for k in j.get("keywords") or []:
                    mark(kws, keyset(k), rnd)
            if j["seed_type"] in ("UrlSeed", "KeywordAndUrlSeed", "SiteSeed"):
                mark(urls, keyset(" ".join(j.get("keywords") or []) + " " + (j.get("seed_group") or "")
                                  + " " + (j.get("url") or "")), rnd)
            for r in j.get("records", []):
                mark(found, keyset(r["keyword"]), rnd, L.norm(r["keyword"]))
        for s in L.iter_suggest(rnd):
            for t in s.get("suggestions", []):
                mark(found, keyset(t), rnd, L.norm(t))
        for d in L.iter_serp(rnd):
            for t in d.get("related", []) + d.get("paa", []):
                mark(found, keyset(t), rnd, L.norm(t))

    rows = []
    for c in combo_list:
        key = " × ".join(c)
        rows.append(dict(combination=key, serp_searched=serp.get(key, 0), kwp_keyword_seeded=kws.get(key, 0),
                         kwp_url_seeded=urls.get(key, 0), discovered_keywords_count=len(found.get(key, ())),
                         last_round=last.get(key, "")))
    with (L.HERE / "coverage.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    untouched = [r for r in rows if not r["serp_searched"] and not r["kwp_keyword_seeded"]]
    no_kw = [r for r in rows if r["discovered_keywords_count"] == 0]
    print(f"combinations {len(rows)} / SERP・KWPとも未実施 {len(untouched)} / 発見KW0 {len(no_kw)}")


if __name__ == "__main__":
    main()

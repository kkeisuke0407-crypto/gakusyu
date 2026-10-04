# -*- coding: utf-8 -*-
"""ソウガクKW母集団の共通部品：意図マップの読み込み・タグ付け・全ソースの読み出し。

タグ付けはデータ整理のためだけ（評価しない）。照合は NFKC＋空白除去＋小文字化した文字列への部分一致。
"""
from __future__ import annotations

import csv
import json
import re
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Iterator

HERE = Path(__file__).resolve().parent
AXIS_COLUMN = {
    "発達特性": "condition_or_trait",
    "子どもの属性": "target_attribute",
    "学習課題": "problem_or_need",
    "保護者の悩み": "problem_or_need",
    "シチュエーション・出来事": "problem_or_need",
    "解決手段": "solution_type",
    "検討行動": "decision_stage",
    "検索者の立場": "target_attribute",
    "地域": "target_attribute",
}


def norm(text: str) -> str:
    """normalized_keyword：NFKC＋空白除去＋小文字化（表記の照合用。元の語は別に残す）"""
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", str(text))).lower()


def load_map() -> dict:
    return json.loads((HERE / "00_意図マップ.json").read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def _compiled():
    m = load_map()
    axes = []
    for axis, cats in m["axes"].items():
        for cat, spec in cats.items():
            terms = sorted({norm(t) for t in spec["terms"] if t}, key=len, reverse=True)
            axes.append((axis, cat, terms))
    intents = [(name, set(spec["any_axes"])) for name, spec in m["intent_categories"].items()]
    intents.append(("__fallback__", m.get("fallback_trait_only")))
    vocab = sorted({t for _, _, ts in axes for t in ts}, key=len, reverse=True)
    return axes, intents, vocab


def reset_cache():
    _compiled.cache_clear()


def tag(text: str) -> dict:
    """軸カテゴリ・大分類を返す。ASCII の短い語（ld, add, iq 等）は前後が英字でないときだけ当てる。"""
    axes, intents, _ = _compiled()
    n = norm(text)
    hits = []
    for axis, cat, terms in axes:
        for t in terms:
            if t.isascii() and len(t) <= 3:
                if re.search(rf"(?<![a-z]){re.escape(t)}(?![a-z])", n):
                    hits.append((axis, cat))
                    break
            elif t in n:
                hits.append((axis, cat))
                break
    keys = {f"{a}/{c}" for a, c in hits}
    fallback = next((need for name, need in intents if name == "__fallback__"), None)
    cats = [name for name, need in intents if name != "__fallback__" and keys & need]
    # 発達特性の語だけに当たり、他の大分類に当たらないKWの受け皿（意図マップの fallback_trait_only）
    if not cats and fallback and any(a == "発達特性" for a, _ in hits):
        cats = [fallback]
    out = {"intent_category": cats or ["未分類"], "intent_subcategory": sorted(keys), "axes": hits}
    for col in set(AXIS_COLUMN.values()):
        out[col] = sorted({c for a, c in hits if AXIS_COLUMN.get(a) == col})
    return out


def known_vocab() -> list[str]:
    return _compiled()[2]


# ---------------------------------------------------------------------------
# 各ソースの読み出し
# ---------------------------------------------------------------------------
def rounds_available() -> list[int]:
    rs = set()
    for p in (HERE / "serp").glob("round*"):
        rs.add(int(p.name[5:]))
    for p in (HERE / "raw").glob("kwp_round*.jsonl"):
        rs.add(int(p.stem.replace("kwp_round", "")))
    return sorted(rs)


def iter_kwp(rnd: int | None = None) -> Iterator[dict]:
    for p in sorted((HERE / "raw").glob("kwp_round*.jsonl")):
        r = int(p.stem.replace("kwp_round", ""))
        if rnd is not None and r != rnd:
            continue
        for line in p.open(encoding="utf-8"):
            yield json.loads(line)


def iter_serp(rnd: int | None = None) -> Iterator[dict]:
    for d in sorted((HERE / "serp").glob("round*")):
        r = int(d.name[5:])
        if rnd is not None and r != rnd:
            continue
        for f in sorted(d.glob("*.json")):
            yield json.loads(f.read_text(encoding="utf-8"))


def iter_suggest(rnd: int | None = None) -> Iterator[dict]:
    for p in sorted((HERE / "suggest").glob("round*.jsonl")):
        r = int(p.stem.replace("round", ""))
        if rnd is not None and r != rnd:
            continue
        for line in p.open(encoding="utf-8"):
            yield json.loads(line)


def iter_pages(rnd: int | None = None) -> Iterator[dict]:
    for p in sorted((HERE / "pages").glob("round*.jsonl")):
        r = int(p.stem.replace("round", ""))
        if rnd is not None and r != rnd:
            continue
        for line in p.open(encoding="utf-8"):
            yield json.loads(line)


def iter_natural(rnd: int | None = None) -> Iterator[dict]:
    p = HERE / "queries_natural_language.jsonl"
    if not p.exists():
        return
    for line in p.open(encoding="utf-8"):
        j = json.loads(line)
        if rnd is None or j.get("discovered_round") == rnd:
            yield j


def url_resolver() -> dict:
    p = HERE / "url_resolve.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def urls() -> list[dict]:
    p = HERE / "urls.csv"
    return list(csv.DictReader(p.open(encoding="utf-8-sig"))) if p.exists() else []

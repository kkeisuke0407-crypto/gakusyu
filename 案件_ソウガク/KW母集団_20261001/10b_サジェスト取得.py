# -*- coding: utf-8 -*-
"""Googleの入力補完（サジェスト）を少量・間隔ありで取得する（評価はしない）。

対象：その周回のSERPクエリ・関連検索＋holes_round{n}.txt（穴埋め語）。各語について「語」「語＋空白」の2通り。
出力: suggest/round{n}.jsonl（query, input, suggestions, fetched_at）
使い方: python 10b_サジェスト取得.py 1
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
ROUND = int(sys.argv[1]) if len(sys.argv) > 1 else 1
URL = "https://suggestqueries.google.com/complete/search"


def main():
    terms = []
    for f in sorted((HERE / "serp" / f"round{ROUND}").glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        terms.append(d.get("q", ""))
        terms += d.get("related", [])
    holes = HERE / f"holes_round{ROUND}.txt"   # 穴埋め用の語（18_穴埋め.py が作る）
    if holes.exists():
        terms += [l.strip() for l in holes.open(encoding="utf-8") if l.strip()]
    terms = [t for t in dict.fromkeys(terms) if t]
    out_path = HERE / "suggest" / f"round{ROUND}.jsonl"
    done = set()
    if out_path.exists():
        done = {json.loads(l)["input"] for l in out_path.open(encoding="utf-8")}
    n = 0
    with out_path.open("a", encoding="utf-8") as out:
        for t in terms:
            for inp in (t, t + " "):
                if inp in done:
                    continue
                try:
                    r = requests.get(URL, params={"client": "firefox", "hl": "ja", "gl": "jp", "ie": "utf-8", "oe": "utf-8", "q": inp}, timeout=10)
                    r.encoding = "utf-8"
                    sugg = json.loads(r.text)[1] if r.status_code == 200 else []
                    status = r.status_code
                except Exception as exc:
                    sugg, status = [], f"error: {type(exc).__name__}"
                out.write(json.dumps(dict(query=t, input=inp, status=status, suggestions=sugg, round=ROUND,
                                          fetched_at=time.strftime("%Y-%m-%d %H:%M:%S")), ensure_ascii=False) + "\n")
                out.flush()
                n += 1
                time.sleep(1.0)
    print(f"サジェスト取得 {n} 件（対象語 {len(terms)}）")


if __name__ == "__main__":
    main()

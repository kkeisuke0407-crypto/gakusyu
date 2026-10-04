# -*- coding: utf-8 -*-
"""queries_natural_language.jsonl の intent_category / intent_subcategory を現在の意図マップで埋め直す（行は削除しない）"""
import json
import sys

import lib_soug as L

sys.stdout.reconfigure(encoding="utf-8")
p = L.HERE / "queries_natural_language.jsonl"
rows = [json.loads(l) for l in p.open(encoding="utf-8")]
for r in rows:
    t = L.tag(r["query"])
    r["intent_category"] = " | ".join(t["intent_category"])
    r["intent_subcategory"] = " | ".join(t["intent_subcategory"])
p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
print(len(rows), "未分類", sum(r["intent_category"] == "未分類" for r in rows))

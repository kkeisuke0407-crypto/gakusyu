# -*- coding: utf-8 -*-
"""意図マップへの追記（追記のみ。既存の語・カテゴリは消さない）。
入力：map_updates/round{n}.json
  {"terms": {"軸/カテゴリ": ["語", ...]},          既存カテゴリへの語の追加（無ければ新カテゴリとして作る）
   "intent_categories": {"大分類": ["軸/カテゴリ", ...]},  新しい大分類 or 既存大分類への any_axes 追加
   "note": "採否の根拠（concepts_round{n-1}.csv のどの候補から来たか）"}
使い方: python 16_意図マップ追記.py 2
"""
import json
import sys

import lib_soug as L

sys.stdout.reconfigure(encoding="utf-8")
ROUND = int(sys.argv[1])
upd = json.loads((L.HERE / "map_updates" / f"round{ROUND}.json").read_text(encoding="utf-8"))
m = L.load_map()
new_cats, new_terms, new_intents = [], 0, []
for key, terms in upd.get("terms", {}).items():
    axis, cat = key.split("/", 1)
    cats = m["axes"].setdefault(axis, {})
    if cat not in cats:
        cats[cat] = {"terms": [], "round": ROUND, "source": upd.get("note", "")}
        new_cats.append(key)
    have = set(cats[cat]["terms"])
    for t in terms:
        if t not in have:
            cats[cat]["terms"].append(t)
            have.add(t)
            new_terms += 1
for name, axes in upd.get("intent_categories", {}).items():
    if name not in m["intent_categories"]:
        m["intent_categories"][name] = {"any_axes": [], "round": ROUND}
        new_intents.append(name)
    for a in axes:
        if a not in m["intent_categories"][name]["any_axes"]:
            m["intent_categories"][name]["any_axes"].append(a)
m["history"].append({"round": ROUND, "new_intent_categories": new_intents, "new_subcategories": new_cats,
                     "new_terms": new_terms, "source": upd.get("note", "")})
(L.HERE / "00_意図マップ.json").write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"round{ROUND}: 新大分類 {len(new_intents)} {new_intents}\n新サブカテゴリ {len(new_cats)} {new_cats}\n追加語 {new_terms}")

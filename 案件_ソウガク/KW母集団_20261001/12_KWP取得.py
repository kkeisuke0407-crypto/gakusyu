# -*- coding: utf-8 -*-
"""KWP の4種seed（KeywordSeed / UrlSeed / KeywordAndUrlSeed / SiteSeed）を回す（READ ONLY・再開可能）。

入力: seeds_round{n}.json
  {"keyword_groups": [{"group": "発達障害×家庭教師", "keywords": [5〜10語]}],
   "urls":   [{"url": "...", "group": "競合LP", "note": "..."}],
   "kw_url": [{"group": "...", "keywords": [...], "url": "..."}],
   "sites":  [{"site": "example.com", "group": "..."}]}
出力: raw/kwp_round{n}.jsonl（1リクエスト1行・応答をそのまま）, raw/requests.jsonl
地域：日本全国・日本語・Google検索。limit=0（全ページ）・force_refresh。数値は加工しない。
使い方: python 12_KWP取得.py 1
"""
from __future__ import annotations

import json
import sys
import time
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
ROUND = int(sys.argv[1]) if len(sys.argv) > 1 else 1
sys.path.insert(0, r"C:\Users\user\Documents\google-ads-operations\kwp-mcp\src")
from kwp_mcp.config import Settings      # noqa: E402
from kwp_mcp.server import Context       # noqa: E402

CUSTOMER_ID = "6661622672"
GEO = dict(country="JP", language="ja", network="GOOGLE_SEARCH")


def mdict(gm):
    return dict(avg_monthly_searches=gm.avg_monthly_searches, competition=gm.competition,
                competition_index=gm.competition_index, low_bid=gm.low_top_of_page_bid,
                high_bid=gm.high_top_of_page_bid, average_cpc=gm.average_cpc,
                monthly=[(m.year, m.month_number, m.monthly_searches) for m in gm.monthly_search_volumes])


def jobs_of(spec: dict) -> list[dict]:
    jobs = []
    for g in spec.get("keyword_groups", []):
        jobs.append(dict(id=f"KW:{g['group']}", seed_type="KeywordSeed", seed_group=g["group"],
                         keywords=g["keywords"], url=None, site=None))
    for u in spec.get("urls", []):
        jobs.append(dict(id=f"URL:{u['url']}", seed_type="UrlSeed", seed_group=u.get("group", ""),
                         keywords=[], url=u["url"], site=None))
    for k in spec.get("kw_url", []):
        jobs.append(dict(id=f"KWURL:{k['group']}|{k['url']}", seed_type="KeywordAndUrlSeed",
                         seed_group=k["group"], keywords=k["keywords"], url=k["url"], site=None))
    for s in spec.get("sites", []):
        jobs.append(dict(id=f"SITE:{s['site']}", seed_type="SiteSeed", seed_group=s.get("group", ""),
                         keywords=[], url=None, site=s["site"]))
    return jobs


def main():
    spec = json.loads((HERE / f"seeds_round{ROUND}.json").read_text(encoding="utf-8"))
    planner = Context(Settings.load()).planner
    out_path = HERE / "raw" / f"kwp_round{ROUND}.jsonl"
    done = set()
    if out_path.exists():
        for line in out_path.open(encoding="utf-8"):
            j = json.loads(line)
            if not j.get("error"):
                done.add(j["id"])
    jobs = [j for j in jobs_of(spec) if j["id"] not in done]
    print(f"[round{ROUND}] jobs {len(jobs_of(spec))} / 残り {len(jobs)}", flush=True)
    with out_path.open("a", encoding="utf-8") as f:
        for i, j in enumerate(jobs, 1):
            for attempt in range(3):
                try:
                    out = planner.generate_keyword_ideas(
                        customer_id=CUSTOMER_ID, seed_keywords=j["keywords"] or None, seed_url=j["url"],
                        seed_site=j["site"], limit=0, include_average_cpc=True, force_refresh=True, **GEO)
                    recs = [dict(keyword=r.original_keyword, metrics=mdict(r.google_metrics)) for r in out["records"]]
                    total, err = out.get("total_size"), None
                    break
                except Exception as exc:
                    recs, total, err = [], None, f"{type(exc).__name__}: {str(exc)[:200]}"
                    if "429" in err or "Exhausted" in err:
                        time.sleep(20 * (attempt + 1))
                        continue
                    break
            row = dict(**j, round=ROUND, fetched_at=time.strftime("%Y-%m-%d %H:%M:%S"), error=err,
                       total_size=total, record_count=len(recs), records=recs)
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            f.flush()
            with (HERE / "raw" / "requests.jsonl").open("a", encoding="utf-8") as lg:
                lg.write(json.dumps(dict(round=ROUND, id=j["id"], seed_type=j["seed_type"], records=len(recs),
                                         total_size=total, error=err, at=row["fetched_at"]),
                                    ensure_ascii=False) + "\n")
            if i % 20 == 0 or err:
                print(f"  {i}/{len(jobs)} {j['id'][:50]:<50} {len(recs):>6} {err or ''}", flush=True)
            time.sleep(1.5)
    print("完了", flush=True)


if __name__ == "__main__":
    main()

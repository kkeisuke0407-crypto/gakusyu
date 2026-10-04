# -*- coding: utf-8 -*-
"""SERPの結果ページ・競合サイトの下層ページを取得し、title/H1〜H3/FAQ を抜き出す（評価はしない）。

  1. serp/round{n}/*.json の自然検索・広告のURL（Googleの転送URL）を実URLへ解決（url_resolve.json にキャッシュ）
  2. urls.csv に追記（発見クエリ・順位・種別・ページ種別）
  3. 各ドメインのトップページを取得し、内部リンクから重要な下層ページ（発達障害/ADHD/ASD/LD/小中高/料金/
     無料体験/FAQ/コラム/口コミ 等）を最大 SUBPAGES_PER_DOMAIN 件まで追加
  4. 全ページの title・H1〜H3・FAQ（dt/summary/Q.〜/？で終わる見出し）を pages/round{n}.jsonl に保存
  5. PAA・FAQ質問・Q&Aサイトのタイトルなど検索者の自然文を queries_natural_language.jsonl に追記

robots.txt を確認し、取得間隔は1秒。取得できなかったページも理由つきで記録する。
使い方: python 11_ページ取得.py 1   （周回番号）
"""
from __future__ import annotations

import csv
import json
import threading
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import re
import sys
import time
import urllib.robotparser
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
ROUND = int(sys.argv[1]) if len(sys.argv) > 1 else 1
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
S = requests.Session()
S.headers.update({"User-Agent": UA, "Accept-Language": "ja,en;q=0.5"})
SUBPAGES_PER_DOMAIN = 12
# 下層ページとして拾うリンク（URL・リンク文言のどちらかに当たれば）
SUBPAGE_RX = re.compile(r"発達|adhd|asd|ld|学習障|グレー|自閉|不登校|hattatsu|gakushu|grey|gray|special|support"
                        r"|小学|中学|高校|elementary|junior|high|受験|price|ryokin|料金|fee|cost|course|コース"
                        r"|trial|taiken|体験|無料|faq|よくある|question|column|コラム|blog|article|voice|口コミ|体験談"
                        r"|review|実績|case|results", re.I)
# トップ・下層の展開対象にしない大規模/汎用ドメイン（ページ自体は取得する）
NO_EXPAND = re.compile(r"google\.|youtube\.|amazon\.|rakuten\.|wikipedia\.|chiebukuro|yahoo\.co\.jp|ameblo|note\.com"
                       r"|instagram|twitter|x\.com|facebook|tiktok|hatena|livedoor|goo\.ne\.jp|nhk\.or\.jp|go\.jp"
                       r"|lg\.jp|ac\.jp|mhlw|mext|pref\.|city\.")


class Extract(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cur = None
        self.buf = []
        self.out = {"title": "", "h1": [], "h2": [], "h3": [], "faq": [], "links": []}

    def handle_starttag(self, tag, attrs):
        if tag in ("title", "h1", "h2", "h3", "dt", "summary"):
            self.cur, self.buf = tag, []
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.out["links"].append([href, ""])
                self._a = True

    def handle_endtag(self, tag):
        if tag == self.cur:
            text = re.sub(r"\s+", " ", "".join(self.buf)).strip()
            if text:
                if tag == "title":
                    self.out["title"] = text
                elif tag in ("dt", "summary"):
                    self.out["faq"].append(text)
                else:
                    self.out[tag].append(text)
            self.cur = None
        if tag == "a":
            self._a = False

    def handle_data(self, data):
        if self.cur:
            self.buf.append(data)
        if getattr(self, "_a", False) and self.out["links"]:
            self.out["links"][-1][1] += data.strip()


def resolve(u: str, cache: dict) -> str:
    if "google." not in urlparse(u).netloc or "/goto" not in u and "/url" not in u:
        return u
    if u in cache:
        return cache[u]
    try:
        r = S.get(u, allow_redirects=False, timeout=15)
        real = r.headers.get("location") or u
    except Exception:
        real = u
    cache[u] = real
    time.sleep(0.3)
    return real


ROBOTS: dict[str, urllib.robotparser.RobotFileParser | None] = {}


def allowed(url: str) -> bool:
    p = urlparse(url)
    base = f"{p.scheme}://{p.netloc}"
    if base not in ROBOTS:
        rp = urllib.robotparser.RobotFileParser()
        try:
            r = S.get(base + "/robots.txt", timeout=10)
            rp.parse(r.text.splitlines() if r.status_code == 200 else [])
            ROBOTS[base] = rp
        except Exception:
            ROBOTS[base] = None
    rp = ROBOTS[base]
    return True if rp is None else rp.can_fetch(UA, url)


def fetch(url: str) -> dict:
    rec = {"url": url, "round": ROUND, "fetched_at": time.strftime("%Y-%m-%d %H:%M:%S")}
    if not allowed(url):
        return {**rec, "status": "robots_disallow"}
    try:
        r = S.get(url, timeout=20)
        rec["status"] = r.status_code
        rec["final_url"] = r.url
        if r.status_code != 200 or "html" not in r.headers.get("content-type", ""):
            return rec
        r.encoding = r.apparent_encoding if r.encoding in (None, "ISO-8859-1") else r.encoding
        ex = Extract()
        ex.feed(r.text)
        o = ex.out
        # 「Q.」「Q：」で始まる段落・？で終わる見出しもFAQとして拾う
        qs = re.findall(r"(?:Q[\.．:：]|質問[:：])\s*([^<\n]{6,80}?[？\?])", re.sub(r"<[^>]+>", "\n", r.text))
        faq = list(dict.fromkeys(o["faq"] + qs + [h for h in o["h2"] + o["h3"] if h.endswith(("？", "?"))]))
        rec.update(title=o["title"], h1=o["h1"][:10], h2=o["h2"][:60], h3=o["h3"][:120], faq=faq[:80],
                   links=[[urljoin(r.url, h), t[:60]] for h, t in o["links"]])
    except Exception as exc:
        rec["status"] = f"error: {type(exc).__name__}"
    return rec


def page_kind(url: str, text: str = "") -> str:
    s = (url + " " + text).lower()
    for kind, rx in [("料金", r"price|ryokin|料金|fee|cost"), ("無料体験", r"trial|taiken|体験|無料"),
                     ("FAQ", r"faq|よくある|question"), ("口コミ・体験談", r"voice|口コミ|体験談|review|実績|case"),
                     ("コラム", r"column|コラム|blog|article|media|magazine"),
                     ("発達障害向け", r"発達|adhd|asd|ld|学習障|グレー|自閉|hattatsu|gakushu"),
                     ("不登校向け", r"不登校|futoko"), ("学年向け", r"小学|中学|高校|elementary|junior|high"),
                     ("受験", r"受験|exam")]:
        if re.search(rx, s):
            return kind
    return "トップ" if urlparse(url).path in ("", "/") else "その他"


def main():
    serp_dir = HERE / "serp" / f"round{ROUND}"
    cache_path = HERE / "url_resolve.json"
    cache = json.loads(cache_path.read_text(encoding="utf-8")) if cache_path.exists() else {}
    urls_csv = HERE / "urls.csv"
    known = set()
    if urls_csv.exists():
        known = {r["url"] for r in csv.DictReader(urls_csv.open(encoding="utf-8-sig"))}
    nl_path = HERE / "queries_natural_language.jsonl"
    new_rows, nl = [], []

    for f in sorted(serp_dir.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        q = d.get("q", "")
        for kind in ("organic", "ads"):
            for rank, r in enumerate(d.get(kind, []), 1):
                real = resolve(r.get("url", ""), cache)
                if not real or real in known:
                    continue
                known.add(real)
                new_rows.append(dict(url=real, domain=urlparse(real).netloc, serp_title=r.get("title", ""),
                                     found_query=q, rank=rank, result_type=kind, page_kind=page_kind(real, r.get("title", "")),
                                     source="serp", round=ROUND))
                if "chiebukuro" in real or "detail.chiebukuro" in real or "komachi" in real:
                    nl.append(dict(query=r.get("title", ""), source="Q&A_title", parent_query=q, source_url=real,
                                   discovered_round=ROUND))
        for p in d.get("paa", []):
            if p != q:
                nl.append(dict(query=p, source="Google_PAA", parent_query=q, source_url="", discovered_round=ROUND))
    cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"SERP由来の新規URL {len(new_rows)}", flush=True)

    # ---- ページ取得：ドメインごとに順番（間隔1秒）・ドメイン間は並行（最大8） ----
    pages_path = HERE / "pages" / f"round{ROUND}.jsonl"
    links_path = HERE / "pages" / f"links_round{ROUND}.jsonl"
    done = set()
    if pages_path.exists():
        done = {json.loads(l)["url"] for l in pages_path.open(encoding="utf-8")}
    lock = threading.Lock()
    out = pages_path.open("a", encoding="utf-8")
    lout = links_path.open("a", encoding="utf-8")

    def run_domain(urls_of_domain):
        got = []
        for url in urls_of_domain:
            with lock:
                if url in done:
                    continue
                done.add(url)
            rec = fetch(url)
            with lock:
                out.write(json.dumps({k: v for k, v in rec.items() if k != "links"}, ensure_ascii=False) + "\n")
                out.flush()
                if rec.get("links"):
                    lout.write(json.dumps({"url": url, "links": rec["links"]}, ensure_ascii=False) + "\n")
                    lout.flush()
                for qtext in rec.get("faq", []):
                    nl.append(dict(query=qtext, source="Competitor_FAQ", parent_query="", source_url=url,
                                   discovered_round=ROUND))
            got.append(rec)
            time.sleep(1.0)
        return got

    def run_all(url_list, label):
        by_dom = defaultdict(list)
        for u in url_list:
            by_dom[urlparse(u).netloc].append(u)
        with ThreadPoolExecutor(max_workers=8) as ex:
            list(ex.map(run_domain, by_dom.values()))
        print(f"  {label}: {len(url_list)} URL / {len(by_dom)} ドメイン 完了（取得済み計 {len(done)}）", flush=True)

    # A. SERP由来のURL（＋各ドメインのトップ）
    serp_urls = [r["url"] for r in new_rows] or [r["url"] for r in csv.DictReader(urls_csv.open(encoding="utf-8-sig"))
                                                if r.get("round") == str(ROUND)] if urls_csv.exists() else [r["url"] for r in new_rows]
    tops = []
    for u in serp_urls:
        p = urlparse(u)
        if not NO_EXPAND.search(p.netloc):
            tops.append(f"{p.scheme}://{p.netloc}/")
    run_all(list(dict.fromkeys(serp_urls + tops)), "SERP由来＋トップ")

    # B. 下層展開（取得済みページのリンクから、ドメインごとに最大 SUBPAGES_PER_DOMAIN 件）
    lout.flush()
    links_by_dom = defaultdict(list)
    for line in links_path.open(encoding="utf-8"):
        j = json.loads(line)
        links_by_dom[urlparse(j["url"]).netloc] += j["links"]
    sub = []
    for dom, links in links_by_dom.items():
        if NO_EXPAND.search(dom):
            continue
        cands = []
        for href, text in links:
            pu = urlparse(href)
            clean = href.split("#")[0]
            if pu.netloc != dom or pu.scheme not in ("http", "https") or clean in done or clean in cands:
                continue
            if SUBPAGE_RX.search(pu.path + " " + text):
                cands.append(clean)
        for c in cands[:SUBPAGES_PER_DOMAIN]:
            sub.append(c)
            if c not in known:
                known.add(c)
                new_rows.append(dict(url=c, domain=dom, serp_title="", found_query="", rank="",
                                     result_type="subpage", page_kind=page_kind(c), source="下層展開", round=ROUND))
    run_all(sub, "下層ページ")
    out.close()
    lout.close()

    write_header = not urls_csv.exists()
    with urls_csv.open("a", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["url", "domain", "serp_title", "found_query", "rank", "result_type",
                                          "page_kind", "source", "round"])
        if write_header:
            w.writeheader()
        w.writerows(new_rows)
    with nl_path.open("a", encoding="utf-8") as f:
        seen = set()
        for r in nl:
            key = (r["query"], r["source"], r["source_url"])
            if r["query"] and key not in seen:
                seen.add(key)
                f.write(json.dumps(dict(r, intent_category="", intent_subcategory=""), ensure_ascii=False) + "\n")
    print(f"urls.csv +{len(new_rows)} / pages {len(done)} / 自然文 +{len(nl)}", flush=True)


if __name__ == "__main__":
    main()

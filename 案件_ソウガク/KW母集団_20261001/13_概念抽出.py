# -*- coding: utf-8 -*-
"""未知概念の候補を4種類で抽出する（候補を出すだけ。意図マップへの追加は人が読んで判断する）。

  1. 未知語・未知n-gram：意図マップのどの語彙にも当たらないトークン／語の並び
  2. 新しい組み合わせ：既知語だけでできているが、coverage.csv に無い軸カテゴリの組み合わせ
  3. 新しい検索シチュエーション：時期・場面・節目を表す語を含み、意図マップの「シチュエーション」に当たらないもの
  4. 新しい行動・出来事・困り方：出来事・困り方を表す述語を含み、意図マップに無いもの
入力：その周回のKWP・関連検索・サジェスト・PAA/FAQ自然文・競合見出しの全件（KWは削除しない）
出力：concepts_round{n}.csv（type, candidate, count, total_volume, examples, sources）
使い方: python 13_概念抽出.py 1
"""
from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict

import lib_soug as L

sys.stdout.reconfigure(encoding="utf-8")
ROUND = int(sys.argv[1]) if len(sys.argv) > 1 else 1

# 一般語（どの意図にも当たらなくても概念ではない語）。ここに入れても出力からKWは消えない
STOP = set("""の に を は が で と も へ や か な て た し ない する いる ある こと もの 方 人 子 子供 子ども こども
とは について 方法 やり方 仕方 なぜ どう どうして 何 いつ どこ ため とき 時 中 前 後 年 歳 月 日 等 など 版 最新
2024 2025 2026 おすすめ 比較 ランキング 口コミ 評判 料金 費用 無料 塾 家庭教師 勉強 学習 発達 障害 発達障害 小学生
中学生 高校生 オンライン""".split())
SITUATION = re.compile(r"前|後|直前|時期|から|まで|中に|とき|時に|場合|頃|ころ|以降|入学|卒業|進級|学期|休み|休校"
                       r"|受験期|年長|年中|〜|復帰|再開|始め|初めて")
EVENT = re.compile(r"(られた|された|れた|しまった|てしまう|できない|しない|ない|たい|嫌が|嫌い|泣く|泣き|怒る|怒り|拒否"
                   r"|やめ|辞め|断ら|続かない|行かない|行けない|サボ|遅れ|落ち|下が|荒れ|暴れ|逃げ|疲れ|悩む|悩み|困る"
                   r"|困って|不安|心配|迷う|わからない|分からない)")


def texts_of_round(rnd: int):
    """(text, source, volume, tokens) を返す。tokens はKWPの分かち書きをそのまま使う"""
    for j in L.iter_kwp(rnd):
        for r in j.get("records", []):
            v = r["metrics"].get("avg_monthly_searches") or 0
            yield r["keyword"], f"KWP_{j['seed_type']}", v, r["keyword"].split()
    for d in L.iter_serp(rnd):
        for t in d.get("related", []):
            yield t, "Google_related_search", 0, t.split()
    for s in L.iter_suggest(rnd):
        for t in s.get("suggestions", []):
            yield t, "Google_suggest", 0, t.split()
    for n in L.iter_natural(rnd):
        yield n["query"], n["source"], 0, None
    for p in L.iter_pages(rnd):
        for h in (p.get("h1") or []) + (p.get("h2") or []):
            yield h, "Google_competitor", 0, None


def main():
    vocab = L.known_vocab()
    coverage = set()
    try:
        # 軸の並び順に関係なく照合するため、組み合わせは集合で持つ
        coverage = {frozenset(r["combination"].split(" × "))
                    for r in csv.DictReader((L.HERE / "coverage.csv").open(encoding="utf-8-sig"))}
    except FileNotFoundError:
        pass

    unknown = defaultdict(lambda: [0, 0, [], set()])      # token -> [count, volume, examples, sources]
    combos = defaultdict(lambda: [0, 0, [], set()])
    situ = defaultdict(lambda: [0, 0, [], set()])
    event = defaultdict(lambda: [0, 0, [], set()])

    def add(bucket, key, text, src, vol):
        b = bucket[key]
        b[0] += 1
        b[1] += vol or 0
        if len(b[2]) < 5 and text not in b[2]:
            b[2].append(text)
        b[3].add(src)

    for text, src, vol, toks in texts_of_round(ROUND):
        n = L.norm(text)
        t = L.tag(text)
        # 1. 未知トークン（KWPなど分かち書きのある語）／未知の連続部分（自然文・見出し）
        if toks:
            for tok in toks:
                k = L.norm(tok)
                if len(k) < 2 or k in STOP or k.isdigit() or any(v in k or k in v for v in vocab if len(v) >= 2):
                    continue
                add(unknown, k, text, src, vol)
        else:
            rest = n
            for v in vocab:
                if len(v) >= 2:
                    rest = rest.replace(v, "｜")
            for seg in re.split(r"[｜、。・\s「」『』（）()！!？?：:]+", rest):
                if 3 <= len(seg) <= 12 and seg not in STOP:
                    add(unknown, seg, text, src, vol)
        # 2. 新しい組み合わせ（2軸以上・coverage に無いペア）
        cats = sorted({f"{a}/{c}" for a, c in t["axes"]})
        for i in range(len(cats)):
            for j in range(i + 1, len(cats)):
                if cats[i].split("/")[0] == cats[j].split("/")[0]:
                    continue
                key = f"{cats[i]} × {cats[j]}"
                if frozenset((cats[i], cats[j])) not in coverage:
                    add(combos, key, text, src, vol)
        # 3. シチュエーション（意図マップのシチュエーション軸に当たらないもの）
        n_situ = n.replace("放課後", "")
        if SITUATION.search(n_situ) and not any(a == "シチュエーション・出来事" for a, _ in t["axes"]):
            m = SITUATION.search(n_situ)
            n = n_situ
            add(situ, n[max(0, m.start() - 6): m.end() + 4], text, src, vol)
        # 4. 行動・出来事・困り方（意図マップに当たらない述語）
        for m in EVENT.finditer(n):
            frag = n[max(0, m.start() - 6): m.end()]
            if not any(v in frag for v in vocab if len(v) >= 3 and v.endswith(m.group(0)[-2:])):
                add(event, frag, text, src, vol)

    rows = []
    for typ, bucket, top in (("1_未知語", unknown, 400), ("2_新しい組み合わせ", combos, 300),
                             ("3_シチュエーション", situ, 200), ("4_行動・出来事・困り方", event, 300)):
        items = sorted(bucket.items(), key=lambda kv: (-kv[1][0], -kv[1][1]))[:top]
        for k, (cnt, vol, ex, srcs) in items:
            rows.append(dict(type=typ, candidate=k, count=cnt, total_volume=vol, examples=" / ".join(ex),
                             sources=" | ".join(sorted(srcs)), decision="", note=""))
    out = L.HERE / f"concepts_round{ROUND}.csv"
    with out.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(Counter(r["type"] for r in rows), "→", out.name)


if __name__ == "__main__":
    main()

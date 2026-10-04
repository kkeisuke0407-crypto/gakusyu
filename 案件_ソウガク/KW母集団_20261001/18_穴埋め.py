# -*- coding: utf-8 -*-
"""coverage.csv の「発見KW 0〜4件」の主要2軸・3軸の組み合わせ（＝探索が薄い意図）だけを、次の取得対象にする。
既に十分な組み合わせ（発見5件以上）は再取得しない。件数を増やすことは目的にしない。

出力
  holes_round{n}.csv  : combination, discovered_keywords_count, query（代表語の掛け合わせ）
  holes_round{n}.txt  : サジェスト取得用（10b_サジェスト取得.py が読む）
  seeds_round{n}.json : KWP KeywordSeed（軸の組ごとに 5〜10 語）
使い方: python 18_穴埋め.py 2
"""
import csv
import json
import sys
from collections import defaultdict

import lib_soug as L

sys.stdout.reconfigure(encoding="utf-8")
ROUND = int(sys.argv[1])
THIN = 5
# カテゴリの代表語（検索者が実際に打つ形に近い語）。代表語が無いカテゴリは穴埋め対象にしない
REP = {
    "発達障害": "発達障害", "グレーゾーン": "グレーゾーン", "ADHD": "ADHD", "ASD": "自閉症", "LD・学習障害": "学習障害",
    "境界知能・知的": "境界知能", "その他の特性": "HSC",
    "小学生": "小学生", "中学生": "中学生", "高校生": "高校生", "受験生": "受験", "不登校": "不登校",
    "幼児・未就学": "幼児", "学校種別": "支援学級", "性別・本人": "息子", "大人・大学生（本人）": "大人",
    "勉強できない・しない": "勉強しない", "勉強方法": "勉強方法", "集中・注意": "集中できない",
    "宿題・テスト・成績": "テスト", "授業・学校についていけない": "授業 ついていけない",
    "記憶・読み書き計算": "読み書き", "教科": "算数", "受験・進路": "高校受験", "模試・講習": "夏期講習",
    "学び直し・遅れを取り戻す": "勉強 遅れ 取り戻す", "特性と学力・伸びしろ": "勉強 できる",
    "家庭教師": "家庭教師", "オンライン家庭教師・オンライン塾": "オンライン家庭教師", "塾・個別指導": "塾",
    "発達障害専門・支援": "学習支援", "療育・福祉サービス": "放課後等デイサービス", "フリースクール・居場所": "フリースクール",
    "教材・通信教育・アプリ": "通信教育", "医療・診断": "病院", "知能検査・検査結果": "WISC",
    "習い事・トレーニング": "習い事", "合理的配慮・学校との連携": "合理的配慮", "相談・カウンセリング": "相談",
    "ブランド・指名（塾・家庭教師）": "トライ",
    "比較・おすすめ": "おすすめ", "評判・口コミ": "口コミ", "料金・費用": "料金", "体験・申込・相談": "無料体験",
    "合わない・乗り換え": "合わない", "サービス詳細・利用条件": "対象年齢",
    "親が教えられない": "親 教えられない", "家で勉強しない": "家で勉強しない", "塾が合わない・集団が苦手": "集団塾 合わない",
    "専門の先生を探す": "理解のある先生", "将来・進路不安": "将来 不安", "ゲーム・スマホ・生活・反抗": "ゲーム",
    "行動・情緒・対人の困りごと": "癇癪", "親自身・子育ての辛さ": "子育て 辛い",
    "診断・気づき": "診断された", "断られた・合わなかった": "断られた", "時期・節目": "入学前",
    "学級・学校の移行・転籍": "支援級から通常級", "就学準備・就学先": "就学準備",
}


def main():
    rows = list(csv.DictReader((L.HERE / "coverage.csv").open(encoding="utf-8-sig")))
    holes = []
    for r in rows:
        n = int(r["discovered_keywords_count"])
        if n >= THIN:
            continue
        cats = [c.split("/", 1)[1] for c in r["combination"].split(" × ")]
        if not all(c in REP for c in cats):
            continue
        q = " ".join(REP[c] for c in cats)
        holes.append(dict(combination=r["combination"], discovered_keywords_count=n, query=q))
    with (L.HERE / f"holes_round{ROUND}.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(holes[0].keys()))
        w.writeheader()
        w.writerows(holes)
    (L.HERE / f"holes_round{ROUND}.txt").write_text("\n".join(h["query"] for h in holes) + "\n", encoding="utf-8")
    # KeywordSeed：組み合わせの軸ペア（例：発達特性×検討行動）ごとに、同じ特性の語を 5〜10 語ずつまとめる
    groups = defaultdict(list)
    for h in holes:
        axes = [c.split("/", 1)[0] for c in h["combination"].split(" × ")]
        head = h["combination"].split(" × ")[0].split("/", 1)[1]
        groups[f"穴埋め:{'×'.join(axes)}:{head}"].append(h["query"])
    kg = []
    for g, qs in groups.items():
        qs = list(dict.fromkeys(qs))
        for i in range(0, len(qs), 10):
            kg.append(dict(group=f"{g}#{i // 10 + 1}", keywords=qs[i:i + 10]))
    seeds = L.HERE / f"seeds_round{ROUND}.json"
    spec = json.loads(seeds.read_text(encoding="utf-8")) if seeds.exists() else {}
    spec["keyword_groups"] = kg
    seeds.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"穴（発見{THIN}件未満で代表語あり）{len(holes)} / KeywordSeedグループ {len(kg)}")


if __name__ == "__main__":
    main()

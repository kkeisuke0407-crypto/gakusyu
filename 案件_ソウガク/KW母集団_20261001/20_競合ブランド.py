# -*- coding: utf-8 -*-
"""競合・代替サービスのブランド一覧（competitor_brands.csv）を作る。評価・優先順位は付けない。

候補は既存データ（意図マップのブランド語彙・urls.csv のドメインとサイト名・SERP・競合ページ見出し・
keywords_unique.csv のブランド・指名検索カテゴリ）から人が読んで拾ったもの。
各ブランドについて、どのデータに出ていたかを discovery_source に機械的に記録する。
brand_alias の先頭から SEARCH_FORMS 個を「検索形（ブランド×修飾語の掛け合わせに使う表記）」とする。
出力: competitor_brands.csv（1行=1表記。brand_name・normalized_brand_name・brand_alias・alias_type・
      use_in_matrix・domain・service_type・discovery_source）
"""
import csv
import glob
import json
import sys

import lib_soug as L

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(10 ** 8)
SEARCH_FORMS = 2

# brand_name, [表記（検索形を先頭に）], domain（既存データで観測したものだけ）, service_type
BRANDS = [
    # 家庭教師
    ("家庭教師のトライ", ["トライ", "家庭教師のトライ", "家庭教師 トライ", "try"], "", "家庭教師"),
    ("個別教室のトライ", ["個別教室のトライ", "トライ 個別", "トライ 塾"], "", "個別指導塾"),
    ("トライのオンライン個別指導塾", ["トライ オンライン", "トライのオンライン個別指導塾"], "www.try-online.jp", "オンライン塾"),
    ("トライ式高等学院", ["トライ式高等学院", "トライ 高等学院"], "", "通信制高校サポート校"),
    ("個別指導塾トライプラス", ["トライプラス", "トライ プラス 塾"], "", "個別指導塾"),
    ("オンラインプロ教師のメガスタ", ["メガスタ", "メガスタ オンライン"], "", "オンライン家庭教師"),
    ("家庭教師のあすなろ", ["あすなろ", "家庭教師のあすなろ", "家庭教師 あすなろ"], "www.asunaro-kk.com / www.seisekiup.net", "家庭教師"),
    ("家庭教師のノーバス", ["ノーバス", "家庭教師のノーバス", "nohvas", "個別指導塾ノーバス", "家庭教師ノーバス"], "www.nohvas.com", "家庭教師"),
    ("家庭教師のランナー", ["家庭教師のランナー", "ランナー 家庭教師"], "k-runner.co.jp", "家庭教師"),
    ("家庭教師ファースト", ["家庭教師ファースト", "家庭教師のファースト"], "www.kyoushi1.net", "家庭教師"),
    ("家庭教師のサクシード", ["サクシード", "家庭教師のサクシード"], "www.benkyo.co.jp", "家庭教師"),
    ("学研の家庭教師", ["学研の家庭教師", "学研 家庭教師"], "www.kame.co.jp", "家庭教師"),
    ("家庭教師のガンバ", ["家庭教師のガンバ", "ガンバ 家庭教師"], "", "家庭教師"),
    ("家庭教師のやる気アシスト", ["やる気アシスト", "家庭教師のやる気アシスト"], "www.yaruki-assist.com", "家庭教師"),
    ("家庭教師のマスター", ["家庭教師のマスター", "マスター 家庭教師"], "www.u-master.net", "家庭教師"),
    ("全国家庭教師協会", ["全国家庭教師協会", "家庭教師協会"], "kateikyoushi-pro.com", "家庭教師"),
    ("家庭教師の銀河", ["家庭教師の銀河", "銀河 家庭教師"], "", "家庭教師"),
    ("家庭教師アカデミー", ["家庭教師アカデミー"], "", "家庭教師"),
    ("TOS家庭教師センター", ["TOS 家庭教師", "TOS家庭教師センター"], "www.tos-kc.com / tos-kc1.com", "家庭教師"),
    ("家庭教師のコーチング1", ["コーチング1", "家庭教師のコーチング1", "コーチングワン"], "www.coaching01.com / www.juku-coaching01.com", "発達障害専門 家庭教師"),
    ("プロ家庭教師のジャンプ", ["家庭教師のジャンプ", "ジャンプ 家庭教師", "jump 家庭教師"], "www.jump-japan.co.jp", "発達障害専門 家庭教師"),
    ("メガジュン", ["メガジュン", "プロ家庭教師 メガジュン"], "pro-megajun.com", "発達障害専門 家庭教師"),
    ("キズキプロ家庭教師", ["キズキプロ家庭教師", "キズキ 家庭教師"], "tokyo-yagaku.jp", "不登校・発達障害対応 家庭教師"),
    ("ティントル", ["ティントル", "tintle"], "tintle.net", "不登校専門 家庭教師"),
    ("ウォウフル", ["ウォウフル", "wowfull"], "wowfull.jp", "不登校向け オンライン教室"),
    # オンライン家庭教師・オンライン塾
    ("まなぶてらす", ["まなぶてらす", "マナブテラス", "まなぶ てらす", "学ぶテラス"], "www.manatera.com", "オンライン家庭教師"),
    ("マナリンク", ["マナリンク", "manalink", "マナ リンク"], "manalink.jp", "オンライン家庭教師"),
    ("オンライン家庭教師GIPS", ["GIPS", "ジップス 家庭教師", "GIPS 家庭教師"], "gips-kateikyosi.com", "オンライン家庭教師"),
    ("オンライン個別指導塾リバランス", ["リバランス", "リバランス 塾"], "reba1ance.com", "オンライン塾"),
    ("Preステップオンライン", ["Preステップ", "プレステップ オンライン"], "prestep-online.com", "オンライン塾"),
    # 個別指導塾
    ("個別指導の明光義塾", ["明光義塾", "明光"], "", "個別指導塾"),
    ("東京個別指導学院", ["東京個別指導学院", "東京個別"], "", "個別指導塾"),
    ("ITTO個別指導学院", ["itto", "イットー", "itto個別指導学院", "いっとー"], "", "個別指導塾"),
    ("スクールIE", ["スクールie", "スクールIE", "やる気スイッチ", "ieスクール", "すくーるいえ", "スクールアイイー"], "", "個別指導塾"),
    ("ナビ個別指導学院", ["ナビ個別指導学院", "ナビ個別", "ナビこべつ", "個別指導学院ナビ"], "", "個別指導塾"),
    ("栄光の個別ビザビ", ["ビザビ", "栄光ビザビ"], "", "個別指導塾"),
    ("個別指導Axis", ["アクシス 塾", "axis 個別指導"], "", "個別指導塾"),
    ("森塾", ["森塾"], "", "個別指導塾"),
    ("TOMAS", ["トーマス 塾", "tomas"], "", "個別指導塾"),
    ("武田塾", ["武田塾"], "", "個別指導塾"),
    ("フリーステップ", ["フリーステップ"], "", "個別指導塾"),
    ("京進スクール・ワン", ["スクールワン", "京進スクールワン"], "", "個別指導塾"),
    ("ECCベストワン", ["ベストワン", "ecc ベストワン", "ザ ベストワン"], "", "個別指導塾"),
    ("キズキ共育塾", ["キズキ共育塾", "キズキ", "キズキ教育塾", "キズキ 教育 塾"], "kizuki.or.jp", "不登校・中退向け 個別指導塾"),
    ("キズキビジネスカレッジ", ["キズキビジネスカレッジ"], "", "就労移行支援"),
    ("個別指導塾スタディホップ", ["スタディホップ", "studyhop"], "studyhop.poka-step.jp", "発達支援児向け 個別指導塾"),
    ("さくらOne個別指導塾", ["さくらone", "さくらOne個別指導塾"], "hachiojisakura.com", "個別指導塾"),
    ("はなたに塾", ["はなたに塾"], "hanatanijuku.com", "個別指導塾"),
    ("四谷学院（療育・発達支援）", ["四谷学院 療育", "四谷学院 発達支援"], "yotsuyagakuin-ryoiku.com", "発達障害 療育・学習支援"),
    # 発達障害支援・療育・居場所
    ("LITALICOジュニア", ["リタリコジュニア", "litalicoジュニア", "リタリコ", "リタリコ パーソナル", "リタ リコ ジュニア"], "junior.litalico.jp", "発達障害 療育・学習支援"),
    ("LITALICO発達ナビ", ["発達ナビ", "リタリコ発達ナビ"], "h-navi.jp", "発達障害 情報サイト"),
    ("スタジオそら", ["スタジオそら"], "studiosora.jp", "児童発達支援・放課後等デイサービス"),
    ("スタジオplus+", ["スタジオプラス", "スタジオplus"], "www.st-plus.org", "児童発達支援・放課後等デイサービス"),
    ("Branch", ["ブランチ 不登校", "branch 発達障害"], "branchkids.jp", "不登校・発達障害 居場所"),
    ("ウィズ・ユー", ["ウィズユー", "ウィズ・ユー"], "www.with-ac.com", "放課後等デイサービス・学童"),
    ("ティーンズ", ["ティーンズ 発達障害", "teens 発達障害"], "www.teensmoon.com", "発達障害 学習支援・就労準備"),
    ("ハッピーテラス", ["ハッピーテラス"], "", "児童発達支援・放課後等デイサービス"),
    ("コペルプラス", ["コペルプラス"], "", "児童発達支援"),
    ("こぱんはうすさくら", ["こぱんはうすさくら", "こぱん"], "", "児童発達支援・放課後等デイサービス"),
    # 不登校向け学習支援・フリースクール・通信制
    ("オンラインフリースクール シンガク", ["シンガク フリースクール", "シンガク 不登校"], "www.shingaku-fs.jp", "不登校 オンラインフリースクール"),
    ("学研WILL学園", ["WILL学園", "学研WILL学園"], "www.willschool.net", "フリースクール・サポート校"),
    ("クラスジャパン小中学園", ["クラスジャパン", "クラスジャパン小中学園"], "", "不登校 オンライン学習"),
    ("トウコベ", ["トウコベ"], "", "不登校 オンライン学習"),
    ("青楓館高等学院", ["青楓館高等学院", "青楓館"], "seifukan-gakuin.com", "通信制高校サポート校"),
    ("興学社高等学院", ["興学社高等学院", "興学社"], "highschool.kohgakusha.com", "通信制高校サポート校"),
    # 通信教育・教材・オンライン学習
    ("すらら", ["すらら", "すらら発達障害スクール"], "surala.jp", "通信教育・ICT教材"),
    ("進研ゼミ", ["進研ゼミ", "チャレンジ 進研ゼミ"], "", "通信教育"),
    ("スマイルゼミ", ["スマイルゼミ"], "", "通信教育（タブレット）"),
    ("Z会", ["z会", "Z会 通信教育"], "", "通信教育"),
    ("スタディサプリ", ["スタディサプリ", "スタサプ"], "", "オンライン学習"),
    ("天神", ["天神 教材", "天神 タブレット"], "", "通信教育（タブレット）"),
    ("公文式", ["公文", "くもん", "kumon"], "", "学習教室"),
    ("学研教室", ["学研教室"], "", "学習教室"),
    ("QQキッズ", ["qqキッズ", "QQ English キッズ"], "www.qqeng.com", "オンライン英会話"),
]


def main():
    uniq = {L.norm(r["keyword"]) for r in csv.DictReader((L.HERE / "out" / "keywords_unique.csv").open(encoding="utf-8-sig"))}
    vocab = {L.norm(t) for a in L.load_map()["axes"].values() for c in a.values() for t in c["terms"]}
    url_domains = {r["domain"] for r in L.urls()}
    serp_text = L.norm(" ".join(json.dumps(json.loads(open(f, encoding="utf-8").read()), ensure_ascii=False)
                                for f in glob.glob(str(L.HERE / "serp" / "round*" / "*.json"))))
    page_text = L.norm(" ".join(" ".join([p.get("title") or ""] + (p.get("h1") or []) + (p.get("h2") or []))
                                for p in L.iter_pages()))
    rows = []
    for name, aliases, domain, stype in BRANDS:
        for i, a in enumerate(aliases):
            n = L.norm(a)
            src = []
            if any(n in u for u in uniq):
                src.append("keywords_unique")
            if n in vocab or any(n in v for v in vocab if len(v) >= 3):
                src.append("00_意図マップ")
            if domain and any(d.strip() in url_domains for d in domain.split("/")):
                src.append("urls.csv")
            if n in serp_text:
                src.append("Google_SERP")
            if n in page_text:
                src.append("競合ページ見出し")
            rows.append(dict(brand_name=name, normalized_brand_name=L.norm(name), brand_alias=a,
                             normalized_alias=n, alias_type="検索形" if i < SEARCH_FORMS else "表記揺れ",
                             use_in_matrix=1 if i < SEARCH_FORMS else 0, domain=domain, service_type=stype,
                             discovery_source=" | ".join(src) or "人手追加（既存データで未観測）"))
    with (L.HERE / "competitor_brands.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"ブランド {len(BRANDS)} / 表記 {len(rows)} / 掛け合わせに使う検索形 {sum(r['use_in_matrix'] for r in rows)}")
    miss = [r["brand_alias"] for r in rows if r["discovery_source"].startswith("人手")]
    print("既存データで未観測の表記:", miss)


if __name__ == "__main__":
    main()

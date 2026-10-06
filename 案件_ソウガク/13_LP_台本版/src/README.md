# ソウガクLPの元データ（ここを直して組み立てる）

`python3 build_pages.py` で次の2ページを作る（出力先は1つ上のフォルダ）。

| ページ | 出力 | 中身 |
|---|---|---|
| 王道LP | `index.html` | `lp01_top` → `lp01_compare_h2` → **`common_compare`** → `lp01_points`（3つのポイント） → **`common_after`** |
| LP02（家庭教師→オンライン家庭教師 導線） | `lp02/index.html` | `lp02_top` → `lp02_compare_h2` → **`common_compare`** → **`common_after`**（3つのポイントだけ除外） |

- **太字の `common_*` は2ページ共通**。比較表〜結論CTA（`common_compare`）と、ランキング以降（体験談・無料体験・料金・FAQ・最終CTA・追従ボタンまで／`common_after`）。王道LPを直すときはここを直せば LP02 にも同じ変更が入る。
- LP02 専用は比較表より上（`lp02_top.html`）と比較表の見出し（`lp02_compare_h2.html`）だけ。台本はスプレッドシート「LP02_台本_v1」（中身は v2）。比較表より前に CTA は置かない。
- `<!--SLOT:IMG-xx-->` は `build.py`（画像指示）と `gen_map.json`（完成画像）で画像に置き換わる。
- LP02 はサブフォルダなので、画像・CSS などの相対パスに自動で `../` を付けて出力する。
- LP02 の差し替え条件は URL パラメータ：`?kw=online`（H1・サブコピー後半）、`?grade=sho|chu|ko`（学年の悩みカードをその学年だけに）。

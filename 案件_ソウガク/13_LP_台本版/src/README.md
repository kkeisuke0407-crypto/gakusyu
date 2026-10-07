# ソウガクLPの元データ（ここを直して組み立てる）

`python3 build_pages.py` で次のページを作る（出力先は1つ上のフォルダ）。

| ページ | 出力 | 中身 |
|---|---|---|
| 王道LP | `index.html` | `lp01_top` → **`common_compare`** → `lp01_points`（3つのポイント） → **`common_after`** |
| LP02（家庭教師→オンライン家庭教師 導線） | `lp02/index.html` | `lp02_top` → **`common_compare`** → **`common_after`**（3つのポイントだけ除外） |
| LP03（勉強法・宿題 → 個別支援 導線） | `lp03/index.html` | `lp03_top` → **`common_compare`** → **`common_after`**（3つのポイントだけ除外） |

- **太字の `common_*` は全ページ共通**。比較の見出し「オンライン家庭教師3社を比較」〜比較表〜結論CTA（`common_compare`）と、ランキング以降（体験談・無料体験・料金・FAQ・最終CTA・追従ボタンまで／`common_after`）。ここを直せば全ページに同じ変更が入る。
- 共通部品の中の出し分け：`<!--OUDOU-ONLY-->〜<!--/OUDOU-ONLY-->` は王道LPだけ、`<!--SUB-ONLY-->〜<!--/SUB-ONLY-->` はサブLP（`build_pages.py` の `sub=True`）だけに出る。「3つのポイント」に触れる文や、体験談の形（王道＝mt-story／サブLP＝mt-review）はこれで分けている。
- サブLP専用は比較の見出しより上（`lpXX_top.html`）だけ。比較の見出しから下は全ページ共通（違うのは上の出し分けの印の箇所だけ）。台本はスプレッドシート「LPXX_台本_v1」。比較表より前に CTA は置かない。
- `<!--SLOT:IMG-xx-->` は `build.py`（画像指示）と `gen_map.json`（完成画像）で画像に置き換わる。
- サブLPはサブフォルダなので、画像・CSS などの相対パスに自動で `../` を付けて出力する。
- 差し替え条件は URL パラメータ。
  - LP02：`?kw=online`（H1・会話⑥）、`?grade=sho|chu|ko`（会話①を学年の悩みに）
  - LP03：`?kw=method`（会話の保護者①②を勉強法KW向けに）

## 公開前チェックと公開

- `NODE_PATH=$(npm root -g) node check_pages.cjs`：全ページをスマホ（375px）とPC（1280px）で確認する。
  - 比較表より前のCTA・リンク
  - 追従CTAの出るタイミング
  - 画像切れ・横はみ出し・JSエラー
  - H2がスマホで2行以内か
  - サブLPに「3つのポイント」が残っていないか
- `bash publish.sh "メッセージ"`：ビルド → チェック → 公開ブランチ `codex/online-tutor-pages` へ反映 → 実サイトで一致を確認、までを1回で行う。**開発ブランチへの push だけでは実サイトに出ない**ので、公開は必ずこれで行う。

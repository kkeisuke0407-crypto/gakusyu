# ソクガクLP 計測

対象: https://online-tutor.navolio.net/ と /lp02/〜/lp09/。2026-10-07導入（LP09 は 2026-10-11 追加）。

- GA4: 「ソクガクLP」プロパティ 557942591、測定ID G-FQS2SK5HNF（日本時間・日本円）。
- Google広告: ソウガク 507-589-9384。
- メイン: SougakuConversion（7821324623）、クリックからのオフラインインポート。全件、90日、ラストクリック。ASP/API接続・成果受信は別途必要。
- サブ: Sougaku_MCV_OfficialClick（7826919832）。ソウガクの指定felmatリンクのみ。初回のみ、30日、価値0円。入札には使用しない。Google広告にGA4から同じMCVを重複インポートしない。

## 見る場所

[GA4](https://analytics.google.com/analytics/web/#/a386364116p557942591/reports/intelligenthome)のレポートで「ページとスクリーン」「イベント」を確認。詳細比較は「探索」→「自由形式」で以下を使う。

|目的|行|列|指標・フィルタ|
|---|---|---|---|
|LP比較|LP番号|イベント名|総ユーザー数、イベント数|
|CTAの効き方|LP番号、CTA位置|イベント名|lp_cta_view / sougaku_mcv に絞る|
|離脱位置の目安|LP番号、スクロール到達率|—|lp_scroll の総ユーザー数|
|読み進み|LP番号、セクション|—|lp_section_view の総ユーザー数|
|不安・関心|LP番号、FAQ番号|—|lp_faq_open の総ユーザー数|
|実読時間|LP番号、読了秒数|—|lp_active_read の総ユーザー数|

通常集計は「計測モード = live」で絞る。設定確認用の ?measurement_debug=1 は debug。新しいカスタム項目が通常レポート・探索に使えるまで24〜48時間かかる場合がある。

CTA位置: comparison（比較表）、conclusion（結論文中）、first（冒頭の体験ボタン）、rank1_banner（バナー）、rank1（1位詳細後）、concern_mid / concern_end（不安解消の途中・後）、final（末尾）、sticky（追従）。

MCVは紹介先への遷移であり、無料体験申込・承認成果ではない。GA4のクリックイベント数は再クリックを含む。広告側の「初回のみ」は広告操作1回につき初回。CTAクリック率を比較する際はユーザー数を使い、表示条件（50%以上・1秒）も揃える。

各LPのページビューは1回、スクロール25/50/75/90/100%は各1回、セクション・CTA表示は各1回。実読時間は表示・フォーカス中の30/60/120秒到達。FAQは開くたび記録。閉じたタブ・バックグラウンド時間は実読に含めない。

## 運用

- 共通スクリプト: lp-measurement.js。HTMLの data-cta-id / data-section-id / data-faq-id は改稿しても意味を保持する。
- felmatの ak / pb とリンク先・targetは変更しない。GCLIDのASP側取得とオフライン成果送信はASPに確認。
- GA4へ送るURL引数は既存の広告識別子と `kw / grade / exam` のみ。値は英数字と `_.~+-` の1〜200文字に制限し、その他のURL引数・フォーム値・質問文を送らない。広告パーソナライズ・Googleシグナルは無効。プライバシーページでブラウザごとの計測停止が可能。EEA等では同意未取得状態のストレージ利用を拒否。
- 本番相当の動作テスト: node tests/measurement.test.cjs。
- 公開ブランチ: codex/online-tutor-pages（GitHub Pagesルート）。別ブランチの古いHTMLを上書きしない。

## 2026-10-07 追加改善

- 初回 `page_view` は自動送信を無効にし、`lp_id / measurement_mode / page_location / page_referrer` を指定して1回送信。既存カスタムイベントと同じLP識別情報を使用する。
- `?kw=math` と `?kw=english`、`?grade=chu`、`?exam=junior` などの内部切替をGA4のURLに保持。`measurement_debug` はURLに残さず `measurement_mode=debug` として区別する。
- `lp_other_service_click` の `destination=tintle.net / coaching01.com` と、`sougaku_mcv` の `destination=sougaku` を維持。GA4ではイベントスコープの「遷移先」カスタムディメンションとして使う。
- 初回page_viewの重複、全8LPとdebug/live識別、許可パラメータの保持、任意・不正値の除外を追加テスト。既存のクリック、スクロール、到達、実読、FAQ、計測停止、Google広告MCV送信も継続して検証。

## 2026-10-11 LP09 追加

- `/lp09/` を `lp_id=LP09` として計測（lp-measurement.js のLP判定を /lp02/〜/lp09/ に拡張。/lp10/ など未対応のパスは従来どおり LP01 扱い）。スクリプトの読み込みは `?v=20261011` に更新。
- イベント名・パラメータは既存のまま（page_view / lp_section_view / lp_cta_view / sougaku_mcv / lp_other_service_click / lp_scroll / lp_active_read / lp_faq_open）。新しいイベントは追加していない。
- LP09 独自のセクション: intro_1（書けないにも、いろいろな困り方）／intro_2（家で教えるのが難しいとき）／intro_3（先生を選ぶなら）。比較表以降は全LP共通（comparison〜final）。

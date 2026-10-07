# ソクガクLP 計測

対象: https://online-tutor.navolio.net/ と /lp02/〜/lp08/。2026-10-07導入。

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
- 任意のURL引数・検索語・フォーム値・質問文を送らない。広告パーソナライズ・Googleシグナルは無効。プライバシーページでブラウザごとの計測停止が可能。EEA等では同意未取得状態のストレージ利用を拒否。
- 本番相当の動作テスト: node tests/measurement.test.cjs。
- 公開ブランチ: codex/online-tutor-pages（GitHub Pagesルート）。別ブランチの古いHTMLを上書きしない。

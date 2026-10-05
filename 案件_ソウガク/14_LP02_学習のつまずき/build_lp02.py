# -*- coding: utf-8 -*-
"""LP02（発達特性×学習のつまずき）の index.html を組み立てる。

- 新規部分（FV〜ソウガク単品訴求）：../KW最終選定_20261005/11_LP02_台本_v1.md の文言
- 共通部分：LP01（王道LP）の index.html から該当行をそのままコピー（文言・HTMLを変えない）
  LP01 の正本 = branch claude/amazing-thompson-2rqmiv の 案件_ソウガク/13_LP_台本版/index.html
  （= 公開ブランチ codex/online-tutor-pages の index.html と同一）
  使い方：python3 build_lp02.py <LP01のindex.htmlのパス>
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1]
L = open(SRC, encoding='utf-8').read().split('\n')


def block(a, b, must_start, must_end):
    """LP01 の a〜b 行（1始まり・両端含む）をそのまま返す。行がずれていたら止める"""
    lines = L[a - 1:b]
    assert must_start in lines[0], (a, lines[0])
    assert must_end in lines[-1], (b, lines[-1])
    return '\n'.join(lines)


KV = block(103, 115, 'ソウガク公式LPのキービジュアル', '</figure>')
TOOL = block(119, 121, '<figure class="mt-img">', '</figure>')
VOICES = block(205, 261, '12〜15 体験談パート', 'ソウガクの無料体験を公式サイトで見る')
TRIAL = block(263, 297, '16〜17 無料体験', '無料体験の内容を公式サイトで見る')
FEE = block(299, 326, '18 料金', '料金も含めて')
FAQ = block(328, 338, '19 FAQ', '</div>')
FINAL = block(340, 358, '20 最終CTA', 'ソウガクの公式サイトで確認する')
NOTE_OPERATOR = block(360, 374, '<!-- 注記 -->', '</section>')
FOOTER = block(376, 382, '</article>', '</footer>')
STICKY = block(385, 385, 'class="mt-sticky"', 'ソウガクの公式サイトを見てみる')
SCRIPT_CTA = block(387, 391, '<script>', '</script>')
SCRIPT_STICKY = block(392, 403, '<script>', '</html>')
CTA_HREF = 'https://t.felmat.net/fmcl?ak=C12158L.1.I1680104.D1416296&amp;pb='
assert CTA_HREF in STICKY

# 追従ボタンの監視対象だけ LP02 用に差し替え（LP01は第1位の #cta-rank1。LP02は単品訴求の最初のASPボタン #cta-sogaku）
SCRIPT_STICKY = SCRIPT_STICKY.replace("/* パーツ集 mt-sticky のscript。監視対象は第1位の最初の大ボタン（#cta-rank1） */",
                                      "/* パーツ集 mt-sticky のscript。監視対象はソウガク単品訴求の最初の大ボタン（#cta-sogaku） */")
SCRIPT_STICKY = SCRIPT_STICKY.replace("document.querySelector('#cta-rank1')", "document.querySelector('#cta-sogaku')")
assert '#cta-sogaku' in SCRIPT_STICKY and '#cta-rank1' not in SCRIPT_STICKY

HEAD = '''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>発達特性のある子の勉強法。「できない」をひとまとめにせず、つまずき方から見直す。</title>
<meta name="description" content="宿題に取りかかれない。漢字がなかなか覚えられない。算数だけ途中で止まってしまう。同じ「勉強が苦手」でも、困り方は違います。まずは、どこで止まっているのかを整理することから。">
<link rel="stylesheet" href="parts.css">
<link rel="stylesheet" href="style.css">
<link rel="stylesheet" href="lp02.css">
</head>
<body>
<div class="mt-wrap">
<article class="mt-body">

  <!-- LP02（発達特性×学習のつまずき）：North 17P ④テール型（KV → タイトル → 検索ニーズを満たすコンテンツ → 悩み・選び方 → ソウガク単品訴求） -->
  <!-- 新規部分の文言：../KW最終選定_20261005/11_LP02_台本_v1.md ／ 共通部分：LP01（王道LP）index.html からそのまま流用（build_lp02.py） -->
  <!-- 比較表・ランキング・他社名・他社リンクは入れない -->'''

NEW = '''
  <!-- 01 FV【新規】（ソウガクの名前・申込ボタンはまだ出さない。ボタンはページ内リンク） -->
  <header class="lp02-fv">
    <h1 class="lp02-fv__ttl"><span class="lp-nw">発達特性のある子の勉強法。</span><br><span class="lp02-fv__key"><span class="lp-nw">「できない」を</span><span class="lp-nw">ひとまとめにせず、</span><span class="lp-nw">つまずき方から見直す。</span></span></h1>
  </header>

  <p class="mt-prbar"><span class="lp-nowrap"><b>PR</b>　本ページはプロモーションを含みます</span>　｜　<span class="lp-nowrap">更新日：2026年10月5日</span></p>

  <p>宿題に取りかかれない。<br>漢字がなかなか覚えられない。<br>算数だけ途中で止まってしまう。</p>

  <p>同じ「勉強が苦手」でも、<br>読むところで止まる子、<br>書くことが大変な子、<br>始めるまでに時間がかかる子では、<br>困り方が違います。</p>

  <p>だから、ただ<br>「もっと勉強させる」<br>のではなく、</p>

  <p>まずは、<br><span class="mt-mark">「どこで止まっているのか」</span><br>を整理することから。</p>

  <div class="mt-cta"><a class="mt-cta__btn lp02-anchor-btn" href="#nav">つまずき別の考え方を見る</a></div>

  <!-- 02 まず最初に整理したいこと【新規】 -->
  <h2 class="mt-h2" id="stuck">「勉強できない」は、ひとつの困り方ではありません</h2>

  <div class="mt-check"><ul>
    <li>「やればできるのに、なかなか始めない」</li>
    <li>「説明すると分かったように見えるのに、次の日には忘れている」</li>
    <li>「漢字だけ、何度練習しても覚えにくい」</li>
    <li>「問題文を読むところで止まる」</li>
    <li>「途中で集中が切れて、そのまま終わってしまう」</li>
  </ul></div>

  <p>一言で「勉強が苦手」と言っても、止まっている場所は同じではありません。</p>

  <figure class="mt-img" data-img="IMG-05"><img src="images/gen/05_stuck_4types.webp" alt="同じ『勉強が苦手』でも、止まる場所はそれぞれ違います：読むところで止まる、書くところで止まる、始めるまで時間がかかる、途中で集中が切れる" width="1200" height="900" loading="lazy"></figure>

  <div class="mt-info"><ul>
    <li>読むところで止まる</li>
    <li>書くところで止まる</li>
    <li>始めるまでに時間がかかる</li>
    <li>途中で集中が切れる</li>
  </ul></div>

  <p>では、見直したいポイントが変わります。</p>

  <p><span class="mt-mark">大切なのは、「何が苦手か」だけでなく、「どこで止まっているか」を見ること。</span></p>

  <p>まずは、お子さんの困り方に近いところから見てみてください。</p>

  <!-- 03 悩み別ナビ【新規】 -->
  <h2 class="mt-h2 lp02-target" id="nav">お子さんは、どこで困っていますか？</h2>
  <ul class="lp02-nav">
    <li><a href="#g1"><b>勉強法が分からない・勉強についていけない</b><span>→ 勉強の進め方そのものを見直したい方へ</span></a></li>
    <li><a href="#g2"><b>宿題に取りかかれない・集中が続かない</b><span>→ 始めるまで、続けるところで止まる方へ</span></a></li>
    <li><a href="#g3"><b>漢字・読み書き・算数など、一部で強くつまずく</b><span>→ 教科や作業ごとに困り方が違う方へ</span></a></li>
    <li><a href="#g4"><b>親が教えると、ついぶつかってしまう</b><span>→ 家庭だけで先生役まで抱え込んでいる方へ</span></a></li>
    <li><a href="#g5"><b>学校に行けない時期の勉強が心配</b><span>→ 発達特性があり、家での学習を続けたい方へ</span></a></li>
  </ul>

  <!-- 04 G1｜勉強法・勉強できない【新規】 -->
  <h2 class="mt-h2 lp02-target" id="g1">「もっとやる」より前に、どこで止まっているかを見る</h2>

  <p>発達特性のあるお子さんの勉強で悩むと、</p>
  <p>「勉強時間を増やした方がいいのかな」<br>「もっと繰り返せば覚えられるのかな」</p>
  <p>と考えてしまいがちです。</p>

  <p>でも、始めるところで止まっているのか、<br>読んで理解するところで止まっているのか、<br>覚えたことを使うところで止まっているのかで、困り方は違います。</p>

  <p>たとえば、</p>

  <div class="lp02-case"><p class="lp02-case__ttl">ケース1｜問題を開くまでに時間がかかる</p><p>→ 内容を理解できない以前に、「始めるところ」で止まっているかもしれません。</p></div>
  <div class="lp02-case"><p class="lp02-case__ttl">ケース2｜説明すると分かるのに、自分だけでは解けない</p><p>→ 「分かった」と「自分で進められる」の間に、まだ段差があるのかもしれません。</p></div>
  <div class="lp02-case"><p class="lp02-case__ttl">ケース3｜何度やっても同じところで止まる</p><p>→ 同じやり方を繰り返すより、まず「どこで止まっているか」を見直した方がよいこともあります。</p></div>

  <p>ここで言いたいのは、原因を家庭だけで決めつけることではありません。</p>

  <p><span class="mt-mark">「できない」ではなく、どの場面で困っているのかを具体的にしていく。</span></p>

  <p>それだけでも、次に何を試すかを考えやすくなります。</p>

  <!-- 05 G2｜宿題・着手・集中【新規】 -->
  <h2 class="mt-h2 lp02-target" id="g2">宿題に取りかかれないとき、「やる気がない」で終わらせない</h2>

  <p>「宿題を始めるまでに1時間かかる」<br>「やっと始めても、すぐ別のことをしてしまう」<br>「途中で止まると、そのまま戻れない」</p>

  <p>こうした様子を見ると、つい</p>
  <p>「早くやって」<br>「集中して」</p>
  <p>と言いたくなります。</p>

  <p>でも、家庭で見たいのは、</p>

  <div class="mt-points"><ul>
    <li><b>始めるところ</b>で止まるのか。</li>
    <li><b>続けるところ</b>で止まるのか。</li>
    <li><b>最後まで終えるところ</b>で止まるのか。</li>
  </ul></div>

  <p>という違いです。</p>

  <p>同じ「宿題が進まない」でも、困っている場所は同じとは限りません。</p>

  <p>だからこそ、</p>
  <p>「なぜやらないの？」</p>
  <p>ではなく、</p>
  <p class="mt-oneline"><span>「どこからなら始められそう？」</span></p>
  <p>と、止まっている場所を一緒に見ていく方が、次の打ち手を考えやすくなります。</p>

  <!-- 06 G3｜読み書き・教科別のつまずき【新規】 -->
  <h2 class="mt-h2 lp02-target" id="g3">漢字・読み書き・算数。教科名だけでは見えない「つまずき」があります</h2>

  <div class="mt-check"><ul>
    <li>漢字が覚えられない</li>
    <li>漢字が書けない</li>
    <li>読み書きが苦手</li>
    <li>算数・計算で止まる</li>
    <li>図形が苦手</li>
    <li>英単語が覚えにくい</li>
  </ul></div>

  <p>といった、かなり具体的な悩みも少なくありません。</p>

  <p>ここでも、</p>
  <p>「国語が苦手」<br>「算数が苦手」</p>
  <p>だけで終わらせず、</p>

  <p><span class="mt-mark">読むところなのか、書くところなのか、覚えるところなのか、手順を追うところなのか。</span></p>

  <p>まで見ていくことが大切です。</p>

  <p>同じ教科でも、困り方が違えば、合う進め方も同じとは限りません。</p>

  <h3 class="mt-h3">たとえば</h3>
  <div class="lp02-case"><p class="lp02-case__ttl">漢字が苦手</p><p>→ 読むのか、書くのか、覚えるのか。</p></div>
  <div class="lp02-case"><p class="lp02-case__ttl">算数が苦手</p><p>→ 計算なのか、文章題なのか、手順を追うことなのか。</p></div>
  <div class="lp02-case"><p class="lp02-case__ttl">英語が苦手</p><p>→ 単語を覚えることなのか、読むことなのか、書くことなのか。</p></div>

  <p>「何の教科が苦手か」だけではなく、<br><b>どの作業で止まっているのか</b>まで見ると、必要な学び方を考えやすくなります。</p>

  <!-- 07 G4｜親の教え方・関わり【新規】（親が先生役を続けなくていい＝検索ニーズに答えたあとの感情ブリッジ） -->
  <h2 class="mt-h2 lp02-target" id="g4">親が教えるほど、親子でぶつかってしまうとき</h2>

  <p>「さっき説明したよね」<br>「なんでここが分からないの？」</p>

  <p>本当は怒りたいわけではないのに、毎日の宿題になると、つい言いすぎてしまう。</p>

  <p>ソウガク公式サイトに掲載されている保護者の声にも、家で保護者が勉強を見ると、イライラして親子で言い合いになることがあった例があります。</p>

  <p>ここで、親がもっと上手に教えられるようになることだけが答えではありません。</p>

  <p class="mt-oneline"><span>親が先生役を続けなくてもいい。</span></p>

  <p>家庭の外に、お子さんの困り方を一緒に見てくれる人を増やす。</p>

  <p>それも一つの方法です。</p>

  <!-- 08 G5｜学校に行けない時期の学び【新規】（不登校全般ではなく、発達特性がある子の「学習」に限定） -->
  <h2 class="mt-h2 lp02-target" id="g5">学校に行けない時期も、「家でどう学ぶか」は考えられます</h2>

  <p>発達特性があり、学校へ行けない・行きづらい時期になると、</p>
  <p>「勉強が遅れてしまわないか」<br>「家で何をしたらいいのか」</p>
  <p>と心配になることがあります。</p>

  <p>このページでは、不登校そのものの原因や進路、居場所について答えるのではなく、<br><b>学校に行けない時期の“学習”</b>に絞って考えます。</p>

  <p>家で学ぶ方法の一つとして、オンラインで1対1の授業を受ける選択肢もあります。</p>

  <p>ソウガクの全国オンライン商品は、小学生・中学生・高校生向けのオンライン家庭教師です。</p>

  <p class="mt-small">※発達特性のない不登校児全般を対象としていることは、全国オンライン公式では確認できていません。このセクションは、発達特性があるお子さんの学習について扱います。</p>

  <!-- 09 商品へのブリッジ【新規】 -->
  <h2 class="mt-h2">家庭で工夫しても、「何を変えればいいか分からない」とき</h2>

  <p>ここまで見てきたように、</p>
  <p>「勉強できない」<br>「宿題が進まない」<br>「漢字が覚えられない」</p>
  <p>という言葉だけでは、その子がどこで困っているかまでは分かりません。</p>

  <p>家庭で一つずつ試していく方法もあります。</p>

  <p>でも、毎日の宿題や学校生活の中で、親がずっと</p>
  <p>「次はこの方法？」<br>「これでもダメなら、今度は？」</p>
  <p>と考え続けるのは簡単ではありません。</p>

  <p>そこで選択肢になるのが、</p>

  <p><span class="mt-mark">教え方を増やす前に、その子がどこで止まっているのかを一緒に見てもらうこと。</span></p>

  <p>「何を教えるか」だけではなく、</p>

  <p><b>どこで止まっているかを見て、学び方を組み立ててくれるか。</b></p>

  <p>ここからは、その考え方に近いオンライン家庭教師「ソウガク」を見ていきます。</p>

  <!-- 10 ソウガク単品訴求【新規＋LP01の事実・公式画像を流用】（ランキング・他社比較なし） -->
  <h2 class="mt-h2" id="sogaku">「何を教えるか」だけでなく、「どこで止まっているか」から学び方を組み立てる</h2>

  <p>ソウガクは、発達障害・グレーゾーン専門のオンライン家庭教師です。</p>

KV_BLOCK

  <p>特徴は、ただ1対1で教えることではありません。</p>

  <h3 class="mt-h3"><span class="lp-num">1.</span>アセスメントから個別指導計画へ</h3>
  <p>ソウガクでは、アセスメントをもとに個別指導計画を作成します。</p>
  <p>「国語が苦手」「算数が苦手」だけでなく、<br>今どこでつまずいているのかを整理してから、学び方を考える設計です。</p>

  <h3 class="mt-h3"><span class="lp-num">2.</span>先生個人だけに任せない</h3>
  <p>先生は、一般社団法人 発達凸凹アソシエーションによる教師研修と、座学のマニュアル研修を受けた社会人講師です。</p>
  <p>発達特性への理解を、先生個人の経験だけに任せない仕組みがあります。</p>

  <h3 class="mt-h3"><span class="lp-num">3.</span>授業後も、家庭だけで抱え込まない</h3>
TOOL_BLOCK
  <p>毎回の指導報告があり、家で困ったことがあれば教師や本部に共有できます。</p>
  <p><b>授業をお願いしたあとも、また親だけが先生役に戻らなくていい仕組みです。</b></p>

  <div class="mt-cta" id="cta-sogaku"><p class="mt-cta__micro">＼無料体験2回・1回目は保護者面談も可／</p><a class="mt-cta__btn" href="CTA_HREF" data-cta target="_blank" rel="sponsored nofollow noopener">ソウガクの公式サイトを見てみる</a></div>

  <!-- ここから下は LP01（王道LP）からそのまま流用（文言・HTMLとも変更なし） -->
'''

NEW = NEW.replace('KV_BLOCK', KV).replace('TOOL_BLOCK', TOOL).replace('CTA_HREF', CTA_HREF)

STICKY_BLOCK = ('<!-- 追従ボタン（LP01と同じ。ソウガク単品訴求の最初の大ボタン #cta-sogaku を過ぎたら出す＝検索ニーズの回答中には出さない） -->\n'
                + STICKY)

html = '\n'.join([HEAD, NEW, VOICES, '', TRIAL, '', FEE, '', FAQ, '', FINAL, '', NOTE_OPERATOR, '', FOOTER, '',
                  STICKY_BLOCK, '', SCRIPT_CTA, SCRIPT_STICKY, ''])
open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8').write(html)

# 共通部分が LP01 と1文字も違わないことを確認
src = '\n'.join(L)
for name, b in [('KV', KV), ('TOOL', TOOL), ('VOICES', VOICES), ('TRIAL', TRIAL), ('FEE', FEE), ('FAQ', FAQ),
                ('FINAL', FINAL), ('NOTE_OPERATOR', NOTE_OPERATOR), ('FOOTER', FOOTER), ('STICKY', STICKY), ('SCRIPT_CTA', SCRIPT_CTA)]:
    assert b in src and b in html, name
print('ok', len(html))

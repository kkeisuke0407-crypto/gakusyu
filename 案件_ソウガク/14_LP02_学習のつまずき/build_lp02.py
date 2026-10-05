# -*- coding: utf-8 -*-
"""LP02 v3（発達特性×学習のつまずき｜体験談で読み進める④テール型）の index.html を組み立てて、検証する。

- 上半分（FV〜ソウガク登場〜反論の体験談）：このファイルの TOP（hozon「体験談ランキング型LP パーツ集」の部品とルールで組む）
- 下半分（無料体験・料金・FAQ・最終CTA・注記・運営者情報・フッター・追従ボタン）と、PR帯・公式KV・テキストリンク：
  LP01（王道LP）の index.html から該当行をそのままコピー（文言・HTMLを変えない）
  LP01 の正本 = branch claude/amazing-thompson-2rqmiv の 案件_ソウガク/13_LP_台本版/index.html
使い方：python3 build_lp02.py <LP01のindex.htmlのパス>
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
L = open(sys.argv[1], encoding='utf-8').read().split('\n')


def block(a, b, must_start, must_end):
    """LP01 の a〜b 行（1始まり・両端含む）をそのまま返す。行がずれていたら止める"""
    lines = L[a - 1:b]
    assert must_start in lines[0], (a, lines[0])
    assert must_end in lines[-1], (b, lines[-1])
    return '\n'.join(lines)


PRBAR = block(22, 22, 'class="mt-prbar"', '更新日：2026年10月5日')
KV = block(103, 115, 'ソウガク公式LPのキービジュアル', '</figure>')
TOOL = block(119, 121, '<figure class="mt-img">', '</figure>')
TEXTLINK = block(261, 261, 'class="mt-textlink"', '1回目は保護者だけの面談にもできます')
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

# 追従ボタンの監視対象だけ LP02 用に差し替え（LP01は第1位の #cta-rank1。LP02はソウガク紹介の最初のASPボタン #cta-sogaku）
SCRIPT_STICKY = SCRIPT_STICKY.replace("/* パーツ集 mt-sticky のscript。監視対象は第1位の最初の大ボタン（#cta-rank1） */",
                                      "/* パーツ集 mt-sticky のscript。監視対象はソウガク紹介の最初の大ボタン（#cta-sogaku） */")
SCRIPT_STICKY = SCRIPT_STICKY.replace("document.querySelector('#cta-rank1')", "document.querySelector('#cta-sogaku')")
assert '#cta-sogaku' in SCRIPT_STICKY and '#cta-rank1' not in SCRIPT_STICKY

ICON_PARENT = '<img src="images/gen/icon_parent.webp" alt="" width="240" height="240">'
ICON_EDITOR = '<img src="images/gen/icon_editor.webp" alt="" width="240" height="240">'


def say(text):
    return f'  <div class="mt-say"><span class="mt-say__icon">{ICON_PARENT}</span><p class="mt-say__b">{text}</p></div>'


def talk(side, text):
    if side in ('parent', 'parent_think'):
        think = ' mt-talk__row--think' if side == 'parent_think' else ''
        return (f'    <div class="mt-talk__row mt-talk__row--r{think}"><div class="mt-talk__who"><span class="mt-talk__icon">{ICON_PARENT}</span>'
                f'<span class="mt-talk__name">保護者</span></div><div class="mt-talk__b">{text}</div></div>')
    return (f'    <div class="mt-talk__row"><div class="mt-talk__who"><span class="mt-talk__icon">{ICON_EDITOR}</span>'
            f'<span class="mt-talk__name">編集部</span></div><div class="mt-talk__b">{text}</div></div>')


def review(who, quote):
    """mt-review：見出し＝属性、本文＝公式サイト掲載の声の抜粋（言い換えない）"""
    return (f'  <div class="mt-review"><div class="mt-review__head"><span class="mt-review__icon" aria-hidden="true"></span>'
            f'<p class="mt-review__who">{who}</p></div><p>「{quote}」</p></div>')


SRC_NOTE = '  <p class="mt-small">※ソウガク公式サイト掲載の声を編集部が要約し、一部を抜粋したものです。個人の感想であり、同様の結果を保証するものではありません。</p>'

HEAD = '''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>発達特性のある子の勉強法｜集中・計算・宿題のつまずきにどう向き合う？</title>
<meta name="description" content="発達障害・グレーゾーンなど、発達特性のあるお子さんの勉強法を実例から紹介。集中が切れる、計算で止まる、家で教えるとケンカになる。先生がどう関わったか、ソウガクは何をしてくれるのかまで分かります。">
<link rel="stylesheet" href="parts.css">
<link rel="stylesheet" href="style.css">
<link rel="stylesheet" href="lp02.css">
</head>
<body>
<div class="mt-wrap">
<article class="mt-body">

  <!-- LP02 v3：体験談パーツそのものでストーリーを進める④テール型（悩み → 実例 → 変化 → 意味づけ → 次の疑問）。比較表・ランキング・他社名・他社リンクなし -->
  <!-- 組み方：hozon「体験談ランキング型LP パーツ集」の部品とルール。画像はLP01の既存画像と公式画像だけ（画像指示枠なし） -->'''

TOP = f'''
  <!-- 01 FV：検索意図をそのまま拾い、実例→ソウガクまで読む理由をつくる（タイトル → PR帯 → アイキャッチ → 悩み → 答えの予告 → 3つのケース → ページ内ボタン） -->
  <h1 class="lp-ttl"><span class="lp-nw">発達特性のある子の勉強法。</span><br><span class="lp-nw">何度教えても進まないなら、</span><br><span class="lp-nw">同じやり方を</span><span class="lp-nw">続けなくていい。</span></h1>

{PRBAR}

  <figure class="mt-img"><img src="images/gen/01_fv_evening-desk.webp" alt="夕方の子ども部屋の机に、開いたままの問題集と鉛筆（イメージ）" width="1200" height="800"></figure>

  <p>宿題に取りかかれない。<br>漢字がなかなか覚えられない。<br>算数だけ、いつも同じところで止まる。</p>

  <p>同じ「勉強が進まない」でも、<br><span class="mt-mark">合う声かけも、教え方も同じとは限りません。</span></p>

  <div class="mt-summary"><p class="mt-summary__ttl">ソウガク公式の声にあった3つのケース</p><ul>
    <li>集中が切れても、声かけで戻れた子</li>
    <li>計算は、毎回伝え方を変えた子</li>
    <li>親が全部見なくてよくなった家庭</li>
  </ul></div>

  <p>この3つを見たあとに、<b>ソウガクが実際に何をしてくれるのか</b>も紹介します。</p>

  <div class="mt-cta"><p class="mt-cta__micro">＼先にサービス内容を見たい方はこちら／</p><a class="mt-cta__btn" href="#sogaku">ソウガクは何をしてくれる？ ↓</a></div>

  <!-- 02 導入の会話：短く、実例へ渡す（サービス名は出さない） -->
  <div class="mt-talk">
{talk('parent', '何度説明しても、<br>同じところで止まります…。')}
{talk('editor', '同じやり方を<br>続けなくていいんです。')}
{talk('parent_think', '（じゃあ、どうすれば…？）')}
{talk('editor', 'まずは<span class="mt-mark">先生がどう関わったか</span>を<br>実際の声で見てみましょう。')}
  </div>
  <p class="mt-small">※よくある迷いを編集部が会話形式にしたものです（人物はイメージ）。</p>

  <!-- 03 実例A：集中が切れる子（mt-say → mt-story → mt-review → mt-oneline） -->
  <h2 class="mt-h2">集中が切れても、戻れる声かけがあった</h2>
  <figure class="mt-img" data-img="IMG-14"><img src="images/gen/14_story-c_refocus.webp" alt="集中が切れたときの関わり方：01 集中が切れる→02 短い声かけ→03 もう一度課題へ" width="1200" height="900" loading="lazy"></figure>

{say('宿題を始めても、すぐ集中が切れる…。')}

  <div class="mt-story">
    <p class="mt-story__who">公式サイト掲載の生徒・保護者の声（小学5年生）</p>
    <p>授業中に集中が切れそうになる場面でも、先生の声かけで再び勉強に向かう様子があったそうです。</p>
    <p>本人も先生との授業を楽しみにしている、と保護者の声が掲載されています。</p>
  </div>
{review('小学5年生・保護者', '集中力が切れそうになっても、先生の言葉で、また頑張って、勉強できている姿に感動しています。')}
{SRC_NOTE}

  <p>ずっと集中できなくてもいい。</p>
  <p class="mt-oneline"><span>切れたあとに、戻れるか。</span></p>
  <p>この子の場合は、「集中し続ける」より、<b>集中が切れそうなときの戻し方</b>がポイントでした。</p>

  <!-- 04 実例B：計算につまずく子 -->
  <h2 class="mt-h2">同じ説明で進まないなら、伝え方を変える</h2>
  <figure class="mt-img" data-img="IMG-05"><img src="images/gen/05_stuck_4types.webp" alt="同じ『勉強が苦手』でも、止まる場所はそれぞれ違います：読むところで止まる、書くところで止まる、始めるまで時間がかかる、途中で集中が切れる" width="1200" height="900" loading="lazy"></figure>

{say('何度説明しても、同じところで止まる…。')}

  <div class="mt-story">
    <p class="mt-story__who">公式サイト掲載の保護者の声（小学2年生）</p>
    <p>数の理解が難しく、計算が苦手なお子さん。始める前は、保護者もとても不安だったそうです。</p>
    <p>先生が毎回いろいろなやり方で、分かりやすいように丁寧に教えてくれている、と紹介されています。</p>
  </div>
{review('小学2年生・保護者', '先生が毎回色々なやり方で、娘が分かりやすいように丁寧な指導をしてくださいますのでとてもありがたいです。')}
{SRC_NOTE}

  <p>同じ説明を繰り返すのではなく、</p>
  <p class="mt-oneline"><span>その子に伝わるやり方を探す。</span></p>
  <p>同じ「勉強が苦手」でも、止まる場所はそれぞれ違います。<br>「算数が苦手」で終わらせず、計算なのか、文章題なのか、手順なのか。<br>どこで止まっているかまで見れば、変える場所が分かります。</p>

  <!-- 05 実例C：家で教えるとケンカになる家庭 -->
  <h2 class="mt-h2">家で教えるとケンカになるなら、親が先生役を降りてもいい</h2>
  <figure class="mt-img" data-img="IMG-12"><img src="images/gen/12_story-a_parent-burden.webp" alt="夕方の食卓で、教材を前に困った顔の保護者と、問題に手が止まっている子ども（イメージ）" width="1200" height="800" loading="lazy"></figure>

{say('家で私が教えると、つい言いすぎてしまう…。')}

  <div class="mt-story">
    <p class="mt-story__who">公式サイト掲載の保護者の声（小学4年生・ADHDの診断あり・普通級）</p>
    <p>学校へ行ける日が減り、勉強の遅れが気になっていました。家で保護者が勉強を見ると、イライラして親子で言い合いになることもあったそうです。</p>
    <p>オンラインで週1回学ぶ習慣ができたことで、保護者が「ずっと自分が見なければ」と抱えていた負担が軽くなった、と紹介されています。</p>
  </div>
{review('小学4年生・保護者', '何より私がずっと見なくては・・というプレッシャーから開放されたことが、とても助かっています。')}
{SRC_NOTE}

  <p class="mt-oneline"><span>親が全部教えなくてもいい。</span></p>
  <p>勉強を見る人を、家庭の外にもつくる。<br>それだけで、親子の役割を少し戻せる家庭もあります。</p>

  <figure class="mt-img" data-img="IMG-07"><img src="images/gen/07_after_lesson_share.webp" alt="授業のあとも、家庭とつながれるか：授業→指導報告→保護者→教師・本部へ相談。親がひとりで抱えこまない仕組み" width="1200" height="900" loading="lazy"></figure>
  <p>そのとき見ておきたいのは、授業のあとも、家庭とつながれるか。<br>親がひとりで抱えこまない仕組みがあるかどうかです。</p>

  <!-- 06 3ケースをまとめて、ソウガクへ -->
  <div class="mt-voice"><span class="mt-voice__lbl"><i>○</i>3つのケースで違っていたのは「対応」</span><ul>
    <li>集中が切れたら、<b>声をかけて戻す</b><small>（小学5年生）</small></li>
    <li>伝わらなければ、<b>教え方を変える</b><small>（小学2年生）</small></li>
    <li>家庭で抱えきれない部分は、<b>先生に任せる</b><small>（小学4年生）</small></li>
  </ul></div>
  <p class="mt-small">※ソウガク公式サイト掲載の声をもとに、編集部がまとめたものです。個人の感想です。</p>

  <p>子どもに合わせるのは、教材だけではありません。<br><span class="mt-mark">声かけも、教え方も、家庭との関わり方も変える。</span></p>

  <p><b>これを最初から「発達特性がある子」を前提にやっているのが、ソウガクです。</b></p>

  <!-- 07 ソウガク：mt-bridge で切り替え → H2 → 扉＝公式KV → 早見（mt-spec。中に最初のASPボタン #cta-sogaku）→ 合う家庭 → 中身 → 無料体験 -->
  <div class="mt-bridge" id="sogaku"><p class="mt-bridge__s">発達障害・グレーゾーン専門の<br>オンライン家庭教師</p><p class="mt-bridge__name">＼<span>ソウガク</span>／</p></div>

  <h2 class="mt-h2">ソウガクは、何をしてくれるの？</h2>
{KV}

  <div class="mt-spec">
    <p class="mt-spec__ttl">まずは、ここだけ見ればOK</p>
    <ul class="mt-spec__points">
      <li><em>今どこで困っているか</em>を見る</li>
      <li><em>発達特性を学んだ先生</em>が担当</li>
      <li>授業のあとも<em>相談できる</em></li>
      <li>入会前に<em>相性を見られる</em></li>
    </ul>
    <dl class="mt-spec__grid">
      <div class="mt-spec__cell mt-spec__cell--wide"><dt class="mt-spec__k">無料体験</dt><dd class="mt-spec__mark">2回</dd><dd class="mt-spec__v">1回目は保護者面談も可</dd></div>
      <div class="mt-spec__cell mt-spec__cell--wide"><dt class="mt-spec__k">入会後継続率</dt><dd class="mt-spec__mark">96.7%</dd><dd class="mt-spec__v">公式LP掲載</dd></div>
      <div class="mt-spec__cell mt-spec__cell--wide"><dt class="mt-spec__k">認定講師</dt><dd class="mt-spec__mark">100%</dd><dd class="mt-spec__v">専門研修受講済み（公式LP掲載）</dd></div>
      <div class="mt-spec__cell mt-spec__cell--wide"><dt class="mt-spec__k">返金保証</dt><dd class="mt-spec__mark">1カ月</dd><dd class="mt-spec__v">授業料全額（条件あり・入会金は対象外）</dd></div>
    </dl>
    <div class="mt-cta" id="cta-sogaku"><p class="mt-cta__micro">＼まずは今の困りごとを話してみる／</p><a class="mt-cta__btn" href="{CTA_HREF}" data-cta target="_blank" rel="sponsored nofollow noopener">無料体験で相談してみる</a></div>
  </div>

  <h3 class="mt-h3"><span class="lp-num">1.</span>まず、今どこで困っているかを見る</h3>
  <p>「算数が苦手」で終わらせず、計算なのか、文章題なのか、手順なのか。<br>今どこで止まっているかを見てから、進め方を考えます。</p>
  <p class="mt-small">※公式では、この最初の確認を「アセスメント」と案内しています。ここでは、<b>「どこで困っているかを整理する確認」</b>と考えると分かりやすいです。</p>

  <h3 class="mt-h3"><span class="lp-num">2.</span>その子用の進め方を作る</h3>
  <p>確認した内容をもとに、体験後にお子さん用の個別指導計画を作成します。</p>
  <p>「みんな同じカリキュラム」ではなく、今の困りごとをもとに進め方を決めます。</p>

  <h3 class="mt-h3"><span class="lp-num">3.</span>先生任せにしない</h3>
  <p>先生は、一般社団法人 発達凸凹アソシエーションによる教師研修と、座学のマニュアル研修を受けた社会人講師です。</p>

  <h3 class="mt-h3"><span class="lp-num">4.</span>家で困ったことも相談できる</h3>
{TOOL}
  <p>毎回の指導報告があり、家で困ったことがあれば教師や本部にチャットで共有できます。</p>
  <p><b>授業をお願いしたあと、また親だけで先生役に戻らなくていい。</b></p>

  <div class="mt-check"><p class="mt-check__ttl">こんな家庭に合いやすい</p><ul>
    <li>塾や一般的な家庭教師で、うまくいかなかった</li>
    <li>何をどう教えればいいか、分からなくなってきた</li>
    <li>家で教えると、つい親子でぶつかってしまう</li>
    <li>授業が終わったあとも、相談できる相手がほしい</li>
  </ul><p class="mt-check__foot">1つでも当てはまったら、<span class="mt-mark">無料体験で今の困りごとを話してみる</span>のがおすすめです</p></div>

  <h3 class="mt-h3">無料体験は「授業を試す」だけではありません</h3>
  <p>無料体験は2回まで。1回目を保護者と先生の面談にすることもできます。</p>
  <p><b>体験後には、お子さん用の個別指導計画。</b><br>入会するかどうかは、それを見てから考えられます。</p>

  <div class="mt-points"><ul>
    <li>無料体験2回（1回目は保護者面談も可）</li>
    <li>入会後継続率96.7％（公式LP掲載）</li>
    <li>専門研修を受けた講師100％（公式LP掲載）</li>
    <li>授業料1カ月分返金保証※</li>
  </ul></div>
  <p class="mt-small">※返金保証には条件があります。入会金は対象外です。</p>

  <div class="mt-cta"><p class="mt-cta__micro">＼体験後に、お子さん用の個別指導計画／</p><a class="mt-cta__btn" href="{CTA_HREF}" data-cta target="_blank" rel="sponsored nofollow noopener">ソウガクの公式サイトを見てみる</a></div>

  <!-- 08 いちばん大きい反論を、4つ目の体験談で処理 -->
  <h2 class="mt-h2"><span class="lp-nw">「家でも集中できないのに、</span><span class="lp-nw">オンラインで大丈夫？」</span></h2>
  <figure class="mt-img" data-img="IMG-13"><img src="images/gen/13_story-b_online-desk.webp" alt="家の机でノートパソコンのオンライン授業を受けながら、ノートに書き込む子ども（イメージ）" width="1200" height="800" loading="lazy"></figure>

  <p>無理に「大丈夫です」とは言いません。<br>子どもによって、先生との相性も、画面越しの授業が合うかどうかも違うからです。</p>

  <div class="mt-story">
    <p class="mt-story__who">公式サイト掲載の保護者の声（中学2年生・特別支援学級）</p>
    <p>勉強への苦手意識があり、初回の体験では落ち着いて画面の前に座ることも難しかったそうです。</p>
    <p>先生は急いで授業を進めず、時間をかけて関係をつくりました。その後は授業の時間を楽しみにするようになった、と紹介されています。</p>
  </div>
{review('中学2年生・保護者', 'でも先生が時間をかけて信頼関係を築く努力をしてくださり、今ではこの時間を楽しみにしています。')}
{SRC_NOTE}

  <p>最初から「オンライン授業をちゃんと受けられる子」でなくてもいい。</p>
  <p><span class="mt-mark">合うかどうかは、入会を決める前に体験で見ればいい。</span></p>

{TEXTLINK}

  <!-- ここから下は LP01（王道LP）からそのまま流用（文言・HTMLとも変更なし） -->
'''

STICKY_BLOCK = ('<!-- 追従ボタン（LP01と同じ。ソウガク紹介の最初の大ボタン #cta-sogaku を過ぎたら出す） -->\n' + STICKY)
html = '\n'.join([HEAD, TOP, TRIAL, '', FEE, '', FAQ, '', FINAL, '', NOTE_OPERATOR, '', FOOTER, '',
                  STICKY_BLOCK, '', SCRIPT_CTA, SCRIPT_STICKY, ''])
open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8').write(html)

# ---- 検証 ----
src = '\n'.join(L)
for name, b in [('PRBAR', PRBAR), ('KV', KV), ('TOOL', TOOL), ('TEXTLINK', TEXTLINK), ('TRIAL', TRIAL), ('FEE', FEE), ('FAQ', FAQ),
                ('FINAL', FINAL), ('NOTE_OPERATOR', NOTE_OPERATOR), ('FOOTER', FOOTER), ('STICKY', STICKY), ('SCRIPT_CTA', SCRIPT_CTA)]:
    assert b in src and b in html, 'LP01と違う: ' + name
top = html[:html.index('ここから下は LP01')]
checks = {
    'FVボタン → #sogaku（mt-bridge）': 'href="#sogaku"' in top and 'class="mt-bridge" id="sogaku"' in top,
    'mt-talk は1つ・吹き出し4〜6個・アイコンは画像': top.count('class="mt-talk"') == 1 and 4 <= top.count('class="mt-talk__row') <= 6
    and top.count('mt-talk__icon"><img') == top.count('class="mt-talk__row'),
    'mt-talk にサービス名なし': 'ソウガク' not in top[top.index('class="mt-talk"'):top.index('</div>\n  <p class="mt-small">※よくある迷い')],
    '実例4つ（mt-story → mt-review）・mt-say 3つ': top.count('class="mt-story"') == 4 and top.count('class="mt-review"') == 4 and top.count('class="mt-say"') >= 3,
    'mt-voice で共通点': top.count('class="mt-voice"') == 1,
    'mt-bridge はページに1回・＼／つき': top.count('class="mt-bridge"') == 1 and '＼<span>ソウガク</span>／' in top,
    'mt-spec の中に #cta-sogaku': re.search(r'class="mt-spec".*?id="cta-sogaku".*?</div>\n  </div>', top, re.S) is not None,
    '大ボタンには必ず＼ひとこと／': all('mt-cta__micro' in c for c in re.findall(r'<div class="mt-cta"[^>]*>.*?</div>', html.replace(STICKY, ''), re.S)),  # 追従ボタンはひとことが外側（mt-sticky__micro）
    'mt-conclusion を使っていない（比較表がないため）': 'mt-conclusion' not in html,
    '画像指示枠なし': 'mt-imgslot' not in html,
    '300×250バナーなし': 't.felmat.net/fmimg' not in html,
    '他社名なし': not any(x in html for x in ['ランナー', 'トライ', 'サクシード', 'キズキ', 'メガスタ']),
    'ASPリンクは全部同じ計測URL': set(re.findall(r'href="(https://t\.felmat[^"]+)"', html)) == {CTA_HREF},
    '追従ボタンは #cta-sogaku 起点': "document.querySelector('#cta-sogaku')" in html,
    'noindex': '<meta name="robots" content="noindex, nofollow">' in html,
}
for k, ok in checks.items():
    print(('OK  ' if ok else 'NG  ') + k)
assert all(checks.values())
print('ok', len(html))

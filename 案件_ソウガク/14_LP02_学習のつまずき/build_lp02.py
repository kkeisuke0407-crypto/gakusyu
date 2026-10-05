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
    if side == 'parent':
        return (f'    <div class="mt-talk__row mt-talk__row--r"><div class="mt-talk__who"><span class="mt-talk__icon">{ICON_PARENT}</span>'
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
<title>発達特性のある子の勉強法｜宿題・集中・読み書きのつまずきを実例から見る</title>
<meta name="description" content="発達障害・グレーゾーンなど、発達特性のあるお子さんの勉強法を、宿題・集中・読み書き・漢字・算数の実例から整理。先生がどう関わったかを見ながら、その子に合う学び方を考えます。">
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
  <!-- 01 FV：タイトル → PR帯 → アイキャッチ → 悩みの問いかけ → 3つの実例の予告（mt-summary）→ ページ内ボタン（#sogaku） -->
  <h1 class="lp-ttl"><span class="lp-nw">発達特性のある子の勉強法。</span><br><span class="lp-nw">何度やっても進まないなら、</span><br><span class="lp-nw">「教え方」より先に</span><span class="lp-nw">見たいことがあります。</span></h1>

{PRBAR}

  <figure class="mt-img"><img src="images/gen/01_fv_evening-desk.webp" alt="夕方の子ども部屋の机に、開いたままの問題集と鉛筆（イメージ）" width="1200" height="800"></figure>

  <p>宿題に取りかかれない。<br>漢字がなかなか覚えられない。<br>算数だけ、いつも<br>同じところで止まってしまう。</p>

  <p>同じ「勉強が進まない」でも、<br>困っている場所は一人ひとり違います。</p>

  <div class="mt-summary"><p class="mt-summary__ttl">このあと見ていく、3つの実例</p><ul>
    <li>集中が切れそうになった子</li>
    <li>数の理解・計算につまずいた子</li>
    <li>家で教えるとケンカになる家庭</li>
  </ul></div>

  <p>3つの実例を追うと、ただ「もっと勉強させる」のとは違う共通点が見えてきます。</p>

  <p>そのうえで、<span class="mt-mark">発達障害・グレーゾーン専門のオンライン家庭教師「ソウガク」が、どうやってその子に合う学び方を組み立てているのか</span>まで見ていきます。</p>

  <div class="mt-cta"><p class="mt-cta__micro">＼先に仕組みを見たい方はこちら／</p><a class="mt-cta__btn" href="#sogaku">ソウガクの「学び方の組み立て方」を見る ↓</a></div>

  <!-- 02 導入の会話（mt-talk）：読者の迷い → 実例へ渡す。会話の中でサービス名は出さない -->
  <div class="mt-talk">
{talk('parent', '勉強法はいろいろ試したのに…<br>毎日「早くやって」ばかり。')}
{talk('editor', '止まる場所が違えば、<br>合う関わり方も変わります。')}
{talk('parent', 'でも、家で見分けて<br>毎回変えるのは難しくて…。')}
{talk('editor', 'まずは<span class="mt-mark">先生の関わり方</span>を、<br>実際の声で見てみましょう。')}
  </div>
  <p class="mt-small">※よくある迷いを編集部が会話形式にしたものです（人物はイメージ）。</p>

  <!-- 03 実例A：集中が切れる子（mt-say → mt-story → mt-review） -->
  <h2 class="mt-h2">集中が切れたとき、先生はどうした？</h2>
  <figure class="mt-img" data-img="IMG-14"><img src="images/gen/14_story-c_refocus.webp" alt="集中が切れたときの関わり方：01 集中が切れる→02 短い声かけ→03 もう一度課題へ" width="1200" height="900" loading="lazy"></figure>

{say('宿題を始めても、すぐ集中が切れる…。')}

  <p>「集中して」と言い続けても、なかなか続きません。<br>「集中できない」を、ずっと集中させることだけで解決しようとすると苦しくなります。</p>

  <div class="mt-story">
    <p class="mt-story__who">公式サイト掲載の生徒・保護者の声（小学5年生）</p>
    <p>授業中に集中が切れそうになる場面でも、先生の声かけで再び勉強に向かう様子があったそうです。</p>
    <p>本人も先生との授業を楽しみにしている、と保護者の声が掲載されています。</p>
  </div>
{review('小学5年生・保護者', '集中力が切れそうになっても、先生の言葉で、また頑張って、勉強できている姿に感動しています。')}
{SRC_NOTE}

  <p>この例では、「一度も集中を切らさない」ことではなく、切れそうな場面からもう一度戻る関わりがありました。</p>
  <p>「集中できる・できない」の二択ではなく、<span class="mt-mark">始める／続ける／切れたあとに戻る</span>のどこで困っているかを見ると、必要な関わり方を考えやすくなります。</p>

  <p><b>では、集中ではなく「漢字・計算など一部だけ強くつまずく」場合はどうでしょう。</b></p>

  <!-- 04 実例B：計算につまずく子（mt-say → mt-story → mt-review） -->
  <h2 class="mt-h2">同じ説明を繰り返しても進まないとき</h2>
  <figure class="mt-img" data-img="IMG-05"><img src="images/gen/05_stuck_4types.webp" alt="同じ『勉強が苦手』でも、止まる場所はそれぞれ違います：読むところで止まる、書くところで止まる、始めるまで時間がかかる、途中で集中が切れる" width="1200" height="900" loading="lazy"></figure>

{say('何度説明しても、同じところで止まる…。')}

  <p>同じ「勉強が苦手」でも、止まる場所はそれぞれ違います。</p>
  <p>教科名だけで「苦手」とまとめず、読む・書く・覚える・手順を追うなど、どの作業で止まるかまで見ると、変えるべきところが見えやすくなります。</p>

  <div class="mt-story">
    <p class="mt-story__who">公式サイト掲載の保護者の声（小学2年生）</p>
    <p>数の理解が難しく、計算が苦手なお子さん。始める前は、保護者もとても不安だったそうです。</p>
    <p>先生が毎回いろいろなやり方で、分かりやすいように丁寧に教えてくれている、と紹介されています。</p>
  </div>
{review('小学2年生・保護者', '先生が毎回色々なやり方で、娘が分かりやすいように丁寧な指導をしてくださいますのでとてもありがたいです。')}
{SRC_NOTE}

  <p>同じ説明を繰り返すのではなく、その子の様子を見ながら伝え方を変えている例です。</p>
  <p>漢字なら「読む・書く・覚える」、算数なら「計算・文章題・手順」。<br><span class="mt-mark">どこで止まっているのかを分けて考える</span>と、学び方を変えるヒントになります。</p>

  <p><b>ただ、家庭で毎回それを考えて、教え方まで変え続けるのは簡単ではありません。</b></p>

  <!-- 05 実例C：家で教えるとケンカになる家庭（mt-say → mt-story → mt-review）→ 3つの声の共通点（mt-voice） -->
  <h2 class="mt-h2">親が教えるほど、親子でぶつかってしまうとき</h2>
  <figure class="mt-img" data-img="IMG-12"><img src="images/gen/12_story-a_parent-burden.webp" alt="夕方の食卓で、教材を前に困った顔の保護者と、問題に手が止まっている子ども（イメージ）" width="1200" height="800" loading="lazy"></figure>

{say('家で私が教えると、つい言いすぎてしまう…。')}

  <div class="mt-story">
    <p class="mt-story__who">公式サイト掲載の保護者の声（小学4年生・ADHDの診断あり・普通級）</p>
    <p>学校へ行ける日が減り、勉強の遅れが気になっていました。家で保護者が勉強を見ると、イライラして親子で言い合いになることもあったそうです。</p>
    <p>オンラインで週1回学ぶ習慣ができたことで、保護者が「ずっと自分が見なければ」と抱えていた負担が軽くなった、と紹介されています。</p>
  </div>
{review('小学4年生・保護者', '何より私がずっと見なくては・・というプレッシャーから開放されたことが、とても助かっています。')}
{SRC_NOTE}

  <p>親がもっと上手に教えられるようになることだけが答えではありません。</p>
  <p class="mt-oneline"><span>親が先生役を続けなくてもいい。</span></p>
  <p>家庭の外に、お子さんの困り方を一緒に見てくれる人を増やす。<br>それも一つの方法です。</p>

  <figure class="mt-img" data-img="IMG-07"><img src="images/gen/07_after_lesson_share.webp" alt="授業のあとも、家庭とつながれるか：授業→指導報告→保護者→教師・本部へ相談。親がひとりで抱えこまない仕組み" width="1200" height="900" loading="lazy"></figure>
  <p>そのとき見ておきたいのは、授業のあとも、家庭とつながれるか。<br>親がひとりで抱えこまない仕組みがあるかどうかです。</p>

  <div class="mt-voice"><span class="mt-voice__lbl"><i>○</i>3つの公式の声から見えてきたこと</span><ul>
    <li>集中が切れそうな場面でも、声かけで再び勉強に向かった例がある<small>（小学5年生）</small></li>
    <li>数の理解・計算に難しさがある子へ、毎回やり方を変えて伝えている例がある<small>（小学2年生）</small></li>
    <li>家で教えると親子で言い合いになっていた家庭で、保護者の負担が軽くなった例がある<small>（小学4年生）</small></li>
    <li>学校へ行ける日が減った時期に、オンラインで週1回学ぶ習慣ができた例もある<small>（小学4年生）</small></li>
  </ul></div>

  <p>3つに共通していたのは、「もっとやらせる」ことではありませんでした。</p>
  <p><span class="mt-mark">その子が止まっている場所や、そのときの様子に合わせて、関わり方を変えている。</span></p>
  <p>では、それを毎回「先生個人の経験」だけに任せず、サービスとして続けるには何が必要なのでしょうか。</p>

  <!-- 06 ソウガク登場（mt-bridge で画面を切り替える。ページに1回）→ 公式KV -->
  <div class="mt-bridge" id="sogaku"><p class="mt-bridge__s">ここまでの「その子に合わせる」を、<br>仕組みにしているのが、</p><p class="mt-bridge__name">＼<span>ソウガク</span>／</p></div>

{KV}

  <!-- 07 なぜ合わせられるのか：扉＝公式の指導コミュニケーションツール画面 → mt-spec（中に最初のASPボタン #cta-sogaku） -->
  <h2 class="mt-h2">なぜ、その子ごとに学び方を変えられるの？</h2>
{TOOL}

  <p>その子に合わせた関わり方を、先生個人の経験だけに頼らず続けるための仕組みがあります。</p>

  <div class="mt-spec">
    <p class="mt-spec__ttl">ソウガクの仕組み</p>
    <ul class="mt-spec__points">
      <li><em>アセスメント</em>から個別指導計画を作成</li>
      <li>発達凸凹アソシエーションの<em>教師研修</em></li>
      <li>毎回の<em>指導報告</em>＋教師/本部とチャット</li>
      <li>発達障害・グレーゾーン<em>専門</em></li>
    </ul>
    <dl class="mt-spec__grid">
      <div class="mt-spec__cell mt-spec__cell--wide"><dt class="mt-spec__k">無料体験</dt><dd class="mt-spec__mark">2回</dd><dd class="mt-spec__v">1回目は保護者面談も可</dd></div>
      <div class="mt-spec__cell mt-spec__cell--wide"><dt class="mt-spec__k">入会後継続率</dt><dd class="mt-spec__mark">96.7%</dd><dd class="mt-spec__v">公式LP掲載</dd></div>
      <div class="mt-spec__cell mt-spec__cell--wide"><dt class="mt-spec__k">認定講師</dt><dd class="mt-spec__mark">100%</dd><dd class="mt-spec__v">専門研修受講済み（公式LP掲載）</dd></div>
      <div class="mt-spec__cell mt-spec__cell--wide"><dt class="mt-spec__k">返金保証</dt><dd class="mt-spec__mark">1カ月</dd><dd class="mt-spec__v">授業料全額（条件あり・入会金は対象外）</dd></div>
    </dl>
    <div class="mt-cta" id="cta-sogaku"><p class="mt-cta__micro">＼まずは「どこで困っているか」を相談／</p><a class="mt-cta__btn" href="{CTA_HREF}" data-cta target="_blank" rel="sponsored nofollow noopener">公式サイトで無料体験を見る</a></div>
  </div>

  <!-- 08 読者の最大の反論を4つ目の実例で処理（mt-say → mt-story → mt-review）→ テキストリンク → 無料体験 -->
  <h2 class="mt-h2">でも、オンラインで座っていられる？</h2>
  <figure class="mt-img" data-img="IMG-13"><img src="images/gen/13_story-b_online-desk.webp" alt="家の机でノートパソコンのオンライン授業を受けながら、ノートに書き込む子ども（イメージ）" width="1200" height="800" loading="lazy"></figure>

{say('画面の前に座って、授業を受けられるのかな…。')}

  <div class="mt-story">
    <p class="mt-story__who">公式サイト掲載の保護者の声（中学2年生・特別支援学級）</p>
    <p>勉強への苦手意識があり、初回の体験では落ち着いて画面の前に座ることも難しかったそうです。先生は急いで授業を進めず、時間をかけて関係をつくりました。</p>
    <p>その後は授業の時間を楽しみにするようになり、勉強への苦手意識にも変化を感じている、と紹介されています。</p>
  </div>
{review('中学2年生・保護者', 'でも先生が時間をかけて信頼関係を築く努力をしてくださり、今ではこの時間を楽しみにしています。')}
{SRC_NOTE}

  <p>オンラインだから集中できる、とは限りません。<br>子どもによって、先生との相性も、画面越しの授業が合うかどうかも違います。</p>
  <p>だから、入会してから悩むのではなく、<span class="mt-mark">先に体験で見ておく。</span></p>

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
    '実例4つ（mt-say → mt-story → mt-review）': top.count('class="mt-story"') == 4 and top.count('class="mt-review"') == 4 and top.count('class="mt-say"') == 4,
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

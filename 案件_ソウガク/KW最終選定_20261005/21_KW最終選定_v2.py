# -*- coding: utf-8 -*-
"""ソウガク 出稿KW最終選定 v2：対象者 → KW → ニーズ → LP（2026-10-05）

v1（20_KW最終選定.py）の分類（PF・ニーズクラスター）を土台に、その前段として
「その検索者は現在のソウガク商品の対象者か（ターゲット適合 T1/T2/T3）」を判定し、
運用区分（LP設計コア / 低CPC探索 / REVIEW / EXCLUDE）を付ける。
新LPの要否は「LP設計コア」のKWだけで判断する（探索KWのVolは根拠に使わない）。

■ 対象者条件（公式・全国オンライン商品。2026-10-05に取得した sogaku.jp/online/ 配下と獲得用LP）
- 商品：発達障害・グレーゾーン専門オンライン家庭教師 ソウガク
- 学年：小学生・中学生・高校生コース（料金ページ・コースページ・FAQ）
- 診断：「診断の有無、診断名の申告、手帳などの提出は不要」（FAQ）。グレーゾーンも受講可
- 特性：公式の対象表記は「発達障害・グレーゾーン」。知的障がいのある子の利用者の声あり
- 不登校：獲得用LPの申込フォーム「学習目的」の選択肢に「不登校」があるのみ。発達特性のない不登校児を
  対象とする記載は確認できない → 不登校単体はT2（コアにしない）
- 使わない：sogaku.jp トップ（北海道専門派遣家庭教師＝別商品）
"""
import collections
import csv
import importlib.util
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('v1', os.path.join(HERE, '20_KW最終選定.py'))
v1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v1)
rx, j = v1.rx, v1.j

# 公式の対象（発達障害・グレーゾーン）に含まれる特性語
T1_TRAIT = rx(v1.TRAIT_CORE.pattern, r'adhd', r'(?<![a-z])add(?![a-z])', r'注意欠如', r'注意欠陥', r'多動', r'asd', r'自閉',
              r'アスペ', r'(?<![a-z])ld(?![a-z])', r'学習障害', r'学習障がい', r'ディスレクシア', r'ディスレキシア', r'識字障害',
              r'読字障害', r'書字障害', r'書字表出', r'ディスグラフィア', r'算数障害', r'ディスカリキュリア', r'読み書き障害',
              r'グレーゾーン', r'凸凹', r'境界知能', r'知的障害', r'知的障がい', r'軽度知的', r'知的ボーダー', r'トゥレット',
              r'チック', r'(?<![a-z])dcd(?![a-z])', r'発達性協調')
# 公式の対象表記に含まれるか未確認の特性・状態語（T2）
T2_TRAIT = rx(r'(?<![a-z])hsc(?![a-z])', r'ギフテッド', r'(?<![a-z0-9])2e(?![a-z])', r'緘黙', r'感覚過敏', r'聴覚過敏',
              r'聴覚情報処理', r'(?<![a-z])apd(?![a-z])', r'起立性', r'ワーキングメモリ', r'iq(が)?低')
STUDY_NEAR = rx(r'受験', r'入試', r'進学', r'高校(選び|進学|受験|行ける|どうする)', r'勉強', r'学習(?!障)', r'内申', r'成績', r'塾',
                r'家庭教師', r'通信制')

# v2のクラスター（v1を土台に、特性あり/なしで答えが変わるものだけ分割・新設）
EXTRA = collections.OrderedDict()
EXTRA['N05b'] = dict(name='不登校×家庭教師・塾×料金（特性の言及なし）', pf='②その他ジャンル', base='N05')
EXTRA['N08a'] = dict(name='発達特性×塾・家庭教師が合わない・意味がない', pf='②その他ジャンル', base='N08')
EXTRA['N08b'] = dict(name='塾・家庭教師が合わない・続かない（特性の言及なし）', pf='②その他ジャンル', base='N08')
EXTRA['N20a'] = dict(name='競合×発達障害・グレーゾーン対応の確認', pf='③競合', base='N20')
EXTRA['N20b'] = dict(name='競合×不登校対応の確認（特性の言及なし）', pf='③競合', base='N20')
EXTRA['N22a'] = dict(name='発達特性の子への勉強の教え方・親が教えるとぶつかる', pf='④テール', base='N22')
EXTRA['N22b'] = dict(name='親が勉強を教える・教え方（特性の言及なし）', pf='④テール', base='N22')
EXTRA['N27a'] = dict(name='発達特性×受験・進学（高校受験・中学受験・進路）', pf='④テール', base='N27')
EXTRA['N27b'] = dict(name='発達特性×支援級・通級・学校での対応', pf='④テール', base='N27')
EXTRA['N27c'] = dict(name='支援級・通級・特別支援（特性語なし）', pf='④テール', base='N27')
EXTRA['N37'] = dict(name='発達特性×不登校（学習・家庭教師・遅れ）', pf='④テール（サービス語ありは②）', base=None)

# クラスターの評価（v2）：最初に知りたいこと・距離・王道LP適合・新LP要否・新LPの根拠
EVAL = {
    'N01': ('発達特性のある子に合う家庭教師・塾はどこか', '近い（ジャンルそのもの）', '◎ FVと比較表がそのまま答え', '不要', ''),
    'N02': ('どこがおすすめか・評判はどうか', '近い', '◎ 比較表・ランキング', '不要', ''),
    'N03': ('うちの子の特性（ADHD・LD等）に対応してくれる家庭教師・塾はあるか', '近い', '○ FV「発達障害・グレーゾーン」「診断なしOK」と比較表で答えられる', '不要', ''),
    'N04': ('特性のある子にオンライン授業は合うか・どこがあるか', '近い（ソウガクの形式そのもの）', '○ 本文「オンラインで大丈夫？」で回答', '不要', ''),
    'N05': ('特性のある子の家庭教師はいくらかかるか', '近い', '○ 料金セクション（学年別・入会金・0円項目）で回答', '不要', 'コア8語・小規模。料金FV版は配信データ次第'),
    'N06': ('うちの子の学年で受けられるか', '近い', '○ 小中高の料金表で回答', '不要', ''),
    'N07': ('近くの発達特性向けの塾・家庭教師はあるか', '近い（オンラインへの切替が必要）', '△ 地域の答えはないが、オンラインなら近くになくても受けられると示せる', '不要（王道LPで受ける）', 'コアが小規模で、FVを地域に変えるほどの根拠がない'),
    'N08a': ('特性のある子に塾・家庭教師は意味がないのか／合わない時どう選ぶか', '近い', '○ 「1対1だけで選んでいませんか」と選び方3ポイントが答えになる', '不要', ''),
    'N20a': ('その競合は発達障害・グレーゾーンに対応しているか', '近い', '◎ 比較表1行目「発達特性への位置づけ」', '不要', ''),
    'N22a': ('特性のある子にどう勉強を教えればいいか', '近い（親が先生役を続けない、が王道LPの芯）', '△ 気持ちには寄り添えるが「教え方」に答えていない', '要（LP02に統合）', '「どう対応すればいいか」が最初の答えで、N24と同じ'),
    'N24': ('特性のある子の勉強のつまずき（集中・読み書き・計算・宿題）にどう対応するか', '近い（ソウガクが解決する困りごとそのもの）', '× 王道LPは家庭教師の比較が中心で、対応方法に答えていない', '要（LP02）', 'FV・比較表を見せると「知りたいことと違う」と感じる。対象者確度が高く、王道LPと答えが違う'),
    'N27a': ('特性のある子の受験・進学・進路をどうするか', '中（対象者だが、知りたいのは受験・進路）', '△ 受験・進路への答えはない', '保留（独立LPは作らない。探索後に再判断）', 'T1だが最初の答えが「受験・進路」でLP02と異なるため、LP設計コアから外した（127語・月9,740件は根拠に使わない）'),
    'N37': ('特性があって学校に行けない子の学習をどう続けるか', '中〜近い', '△ 王道LPは不登校に触れていない（体験談に週2登校の例のみ）', 'LP02のセクションで受ける（単独LPにしない）', '対象者確度は高いが、コアの量が小さい。学習の遅れ・家での学び方はLP02の答えと重なる'),
}

# クラスター → (ターゲット適合の既定, 運用区分の既定, 理由)
CORE_CLUSTERS = {'N01', 'N02', 'N03', 'N04', 'N05', 'N06', 'N07', 'N08', 'N20', 'N22', 'N24', 'N27', 'N37'}
FAR_T1 = {'N25': '対象者（特性のある子の保護者）だが、知りたいのは子育て・接し方で学習支援から遠い',
          'N26': '対象者（特性のある子の保護者）だが、知りたいのは診断・特徴で学習支援から遠い'}
T2_CLUSTERS = {
    'N09': '不登校のみ（発達特性が検索語にない）。公式は不登校単体を対象と明記していない',
    'N28': '不登校のみ（発達特性が検索語にない）',
    'N29': '不登校・居場所・フリースクール（発達特性が検索語にない）',
    'N10': '一般の家庭教師・塾（発達特性の文脈なし）', 'N11': '一般の家庭教師・塾の料金（発達特性の文脈なし）',
    'N12': '一般の家庭教師・塾探し（発達特性の文脈なし）', 'N13': '一般のオンライン家庭教師（発達特性の文脈なし）',
    'N14': '競合（直接）の比較検討。発達特性は検索語から判断できない', 'N15': '競合（直接）の指名。発達特性は検索語から判断できない',
    'N16': '競合（カテゴリ）の評判。発達特性は検索語から判断できない', 'N17': '競合（カテゴリ）の料金。発達特性は検索語から判断できない',
    'N18': '競合（カテゴリ）の指名・校舎。発達特性は検索語から判断できない', 'N19': '競合の不満・退会。発達特性は検索語から判断できない',
    'N21': '終了サービス（メガスタ）の乗り換え。発達特性は検索語から判断できない',
    'N23': '一般家庭の勉強・宿題・集中の悩み（発達特性の文脈なし）',
    'N35': '隣接ブランド（教材・受験塾・療育事業者）の評判・料金。発達特性は検索語から判断できない',
}
T3_REVIEW = {'N30': '療育・放課後等デイサービス：ソウガクは療育・福祉サービスではない（検索者は特性のある子の保護者を含むが、目的が別サービス）',
             'N31': '一般の勉強法：検索者は子ども本人が中心で、発達特性の文脈なし',
             'N32': '一般の教材・アプリ：発達特性の文脈なし',
             'R01': '特性語のみ・大人の当事者の可能性', 'R02': '一般の学校・学習情報（悩み・特性の文脈なし）',
             'R03': '10/05のREVIEW（固有名詞・講師側の可能性等）', 'R04': '競合名×受験生本人のコンテンツ'}
T3_EXCLUDE = {'N33': '一般の受験・進路情報（中学受験・高校受験等の単体）。対象者と判断できず、目的が受験情報',
              'N34': '習い事・教室：目的が学習支援と異なる',
              'N36': '隣接ブランドの指名：大半が公式サイト・ログイン目的',
              'R05': '大人・仕事の文脈（対象外：ソウガクは小中高生）'}


def adult(s):
    return v1.ADULT_CTX.search(s) and not v1.CHILD.search(s)


def judge(r, cid, verdict, s):
    """→ (cluster_v2, T, 運用区分, 根拠)"""
    if verdict == '除外':
        return '', 'T3', 'EXCLUDE', r['備考_v1']
    t1 = bool(T1_TRAIT.search(s))
    t2 = bool(T2_TRAIT.search(s))
    fut = bool(v1.FUTOUKOU.search(s))
    brand = cid in ('N14', 'N15', 'N16', 'N17', 'N18', 'N19', 'N20', 'N21', 'N35', 'N36')
    if re.search(r'トライアスロン|トライアル(?!.*(体験|授業))', s):
        return cid, 'T3', 'EXCLUDE', '別業種の同名（トライアスロン・トライアル）'
    if cid in T3_EXCLUDE:
        return cid, 'T3', 'EXCLUDE', T3_EXCLUDE[cid]
    if t1 and re.search(r'英語|english', s) and not re.search(
            r'勉強|学習(?!障)|苦手|覚え|単語|教え|塾|家庭教師|授業|できない|読め|書け|テスト|成績|リスニング|発音|スペル|文法|教材|英検',
            T1_TRAIT.sub('', s)):
        return cid, 'T3', 'REVIEW', '特性語＋英語のみ：英訳（英語での言い方）を調べている可能性が高い'
    if cid in T3_REVIEW:
        return cid, 'T3', 'REVIEW', T3_REVIEW[cid]
    if t1 and adult(s):
        return cid, 'T3', 'REVIEW', '特性語あり。ただし大人・仕事の文脈'
    # 発達特性×不登校（③競合の特性確認は N20a に残す）
    if t1 and fut and not brand:
        return 'N37', 'T1', 'LP設計コア', '公式対象の特性語＋不登校（学習・サービスの文脈）'
    if cid in FAR_T1:
        if t1:
            return cid, 'T1', '低CPC探索', FAR_T1[cid]
        return cid, 'T2', '低CPC探索', '特性の状態語のみ（HSC・ギフテッド等は公式の対象表記に含まれるか未確認）'
    if cid == 'N35' and t1:
        return cid, 'T1', '低CPC探索', '対象者（特性語あり）だが、関心は隣接ブランド（教材・受験塾等）の対応・評判'
    if cid in T2_CLUSTERS:
        return cid, 'T2', '低CPC探索', T2_CLUSTERS[cid]
    if cid in CORE_CLUSTERS:
        sub = cid
        if cid == 'N08':
            sub = 'N08a' if t1 else 'N08b'
        elif cid == 'N20':
            sub = 'N20a' if t1 else 'N20b'
        elif cid == 'N22':
            sub = 'N22a' if t1 else 'N22b'
        elif cid == 'N27':
            if t1 and STUDY_NEAR.search(T1_TRAIT.sub('', s)):
                sub = 'N27a'
            elif t1:
                sub = 'N27b'
            else:
                sub = 'N27c'
        elif cid == 'N05' and not t1:
            sub = 'N05b'
        if sub == 'N27a':
            return sub, 'T1', '低CPC探索', '対象者（特性のある子の保護者）だが、最初に知りたいのは受験・進路で、LP02（学習のつまずきへの対処）と答えが違う。独立LPは作らず探索後に再判断'
        if sub == 'N27b':
            return sub, 'T1', '低CPC探索', '対象者（特性のある子の保護者）だが、知りたいのは支援級・通級・学校の制度で学習支援から遠い'
        if t1:
            return sub, 'T1', 'LP設計コア', '公式の対象（発達障害・グレーゾーン）に含まれる特性語＋子ども・学習・サービスの文脈'
        if t2:
            return sub, 'T2', '低CPC探索', 'HSC・ギフテッド等：公式の対象表記（発達障害・グレーゾーン）に含まれるか未確認'
        why = {'N05b': '不登校のみの料金（発達特性が検索語にない）', 'N08b': '一般の「合わない」（発達特性の文脈なし）',
               'N20b': '競合×不登校（発達特性が検索語にない）', 'N22b': '一般の「親が教える」（発達特性の文脈なし）',
               'N27c': '支援級・通級の語のみ（特性のある家庭の可能性は高いが、検索語から特性を確定できない）'}
        return sub, 'T2', '低CPC探索', why.get(sub, '特性語が検索語から確認できない')
    return cid, 'T3', 'REVIEW', '未分類'


def cname(cid):
    if cid in EXTRA:
        return EXTRA[cid]['name'], EXTRA[cid]['pf']
    c = v1.CL.get(cid)
    return (c['name'], c['pf']) if c else ('', '')


LP_OF_CORE = {'N01': 'LP01', 'N02': 'LP01', 'N03': 'LP01', 'N04': 'LP01', 'N05': 'LP01', 'N06': 'LP01', 'N07': 'LP01',
              'N08a': 'LP01', 'N20a': 'LP01', 'N24': 'LP02', 'N22a': 'LP02', 'N37': 'LP02'}
# 探索KWの送客先（新LPの根拠には使わない）
LP_OF_EXPLORE = {'N25': 'LP02', 'N26': 'LP02', 'N27b': 'LP02', 'N24': 'LP02', 'N27a': 'LP02'}


def route(cid, op):
    if op == 'LP設計コア':
        lp = LP_OF_CORE.get(cid, 'LP01')
    elif op == '低CPC探索':
        lp = LP_OF_EXPLORE.get(cid, 'LP01')
    else:
        return '—'
    return 'LP01' if lp == 'LP01' else 'LP02（制作まではLP01）'


def main():
    rows = list(csv.DictReader(open(v1.SRC, encoding='utf-8-sig')))
    assert len(rows) == 44783
    grp_n, grp_v = collections.Counter(), collections.Counter()
    for r in rows:
        if r['cluster_id']:
            grp_n[r['cluster_id']] += 1
            grp_v[r['cluster_id']] += v1.vol(r)
    out = []
    for r in rows:
        if r['判定'] != 'EXCLUDE' and r['投入'] != '代表':
            continue
        cid, verdict, note = v1.classify(r)
        r['備考_v1'] = note
        s = j(r['keyword'])
        cid2, t, op, why = judge(r, cid, verdict, s)
        name, pf = cname(cid2) if cid2 else ('', '')
        if cid2 == 'N37':
            pf = '②その他ジャンル' if v1.SERVICE.search(s) else '④テール'
        n = grp_n[r['cluster_id']] if r['cluster_id'] else 1
        gv = grp_v[r['cluster_id']] if r['cluster_id'] else v1.vol(r)
        tl = {'T1': 'T1 コア', 'T2': 'T2 探索', 'T3': 'T3 対象外/遠い'}[t]
        out.append({
            '代表KW': r['keyword'], '元KW数': n, '検索Vol': gv, 'PF': pf, 'ターゲット適合': tl, '運用区分': op,
            '対象者と判断した根拠': why,
            '検索意図': (EVAL[cid2][0] if cid2 in EVAL else (v1.CL[cid2]['first'] if cid2 in v1.CL else r['検索意図'])),
            '一致タイプ候補': ('完全一致' if op in ('LP設計コア', '低CPC探索') else '—'), '送客LP': route(cid2, op),
            'クラスターID': cid2, 'クラスター名': name, 'v1クラスター': cid or '', 'v1判定': verdict,
            '代表KWの検索Vol': v1.vol(r), '旧判定_1005': r['判定'], '旧PF_台帳': r['portfolio'], '競合ブランド': r['brand'],
            'CPC低': r['low_top_of_page_bid'], 'CPC高': r['high_top_of_page_bid'], '競合性': r['competition'], 'シート行': r['sheet_row']})
    return out


OPS = ['LP設計コア', '低CPC探索', 'REVIEW', 'EXCLUDE']


def write(path, rows):
    with open(os.path.join(HERE, path), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


LPS = [
    dict(id='LP01', name='王道比較LP（既存・完成）', pf='①ジャンル王道／②その他ジャンル／③競合',
         need='発達特性のある子に合う家庭教師・塾はどこか（比較・選び方・ランキング）',
         diff='—（既存）', need_new='不要（完成済み）', prio='完成済み'),
    dict(id='LP02', name='発達特性×学習のつまずき（④テール型）', pf='④テール',
         need='特性のある子の勉強のつまずき（集中・読み書き・計算・宿題・教え方・学校に行けない時期の学び方）にどう対応すればいいか',
         diff='王道LPは「どの家庭教師を選ぶか」に答える比較LP。この検索者は「家庭でどう対応するか」を先に知りたく、FV・比較表を最初に見せると「知りたいことと違う」となる',
         need_new='要', prio='1'),
]
CANDIDATES = [
    ('不登校専用LP（v1のLP03）', '作らない',
     '発達特性×不登校（N37）のコアは26語・月290件のみ。特性のない不登校KW（N09・N28・N29）は、公式が不登校単体を対象と明記していないためT2（探索）で、LP根拠に使えない。N37はLP02の「学校に行けない時期の学び方」セクションで受ける'),
    ('合わない・乗り換えLP（v1のLP04）', '作らない',
     '発達特性×合わない（N08a）のコアは7語・月480件。「1対1だけで選んでいませんか」と選び方3ポイントで王道LPが答えられる（○）。一般の「塾 合わない」（N08b）はT2'),
    ('家庭学習の悩み・共通テールLP（v1のLP05）', '作らない',
     '特性語を含む家庭学習の悩み（宿題・集中・教え方）はN24・N22aとしてLP02のコアに入る。特性語のない「中学生 勉強しない」等（N23・N22b）はT2で、LP根拠に使えない'),
    ('発達特性×受験・進学LP', '探索後に再判断（現時点では作らない）',
     'N27a（127語・月9,740件）は対象者T1だが、最初に知りたいのは「受験・進路」でLP02とも王道LPとも答えが違う。LP設計コアから外し、低CPC探索として配信してSearch Terms・MCVで受験・進路の反応を見てから独立LPの要否を判断する'),
]


def write_v2(path, rows):
    write(path, rows)


if __name__ == '__main__':
    out = main()
    out.sort(key=lambda o: (OPS.index(o['運用区分']), o['クラスターID'] or 'Z', -o['検索Vol'], o['代表KW']))
    write('01_KW最終選定_North_v2.csv', out)
    # ---- クラスター
    agg = collections.OrderedDict()
    order = list(v1.CL.keys()) + list(EXTRA.keys())
    for o in out:
        cid = o['クラスターID']
        if not cid:
            continue
        a = agg.setdefault(cid, dict(core_n=0, core_v=0, ex_n=0, ex_v=0, rev=0, exc=0, core_kw=[], all_kw=[], T=collections.Counter()))
        a['T'][o['ターゲット適合']] += 1
        a['all_kw'].append((o['検索Vol'], o['代表KW']))
        if o['運用区分'] == 'LP設計コア':
            a['core_n'] += 1; a['core_v'] += o['検索Vol']; a['core_kw'].append((o['検索Vol'], o['代表KW']))
        elif o['運用区分'] == '低CPC探索':
            a['ex_n'] += 1; a['ex_v'] += o['検索Vol']
        elif o['運用区分'] == 'REVIEW':
            a['rev'] += 1
        else:
            a['exc'] += 1
    crow = []
    for cid in sorted(agg, key=lambda c: (order.index(c) if c in order else 999, c)):
        a = agg[cid]
        name, pf = cname(cid)
        base = EXTRA[cid]['base'] if cid in EXTRA else cid
        c1 = v1.CL.get(base) or {}
        first, dist, fit, need, why = EVAL.get(cid, (c1.get('first', ''), '', '', '', ''))
        if cid not in EVAL:
            if a['core_n'] == 0 and a['ex_n'] > 0:
                dist = '遠い〜中（対象者を検索語から確定できない）'
                fit = '（コアKWなし）探索は王道LPで受ける' if cid not in ('N25', 'N26', 'N27b') else '（コアKWなし）探索はLP02で受ける'
                need, why = '不要（LP根拠にしない）', '探索KWのみ。Volは新LP根拠に使わない'
            elif a['core_n'] == 0:
                dist = '対象外／遠い'
                fit, need, why = '—', '不要', 'REVIEW・EXCLUDEのみ'
        tmain = a['T'].most_common(1)[0][0]
        crow.append({'クラスターID': cid, 'クラスター名': name, 'PF': pf, 'ターゲット適合': tmain,
                     'ターゲット適合の内訳': ' / '.join(f'{k}:{v}' for k, v in sorted(a['T'].items())),
                     'LP設計コアKW数': a['core_n'], 'LP設計コア検索Vol': a['core_v'],
                     '低CPC探索KW数': a['ex_n'], '低CPC探索検索Vol': a['ex_v'], 'REVIEW数': a['rev'], 'EXCLUDE数': a['exc'],
                     '代表コアKW': ' / '.join(f'{kw}（{v:,}）' for v, kw in sorted(a['core_kw'], reverse=True)[:5]),
                     '主要KW（全区分・参考）': ' / '.join(f'{kw}（{v:,}）' for v, kw in sorted(a['all_kw'], reverse=True)[:3]),
                     '最初に知りたいこと': first or c1.get('first', ''), 'ソウガクとの距離': dist, '既存王道LP適合': fit,
                     '新LP要否': need, '新LPを作る根拠': why,
                     '送客LP（コア）': (LP_OF_CORE.get(cid, 'LP01') if a['core_n'] else '—')})
    write('02_KWニーズクラスター_v2.csv', crow)
    # ---- LP
    lrow = []
    for L in LPS:
        cs = [c for c in agg if agg[c]['core_n'] and LP_OF_CORE.get(c, 'LP01') == L['id']]
        exs = [o for o in out if o['運用区分'] == '低CPC探索' and o['送客LP'].startswith(L['id'])]
        core_kw = sorted([t for c in cs for t in agg[c]['core_kw']], reverse=True)
        lrow.append({'LP ID': L['id'], '仮名': L['name'], '対象PF': L['pf'], '対象コアクラスター': ' / '.join(cs),
                     'コア代表KW': ' / '.join(kw for _, kw in core_kw[:5]),
                     'コアKW数': sum(agg[c]['core_n'] for c in cs), 'コア検索Volume': sum(agg[c]['core_v'] for c in cs),
                     '探索KW数': len(exs), '探索検索Volume': sum(o['検索Vol'] for o in exs),
                     '最初に満たすニーズ': L['need'], '既存王道LPとの差': L['diff'], '新LP要否': L['need_new'], '制作優先度': L['prio']})
    for name, verdict, why in CANDIDATES:
        lrow.append({'LP ID': '—', '仮名': name, '対象PF': '', '対象コアクラスター': '', 'コア代表KW': '', 'コアKW数': '',
                     'コア検索Volume': '', '探索KW数': '', '探索検索Volume': '', '最初に満たすニーズ': '',
                     '既存王道LPとの差': why, '新LP要否': verdict, '制作優先度': '—'})
    write('03_必要LP設計_v2.csv', lrow)
    # 新LP（LP02）の根拠になっているコアKWだけ／探索KWは別ファイル
    cols = ['代表KW', '元KW数', '検索Vol', 'PF', 'ターゲット適合', '運用区分', 'クラスターID', 'クラスター名', '対象者と判断した根拠']
    lp02_core = [{k: o[k] for k in cols} for o in out if o['運用区分'] == 'LP設計コア' and o['送客LP'].startswith('LP02')]
    lp02_ex = [{k: o[k] for k in cols} for o in out if o['運用区分'] == '低CPC探索' and o['送客LP'].startswith('LP02')]
    write('06_LP02_根拠コアKW_v2.csv', lp02_core)
    write('07_LP02_探索KW_根拠外_v2.csv', lp02_ex)
    print(len(out), collections.Counter(o['運用区分'] for o in out))
    for r in lrow[:2]:
        print(r['LP ID'], r['対象コアクラスター'], r['コアKW数'], r['コア検索Volume'], r['探索KW数'], r['探索検索Volume'])

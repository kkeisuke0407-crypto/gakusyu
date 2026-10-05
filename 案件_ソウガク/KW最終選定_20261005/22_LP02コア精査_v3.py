# -*- coding: utf-8 -*-
"""ソウガク LP02コア精査 v3（2026-10-05）

v2（21_KW最終選定_v2.py）の結果に2つの精査を重ねる。LP本数（LP01＋LP02）は変えない。

1. 知的障害・境界知能の再判定（全KW）
   全国オンライン公式（sogaku.jp/online/ 配下・獲得用LP・FAQ・料金）の対象表記は「発達障害・グレーゾーン」のみ。
   知的障がいは利用者の声に1件あるだけで、対象として明示されていない。
   → 特性語が知的障害・境界知能だけのKWは T1 → T2（低CPC探索）。発達障害・LD等の語も含むものはT1のまま。

2. LP02コア519語の1語ずつの精査
   残す条件：最初に欲しい答えが「発達特性のある子の学習のつまずきに、どう学ぶか／どう対応するか」であること
   （勉強できない・勉強法・教え方・宿題・集中（子ども・学習の文脈）・読み書き・漢字・算数・取りかかれない・
     「なぜ勉強できないのか」等の原因理解→対処）。
   外すもの：特性と学力の関係（できる・得意・学力）／診断・特徴の確認／薬／大人・仕事・人間関係の文脈／
             勉強会・研修／教材・アプリ・プリント探し／将来の見通し／子ども・学習の語がない「集中」
"""
import collections
import csv
import importlib.util
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('v2', os.path.join(HERE, '21_KW最終選定_v2.py'))
v2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v2)
j, rx = v2.j, v2.rx

INTELLECT = rx(r'境界知能', r'知的障害', r'知的障がい', r'軽度知的', r'知的ボーダー')

# ---- LP02コアから外すKW（1語ずつ判定）。キーは表記そのまま（空白は無視して照合）
EXPLORE = '低CPC探索'
REVIEW = 'REVIEW'
DROP = {}


def put(op, reason, kws):
    for k in kws.split('｜'):
        k = k.strip()
        if k:
            DROP[j(k)] = (op, reason)


put(EXPLORE, '特性と学力の関係を知りたい情報意図（できる・得意・学力）。対処法が最初のニーズではない',
    'adhd 勉強 できる｜発達 障害 勉強 は できる｜発達障害 学力 高い｜adhd 学力｜発達障害 勉強はできる 知恵袋｜adhd 国語 得意｜'
    'asd 勉強 できる｜adhd 数学 得意｜自 閉 症 勉強 できる｜発達 障害 学力｜adhd 暗記 得意｜asd 国語 得意｜アスペルガー 勉強 できる｜'
    '勉強 は できる けど 発達 障害｜adhd 成績｜発達 障害 学力 低い｜アスペルガー 学力｜アスペルガー 症候群 勉強 できる｜'
    'グレー ゾーン 勉強 できる｜アスペルガー 学習 能力｜発達 障害 勉強 得意｜発達 障害 学習 能力｜ADHDは学力が低いですか？｜'
    'ASDの人は勉強できますか？｜ASDの人は国語が得意ですか？｜ASDの人は学力は高いですか？｜グレーゾーンでも勉強はできる？｜'
    '学習 障害 勉強 できる｜発達 障害 勉強 は できる なぜ｜発達障害 国語 得意｜発達障害 小学生 勉強できる｜発達障害でも勉強はできますか？｜'
    'ADHDの国語の特徴は？｜ASDの苦手な教科は？｜adhd 苦手 な 教科｜発達 障害 苦手 科目｜adhd 苦手 科目')
put(EXPLORE, '診断・特徴の確認（「発達障害かどうか」「特徴」）が最初のニーズ',
    '学習 障害 小学生 特徴 算数｜学習 障害 算数 特徴｜学習 障害 算数 診断｜勉強しても点数が取れないのは発達障害ですか？｜'
    '勉強についていけないのは発達障害ですか？｜家で勉強できないのはADHDが原因ですか？｜発達障害は勉強についていけないのでしょうか？｜'
    'ld 限局 性 学習 症｜限局 性 学習 症 ディスレクシア｜外国 語 学習 障害｜発達障害で数を数えるのが苦手な人は？｜学習障害 不登校 原因')
put(EXPLORE, '将来の見通しが最初のニーズ',
    '発達障害 勉強 しない 将来｜発達 障害 勉強 できない 将来')
put(EXPLORE, '教材・アプリ・プリント・タブレット探しが最初のニーズ（商品・無料素材の情報）',
    'タブレット 学習 発達 障害｜発達 障害 タブレット 学習 おすすめ｜学習 障害 教材｜書 字 障害 教材｜ディスレクシア 教材｜'
    '発達 障害 タブレット 学習 中学生｜発達 障害 タブレット 学習 無料｜グレー ゾーン の 子ども に 対応 した 算数 ワーク｜'
    '学習 障害 タブレット 学習｜発達 障害 学習 プリント｜学習障害 おすすめ ドリル｜adhd プリント｜グレー ゾーン 算数 ワーク｜'
    '発達 障害 タブレット 学習 小学生｜発達 障害 向け 教材｜発達 障害 国語 プリント｜発達 障害 学習 教材｜発達障害 タブレット学習 ベネッセ｜'
    'adhd タブレット｜adhd ドリル｜adhd 教材｜ld 漢字 アプリ｜ディスレクシア タブレット｜学習 障害 タブレット アプリ｜学習 障害 算数 アプリ｜'
    '発達 障害 タブレット 教材｜発達 障害 児 学習 プリント｜発達 障害 児 用 学習 教材｜発達 障害 児 用 学習 教材 無料｜発達 障害 学習 アプリ｜'
    '発達 障害 支援 教材｜発達 障害 教材 プリント｜発達 障害 通信 教材｜読み書き 障害 タブレット｜学習障害 タブレット おすすめ｜'
    '発達障害 勉強 アプリ｜発達障害の学習アプリで無料のものは？｜発達 障害 学習 机')
put(EXPLORE, '「苦手」だが子ども・教科・学習の語がない（大人の当事者の可能性が高い）',
    '発達 障害 耳 から の 情報 が 苦手｜文章 が 苦手 発達 障害｜asd 文章 苦手｜数字 が 苦手 発達 障害｜発達障害 語学 が苦手｜覚えるのが苦手 発達障害')
put(EXPLORE, '「集中」だが子ども・学習の語がない（大人の当事者の可能性が高い）',
    'adhd 集中 できない｜ADHD 集中する方法｜発達 障害 集中 できない｜adhd 集中｜adhd 集中 できない 対策｜adhd 集中 力 が ない｜'
    '集中 力 が ない 発達 障害｜集中 力 が 続か ない adhd｜自 閉 症 集中 できない｜adhd 集中 できない とき｜アスペルガー 集中 できない｜'
    '集中 が 続か ない 発達 障害｜ADHDは集中力がないのはなぜですか？｜adhd 集中する方法 薬以外｜adhd 集中する方法 音楽｜'
    'グレー ゾーン 集中 できない｜発達障害 集中できない 対策｜adhd テレビ 集中｜adhd テレビ 集中 できない')
put(REVIEW, '薬・医療が最初のニーズ（LP02では答えない。医療系の広告表現にも注意）',
    'adhd 集中 できない 薬｜adhd 薬 勉強｜発達障害 集中できない 薬')
put(REVIEW, '大人・仕事・人間関係の文脈（学習のつまずきではない）',
    'adhd コミュニケーション 苦手｜adhd 手続き 苦手｜アスペルガー 会議 が 苦手｜adhd 書類 苦手｜adhd 人付き合い 苦手｜adhd 会話 苦手｜'
    'adhd 会議 苦手｜adhd 計画 苦手｜asd 会話 苦手｜学習 障害 話す の が 苦手｜学習 障害 話す こと が 苦手｜発達障害 相談が苦手｜'
    '発達障害 ゲーム 苦手｜自閉症 ゲーム 苦手｜asd 苦手｜adhd 苦手｜アスペルガー 苦手｜adhd 試験 苦手｜adhd 試験 勉強｜知 的 障害 者 勉強 方法')
put(REVIEW, '勉強会・研修・発達障害について学びたい（支援者側の可能性）',
    '発達 障害 勉強 会｜adhd 勉強 会｜発達 障害 学習 会｜発達障害の勉強 が したい')


def main():
    out = v2.main()
    lp02_before = [o for o in out if o['運用区分'] == 'LP設計コア' and o['送客LP'].startswith('LP02')]
    assert len(lp02_before) == 519, len(lp02_before)
    audit = []
    n_int = collections.Counter()
    for o in out:
        s = j(o['代表KW'])
        was_lp02_core = o['運用区分'] == 'LP設計コア' and o['送客LP'].startswith('LP02')
        decision, reason = '残す', ''
        # 1. 知的障害・境界知能
        if o['ターゲット適合'].startswith('T1') and INTELLECT.search(s) and not v2.T1_TRAIT.search(INTELLECT.sub('', s)):
            n_int[o['運用区分']] += 1
            o['ターゲット適合'] = 'T2 探索'
            if o['運用区分'] == 'LP設計コア':
                o['運用区分'] = '低CPC探索'
            o['対象者と判断した根拠'] = ('知的障害・境界知能：全国オンライン公式の対象表記は「発達障害・グレーゾーン」のみで、'
                                  '知的障がいは利用者の声の事例だけ（対象として明示なし）。T1と断定しない')
            decision, reason = '外す（探索）', '知的障害・境界知能（公式の対象に明示なし→T2）'
        # 2. LP02コアの1語ずつの精査
        elif was_lp02_core and s in DROP:
            op, why = DROP[s]
            o['運用区分'] = op
            o['対象者と判断した根拠'] = 'T1だがLP02コアから除外：' + why
            if op == REVIEW:
                o['送客LP'] = '—'
                o['一致タイプ候補'] = '—'
            decision, reason = ('外す（探索）' if op == EXPLORE else '外す（REVIEW）'), why
        if was_lp02_core:
            audit.append({'No': len(audit) + 1, '代表KW': o['代表KW'], '検索Vol': o['検索Vol'], 'v2クラスター': o['クラスターID'],
                          '精査結果': decision, '理由': reason or '最初の答えが「特性のある子の学習のつまずきにどう対応するか」でLP02が満たせる',
                          '運用区分_v3': o['運用区分'], 'ターゲット適合_v3': o['ターゲット適合']})
    missing = [k for k in DROP if not any(j(a['代表KW']) == k for a in audit)]
    assert not missing, missing
    return out, audit, n_int


def aggregate(out):
    agg = collections.OrderedDict()
    for o in out:
        cid = o['クラスターID']
        if not cid:
            continue
        a = agg.setdefault(cid, dict(core_n=0, core_v=0, ex_n=0, ex_v=0, rev=0, exc=0, core_kw=[], T=collections.Counter()))
        a['T'][o['ターゲット適合']] += 1
        if o['運用区分'] == 'LP設計コア':
            a['core_n'] += 1
            a['core_v'] += o['検索Vol']
            a['core_kw'].append((o['検索Vol'], o['代表KW']))
        elif o['運用区分'] == '低CPC探索':
            a['ex_n'] += 1
            a['ex_v'] += o['検索Vol']
        elif o['運用区分'] == 'REVIEW':
            a['rev'] += 1
        else:
            a['exc'] += 1
    return agg


if __name__ == '__main__':
    out, audit, n_int = main()
    out.sort(key=lambda o: (v2.OPS.index(o['運用区分']), o['クラスターID'] or 'Z', -o['検索Vol'], o['代表KW']))
    v2.write('01_KW最終選定_North_v3.csv', out)
    v2.write('08_LP02コア精査_v3.csv', audit)
    cols = ['代表KW', '元KW数', '検索Vol', 'PF', 'ターゲット適合', '運用区分', 'クラスターID', 'クラスター名', '対象者と判断した根拠']
    core = [{k: o[k] for k in cols} for o in out if o['運用区分'] == 'LP設計コア' and o['送客LP'].startswith('LP02')]
    ex = [{k: o[k] for k in cols} for o in out if o['運用区分'] == '低CPC探索' and o['送客LP'].startswith('LP02')]
    v2.write('06_LP02_根拠コアKW_v3.csv', core)
    v2.write('07_LP02_探索KW_根拠外_v3.csv', ex)
    # クラスター（v2の表にコア／探索の数字だけ更新）
    agg = aggregate(out)
    crow = list(csv.DictReader(open(os.path.join(HERE, '02_KWニーズクラスター_v2.csv'), encoding='utf-8-sig')))
    for c in crow:
        a = agg.get(c['クラスターID'])
        if not a:
            continue
        c['ターゲット適合'] = a['T'].most_common(1)[0][0]
        c['ターゲット適合の内訳'] = ' / '.join(f'{k}:{v}' for k, v in sorted(a['T'].items()))
        c['LP設計コアKW数'], c['LP設計コア検索Vol'] = a['core_n'], a['core_v']
        c['低CPC探索KW数'], c['低CPC探索検索Vol'] = a['ex_n'], a['ex_v']
        c['REVIEW数'], c['EXCLUDE数'] = a['rev'], a['exc']
        c['代表コアKW'] = ' / '.join(f'{kw}（{v:,}）' for v, kw in sorted(a['core_kw'], reverse=True)[:5])
        if a['core_n'] == 0 and c['送客LP（コア）'] != '—':
            c['送客LP（コア）'] = '—'
    v2.write('02_KWニーズクラスター_v3.csv', crow)
    lrow = list(csv.DictReader(open(os.path.join(HERE, '03_必要LP設計_v2.csv'), encoding='utf-8-sig')))
    for L in lrow:
        if L['LP ID'] not in ('LP01', 'LP02'):
            continue
        cs = [c for c in agg if agg[c]['core_n'] and v2.LP_OF_CORE.get(c, 'LP01') == L['LP ID']]
        exs = [o for o in out if o['運用区分'] == '低CPC探索' and o['送客LP'].startswith(L['LP ID'])]
        kw = sorted([t for c in cs for t in agg[c]['core_kw']], reverse=True)
        L['対象コアクラスター'] = ' / '.join(cs)
        L['コア代表KW'] = ' / '.join(k for _, k in kw[:5])
        L['コアKW数'] = sum(agg[c]['core_n'] for c in cs)
        L['コア検索Volume'] = sum(agg[c]['core_v'] for c in cs)
        L['探索KW数'] = len(exs)
        L['探索検索Volume'] = sum(o['検索Vol'] for o in exs)
    v2.write('03_必要LP設計_v3.csv', lrow)
    # 集計表示
    print('全体', len(out), collections.Counter(o['運用区分'] for o in out))
    print('知的・境界 T1→T2', dict(n_int))
    print('精査', collections.Counter(a['精査結果'] for a in audit))
    print('LP02 core', len(core), sum(o['検索Vol'] for o in core), collections.Counter(o['クラスターID'] for o in core))
    for c in ('N24', 'N22a', 'N37'):
        print(c, sum(1 for o in core if o['クラスターID'] == c), sum(o['検索Vol'] for o in core if o['クラスターID'] == c))
    print('LP02 explore', len(ex), sum(o['検索Vol'] for o in ex))
    for L in lrow[:2]:
        print(L['LP ID'], L['コアKW数'], L['コア検索Volume'], L['探索KW数'], L['探索検索Volume'])
    core_all = [o for o in out if o['運用区分'] == 'LP設計コア']
    print('core all', len(core_all), sum(o['検索Vol'] for o in core_all), collections.Counter(o['PF'] for o in core_all))

# -*- coding: utf-8 -*-
"""
ソウガク 出稿候補44,783KWの機械仕分け（2026-10-05）

方針（ユーザー決定）:
  母集団は保存。広告投入前に「明確な不適合」と「意味的重複」だけ機械的に落とし、
  少しでも成約ストーリーが作れるものは 10円前後の完全一致で市場に聞く。
  判定基準は1つ:
    「この検索をしている人にソウガクを提示して、無料体験を申し込む合理的なストーリーを1本でも作れるか？」
  検索vol・KWP単価・「情報収集っぽい」では落とさない。

入力:
  ../KW母集団_20261001/out/keywords_unique.csv   （スプシ「KW母集団」A〜W列と同順・同件数）
  00_シート判定_20261005.csv                      （スプシ「KW母集団」X列portfolio・AC列競合ブランド判定のスナップショット）
出力:
  01_KW仕分け_全件.csv      出稿候補44,783KW すべてに判定・クラスター・意図・検索者・LP・理由・確信度
  02_投入KW_10円探索.csv    KEEPのクラスター代表（10円完全一致で投入）
  03_投入KW_CORE.csv        COREのクラスター代表（別キャンペーン・CPC上げ可）
  04_要確認_EXCLUDE.csv     人が見るのはここ
  05_要確認_REVIEW.csv      人が見るのはここ
  06_集計.md
"""
import csv
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'KW母集団_20261001', 'out', 'keywords_unique.csv')
SHEET = os.path.join(HERE, '00_シート判定_20261005.csv')

csv.field_size_limit(sys.maxsize)


def norm(s):
    s = unicodedata.normalize('NFKC', s or '').lower()
    return re.sub(r'\s+', ' ', s).strip()


def joined(s):
    return norm(s).replace(' ', '')


def rx(*parts):
    return re.compile('|'.join(parts))


# ---------------------------------------------------------------------------
# 語彙
# ---------------------------------------------------------------------------
TRAIT = rx(r'発達障害', r'発達障がい', r'発達障碍', r'発達特性', r'発達凸凹', r'凸凹', r'発達の(遅れ|偏り)', r'発達遅',
           r'発達(が|に)(気になる|心配)', r'発達グレー', r'adhd', r'add(?![a-z])', r'注意欠如', r'注意欠陥', r'多動',
           r'asd', r'自閉', r'アスペ', r'(?<![a-z])ld(?![a-z])', r'学習障害', r'学習障がい', r'ディスレクシア', r'ディスレキシア',
           r'識字障害', r'読字障害', r'書字障害', r'書字表出', r'ディスグラフィア', r'算数障害', r'ディスカリキュリア',
           r'読み書き障害', r'グレーゾーン', r'グレー', r'境界知能', r'境界域', r'知的障害', r'知的障がい', r'軽度知的',
           r'知的ボーダー', r'ボーダー', r'iq(が)?低', r'hsc', r'hsp', r'緘黙', r'チック', r'トゥレット', r'dcd',
           r'発達性協調', r'不器用', r'感覚過敏', r'聴覚過敏', r'聴覚情報処理', r'apd', r'ワーキングメモリ',
           r'起立性', r'od(?![a-z])', r'ギフテッド', r'2e(?![a-z])', r'ダウン症', r'てんかん', r'発達')
FUTOUKOU = rx(r'不登校', r'登校しぶり', r'登校渋り', r'行き渋り', r'行きしぶり', r'五月雨登校', r'別室登校', r'保健室登校',
              r'学校(に)?(行けない|行かない|行きたくない|休みがち|休む|いけない)', r'学校休', r'ひきこもり', r'引きこもり',
              r'不登校気味', r'登校拒否', r'出席日数', r'フリースクール')
SERVICE_TUTOR = rx(r'家庭教師', r'かてきょ', r'カテキョ', r'プロ教師', r'個別指導', r'個別教室', r'マンツーマン',
                   r'オンライン(授業|学習|指導|教室|個別|レッスン)', r'学習支援', r'学習サポート', r'勉強サポート',
                   r'学習指導', r'塾', r'予備校', r'(勉強|学習)(を)?(教えて|見て)(くれる|もらう|もらえる|ほしい)',
                   r'教えてくれる(人|先生|ところ)', r'専門の先生', r'先生を探', r'1対1', r'一対一')
SERVICE_SUPPORT = rx(r'学習塾', r'療育', r'放課後(等)?デイ', r'放デイ', r'児童発達支援', r'通級', r'支援級', r'特別支援',
                     r'フリースクール', r'サポート校', r'通信制', r'通信教育', r'タブレット(学習|教材)', r'教材', r'ドリル',
                     r'問題集', r'アプリ', r'習い事', r'教室', r'スクール', r'学院', r'学園', r'ゼミナール', r'ゼミ',
                     r'アカデミー', r'相談(窓口|先|室)?', r'カウンセ', r'発達支援', r'学童')
COMPARE = rx(r'おすすめ', r'オススメ', r'比較', r'ランキング', r'人気', r'選び方', r'選ぶ', r'どこがいい', r'どっち',
             r'口コミ', r'くちコミ', r'クチコミ', r'評判', r'評価', r'レビュー', r'感想', r'料金', r'費用', r'値段', r'月謝',
             r'価格', r'相場', r'安い', r'高い', r'無料体験', r'体験', r'申込', r'申し込み', r'問い合わせ', r'資料請求',
             r'入会', r'2ch', r'5ch', r'知恵袋', r'ブログ', r'実績', r'効果', r'合格', r'成績(が)?(上が|伸)')
SWITCH = rx(r'合わない', r'あわない', r'合ってない', r'辞めたい', r'やめたい', r'辞め(る|た)', r'やめ(る|た)', r'退会', r'解約',
            r'意味ない', r'意味がない', r'効果ない', r'ついていけない', r'ついて行けない', r'断られ', r'行きたくない',
            r'行かない', r'嫌がる', r'いやがる', r'続かない', r'向いてない', r'向いていない', r'失敗', r'後悔', r'最悪',
            r'ひどい', r'酷い', r'トラブル', r'苦情', r'クレーム', r'怪しい', r'やばい', r'ヤバい', r'しつこい', r'勧誘',
            r'乗り換え', r'変える', r'変えたい', r'倒産', r'終了', r'撤退', r'つぶれ', r'休会', r'募集停止')

# 成約ストーリーの「足場」になる領域語。これを1つも含まないKWは、ソウガク（子どもの学習・発達特性）とつながらない。
ANCHOR = rx(TRAIT.pattern, FUTOUKOU.pattern, SERVICE_TUTOR.pattern, SERVICE_SUPPORT.pattern,
            r'子供', r'子ども', r'こども', r'子ど', r'(?<![a-zぁ-ん])子(?![宮])', r'息子', r'娘', r'わが子', r'我が子', r'うちの子',
            r'キッズ', r'児童', r'生徒', r'小学', r'中学', r'高校', r'小[1-6１-６一二三四五六]', r'中[1-3１-３一二三]',
            r'高[1-3１-３一二三](?![a-z0-9])', r'[1-6一二三四五六]年生', r'年生', r'学年', r'新学期', r'入学', r'卒業',
            r'学校', r'学級', r'クラス', r'担任', r'先生', r'授業', r'勉強', r'学習', r'宿題', r'課題', r'テスト', r'試験',
            r'定期', r'期末', r'中間', r'模試', r'受験', r'入試', r'内申', r'偏差値', r'志望校', r'推薦', r'進学', r'進路',
            r'成績', r'点数', r'通知表', r'教科', r'科目', r'算数', r'数学', r'国語', r'英語', r'理科', r'社会', r'漢字',
            r'計算', r'九九', r'音読', r'読み書き', r'読み', r'書き', r'作文', r'読解', r'文章題', r'文章', r'単語', r'英単語',
            r'英検', r'漢検', r'数検', r'足し算', r'引き算', r'掛け算', r'かけ算', r'割り算', r'わり算', r'分数', r'小数',
            r'図形', r'方程式', r'関数', r'歴史', r'地理', r'公民', r'物理', r'化学', r'生物', r'古文', r'漢文', r'文法',
            r'暗記', r'記憶', r'覚え', r'集中', r'やる気', r'勉強法', r'苦手', r'克服', r'できない', r'わからない', r'分からない',
            r'ついていけない', r'遅れ', r'つまず', r'つまづ', r'落ちこぼれ', r'親', r'母', r'父', r'ママ', r'パパ', r'保護者',
            r'子育て', r'育児', r'しつけ', r'反抗期', r'思春期', r'癇癪', r'かんしゃく', r'パニック', r'こだわり', r'ゲーム',
            r'スマホ', r'夏休み', r'冬休み', r'春休み', r'部活', r'知能', r'iq', r'wisc', r'ウィスク', r'検査', r'診断',
            r'障害', r'障がい', r'特性', r'不注意', r'衝動', r'過敏', r'情緒', r'言語', r'吃音', r'不安', r'登校',
            r'放課後', r'幼稚園', r'保育園', r'年長', r'年中', r'就学', r'自習', r'独学', r'参考書', r'教え方', r'教える',
            r'英会話', r'プログラミング', r'そろばん', r'書道', r'ピアノ', r'スイミング', r'中受', r'高受', r'大学受験',
            r'中高一貫', r'私立', r'公立', r'学力', r'教師', r'個別', r'講習', r'珠算', r'暗算', r'フォニックス', r'速読',
            r'知育', r'体操教室', r'ペアトレ', r'ペアレントトレーニング', r'処理速度', r'知性', r'座って', r'じっと',
            r'落ち着き', r'忘れ物', r'片付け', r'朝起きられない', r'友達', r'いじめ', r'癖', r'性格', r'敏感', r'gifted',
            r'sst', r'ソーシャルスキル', r'コロロ', r'テクシア', r'autis', r'dyslex', r'adhl', r'転入', r'転学', r'編入', r'学費',
            r'運動会', r'タブレット', r'通信', r'高専', r'クラーク', r'伝記', r'絵本', r'児童書', r'知育')

# --- HARD EXCLUDE 系 ---------------------------------------------------------
SUPPLY = rx(r'求人', r'募集', r'採用', r'アルバイト', r'バイト', r'給料', r'給与', r'時給', r'日給', r'月給', r'年収', r'月収',
            r'収入', r'稼げ', r'稼ぐ', r'報酬', r'講師登録', r'登録講師', r'講師になる', r'講師になりたい', r'教師になる',
            r'先生になる', r'先生になりたい', r'なるには', r'なり方', r'(講師|バイト|塾講師|教員|家庭教師)(の)?面接', r'志望動機', r'履歴書', r'職務経歴',
            r'転職', r'副業', r'在宅ワーク', r'業務委託', r'正社員', r'契約社員', r'派遣', r'社員', r'新卒', r'中途',
            r'インターン', r'シフト', r'働き方', r'働く', r'働きやすい', r'職場', r'離職', r'辞めたい講師', r'講師(が|を)?辞め',
            r'講師きつい', r'講師(の)?仕事', r'教師の仕事', r'家庭教師(の)?仕事', r'塾講師', r'チューター(募集|バイト)',
            r'保育士', r'児発管', r'児童発達支援管理責任者', r'サビ管', r'指導員', r'支援員', r'職員', r'スタッフ',
            r'研修', r'教員', r'教職', r'教育実習', r'教員免許', r'認定講座', r'養成講座', r'養成', r'eラーニング')
TEACHER_SIDE = rx(r'指導案', r'授業案', r'授業づくり', r'教材研究', r'板書計画', r'学級経営', r'所見', r'文例', r'記入例',
                  r'様式', r'学習指導要領', r'評価規準', r'観点別評価', r'研究授業', r'校内研', r'コーディネーター',
                  r'保護者対応', r'教員向け', r'先生向け', r'支援者向け', r'教師向け', r'診療情報提供書')
PLAN_DOC = rx(r'個別の?指導計画', r'指導計画', r'個別の?(教育)?支援計画', r'支援計画')
BUSINESS = rx(r'開業', r'開設', r'独立', r'起業', r'(塾|教室|事業所|放デイ)経営', r'経営者', r'経営(ノウハウ|難)', r'フランチャイズ', r'fc加盟', r'加盟', r'オーナー', r'運営(会社|法人|母体)?',
              r'指定申請', r'指定基準', r'人員基準', r'加算', r'減算', r'報酬改定', r'単価', r'国保連', r'報酬請求', r'実地指導',
              r'監査', r'売上', r'売り上げ', r'収益', r'利益', r'儲か', r'm&a', r'買収', r'株価', r'株式', r'上場', r'ir(?![a-z])',
              r'決算', r'資本金', r'代表取締役', r'社長', r'会社概要', r'本社', r'本部', r'従業員数', r'事業所(番号|数)',
              r'営業時間', r'電話番号', r'住所', r'所在地', r'アクセス', r'駐車場', r'地図', r'マップ', r'行き方')
RESEARCH = rx(r'(?<!小)論文', r'卒論', r'修論', r'(?<!自由)研究(?!授業)', r'文献', r'(?<!進)学会', r'統計', r'調査結果',
              r'有病率', r'英語で(言う|なんて|何|表現|書く)', r'を英語で', r'英訳', r'英語表記', r'略語', r'icd', r'dsm', r'定義', r'語源', r'由来')
ADULT = rx(r'大人', r'成人', r'社会人', r'(?<!小)(?<!中)(?<!高)大学生', r'大学(で|に)?(行けない|中退|退学|休学|単位)',
           r'上司', r'部下', r'同僚', r'会社員', r'職業', r'就職', r'就活', r'就労', r'障害者雇用', r'障害年金', r'年金',
           r'a型', r'b型', r'作業所', r'グループホーム', r'一人暮らし', r'生活保護', r'恋愛', r'結婚', r'離婚', r'(?<![工丈])夫(?!婦)', r'旦那',
           r'妻', r'嫁', r'彼氏', r'彼女', r'婚活', r'妊娠', r'出産', r'妊婦', r'不妊', r'更年期', r'老後', r'高齢', r'認知症',
           r'介護', r'運転', r'飲酒', r'アルコール', r'性欲', r'風俗', r'借金', r'浪費', r'ギャンブル', r'パチンコ', r'犯罪',
           r'刑務所', r'逮捕', r'女性(の)?特徴', r'男性(の)?特徴', r'30代', r'40代', r'50代', r'20代', r'30歳', r'40歳')
INFANT = rx(r'赤ちゃん', r'乳児', r'新生児', r'(?<![0-9])[0-3]歳', r'生後',
            r'乳幼児', r'(?<![0-9])[0-3]才', r'歳半', r'才半', r'健診', r'検診', r'離乳食', r'夜泣き', r'イヤイヤ期',
            r'喃語', r'ハイハイ', r'寝返り', r'ベビー', r'保育園')
MEMBER = rx(r'ログイン', r'マイページ', r'会員(ページ|サイト|専用)', r'パスワード', r'id(を)?忘れ', r'口座', r'振替', r'振り替え',
            r'引き落とし', r'引落', r'振込', r'振り込み', r'領収書', r'請求書', r'支払い方法', r'支払方法', r'欠席連絡', r'教材(が)?届かない', r'アプリ(の)?ダウンロード', r'ダウンロード', r'インストール', r'不具合', r'エラー',
            r'つながらない', r'繋がらない', r'zoom(の)?使い方', r'設定方法', r'年間行事', r'行事予定', r'時程')
MEDICAL_ONLY = rx(r'コンサータ', r'ストラテラ', r'インチュニブ', r'ビバンセ', r'エビリファイ', r'リスパダール', r'メラトベル',
                  r'副作用', r'処方', r'薬価', r'ジェネリック', r'飲み合わせ')
EXAM_LOGISTICS = rx(r'模試(の)?(日程|申し込み|申込|会場|返却|判定基準)', r'(日程|会場|解答速報|合格発表|合格最低点|募集要項|出願|願書|オープンキャンパス|制服|校則|奨学金|偏差値表|偏差値一覧)',
                    r'(大学|学部)(の)?偏差値', r'共通テスト', r'センター試験', r'二次試験', r'医学部', r'東大', r'京大', r'早慶',
                    r'march', r'関関同立', r'旧帝', r'難関大', r'鉄緑会', r'医専', r'看護学校', r'看護', r'歯学部', r'薬学部',
                    r'獣医', r'大学院', r'公務員', r'宅建', r'簿記', r'toeic', r'toefl', r'ielts', r'司法', r'税理士',
                    r'会計士', r'行政書士', r'社労士', r'fp(?![a-z])', r'看護師', r'保健師', r'教員採用')
CELEB = rx(r'有名人', r'芸能人', r'著名人', r'偉人', r'ユーチューバー', r'youtuber', r'漫画', r'マンガ', r'ドラマ', r'映画',
           r'アニメ', r'キャラ', r'小説', r'歌詞', r'名言', r'ことわざ', r'イラスト', r'フリー素材', r'素材', r'壁紙', r'画像',
           r'ニュース', r'事件', r'炎上', r'wiki', r'ウィキ', r'tiktok', r'インスタ', r'ツイッター',
           r'twitter', r'(?<![a-z])cm(?![a-z])', r'cm曲', r'歌', r'俳優', r'女優', r'タレント')

# --- 検索者推定 -----------------------------------------------------------------
PARENT_HINT = rx(r'子供', r'子ども', r'こども', r'子ど', r'息子', r'娘', r'わが子', r'我が子', r'うちの子', r'親', r'母', r'父',
                 r'ママ', r'パパ', r'保護者', r'子育て', r'育児', r'しつけ', r'接し方', r'関わり方', r'声かけ', r'声掛け',
                 r'させる', r'させたい', r'させ方', r'教え方', r'教える', r'家庭教師', r'塾', r'個別指導', r'療育', r'放課後',
                 r'料金', r'費用', r'月謝', r'口コミ', r'評判', r'体験', r'申込', r'入会', r'退会', r'解約', r'受診', r'診断',
                 r'病院', r'相談', r'小学生', r'幼稚園', r'年長', r'就学', r'支援級', r'通級', r'特別支援', r'反抗期',
                 r'思春期', r'不登校', r'行き渋り', r'登校しぶり', r'癇癪', r'かんしゃく')
CHILD_HINT = rx(r'勉強法', r'勉強方法', r'勉強のやり方', r'覚え方', r'暗記', r'やる気(が)?(出ない|出す|でない)', r'集中(する)?方法',
                r'眠い', r'眠くなる', r'寝る', r'めんどくさい', r'面倒', r'だるい', r'つらい', r'辛い', r'したくない', r'やりたくない',
                r'受験生', r'高校生', r'中学生', r'中[1-3]', r'高[1-3]', r'定期テスト', r'期末', r'中間テスト', r'模試', r'偏差値',
                r'共通テスト', r'参考書', r'問題集', r'独学', r'自習', r'勉強時間', r'英単語', r'公式', r'解き方', r'問題',
                r'答え', r'解答', r'わからない', r'分からない', r'できない')


# ---------------------------------------------------------------------------
# 意味的重複（Google完全一致の「同じ意味・同じ意図」で吸収される範囲だけ）
# ---------------------------------------------------------------------------
SYNONYMS = [
    (r'発達障がい|発達障碍|発達しょうがい', '発達障害'),
    (r'子ども|こども|子供|コドモ|子ど(?!も)', '子供'),
    (r'(?<![a-z])ld(?![a-z])|学習障がい|学習障碍', '学習障害'),
    (r'注意欠如多動症|注意欠陥多動性障害|注意欠如多動性障害|注意欠陥多動障害|注意欠如・多動症|注意欠如/多動症', 'adhd'),
    (r'自閉スペクトラム症|自閉症スペクトラム障害|自閉症スペクトラム|自閉スペクトラム|自閉症スペクトラム症', 'asd'),
    (r'グレー ゾーン|グレイゾーン', 'グレーゾーン'),
    (r'家庭 教師|かてきょ|カテキョ', '家庭教師'),
    (r'個別 指導', '個別指導'),
    (r'不 登校|ふとうこう', '不登校'),
    (r'オンライン家庭教師', 'オンライン 家庭教師'),
    (r'ランキング|人気', 'おすすめ'),
    (r'クチコミ|くちコミ', '口コミ'),
    (r'値段|月謝|価格', '料金'),
    (r'ひとり|1人', '一人'),
    (r'小学校', '小学生'),
    (r'中学校', '中学生'),
    (r'高校生|高等学校', '高校'),
    (r'できない子|出来ない子', 'できない'),
    (r'出来ない', 'できない'),
    (r'分からない|わかんない', 'わからない'),
    (r'勉強方法|勉強の仕方|勉強のやり方|勉強のしかた|勉強法', '勉強法'),
    (r'教え方|教える方法|教えかた', '教え方'),
    (r'中[1１一]|中学1年|中学一年', '中1'), (r'中[2２二]|中学2年|中学二年', '中2'), (r'中[3３三]|中学3年|中学三年', '中3'),
    (r'高[1１一]|高校1年|高校一年', '高1'), (r'高[2２二]|高校2年|高校二年', '高2'), (r'高[3３三]|高校3年|高校三年', '高3'),
    (r'小学[1１一]年(生)?|小[1１一]', '小1'), (r'小学[2２二]年(生)?|小[2２二]', '小2'), (r'小学[3３三]年(生)?|小[3３三]', '小3'),
    (r'小学[4４四]年(生)?|小[4４四]', '小4'), (r'小学[5５五]年(生)?|小[5５五]', '小5'), (r'小学[6６六]年(生)?|小[6６六]', '小6'),
]
SYN_RX = [(re.compile(a), b) for a, b in SYNONYMS]
# Googleが「暗黙の語・機能語」として吸収しやすい語（意味を変えない）
FILLER = {'の', 'を', 'が', 'は', 'に', 'で', 'と', 'も', 'へ', 'や', 'か', 'な', 'って', 'について', 'とか', 'から', 'まで',
          'の子', 'な子', '子の', 'する', 'した', 'いる', 'ある', 'たち', '達'}
# 「子供」は残りが2語以上の具体KWのときだけ暗黙語として吸収（「英語」と「子ども 英語」は別意図のまま）
KID_FILLER = {'子供', 'お子さん', 'お子様', 'お子さま', '子', 'ない子'}
# 「専門・対応・向け」はサービス語があるときだけ吸収（「発達障害 家庭教師 専門」≒「発達障害 家庭教師」）
SERVICE_FILLER = {'向け', '対応', '専門', '向き'}
SERVICE_TOKENS = {'家庭教師', '塾', '個別指導', '教室', 'スクール', '学習支援', '療育', 'オンライン'}


def tokenize_factory():
    try:
        from janome.tokenizer import Tokenizer
        t = Tokenizer()
        return lambda s: [m.surface for m in t.tokenize(s)]
    except Exception:  # janome が無い環境ではKWP分かち書きをそのまま使う
        return lambda s: s.split(' ')


_tok = tokenize_factory()
_tok_cache = {}


def dedup_key(kw):
    s = norm(kw)
    for r, b in SYN_RX:
        s = r.sub(b, s)
    s = s.replace(' ', '')
    for r, b in SYN_RX:  # 結合後に成立する表記揺れも吸収
        s = r.sub(b, s)
    s = s.replace('とは', '〓')  # 「とは」は意図を変えるので機能語扱いしない
    if s not in _tok_cache:
        _tok_cache[s] = _tok(s)
    toks = [('とは' if w == '〓' else w) for w in _tok_cache[s] if w.strip() and w not in FILLER]
    content = [w for w in toks if w not in KID_FILLER and w not in SERVICE_FILLER]
    if len(set(content)) >= 2:
        toks = [w for w in toks if w not in KID_FILLER]
    if set(toks) & SERVICE_TOKENS or any('家庭教師' in w or '塾' in w for w in toks):
        toks = [w for w in toks if w not in SERVICE_FILLER]
    toks = sorted(set(toks))
    return ' '.join(toks) if toks else s


# ---------------------------------------------------------------------------
# 分類
# ---------------------------------------------------------------------------
def load():
    sheet = {}
    with open(SHEET, encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            sheet[int(r['sheet_row'])] = r
    out = []
    with open(SRC, encoding='utf-8-sig') as f:
        for i, r in enumerate(csv.DictReader(f)):
            row = i + 2
            sj = sheet[row]
            assert sj['keyword'] == r['keyword'], (row, sj['keyword'], r['keyword'])
            r['sheet_row'] = row
            r['portfolio'] = sj['portfolio']
            r['brand'] = sj['競合ブランド判定']
            out.append(r)
    return out


def has(rx_, s):
    return rx_.search(s) is not None


# 競合ブランド表記（competitor_brands.csv）。単体だと別業種と衝突しやすい短い表記は AMBIGUOUS として扱う
def load_aliases():
    path = os.path.join(HERE, '..', 'KW母集団_20261001', 'competitor_brands.csv')
    al = set()
    with open(path, encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            for k in ('brand_name', 'brand_alias'):
                a = joined(r[k])
                if len(a) >= 2:
                    al.add(a)
    al |= {'サピ', 'マナビス', 'コペル', '学研', '河合', '早稲田アカデミー', '明光', '京進', '能開', '栄光の個別', '個別ナビ', 'ナビ個別', 'リタリコ', 'litalico', 'こぱん', 'キズキ', '青楓館',
           'イットー', 'いっとー', 'itto', 'すらら', 'スララ', 'しちだ', '四谷学院', 'ecc', 'イーシーシー', 'サピックス',
           'sapix', '日能研', '早稲アカ', '馬渕', '臨海', 'グノーブル', 'ena', 'tomas', 'トーマス', 'ie個別', 'スクールie',
           'ベストワン', 'リバランス', 'サクシード', 'succeed', 'gips', 'ジップス', 'アクシス', 'axis', 'トライ', 'あすなろ',
           'ウィズユー', 'ブランチ', 'ティーンズ'}
    return al


ALIASES = sorted(load_aliases(), key=len, reverse=True)
AMBIGUOUS = {'トライ', 'try', 'あすなろ', 'サクシード', 'succeed', 'ベストワン', 'リバランス', 'gips', 'ジップス', 'アクシス',
             'axis', 'トーマス', 'tomas', 'ena', 'ie個別', '天神', 'ポピー', 'ブランチ', 'branch', 'ティーンズ', 'teens',
             'ウィズユー', 'ウィズ・ユー', 'スタジオそら', 'スタジオプラス', 'スタジオplus', 'ecc', 'イーシーシー', 'ナビ個別',
             '個別ナビ', 'ランナー', 'マスター', 'ファースト', 'ガンバ', 'ジャンプ', 'jump', 'コペルプラス', 'ハッピーテラス',
             'やる気スイッチ', 'しちだ', 'ザベストワン', 'next'}
EDU_MOD = rx(COMPARE.pattern, SWITCH.pattern, r'講習', r'夏期', r'冬期', r'春期', r'合格実績', r'実績', r'(?<![a-z])校$', r'校舎',
             r'教室', r'入会', r'入塾', r'メリット', r'デメリット', r'違い', r'他社', r'怪しい', r'個別', r'塾', r'家庭教師',
             r'授業', r'先生', r'講師', r'コース', r'カリキュラム', r'教材', r'テキスト', r'オンライン', r'体験', r'相談')
STUDY = rx(r'勉強', r'学習', r'解き方', r'読解', r'子供', r'子ども', r'こども', r'療育', r'宿題', r'受験相談', r'授業', r'塾',
           r'家庭教師', r'教材', r'問題', r'単語', r'暗記')


def alias_in(s):
    for a in ALIASES:
        if a in s:
            return a
    return ''


def classify(r):
    """returns (判定, 理由, 確信度)"""
    s = joined(r['keyword'])
    pf = r['portfolio']
    brand = r['brand']
    is_comp = pf.startswith('③')
    trait = has(TRAIT, s)
    futo = has(FUTOUKOU, s)
    tutor = has(SERVICE_TUTOR, s)
    cmp_ = has(COMPARE, s)
    sw = has(SWITCH, s)
    kids = has(rx(r'子供', r'子ども', r'こども', r'息子', r'娘', r'小学', r'中学', r'高校', r'児童', r'生徒', r'キッズ'), s)
    alias = '' if is_comp or brand else alias_in(s)

    # ---- HARD EXCLUDE（絶対にないもの）----
    toks = norm(r['keyword']).split(' ')
    if any(t in ('英語', 'english') for t in toks) and len(toks) <= 3 and \
            all(t in ('英語', 'english') or re.fullmatch(r'[ぁ-ん]{1,3}|[a-z]{1,2}', t) for t in toks):
        return 'EXCLUDE', '語句の英訳・文法の調べもの', '中'
    if has(rx(r'ブログ'), s) and has(rx(r'書き方', r'始め', r'テンプレ', r'コツ', r'ツール', r'デザイン', r'収益', r'稼', r'アフィリ',
                                       r'ネタ', r'文字数', r'作り方', r'開設', r'無料'), s) and not (trait or futo or has(STUDY, s)):
        return 'EXCLUDE', 'ブログ運営（書き手側）', '高'
    if has(SUPPLY, s) and not has(rx(r'募集停止', r'募集終了', r'生徒募集', r'入塾募集', r'家庭教師(の)?派遣(会社|センター)'), s):
        return 'EXCLUDE', '供給側（求人・講師・社員・研修など働く側）', '高'
    if has(rx(r'大学生'), s) and has(rx(r'家庭教師', r'塾', r'チューター', r'講師'), s):
        return 'REVIEW', '大学生×家庭教師（依頼側か講師側か不明）', '低'
    if has(rx(r'資格', r'支援士', r'サポーター(認定)?'), s):
        if has(rx(r'支援', r'発達', r'障害', r'療育', r'自閉', r'アスペ', r'adhd', r'asd', r'学ぶ', r'取得', r'国家', r'講師', r'先生',
                  r'教師', r'保育', r'公務員', r'キャリア', r'大学', r'高卒', r'通信'), s):
            return 'EXCLUDE', '支援者・講師・大人向けの資格取得', '高'
        if not has(rx(r'小学', r'中学', r'高校', r'子供', r'子ども', r'珠算', r'暗算', r'検定', r'英検', r'漢検'), s):
            return 'REVIEW', '資格語（誰の資格か不明）', '低'
    if has(BUSINESS, s):
        nav = has(rx(r'電話番号', r'住所', r'所在地', r'アクセス', r'駐車場', r'地図', r'マップ', r'行き方', r'営業時間'), s)
        if nav and not cmp_:
            return 'EXCLUDE', '既存ブランド/施設へのナビゲーション（連絡先・場所）', '中'
        if not nav:
            if has(rx(r'運営(会社|法人|母体)?', r'本社', r'本部', r'社長', r'代表取締役', r'会社概要'), s) and (is_comp or brand or alias or trait):
                return 'REVIEW', '運営会社確認（比較検討の裏取りの可能性）', '低'
            return 'EXCLUDE', '事業者・経営・投資側', '高'
    if has(MEMBER, s) or ((brand or is_comp or alias or has(rx(r'塾'), s)) and
                          has(rx(r'時間割', r'スケジュール', r'カレンダー', r'休み(の日|はいつ)', r'祝日', r'欠席', r'振替メール'), s)):
        return 'EXCLUDE', '既存利用者の手続き・ログイン・スケジュール', '高'
    if has(ADULT, s) and not kids:
        return 'EXCLUDE', '対象外（成人当事者・大人の生活/仕事/恋愛）', '高'
    if not is_comp:
        if has(TEACHER_SIDE, s):
            return 'EXCLUDE', '教員・支援者側の業務（指導案/所見/書式等）', '中'
        if has(PLAN_DOC, s):
            return 'REVIEW', '個別の指導計画/支援計画（保護者も関わるが教員側寄り）', '低'
        if has(RESEARCH, s):
            return 'EXCLUDE', '研究・論文・語義確認', '中'
        if has(INFANT, s) and not has(rx(r'小学', r'就学', r'入学', r'勉強', r'学習'), s):
            return 'EXCLUDE', '対象外（0〜3歳・乳幼児）', '高'
        if has(EXAM_LOGISTICS, s) and not (trait or futo or tutor or sw):
            return 'EXCLUDE', '試験の事務情報/大学受験・資格試験（特性・支援文脈なし）', '中'
        if has(CELEB, s) and not (tutor or cmp_ or has(STUDY, s) or trait or futo):
            return 'EXCLUDE', '娯楽・有名人・メディア・素材', '中'
        if has(MEDICAL_ONLY, s) and not (tutor or has(rx(r'勉強', r'学習', r'成績', r'集中'), s)):
            return 'REVIEW', '服薬情報（親だが学習支援への距離が遠い）', '低'
        if not has(ANCHOR, s) and not brand:
            if alias:
                if alias in AMBIGUOUS and not has(EDU_MOD, s):
                    if alias in ('トライ', 'try') and not has(rx(r'トライアル', r'トライク', r'トライアスロン', r"let'stry",
                                                                  r'try&try', r'トライ&トライ', r'トライっと', r'ハイジ', r'トライバル'), s):
                        return 'REVIEW', '「トライ」＋地名等（トライの教室か別物か不明）', '低'
                    return 'EXCLUDE', '競合別名の別業種誤爆（教育語なし）', '中'
                if alias in AMBIGUOUS and has(rx(r'株', r'投資', r'ミルク', r'パン', r'ヨガ', r'ピラティス', r'映画', r'歌',
                                                 r'ケツメイシ', r'通販', r'楽天', r'kg', r'mm', r'荘', r'介護', r'車'), s):
                    return 'EXCLUDE', '競合別名の別業種誤爆', '高'
            elif has(rx(r'パン', r'シュレッダー', r'法テラス', r'外来', r'共済', r'入院', r'ヨガ', r'ピラティス', r'ダンス',
                        r'クルーズ', r'証券', r'株', r'投資', r'ローン', r'保険', r'不動産', r'車', r'ホテル', r'旅行'), s):
                return 'EXCLUDE', '領域語なし（別業種・生活一般）', '高'
            elif len(re.sub(COMPARE.pattern + r'|' + SWITCH.pattern + r'|会社|電話|お|faq|悪い|良い|いい|問合せ', '', s)) <= 1:
                return 'EXCLUDE', '対象のない比較語のみ（何の評判か不明）', '中'
            elif has(rx(r'歯医者', r'歯科', r'耳鼻', r'眼科', r'皮膚科', r'婦人科', r'泌尿器', r'整形', r'内科', r'医院',
                        r'クリニック', r'病院', r'ホスピタル', r'医療センター', r'メディカル'), s):
                return 'EXCLUDE', '医療機関の口コミ等（発達・小児文脈なし）', '中'
            elif has(rx(r'ブログ', r'サイト', r'メール'), s) or len(norm(r['keyword']).split(' ')) <= 3 and \
                    re.sub(r'体験|料金|無料|値段|金額|評判|口コミ|おすすめ|ランキング|予約', '', s) and \
                    not has(rx(r'個別', r'講習', r'教室', r'スクール', r'学院', r'ゼミ', r'塾', r'館', r'アカデミー', r'ラボ'), s) and \
                    has(rx(r'^(体験|料金|無料)', r'(体験|料金|無料)$'), s) and \
                    not has(rx(r'[a-z]{3,}', r'[ァ-ヶー]{3,}'), re.sub(r'体験|料金|無料|値段|金額|評判|口コミ', '', s)):
                return 'EXCLUDE', '地名/汎用語×体験・料金のみ（何のサービスか不明）', '中'
            elif cmp_ or has(rx(r'個別', r'講習', r'教室', r'スクール', r'学院', r'ゼミ', r'塾'), s):
                return 'REVIEW', '固有名詞×比較/教育語（教育サービスか要確認）', '低'
            else:
                return 'EXCLUDE', '領域語なし（子ども・学習・特性・支援のいずれにも接続しない）', '中'

    # ---- CORE（本命：別管理でCPCを上げて取りに行くレイヤー）----
    if (trait or futo) and tutor:
        return 'CORE', '特性/不登校×家庭教師・塾・個別', '高'
    if pf == '③X 終了サービス/乗換え':
        return 'CORE', '終了競合の乗換え需要', '高'
    if pf == '③A 直接競合':
        return 'CORE', '直接競合（特性/不登校×1対1学習支援）', '高'
    if pf == '③B カテゴリ競合' and (cmp_ or sw or trait or futo or '資料請求' in s):
        return 'CORE', 'カテゴリ競合×比較/評判/料金/乗換え/特性', '中'
    if pf == '①王道' and (trait or futo):
        return 'CORE', '特性/不登校×比較・おすすめ', '高'
    if has(rx(r'家庭教師', r'個別指導', r'マンツーマン', r'学習支援'), s) and has(rx(r'特性', r'障害', r'障がい', r'苦手な子', r'できない子',
                                                                                     r'ついていけない', r'理解して', r'ゆっくり',
                                                                                     r'自分のペース', r'集中できない', r'勉強嫌い'), s):
        return 'CORE', 'サービス語×つまずき・特性を示す語', '中'

    # ---- REVIEW（機械では決めきれないもの）----
    if has(rx(r'講師', r'先生', r'教師', r'チューター'), s) and not (kids or trait or futo or cmp_ or sw or is_comp or brand or alias) and \
            not has(rx(r'家庭教師', r'プロ教師', r'先生を探', r'専門の先生', r'教えてくれる', r'塾'), s):
        return 'REVIEW', '講師/先生語のみ（求職者・教員側の可能性）', '低'

    # ---- KEEP（低CPC探索）----
    return 'KEEP', '成約ストーリーを否定できない', None


def intent_of(r, verdict):
    s = joined(r['keyword'])
    pf = r['portfolio']
    trait = has(TRAIT, s)
    futo = has(FUTOUKOU, s)
    if verdict == 'EXCLUDE':
        return '対象外'
    if pf.startswith('③') or r['brand'] or alias_in(s):
        if has(SWITCH, s):
            return '競合の不満・乗り換え'
        if has(COMPARE, s):
            return '競合の比較検討（評判・料金）'
        if trait or futo:
            return '競合×特性/不登校対応の確認'
        return '競合指名・周辺'
    if (trait or futo) and has(SERVICE_TUTOR, s):
        return 'サービス探し（特性/不登校×学習支援）'
    if has(COMPARE, s) and has(SERVICE_TUTOR, s):
        return 'サービス比較（家庭教師・塾一般）'
    if has(SWITCH, s) and has(SERVICE_TUTOR, s):
        return '塾・家庭教師が合わない'
    if has(SERVICE_TUTOR, s):
        if has(rx(r'近く', r'駅', r'市', r'区', r'町', r'県', r'校$', r'教室$'), s) or 'エリア' in r['intent_category'] or '地域' in r['intent_category']:
            return 'サービス探し（地域の塾・個別）'
        return 'サービス探し（家庭教師・塾一般）'
    if futo or has(rx(r'別室', r'保健室', r'登校', r'支援級', r'通級', r'特別支援', r'特別学級', r'情緒学級', r'転校', r'転籍',
                      r'学校生活', r'普通級', r'通常級', r'いじめ', r'友達', r'担任'), s):
        return '不登校・学校生活'
    if has(rx(r'受験', r'入試', r'高校受験', r'内申', r'偏差値', r'志望校', r'進学', r'進路', r'通信制', r'サポート校', r'推薦', r'将来',
                 r'編入', r'転入', r'転学', r'併願', r'高専', r'学費'), s):
        return '受験・進路'
    if has(rx(r'勉強しない', r'勉強(を)?しない', r'やる気', r'宿題', r'集中', r'ゲーム', r'スマホ', r'反抗', r'喧嘩', r'けんか', r'怒',
                 r'イライラ', r'疲れ', r'しんどい', r'つらい', r'辛い', r'限界', r'教え方', r'教えられない', r'家庭学習', r'親'), s):
        return '家庭学習・親の悩み'
    if has(rx(r'苦手', r'できない', r'わからない', r'ついていけない', r'遅れ', r'つまず', r'つまづ', r'覚えられない', r'書けない',
                 r'読めない', r'落ちこぼれ', r'克服', r'勉強法', r'覚え方', r'やり方', r'コツ'), s):
        return '学習のつまずき・勉強法'
    if trait or has(rx(r'知能', r'iq', r'wisc', r'検査', r'診断', r'特徴', r'チェック', r'とは', r'症状', r'原因'), s):
        return '特性理解・診断'
    if has(rx(r'療育', r'放課後', r'デイ', r'児童発達', r'フリースクール', r'居場所', r'相談', r'カウンセ'), s):
        return '療育・福祉・居場所'
    if has(rx(r'教材', r'ドリル', r'問題集', r'アプリ', r'通信', r'タブレット', r'参考書', r'プリント'), s):
        return '教材・通信・アプリ'
    if has(rx(r'習い事', r'教室', r'スクール', r'プログラミング', r'そろばん', r'英会話'), s):
        return '習い事・教室'
    return '学習・学校の一般情報'


def searcher_of(r, verdict, reason):
    s = joined(r['keyword'])
    if verdict == 'EXCLUDE':
        if reason.startswith('供給側'):
            return '講師・求職者'
        if reason.startswith('教員'):
            return '教員・支援者'
        if reason.startswith('事業者'):
            return '事業者・投資家'
        if reason.startswith('研究'):
            return '研究・学生'
        if reason.startswith('対象外（成人'):
            return '成人当事者・家族'
        if reason.startswith('対象外（0'):
            return '乳幼児の保護者'
        if reason.startswith('既存利用者') or reason.startswith('既存ブランド'):
            return '既存利用者'
        return '不明'
    if reason.startswith('講師/先生語') or reason.startswith('大学生'):
        return '不明（保護者 or 講師側）'
    if r['portfolio'].startswith('③') or r['brand'] or has(PARENT_HINT, s):
        return '保護者'
    if has(CHILD_HINT, s) and not has(TRAIT, s):
        return '子ども本人（推定）'
    return '保護者（推定）'


def lp_of(r, verdict, intent):
    if verdict == 'EXCLUDE':
        return ''
    if intent.startswith('サービス探し（特性') or intent.startswith('サービス比較'):
        return 'A'
    if intent.startswith('競合') or intent in ('塾・家庭教師が合わない', 'サービス探し（地域の塾・個別）', 'サービス探し（家庭教師・塾一般）'):
        return 'B'
    if intent in ('不登校・学校生活', '受験・進路'):
        return 'D'
    return 'C'


LP_NAME = {
    'A': 'A サービス直結（発達特性×オンライン家庭教師／比較・料金）',
    'B': 'B 比較・乗り換え（普通の塾・家庭教師が合わない子に）',
    'C': 'C 家庭学習・特性の悩み（親だけで抱え込まなくていい）',
    'D': 'D 不登校・学校・進路（学びの遅れと居場所）',
}


def main():
    rows = load()
    cand = [r for r in rows if r['portfolio'] != '除外']
    print('出稿候補', len(cand), file=sys.stderr)

    for r in cand:
        v, why, conf = classify(r)
        r['判定'] = v
        r['理由'] = why
        r['検索意図'] = intent_of(r, v)
        r['検索者推定'] = searcher_of(r, v, why)
        r['LP'] = lp_of(r, v, r['検索意図'])
        if conf is None:  # KEEPの確信度: 足場の強さで決める
            s = joined(r['keyword'])
            if has(TRAIT, s) or has(FUTOUKOU, s) or r['portfolio'].startswith('③') or has(SERVICE_TUTOR, s):
                conf = '高'
            elif has(PARENT_HINT, s) or has(SWITCH, s) or r['検索意図'] in ('家庭学習・親の悩み', '学習のつまずき・勉強法'):
                conf = '中'
            else:
                conf = '低'
        r['確信度'] = conf
        r['dedup_key'] = dedup_key(r['keyword'])

    # ---- 意味的重複クラスター（EXCLUDE以外で作る）----
    groups = defaultdict(list)
    for r in cand:
        if r['判定'] != 'EXCLUDE':
            groups[(r['dedup_key'], r['brand'])].append(r)

    def vol(r):
        try:
            return int(float(r['average_monthly_searches'] or 0))
        except ValueError:
            return 0

    def src_rank(r):
        ds = r['discovery_source']
        return 0 if 'KWP' in ds else 1

    rank = {'CORE': 0, 'KEEP': 1, 'REVIEW': 2}
    cid = 0
    for key, members in sorted(groups.items(), key=lambda kv: kv[0]):
        cid += 1
        members.sort(key=lambda r: (rank[r['判定']], -vol(r), src_rank(r), len(norm(r['keyword'])), r['sheet_row']))
        rep = members[0]
        # クラスターの判定は代表に寄せる（CORE>KEEP>REVIEW）
        for m in members:
            m['cluster_id'] = 'C%05d' % cid
            m['cluster_size'] = len(members)
            m['代表KW'] = rep['keyword']
            m['投入'] = '代表' if m is rep else '重複（代表に統合）'
    ex_id = 0
    for r in cand:
        if r['判定'] == 'EXCLUDE':
            ex_id += 1
            r['cluster_id'] = ''
            r['cluster_size'] = ''
            r['代表KW'] = ''
            r['投入'] = '除外'

    write_outputs(cand)


COLS = ['sheet_row', 'keyword', '判定', '投入', 'cluster_id', 'cluster_size', '代表KW', '検索意図', '検索者推定', 'LP',
        '理由', '確信度', 'portfolio', 'brand', 'average_monthly_searches', 'low_top_of_page_bid', 'high_top_of_page_bid',
        'competition', 'intent_category', 'discovery_source']


def wcsv(path, rows, cols=COLS):
    with open(os.path.join(HERE, path), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in rows:
            w.writerow([r.get(c, '') for c in cols])


def write_outputs(cand):
    order = {'CORE': 0, 'KEEP': 1, 'REVIEW': 2, 'EXCLUDE': 3}
    cand.sort(key=lambda r: (order[r['判定']], r.get('cluster_id') or 'Z', r['sheet_row']))
    wcsv('01_KW仕分け_全件.csv', cand)
    wcsv('02_投入KW_10円探索.csv', [r for r in cand if r['判定'] == 'KEEP' and r['投入'] == '代表'])
    wcsv('03_投入KW_CORE.csv', [r for r in cand if r['判定'] == 'CORE' and r['投入'] == '代表'])
    ex = sorted([r for r in cand if r['判定'] == 'EXCLUDE'], key=lambda r: (r['理由'], r['sheet_row']))
    wcsv('04_要確認_EXCLUDE.csv', ex)
    rv = sorted([r for r in cand if r['判定'] == 'REVIEW'], key=lambda r: (r['理由'], r['sheet_row']))
    wcsv('05_要確認_REVIEW.csv', rv)
    summary(cand)


def summary(cand):
    c = Counter(r['判定'] for r in cand)
    rep = Counter(r['判定'] for r in cand if r['投入'] == '代表')
    lines = ['# ソウガク 出稿候補KW 機械仕分け（2026-10-05）', '',
             '判定基準：「この検索をしている人にソウガクを提示して、無料体験を申し込む合理的なストーリーを1本でも作れるか？」',
             '検索vol・KWP単価・情報収集っぽさでは落とさない。落とすのは「明確な不適合」と「意味的重複」だけ。', '',
             '## 判定別', '', '| 判定 | KW数 | 投入数（重複統合後の代表） | 重複で統合 |', '|---|---:|---:|---:|']
    for k in ['CORE', 'KEEP', 'REVIEW', 'EXCLUDE']:
        n = c.get(k, 0)
        p = rep.get(k, 0) if k != 'EXCLUDE' else 0
        lines.append('| %s | %s | %s | %s |' % (k, f'{n:,}', f'{p:,}' if k != 'EXCLUDE' else '-', f'{n - p:,}' if k != 'EXCLUDE' else '-'))
    lines.append('| 計 | %s | %s | |' % (f'{len(cand):,}', f'{sum(rep.values()):,}'))
    lines += ['', '## EXCLUDE 理由別', '', '| 理由 | KW数 |', '|---|---:|']
    for k, n in Counter(r['理由'] for r in cand if r['判定'] == 'EXCLUDE').most_common():
        lines.append(f'| {k} | {n:,} |')
    lines += ['', '## REVIEW 理由別', '', '| 理由 | KW数 |', '|---|---:|']
    for k, n in Counter(r['理由'] for r in cand if r['判定'] == 'REVIEW').most_common():
        lines.append(f'| {k} | {n:,} |')
    lines += ['', '## CORE 理由別', '', '| 理由 | KW数 | 代表 |', '|---|---:|---:|']
    cr = Counter(r['理由'] for r in cand if r['判定'] == 'CORE' and r['投入'] == '代表')
    for k, n in Counter(r['理由'] for r in cand if r['判定'] == 'CORE').most_common():
        lines.append(f'| {k} | {n:,} | {cr[k]:,} |')
    lines += ['', '## 投入KW（代表）× 検索意図 × LP', '', '| 検索意図 | LP | CORE | KEEP | REVIEW |', '|---|---|---:|---:|---:|']
    t = Counter((r['検索意図'], r['LP'], r['判定']) for r in cand if r['投入'] == '代表')
    keys = sorted({(a, b) for a, b, _ in t}, key=lambda k: -sum(t[(k[0], k[1], v)] for v in ('CORE', 'KEEP', 'REVIEW')))
    for a, b in keys:
        lines.append(f'| {a} | {b} | {t[(a, b, "CORE")]:,} | {t[(a, b, "KEEP")]:,} | {t[(a, b, "REVIEW")]:,} |')
    lines += ['', '## 検索者推定（投入代表）', '', '| 検索者 | KW数 |', '|---|---:|']
    for k, n in Counter(r['検索者推定'] for r in cand if r['投入'] == '代表').most_common():
        lines.append(f'| {k} | {n:,} |')
    lines += ['', '## LP定義', '']
    for k, v in LP_NAME.items():
        lines.append(f'- {v}')
    with open(os.path.join(HERE, '06_集計.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()

"""TOP3比較・ランキング版（/ranking/）の組み立て

部品は「比較・ランキング型LP パーツ集」（https://hakobu-family.com/lp-parts-yakuzaishi/、yk-*）の
HTML・ルールどおり。parts.css は ranking/yk-parts.css に写して使う（原本ハッシュは ranking_台本.md）。
会社の事実はすべて下の SERVICES に集め、出典URLと確認日を持たせる。順位・総合評価は AXES の採点から計算する
（基準は ranking/method.html に公開）。
  python3 build_ranking.py
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "ranking")
CHECKED = "2026年10月17日"
CHECKED_ISO = "2026-10-17"
UPDATED = "2026年10月"
SITE = "わが子の学び方ガイド"
ASP = "https://t.felmat.net/fmcl?ak=C12158L.1.I1680104.D1416296&amp;pb="
ASP_IMG = "https://t.felmat.net/fmimg/C12158L.I1680104.D1416296"
IMG = "../images/"

# 採点の7項目（ranking/method.html に基準を公開）
AXES = [
    ("support", "特性への対応", "発達特性への対応"),
    ("teacher", "先生", "先生の体制"),
    ("trial", "入会前の確認", "入会前に確かめられること"),
    ("time", "授業時間", "短い時間から始められるか"),
    ("parent", "保護者サポート", "保護者サポート"),
    ("price", "料金", "料金（小学生の月額の目安）"),
    ("contract", "費用・契約", "費用と契約の分かりやすさ"),
]

S = {}
S["sogaku"] = dict(
    name="ソウガク", short="ソウガク", full="発達障害・グレーゾーン専門オンライン家庭教師ソウガク",
    logo=("logos/sogaku-logo.svg", 500, 186), url=ASP, sponsored=True,
    official="https://sogaku.jp/online/",
    scores=dict(support=5, teacher=5, trial=5, time=5, parent=5, price=4, contract=5),
    price_month=13200, min_minutes=25,
    best3=("発達障害・グレーゾーン専門", "担当予定の先生と2回体験できます", "先生は専門機関の研修を受けた社会人で、小学生は25分から受けられます。"),
    target="小学生〜高校生", btn_catch="診断なし・グレーゾーンでも相談OK", btn="無料体験を公式で見る",
    catch="発達特性を学んだ社会人講師。授業は小学生25分から！<br>担当予定の先生と無料体験2回",
    cmp_text="サービス全体が発達障害・グレーゾーン専門。先生は全員、専門機関の研修を受けた社会人。担当予定の先生と2回の無料体験で相性を確かめられる。",
    chips=[("is-pink", "25分から"), ("", "毎回の報告"), ("", "体験2回"), ("", "違約金0円")],
    features=[
        ('先生は全員<span class="yk-mark">専門機関の研修を受けた社会人講師</span>', "https://sogaku.jp/online/tutor.html"),
        ("専門家が開発したアセスメントシートで、一人ずつ指導計画を作る", "https://sogaku.jp/online/reason.html"),
        ('授業は<span class="yk-red">小学生25分</span>から（中高生は35分から）', "https://sogaku.jp/online/fee.html"),
        ("無料体験は2回。入会後に担当する予定の先生が担当", "https://sogaku.jp/online/faq.html"),
        ("授業のたびにアプリで指導報告。先生・本部にチャットで相談", "https://sogaku.jp/online/course.html"),
        ("違約金・途中解約料0円。契約期間の縛りなし", "https://sogaku.jp/online/reason.html"),
        ("担任制で毎回同じ先生。手元をスマホで映せば、書けているかも先生が確認", "https://sogaku.jp/online/trial-flow.html"),
    ],
    editor=('ソウガクは、サービス全体が発達障害・グレーゾーン専門です。先生は全員が社会人で、発達支援の専門機関「発達凸凹アソシエーション」の研修を受けています。臨床心理士や作業療法士、放課後等デイサービスで働いた経験のある先生も在籍しています。'
            '<span class="yk-mark">入会後に担当する予定の先生の無料体験を、2回まで受けてから決められる</span>と公式に明記しているのは、比較した6社の中でソウガクだけでした※1。'
            '授業は小学生なら<span class="yk-red">25分</span>から選べて、違約金や途中解約料もかかりません。「長い授業は続かないかも」「先生との相性が心配」という家庭が、最初に試しやすいサービスです。',
            "※1 各社公式サイトの無料体験の説明による。TOSは1回・訪問の説明"),
    info=[("料金の目安", "月13,200円〜<small>小学生25分×月4回・税込。別途入会金22,000円（キャンペーンで無料の場合あり）</small>"),
          ("対応学年", "小学生〜高校生<small>全国・オンライン（Zoom）</small>"),
          ("1回の授業", "小学生25分・50分・75分<br>中高生35分・60分・75分"),
          ("先生", "全員が専門機関の研修を受けた社会人講師"),
          ("保護者サポート", "毎回の指導報告・先生・本部とチャット・定期的な保護者面談・保護者向け勉強会"),
          ("無料体験", "2回。担当予定の先生が担当（1回目は保護者面談にもできる）")],
    plans=[("小学生", "25分×月4回", "13,200円", "50分×月4回は22,000円"),
           ("中学生", "35分×月4回", "18,480円", "60分×月4回は26,400円"),
           ("高校生", "35分×月4回", "21,560円", "60分×月4回は29,920円")],
    plan_src="https://sogaku.jp/online/fee.html", plan_note="すべて税込。入会金22,000円は別途。同じコースなら卒業まで料金は上がりません",
    voices=[("中学2年生・特別支援学級の保護者",
             "勉強に苦手意識があり、初回の体験では画面の前に座っているのも難しかった。先生が急がずに時間をかけて関係をつくり、今は授業の時間を楽しみにしている。"),
            ("小学4年生・ADHDの診断ありの保護者",
             "学校へ行ける日が減り、家で勉強を見ると親子で言い合いになっていた。週1回オンラインで学ぶ習慣ができ、「ずっと自分が見なければ」という負担が軽くなった。"),
            ("中学2年生の保護者（岡山県）",
             "子どものタイプに合わせた学び方を相談できる先生に初めて出会えた。他社と違って、体験を何回か受けられたのも助かった。")],
    voice_src="https://sogaku.jp/online/voice.html", voice_pick=1,
    operator=None,
)
S["rebalance"] = dict(
    name="オンライン個別指導塾リバランス", short="リバランス", full="オンライン個別指導塾リバランス（発達障害・グレーゾーン・ギフテッド専門）",
    logo=("logos/rebalance-logo.png", 500, 160), url="https://reba1ance.com/", sponsored=False,
    official="https://reba1ance.com/",
    scores=dict(support=5, teacher=5, trial=4, time=3, parent=5, price=2, contract=4),
    price_month=22000, min_minutes=60,
    best3=("発達障害・ギフテッド専門のオンライン塾", "約90分の無料体験で指導計画を提案", "学生の先生も、プロと同じ研修を受けたセミプロです。"),
    target="小学1年生〜中学3年生", btn_catch="体験だけでも個別指導計画書がもらえる", btn="無料体験学習を公式で見る",
    catch="発達障害・ギフテッド専門のオンライン個別指導<br>約90分の無料体験で、個別指導計画書を提案",
    cmp_text="LD・ADHD・ASD・グレーゾーン・2E専門。授業後は毎回フィードバック。授業は60分から。",
    chips=[("is-pink", "指導計画書"), ("", "毎回の報告"), ("is-gray", "60分から")],
    features=[
        ('<span class="yk-mark">LD・ADHD・ASD・グレーゾーン・ギフテッド（2E）</span>専門。完全1対1のライブ授業', "https://reba1ance.com/faq/"),
        ('約90分の無料体験のあと、<span class="yk-red">個別指導計画書（IEP）</span>をメールで受け取れる', "https://reba1ance.com/system/"),
        ("学生の先生も、プロ講師と同じ学科研修・技能研修を終えた「セミプロ講師」", "https://reba1ance.com/faq/"),
        ("授業後に毎回フィードバック。授業以外も教務に相談できる", "https://reba1ance.com/system/"),
    ],
    editor=('リバランスは、LD・ADHD・ASD・グレーゾーン・ギフテッド（2E）専門のオンライン個別指導塾です。学習内容のレベルは下げずに、伝え方や答え方を工夫する「アコモデーション」を方針にしています。'
            '約90分の無料体験では、聞き取りと模擬授業のあとに<span class="yk-red">個別指導計画書（IEP）</span>が提案され、入会しなくても受け取れます。'
            '授業は60分からで料金も高めですが、<span class="yk-mark">中学受験・高校受験まで特性に合わせて相談したい家庭</span>に向いています。', ""),
    info=[("料金の目安", "60分×月4回 22,000円〜<small>税込（セミプロ講師）。プロ講師は28,600円〜。別途入会金19,800円・年間管理費26,400円</small>"),
          ("対応学年", "小学1年生〜中学3年生<small>全国・海外からオンライン</small>"),
          ("1回の授業", "60分〜<small>回数・時間はプランで相談</small>"),
          ("先生", "プロ講師（社会人・有資格の学生）と、同じ研修を終えたセミプロ講師（学生）"),
          ("保護者サポート", "毎回のフィードバック・教務への相談・無料の定期面談"),
          ("無料体験", "約90分のオンライン体験（聞き取り・模擬授業・指導方針の提案）")],
    plans=[("小学生〜中学生", "セミプロ講師・60分×月4回", "22,000円〜", "入会金19,800円・年間管理費26,400円は別途"),
           ("小学生〜中学生", "プロ講師・60分×月4回", "28,600円〜", "入会金19,800円・年間管理費26,400円は別途")],
    plan_src="https://reba1ance.com/budget/", plan_note="すべて税込。入会金19,800円・年間管理費26,400円は別途",
    voices=[("会員の保護者（公式サイト掲載のGoogleの口コミ）",
             "勉強が大嫌いだった子が、数か月で難しい問題にも挑戦できるようになった。授業に本人の興味のあることを取り入れてくれて、親にも毎回フィードバックをくれる。")],
    voice_src="https://reba1ance.com/",
    operator="リバランス株式会社",
)
S["try"] = dict(
    name="トライのオンライン個別指導塾", short="トライ", full="トライのオンライン個別指導塾（発達特性サポートコース）",
    logo=("logos/try-logo.svg", 220, 28), url="https://www.try-online.jp/kobetsu/tokusei/", sponsored=False,
    official="https://www.try-online.jp/kobetsu/tokusei/",
    scores=dict(support=4, teacher=4, trial=4, time=3, parent=5, price=4, contract=4),
    price_month=14960, min_minutes=60,
    best3=("発達特性サポートコース", "WISC検査の結果を学習に活かす", "教師とは別に教育プランナーが専任でつきます。"),
    target="小学生〜高校生", btn_catch="学習面談は入会しなくても受けられる", btn="無料の学習面談を公式で見る",
    catch="発達特性サポートコースあり<br>WISC検査の結果をもとに学習をサポート",
    cmp_text="正社員の教育プランナーが専任でつき、WISC検査の結果をもとに学習計画を立てる。",
    chips=[("is-pink", "WISC活用"), ("", "教育プランナー"), ("", "カメラオフ可")],
    features=[
        ('教師とは別に、正社員の<span class="yk-mark">教育プランナー</span>が専任でつく', "https://www.try-online.jp/kobetsu/tokusei/"),
        ('<span class="yk-red">WISC検査の結果</span>をもとに、得意を伸ばし苦手をカバー', "https://www.try-online.jp/kobetsu/tokusei/"),
        ("保護者の同席・カメラオフでの受講もできる", "https://www.try-online.jp/kobetsu/tokusei/"),
        ("学習管理アプリで、毎回の授業の進捗が見える", "https://www.try-online.jp/kobetsu/price/"),
    ],
    editor=('トライのオンライン個別指導塾には発達特性サポートコースがあり、<span class="yk-red">WISC検査の結果</span>をもとに学習を組み立てます。'
            '教師とは別に正社員の教育プランナーが専任でつき、定期的な面談や電話・LINEで相談できます。'
            '<span class="yk-mark">検査結果をどう勉強に活かせばいいか迷っている家庭</span>に向いています。', ""),
    info=[("料金の目安", "小学生 60分×月4回 14,960円〜<small>税込。別途入会金11,000円</small>"),
          ("対応学年", "小学生〜高校生<small>高卒生も相談可</small>"),
          ("1回の授業", "1コマ60分（料金例）<small>時間・回数・教科は変更できる</small>"),
          ("先生", "登録教師33万人（2024年3月時点・公式）から選ぶ。専任制で原則同じ先生"),
          ("保護者サポート", "教育プランナーの定期面談・電話・LINE、学習管理アプリ"),
          ("無料体験", "無料の学習面談と、体験授業（英語か数学。約30分と約60分の両方の記載あり）")],
    plans=[("小学生", "1コマ60分×月4回", "14,960円〜", "入会金11,000円は別途"),
           ("中学生", "1コマ60分×月4回", "17,600円〜", "入会金11,000円は別途"),
           ("高校生", "1コマ60分×月4回", "21,120円〜", "入会金11,000円は別途")],
    plan_src="https://www.try-online.jp/kobetsu/price/", plan_note="すべて税込。入会金11,000円は別途",
    voices=[],
    voice_src=None,
    operator="株式会社トライグループ",
)
S["coaching1"] = dict(
    name="個別指導のコーチング1", short="コーチング1", full="個別指導のコーチング1（発達障害専門の学習進学塾・オンライン指導）",
    logo=("logos/coaching1-juku-logo.png", 294, 44), url="https://www.juku-coaching01.com/", sponsored=False,
    official="https://www.juku-coaching01.com/",
    scores=dict(support=5, teacher=4, trial=4, time=3, parent=5, price=2, contract=4),
    price_month=25300, min_minutes=60,
    best3=("発達障害専門の学習進学塾", "中学・高校受験に対応", "提携する臨床心理士の発達検査を受けられます。"),
    target="年長〜高校3年生", btn_catch="無料の体験学習・学習カウンセリングあり", btn="無料体験を公式で見る",
    catch="発達障害・グレーゾーン専門の学習進学塾<br>オンライン指導は全国対応、受験にも対応",
    cmp_text="発達障害・グレーゾーン専門。臨床心理士の発達検査と受験対策が特徴。オンラインは60分から。",
    chips=[("is-pink", "受験対策"), ("", "発達検査"), ("", "毎回の報告書")],
    features=[
        ('提携する<span class="yk-mark">臨床心理士の発達検査</span>を受けられる', "https://www.juku-coaching01.com/guide/developmentaltest/"),
        ('発達特性のある子の<span class="yk-red">中学受験・高校受験</span>に対応', "https://www.juku-coaching01.com/"),
        ("発達指導の講師は独自の研修を受けて担当。毎回の指導報告書", "https://www.juku-coaching01.com/starting/"),
        ("授業以外のことも教務部に相談できる", "https://www.juku-coaching01.com/starting/"),
    ],
    editor=('コーチング1は、発達障害・グレーゾーンの子のための学習進学塾です。教室のほかにオンライン指導があり、全国から受けられます。'
            '提携する臨床心理士の発達検査を受けられること、<span class="yk-red">発達特性のある子の中学受験・高校受験</span>に対応していることが特徴です。'
            'オンラインは60分×月4回で25,300円（税込）からで、別に入会金と年会費がかかりますが、<span class="yk-mark">受験まで見据えて専門の塾に任せたい家庭</span>には候補になります。', ""),
    info=[("料金の目安", "オンライン 60分×月4回 25,300円<small>税込。別途入会金18,700円・年会費26,400円</small>"),
          ("対応学年", "年長〜高校3年生<small>オンラインは全国・海外から</small>"),
          ("1回の授業", "60分・90分・120分<small>月4回か月8回</small>"),
          ("先生", "独自の研修を受けた講師（チーム制）"),
          ("保護者サポート", "毎回の指導報告書・教務部に相談"),
          ("無料体験", "体験授業と学習カウンセリング（担当教務と約120分。オンラインも可）")],
    plans=[("全学年", "オンライン・60分×月4回", "25,300円", "入会金18,700円・年会費26,400円は別途"),
           ("全学年", "オンライン・90分×月4回", "37,400円", "入会金18,700円・年会費26,400円は別途"),
           ("全学年", "オンライン・60分×月8回", "48,400円", "入会金18,700円・年会費26,400円は別途")],
    plan_src="https://www.juku-coaching01.com/price/", plan_note="すべて税込。入会金18,700円・年会費26,400円は別途",
    voices=[("ADHDの子の保護者（公式サイト掲載）",
             "担当の教務スタッフが、子どもにできることとできないことを見極めて学習プランを立ててくれた。子どもに無理をさせずに勉強させられるようになり、親の負担も軽くなった。")],
    voice_src="https://www.juku-coaching01.com/voice/",
    operator="株式会社AXT",
)
S["kizuki"] = dict(
    name="キズキ共育塾", short="キズキ", full="キズキ共育塾（オンライン校・完全1対1の個別指導）",
    logo=("logos/kizuki-logo.svg", 266, 100), url="https://kizuki.or.jp/facility/online/", sponsored=False,
    official="https://kizuki.or.jp/facility/online/",
    scores=dict(support=4, teacher=3, trial=3, time=4, parent=4, price=2, contract=4),
    price_month=24200, min_minutes=50,
    best3=("不登校・発達障害の子の学び直し", "50分の完全1対1", "保護者向けのおやサポメンターがあります。"),
    target="小学生〜社会人", btn_catch="保護者だけの相談・見学もできる", btn="無料の入会相談を公式で見る",
    catch="不登校・発達障害・グレーゾーンの学び直しを支える<br>完全1対1の個別指導（オンライン校あり）",
    cmp_text="不登校・発達障害の子の学び直しと受験。授業は50分から。常設の無料体験はない。",
    chips=[("is-pink", "50分から"), ("", "メンター"), ("", "出席扱いの相談")],
    features=[
        ('<span class="yk-mark">不登校・発達障害・グレーゾーン</span>の子の学び直しと受験を、完全1対1で', "https://kizuki.or.jp/"),
        ('授業とは別に、学習計画や特性を一緒に考える<span class="yk-red">メンターサポート</span>', "https://kizuki.or.jp/courses/"),
        ("保護者向けの「おやサポメンター」（月1回30分）で、教務から学習状況を聞ける", "https://kizuki.or.jp/courses/"),
        ("顔を見せるのが苦手なら、音声とチャットだけで授業を受けられる", "https://kizuki.or.jp/facility/online/"),
    ],
    editor=('キズキ共育塾は、不登校・発達障害・グレーゾーンの子や、中退・社会人の学び直しを支える完全1対1の個別指導塾です。'
            'オンライン校なら全国から受けられ、顔を見せるのが苦手な子は音声とチャットだけで授業を受けることもできます。授業とは別に、学習計画や特性を一緒に考える<span class="yk-red">メンターサポート</span>があります。'
            '常設の無料体験授業はありませんが、保護者だけの相談や見学ができるので、<span class="yk-mark">学校に行きづらい状態からの学び直しを考えている家庭</span>に向いています。', ""),
    info=[("料金の目安", "50分×月4回 24,200円〜<small>税込。学年ごとの金額は記載なし（中学3年生の例は30,800円〜）。別途入会金16,500円ほか</small>"),
          ("対応学年", "小学生〜社会人<small>オンライン校は全国・海外から</small>"),
          ("1回の授業", "50分か80分<small>1科目につき月4コマ</small>"),
          ("先生", "面談の内容をもとに講師を選定。プロ講師のコースあり"),
          ("保護者サポート", "おやサポメンター（月1回30分）・保護者だけの相談"),
          ("無料体験", "常設の体験授業はなし（期間限定の場合あり）。無料の入会相談・見学")],
    plans=[("中学3年生", "50分×月4回（メンターなし）", "30,800円〜", "公式の料金例"),
           ("中学3年生", "80分×月4回（メンターなし）", "36,300円〜", "公式の料金例"),
           ("中学3年生", "50分×月4回（メンターあり）", "39,600円〜", "公式の料金例")],
    plan_tag="料金例", plan_src="https://kizuki.or.jp/courses/",
    plan_note="すべて税込。入会金16,500円・事務手数料5,500円・選抜費11,000円〜は別途。小学生の料金は要確認",
    voices=[("ASDのある子の保護者（公式サイト掲載）",
             "入塾前の見学や面談で、子どもの特性を理解してもらえると思えた。宿題の量も講師と子どもが相談して決めてくれるので、自分から取り組めている。")],
    voice_src="https://kizuki.or.jp/voice/",
    operator="株式会社キズキ",
)
S["tos"] = dict(
    name="TOS家庭教師センター", short="TOS", full="TOS家庭教師センター（オンラインコース）",
    logo=("logos/tos-logo.png", 600, 80), url="https://tos-kc1.com/", sponsored=False,
    official="https://tos-kc1.com/",
    scores=dict(support=4, teacher=4, trial=5, time=3, parent=4, price=3, contract=4),
    price_month=19400, min_minutes=60,
    best3=("不登校・発達障害対策の家庭教師", "実際に担当する先生の無料体験", "専門スタッフの発達検査を自宅で受けられます。"),
    target="幼児〜社会人", btn_catch="体験の前に入会金はかからない", btn="無料体験を公式で見る",
    catch="不登校・発達障害・成績不振対策の家庭教師<br>無料体験は実際に担当する先生が担当",
    cmp_text="実際に担当する先生の無料体験。WISCなどの発達検査を自宅で受けられる（有料）。オンラインは60分から。",
    chips=[("is-pink", "担当の先生と体験"), ("", "発達検査"), ("is-gray", "60分から")],
    features=[
        ('無料体験は<span class="yk-mark">実際に担当する家庭教師</span>が担当（面談を含めて40分〜1時間）', "https://tos-kc1.com/trust/trial/"),
        ('専門スタッフによる<span class="yk-red">WISC・田中ビネーなどの発達検査</span>を自宅で受けられる（有料）', "https://tos-kc1.com/trust/guide/trip-service/"),
        ("臨床心理士などのカウンセラーによる心理カウンセリング（有料・オンライン可）", "https://tos-kc1.com/pdd/counseling/"),
        ("解約金・違約金なし。先生の交代は何回でも無料", "https://tos-kc1.com/trust/"),
    ],
    editor=('TOS家庭教師センターは、不登校・発達障害・成績不振対策を掲げる家庭教師センターで、オンラインコースもあります。'
            '無料体験は<span class="yk-red">実際に担当する家庭教師</span>が行い、気に入ってから入会を決められます。専門スタッフによる発達検査や、臨床心理士などのカウンセリング（どちらも有料）も受けられます。'
            'ただし体験の説明は訪問を前提にした書き方なので、<span class="yk-mark">オンラインでも同じ形で体験できるかは申し込み時に確認</span>してください。', ""),
    info=[("料金の目安", "オンライン 60分×月4回 19,400円<small>税込（幼児〜中学3年生）。別途入会金33,000円</small>"),
          ("対応学年", "幼児〜社会人<small>オンラインの対象地域は公式に記載なし</small>"),
          ("1回の授業", "オンラインは60分か90分<small>月4回か月8回</small>"),
          ("先生", "大学生・社会人・プロの登録教師から選定。発達障害児指導の勉強会を開催"),
          ("保護者サポート", "センターで随時学習相談。先生は月1回センターへ報告"),
          ("無料体験", "実際に担当する先生による体験（面談を含めて40分〜1時間）")],
    plans=[("幼児〜中学3年生", "オンライン・60分×月4回", "19,400円", "入会金33,000円は別途"),
           ("高校1年生", "オンライン・60分×月4回", "20,400円", "入会金33,000円は別途"),
           ("高校3年生", "オンライン・60分×月4回", "22,400円", "入会金33,000円は別途")],
    plan_src="https://tos-kc1.com/course/", plan_note="すべて税込。入会金33,000円は別途",
    voices=[],
    voice_src=None,
    operator="TOS CO., LTD.",
)

# 採点の根拠（method.html の根拠表。各社公式サイトの記載、2026-10-14確認）
WHY = {
    "sogaku": dict(support="発達障害・グレーゾーン専門。発達凸凹アソシエーションが講師研修・アセスメントシート・教材アドバイスに関わる", teacher="先生は全員社会人で、専門機関の教師研修とマニュアル研修を受けている（臨床心理士・作業療法士などの資格者も在籍）", trial="無料体験2回。入会後に担当する予定の先生が体験を担当と明記", time="小学生25分・中高生35分のコース", parent="毎回の指導報告＋先生・本部とチャット、定期的な保護者面談、保護者向け勉強会", price="小学生25分×月4回 13,200円（税込）", contract="入会金22,000円（税込）、年会費・保証金・更新費・違約金・途中解約料0円、契約期間の縛りなし、月単位の休会・退会、退会は前月10日までと本体ページに明記"),
    "rebalance": dict(support="LD・ADHD・ASD・グレーゾーン・ギフテッド（2E）専門。臨床心理士との連携、日本LD学会の機関会員", teacher="プロ講師（社会人・有資格の学生）と、プロと同じ学科研修・技能研修を終えたセミプロ講師（学生）が指導と記載", trial="約90分の無料オンライン体験（聞き取り・子どもとの模擬授業・指導方針の提案）。担当予定の先生が行うかは記載なし", time="1回60分から", parent="授業後に毎回フィードバック＋教務への相談、無料の定期面談", price="セミプロ講師 60分×月4回 22,000円〜（税込）", contract="入会金19,800円・年間管理費26,400円（税込）、指定教材なし、中途解約の条件は特商法表記に明記。休会の決まりは記載なし"),
    "try": dict(support="発達特性サポートコース。教育プランナーが専任、WISC検査の結果を活用", teacher="個性別支援の認定教師から、ヒアリングをもとに選定", time="料金例は1コマ60分", price="小学生 60分×月4回 14,960円", parent="アプリで毎回の進捗＋教育プランナーの定期面談・電話・LINE", trial="無料体験授業（英語か数学。公式ページにより約30分・約60分の記載）＋無料の学習面談", contract="入会金11,000円（税込）、教材費・年会費なし、前月までの申し出で解約金なしと記載。最低期間・休会は記載なし"),
    "coaching1": dict(support="発達障害・グレーゾーン専門。提携する臨床心理士の発達検査", teacher="発達指導・SSTの講師に独自の研修システム", trial="約120分の無料体験学習・学習カウンセリング（担当教務。オンラインも可）", time="オンラインは1回60分から", parent="毎回の指導報告書＋教務部に相談", price="オンライン 60分×月4回 25,300円（税込）", contract="入会金18,700円・年会費26,400円（税込）、教材費なし、中途解約の条件は特商法表記に明記（契約は1年の自動更新）。休会の決まりは記載なし"),
    "kizuki": dict(support="不登校・発達障害・グレーゾーンなどの学び直しを掲げる。メンターがアセスメントで特性を一緒に確かめる", teacher="面談をもとに講師を選定。「特性×学び」に特化した専門講師のコースあり（講師研修の記載は限られる）", trial="常設の無料体験授業なし（期間限定の場合あり）。無料の入会相談・見学（保護者だけも可）", time="1回50分から", parent="おやサポメンター（月1回30分）で教務から学習状況の説明。毎回の授業報告の記載なし", price="1回50分×月4回 24,200円〜（税込・学年の記載なし。中学3年生の例は30,800円〜）", contract="入会金16,500円・事務手数料5,500円・選抜費11,000円〜、教材は家庭で用意、休会・退会・入会キャンセルは規約に明記（退会の締め切りがよくある質問と規約で異なる）"),
    "tos": dict(support="不登校・発達障害対策を掲げる。専門スタッフの発達検査、臨床心理士などのカウンセリング（いずれも有料）", teacher="登録教師向けに発達障害児指導の勉強会・資格講座を開催。臨床心理士資格の家庭教師も在籍", trial="実際に担当する家庭教師による無料体験と明記（訪問を前提にした説明。オンラインでも同じかは要確認）", time="オンラインは1回60分から", parent="センターで随時学習相談。先生は月1回センターへ報告", price="オンライン 幼児〜中学3年生 60分×月4回 19,400円（税込）", contract="入会金33,000円（税込）、テキスト代・管理費なし、解約金・違約金なし（退会は1か月以上前、最低1か月・6時間）。休会の決まりは記載なし"),
}

ORDER_TIE = ["support", "teacher"]


def total(s):
    return round(sum(s["scores"].values()) / len(AXES), 1)


RANK = sorted(S, key=lambda k: (-total(S[k]), *[-S[k]["scores"][a] for a in ORDER_TIE], S[k]["price_month"]))
for i, k in enumerate(RANK, 1):
    S[k]["rank"] = i
    S[k]["id"] = k
    S[k]["total"] = total(S[k])


def stars(v):
    n = int(v + 0.5)
    return "★" * n + "☆" * (5 - n)


def grade(v):
    return "S" if v >= 4.5 else "A" if v >= 4.0 else "B"


# ボタンの上の一言（置き場所ごとに変える。なければ btn_catch）。すべて公式サイトの記載にもとづく
CATCH = {
    "sogaku": {"compare": "比較17項目のうち13項目で◎", "combo": "体験は2回とも無料", "rank_tab": "担当予定の先生と無料体験2回",
               "plan": "違約金・途中解約料0円", "plan_card": "科目を増やしても料金は同じ", "pickup": "合わなければ先生の交代も無料",
               "detail_strength": "先生は全員、研修を受けた社会人", "detail_fit": "当てはまったら、まず体験で相性を確認",
               "detail_fee": "入会金はキャンペーンで無料の場合あり", "detail_flow": "申込フォームは簡単3分（公式）",
               "detail_voice": "担任制で、毎回同じ先生が教える", "detail_faq": "違約金・途中解約料0円"},
    "rebalance": {"rank_tab": "体験だけでも個別指導計画書がもらえる", "plan": "一律の料金表はなく、予算に合わせて提案",
                  "detail_strength": "授業後は毎回フィードバック", "detail_fee": "指定教材は原則なし",
                  "detail_flow": "体験は約90分・オンライン", "detail_voice": "体験だけでも指導計画書がもらえる", "detail_faq": "診断を受けていなくても指導できる"},
    "try": {"rank_tab": "教育プランナーが専任でつく", "plan": "教材費・年会費なしと公式に記載",
            "detail_strength": "WISC検査の結果を学習に活かす", "detail_fee": "前月までの申し出で解約金なし",
            "detail_flow": "保護者だけの面談もできる", "detail_faq": "前日22時までの連絡で振替できる"},
    "coaching1": {"rank_tab": "発達特性のある子の受験に対応", "plan": "教材費・ファイル代はかからない",
                  "detail_strength": "提携する臨床心理士の発達検査あり", "detail_fee": "教材は市販のものから選ぶ方針",
                  "detail_flow": "体験はオンラインでも受けられる", "detail_voice": "毎回の指導報告書あり", "detail_faq": "診断がなくても指導を受けられる"},
    "kizuki": {"rank_tab": "保護者だけの相談・見学もできる", "plan": "講師・科目の変更は無料",
               "detail_strength": "顔を出さずに音声とチャットで受けられる", "detail_fee": "入会8日以内のキャンセルは全額返金（規約）",
               "detail_flow": "面談は電話・オンラインでもできる", "detail_voice": "保護者だけの相談・見学もできる", "detail_faq": "出席扱いの相談もできる"},
    "tos": {"rank_tab": "実際に担当する先生と無料体験", "plan": "テキスト代・管理費はかからない",
            "detail_strength": "先生の交代は何回でも無料", "detail_fee": "解約金・違約金はかからない",
            "detail_flow": "体験の前に入会金はかからない", "detail_faq": "心理カウンセリングだけの相談もできる"},
}


def catch(s, key):
    return CATCH.get(s["id"], {}).get(key, s["btn_catch"])


def esc(t):
    return html.escape(t, quote=True)


def link_attrs(s, cta=None):
    if s["sponsored"]:
        return f'href="{s["url"]}" target="_blank" rel="sponsored nofollow noopener" data-cta data-cta-id="{cta or "ranking"}"'
    return f'href="{s["url"]}" target="_blank" rel="nofollow noopener" data-other-cta="{cta or "ranking"}"'


def logo_img(s, cls="", alt=None, lazy=True):
    f, w, h = s["logo"]
    return f'<img{(" class=%s" % chr(34) + cls + chr(34)) if cls else ""} src="{IMG}{f}" alt="{esc(s["name"] if alt is None else alt)}" width="{w}" height="{h}"{" loading=" + chr(34) + "lazy" + chr(34) if lazy else ""}>'


def banner(s, cls, cta):
    """公式バナー枠：ソウガクはASP発行バナー（コードのまま）、ほかはASP素材がないので公式ロゴで代える"""
    if s["sponsored"]:
        return (f'<a class="{cls} rk-banner" {link_attrs(s, cta)}><img src="{ASP_IMG}" width="300" height="250" '
                f'alt="{esc(s["full"])}" loading="lazy"></a>')
    return f'<span class="{cls} rk-logobox">{logo_img(s)}</span>'


def topshot(s, cta):
    """各社公式サイトのトップページの画面（CHECKED時点、images/official/top/）。ランキングのイチオシタブに置く"""
    img = f'<img src="{IMG}official/top/{s["id"]}.webp" alt="{esc(s["name"])}公式サイトのトップページの画面" width="960" height="600" loading="lazy">'
    return (f'<figure class="rk-topshot"><a {link_attrs(s, cta)}>{img}</a>'
            f'<figcaption>{esc(s["short"])}公式サイトのトップページ（{CHECKED}時点）</figcaption></figure>')


def head(title, desc):
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="stylesheet" href="../parts.css">
<link rel="stylesheet" href="yk-parts.css">
<link rel="stylesheet" href="ranking.css">
<script defer src="../lp-measurement.js?v=20261016"></script>
</head>
<body>
<main class="yk-body rk-wrap">
"""


FOOTER = f"""
<footer class="yk-footer"><ul><li><a href="../operator.html">運営者情報</a></li><li><a href="method.html">ランキング調査概要</a></li><li><a href="../privacy.html">プライバシーポリシー</a></li><li><a href="../disclosure.html">広告掲載について</a></li></ul><small>© {SITE}</small></footer>
"""

RADAR_JS = """<script>
/* yk-radar：data-labels（カンマ区切り）と data-scores（同じ数）からレーダーチャートを描く。ページ末尾に1回だけ置く */
document.querySelectorAll('.yk-radar[data-labels]').forEach(function (el) {
  var L = el.dataset.labels.split(','), S = el.dataset.scores.split(',').map(Number), M = +(el.dataset.max || 5), n = L.length, cx = 160, cy = 150, R = 100;
  function p(i, r) { var a = -Math.PI / 2 + i * 2 * Math.PI / n; return [(cx + r * Math.cos(a)).toFixed(1), (cy + r * Math.sin(a)).toFixed(1)]; }
  var s = '<svg viewBox="0 0 320 300" role="img" aria-label="' + (el.dataset.name || '') + 'の評価：' + L.map(function (l, i) { return l + ' ' + S[i]; }).join('、') + '">';
  for (var k = 1; k <= M; k++) s += '<polygon points="' + L.map(function (_, i) { return p(i, R * k / M).join(','); }).join(' ') + '" fill="none" stroke="#c9d3e3"/>';
  L.forEach(function (l, i) { var a = p(i, R), b = p(i, R + 24); s += '<line x1="' + cx + '" y1="' + cy + '" x2="' + a[0] + '" y2="' + a[1] + '" stroke="#c9d3e3"/><text x="' + b[0] + '" y="' + b[1] + '" text-anchor="middle" dominant-baseline="middle" font-size="12" font-weight="700" fill="#444">' + l + '</text>'; });
  s += '<polygon points="' + S.map(function (v, i) { return p(i, R * v / M).join(','); }).join(' ') + '" fill="rgba(47,103,184,.18)" stroke="#2f67b8" stroke-width="2.5"/></svg>';
  el.innerHTML = s;
});
</script>
"""


def end(scripts=""):
    return FOOTER + "</main>\n" + scripts + "</body>\n</html>\n"


def radar(s):
    labels = ",".join(a[1] for a in AXES)
    scores = ",".join(str(s["scores"][a[0]]) for a in AXES)
    return (f'<div class="yk-radar" data-name="{esc(s["short"])}" data-labels="{labels}" data-scores="{scores}"></div>\n')


def info_table(s):
    r = s["info"]
    rows = ""
    for i in range(0, 6, 2):
        (a, av), (b, bv) = r[i], r[i + 1]
        left = ' class="is-left"' if i == 4 else ""
        rows += f"<tr><th>{a}</th><th>{b}</th></tr><tr><td{left}>{av}</td><td{left}>{bv}</td></tr>"
    return f'<table class="yk-info">{rows}</table>'


def features(s, ttl="特徴"):
    lis = "".join(f'<li><span>{t}</span></li>' for t, _ in s["features"])
    return (f'<div class="yk-features"><p class="yk-features__ttl">{ttl}</p><ul>{lis}'
            f'<li><span class="yk-red">対象：{s["target"]}</span></li></ul></div>')


def jobex(s):
    cards = ""
    for i, (g, plan, price, note) in enumerate(s["plans"], 1):
        cards += (f'<div class="yk-jobex"><p class="yk-jobex__ttl">料金プランの例{i}</p><ul class="yk-tags yk-tags--green"><li>{g}</li><li>{s.get("plan_tag", "オンライン")}</li></ul>'
                  f'<table class="yk-kv"><tr><th>{s.get("plan_label", "月額")}</th><td><b>{price}</b></td></tr><tr><th>授業</th><td>{plan}</td></tr><tr><th>補足</th><td>{note}</td></tr></table>'
                  f'<p class="yk-catch">{esc(catch(s, "plan"))}</p><a class="yk-btn yk-btn--sm" {link_attrs(s, "rank_plan")}>公式で料金を見る</a>'
                  f'<span class="yk-jobex__logo" style="display:block">{logo_img(s, alt="")}</span></div>')
    hint = '<p class="yk-hint">横にスクロールできます</p>' if len(s["plans"]) > 1 else ""
    return (f'{hint}<div class="yk-hscroll">{cards}</div>\n'
            f'<p class="yk-small">※{s["plan_note"]}。出典：<a href="{s["plan_src"]}" target="_blank" rel="nofollow noopener">{esc(s["short"])}公式サイト</a></p>')


def voices(s):
    if not s["voices"]:
        return ""
    i = s.get("voice_pick", 0)
    lis = "".join(f'<li><div class="yk-voice__who"><span class="yk-voice__face"><img src="{IMG}gen/icon_parent2.webp" alt="" width="240" height="240" loading="lazy"></span>{esc(w)}</div><p>{esc(t)}</p></li>'
                  for w, t in s["voices"][i:i + 1])
    return (f'<h4 class="yk-voice__ttl">{esc(s["short"])}の口コミ</h4>\n<ul class="yk-voice">{lis}</ul>\n'
            f'<p class="yk-small">※<a href="{s["voice_src"]}" target="_blank" rel="nofollow noopener">{esc(s["short"])}公式サイト</a>掲載の声を要約。個人の感想です。</p>')


def btn_main(s, cta, text=None):
    return f'<p class="yk-catch">{esc(catch(s, cta))}</p><a class="yk-btn" {link_attrs(s, cta)}>{text or s["btn"]}</a>'


# ---------------------------------------------------------------- トップ
def talk_row(who, text, right):
    icon = "icon_parent2" if who == "保護者" else "icon_editor2"
    r = " mt-talk__row--r" if right else ""
    return (f'<div class="mt-talk__row{r}"><div class="mt-talk__who"><span class="mt-talk__icon"><img src="{IMG}gen/{icon}.webp" '
            f'srcset="{IMG}gen/{icon}-120.webp 120w, {IMG}gen/{icon}.webp 240w" sizes="56px" alt="" width="240" height="240"></span>'
            f'<span class="mt-talk__name">{who}</span></div><div class="mt-talk__b">{text}</div></div>')


# 項目別の詳細比較（各社公式サイトの記載、CHECKED確認）。記号は当サイトの判断：◎＝特に手厚い／○＝ある／△＝限られる／－＝公式に記載なし
# グループ＝比較表のタブ。各項目は会社ID→（記号, 短い説明）
CMP_GROUPS = [
    ("特性・先生", ["専門の範囲", "専門家の関わり", "先生", "指導計画", "診断・手帳"]),
    ("体験・授業", ["最短の授業", "体験を担当する人", "体験の回数・時間", "授業の報告", "保護者の相談", "時間の融通", "学校に行きづらい子"]),
    ("料金・契約", ["小学生の料金", "入会金", "教材費", "解約・違約金", "先生の交代"]),
]
CMP = {
    "sogaku": {
        "専門の範囲": ("◎", "発達障害・グレーゾーン専門"),
        "専門家の関わり": ("◎", "専門機関（発達凸凹アソシエーション）が講師研修・アセスメントシート・教材アドバイス"),
        "先生": ("◎", "全員が社会人で、専門機関の研修を受講。臨床心理士・作業療法士などの資格者も在籍"),
        "指導計画": ("◎", "専門家が開発したアセスメントシートで一人ずつ作成。体験後に受け取れる"),
        "診断・手帳": ("◎", "診断は不要。診断名の申告・手帳の提出も不要と明記"),
        "最短の授業": ("◎", "小学生25分・中高生35分"),
        "体験を担当する人": ("◎", "入会後に担当する予定の先生"),
        "体験の回数・時間": ("◎", "2回。小学生25分か50分（中高生35分か60分）。1回目を保護者面談にもできる"),
        "授業の報告": ("◎", "毎回、アプリで指導報告。状況と対策も定期的にフィードバック"),
        "保護者の相談": ("◎", "先生・本部にチャット。定期的な保護者面談、保護者向け勉強会、家での学習環境のアドバイス"),
        "時間の融通": ("○", "土日・夜21時〜・午前も可。回数・時間は月ごとに変更、同じ月内で振替"),
        "学校に行きづらい子": ("○", "午前中の授業に対応"),
        "小学生の料金": ("◎", "25分×月4回 13,200円（税込）。6社で月額の目安がいちばん低い"),
        "入会金": ("○", "22,000円（税込）。キャンペーンで無料の場合あり"),
        "教材費": ("◎", "購入不要。専門家の推奨教材リストから選ぶ。学習ツール（映像授業2,000本など）も追加費用なし"),
        "解約・違約金": ("◎", "違約金・途中解約料0円、契約期間の縛りなし、月単位で休会・退会"),
        "先生の交代": ("◎", "何度でも無料。性別の希望も伝えられる。担任制で毎回同じ先生"),
    },
    "rebalance": {
        "専門の範囲": ("◎", "LD・ADHD・ASD・グレーゾーン・ギフテッド（2E）専門"),
        "専門家の関わり": ("○", "臨床心理士との連携、日本LD学会の機関会員。体験では発達検査の結果も読み解く"),
        "先生": ("◎", "プロ講師（社会人・有資格の学生）と、同じ学科研修・技能研修を終えたセミプロ講師"),
        "指導計画": ("◎", "体験後に個別指導計画書（IEP）をメールで共有。入会しなくても受け取れる"),
        "診断・手帳": ("◎", "確定診断のないグレーゾーンの子のほうが多いと記載。検査なしでも指導できる"),
        "最短の授業": ("△", "1回60分から"),
        "体験を担当する人": ("△", "記載なし（体験のあとに合う先生を選ぶ）"),
        "体験の回数・時間": ("○", "約90分（聞き取り30分・模擬授業30分・提案30分）"),
        "授業の報告": ("◎", "授業後に毎回フィードバック（5分程度）"),
        "保護者の相談": ("◎", "教務に相談、無料の定期面談。AIのペアレントトレーニングもある"),
        "時間の融通": ("○", "前日までの連絡で振替。難しければ翌月以降に繰り越し"),
        "学校に行きづらい子": ("○", "不登校でも指導できると記載"),
        "小学生の料金": ("△", "60分×月4回 22,000円〜（税込・セミプロ講師）"),
        "入会金": ("○", "19,800円（税込）。別に年間管理費26,400円"),
        "教材費": ("◎", "指定教材は原則なし。学校のテキスト中心"),
        "解約・違約金": ("○", "前月末までの申し出で中途解約金なし（即時解約は月謝1か月分か2万円の低い方）"),
        "先生の交代": ("－", "交代の決まりは記載なし（担当制で原則同じ講師）"),
    },
    "try": {
        "専門の範囲": ("○", "オンライン個別指導塾のコースの一つ（発達特性サポートコース）"),
        "専門家の関わり": ("○", "正社員の教育プランナーが家庭ごとに付く"),
        "先生": ("○", "個性別支援の認定教師から選ぶ。全員が研修を受講"),
        "指導計画": ("◎", "教育プランナーが専用カリキュラムを作成。WISC検査の結果をもとにサポート"),
        "診断・手帳": ("○", "発達障害・学習障害があっても入会できる（要否の明記なし）"),
        "最短の授業": ("△", "料金例は1コマ60分（最短の明記なし）"),
        "体験を担当する人": ("△", "記載なし（事前の学習面談は教育プランナー）"),
        "体験の回数・時間": ("○", "体験授業（英語か数学。約30分・約60分とページで記載が異なる）＋無料の学習面談"),
        "授業の報告": ("◎", "アプリで授業ごとの進み具合と先生のコメント"),
        "保護者の相談": ("◎", "教育プランナーが定期面談。電話・LINEでも相談"),
        "時間の融通": ("◎", "日程は自由。前日22時までの連絡で無料振替。回数・科目・時間はいつでも変更"),
        "学校に行きづらい子": ("◎", "不登校サポートコース。在籍校で出席と認められた実績あり"),
        "小学生の料金": ("○", "60分×月4回 14,960円〜（税込）"),
        "入会金": ("○", "11,000円（税込）"),
        "教材費": ("◎", "教材費無料。年会費・登録料・更新費なし"),
        "解約・違約金": ("○", "前月までの申し出で解約金なし。8日以内はクーリングオフ"),
        "先生の交代": ("◎", "何度でも無料。教科ごとに選んでも追加費用なし"),
    },
    "coaching1": {
        "専門の範囲": ("◎", "発達障害・グレーゾーン専門の学習進学塾"),
        "専門家の関わり": ("◎", "提携する臨床心理士の発達検査を受けられる"),
        "先生": ("○", "発達指導の講師は独自の研修を受けて担当（チーム制）"),
        "指導計画": ("◎", "WISCなどのデータで特性を分析して学習計画"),
        "診断・手帳": ("○", "診断・発達検査がなくても指導すると記載"),
        "最短の授業": ("△", "オンラインは1回60分から"),
        "体験を担当する人": ("△", "担当教務（スタッフ）"),
        "体験の回数・時間": ("○", "体験授業と学習カウンセリングで約120分（オンラインも可）"),
        "授業の報告": ("◎", "毎回、指導報告書"),
        "保護者の相談": ("○", "授業以外も教務部に相談できる"),
        "時間の融通": ("△", "振替あり。オンライン指導は翌月以降への振替不可"),
        "学校に行きづらい子": ("○", "不登校コーチングあり"),
        "小学生の料金": ("△", "オンライン60分×月4回 25,300円（税込）"),
        "入会金": ("○", "18,700円（税込）。別に年会費26,400円"),
        "教材費": ("◎", "教材費・ファイル代などはかからない"),
        "解約・違約金": ("△", "前月末までの申し出で中途解約金なし。契約期間は1年で自動更新"),
        "先生の交代": ("－", "交代の決まりは記載なし（チーム制で講師の入れ替わりあり）"),
    },
    "kizuki": {
        "専門の範囲": ("○", "不登校・発達障害・グレーゾーン・中退・社会人の学び直し"),
        "専門家の関わり": ("△", "メンターがアセスメントで特性を一緒に確かめる（専門家の関わりの記載なし）"),
        "先生": ("○", "面談をもとに講師を選定。プロ講師や「特性×学び」に特化した専門講師のコースあり"),
        "指導計画": ("○", "入会アセスメントに合わせて講師を提案。メンターと学習計画をつくる"),
        "診断・手帳": ("○", "グレーゾーンも対象と記載（要否の明記なし）"),
        "最短の授業": ("○", "1回50分"),
        "体験を担当する人": ("－", "常設の体験授業なし（期間限定の場合あり）"),
        "体験の回数・時間": ("△", "無料の入会相談・見学のみ（保護者だけの相談もできる）"),
        "授業の報告": ("－", "毎回の報告の記載なし"),
        "保護者の相談": ("○", "おやサポメンター（月1回30分）で教務から学習状況を聞ける"),
        "時間の融通": ("○", "前日までの連絡で無料変更・振替。21時まで授業"),
        "学校に行きづらい子": ("◎", "不登校の学び直しが中心。出席扱いの相談もできる"),
        "小学生の料金": ("－", "要確認。小学生の金額は記載なし（50分×月4回24,200円〜の記載、中3の例は30,800円〜）"),
        "入会金": ("△", "16,500円＋事務手数料5,500円＋選抜費11,000円〜"),
        "教材費": ("○", "市販の参考書や手持ちの教材を使う（家庭で用意）"),
        "解約・違約金": ("○", "入会8日以内のキャンセルは全額返金。休会・退会は前々月末までに申請（規約）"),
        "先生の交代": ("◎", "講師・科目の変更は無料"),
    },
    "tos": {
        "専門の範囲": ("○", "不登校・発達障害・成績不振対策の家庭教師"),
        "専門家の関わり": ("○", "専門スタッフの発達検査、臨床心理士などのカウンセリング（いずれも有料）"),
        "先生": ("○", "大学生・社会人・プロから選定。発達障害児指導の勉強会・資格講座を開催"),
        "指導計画": ("○", "希望を聞いて先生を選び、体験で先生が目標と方針を確認"),
        "診断・手帳": ("－", "要否の記載なし"),
        "最短の授業": ("△", "オンラインは1回60分から"),
        "体験を担当する人": ("◎", "実際に担当する家庭教師（オンラインでも同じかは要確認）"),
        "体験の回数・時間": ("○", "面談を含めて40分〜1時間（体験授業は20〜30分）"),
        "授業の報告": ("△", "先生は月1回センターへ報告（保護者への報告の頻度は記載なし）"),
        "保護者の相談": ("○", "センターで随時学習相談。カウンセリングは有料"),
        "時間の融通": ("○", "土日・遅い時間も相談できる。テスト前は回数を増やせる"),
        "学校に行きづらい子": ("◎", "不登校からの受験・高認に対応"),
        "小学生の料金": ("○", "オンライン60分×月4回 19,400円（税込）"),
        "入会金": ("△", "33,000円（税込）"),
        "教材費": ("◎", "テキスト代・手数料・管理費などの追加費用なし"),
        "解約・違約金": ("○", "解約金・違約金なし。退会は1か月以上前に連絡、最低1か月・6時間"),
        "先生の交代": ("◎", "何回でも無料"),
    },
}
N_ITEMS = sum(len(items) for _, items in CMP_GROUPS)
# 「総合」タブの無料体験の欄：太字の一言＋補足1行（各社公式の記載、CHECKED確認）。記号は採点「入会前に確かめられること」の点
TRIAL_CELL = {
    "sogaku": ("担当予定の先生と2回", "25分か50分。1回目は親の面談にもできる"),
    "rebalance": ("体験授業あり", "約90分。担当者の記載なし"),
    "try": ("体験授業あり", "英語か数学。担当者の記載なし"),
    "coaching1": ("体験授業あり", "約120分。教務スタッフが担当"),
    "tos": ("担当予定の先生と1回", "40分〜1時間。オンラインは要確認"),
    "kizuki": ("体験授業なし", "入会相談・見学のみ"),
}
TRIAL_LEGEND = "◎＝入会後に担当する先生と試せる／○＝子どもが体験授業を受けられる／△＝相談・見学だけ"
CATCH["sogaku"]["compare"] = f"比較{N_ITEMS}項目のうち{sum(1 for _, items in CMP_GROUPS for it in items if CMP['sogaku'][it][0] == '◎')}項目で◎"


def top():
    R = [S[k] for k in RANK]
    names = "・".join(s["short"] for s in R)
    n_ax = len(AXES)
    o = head("【2026年10月】発達障害・グレーゾーンの子に合うオンライン家庭教師ランキングTOP3｜6社を比較",
             f"発達障害・グレーゾーンの子に対応したオンライン家庭教師6社（{names}）を、発達特性への対応・先生・入会前の確認・授業時間・保護者サポート・料金・費用と契約の{n_ax}項目で採点し、{N_ITEMS}項目で比較しました。")
    # A-1 FV ヒーロー画像（上に更新日【最新】、下にロゴの横流し）
    logos = "".join(f'<li>{logo_img(s, alt=s["name"])}</li>' for s in R) + "".join(f'<li>{logo_img(s, alt="")}</li>' for s in R)
    o += f"""
<!-- A-1 FV：更新日の帯（rk-update）＋ヒーロー画像（王道LPと同じ 00_hero_top3_v3。見出しは画像内の文字、同じ文を lp-sr に持つ）＋ロゴの横流し（yk-logos、2周目は alt=""） -->
<p class="rk-update"><time datetime="{CHECKED_ISO}">{CHECKED}</time><span>【最新】</span></p>
<h1 class="lp-hero"><span class="lp-sr">発達障害・グレーゾーンの子に合う オンライン家庭教師ランキングTOP3</span><img fetchpriority="high" src="{IMG}gen/00_hero_top3_v3.webp" srcset="{IMG}gen/00_hero_top3_v3-608.webp 608w, {IMG}gen/00_hero_top3_v3-912.webp 912w, {IMG}gen/00_hero_top3_v3.webp 1200w" sizes="(max-width: 751px) 100vw, 696px" alt="" width="1200" height="675"></h1>
<div class="yk-logos rk-logos" role="region" aria-label="比較したオンライン家庭教師6社"><ul class="yk-logos__track">{logos}</ul></div>
<p class="yk-pr"><b>PR</b><span>本ページは<wbr>広告・<wbr>アフィリエイトリンクを<wbr>含み⁠ま⁠す⁠。</span></p>
"""
    # A-2 導入会話（画像なし）
    rows = [
        ("保護者", "宿題を見ると、すぐ親子げんかに…。<span class='mt-mark'>発達特性を分かってくれる先生</span>って、どう選べばいいんでしょう？", True),
        ("編集部", "見るのは3つ。<b>先生が発達特性を学んでいるか</b>、<b>授業の長さ</b>、<b>入会前に実際の先生と試せるか</b>です。", False),
        ("保護者", "30分も座っていられるか心配で…。診断もまだなんです。", True),
        ("編集部", f"それなら、小学生は25分から選べて、診断なしでも相談できる<span class='mt-mark'>ソウガク</span>から試すのがおすすめです。6社を{n_ax}つの基準で採点したTOP3を下にまとめました。", False),
    ]
    o += ('\n<!-- A-2 導入会話（mt-talk）：FV直下。画像なし。よくある迷いを編集部が会話例にしたもの（実在の発言ではない） -->\n<div class="mt-talk" data-section-id="talk">'
          + "".join(talk_row(w, t, r) for w, t, r in rows) + '</div>\n')
    # B-1 BEST3
    items = ""
    for s in R[:3]:
        r, m, t = s["best3"]
        items += (f'<li class="yk-best3__item"><span class="yk-best3__crown">{s["rank"]}</span><span class="yk-best3__logo">{logo_img(s, lazy=False)}</span>'
                  f'<p class="yk-best3__text"><span class="yk-red">{r}</span><br><span class="yk-mark">{m}</span>。{t}</p>'
                  f'<p class="yk-catch">総合評価 {s["total"]}</p>'
                  f'<a class="yk-btn yk-btn--sm" {link_attrs(s, "best3")}>公式サイト</a></li>')
    o += f'\n<!-- B-1 BEST3（yk-best3）：順位の根拠は method.html -->\n<section class="yk-best3"><h2 class="yk-best3__ttl" data-section-id="best3"><em>発達特性</em>に強いオンライン家庭教師<em>TOP3</em></h2>\n<ol class="yk-best3__list">{items}</ol></section>\n'
    # B-2 ソウガクの目的別プラン（求人の例カードの型）
    sg = S["sogaku"]
    jobs = [
        ("集中が続きにくい・低学年", "05_online_home.webp", "家のノートパソコンで学ぶ子ども", "小学生", "25分×月4回", "13,200円", ["25分から", "体験2回", "毎回の報告"]),
        ("小学生でしっかり学びたい", "08_calm_home.webp", "落ち着いた部屋の机に向かう子ども", "小学生", "50分×月4回（公式のおすすめ）", "22,000円", ["5教科", "毎回の報告", "教材購入なし"]),
        ("中学生・受験も見据えて", "04_one_on_one.webp", "机で勉強する子ども", "中学生", "35分×月4回（60分は26,400円）", "18,480円", ["受験対策にも対応", "受験生割増なし", "振替あり"]),
        ("高校生・得意を活かしたい", "01_fv_study.webp", "机でノートに書く子ども", "高校生", "35分×月4回（60分は29,920円）", "21,560円", ["得意を活かす", "学年で料金アップなし", "違約金0円"]),
    ]
    cards = ""
    for ttl, img, alt, g, plan, pay, tags in jobs:
        tg = "".join(f"<li>{t}</li>" for t in tags)
        cards += (f'<div class="yk-jobcard"><h3 class="yk-jobcard__ttl">{ttl}</h3><img class="yk-jobcard__img" src="{IMG}{img}" alt="{alt}（イメージ）" width="960" height="640" loading="lazy">'
                  f'<p class="yk-jobcard__pay">月額<b>{pay}</b></p><table class="yk-kv"><tr><th>学年</th><td>{g}</td></tr>'
                  f'<tr><th>授業</th><td>{plan}</td></tr></table><ul class="yk-tags">{tg}</ul>'
                  f'<p class="yk-catch">{esc(catch(sg, "plan_card"))}</p><a class="yk-btn yk-btn--sm" {link_attrs(sg, "plan_card")}>無料体験を公式で見る</a></div>')
    o += f"""
<!-- B-2 1位ソウガクの目的別プラン（yk-hscroll + yk-jobcard）：公式の料金表（{sg["plan_src"]}、{CHECKED}確認） -->
<h2 class="yk-sec-ttl" data-section-id="plans">1位<em>ソウガク</em>の料金プラン｜目的別の例</h2>
<p class="yk-hint">横にスクロールできます</p>
<div class="yk-hscroll">{cards}</div>
<p class="yk-small">※月4回・税込。入会金22,000円は別途（キャンペーンで無料の場合あり）。写真はイメージです。</p>
"""
    # C-1 比較表（タブ：総合＋17項目を3つのタブに）
    def mk(v):
        return {5: "◎", 4: "○", 3: "△", 2: "△", 1: "×"}[v]
    rows = ""
    for s in R:
        chips = "".join(f'<li class="{c}">{t}</li>' if c else f"<li>{t}</li>" for c, t in s["chips"])
        rows += (f'<tr{" class=" + chr(34) + "is-pick" + chr(34) if s["rank"] == 1 else ""}><td><span class="yk-cmp__rank">{s["rank"]}</span><span class="yk-cmp__logo" style="display:block">{logo_img(s)}</span>'
                 f'<a class="yk-cmp__name" href="{s["id"]}.html">{esc(s["short"])}</a><span class="yk-stars">{stars(s["total"])}</span><span class="yk-grade">総合評価 <b>{s["total"]}</b></span></td>'
                 f'<td><span class="yk-maru">{mk(s["scores"]["trial"])}</span><b class="rk-trial__b">{TRIAL_CELL[s["id"]][0]}</b><small class="rk-trial__s">{TRIAL_CELL[s["id"]][1]}</small></td>'
                 f'<td class="is-left">{s["cmp_text"]}<ul class="yk-chips">{chips}</ul></td>'
                 f'<td><a class="yk-btn yk-btn--sm" {link_attrs(s, "comparison")}>公式</a></td></tr>')
    heads = "".join(f'<th{" class=" + chr(34) + "is-pick" + chr(34) if s["rank"] == 1 else ""}>{s["rank"]}位<br>{esc(s["short"])}</th>' for s in R)
    panels = ""
    for _, items in CMP_GROUPS:
        body = ""
        for it in items:
            tds = "".join(f'<td class="is-left{" is-pick" if s["rank"] == 1 else ""}"><span class="yk-maru">{CMP[s["id"]][it][0]}</span>{CMP[s["id"]][it][1]}</td>' for s in R)
            body += f"<tr><th>{it}</th>{tds}</tr>"
        panels += f'\n    <div><p class="yk-hint">横にスクロールできます</p><div class="rk-scroll"><table class="yk-cmp rk-detail-cmp"><tr><th>項目</th>{heads}</tr>{body}</table></div></div>'
    labels = "".join(f'<label for="cmp1-{i}">{g}</label>' for i, (g, _) in enumerate(CMP_GROUPS, 2))
    radios = "".join(f'<input type="radio" name="cmp1" id="cmp1-{i}">' for i in range(2, len(CMP_GROUPS) + 2))
    win = sum(1 for _, items in CMP_GROUPS for it in items if CMP["sogaku"][it][0] == "◎")
    o += f"""
<!-- C-1 タブ切替の比較表（yk-tabs + yk-cmp + yk-fold）：総合（6社・採点）＋{N_ITEMS}項目を3つのタブに。各社公式サイトの記載（{CHECKED}確認）。採点の基準は method.html -->
<h2 class="yk-sec-ttl" id="compare" data-section-id="comparison"><em>6社</em>を{N_ITEMS}項目で比較</h2>
<p>先生・体験・授業の長さ・報告・費用や契約まで、各社の公式サイトに書かれていることを並べました。<span class="yk-mark">1位のソウガクは{N_ITEMS}項目のうち{win}項目で◎</span>です。</p>
<div class="yk-tabs rk-tabs4">
  <input type="radio" name="cmp1" id="cmp1-1" checked>{radios}
  <div class="yk-tabs__labels"><label for="cmp1-1">総合</label>{labels}</div>
  <div class="yk-tabs__panels">
    <div><p class="rk-trial-legend">無料体験の記号：{TRIAL_LEGEND}</p><div class="yk-fold"><input type="checkbox" id="cmp1-more"><div class="yk-fold__body">
      <table class="yk-cmp"><colgroup><col class="c1"><col class="c2"><col><col class="c4"></colgroup>
        <tr><th>サービス</th><th>無料体験</th><th>編集部のひとこと</th><th>公式</th></tr>
        {rows}
      </table></div><label class="yk-fold__btn" for="cmp1-more">もっと見る</label></div></div>{panels}
  </div>
</div>
<p class="yk-small">※◎＝特に手厚い、○＝ある、△＝限られる、－＝記載なし。各社公式サイトの記載をもとにした当サイトの判断です（{CHECKED}確認・<a href="method.html">採点基準</a>）。</p>
{btn_main(sg, "compare")}
"""
    # C-2 2軸マップ（縦＝入会前の確認、横＝特性への対応＋先生）
    pos = {"sogaku": (80, 16), "tos": (27, 16), "rebalance": (84, 58), "coaching1": (55, 42), "try": (25, 50), "kizuki": (19, 84)}
    items = ""
    for s in R:
        x, y = pos[s["id"]]
        if s["rank"] == 1:
            items += (f'<div class="yk-matrix__item is-pick" style="--x:{x}%;--y:{y}%"><span class="rk-mlogo">{logo_img(s)}</span><ul><li>✔ 担当予定の先生と体験2回</li>'
                      f'<li>✔ 全員が研修を受けた社会人講師</li></ul></div>')
        else:
            items += f'<span class="yk-matrix__item" style="--x:{x}%;--y:{y}%">{logo_img(s)}</span>'
    o += f"""
<!-- C-2 2軸の早見表（yk-matrix）：縦＝採点「入会前に確かめられること」、横＝採点「特性への対応＋先生」（method.html） -->
<h2 class="yk-sec-ttl" data-section-id="matrix">ひと目でわかる<em>6社の位置</em></h2>
<div class="yk-matrix">
  <span class="yk-matrix__ax yk-matrix__ax--t">担当の先生と試せる</span><span class="yk-matrix__ax yk-matrix__ax--b">相談が中心</span><span class="yk-matrix__ax yk-matrix__ax--l">特性への支援 標準</span><span class="yk-matrix__ax yk-matrix__ax--r">特性への支援 厚い</span>
  {items}
</div>
<p class="yk-small">※縦・横は当サイトの採点です（<a href="method.html">採点基準</a>）。</p>
"""
    # C-3 ソウガクの無料体験2回（yk-combo の型をソウガク1社で使う）
    o += f"""
<!-- C-3 無料体験のすすめ（yk-combo）：ソウガク1社・カード1枚（公式 faq.html・trial-flow.html、{CHECKED}確認） -->
<section class="yk-combo"><h2 class="yk-combo__ttl" data-section-id="trial"><em>ソウガク</em>の無料体験2回で<br>先生との相性を確かめましょう！</h2>
  <div class="yk-combo__card"><p class="yk-combo__head">担当予定の先生と、2回試してから決められる</p><span class="yk-combo__logo" style="display:block">{logo_img(sg)}</span><a class="yk-combo__link" href="sogaku.html#f3">体験の流れを見る</a>
    <ul class="yk-combo__points"><li><b>1回目は保護者と先生の面談にもできる！</b><br>体験では、入会後に受け持つ予定の先生が教えます。子どもの様子や苦手なことを先に伝えてから、2回目に授業を受けられます。</li><li><b>小学生は25分か50分！</b><br>中高生は35分か60分。最初に流れを説明して、できることから始めます。</li><li><b>体験後に指導計画がもらえる</b><br>得意・不得意をまとめた、その子だけの指導計画を受け取れます。相性が合えば、そのまま同じ先生が担当します。無理な入会の勧誘や教材の販売もありません（公式）。</li></ul>
    {btn_main(sg, "combo")}</div>
</section>
"""
    # D ランキング
    o += f"""
<!-- D ランキング：順位見出し→赤キャッチ→タブ（イチオシ／基本情報／料金プラン例）→特徴→編集部→口コミ→2ボタン -->
<h2 class="yk-sec-ttl" id="ranking" data-section-id="ranking">発達特性に強いオンライン家庭教師<br><em>おすすめランキング</em></h2>
<div class="mt-say"><span class="mt-say__icon"><img src="{IMG}gen/icon_editor2.webp" alt="" width="240" height="240" loading="lazy"></span><p class="mt-say__b">先生との相性は、体験してみないと分かりません。ソウガクは入会後に担当する予定の先生と2回体験できるので、まずはそこで確かめるのがおすすめです。</p></div>
"""
    for s in R:
        n = s["rank"]
        medal = "yk-medal" + {1: "", 2: " yk-medal--2", 3: " yk-medal--3"}.get(n, " yk-medal--n")
        o += f"""
<!-- 第{n}位 {s["name"]}（事実の出典：{s["official"]} ほか、{CHECKED}確認） -->
<div class="yk-rankarea" id="rank-{s["id"]}" data-section-id="rank_{s["id"]}"><h3 class="yk-rankhead"><span class="{medal}">{n}</span>{esc(s["name"])}</h3><p class="yk-rankcatch">{s["catch"]}</p>
<div class="yk-tabs">
  <input type="radio" name="rk{n}" id="rk{n}-1" checked><input type="radio" name="rk{n}" id="rk{n}-2"><input type="radio" name="rk{n}" id="rk{n}-3">
  <div class="yk-tabs__labels"><label for="rk{n}-1">イチオシ<br>ポイント</label><label for="rk{n}-2">基本情報</label><label for="rk{n}-3">料金<br>プラン例</label></div>
  <div class="yk-tabs__panels" style="background:#fff;padding:10px">
    <div>{topshot(s, "rank_topshot")}{btn_main(s, "rank_tab")}
    {features(s)}</div>
    <div>{radar(s)}
    {info_table(s)}</div>
    <div>{jobex(s)}</div>
  </div>
</div>
<div class="yk-editor"><p class="yk-editor__ttl">編集部の<em>イチオシ</em>ポイント</p><img class="yk-editor__chara" src="{IMG}gen/icon_editor2.webp" alt="" width="240" height="240" loading="lazy">
<div class="yk-editor__body"><p>{s["editor"][0]}</p>{('<p class="yk-small" style="text-align:right">' + s["editor"][1] + '</p>') if s["editor"][1] else ""}</div></div>
{voices(s)}
<div class="yk-btnpair"><a class="yk-btn yk-btn--sub" href="{s["id"]}.html">詳細は<br>こちら</a><div>{btn_main(s, "rank")}</div></div>
</div>
"""
    # E-1 迷ったらまずは（ソウガクだけ）
    o += f"""
<!-- E-1 迷ったらまずは（yk-pickup）：ソウガク1社 -->
<section class="yk-pickup"><h2 class="yk-pickup__ttl" data-section-id="pickup"><small>迷ったらまずは</small><br><em>ソウガク</em>の無料体験から！</h2>
<ul class="yk-pickup__list">
  <li class="yk-pickup__item"><p class="yk-pickup__name">ソウガク</p>{banner(sg, "yk-pickup__img", "pickup_banner")}<p class="yk-pickup__text">発達特性を学んだ社会人講師が担当し、授業は小学生25分・中高生35分から選べます。担当予定の先生と2回試してから決められます。違約金・途中解約料は0円です。</p><p class="yk-catch">{esc(catch(sg, "pickup"))}</p><a class="yk-btn yk-btn--sm" {link_attrs(sg, "pickup")}>無料体験を公式で見る</a></li>
</ul></section>
"""
    # E-2 診断
    o += f"""
<!-- E-2 診断フォーム（yk-finder）：結果は下の rk-result にその場で表示。判定は各社公式の記載で決められる条件だけ（rules は ranking.js） -->
<form class="yk-finder" id="finder" data-section-id="finder" action="#finder-result"><p class="yk-finder__ttl">オンライン家庭教師<br><em>かんたん</em>診断</p>
  <label class="yk-finder__row">学年<select name="grade"><option value="">指定なし</option><option value="pre">未就学</option><option value="es">小学生</option><option value="jhs">中学生</option><option value="hs">高校生</option></select></label>
  <label class="yk-finder__row">いちばん気になること<select name="concern"><option value="">指定なし</option><option value="focus">集中が続きにくい</option><option value="match">先生との相性</option><option value="nodiag">診断を受けていない</option><option value="school">学校に行きづらい</option><option value="exam">受験を考えている</option><option value="cost">費用を抑えたい</option></select></label>
  <label class="yk-finder__row">1回の授業の長さ<select name="length"><option value="">指定なし</option><option value="short">30分くらいまで</option><option value="mid">60分くらい</option><option value="long">90分でもよい</option></select></label>
  <fieldset><legend>こだわり条件</legend><div class="yk-finder__checks"><label><input type="checkbox" name="report">毎回の報告がほしい</label><label><input type="checkbox" name="adult">社会人の先生がいい</label><label><input type="checkbox" name="contract">解約の決まりが明確</label><label><input type="checkbox" name="flex">回数を固定したくない</label></div></fieldset>
  <button class="yk-finder__submit" type="submit">診断する</button></form>
<div class="rk-result" id="finder-result" aria-live="polite" hidden></div>
<p class="yk-small">※公式サイトの記載をもとにした目安です。入力内容は送信・保存しません。</p>
"""
    js = RADAR_JS + '<script src="ranking.js"></script>\n'
    return o + end(js)


# ---------------------------------------------------------------- 個別ページ
DETAIL = {}
DETAIL["sogaku"] = dict(
    strengths=[
        ("発達特性を学んだ社会人講師が教える",
         "<p>ソウガクの先生は全員が社会人で、発達支援の専門機関「一般社団法人 発達凸凹アソシエーション」による教師研修と、座学のマニュアル研修を受けています。発達凸凹アソシエーションは2014年から発達障害・グレーゾーンの保護者向け研修を行っている団体で、講師研修のほか、教材のアドバイスやスタッフ研修にも関わっています。放課後等デイサービスや児童発達支援事業所で働いた経験がある先生や、臨床心理士・作業療法士・学校教員などの資格を持つ先生も在籍しています。</p>"
         "<p>宿題を始めるまでに時間がかかる、説明の途中で気がそれる。そんなときの声のかけ方を学んだ先生が担当します。</p>",
         ("official/sogaku/course-top_tool_communication.png", 600, 487, "授業後の指導報告と、教師・本部とのチャットの画面", "https://sogaku.jp/online/course.html")),
        ("小学生は25分から。短い授業で始められる",
         "<p>コースは小学生が25分・50分・75分、中高生が35分・60分・75分です。集中が続きにくい子や低学年向けに、短いコースが用意されています。勉強だけでなく、会話や脳トレのようなゲームを取り入れることもあります。</p>",
         None),
        ("担当予定の先生と、無料体験を2回受けられる",
         "<p>無料体験は2回で、入会後に受け持つ予定の先生が教えます。1回目は保護者面談にすることもできます。体験のあとは、先生とスタッフが作った指導計画を受け取れます。</p>",
         ("official/sogaku/taiken-yousu2_pc.png", 1000, 350, "体験授業の様子（オンライン授業の画面）", "https://sogaku.jp/online-lp/01/index_i.html")),
        ("担任制で毎回同じ先生。手元の様子も確認してもらえる",
         "<p>授業は完全マンツーマンの担任制で、毎回先生が代わることはありません。授業はZoomで、パソコンとは別にスマートフォンをスタンドなどに置いて手元を映すと、書けているか・ノートを取れているかを先生が随時確認できると公式に書かれています（おすすめの受講環境）。書くのが苦手な子も、手元を見ながら教えてもらえます。</p>",
         None),
        ("専門家が作ったアセスメントシートで、指導計画を作る",
         "<p>専門家が開発したアセスメントシートで、記憶力・集中力などのつまずきの原因を特性面と環境面から見て、一人ずつ指導計画をつくります。たとえば「1回の指示を1つにする」「漢字は部首などに分けて教える」「TODOリストや手順表を作る」といった支援です。授業でも、最初にその日の流れを説明して見通しを持たせてから始めます。体験のあとに、その子だけの指導計画を受け取れます。</p>",
         None),
        ("授業のたびに報告が届き、家での学習環境も相談できる",
         "<p>授業が終わるたびに、先生が専用アプリで指導報告を送ります。気になることは、先生や本部にチャットで相談できます。授業の様子はアセスメントシートに記録され、状況と対策を定期的に保護者に伝えます。保護者面談も定期的にあります。</p>"
         "<p>受講前や受講中には、気が散るものがないか、何をどのくらいやるかの見通し、勉強に入る前の切り替えなど、家での学習環境のアドバイスも受けられます。保護者向けの勉強会や相談窓口もあります。</p>",
         None),
        ("違約金・途中解約料は0円。卒業まで料金は上がらない",
         "<p>年会費・保証金・更新費・教師交代費・違約金・途中解約料はすべて0円で、契約期間の縛りもありません。月単位で休会・退会ができ、再開するときは入会金がかかりません。同じコースなら入会から卒業まで料金は上がらず（例：小学1年生で入会しても小学校卒業まで同じ）、受験生になっても、科目を増やしても変わりません。教材は発達障害の専門家が作った推奨教材リストから先生と相談して選び、買う必要はありません（映像授業2,000本・ドリル10,000問の学習ツールも追加費用なし）。6か月以上まとめて払うと月謝が5〜10%割引になる制度もあり、その場合も契約期間の縛りはありません。</p>",
         None),
    ],
    fit=["長い授業だと集中が続かないかもしれない", "学生ではなく、社会人の先生に見てほしい", "発達特性について学んだ先生に教えてほしい", "入会前に、実際に担当する先生と話してみたい", "診断はないが、グレーゾーンかもしれない", "親が勉強を見ると、ついケンカになってしまう"],
    check=["授業の振替は同じ月の中で、前日までの連絡が必要", "入会金22,000円（税込）が別にかかる（キャンペーンで無料になる場合あり）", "授業はオンラインのみ（パソコン・タブレット・スマホのいずれか）", "返金保証は公式の広告ページに記載。条件あり（下のよくある質問）", "退会の連絡は前月10日まで（メールか電話）", "手元を映すため、パソコンのほかにスマートフォン（とスタンド）があると指導しやすい（公式のおすすめ環境）"],
    steps=[("申し込む", "公式サイトのフォーム、公式LINE、電話（0120-907-377）から申し込みます。"),
           ("事前のヒアリング", "教務担当が、学習状況や希望の先生、日時を聞きます。"),
           ("無料体験を2回受ける", "ヒアリングをもとに選ばれた先生が担当。体験後に個別の指導計画とフィードバックを受け取ります。"),
           ("入会を決める", "相性が合えば、体験の先生がそのまま担当します。合わなければ入会しなくて大丈夫です。")],
    steps_src="https://sogaku.jp/online/trial-flow.html",
    form=("無料体験の申込フォームの入力項目", ["お子さんのお名前（必須）", "お子さんのお名前のフリガナ（必須）", "お子さんの学年（必須）", "電話番号（必須）", "メールアドレス（必須）", "体験希望コース：無料体験授業／無料説明会（必須）", "質問・相談・要望（任意）"],
          "https://sogaku.jp/online/trial.html", "公式の申込フォームの表示は「簡単3分」。"),
    shot_trial=("official/sogaku/trial-contents2.png", 1000, 764, "無料体験授業の内容（流れの説明・できる問題・チャレンジ問題・まとめ）", "https://sogaku.jp/online-lp/01/index_i.html"),
    fee=[("小学生", "25分　13,200円", "50分　22,000円"), ("中学生", "35分　18,480円", "60分　26,400円"), ("高校生", "35分　21,560円", "60分　29,920円")],
    fee_note="すべて月4回・税込。入会金22,000円（税込）は別途。保証金・更新費・教師交代費は0円で、月謝以外の会費もかかりません。科目数による料金アップ、受験生の割増なし。きょうだいの2人目以降は入会金免除、ひとり親家庭は入会金半額。6か月以上まとめて払うと月謝が5〜10%割引（契約期間の縛りなし）。",
    fee_src="https://sogaku.jp/online/fee.html",
    faq=[("診断がついていなくても受けられますか？", "はい。診断がなくても、グレーゾーンでも受講できます。診断名の申告や手帳・受給者証の提出も不要です。"),
         ("集中力が続かなくても大丈夫？", "集中が続きにくい子向けに、小学生は25分、中高生は35分の短いコースがあります。"),
         ("先生が合わなかったら？", "教師の交代は何度でも無料です。担当教師の性別の希望も伝えられます。"),
         ("体験後にしつこく勧誘されませんか？", "公式サイトのよくある質問で、無理な勧誘は一切ないと明記されています。"),
         ("保護者が家にいなくても受けられますか？", "受けられます。指導内容の報告は専用アプリで確認できます。ただし初回の授業は、できるだけ同席してほしいと公式に書かれています。"),
         ("ほかの塾や習い事と一緒に使えますか？", "併用できます。オンラインのプログラミング教室などと一緒に使っている子が多いと公式に書かれています。"),
         ("返金保証はありますか？", "公式の広告ページ（無料体験の案内ページ）に、授業料1か月分の全額返金保証が載っています。対象は小学生25分・50分、中高生35分・60分の月4回までのコースで、初めて利用する家庭（1世帯1回）、初回授業日から30日以内の連絡、最低1回の授業受講が条件です。入会金は対象外です。通常の公式サイトには載っていないため、申し込む前に条件を確認してください。")],
    faq_src="https://sogaku.jp/online/faq.html",
)
DETAIL["rebalance"] = dict(
    strengths=[
        ("LD・ADHD・ASD・グレーゾーン・ギフテッド専門",
         "<p>リバランスは、LD（学習障害）・ADHD・ASD・グレーゾーン・ギフテッド（2E）の子のためのオンライン個別指導塾です。学習内容のレベルを下げるのではなく、伝え方や答え方を工夫する「アコモデーション」を方針にしています。授業は完全1対1のライブ授業で、日本全国と海外から受けられます。</p>", None),
        ("約90分の無料体験で、個別指導計画書を受け取れる",
         "<p>無料体験は約90分のオンラインで、学習状況の聞き取り（約30分）、子どもとの模擬授業（約30分）、指導方針の提案（約30分）を行います。WISCなどの検査結果があれば解釈も含めて分析し、個別指導計画書（IEP）をメールで共有します。入会しなくても、体験を受けた希望者全員が受け取れると公式に書かれています。</p>", None),
        ("学生の先生も、プロと同じ研修を受けたセミプロ",
         "<p>先生はプロ講師（社会人か、特別支援教育士などの資格を持つ学生）が中心です。学生の先生も、プロ講師と同じ学科研修と技能研修を終えた「セミプロ講師」が担当します。担当制で、原則として同じ先生が教えます。</p>", None),
        ("授業のたびにフィードバック。教務にも相談できる",
         "<p>授業が終わると、保護者に当日の指導内容をフィードバックします（5分程度）。授業以外のことも教務に相談でき、無料の定期面談もあります。家庭学習で分からないときは、AIの質問チャットも使えます。</p>", None),
    ],
    fit=["LD・ADHD・ASDなど、特性に合わせた教え方をしてほしい", "診断はないが、グレーゾーンかもしれない", "中学受験・高校受験も考えている", "入会前に、指導計画の提案を受けてから決めたい"],
    check=["料金の表示は1回60分から（短い時間を希望する場合は体験時に相談）", "60分×月4回22,000円〜（税込）のほか、入会金19,800円と年間管理費26,400円がかかる", "対象学年は小学1年生〜中学3年生（外れていても相談できる場合あり）", "体験を担当する人が、入会後の先生かどうかは記載なし", "指導開始は申し込み手続きの翌月から"],
    steps=[("問い合わせ", "Webか電話（0120-609-216）で、体験学習・資料請求を申し込みます。"),
           ("無料のオンライン体験（約90分）", "学習状況の聞き取り・子どもとの模擬授業・指導方針の提案を行います。"),
           ("個別指導計画書の提案", "発達の特性や学習状況を分析した個別指導計画書（IEP）が、体験後にメールで届きます。"),
           ("申し込み・指導開始", "料金プランを相談して決め、申し込み手続きの翌月から授業が始まります。")],
    steps_src="https://reba1ance.com/system/",
    faq=[("診断を受けていなくても指導してもらえますか？", "はい。確定診断を受けていないグレーゾーンの子のほうが多く、検査を受けていなくても指導できると公式に書かれています。"),
         ("知的障害がある場合は対象になりますか？", "学習塾のため、知的障害のある子は対象外と公式に書かれています。"),
         ("休んだ授業の振替はできますか？", "前日までの連絡で振替できます。できるだけ同じ月に振り替え、難しい場合は翌月以降に繰り越せます。"),
         ("教材は何を使いますか？", "指定の教材は原則使わず、学校のテキストを中心に使います。必要なら市販のテキストをすすめる方針です。")],
    faq_src="https://reba1ance.com/faq/",
)
DETAIL["try"] = dict(
    strengths=[
        ("教師とは別に、教育プランナーが専任でつく",
         "<p>トライでは、教師とは別に正社員の「教育プランナー」が家庭ごとにつきます。保護者との面談で悩みや学習状況を聞き、得意・苦手や理解のスピードに合わせたカリキュラムを作ります。先生に直接言いづらい配慮の相談もできます。</p>", None),
        ("WISC検査の結果をもとに学習をサポート",
         "<p>WISC検査の結果をもとに、得意な分野を伸ばし、苦手な部分を無理なくカバーできるよう学習を組み立てます。</p>", None),
        ("カメラオフや保護者同席でも受けられる",
         "<p>子どもが落ち着く場所で受講でき、保護者が同席して見守ることもできます。カメラはオンが推奨ですが、難しければオフでも受講できます。話すのが難しい子は、Zoomのチャットでやりとりすることもできます。</p>", None),
        ("アプリで毎回の授業の進捗が見える",
         "<p>無料の学習管理アプリで、毎回の授業の進捗や教師のコメントを確認できます。教材費は無料で、中高生向けの映像授業「Try IT」も見放題です。</p>", None),
    ],
    fit=["WISCなどの検査結果を勉強に活かしたい", "先生とは別に、相談できる担当者がほしい", "カメラオフや保護者同席から始めたい", "受験や英検の対策も考えている"],
    check=["入会金11,000円（税込）が別にかかる", "料金例は1コマ60分（短い授業は学習面談で要確認）", "体験授業は英語か数学（時間は約30分・約60分とページにより記載が異なる）"],
    steps=[("学習面談の案内", "電話で、無料の学習面談（Zoom）が案内されます。"),
           ("無料の学習面談", "教育プランナーが悩みや目標を聞き、コースや学習法、料金を提案します。入会しなくても受けられます。"),
           ("先生の決定", "登録教師33万人（2024年3月時点・公式）から担当が選ばれ、授業の前に先生からあいさつがあります。"),
           ("授業スタート", "アプリで自動発行されるZoomのURLから授業に入ります。")],
    steps_src="https://www.try-online.jp/kobetsu/tokusei/",
    faq=[("発達障害・学習障害があっても入会できますか？", "はい。マンツーマンなので、子どもが理解できるペースで授業を行うと公式に書かれています。不安な場合は入会前の無料体験授業がすすめられています。"),
         ("学習面談は保護者だけでも受けられますか？", "通常は親子での参加ですが、難しい場合は保護者だけでも面談できます。"),
         ("授業の振替はできますか？", "前日22時までの連絡で振替できます。")],
    faq_src="https://www.try-online.jp/kobetsu/tokusei/",
)
DETAIL["coaching1"] = dict(
    strengths=[
        ("提携する臨床心理士の発達検査を受けられる",
         "<p>コーチング1グループでは、提携している臨床心理士による発達検査（知能検査）を受けられます。診断ではなく得意・不得意をつかむことが目的で、検査結果は学習指導やSSTに反映されます。</p>", None),
        ("発達特性のある子の中学受験・高校受験に対応",
         "<p>コーチング1は、発達障害・グレーゾーンの子のための学習進学塾です。WISCなどの検査結果から特性を分析し、その子に合った勉強のやり方を見つけて、中学受験・高校受験まで伴走します。</p>", None),
        ("オンライン指導は全国から。完全1対1",
         "<p>教室（首都圏・関西圏）のほかにオンライン指導があり、全国・海外から受けられます。指導はすべて完全マンツーマンです。</p>", None),
        ("毎回の指導報告書と、教務部への相談",
         "<p>授業の終わりには指導報告書でその日の内容を伝えます。授業以外のことも教務部に相談でき、教務は担当講師と毎月の報告書などで指導状況を確認しています。</p>", None),
    ],
    fit=["発達特性があっても受験を目指したい", "発達検査で得意・不得意を知りたい", "授業の内容を毎回報告してほしい", "60分以上の授業でも取り組める"],
    check=["オンラインは1回60分から。60分×月4回で25,300円（税込）", "入会金18,700円と年会費26,400円が別にかかる", "契約期間は1年で自動更新（変更は前月末までに連絡）", "オンライン指導は翌月以降への振替ができない", "チーム制のため、講師が入れ替わることがある"],
    steps=[("資料請求・問い合わせ", "Webか電話で問い合わせます。"),
           ("無料の体験学習・カウンセリング（約120分）", "担当教務との面談（体験授業と相談を含む）で特性や学習状況を分析し、学習指導案が提案されます。オンラインでも受けられます（完全予約制）。"),
           ("申し込み", "指導プランと料金プランを相談して決めます。"),
           ("指導開始", "オンライン指導は申し込み月の翌月から始まります。")],
    steps_src="https://www.juku-coaching01.com/starting/",
    faq=[("診断や発達検査を受けていなくても指導してもらえますか？", "はい。確定診断や発達検査がなくても、発達障害の疑いや傾向があれば指導すると公式に書かれています。"),
         ("先生はいつも同じですか？", "チーム制のため、講師が入れ替わることがあります。入れ替わる場合は引き継ぎを行います。"),
         ("休んだ授業の振替はできますか？", "できるだけ同じ月に振り替えます。ただし、オンライン指導は翌月以降への振替ができません。")],
    faq_src="https://www.juku-coaching01.com/others/faq/",
)
DETAIL["kizuki"] = dict(
    strengths=[
        ("不登校・発達障害の子の学び直しを、完全1対1で",
         "<p>キズキ共育塾は、不登校・発達障害・グレーゾーンの子や、中退・社会人の学び直しと受験を支える完全1対1の個別指導塾です。小学校の内容から大学受験まで対応しています。</p>", None),
        ("オンライン校は全国から。顔を出さなくても受けられる",
         "<p>オンライン校はGoogle Meetで授業を行い、全国・海外から受けられます。顔を見せるのが苦手な子は、音声とチャットだけで授業を受けることもできます。</p>", None),
        ("授業とは別のメンターサポート",
         "<p>学習計画を一緒に立てる「じぶんマナビメンター」、特性を知って行動の目標を決める「じぶんモチベメンター」（いずれも月2回30分）、保護者向けの「おやサポメンター」（月1回30分）から選べます。メンターなしのプランもあります。</p>", None),
        ("講師・科目の変更は無料。出席扱いの相談もできる",
         "<p>担当講師や科目の変更、通塾とオンラインの切り替えは無料です。在籍校の判断によっては、キズキでの学習を小中学校の出席日数として数えられる場合があります。</p>", None),
    ],
    fit=["学校に行きづらい状態から、少しずつ勉強を再開したい", "顔を出さずに授業を受けたい", "勉強とあわせて、学習計画や気持ちの面も相談したい", "保護者だけで先に相談したい"],
    check=["常設の無料体験授業はない（期間限定で行う場合あり）", "小学生の料金は公式に記載がない（50分×月4回24,200円〜の記載、中学3年生の例は30,800円〜）", "入会時に入会金16,500円・事務手数料5,500円・選抜費11,000円〜がかかる", "教材は家庭で用意する（市販の参考書など）", "休会・退会は前々月末までに申請（規約）。休会中は月3,300円"],
    steps=[("問い合わせ", "電話（0120-501-858）、問い合わせフォーム、LINEから連絡します。"),
           ("面談・入会", "教室か電話・オンラインで面談し、システムや方針の説明を受けます。保護者だけの相談もできます。"),
           ("講師と学習方針の決定", "目標に沿った学習方針を決め、担当の講師を選びます。"),
           ("授業開始", "入会手続きから1〜2週間ほどで授業が始まります。")],
    steps_src="https://kizuki.or.jp/courses/",
    faq=[("体験授業はできますか？", "常設のサービスとしては行っておらず、期間限定で行うことがあると公式に書かれています。"),
         ("キズキでの学習を、学校の出席として数えてもらえますか？", "在籍している学校の判断によって数えられる場合があり、実例も多いと公式に書かれています。"),
         ("休会はできますか？", "1か月単位で休めます。規約では申請期限は前々月末までで、休会月は休会費3,300円（税込）がかかります。")],
    faq_src="https://kizuki.or.jp/questions/",
)
DETAIL["tos"] = dict(
    strengths=[
        ("無料体験は、実際に担当する家庭教師が行う",
         "<p>TOSの無料体験は、その回だけの先生ではなく、これから実際に教える家庭教師が担当します。面談を含めて40分〜1時間ほどで、体験の前に入会金はかかりません。合わなければ先生の交代も無料です。体験の説明は家庭教師の訪問を前提にしているため、オンラインコースでも同じ形かは申し込み時に確認してください。</p>", None),
        ("WISCなどの発達検査を自宅で受けられる",
         "<p>専門スタッフによるWISC-Ⅳ・田中ビネー・K-ABCなどの発達検査を自宅で受けられます（有料。会員は検査とカウンセリングで38,500円・税込）。</p>", None),
        ("臨床心理士などのカウンセリング",
         "<p>不登校・発達障害などの悩みに、家庭教師経験のあるカウンセラーや臨床心理士がカウンセリングを行います（有料。1時間5,500円・税込〜）。現在は基本的にオンラインで、保護者だけの相談もできます。</p>", None),
        ("月謝制で、解約金・違約金なし",
         "<p>契約は1か月単位の月謝制で、解約金・違約金はありません。退会の連絡は1か月以上前に必要で、最低1か月・6時間以上の受講が条件です。テキスト代・手数料・管理費などの追加費用もありません。</p>", None),
    ],
    fit=["入会前に、実際に担当する先生と会って決めたい", "発達検査やカウンセリングも同じところで受けたい", "不登校からの受験・高認も考えている", "教材の販売やローン契約がないところがいい"],
    check=["オンラインの授業は1回60分から", "入会金33,000円（税込）がかかる", "体験の説明は訪問が前提。オンラインでも担当の先生と体験できるかは要確認", "オンラインコースの詳しい説明ページは確認時点で表示されなかった（対象地域は記載なし）", "発達検査・カウンセリングは別料金"],
    steps=[("問い合わせ・申し込み", "電話（0120-12-6446）かWebのフォームから申し込みます。"),
           ("家庭教師の選定", "希望の条件をもとに家庭教師を選び、日程を打ち合わせます（平均3〜4日前後）。"),
           ("無料体験", "体験授業20〜30分と、保護者を含めたヒアリング20〜30分を行います。"),
           ("入会手続き・指導開始", "体験した先生に決めたら入会の手続きをして、指導が始まります。")],
    steps_src="https://tos-kc1.com/join/",
    faq=[("解約・退会に費用はかかりますか？", "かかりません。違約金などもないと公式に書かれています。"),
         ("発達障害かもしれないと言われました。検査は受けられますか？", "専門スタッフによる発達検査（WISC・田中ビネー）を自宅で受けられます。"),
         ("1か月だけの短期でも頼めますか？", "できます。ただし最低6時間以上の受講が必要です。")],
    faq_src="https://tos-kc1.com/join/qa/",
)


def shot(img, cls="yk-shot"):
    f, w, h, alt, src = img
    return (f'<figure class="{cls}"><img class="yk-shot__img rk-shotimg" src="{IMG}{f}" alt="{esc(alt)}" width="{w}" height="{h}" loading="lazy">'
            f'<figcaption>出典：<a href="{src}" target="_blank" rel="nofollow noopener">{"ソウガク公式サイト"}</a></figcaption></figure>')


def order_box(ttl, label, items, prefix):
    lis = "".join(f'<li><span>{label}{i}</span><a href="#{prefix}{i}">{esc(t)}</a></li>' for i, t in enumerate(items, 1))
    return f'<div class="yk-order"><p class="yk-order__ttl">{esc(ttl)}</p><ol>{lis}</ol></div>'


def detail(k):
    s, d = S[k], DETAIL[k]
    o = head(f"{s['name']}の特徴・料金・無料体験｜発達特性のある子のオンライン家庭教師", f"{s['full']}の特徴、料金、無料体験の流れ、口コミ、よくある質問を公式サイトの情報からまとめました（{CHECKED}確認）。")
    o += f'\n<!-- F-1 パンくず（yk-crumb） -->\n<nav class="yk-crumb"><a href="./">TOP</a><span>{esc(s["name"])}</span></nav>\n'
    o += f"""
<!-- F-2 サービス概要（yk-svchead）：右は公式バナー（ASP素材がない会社は公式ロゴ） -->
<p class="yk-svchead__name">{esc(s["name"])}</p><p class="yk-svchead__catch">{s["catch"].replace("<br>", " ")}</p>
<div class="yk-svchead__grid">{features(s)}{banner(s, "yk-svchead__img", "detail_banner")}</div>
{info_table(s)}
{btn_main(s, "detail_top")}
<p class="rk-rankline">当サイトのランキング：<b>{s["rank"]}位</b>（総合評価 {s["total"]}／5）<a href="./#rank-{s['id']}">ランキングを見る</a></p>
"""
    # 強み
    names = [t for t, _, _ in d["strengths"]]
    o += f'\n<!-- F-4 番号つき目次（yk-order）→ F-5 番号ラベルつき見出し（yk-numh）→ F-3 公式画面（yk-shot） -->\n<h2 class="yk-sec-ttl" data-section-id="strength">{esc(s["short"])}の<em>強み</em></h2>\n{order_box(s["short"] + "の強み", "強み", names, "s")}\n'
    for i, (t, body, img) in enumerate(d["strengths"], 1):
        o += f'<h3 class="yk-numh" id="s{i}"><span>強み{i}</span>{esc(t)}</h3>\n{body}\n'
        if img:
            o += shot(img) + "\n"
    o += f'<p class="yk-small">※出典：<a href="{s["official"]}" target="_blank" rel="nofollow noopener">{esc(s["short"])}公式サイト</a>ほか。</p>\n{btn_main(s, "detail_strength")}\n'
    # こんな方に
    fit = "".join(f"<li>{esc(t)}</li>" for t in d["fit"])
    chk = "".join(f"<li>{esc(t)}</li>" for t in d["check"])
    o += f"""
<!-- F-6 チェックの箱（yk-listbox）：公式の対象・強みから書く。感想で作らない -->
<h2 class="yk-sec-ttl" data-section-id="fit">{esc(s["short"])}が<em>向いている家庭</em></h2>
<div class="yk-listbox"><p class="yk-listbox__ttl">こんな家庭に向いています</p><ul>{fit}</ul></div>
<div class="yk-listbox"><p class="yk-listbox__ttl">申し込む前に確認したいこと</p><ul>{chk}</ul></div>
{btn_main(s, "detail_fit")}
"""
    # 料金
    if "fee" in d:
        rows = "".join(f"<tr><th>{g}</th><td>{a}</td><td>{b}</td></tr>" for g, a, b in d["fee"])
        o += f"""
<h2 class="yk-sec-ttl" data-section-id="fee">{esc(s["short"])}の<em>料金</em></h2>
<table class="rk-fee"><tr><th>学年</th><th>短いコース</th><th>長いコース</th></tr>{rows}</table>
<p class="yk-small">※{d["fee_note"]} 出典：<a href="{d["fee_src"]}" target="_blank" rel="nofollow noopener">公式サイト</a></p>
"""
    else:
        o += f'\n<h2 class="yk-sec-ttl" data-section-id="fee">{esc(s["short"])}の<em>料金</em></h2>\n{jobex(s)}\n'
    o += btn_main(s, "detail_fee") + "\n"
    # 手順
    steps = [t for t, _ in d["steps"]]
    o += f'\n<h2 class="yk-sec-ttl" data-section-id="flow">無料体験・<em>申し込みの流れ</em></h2>\n{order_box("申し込みの流れ", "ステップ", steps, "f")}\n'
    for i, (t, body) in enumerate(d["steps"], 1):
        o += f'<h3 class="yk-numh" id="f{i}"><span>ステップ{i}</span>{esc(t)}</h3>\n<p>{esc(body)}</p>\n'
        if k == "sogaku" and i == 3:
            o += shot(d["shot_trial"]) + "\n"
    if "form" in d:
        ttl, items, src, _ = d["form"]
        lis = "".join(f"<li>{esc(t)}</li>" for t in items)
        o += f'<div class="yk-listbox"><p class="yk-listbox__ttl">{esc(ttl)}</p><ul>{lis}</ul></div>\n<p class="yk-small">※出典：<a href="{src}" target="_blank" rel="nofollow noopener">公式サイトの申込フォーム</a>（広告のリンク先では項目が異なる場合あり）。</p>\n'
    o += f'<p class="yk-small">※流れの出典：<a href="{d["steps_src"]}" target="_blank" rel="nofollow noopener">{esc(s["short"])}公式サイト</a>。</p>\n{btn_main(s, "detail_flow")}\n'
    # 口コミ
    if s["voices"]:
        o += f'\n<h2 class="yk-sec-ttl" data-section-id="voice">{esc(s["short"])}の<em>口コミ・評判</em></h2>\n{voices(s)}\n{btn_main(s, "detail_voice")}\n'
    # FAQ
    qs = [q for q, _ in d["faq"]]
    o += f'\n<h2 class="yk-sec-ttl" data-section-id="faq">よくある<em>質問</em></h2>\n{order_box("よくある質問", "質問", qs, "q")}\n'
    for i, (q, a) in enumerate(d["faq"], 1):
        o += f'<h3 class="yk-numh" id="q{i}"><span>質問{i}</span>{esc(q)}</h3>\n<p>{esc(a)}</p>\n'
    o += f'<p class="yk-small">※出典：<a href="{d["faq_src"]}" target="_blank" rel="nofollow noopener">{esc(s["short"])}公式サイト</a>。このページは{CHECKED}時点の公式サイトの情報です。</p>\n{btn_main(s, "detail_faq")}\n'
    if s["operator"]:
        o += f'<p class="yk-small">運営会社：{esc(s["operator"])}（公式サイトの表記）。当サイトは{esc(s["short"])}と広告契約をしていません。</p>\n'
    o += '<p class="rk-back"><a href="./#ranking">ランキングに戻る</a></p>\n'
    return o + end()


# ---------------------------------------------------------------- 調査概要
def method():
    R = [S[k] for k in RANK]
    crit = [
        ("support", "発達特性への対応", ["5：サービス全体が発達障害・グレーゾーン専門で、外部の専門家・専門機関が関わる仕組み（先生の研修、指導計画のシートなど）を公表", "4：発達特性・不登校向けのコースや支援があり、特性を聞き取る専任・有資格のスタッフの関与を公表", "3：発達特性のある子も受講できると記載"]),
        ("teacher", "先生の体制", ["5：担当する先生全員が、発達特性についての専門研修を受けていると公表", "4：特性を聞いて指導前に先生へ研修を行う、または発達特性を扱う講師研修があることを公表", "3：講師研修や、不登校・特性の指導経験がある先生の在籍を公表"]),
        ("trial", "入会前に確かめられること", ["5：入会後に担当する予定の先生による無料体験を、公式に明記", "4：子どもが受けられる無料の体験授業・体験レッスンがある（担当は先生以外のスタッフ）", "3：保護者との無料相談が中心で、子どもの体験は希望制・内容が限られる"]),
        ("time", "短い時間から始められるか", ["5：1回30分未満の授業を選べる", "4：1回30分〜59分から（30分単位を含む）", "3：1回60分から", "2：1回90分から"]),
        ("parent", "保護者サポート", ["5：毎回の授業報告と、授業以外の相談（チャット・LINE・面談・教務への相談）の両方を公表", "4：相談窓口（LINE・面談など）や定期的な報告・本部からの確認を公表", "3：相談窓口の記載のみ"]),
        ("price", "料金", ["小学生の月額の、公式の最安表示（入会金は含めない）", "5：11,000円未満／4：11,000〜14,999円／3：15,000〜19,999円／2：20,000〜29,999円／1：30,000円以上"]),
        ("contract", "費用と契約の分かりやすさ", ["5：入会金・教材費・解約の条件（違約金・最低期間）・休会を、公式の本体ページに明記", "4：一部を本体ページに明記", "3：本体ページに記載がなく、広告用LPやコラムでのみ説明", "2：公式サイトに記載なし"]),
    ]
    rows = "".join(f'<tr><th>{t}</th><td class="is-left">' + "<br>".join(esc(x) for x in c) + "</td></tr>" for _, t, c in crit)
    head_cells = "".join(f"<th>{a[1]}</th>" for a in AXES)
    score_rows = "".join(f'<tr><td>{s["rank"]}位 {esc(s["short"])}</td>' + "".join(f'<td>{s["scores"][a[0]]}</td>' for a in AXES) + f'<td><b>{s["total"]}</b></td></tr>' for s in R)
    src = "".join(f'<li>{esc(s["name"])}：<a href="{s["official"]}" target="_blank" rel="nofollow noopener">{esc(s["official"])}</a>、<a href="{s["plan_src"]}" target="_blank" rel="nofollow noopener">料金</a>、<a href="{DETAIL[s["id"]]["steps_src"]}" target="_blank" rel="nofollow noopener">申し込みの流れ</a></li>' for s in R)
    why = ""
    for s in R:
        trs = "".join(f'<tr><th>{a[2]}</th><td><b>{s["scores"][a[0]]}</b></td><td class="is-left">{esc(WHY[s["id"]][a[0]])}</td></tr>' for a in AXES)
        why += f'<h3 class="rk-h3">{s["rank"]}位 {esc(s["name"])}（総合評価 {s["total"]}）</h3>\n<table class="yk-cmp rk-why"><colgroup><col class="c1"><col class="rk-c-score"><col></colgroup>{trs}</table>\n'
    o = head("ランキング調査概要｜オンライン家庭教師6社の比較", "オンライン家庭教師6社の順位・総合評価・星・比較表の記号の決め方と、確認した公式情報の一覧です。")
    o += f"""
<nav class="yk-crumb"><a href="./">TOP</a><span>ランキング調査概要</span></nav>
<h1 class="rk-h1">ランキング調査概要</h1>
<h2 class="yk-sec-ttl">調べたもの</h2>
<ul class="rk-list"><li>対象：発達障害・グレーゾーン・不登校の子に対応すると公式サイトに書かれ、オンラインで受講できる家庭教師・個別指導 6社（上位3社をトップページでTOP3として紹介）</li>
<li>選び方：「発達障害・グレーゾーン専門」または発達特性・不登校向けのコースをうたい、オンラインで1対1の授業を受けられ、料金と入会前の体験・相談の内容を公式サイトで確かめられる会社から選びました（2026年10月17日に選び直し）</li>
<li>料金の比べ方：小学生・月4回の、公式の最安表示（税込・入会金は含めない）。小学生の金額が書かれていない会社は、その旨を「要確認」として書いています</li>
<li>方法：各社の公式サイトを{CHECKED}に確認（料金・授業時間・先生・研修・体験・保護者サポート・費用と契約・よくある質問）。口コミサイトや利用者アンケートの点数は使っていません</li>
<li>広告：ソウガクのみアフィリエイト広告の契約があります。順位は契約の有無ではなく、下の基準で決めています</li></ul>
<h2 class="yk-sec-ttl">採点の基準（各5点満点）</h2>
<table class="yk-cmp rk-cmp-text rk-crit">{rows}</table>
<h2 class="yk-sec-ttl">総合評価・星・記号の決め方</h2>
<ul class="rk-list"><li>総合評価：{len(AXES)}項目の点数の平均（小数第2位を四捨五入）</li>
<li>星：総合評価を四捨五入した数（例：4.9→★5、4.0→★4、3.7→★4）</li>
<li>総合評価のランク：S＝4.5以上、A＝4.0以上、B＝4.0未満</li>
<li>同点のとき：「発達特性への対応」→「先生の体制」→小学生の月額の目安が安い順</li>
<li>「総合」タブの無料体験の記号：採点「入会前に確かめられること」が5点＝◎（入会後に担当する先生と試せる）、4点＝○（子どもが体験授業を受けられる）、3点・2点＝△（相談・見学だけ）、1点＝×</li><li>そのほかの比較項目の記号は、各社公式サイトの記載をもとにした当サイトの判断：◎＝特に手厚い、○＝ある、△＝限られる、－＝公式に記載なし</li></ul>
<h2 class="yk-sec-ttl">採点の結果</h2>
<div class="rk-scroll"><table class="yk-cmp"><tr><th>サービス</th>{head_cells}<th>総合</th></tr>{score_rows}</table></div>
<h2 class="yk-sec-ttl">採点の根拠</h2>
{why}
<h2 class="yk-sec-ttl">確認した公式ページ</h2>
<ul class="rk-list">{src}</ul>
<p class="yk-small">※料金・内容は変わることがあります。申し込む前に各社の公式サイトで最新の情報を確認してください。</p>
<p class="rk-back"><a href="./">TOPに戻る</a></p>
"""
    return o + end()


def main():
    os.makedirs(OUT, exist_ok=True)
    pages = {"index.html": top(), "method.html": method()}
    for k in S:
        pages[f"{k}.html"] = detail(k)
    for name, text in pages.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(text)
    for k in RANK:
        print(S[k]["rank"], S[k]["short"], S[k]["total"], list(S[k]["scores"].values()))
    print("wrote", ", ".join(pages))


if __name__ == "__main__":
    main()

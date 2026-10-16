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
CHECKED = "2026年10月16日"
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
    best3=("発達障害・グレーゾーン専門", "担当予定の先生と無料体験2回", "専門機関の研修を受けた社会人講師が、小学生なら25分から教えます。"),
    target="小学生〜高校生", btn_catch="診断なし・グレーゾーンでも相談OK", btn="無料体験を公式で見る",
    catch="発達特性を学んだ社会人講師が25分から教える！<br>担当予定の先生と無料体験2回",
    cmp_text="サービス全体が発達障害・グレーゾーン専門。先生は全員、専門機関の研修を受けた社会人。担当予定の先生と2回の無料体験で相性を確かめられる。",
    chips=[("is-pink", "25分から"), ("", "毎回の報告"), ("", "体験2回"), ("", "違約金0円")],
    features=[
        ('先生は全員<span class="yk-mark">専門機関の研修を受けた社会人講師</span>', "https://sogaku.jp/online/tutor.html"),
        ("専門家が開発したアセスメントシートで、一人ずつ指導計画をつくる", "https://sogaku.jp/online/reason.html"),
        ('授業は<span class="yk-red">小学生25分</span>から（中高生は35分から）', "https://sogaku.jp/online/fee.html"),
        ("無料体験は2回。入会後に担当する予定の先生が担当", "https://sogaku.jp/online/faq.html"),
        ("授業のたびにアプリで指導報告。先生・本部にチャットで相談", "https://sogaku.jp/online/course.html"),
        ("違約金・途中解約料0円。契約期間の縛りなし", "https://sogaku.jp/online/reason.html"),
    ],
    editor=('ソウガクは、サービス全体が発達障害・グレーゾーン専門です。先生は全員が社会人で、発達支援の専門機関「発達凸凹アソシエーション」の研修を受けています。臨床心理士や作業療法士、放課後等デイサービスで働いた経験のある先生も在籍しています。'
            '<span class="yk-mark">入会後に担当する予定の先生と、2回の無料体験で試してから決められる</span>と公式に明記しているのは、3社の中でソウガクだけでした※1。'
            '授業は小学生なら<span class="yk-red">25分</span>から選べて、違約金や途中解約料もかかりません。「長い授業は続かないかも」「先生との相性が心配」という家庭が、最初に試しやすいサービスです。',
            "※1 各社公式サイトの無料体験の説明による（" + CHECKED + "確認）"),
    info=[("料金の目安", "月13,200円〜<small>小学生25分×月4回・税込。別途入会金22,000円（キャンペーンで無料の場合あり）</small>"),
          ("対応学年", "小学生〜高校生<small>全国・オンライン（Zoom）</small>"),
          ("1回の授業", "小学生25分・50分・75分<br>中高生35分・60分・75分"),
          ("先生", "全員が専門機関の研修を受けた社会人講師"),
          ("保護者サポート", "毎回の指導報告・先生/本部とチャット・定期的な保護者面談・保護者向け勉強会"),
          ("無料体験", "2回。担当予定の先生が担当（1回目は保護者面談にもできる）")],
    plans=[("小学生", "25分×月4回", "13,200円", "50分×月4回は22,000円"),
           ("中学生", "35分×月4回", "18,480円", "60分×月4回は26,400円"),
           ("高校生", "35分×月4回", "21,560円", "60分×月4回は29,920円")],
    plan_src="https://sogaku.jp/online/fee.html", plan_note="すべて税込。入会金22,000円（税込）は別途。学年が上がっても、受験生になっても、科目を増やしても料金は変わりません",
    voices=[("中学2年生・特別支援学級の保護者",
             "勉強に苦手意識があり、初回の体験では画面の前に座っているのも難しかった。先生が急がずに時間をかけて関係をつくり、今は授業の時間を楽しみにしている。"),
            ("小学4年生・ADHDの診断ありの保護者",
             "学校へ行ける日が減り、家で勉強を見ると親子で言い合いになっていた。週1回オンラインで学ぶ習慣ができ、「ずっと自分が見なければ」という負担が軽くなった。"),
            ("中学2年生の保護者（岡山県）",
             "子どものタイプに合わせた学び方を相談できる先生に初めて出会えた。他社と違って、体験を何回か受けられたのも助かった。")],
    voice_src="https://sogaku.jp/online/voice.html",
    operator=None,
)
S["runner"] = dict(
    name="家庭教師のランナー", short="ランナー", full="家庭教師のランナー（発達障害サポート・オンライン指導）",
    logo=("logos/runner-logo.svg", 406, 141), url="https://k-runner.co.jp/course/developmental-disabilities/", sponsored=False,
    official="https://k-runner.co.jp/course/developmental-disabilities/",
    scores=dict(support=4, teacher=4, trial=4, time=4, parent=4, price=5, contract=3),
    price_month=9000, min_minutes=30,
    best3=("勉強が苦手な子専門", "1コマ30分900円から", "発達障害サポートあり。オンラインと訪問を切り替えられます。"),
    target="未就学児〜高校生", btn_catch="他社との比較も歓迎と公式に明記", btn="無料体験レッスンを公式で見る",
    catch="勉強が苦手な子専門。発達障害サポートあり<br>先生は約14万人の登録から本部が選ぶ",
    cmp_text="発達障害コミュニケーション指導者のスタッフが先生を支える。料金は指導した分だけ。",
    chips=[("is-pink", "30分単位"), ("", "LINE相談"), ("is-gray", "訪問にも切替")],
    features=[
        ('<span class="yk-mark">「発達障害コミュニケーション指導者」</span>のスタッフが担当の先生を指導', "https://k-runner.co.jp/course/developmental-disabilities/"),
        ("体験で作ったカルテから先生候補を10〜20名選び、面談して決める", "https://k-runner.co.jp/course/online/"),
        ('1コマ30分<span class="yk-red">900円</span>（小中学生）。指導した分だけの支払い', "https://k-runner.co.jp/course/developmental-disabilities/"),
        ("分からない問題はLINEで写真を送ると、解説動画で返ってくる", "https://k-runner.co.jp/course/online/"),
    ],
    editor=('ランナーは「勉強が苦手な子専門」の家庭教師で、その中に発達障害サポートがあります。決まったカリキュラムを置かず、特性に合わせて教え方を変える方針です。'
            '料金は<span class="yk-red">1コマ30分900円</span>（小中学生）からで、指導した分だけの支払い。'
            '<span class="yk-mark">約14万人の登録から本部が先生を選び、合わなければ何度でも無料で交代できる</span>ので、先生選びを丁寧にしたい家庭に向いています。', ""),
    info=[("料金の目安", "小学生 月9,000円〜<small>教科数・時間・回数で変わる。地域差あり</small>"),
          ("対応学年", "未就学児〜高校生<small>オンラインは全国・海外から</small>"),
          ("1回の授業", "30分単位で組める<small>1コマ30分900円〜（高校生1,000円〜）</small>"),
          ("先生", "大学生〜社会人の登録者から本部が選考し、指導前に研修<small>先生紹介のページは大学生・大学院生が中心</small>"),
          ("保護者サポート", "公式LINEで相談・本部から定期的に状況確認"),
          ("無料体験", "90分の体験レッスン（学習アドバイザーが担当。先生は入会後に選考）")],
    plans=[("小学生", "教科数・時間・回数は自由", "9,000円〜", "1コマ30分900円"),
           ("中学生", "教科数・時間・回数は自由", "13,000円〜", "1コマ30分900円"),
           ("高校生", "教科数・時間・回数は自由", "15,400円〜", "1コマ30分1,000円")],
    plan_src="https://k-runner.co.jp/course/online/", plan_note="地域によって料金が異なる場合あり（公式）。税込・税抜の表記、入会金、解約の決まりは公式の本体ページに記載なし",
    voices=[("会員の保護者（公式サイト掲載）",
             "息子は対面が苦手で、オンラインを強く希望した。始めてみると対面と変わらず、分からないところは何度も教えてもらえた。"),
            ("会員の保護者（公式サイト掲載）",
             "先生が、親からの勉強の相談にも丁寧にのってくれた。")],
    voice_src="https://k-runner.co.jp/course/online/",
    operator="マインズ株式会社",
)
S["tintle"] = dict(
    name="ティントル", short="ティントル", full="不登校専門オンライン個別指導ティントル",
    logo=("logos/tintle-logo.png", 498, 108), url="https://tintle.net/", sponsored=False,
    official="https://tintle.net/",
    scores=dict(support=4, teacher=4, trial=3, time=4, parent=4, price=5, contract=2),
    price_month=10560, min_minutes=30,
    best3=("不登校専門のオンライン個別指導", "30分単位・受けた分だけ後払い", "発達障がい・支援級・行き渋りの子も対象です。"),
    target="小学生〜高校生", btn_catch="まずは個別相談会から", btn="個別相談会を公式で見る",
    catch="学校に行きづらい子の専門オンライン個別指導<br>30分単位、受けた分だけの後払い",
    cmp_text="不登校専門。授業の曜日・時間・回数を固定せず、受けた分だけ後払い。出席扱いの申請にも対応。",
    chips=[("is-pink", "30分単位"), ("", "後払い"), ("", "出席扱い申請")],
    features=[
        ('<span class="yk-mark">不登校専門</span>。発達障がい・支援級・行き渋りの子も対象', "https://tintle.net/"),
        ('1コマ<span class="yk-red">30分</span>、受けた分だけの後払い。曜日・回数は自由', "https://tintle.net/pricetable/"),
        ("講師とは別に、不登校心理相談士の資格を持つスタッフが家庭を支える", "https://tintle.net/"),
        ("自宅学習を学校の出席扱いとして申請できるコースあり", "https://tintle.net/"),
    ],
    editor=('ティントルは不登校専門のオンライン個別指導で、発達障がいや支援級、行き渋りの子も対象にしています。'
            '授業は<span class="yk-red">1コマ30分</span>単位で、曜日・時間・回数を固定しません。'
            '<span class="yk-mark">「慣れるまでは少なめに、しんどい日は休む」という使い方ができる</span>ので、学校に行きづらい日が続いている家庭に向いています。先生は現役の大学生です。', ""),
    info=[("料金の目安", "小学生 週1回1時間 月10,560円〜<small>4週換算・税込（Cランクの講師）</small>"),
          ("対応学年", "小学生〜高校生<small>全国・オンライン</small>"),
          ("1回の授業", "1コマ30分<small>曜日・時間・回数は自由</small>"),
          ("先生", "現役の大学生（講師研修・不登校対応の研修あり）"),
          ("保護者サポート", "不登校心理相談士がオンライン面談・LINE・電話で相談"),
          ("無料体験", "個別相談会（約1時間・サポートスタッフが担当）。子どもの体験は希望制")],
    plans=[("小学生", "週1回1時間（4週換算）", "10,560円〜", "1コマ30分1,320円〜"),
           ("中学生", "週1回1時間（4週換算）", "14,960円〜", "1コマ30分1,870円〜"),
           ("高校生", "週1回1時間（4週換算）", "23,760円〜", "1コマ30分2,970円〜")],
    plan_src="https://tintle.net/pricetable/", plan_note="すべて税込。講師のランク（S〜C）で1コマの料金が変わり、高校生はS・Aランクのみ。入会金・解約の決まりは公式サイトに記載なし",
    voices=[("中学2年生の保護者（公式サイト掲載）",
             "先生のおかげで、勉強への意欲が少しずつ出てきた。宿題を出してもらえるのも親としてありがたい。"),
            ("個別相談会に参加した保護者（公式サイト掲載）",
             "子どもの困りごとを理解して無理のない提案をしてもらえたが、本人のやる気がいまひとつで、入会はいったん見送った。")],
    voice_src="https://tintle.net/flow/",
    operator="LIVE株式会社",
)
S["succeed"] = dict(
    name="家庭教師のサクシード", short="サクシード", full="家庭教師のサクシード（LD・ADHD・ASDサポートコース／オンライン家庭教師）",
    logo=("logos/succeed-logo.png", 270, 47), url="https://www.benkyo.co.jp/course/ld-adhd-asd/", sponsored=False,
    official="https://www.benkyo.co.jp/course/ld-adhd-asd/",
    scores=dict(support=4, teacher=4, trial=4, time=3, parent=5, price=4, contract=4),
    price_month=12320, min_minutes=60,
    best3=("LD・ADHD・ASDサポートコース", "毎回の授業報告＋月1回の面談", "オンラインは60分の無料体験授業があります。"),
    target="小学生〜高校生", btn_catch="無料体験は通常と同じ60分", btn="無料体験授業を公式で見る",
    catch="LD・ADHD・ASDサポートコースあり<br>オンラインは毎回の報告と月1回の保護者面談",
    cmp_text="専門スタッフが特性を聞き取り、発達支援の指導経験が豊富な先生から選ぶ。",
    chips=[("is-pink", "月1回の面談"), ("", "毎回の報告"), ("is-gray", "訪問も可")],
    features=[
        ('<span class="yk-mark">専門スタッフ</span>が親子と面談して特性を聞き取る', "https://www.benkyo.co.jp/course/ld-adhd-asd/"),
        ("発達支援の指導経験が豊富な先生から選抜", "https://www.benkyo.co.jp/course/ld-adhd-asd/"),
        ('オンラインは<span class="yk-red">毎回の授業報告＋月1回の保護者面談</span>', "https://www.benkyo.co.jp/course/online/"),
        ("先生の交代は何度でも無料。退会費・違約金なし", "https://www.benkyo.co.jp/course/online/"),
    ],
    editor=('サクシードには、LD・ADHD・ASDサポートコースがあります。専門スタッフが親子と面談して特性を聞き取り、発達支援の指導経験が豊富な先生から担当を選ぶ方針です。'
            'オンライン家庭教師では、毎回の授業報告に加えて<span class="yk-red">月に1回の保護者面談</span>があります。'
            '<span class="yk-mark">授業の様子を定期的に聞きながら進めたい家庭</span>に合います。', ""),
    info=[("料金の目安", "オンライン小学生 1時間3,080円〜<small>税込。月4回なら12,320円〜（当サイト計算）</small>"),
          ("対応学年", "小学生〜高校生<small>オンラインは全国・海外から</small>"),
          ("1回の授業", "1時間単位の料金<small>1コマの時間・回数で見積もり</small>"),
          ("先生", "発達支援の指導経験が豊富な先生から選抜"),
          ("保護者サポート", "毎回の授業報告・月1回の保護者面談"),
          ("無料体験", "オンラインは60分の無料体験授業")],
    plans=[("小学生", "オンライン・1時間あたり", "3,080円〜", "月4回なら12,320円〜（当サイト計算）"),
           ("中学生", "オンライン・1時間あたり", "4,070円〜", "月4回なら16,280円〜（当サイト計算）"),
           ("高校生", "オンライン・1時間あたり", "5,280円〜", "月4回なら21,120円〜（当サイト計算）")],
    plan_src="https://www.benkyo.co.jp/course/online/", plan_note="すべて税込。LD・ADHD・ASDサポートコース（訪問）の指導料は1時間5,830円〜（税込）",
    voices=[("読み書きに苦手がある子の保護者（公式サイト掲載）",
             "学習障がいにも対応していると知って選んだ。先生が「楽しく学ぶ」環境をつくってくれて、いつも部屋から笑い声が聞こえていた。"),
            ("中学2年生の保護者（公式サイト掲載）",
             "オンライン授業をきっかけに、少しずつ前向きな姿勢が戻ってきた。今は自分から机に向かうようになった。")],
    voice_src="https://www.benkyo.co.jp/course/ld-adhd-asd/",
    operator="株式会社サクシード",
)
S["try"] = dict(
    name="トライのオンライン個別指導塾", short="トライ", full="トライのオンライン個別指導塾（発達特性サポートコース）",
    logo=("logos/try-logo.svg", 220, 28), url="https://www.try-online.jp/kobetsu/tokusei/", sponsored=False,
    official="https://www.try-online.jp/kobetsu/tokusei/",
    scores=dict(support=4, teacher=4, trial=4, time=3, parent=5, price=4, contract=4),
    price_month=14960, min_minutes=60,
    best3=("発達特性サポートコース", "WISCの結果を学習に活かす", "教師とは別に教育プランナーが専任でつきます。"),
    target="小学生〜高校生", btn_catch="学習面談は入会しなくても受けられる", btn="無料の学習面談を公式で見る",
    catch="発達特性サポートコースあり<br>WISC検査の結果をもとに学習をサポート",
    cmp_text="正社員の教育プランナーが専任でつき、WISCの結果をもとに学習計画を立てる。",
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
          ("先生", "33万人の登録教師から選ぶ。専任制で原則同じ教師"),
          ("保護者サポート", "教育プランナーの定期面談・電話・LINE、学習管理アプリ"),
          ("無料体験", "無料の学習面談と、約30分の体験授業（英語か数学）")],
    plans=[("小学生", "1コマ60分×月4回", "14,960円〜", "入会金11,000円は別途"),
           ("中学生", "1コマ60分×月4回", "17,600円〜", "入会金11,000円は別途"),
           ("高校生", "1コマ60分×月4回", "21,120円〜", "入会金11,000円は別途")],
    plan_src="https://www.try-online.jp/kobetsu/price/", plan_note="すべて税込。年会費・登録料はなし（公式）",
    voices=[],
    voice_src=None,
    operator="株式会社トライグループ",
)
S["coaching1"] = dict(
    name="家庭教師のコーチング1", short="コーチング1", full="家庭教師のコーチング1（発達障害・グレーゾーン専門）",
    logo=("logos/coaching1-logo.png", 293, 27), url="https://coaching01.com/type/ldadhdas.html", sponsored=False,
    official="https://coaching01.com/type/ldadhdas.html",
    scores=dict(support=5, teacher=4, trial=4, time=2, parent=5, price=1, contract=4),
    price_month=30690, min_minutes=90,
    best3=("発達障害・グレーゾーン専門", "中学・高校受験に対応", "提携する臨床心理士の発達検査を受けられます。"),
    target="小学1年生〜高校3年生", btn_catch="無料の体験学習・学習カウンセリングあり", btn="無料体験を公式で見る",
    catch="発達障害・グレーゾーン専門の家庭教師<br>発達特性のある子の中学・高校受験に対応",
    cmp_text="発達障害・グレーゾーン専門。臨床心理士の発達検査と、受験対策が特徴。授業は90分から。",
    chips=[("is-pink", "受験対策"), ("", "発達検査"), ("is-gray", "90分から")],
    features=[
        ('提携する<span class="yk-mark">臨床心理士の発達検査</span>を受けられる', "https://coaching01.com/type/ldadhdas.html"),
        ('発達特性のある子の<span class="yk-red">中学受験・高校受験</span>に対応', "https://coaching01.com/type/ldadhdas.html"),
        ("独自の研修を受けた先生が担当。毎回の指導報告書", "https://coaching01.com/starting.html"),
        ("授業以外のことも教務部に相談できる", "https://coaching01.com/starting.html"),
    ],
    editor=('コーチング1は、発達障害・グレーゾーン専門の家庭教師です。提携する臨床心理士の発達検査を受けられること、'
            '<span class="yk-red">発達特性のある子の中学受験・高校受験</span>に対応していることが、6社の中でも目立つ特徴です。'
            '授業は1回90分からで料金は6社で最も高めですが、<span class="yk-mark">受験まで見据えて専門の家庭教師に任せたい家庭</span>には候補になります。', ""),
    info=[("料金の目安", "週1回90分 月30,690円〜<small>税込。別途入会金18,700円・年会費</small>"),
          ("対応学年", "小学1年生〜高校3年生<small>オンラインは全国から</small>"),
          ("1回の授業", "90分〜<small>回数・時間は目的に合わせて相談</small>"),
          ("先生", "独自の研修を受けた先生"),
          ("保護者サポート", "毎回の指導報告書・教務部に相談"),
          ("無料体験", "体験学習・学習カウンセリング（約120分）")],
    plans=[("小学生〜高校生", "週1回90分〜", "30,690円〜", "入会金18,700円・年会費は別途")],
    plan_src="https://coaching01.com/price.html", plan_note="すべて税込。交通費は訪問の場合のみ実費",
    voices=[],
    voice_src=None,
    operator="株式会社AXT",
)

# 採点の根拠（method.html の根拠表。各社公式サイトの記載、2026-10-14確認）
WHY = {
    "sogaku": dict(support="発達障害・グレーゾーン専門。発達凸凹アソシエーションが講師研修・アセスメントシート・教材アドバイスに関わる", teacher="先生は全員社会人で、専門機関の教師研修とマニュアル研修を受けている（臨床心理士・作業療法士などの資格者も在籍）", trial="無料体験2回。入会後に担当する予定の先生が体験を担当と明記", time="小学生25分・中高生35分のコース", parent="毎回の指導報告＋先生・本部とチャット、定期的な保護者面談、保護者向け勉強会", price="小学生25分×月4回 13,200円（税込）", contract="入会金22,000円（税込）、年会費・保証金・更新費・違約金・途中解約料0円、契約期間の縛りなし、月単位の休会・退会、退会は前月10日までと本体ページに明記"),
    "runner": dict(support="勉強が苦手な子専門の中に発達障害サポートのコース。発達障害コミュニケーション指導者のスタッフが先生を指導", teacher="カルテから10〜20名の候補→面談で決定、指導前に特性と指導法を研修（先生紹介は大学生・大学院生が中心）", trial="90分の無料体験レッスン（学習アドバイザーが担当、先生は申込後に選考）", time="1コマ30分単位", parent="毎月の指導報告書、公式LINEで相談、本部から定期的に状況確認", price="小学生 9,000円〜（1コマ30分900円）", contract="入会金・税込かどうか・最低契約期間・解約の決まりは本体ページに記載なし（広告用LPに「1ヶ月ごとの更新制、違約金は基本的になし」）"),
    "tintle": dict(support="不登校専門。発達障がい・グレーゾーン・支援級も対象、不登校心理相談士が家庭を担当", teacher="全員が現役の大学生。初任者研修（発達障害の特性を含む）と担当生徒ごとの研修", trial="保護者の個別相談会（約1時間・サポートスタッフ）。子どもの体験は希望制で、担当講師は入会書類の返送後に決定", time="1コマ30分", parent="不登校心理相談士がオンライン面談・LINE・電話で相談（毎回の授業報告の記載なし）", price="小学生 週1回1時間 月10,560円〜（4週換算・税込）", contract="入会金・教材費・最低契約期間・解約・休会の決まりは公式サイトに記載なし（キャンセルは1時間前まで無料と記載）"),
    "succeed": dict(support="LD・ADHD・ASDサポートコース。専門スタッフが親子と面談", teacher="発達支援の指導経験が豊富な先生から選抜", time="1時間単位の料金", price="オンライン小学生 1時間3,080円×月4回＝12,320円", parent="毎回の授業報告＋月1回の保護者面談", trial="オンライン60分の無料体験（担当予定の先生ではない。先生は申込後に指定）", contract="教材費なし、退会費・違約金なし（1か月前に通知）、8日以内は解約可と記載。入会金・最低期間・休会は記載なし"),
    "try": dict(support="発達特性サポートコース。教育プランナーが専任、WISCの結果を活用", teacher="不登校・発達特性の指導実績がある教師が在籍、ヒアリングをもとに選定", time="料金例は1コマ60分", price="小学生 60分×月4回 14,960円", parent="アプリで毎回の進捗＋教育プランナーの定期面談・電話・LINE", trial="約30分の無料体験授業（英語か数学）＋無料学習面談", contract="入会金11,000円（税込）、教材費・年会費なし、前月までの申し出で解約金なしと記載。最低期間・休会は記載なし"),
    "coaching1": dict(support="発達障害・グレーゾーン専門。提携する臨床心理士の発達検査", teacher="独自の研修を受けた先生", time="1回90分から", price="週1回90分 月30,690円〜", parent="毎回の指導報告書＋教務部に相談", trial="約120分の無料体験学習・学習カウンセリング（担当教務）", contract="入会金18,700円（税込）、教材費なし、年会費あり（金額の記載なし）。解約・違約金・最低期間・休会は記載なし"),
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


def esc(t):
    return html.escape(t, quote=True)


def link_attrs(s, cta=None):
    if s["sponsored"]:
        return f'href="{s["url"]}" target="_blank" rel="sponsored nofollow noopener" data-cta data-cta-id="{cta or "ranking"}"'
    return f'href="{s["url"]}" target="_blank" rel="nofollow noopener"'


def logo_img(s, cls="", alt=None, lazy=True):
    f, w, h = s["logo"]
    return f'<img{(" class=%s" % chr(34) + cls + chr(34)) if cls else ""} src="{IMG}{f}" alt="{esc(s["name"] if alt is None else alt)}" width="{w}" height="{h}"{" loading=" + chr(34) + "lazy" + chr(34) if lazy else ""}>'


def banner(s, cls, cta):
    """公式バナー枠：ソウガクはASP発行バナー（コードのまま）、ほかはASP素材がないので公式ロゴで代える"""
    if s["sponsored"]:
        return (f'<a class="{cls} rk-banner" {link_attrs(s, cta)}><img src="{ASP_IMG}" width="300" height="250" '
                f'alt="{esc(s["full"])}" loading="lazy"></a>')
    return f'<span class="{cls} rk-logobox">{logo_img(s)}</span>'


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
    return (f'<div class="yk-radar" data-name="{esc(s["short"])}" data-labels="{labels}" data-scores="{scores}"></div>\n'
            f'<p class="yk-small yk-radar__note">※編集部の採点（基準は<a href="method.html">ランキング調査概要</a>）。総合評価 {s["total"]}</p>')


def info_table(s):
    r = s["info"]
    rows = ""
    for i in range(0, 6, 2):
        (a, av), (b, bv) = r[i], r[i + 1]
        left = ' class="is-left"' if i == 4 else ""
        rows += f"<tr><th>{a}</th><th>{b}</th></tr><tr><td{left}>{av}</td><td{left}>{bv}</td></tr>"
    return f'<table class="yk-info">{rows}</table>\n<p class="yk-small">※各社公式サイトの記載（{CHECKED}確認）。</p>'


def features(s, ttl="特徴"):
    lis = "".join(f'<li><span>{t}</span></li>' for t, _ in s["features"])
    return (f'<div class="yk-features"><p class="yk-features__ttl">{ttl}</p><ul>{lis}'
            f'<li><span class="yk-red">対象：{s["target"]}</span></li></ul></div>')


def jobex(s):
    cards = ""
    for i, (g, plan, price, note) in enumerate(s["plans"], 1):
        cards += (f'<div class="yk-jobex"><p class="yk-jobex__ttl">料金プランの例{i}</p><ul class="yk-tags yk-tags--green"><li>{g}</li><li>オンライン</li></ul>'
                  f'<table class="yk-kv"><tr><th>月額</th><td><b>{price}</b></td></tr><tr><th>授業</th><td>{plan}</td></tr><tr><th>補足</th><td>{note}</td></tr></table>'
                  f'<p class="yk-catch">{esc(s["btn_catch"])}</p><a class="yk-btn yk-btn--sm" {link_attrs(s, "rank_plan")}>公式で料金を見る</a>'
                  f'<span class="yk-jobex__logo" style="display:block">{logo_img(s, alt="")}</span></div>')
    hint = '<p class="yk-hint">横にスクロールできます</p>' if len(s["plans"]) > 1 else ""
    return (f'{hint}<div class="yk-hscroll">{cards}</div>\n'
            f'<p class="yk-small">※{s["plan_note"]}。出典：<a href="{s["plan_src"]}" target="_blank" rel="nofollow noopener">{esc(s["short"])}公式サイト</a>（{CHECKED}確認）</p>')


def voices(s):
    if not s["voices"]:
        return ""
    lis = "".join(f'<li><div class="yk-voice__who"><span class="yk-voice__face"><img src="{IMG}gen/icon_parent_illust.webp" alt="" width="240" height="240" loading="lazy"></span>{esc(w)}</div><p>{esc(t)}</p></li>'
                  for w, t in s["voices"])
    return (f'<h4 class="yk-voice__ttl">{esc(s["short"])}の口コミ</h4>\n<ul class="yk-voice">{lis}</ul>\n'
            f'<p class="yk-small">※<a href="{s["voice_src"]}" target="_blank" rel="nofollow noopener">{esc(s["short"])}公式サイト</a>掲載の声を当サイトで要約。個人の感想です。アイコンはイメージです。</p>')


def btn_main(s, cta, text=None):
    return f'<p class="yk-catch">{esc(s["btn_catch"])}</p><a class="yk-btn" {link_attrs(s, cta)}>{text or s["btn"]}</a>'


# ---------------------------------------------------------------- トップ
def talk_row(who, text, right):
    icon = "icon_parent_illust" if who == "保護者" else "icon_editor_illust"
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
        "先生": ("◎", "全員が社会人。全員が専門機関の研修を受講。臨床心理士・作業療法士などの資格者も在籍"),
        "指導計画": ("◎", "専門家が開発したアセスメントシートで一人ずつ作成。体験後に受け取れる"),
        "診断・手帳": ("◎", "不要（診断名の申告・手帳の提出も不要）と明記"),
        "最短の授業": ("◎", "小学生25分・中高生35分"),
        "体験を担当する人": ("◎", "入会後に担当する予定の先生"),
        "体験の回数・時間": ("◎", "2回。小学生25分か50分（中高生35分か60分）。1回目を保護者面談にもできる"),
        "授業の報告": ("◎", "毎回、アプリで指導報告"),
        "保護者の相談": ("◎", "先生・本部にチャット。定期的な保護者面談、保護者向け勉強会"),
        "時間の融通": ("○", "土日・夜21時〜・午前も可。回数・時間は月ごとに変更、同じ月内で振替"),
        "学校に行きづらい子": ("○", "午前中の授業に対応"),
        "小学生の料金": ("○", "25分×月4回 13,200円（税込）"),
        "入会金": ("○", "22,000円（税込）。キャンペーンで無料の場合あり"),
        "教材費": ("◎", "購入不要。学習ツール（映像授業2,000本など）も追加費用なし"),
        "解約・違約金": ("◎", "違約金・途中解約料0円、契約期間の縛りなし、月単位で休会・退会"),
        "先生の交代": ("◎", "何度でも無料。性別の希望も伝えられる"),
    },
    "runner": {
        "専門の範囲": ("○", "勉強が苦手な子専門。発達障害サポートはコースの一つ"),
        "専門家の関わり": ("○", "「発達障害コミュニケーション指導者」の本部スタッフが先生を指導"),
        "先生": ("○", "大学生〜社会人の登録者から本部が選考（紹介ページは大学生・大学院生が中心）"),
        "指導計画": ("○", "決まったカリキュラムを置かず、特性に合わせて教え方を変える"),
        "診断・手帳": ("○", "グレーゾーンも対象と記載"),
        "最短の授業": ("○", "1コマ30分単位"),
        "体験を担当する人": ("△", "学習アドバイザー（先生は申込後に選考）"),
        "体験の回数・時間": ("○", "1回・90分程度"),
        "授業の報告": ("○", "毎月の指導報告書"),
        "保護者の相談": ("○", "公式LINE・電話・メール・Web面談"),
        "時間の融通": ("○", "指導した分だけ支払い。20時・21時開始も可"),
        "学校に行きづらい子": ("○", "不登校のコースあり"),
        "小学生の料金": ("◎", "1コマ30分900円。9,000円〜（税込・税抜の記載なし）"),
        "入会金": ("－", "公式に記載なし"),
        "教材費": ("○", "高額教材の販売なし（広告用LPの記載）"),
        "解約・違約金": ("△", "本体ページに記載なし（広告用LPに「1ヶ月ごとの更新制、違約金は基本的になし」）"),
        "先生の交代": ("○", "何度でも無料"),
    },
    "tintle": {
        "専門の範囲": ("○", "不登校専門。発達障がい・グレーゾーンも対象"),
        "専門家の関わり": ("○", "不登校心理相談士の本部スタッフが家庭を担当"),
        "先生": ("△", "全員が現役の大学生"),
        "指導計画": ("○", "入会前のカウンセリングをもとに決める"),
        "診断・手帳": ("○", "検査を受けていない子も対応と記載"),
        "最短の授業": ("○", "1コマ30分"),
        "体験を担当する人": ("△", "サポートスタッフ（講師は入会書類の返送後に決定）"),
        "体験の回数・時間": ("○", "保護者の相談会 約1時間（何度でも）。子どもの体験は希望制"),
        "授業の報告": ("－", "保護者向けの定期報告の頻度は記載なし"),
        "保護者の相談": ("◎", "不登校心理相談士がLINE・電話・オンライン面談（無料）"),
        "時間の融通": ("◎", "曜日・時間・回数を固定しない。1時間前までキャンセル無料"),
        "学校に行きづらい子": ("◎", "不登校専門。出席扱いの申請オプション（有料）"),
        "小学生の料金": ("◎", "1コマ30分1,320円〜。週1回1時間で月10,560円〜（税込）"),
        "入会金": ("－", "公式に記載なし"),
        "教材費": ("－", "公式に記載なし"),
        "解約・違約金": ("－", "公式に記載なし"),
        "先生の交代": ("－", "公式に記載なし"),
    },
    "succeed": {
        "専門の範囲": ("○", "総合家庭教師のコースの一つ（LD・ADHD・ASDサポートコース）"),
        "専門家の関わり": ("○", "特性が強い子は専門スタッフが親子と面談し、講師へ引き継ぐ"),
        "先生": ("○", "大学生からプロまで。発達支援の指導経験がある先生から専任スタッフが選ぶ"),
        "指導計画": ("○", "特性に合わせたオーダーメイドのカリキュラム。検査結果も参照"),
        "診断・手帳": ("△", "要否の明記なし（診断があれば検査結果を参照）"),
        "最短の授業": ("△", "1時間単位（オンラインの通常授業は60分）"),
        "体験を担当する人": ("△", "担当予定の先生ではない（先生は申込後に指定）"),
        "体験の回数・時間": ("○", "60分（オンライン）"),
        "授業の報告": ("◎", "毎回の授業報告（オンライン）"),
        "保護者の相談": ("◎", "月1回の保護者面談。専門スタッフにいつでも相談（LDコース）"),
        "時間の融通": ("○", "曜日・時間を選べる。振替あり、月の回数を増減できる"),
        "学校に行きづらい子": ("○", "不登校サポートコースあり"),
        "小学生の料金": ("○", "オンライン1時間3,080円〜。月4回で12,320円〜（税込・当サイト計算）"),
        "入会金": ("－", "公式に記載なし"),
        "教材費": ("○", "追加の教材費なし（手持ちの教材を使う）"),
        "解約・違約金": ("△", "退会費・違約金なしと記載。ただし特商法表記に、1か月前の通知がない場合の支払いの定めあり"),
        "先生の交代": ("○", "何度でも無料"),
    },
    "try": {
        "専門の範囲": ("○", "オンライン個別指導塾のコースの一つ（発達特性サポートコース）"),
        "専門家の関わり": ("○", "正社員の教育プランナーが家庭ごとに付く"),
        "先生": ("○", "プロから学生まで。全員が研修を受講。特性の指導実績がある先生が在籍"),
        "指導計画": ("◎", "教育プランナーが専用カリキュラムを作成。WISCの検査結果をもとにサポート"),
        "診断・手帳": ("○", "発達障がい・学習障がいがあっても入会できる（要否の明記なし）"),
        "最短の授業": ("△", "料金例は1コマ60分（最短の明記なし）"),
        "体験を担当する人": ("△", "記載なし（事前の学習面談は教育プランナー）"),
        "体験の回数・時間": ("○", "約30分（英語か数学）＋無料学習面談"),
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
        "専門の範囲": ("◎", "「発達障害・グレーゾーン専門」を掲げる"),
        "専門家の関わり": ("◎", "提携する臨床心理士の発達検査。面談は発達障害専門のスタッフ"),
        "先生": ("○", "大学生6割・大学院生1割・プロ3割。独自の研修"),
        "指導計画": ("◎", "WISCなどのデータで特性を分析して学習計画"),
        "診断・手帳": ("○", "確定診断のない子の悩みも対象例に挙げる（要否の明記なし）"),
        "最短の授業": ("△", "1回90分から"),
        "体験を担当する人": ("△", "担当教務（スタッフ）"),
        "体験の回数・時間": ("○", "体験学習と学習カウンセリングで約120分"),
        "授業の報告": ("◎", "毎回、指導報告書"),
        "保護者の相談": ("○", "教務部に相談。教務スタッフが定期的に連絡"),
        "時間の融通": ("○", "振替あり（前日までに連絡）。回数・時間のパターンを選べる"),
        "学校に行きづらい子": ("○", "不登校でも指導（不登校コーチング）"),
        "小学生の料金": ("△", "週1回90分から月30,690円〜（税込）"),
        "入会金": ("○", "18,700円（税込）"),
        "教材費": ("○", "教材費なし。年会費あり（金額の記載なし）"),
        "解約・違約金": ("－", "公式に記載なし"),
        "先生の交代": ("○", "何回でも無料"),
    },
}
N_ITEMS = sum(len(items) for _, items in CMP_GROUPS)


def top():
    R = [S[k] for k in RANK]
    names = "・".join(s["short"] for s in R)
    n_ax = len(AXES)
    o = head("【2026年10月】発達障害・グレーゾーンの子に合うオンライン家庭教師ランキングTOP3｜6社を比較",
             f"発達障害・グレーゾーンの子に対応したオンライン家庭教師6社（{names}）を、発達特性への対応・先生・入会前の確認・授業時間・保護者サポート・料金・費用と契約の{n_ax}項目で採点し、{N_ITEMS}項目で比較しました。")
    # A-0 PR（FVの上）
    o += '\n<!-- A-0 PR表記（yk-pr）：FVの上。FV直下は会話にするため -->\n<p class="yk-pr"><b>PR</b><span>当サイトはアフィリエイト広告を利用しており、ソウガクのプロモーションを含みます。順位は広告の有無ではなく、<a href="method.html">公開している採点基準</a>で決めています（' + UPDATED + '最新版）。</span></p>\n'
    # A-1 FV ヒーロー画像
    o += f"""
<!-- A-1 FV：ヒーロー画像（王道LPと同じ 00_hero_top3_v3。見出しは画像内の文字、同じ文を lp-sr に持つ） -->
<h1 class="lp-hero"><span class="lp-sr">発達障害・グレーゾーンの子に合う オンライン家庭教師ランキングTOP3</span><img fetchpriority="high" src="{IMG}gen/00_hero_top3_v3.webp" srcset="{IMG}gen/00_hero_top3_v3-608.webp 608w, {IMG}gen/00_hero_top3_v3-912.webp 912w, {IMG}gen/00_hero_top3_v3.webp 1200w" sizes="(max-width: 751px) 100vw, 696px" alt="" width="1200" height="675"></h1>
"""
    # A-2 導入会話（画像なし）
    rows = [
        ("保護者", "宿題を見ていると、すぐ親子げんかになってしまって…。家庭教師をお願いしたいけど、<span class='mt-mark'>発達特性を分かってくれる先生</span>って、どう選べばいいんでしょう？", True),
        ("編集部", "見るところは3つです。<b>先生が発達特性を学んでいるか</b>、<b>授業の長さが子どもに合うか</b>、そして<b>入会前に実際の先生と試せるか</b>。", False),
        ("保護者", "うちの子、30分も座っていられるか心配で…。診断もまだ受けていないんです。", True),
        ("編集部", "それなら、小学生は25分から選べて、診断なしでも相談できる<span class='mt-mark'>ソウガク</span>から見てみてください。入会後に担当する予定の先生と、無料体験を2回受けられます。", False),
        ("保護者", "ほかの家庭教師とも比べてから決めたいです。", True),
        ("編集部", f"発達特性に対応したオンライン家庭教師6社の公式サイトを{CHECKED}に確認して、{n_ax}つの基準で採点しました。上位3社をTOP3として紹介しています。", False),
    ]
    o += ('\n<!-- A-2 導入会話（mt-talk）：FV直下。画像なし。よくある迷いを編集部が会話例にしたもの（実在の発言ではない） -->\n<div class="mt-talk">'
          + "".join(talk_row(w, t, r) for w, t, r in rows) + '</div>\n<p class="yk-small">※よくある迷いを編集部が会話形式にしたものです（人物はイメージ）。</p>\n')
    # B-1 BEST3
    items = ""
    for s in R[:3]:
        r, m, t = s["best3"]
        items += (f'<li class="yk-best3__item"><span class="yk-best3__crown">{s["rank"]}</span><span class="yk-best3__logo">{logo_img(s, lazy=False)}</span>'
                  f'<p class="yk-best3__text"><span class="yk-red">{r}</span><br><span class="yk-mark">{m}</span>。{t}</p>'
                  f'<p class="yk-best3__note">※対象は{s["target"]}</p><p class="yk-catch">総合評価 {s["total"]}</p>'
                  f'<a class="yk-btn yk-btn--sm" {link_attrs(s, "best3")}>公式サイト</a></li>')
    o += f'\n<!-- B-1 BEST3（yk-best3）：順位の根拠は method.html -->\n<section class="yk-best3"><h2 class="yk-best3__ttl"><em>発達特性</em>に強いオンライン家庭教師<em>TOP3</em></h2>\n<ol class="yk-best3__list">{items}</ol></section>\n'
    # B-2 ソウガクの目的別プラン（求人の例カードの型）
    sg = S["sogaku"]
    jobs = [
        ("集中が続きにくい・低学年", "05_online_home.webp", "家のノートパソコンで学ぶ子ども", "小学生", "25分×月4回", "13,200円", ["25分から", "体験2回", "毎回の報告"]),
        ("小学生でしっかり学びたい", "08_calm_home.webp", "落ち着いた部屋の机に向かう子ども", "小学生", "50分×月4回（公式のおすすめ）", "22,000円", ["5教科", "科目数で料金同じ", "教材購入なし"]),
        ("中学生・受験も見すえて", "04_one_on_one.webp", "机で勉強する子ども", "中学生", "35分×月4回（60分は26,400円）", "18,480円", ["受験対策にも対応", "受験生割増なし", "振替あり"]),
        ("高校生・得意を活かしたい", "01_fv_study.webp", "机でノートに書く子ども", "高校生", "35分×月4回（60分は29,920円）", "21,560円", ["得意を活かす", "学年で料金UPなし", "違約金0円"]),
    ]
    cards = ""
    for ttl, img, alt, g, plan, pay, tags in jobs:
        tg = "".join(f"<li>{t}</li>" for t in tags)
        cards += (f'<div class="yk-jobcard"><h3 class="yk-jobcard__ttl">{ttl}</h3><img class="yk-jobcard__img" src="{IMG}{img}" alt="{alt}（イメージ）" width="960" height="640" loading="lazy">'
                  f'<p class="yk-jobcard__pay">月額<b>{pay}</b></p><table class="yk-kv"><tr><th>学年</th><td>{g}</td></tr>'
                  f'<tr><th>授業</th><td>{plan}</td></tr></table><ul class="yk-tags">{tg}</ul>'
                  f'<p class="yk-catch">{esc(sg["btn_catch"])}</p><a class="yk-btn yk-btn--sm" {link_attrs(sg, "plan_card")}>無料体験を公式で見る</a></div>')
    o += f"""
<!-- B-2 1位ソウガクの目的別プラン（yk-hscroll + yk-jobcard）：公式の料金表（{sg["plan_src"]}、{CHECKED}確認） -->
<h2 class="yk-sec-ttl">1位<em>ソウガク</em>の料金プラン｜目的別の例</h2>
<p class="yk-hint">横にスクロールできます</p>
<div class="yk-hscroll">{cards}</div>
<p class="yk-small">※月額は<a href="{sg["plan_src"]}" target="_blank" rel="nofollow noopener">ソウガク公式サイト</a>の料金表（月4回・税込、{CHECKED}確認）。入会金22,000円（税込）は別途（キャンペーンで無料の場合あり）。月8回のコースもあります。写真はイメージです。</p>
"""
    # C-1 比較表（タブ：総合＋17項目を3つのタブに）
    def mk(v):
        return {5: "◎", 4: "○", 3: "△", 2: "△", 1: "×"}[v]
    rows = ""
    for s in R:
        chips = "".join(f'<li class="{c}">{t}</li>' if c else f"<li>{t}</li>" for c, t in s["chips"])
        rows += (f'<tr{" class=" + chr(34) + "is-pick" + chr(34) if s["rank"] == 1 else ""}><td><span class="yk-cmp__rank">{s["rank"]}</span><span class="yk-cmp__logo" style="display:block">{logo_img(s)}</span>'
                 f'<a class="yk-cmp__name" href="{s["id"]}.html">{esc(s["short"])}</a><span class="yk-stars">{stars(s["total"])}</span><span class="yk-grade">総合評価 <b>{s["total"]}</b></span></td>'
                 f'<td><span class="yk-maru">{mk(s["scores"]["trial"])}</span>{CMP[s["id"]]["体験を担当する人"][1]}</td>'
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
<h2 class="yk-sec-ttl" id="compare"><em>6社</em>を{N_ITEMS}項目で比較</h2>
<p>先生・体験・授業の長さ・報告・費用や契約まで、各社の公式サイトに書かれていることを並べました。<span class="yk-mark">1位のソウガクは{N_ITEMS}項目のうち{win}項目で◎</span>です。</p>
<div class="yk-tabs rk-tabs4">
  <input type="radio" name="cmp1" id="cmp1-1" checked>{radios}
  <div class="yk-tabs__labels"><label for="cmp1-1">総合</label>{labels}</div>
  <div class="yk-tabs__panels">
    <div><div class="yk-fold"><input type="checkbox" id="cmp1-more"><div class="yk-fold__body">
      <table class="yk-cmp"><colgroup><col class="c1"><col class="c2"><col><col class="c4"></colgroup>
        <tr><th>サービス</th><th>入会前の体験</th><th>編集部のひとこと</th><th>公式</th></tr>
        {rows}
      </table></div><label class="yk-fold__btn" for="cmp1-more">もっと見る</label></div></div>{panels}
  </div>
</div>
<p class="yk-small">※◎＝特に手厚い、○＝ある、△＝限られる、－＝公式に記載なし（各社公式サイトの記載をもとにした当サイトの判断、{CHECKED}確認）。「総合」の入会前の体験の記号と総合評価は、<a href="method.html">ランキング調査概要</a>で公開している{n_ax}項目の採点によります。ランナーの解約・教材の欄は、本体ページにない内容を広告用LPの記載で補っています。</p>
{btn_main(sg, "compare")}
"""
    # C-2 2軸マップ（縦＝入会前の確認、横＝特性への対応＋先生）
    pos = {"sogaku": (80, 16), "coaching1": (76, 52), "runner": (25, 40), "succeed": (25, 53), "try": (25, 66), "tintle": (25, 86)}
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
<h2 class="yk-sec-ttl">ひと目でわかる<em>6社の位置</em></h2>
<div class="yk-matrix">
  <span class="yk-matrix__ax yk-matrix__ax--t">担当の先生と試せる</span><span class="yk-matrix__ax yk-matrix__ax--b">相談が中心</span><span class="yk-matrix__ax yk-matrix__ax--l">特性への支援 標準</span><span class="yk-matrix__ax yk-matrix__ax--r">特性への支援 厚い</span>
  {items}
</div>
<p class="yk-small">※縦は当サイトの採点「入会前に確かめられること」、横は「発達特性への対応」と「先生の体制」の合計（<a href="method.html">基準</a>）。同じ値の会社は重ならないよう上下にずらしています。</p>
"""
    # C-3 ソウガクの無料体験2回（yk-combo の型をソウガク1社で使う）
    o += f"""
<!-- C-3 無料体験のすすめ（yk-combo）：ソウガク1社・カード1枚（公式 faq.html・trial-flow.html、{CHECKED}確認） -->
<section class="yk-combo"><h2 class="yk-combo__ttl"><em>ソウガク</em>の無料体験2回で<br>先生との相性を確かめましょう！</h2>
  <div class="yk-combo__card"><p class="yk-combo__head">担当予定の先生と、2回試してから決められる</p><span class="yk-combo__logo" style="display:block">{logo_img(sg)}</span><a class="yk-combo__link" href="sogaku.html#f3">体験の流れを見る</a>
    <ul class="yk-combo__points"><li><b>1回目は保護者と先生の面談にもできる！</b><br>体験を担当するのは、入会後に担当する予定の先生。子どもの様子や苦手なことを先に伝えてから、2回目に授業を受けられます。</li><li><b>小学生は25分か50分！</b><br>中高生は35分か60分。最初に流れを説明して、できることから始めます。</li><li><b>体験後に指導計画がもらえる</b><br>得意・不得意をまとめた、その子だけの指導計画を受け取れます。相性が合えば、そのまま同じ先生が担当します。</li></ul>
    {btn_main(sg, "combo")}</div>
</section>
<p class="yk-small">※体験は無料・2回まで（1回目から子どもの授業にすることもできます）。体験の前に教務担当が学習状況や希望を聞きます。申込フォームは「簡単3分。無理な入会・教材販売はございません」と公式に記載（<a href="https://sogaku.jp/online/faq.html" target="_blank" rel="nofollow noopener">公式のよくある質問</a>、{CHECKED}確認）。</p>
"""
    # D ランキング
    o += f"""
<!-- D ランキング：順位見出し→赤キャッチ→タブ（イチオシ／基本情報／料金プラン例）→特徴→編集部→口コミ→2ボタン -->
<h2 class="yk-sec-ttl" id="ranking">発達特性に強いオンライン家庭教師<br><em>おすすめランキング</em></h2>
<div class="mt-say"><span class="mt-say__icon"><img src="{IMG}gen/icon_editor_illust.webp" alt="" width="240" height="240" loading="lazy"></span><p class="mt-say__b">先生との相性は、体験してみないと分かりません。ソウガクは入会後に担当する予定の先生と2回体験できるので、まずはそこで確かめるのがおすすめです。</p></div>
"""
    for s in R:
        n = s["rank"]
        medal = "yk-medal" + {1: "", 2: " yk-medal--2", 3: " yk-medal--3"}.get(n, " yk-medal--n")
        o += f"""
<!-- 第{n}位 {s["name"]}（事実の出典：{s["official"]} ほか、{CHECKED}確認） -->
<div class="yk-rankarea" id="rank-{s["id"]}"><h3 class="yk-rankhead"><span class="{medal}">{n}</span>{esc(s["name"])}</h3><p class="yk-rankcatch">{s["catch"]}</p>
<div class="yk-tabs">
  <input type="radio" name="rk{n}" id="rk{n}-1" checked><input type="radio" name="rk{n}" id="rk{n}-2"><input type="radio" name="rk{n}" id="rk{n}-3">
  <div class="yk-tabs__labels"><label for="rk{n}-1">イチオシ<br>ポイント</label><label for="rk{n}-2">基本情報</label><label for="rk{n}-3">料金<br>プラン例</label></div>
  <div class="yk-tabs__panels" style="background:#fff;padding:10px">
    <div>{banner(s, "rk-tabbanner", "rank_banner")}{btn_main(s, "rank_tab")}
    {features(s)}</div>
    <div>{radar(s)}
    {info_table(s)}</div>
    <div>{jobex(s)}</div>
  </div>
</div>
<div class="yk-editor"><p class="yk-editor__ttl">編集部の<em>イチオシ</em>ポイント</p><img class="yk-editor__chara" src="{IMG}gen/icon_editor_illust.webp" alt="" width="240" height="240" loading="lazy">
<div class="yk-editor__body"><p>{s["editor"][0]}</p>{('<p class="yk-small" style="text-align:right">' + s["editor"][1] + '</p>') if s["editor"][1] else ""}</div></div>
{voices(s)}
<div class="yk-btnpair"><a class="yk-btn yk-btn--sub" href="{s["id"]}.html">詳細は<br>こちら</a><div>{btn_main(s, "rank")}</div></div>
</div>
"""
    # E-1 迷ったらまずは（ソウガクだけ）
    o += f"""
<!-- E-1 迷ったらまずは（yk-pickup）：ソウガク1社 -->
<section class="yk-pickup"><h2 class="yk-pickup__ttl"><small>迷ったらまずは</small><br><em>ソウガク</em>の無料体験から！</h2>
<ul class="yk-pickup__list">
  <li class="yk-pickup__item"><p class="yk-pickup__name">ソウガク</p>{banner(sg, "yk-pickup__img", "pickup_banner")}<p class="yk-pickup__text">発達特性を学んだ社会人講師と、25分の短い授業から。担当予定の先生と2回試してから決められます。違約金・途中解約料は0円です。</p><p class="yk-catch">診断なし・グレーゾーンでもOK</p><a class="yk-btn yk-btn--sm" {link_attrs(sg, "pickup")}>無料体験を公式で見る</a></li>
</ul></section>
"""
    # E-2 診断
    o += f"""
<!-- E-2 診断フォーム（yk-finder）：結果は下の rk-result にその場で表示。判定は各社公式の記載で決められる条件だけ（rules は ranking.js） -->
<form class="yk-finder" id="finder" action="#finder-result"><p class="yk-finder__ttl">オンライン家庭教師<br><em>かんたん</em>診断</p>
  <label class="yk-finder__row">学年<select name="grade"><option value="">指定なし</option><option value="pre">未就学</option><option value="es">小学生</option><option value="jhs">中学生</option><option value="hs">高校生</option></select></label>
  <label class="yk-finder__row">いちばん気になること<select name="concern"><option value="">指定なし</option><option value="focus">集中が続きにくい</option><option value="match">先生との相性</option><option value="nodiag">診断を受けていない</option><option value="school">学校に行きづらい</option><option value="exam">受験を考えている</option><option value="cost">費用を抑えたい</option></select></label>
  <label class="yk-finder__row">1回の授業の長さ<select name="length"><option value="">指定なし</option><option value="short">30分くらいまで</option><option value="mid">60分くらい</option><option value="long">90分でもよい</option></select></label>
  <fieldset><legend>こだわり条件</legend><div class="yk-finder__checks"><label><input type="checkbox" name="report">毎回の報告がほしい</label><label><input type="checkbox" name="adult">社会人の先生がいい</label><label><input type="checkbox" name="contract">解約のルールが明確</label><label><input type="checkbox" name="flex">回数を固定したくない</label></div></fieldset>
  <button class="yk-finder__submit" type="submit">診断する</button></form>
<div class="rk-result" id="finder-result" aria-live="polite" hidden></div>
<p class="yk-small">※診断は各社公式サイトの記載（{CHECKED}確認）をもとに当サイトが判定したもので、合う・合わないを保証するものではありません。入力した内容は送信・保存しません。</p>
"""
    js = RADAR_JS + '<script src="ranking.js"></script>\n'
    return o + end(js)


# ---------------------------------------------------------------- 個別ページ
DETAIL = {}
DETAIL["sogaku"] = dict(
    strengths=[
        ("発達特性を学んだ社会人講師が教える",
         "<p>ソウガクの先生は全員が社会人で、発達支援の専門機関「一般社団法人 発達凸凹アソシエーション」による教師研修と、座学のマニュアル研修を受けています。発達凸凹アソシエーションは2014年から発達障害・グレーゾーンの保護者向け研修を行っている団体で、講師研修のほか、教材のアドバイスやスタッフ研修にも関わっています。放課後等デイサービスや児童発達支援事業所での勤務経験、臨床心理士・作業療法士・学校教員などの資格を持つ先生も在籍しています。</p>"
         "<p>宿題を始めるまでに時間がかかる、説明の途中で気がそれる。そんなときの声のかけ方を学んだ先生が担当します。</p>",
         ("official/sogaku/course-top_tool_communication.png", 600, 487, "授業後の指導報告と、教師・本部とのチャットの画面", "https://sogaku.jp/online/course.html")),
        ("小学生は25分から。短い授業で始められる",
         "<p>コースは小学生が25分か50分、中高生が35分か60分です。集中が続きにくい子や低学年向けに、短いコースが用意されています。勉強だけでなく、会話や脳トレのようなゲームを取り入れることもあります。</p>",
         None),
        ("担当予定の先生と、無料体験を2回受けられる",
         "<p>無料体験は2回で、体験を担当するのは入会後に担当する予定の先生です。1回目は保護者面談にすることもできます。体験のあとは、先生と教務が作った指導計画を受け取れます。</p>",
         ("official/sogaku/taiken-yousu2_pc.png", 1000, 350, "体験授業の様子（オンライン授業の画面）", "https://sogaku.jp/online-lp/01/index_i.html")),
        ("専門家が作ったアセスメントシートで、指導計画をつくる",
         "<p>専門家が開発したアセスメントシートで、記憶力・集中力などのつまずきの原因を特性面と環境面から見て、一人ずつ指導計画をつくります。たとえば「1回の指示を1つにする」「授業の最初に流れを説明して見通しを持たせる」といった支援です。体験のあとに、その子だけの指導計画を受け取れます。</p>",
         None),
        ("授業のたびに報告が届き、チャットで相談できる",
         "<p>授業が終わるたびに、先生が専用アプリで指導報告を送ります。気になることは、教師や本部にチャットで相談できます。保護者向けの勉強会や相談窓口もあります。</p>",
         None),
        ("違約金・途中解約料は0円。学年が上がっても料金は同じ",
         "<p>年会費・保証金・更新費・教師交代費・違約金・途中解約料はすべて0円で、契約期間の縛りもありません。月単位で休会・退会ができ、再開するときは入会金がかかりません。学年が上がっても、受験生になっても、科目を増やしても料金は変わらず、教材を買う必要もありません（映像授業2,000本・ドリル10,000問の学習ツールも追加費用なし）。</p>",
         None),
    ],
    fit=["長い授業だと集中が続かないかもしれない", "学生ではなく、社会人の先生に見てほしい", "発達特性について学んだ先生に教えてほしい", "入会前に、実際に担当する先生と話してみたい", "診断はないが、グレーゾーンかもしれない"],
    check=["授業の振替は同じ月の中で、前日までの連絡が必要", "入会金22,000円（税込）が別にかかる（キャンペーンで無料になる場合あり）", "授業はオンラインのみ（パソコン・タブレット・スマホのいずれか）", "返金保証には条件がある（下のよくある質問）"],
    steps=[("申し込む", "公式サイトのフォーム、公式LINE、電話（0120-907-377）から申し込みます。"),
           ("事前のヒアリング", "教務担当が、学習状況や希望の先生、日時を聞きます。"),
           ("無料体験を2回受ける", "ヒアリングをもとに選ばれた先生が担当。体験後に個別の指導計画とフィードバックを受け取ります。"),
           ("入会を決める", "相性が合えば、体験の先生がそのまま担当します。合わなければ入会しなくて大丈夫です。")],
    steps_src="https://sogaku.jp/online/trial-flow.html",
    form=("無料体験の申込フォームの入力項目", ["お子さんのお名前（必須）", "お子さんのお名前のフリガナ（必須）", "お子さんの学年（必須）", "電話番号（必須）", "メールアドレス（必須）", "体験希望コース：無料体験授業／無料説明会（必須）", "質問・相談・要望（任意）"],
          "https://sogaku.jp/online/trial.html", "公式の申込フォームの表示は「簡単3分」。"),
    shot_trial=("official/sogaku/trial-contents2.png", 1000, 764, "無料体験授業の内容（流れの説明・できる問題・チャレンジ問題・まとめ）", "https://sogaku.jp/online-lp/01/index_i.html"),
    fee=[("小学生", "25分　13,200円", "50分　22,000円"), ("中学生", "35分　18,480円", "60分　26,400円"), ("高校生", "35分　21,560円", "60分　29,920円")],
    fee_note="すべて月4回・税込。入会金22,000円（税込）は別途。保証金・月会費・更新費・教師交代費は0円。科目数による料金アップ、受験生の割増なし。きょうだいの2人目以降は入会金免除、ひとり親家庭は入会金半額。",
    fee_src="https://sogaku.jp/online/fee.html",
    faq=[("診断がついていなくても受けられますか？", "はい。診断がなくても、グレーゾーンでも受講できます。診断名の申告や手帳・受給者証の提出も不要です。"),
         ("集中力が続かなくても大丈夫？", "集中が続きにくい子向けに、小学生は25分、中高生は35分の短いコースがあります。"),
         ("先生が合わなかったら？", "教師の交代は何度でも無料です。担当教師の性別の希望も伝えられます。"),
         ("体験後にしつこく勧誘されませんか？", "公式サイトのよくある質問で、無理な勧誘は一切ないと明記されています。"),
         ("返金保証はありますか？", "授業料1カ月分の全額返金保証があります。入会金は対象外で、初めて利用する家庭（1世帯1回）、初回授業日から30日以内の連絡、最低1回の授業受講などの条件があります。申込前に公式サイトで最新の条件を確認してください。")],
    faq_src="https://sogaku.jp/online/faq.html",
)
DETAIL["runner"] = dict(
    strengths=[
        ("特性に合わせて、教え方・覚え方を変える",
         "<p>ランナーの発達障害サポートには、あえて決まったカリキュラムがありません。集中が続きにくい子には時間を短く区切る、書いて覚えるのが苦手な子には声に出す方法を試す、など特性に合わせて教え方を変える方針です。「発達障害コミュニケーション指導者」の資格を持つスタッフが、担当の先生を指導します。</p>", None),
        ("約14万人の登録から、本部が先生を選ぶ",
         "<p>体験レッスンで作った指導カルテをもとに、本部が10〜20名ほどの先生候補を選び、数名と面談して担当を決めます。指導を始める前に、子どもの特性と接し方を先生に伝えます。合わなければ、先生の交代は何度でも無料です。</p>", None),
        ("1コマ30分900円から。指導した分だけ払う",
         "<p>指導料は1コマ30分あたり、未就学児・小学生・中学生が900円、高校生が1,000円です。指導した分だけの支払いで、体調不良などで休んだ分は差し引かれます。きょうだい同時指導の割引や、ひとり親家庭向けの指導料1カ月無料券もあります。</p>", None),
        ("授業がない日もLINEで質問できる",
         "<p>分からない問題の写真をLINEで送ると、スタッフが解説動画で答えます。保護者も公式LINEで相談でき、本部からも定期的に様子を確認します。オンラインから訪問指導への切り替えもできます。</p>", None),
    ],
    fit=["勉強そのものに苦手意識が強い", "先生の候補が多い中から選んでほしい", "費用を抑えて、少ない回数から始めたい", "オンラインと訪問の両方を候補にしたい"],
    check=["入会金・税込かどうか・最低契約期間・解約の決まりが公式の本体ページに書かれていない（体験時に確認）", "体験レッスン（90分）は学習アドバイザーが担当。担当の先生は申し込み後に選考", "先生紹介のページの先生は大学生・大学院生が中心", "料金は地域によって異なる場合がある"],
    steps=[("体験レッスンを予約", "Webか電話で予約します。土日祝日も受けられます。"),
           ("体験レッスン（90分）", "学習アドバイザーが、学習状況や悩みを親子に聞き、勉強のやり方を伝えます。"),
           ("申し込み", "料金と指導プランを、家庭の希望を聞きながら決めます。"),
           ("先生の選考・研修", "カルテをもとに10〜20名の候補から面接で絞り、指導方法を先生に伝えます。"),
           ("指導開始", "初回は自己紹介や雑談から。合わなければ先生は何度でも無料で交代できます。")],
    steps_src="https://k-runner.co.jp/course/online/",
    faq=[("不登校でも指導してもらえますか？", "はい。不登校の子の指導も多く任されていると公式サイトに書かれています。最初は会話だけで終わる日があってもよい、という方針です。"),
         ("回数や曜日は変えられますか？", "担当の先生と相談して変更できます。指導料は指導した分だけの支払いです。"),
         ("オンライン指導はパソコンで受けたほうがいいですか？", "パソコンやタブレットが推奨です。スマホでも受けられます。"),
         ("先生と合わなかったら？", "オンライン指導でも、先生の交代は何度でも無料です。")],
    faq_src="https://k-runner.co.jp/faq/",
)
DETAIL["tintle"] = dict(
    strengths=[
        ("不登校・行き渋りの子のための個別指導",
         "<p>ティントルは不登校専門のオンライン家庭教師です。不登校のほか、行き渋り、五月雨登校、支援級に通う子、ADHD・ASD・SLDなど特性のある子も対象にしています。前の学年の内容のやり直しから受験対策まで、自分のペースで進められます。</p>", None),
        ("1コマ30分。曜日も回数も固定しない",
         "<p>授業は1コマ30分単位で、受けた分だけの後払いです。慣れるまでは少なめに、しんどい日は休む、という使い方ができます。授業開始1時間前までの連絡なら、当日でもキャンセル料はかかりません。</p>", None),
        ("不登校心理相談士が家庭を支える",
         "<p>講師とは別に、不登校心理相談士の資格を持つ本部スタッフが家庭ごとにつきます。子どもの勉強だけでなく、保護者の悩みにもオンライン面談・LINE・電話で対応します。</p>", None),
        ("自宅学習を出席扱いとして申請できる",
         "<p>オプションの「ホームスクーリングコース」で、ティントルでの学習を学校の出席扱いとして申請できます。</p>", None),
    ],
    fit=["学校に行きづらい日が続いている", "授業の回数を固定したくない", "年の近いお兄さん・お姉さんのような先生がいい", "出席扱いの申請も考えたい"],
    check=["先生は全員が現役の大学生", "最短の授業は30分（25分のような短いコースはない）", "担当の講師が決まるのは入会書類の返送後。担当予定の講師と体験できるという記載はない", "入会金・最低契約期間・解約の決まりが公式サイトに書かれていない", "講師のランク（S〜C）で1コマの料金が変わる"],
    steps=[("個別相談会（約1時間）", "子どもの状況や悩み、目標、希望の予算を伝えます。パソコン・タブレット・スマホで参加できます。"),
           ("プランの提案", "相談の内容をもとに、家庭に合わせたプランと料金が提案されます。"),
           ("子どもの体験（希望制）", "相談会に続けて、または別の日に、指導の仕組みを体験できます。"),
           ("入会・顔合わせ", "Webで手続きし、サポートスタッフ同席で講師と顔合わせ。入会から最短2週間ほどで始められます。")],
    steps_src="https://tintle.net/flow/",
    faq=[("入会したらすぐに授業を始めないといけませんか？", "指導料は受けた分だけの後払いで、回数の制限はありません。入会後にサポートを受けて、やる気が出てから授業を始める生徒もいると公式に書かれています。"),
         ("他社と迷っていても相談できますか？", "はい。個別相談会のあとに期間をおいて考えてもよく、無理な営業はしないと公式に書かれています。"),
         ("授業を休むときは？", "授業開始1時間前までの連絡なら、キャンセル料はかかりません。")],
    faq_src="https://tintle.net/flow/",
)

DETAIL["succeed"] = dict(
    strengths=[
        ("専門スタッフが特性を聞き取ってから始める",
         "<p>特性が強い子の場合は、専門スタッフが保護者と子どもに面談し、学校や家での様子、特性からくる行動を聞き取ります。診断を受けている場合は、差し支えない範囲で検査結果も共有します。担当の先生は、専門スタッフから引き継ぎを受けてから指導を始めます。</p>", None),
        ("発達支援の指導経験が豊富な先生から選ぶ",
         "<p>専任スタッフが特性を聞いたうえで、発達支援の指導経験が豊富な先生から担当を選びます。絵や図で説明する、短い言葉で伝えるなど、その子が学びやすい方法でカリキュラムを組む方針です。</p>", None),
        ("オンラインは毎回の報告と月1回の面談",
         "<p>オンライン家庭教師では、毎回の授業報告とは別に、月に1回の保護者面談があります。先生への要望もこの面談で伝えられます。</p>", None),
        ("月謝制で、退会費・違約金なし",
         "<p>支払いは月謝制で、一括前払いやローン契約ではありません。申込日を含め8日以内なら無条件で解約でき、1カ月前までに伝えれば月末で退会できます。先生の交代は何度でも無料です。</p>", None),
    ],
    fit=["LD・ADHD・ASDなど、特性がある程度分かっている", "発達支援の経験がある先生を選びたい", "授業の様子を毎月聞きながら進めたい", "訪問とオンラインの両方を候補にしたい"],
    check=["オンラインの料金は1時間単位（短い授業の設定は要確認）", "入会後、先生の選考に10営業日ほどかかる", "LD・ADHD・ASDサポートコース（訪問）は1時間5,830円〜"],
    steps=[("問い合わせ", "電話かWebのフォームから問い合わせます。"),
           ("無料体験授業（60分）", "通常と同じ60分の授業を受け、手持ちの機器で授業を受けられるかも確認します。"),
           ("申し込み・先生の指定", "候補の先生の中から選べます。"),
           ("授業スタート", "入会後、先生の選考に10営業日ほどかかります。")],
    steps_src="https://www.benkyo.co.jp/course/online/",
    faq=[("先生が合わなかったら変更できますか？", "はい。講師の変更は無料で何回でもできます。"),
         ("特別な機器は必要ですか？", "普段使っているパソコン・タブレット・スマホのいずれかがあれば受講できます。機器の貸し出しはありません。"),
         ("苦手な科目だけ受講できますか？", "はい。希望の科目だけ受けられ、途中で変えることもできます。")],
    faq_src="https://www.benkyo.co.jp/course/online/",
)
DETAIL["try"] = dict(
    strengths=[
        ("教師とは別に、教育プランナーが専任でつく",
         "<p>トライでは、教師とは別に正社員の「教育プランナー」が家庭ごとにつきます。保護者との面談で悩みや学習状況を聞き、得意・苦手や理解のスピードに合わせたカリキュラムを作ります。先生に直接言いづらい配慮の相談もできます。</p>", None),
        ("WISC検査の結果をもとに学習をサポート",
         "<p>WISCの検査結果をもとに、得意な分野を伸ばし、苦手な部分を無理なくカバーできるよう学習を組み立てます。</p>", None),
        ("カメラオフや保護者同席でも受けられる",
         "<p>子どもが落ち着く場所で受講でき、保護者が同席して見守ることもできます。カメラはオンが推奨ですが、難しければオフでも受講できます。話すのが難しい子は、Zoomのチャットでやりとりすることもできます。</p>", None),
        ("アプリで毎回の授業の進捗が見える",
         "<p>無料の学習管理アプリで、毎回の授業の進捗や教師のコメントを確認できます。教材費は無料で、中高生向けの映像授業「Try IT」も見放題です。</p>", None),
    ],
    fit=["WISCなどの検査結果を勉強に活かしたい", "先生とは別に、相談できる担当者がほしい", "カメラオフや保護者同席から始めたい", "受験や英検の対策も考えている"],
    check=["入会金11,000円（税込）が別にかかる", "料金例は1コマ60分（短い授業は学習面談で要確認）", "体験授業は約30分・英語か数学"],
    steps=[("学習面談の案内", "電話で、無料の学習面談（Zoom）が案内されます。"),
           ("無料学習面談", "教育プランナーが悩みや目標を聞き、コースや学習法、料金を提案します。入会しなくても受けられます。"),
           ("教師決定", "33万人の登録教師から選ばれ、授業の前に教師から挨拶があります。"),
           ("授業スタート", "アプリから自動で発行されるZoomで授業に入ります。")],
    steps_src="https://www.try-online.jp/kobetsu/tokusei/",
    faq=[("発達障がい・学習障がいがあっても入会できますか？", "はい。マンツーマンなので、子どもが理解できるペースで授業を行うと公式に書かれています。不安な場合は入会前の無料体験授業がすすめられています。"),
         ("学習面談は親だけでも受けられますか？", "通常は親子での参加ですが、難しい場合は保護者だけでも面談できます。"),
         ("授業の振り替えはできますか？", "前日22時までの連絡で振り替えられます。")],
    faq_src="https://www.try-online.jp/kobetsu/tokusei/",
)
DETAIL["coaching1"] = dict(
    strengths=[
        ("提携する臨床心理士の発達検査を受けられる",
         "<p>コーチング1グループでは、提携している臨床心理士による発達検査を受けられます。子どもの能力の全体像や得意・不得意を客観的に知り、関わり方の工夫につなげることができます。</p>", None),
        ("発達特性のある子の中学受験・高校受験に対応",
         "<p>発達障害・グレーゾーンの子の多くは、適切な学習指導を行えば中学受験・高校受験が可能だという考えで、進学家庭教師として受験対策を行っています。</p>", None),
        ("「コーチング」で家での学習習慣をつくる",
         "<p>問題の解説だけでなく、子どもの特性や目標に合わせた学習計画を作り、学習を管理しながら家での学習習慣づくりを目指します。先生は独自の研修を受けてから指導に入ります。</p>", None),
        ("毎回の指導報告書と、教務部への相談",
         "<p>授業の終わりに指導報告書で当日の内容を報告します。授業以外のことも教務部に相談でき、教務は担当の先生と毎月の報告書でやりとりしています。</p>", None),
    ],
    fit=["発達特性があっても受験を目指したい", "発達検査で得意・不得意を知りたい", "家での学習習慣までつくってほしい", "1回の授業が長めでも取り組める"],
    check=["授業は1回90分から", "料金は6社で最も高め（月30,690円〜・入会金18,700円・年会費）", "体験学習は自宅での面談が基本で、対象エリアがある"],
    steps=[("資料請求・問い合わせ", "Webか電話で問い合わせます。"),
           ("無料体験学習・カウンセリング（約120分）", "担当教務との面談（授業と相談を含む）で学習状況を分析し、指導案が提案されます。完全予約制です。"),
           ("申し込み", "専属教務が学習計画を立て、子どもに合う先生と料金プランを決めます。"),
           ("指導開始", "申し込み手続き完了の翌月から始まります（15日以降の申し込みは間に合わない場合あり）。")],
    steps_src="https://coaching01.com/starting.html",
    faq=[("体験学習・カウンセリングはどこで受けますか？", "公式の流れでは自宅で行い、対象エリアは東京都・神奈川県・千葉県・埼玉県・愛知県・大阪府・京都府・兵庫県・奈良県です。エリア外でオンラインを希望する場合は、問い合わせ時に確認してください。"),
         ("教材費はかかりますか？", "教材費・ファイル代などはかからず、教材は市販のものをすすめる方針です。"),
         ("料金はいくらですか？", "入会金18,700円（税込）、週1回90分〜で月30,690円〜（税込）、別途申込期間に応じた年会費があります。")],
    faq_src="https://coaching01.com/price.html",
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
<p class="rk-rankline">当サイトのランキング：<b>第{s["rank"]}位</b>（総合評価 {s["total"]}／5）<a href="./#rank-{s['id']}">ランキングで見る</a></p>
"""
    # 強み
    names = [t for t, _, _ in d["strengths"]]
    o += f'\n<!-- F-4 番号つき目次（yk-order）→ F-5 番号ラベルつき見出し（yk-numh）→ F-3 公式画面（yk-shot） -->\n<h2 class="yk-sec-ttl">{esc(s["short"])}の<em>強み</em></h2>\n{order_box(s["short"] + "の強み", "強み", names, "s")}\n'
    for i, (t, body, img) in enumerate(d["strengths"], 1):
        o += f'<h3 class="yk-numh" id="s{i}"><span>強み{i}</span>{esc(t)}</h3>\n{body}\n'
        if img:
            o += shot(img) + "\n"
    o += f'<p class="yk-small">※出典：<a href="{s["official"]}" target="_blank" rel="nofollow noopener">{esc(s["short"])}公式サイト</a>ほか（{CHECKED}確認）。</p>\n{btn_main(s, "detail_strength")}\n'
    # こんな方に
    fit = "".join(f"<li>{esc(t)}</li>" for t in d["fit"])
    chk = "".join(f"<li>{esc(t)}</li>" for t in d["check"])
    o += f"""
<!-- F-6 チェックの箱（yk-listbox）：公式の対象・強みから書く。感想で作らない -->
<h2 class="yk-sec-ttl">{esc(s["short"])}が<em>向いている家庭</em></h2>
<div class="yk-listbox"><p class="yk-listbox__ttl">こんな家庭に向いています</p><ul>{fit}</ul></div>
<div class="yk-listbox"><p class="yk-listbox__ttl">申し込む前に確認したいこと</p><ul>{chk}</ul></div>
{btn_main(s, "detail_fit")}
"""
    # 料金
    if "fee" in d:
        rows = "".join(f"<tr><th>{g}</th><td>{a}</td><td>{b}</td></tr>" for g, a, b in d["fee"])
        o += f"""
<h2 class="yk-sec-ttl">{esc(s["short"])}の<em>料金</em></h2>
<table class="rk-fee"><tr><th>学年</th><th>短いコース</th><th>長いコース</th></tr>{rows}</table>
<p class="yk-small">※{d["fee_note"]} 出典：<a href="{d["fee_src"]}" target="_blank" rel="nofollow noopener">公式サイト</a>（{CHECKED}確認）</p>
"""
    else:
        o += f'\n<h2 class="yk-sec-ttl">{esc(s["short"])}の<em>料金</em></h2>\n{jobex(s)}\n'
    o += btn_main(s, "detail_fee") + "\n"
    # 手順
    steps = [t for t, _ in d["steps"]]
    o += f'\n<h2 class="yk-sec-ttl">無料体験・<em>申し込みの流れ</em></h2>\n{order_box("申し込みの流れ", "ステップ", steps, "f")}\n'
    for i, (t, body) in enumerate(d["steps"], 1):
        o += f'<h3 class="yk-numh" id="f{i}"><span>ステップ{i}</span>{esc(t)}</h3>\n<p>{esc(body)}</p>\n'
        if k == "sogaku" and i == 3:
            o += shot(d["shot_trial"]) + "\n"
    if "form" in d:
        ttl, items, src, note = d["form"]
        lis = "".join(f"<li>{esc(t)}</li>" for t in items)
        o += f'<div class="yk-listbox"><p class="yk-listbox__ttl">{esc(ttl)}</p><ul>{lis}</ul></div>\n<p class="yk-small">※{note}出典：<a href="{src}" target="_blank" rel="nofollow noopener">公式サイトの申込フォーム</a>（{CHECKED}確認）。広告のリンク先のページでは項目が異なる場合があります。</p>\n'
    o += f'<p class="yk-small">※流れの出典：<a href="{d["steps_src"]}" target="_blank" rel="nofollow noopener">{esc(s["short"])}公式サイト</a>（{CHECKED}確認）。</p>\n{btn_main(s, "detail_flow")}\n'
    # 口コミ
    if s["voices"]:
        o += f'\n<h2 class="yk-sec-ttl">{esc(s["short"])}の<em>口コミ・評判</em></h2>\n{voices(s)}\n{btn_main(s, "detail_voice")}\n'
    # FAQ
    qs = [q for q, _ in d["faq"]]
    o += f'\n<h2 class="yk-sec-ttl">よくある<em>質問</em></h2>\n{order_box("よくある質問", "質問", qs, "q")}\n'
    for i, (q, a) in enumerate(d["faq"], 1):
        o += f'<h3 class="yk-numh" id="q{i}"><span>質問{i}</span>{esc(q)}</h3>\n<p>{esc(a)}</p>\n'
    o += f'<p class="yk-small">※出典：<a href="{d["faq_src"]}" target="_blank" rel="nofollow noopener">{esc(s["short"])}公式サイト</a>（{CHECKED}確認）。</p>\n{btn_main(s, "detail_faq")}\n'
    if s["operator"]:
        o += f'<p class="yk-small">運営会社：{esc(s["operator"])}（公式サイトの表記）。当サイトは{esc(s["short"])}と広告契約をしていません。</p>\n'
    o += '<p class="rk-back"><a href="./#ranking">ランキングに戻る</a></p>\n'
    return o + end()


# ---------------------------------------------------------------- 調査概要
def method():
    R = [S[k] for k in RANK]
    crit = [
        ("support", "発達特性への対応", ["5：サービス全体が発達障害・グレーゾーン専門で、外部の専門家・専門機関が関わる仕組み（先生の研修、指導計画のシートなど）を公表", "4：発達特性・不登校向けのコースや支援があり、特性を聞き取る専任・有資格のスタッフの関与を公表", "3：発達特性のある子も受講できると記載"]),
        ("teacher", "先生の体制", ["5：担当する先生全員が、発達特性についての専門研修を受けていると公表", "4：特性を聞いたうえで、指導前に特性に合わせた研修をする、または発達特性を扱う講師研修を公表", "3：講師研修や、不登校・特性の指導経験がある先生の在籍を公表"]),
        ("trial", "入会前に確かめられること", ["5：入会後に担当する予定の先生による無料体験を、公式に明記", "4：子どもが受けられる無料の体験授業・体験レッスンがある（担当は先生以外のスタッフ）", "3：保護者との無料相談が中心で、子どもの体験は希望制・内容が限られる"]),
        ("time", "短い時間から始められるか", ["5：1回30分未満の授業を選べる", "4：30分から（30分単位を含む）", "3：1回60分から", "2：1回90分から"]),
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
<li>方法：各社の公式サイトを{CHECKED}に確認（料金・授業時間・先生・研修・体験・保護者サポート・費用と契約・よくある質問）。口コミサイトや利用者アンケートの点数は使っていません</li>
<li>広告：ソウガクのみアフィリエイト広告の契約があります。順位は契約の有無ではなく、下の基準で決めています</li></ul>
<h2 class="yk-sec-ttl">採点の基準（各5点満点）</h2>
<table class="yk-cmp rk-cmp-text rk-crit">{rows}</table>
<h2 class="yk-sec-ttl">総合評価・星・記号の決め方</h2>
<ul class="rk-list"><li>総合評価：{len(AXES)}項目の点数の平均（小数第2位を四捨五入）</li>
<li>星：総合評価を四捨五入した数（例：4.9→★5、4.0→★4、3.7→★4）</li>
<li>総合評価のランク：S＝4.5以上、A＝4.0以上、B＝4.0未満</li>
<li>同点のとき：「発達特性への対応」→「先生の体制」→小学生の月額の目安が安い順</li>
<li>比較表の◎○△×：5点＝◎、4点＝○、3点・2点＝△、1点＝×</li></ul>
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

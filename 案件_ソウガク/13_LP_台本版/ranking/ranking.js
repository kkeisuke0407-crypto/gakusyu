/* yk-finder（オンライン家庭教師かんたん診断）の判定。
   点数は各社公式サイトの記載（2026-10-14確認）で決められる条件だけ。入力内容は送信・保存しない。 */
(function () {
  'use strict';
  var form = document.getElementById('finder');
  var out = document.getElementById('finder-result');
  if (!form || !out) return;
  var SV = {
    sogaku: { name: 'ソウガク', base: 4.8 },
    runner: { name: '家庭教師のランナー', base: 4.2 },
    tintle: { name: 'ティントル', base: 4.2 },
    succeed: { name: '家庭教師のサクシード', base: 4.0 },
    'try': { name: 'トライのオンライン個別指導塾', base: 4.0 },
    coaching1: { name: '家庭教師のコーチング1', base: 3.5 }
  };
  // [条件, 会社, 点, 理由]
  var RULES = [
    ['grade:pre', 'runner', 3, '未就学児から指導している'],
    ['concern:focus', 'sogaku', 3, '集中が続きにくい子向けに小学生25分のコースがある'],
    ['concern:focus', 'tintle', 2, '1コマ30分単位で受けられる'],
    ['concern:focus', 'runner', 1, '集中が続きにくい子には時間を短く区切る方針'],
    ['concern:school', 'tintle', 3, '不登校専門。出席扱いの申請ができるコースもある'],
    ['concern:school', 'runner', 1, '不登校の子の指導も多いと公式に記載'],
    ['concern:school', 'try', 1, '受講が在籍校で出席と認定された実績があると公式に記載'],
    ['concern:exam', 'coaching1', 3, '発達特性のある子の中学・高校受験に対応'],
    ['concern:exam', 'runner', 1, '定期テスト対策から受験指導まで対応'],
    ['concern:exam', 'try', 1, '受験・英検の対策にも対応'],
    ['concern:cost', 'runner', 2, '1コマ30分900円から、指導した分だけの支払い'],
    ['concern:cost', 'tintle', 2, '受けた分だけの後払い（小学生は1コマ30分1,320円〜）'],
    ['concern:cost', 'succeed', 1, 'オンラインは月会費・交通費がかからない'],
    ['concern:match', 'sogaku', 3, '入会後に担当する予定の先生と無料体験を2回受けられる'],
    ['concern:match', 'runner', 1, '約14万人の登録から本部が先生を選び、交代は何度でも無料'],
    ['length:short', 'sogaku', 2, '小学生25分・中高生35分から選べる'],
    ['length:short', 'tintle', 2, '1コマ30分'],
    ['length:mid', 'succeed', 1, 'オンラインは1時間単位'],
    ['length:mid', 'try', 1, '料金例は1コマ60分'],
    ['length:long', 'coaching1', 1, '1回90分から'],
    ['report', 'sogaku', 1, '授業のたびに指導報告が届く'],
    ['report', 'succeed', 1, '毎回の授業報告と月1回の保護者面談'],
    ['report', 'coaching1', 1, '毎回の指導報告書'],
    ['report', 'try', 1, '学習管理アプリで毎回の進捗が見える'],
    ['flex', 'tintle', 2, '曜日・時間・回数を固定しない'],
    ['flex', 'runner', 1, '回数・時間は先生と相談して変えられる'],
    ['visit', 'runner', 2, 'オンラインから訪問指導に切り替えられる'],
    ['visit', 'succeed', 1, '訪問の家庭教師もある'],
    ['visit', 'coaching1', 1, '訪問指導もある（対象エリアあり）'],
    ['test', 'try', 2, 'WISC検査の結果をもとに学習をサポート'],
    ['test', 'coaching1', 2, '提携する臨床心理士の発達検査を受けられる']
  ];
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var on = {};
    ['grade', 'concern', 'length'].forEach(function (n) { var v = form.elements[n].value; if (v) on[n + ':' + v] = true; });
    ['report', 'flex', 'visit', 'test'].forEach(function (n) { if (form.elements[n].checked) on[n] = true; });
    var score = {}, why = {};
    Object.keys(SV).forEach(function (k) { score[k] = 0; why[k] = []; });
    RULES.forEach(function (r) { if (on[r[0]]) { score[r[1]] += r[2]; why[r[1]].push(r[3]); } });
    var keys = Object.keys(SV).sort(function (a, b) { return (score[b] - score[a]) || (SV[b].base - SV[a].base); });
    var top = keys.slice(0, 2);
    var anyRule = Object.keys(on).length > 0;
    var h = '<p class="rk-result__ttl">' + (anyRule ? '条件に合いやすいのはこの2社' : '条件を選ぶと絞り込めます。いまは総合評価の上位2社') + '</p><ol>';
    top.forEach(function (k, i) {
      var reasons = why[k].length ? why[k] : ['総合評価 ' + SV[k].base + '（ランキング' + (keys.indexOf(k) + 1) + '位）'];
      h += '<li><b>' + (i + 1) + '. ' + SV[k].name + '</b><ul>' + reasons.map(function (t) { return '<li>' + t + '</li>'; }).join('') + '</ul><a href="' + k + '.html">' + SV[k].name + 'の詳細を見る</a></li>';
    });
    out.innerHTML = h + '</ol>';
    out.hidden = false;
    out.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  });
})();

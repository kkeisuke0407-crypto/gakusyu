/* yk-finder（オンライン家庭教師かんたん診断）の判定。
   点数は各社公式サイトの記載（2026-10-17確認）で決められる条件だけ。入力内容は送信・保存しない。 */
(function () {
  'use strict';
  var form = document.getElementById('finder');
  var out = document.getElementById('finder-result');
  if (!form || !out) return;
  var SV = {
    sogaku: { name: 'ソウガク', base: 4.9 },
    rebalance: { name: 'オンライン個別指導塾リバランス', base: 4.0 },
    'try': { name: 'トライのオンライン個別指導塾', base: 4.0 },
    coaching1: { name: '個別指導のコーチング1', base: 3.9 },
    tos: { name: 'TOS家庭教師センター', base: 3.9 },
    kizuki: { name: 'キズキ共育塾', base: 3.4 }
  };
  // [条件, 会社, 点, 理由]
  var RULES = [
    ['grade:pre', 'coaching1', 2, '年長から対象（オンライン指導も全学年）'],
    ['grade:pre', 'tos', 2, '幼児から対象'],
    ['grade:hs', 'kizuki', 1, '大学受験・高卒認定まで対応'],
    ['grade:hs', 'tos', 1, '高校生・高卒認定にも対応'],
    ['concern:focus', 'sogaku', 3, '集中が続きにくい子向けに小学生25分のコースがある'],
    ['concern:focus', 'kizuki', 1, '1回50分から受けられる'],
    ['concern:focus', 'rebalance', 1, 'ADHDの子には指示や課題を細かく分ける方針'],
    ['concern:match', 'sogaku', 3, '入会後に担当する予定の先生と無料体験を2回受けられる'],
    ['concern:match', 'tos', 2, '実際に担当する家庭教師が無料体験を行う（オンラインでも同じかは要確認）'],
    ['concern:match', 'kizuki', 1, '講師・科目の変更は無料'],
    ['concern:nodiag', 'sogaku', 3, '診断なし・グレーゾーンでも受講でき、手帳の提出も不要と明記'],
    ['concern:nodiag', 'rebalance', 2, '確定診断のないグレーゾーンの子のほうが多いと記載'],
    ['concern:nodiag', 'coaching1', 1, '診断・発達検査がなくても指導すると記載'],
    ['concern:school', 'kizuki', 3, '不登校の学び直しが中心。出席扱いの相談もできる'],
    ['concern:school', 'tos', 2, '不登校からの受験・高卒認定に対応'],
    ['concern:school', 'try', 1, '受講が在籍校で出席と認定された実績があると公式に記載'],
    ['concern:school', 'sogaku', 1, '午前中の授業にも対応'],
    ['concern:school', 'rebalance', 1, '不登校でも指導できると記載'],
    ['concern:exam', 'coaching1', 3, '発達特性のある子の中学・高校受験に対応'],
    ['concern:exam', 'rebalance', 2, '特性に合わせて中学受験・高校受験の対策をすると記載'],
    ['concern:exam', 'try', 1, '受験・英検の対策にも対応'],
    ['concern:exam', 'sogaku', 1, '中学生コースは受験対策にも対応。受験生の割増なし'],
    ['concern:exam', 'tos', 1, '不登校からの高校・大学受験に対応'],
    ['concern:cost', 'sogaku', 2, '小学生25分×月4回 13,200円（税込）から。6社で月額の目安がいちばん低い'],
    ['concern:cost', 'try', 2, '60分×月4回 14,960円（税込）から'],
    ['concern:cost', 'tos', 1, 'オンライン60分×月4回 19,400円（税込）から。テキスト代・管理費なし'],
    ['length:short', 'sogaku', 2, '小学生25分・中高生35分から選べる'],
    ['length:mid', 'sogaku', 1, '小学生50分・中高生60分のコース'],
    ['length:mid', 'try', 1, '料金例は1コマ60分'],
    ['length:mid', 'rebalance', 1, '1回60分から'],
    ['length:mid', 'coaching1', 1, 'オンラインは60分から'],
    ['length:mid', 'tos', 1, 'オンラインは60分から'],
    ['length:long', 'coaching1', 2, '60分・90分・120分から選べる'],
    ['length:long', 'tos', 1, 'オンラインは90分のコースもある'],
    ['length:long', 'kizuki', 1, '80分のコースもある'],
    ['report', 'sogaku', 2, '授業のたびにアプリで指導報告が届く'],
    ['report', 'rebalance', 2, '授業後に毎回フィードバックがある'],
    ['report', 'coaching1', 1, '毎回の指導報告書'],
    ['report', 'try', 1, '学習管理アプリで毎回の進捗が見える'],
    ['adult', 'sogaku', 3, '先生は全員が社会人'],
    ['adult', 'rebalance', 1, 'プロ講師（社会人・有資格の学生）中心の体制'],
    ['adult', 'tos', 1, 'オンライン用のプロコースがある'],
    ['contract', 'sogaku', 3, '違約金・途中解約料0円、月単位で休会・退会できると明記'],
    ['contract', 'tos', 2, '解約金・違約金なし。1か月単位の契約'],
    ['contract', 'kizuki', 1, '休会・退会・入会キャンセルの決まりを規約に明記'],
    ['flex', 'sogaku', 1, '回数・時間を月ごとに変えられる'],
    ['flex', 'kizuki', 1, '前日までの連絡で授業日時を無料で変えられる'],
    ['flex', 'tos', 1, 'テスト前だけ回数を増やせる']
  ];
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var on = {};
    ['grade', 'concern', 'length'].forEach(function (n) { var v = form.elements[n].value; if (v) on[n + ':' + v] = true; });
    ['report', 'adult', 'contract', 'flex'].forEach(function (n) { if (form.elements[n].checked) on[n] = true; });
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

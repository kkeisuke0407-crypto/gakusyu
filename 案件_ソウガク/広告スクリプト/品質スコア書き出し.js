/**
 * ソウガク｜品質スコアをスプレッドシートへ書き出す Google 広告スクリプト（読み取り専用）
 *
 * 書き出し先：「ソウガク PPC広告運用 CPA分析」に2つのタブを作って毎回上書きする（既存のタブには触らない）
 *   - 品質スコア_KW：キーワードごとの 品質スコア／LPの利便性／広告の関連性／推定クリック率＋直近30日の実績＋広告の最終URL
 *   - 品質スコア_AG：広告グループごとに「LPの利便性」の内訳（表示回数で重み付け）
 * 広告・入札・予算は一切変更しない（AdsApp.search で読むだけ）。
 *
 * 設置：Google 広告（ソウガクのアカウント）→ ツール → 一括操作 → スクリプト → ＋ → このファイルを貼り付け
 *       → 承認 → プレビューで確認 → 実行 → 頻度「毎日」（午前6時ごろ）
 */

var CONFIG = {
  SPREADSHEET_ID: '1CKnCHEP6gzprB5ixF-FrYc4KlwLk7XzstuC1OYqEp0M',
  KW_TAB: '品質スコア_KW',
  AG_TAB: '品質スコア_AG',
  // 対象キャンペーン名（完全一致）。空にするとアカウント内の全キャンペーン
  CAMPAIGN_NAMES: ['①王道', '②その他ジャンル', '③競合', '④テール'],
  DATE_RANGE: 'LAST_30_DAYS'
};

var LEVEL = { ABOVE_AVERAGE: '平均より上', AVERAGE: '平均的', BELOW_AVERAGE: '平均より下' };
var MATCH = { EXACT: '完全一致', PHRASE: 'フレーズ一致', BROAD: '部分一致' };
var STATUS = { ENABLED: '有効', PAUSED: '停止' };

function main() {
  var cpWhere = "campaign.status != 'REMOVED' AND ad_group.status != 'REMOVED'";
  if (CONFIG.CAMPAIGN_NAMES.length) {
    cpWhere += ' AND campaign.name IN (' + CONFIG.CAMPAIGN_NAMES.map(function (n) { return "'" + n.replace(/'/g, "\\'") + "'"; }).join(', ') + ')';
  }
  var where = cpWhere + " AND ad_group_criterion.status != 'REMOVED' AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE";

  // 1) 全キーワードの品質（実績がないキーワードも含める）
  var kws = {};
  var order = [];
  var it = AdsApp.search(
    'SELECT campaign.name, ad_group.id, ad_group.name, ad_group_criterion.criterion_id, ' +
    'ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status, ' +
    'ad_group_criterion.final_urls, ad_group_criterion.quality_info.quality_score, ' +
    'ad_group_criterion.quality_info.post_click_quality_score, ad_group_criterion.quality_info.creative_quality_score, ' +
    'ad_group_criterion.quality_info.search_predicted_ctr ' +
    'FROM ad_group_criterion WHERE ' + where);
  while (it.hasNext()) {
    var r = it.next();
    var c = r.adGroupCriterion;
    var q = c.qualityInfo || {};
    var key = r.adGroup.id + '~' + c.criterionId;
    kws[key] = {
      campaign: r.campaign.name, adGroupId: r.adGroup.id, adGroup: r.adGroup.name,
      keyword: c.keyword.text, match: MATCH[c.keyword.matchType] || c.keyword.matchType, status: STATUS[c.status] || c.status,
      qs: q.qualityScore || '', lp: LEVEL[q.postClickQualityScore] || '—', ad: LEVEL[q.creativeQualityScore] || '—',
      ctr: LEVEL[q.searchPredictedCtr] || '—', kwUrl: (c.finalUrls || []).join(' '),
      imp: 0, clk: 0, cost: 0
    };
    order.push(key);
  }

  // 2) 直近30日の実績
  var mt = AdsApp.search(
    'SELECT ad_group.id, ad_group_criterion.criterion_id, metrics.impressions, metrics.clicks, metrics.cost_micros ' +
    'FROM keyword_view WHERE segments.date DURING ' + CONFIG.DATE_RANGE + ' AND ' + where);
  while (mt.hasNext()) {
    var m = mt.next();
    var k = kws[m.adGroup.id + '~' + m.adGroupCriterion.criterionId];
    if (!k) continue;
    k.imp += Number(m.metrics.impressions || 0);
    k.clk += Number(m.metrics.clicks || 0);
    k.cost += Number(m.metrics.costMicros || 0) / 1e6;
  }

  // 3) 広告グループごとの広告の最終URL（キーワードに最終URLがない場合はこちらが着地先）
  var adUrls = {};
  var at = AdsApp.search(
    "SELECT ad_group.id, ad_group_ad.ad.final_urls FROM ad_group_ad WHERE ad_group_ad.status = 'ENABLED' AND " + cpWhere);
  while (at.hasNext()) {
    var a = at.next();
    var set = adUrls[a.adGroup.id] = adUrls[a.adGroup.id] || {};
    (a.adGroupAd.ad.finalUrls || []).forEach(function (u) { set[u] = true; });
  }

  // 4) 書き出し
  var ss = SpreadsheetApp.openById(CONFIG.SPREADSHEET_ID);
  var now = Utilities.formatDate(new Date(), AdsApp.currentAccount().getTimeZone(), 'yyyy/MM/dd HH:mm');

  var kwRows = order.map(function (key) {
    var k = kws[key];
    var url = k.kwUrl || Object.keys(adUrls[k.adGroupId] || {}).join(' ');
    return [k.campaign, k.adGroup, k.keyword, k.match, k.status, k.qs, k.lp, k.ad, k.ctr, k.imp, k.clk, Math.round(k.cost), url];
  });
  kwRows.sort(function (x, y) { return y[9] - x[9]; }); // 表示回数の多い順
  writeTab(ss, CONFIG.KW_TAB, [
    ['更新', now, '期間', CONFIG.DATE_RANGE, '品質の値は現時点のもの。表示回数が少ないキーワードは「—」（未評価）'],
    [],
    ['キャンペーン', '広告グループ', 'キーワード', 'マッチ', '状態', '品質スコア', 'LPの利便性', '広告の関連性', '推定クリック率', '表示回数(30日)', 'クリック(30日)', '費用(30日)', '着地先URL']
  ].concat(kwRows));

  // 広告グループ集計：LPの利便性を表示回数で重み付け
  var ags = {};
  order.forEach(function (key) {
    var k = kws[key];
    var g = ags[k.adGroupId] = ags[k.adGroupId] || { campaign: k.campaign, adGroup: k.adGroup, n: 0, rated: 0, imp: 0, below: 0, avg: 0, above: 0, none: 0, qsSum: 0, qsImp: 0 };
    g.n++; g.imp += k.imp;
    if (k.lp === LEVEL.BELOW_AVERAGE) g.below += k.imp; else if (k.lp === LEVEL.AVERAGE) g.avg += k.imp; else if (k.lp === LEVEL.ABOVE_AVERAGE) g.above += k.imp; else g.none += k.imp;
    if (k.lp !== '—') g.rated++;
    if (k.qs) { g.qsSum += k.qs * k.imp; g.qsImp += k.imp; }
  });
  var pct = function (a, b) { return b ? Math.round(a / b * 1000) / 10 + '%' : ''; };
  var agRows = Object.keys(ags).map(function (id) {
    var g = ags[id];
    return [g.campaign, g.adGroup, g.n, g.rated, g.imp, pct(g.below, g.imp), pct(g.avg, g.imp), pct(g.above, g.imp), pct(g.none, g.imp),
      g.qsImp ? Math.round(g.qsSum / g.qsImp * 10) / 10 : '', Object.keys(adUrls[id] || {}).join(' ')];
  });
  agRows.sort(function (x, y) { return y[4] - x[4]; });
  writeTab(ss, CONFIG.AG_TAB, [
    ['更新', now, '期間', CONFIG.DATE_RANGE, '割合は表示回数での重み付け。「未評価」は品質がまだ出ていない分'],
    [],
    ['キャンペーン', '広告グループ', 'KW数', 'LP評価ありKW数', '表示回数(30日)', 'LP 平均より下', 'LP 平均的', 'LP 平均より上', 'LP 未評価', '品質スコア(加重平均)', '広告の最終URL']
  ].concat(agRows));

  Logger.log('キーワード ' + kwRows.length + ' 件、広告グループ ' + agRows.length + ' 件を書き出しました');
}

function writeTab(ss, name, rows) {
  var sh = ss.getSheetByName(name) || ss.insertSheet(name);
  sh.clearContents();
  var width = rows.reduce(function (w, r) { return Math.max(w, r.length); }, 1);
  var data = rows.map(function (r) { var x = r.slice(); while (x.length < width) x.push(''); return x; });
  sh.getRange(1, 1, data.length, width).setValues(data);
  sh.setFrozenRows(3);
  sh.getRange(3, 1, 1, width).setFontWeight('bold');
}

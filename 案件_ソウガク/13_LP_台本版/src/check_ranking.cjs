// TOP3比較・ランキング版（/ranking/）の公開前チェック。1つでもNGなら終了コード1（publish.sh が止まる）
//   NODE_PATH=$(npm root -g) node src/check_ranking.cjs
// 見ること：375px・1280pxで横はみ出しなし／画像が読める・alt・width・height／パーツ集の見本の残り（#sample・yk-ph・◯・サービスA・画像指示枠）なし／
// 使うと決めたパーツが使われている／レーダー3つ／診断フォームで結果が出る
// 2026-10-16 ユーザー指示で外した部品：fv-1 yk-hero（→ヒーロー画像 lp-hero）、fv-2 ロゴの横流し・image-2 導入画像（FV直下は画像なしの会話）
const path = require('path');
const { chromium } = require('playwright');
const DIR = 'file://' + path.resolve(__dirname, '..', 'ranking') + '/';
const PAGES = ['index', 'sogaku', 'rebalance', 'try', 'coaching1', 'tos', 'kizuki', 'method'];
// パーツ集の29部品（image-1 の画像指示枠 mt-imgslot は制作中だけ使い、公開ページに残してはいけない）
const PARTS = {
  'FV ヒーロー画像': '.lp-hero--text img', 'FV 見える見出し': '.lp-hero--text h1.lp-hero__ttl', '導入会話': '.lp-hero ~ .mt-talk', 'fv-3 PR表記': '.yk-pr', 'top-1 BEST3': '.yk-best3', 'top-2 求人の例カード': '.yk-hscroll .yk-jobcard',
  'compare-1 タブ切替の比較表': '.yk-tabs .yk-cmp, .yk-fold', 'compare-2 2軸の早見表': '.yk-matrix', 'compare-3 2社併用': '.yk-combo',
  'rank-1 順位見出し': '.yk-rankhead', 'rank-2 ランキング内のタブ': '.yk-rankarea .yk-tabs', 'rank-3 特徴': '.yk-features', 'rank-4 編集部': '.yk-editor',
  'rank-5 口コミ': '.yk-voice', 'rank-6 2ボタン': '.yk-btnpair', 'rank-7 レーダー': '.yk-radar svg', 'rank-8 基本情報の表': '.yk-info', 'rank-9 求人例カード': '.yk-jobex',
  'close-1 迷ったらまずは': '.yk-pickup', 'close-2 診断': '.yk-finder', 'close-3 フッター': '.yk-footer',
  'detail-1 パンくず': '.yk-crumb', 'detail-2 サービス概要': '.yk-svchead__grid', 'detail-3 公式画面': '.yk-shot', 'detail-4 目次ボックス': '.yk-order',
  'detail-5 番号見出し': '.yk-numh', 'detail-6 チェックの箱': '.yk-listbox', 'detail-7 登録ボタン': 'main > .yk-btn',
};
const NG = ['#sample', 'yk-ph', '◯', 'サービスA', 'mt-imgslot', '薬剤師', '求人', 'undefined', 'None', 'NaN'];
(async () => {
  const b = await chromium.launch();
  const fails = [];
  const found = {};
  for (const w of [375, 1280]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } });
    const errs = [];
    p.on('pageerror', e => errs.push(e.message));
    for (const n of PAGES) {
      await p.goto(DIR + n + '.html', { waitUntil: 'load' });
      await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 20)); } window.scrollTo(0, 0); });
      await p.waitForTimeout(300);
      const r = await p.evaluate(([NG, PARTS]) => {
        const html = document.documentElement.outerHTML;
        const imgs = [...document.images];
        const parts = {};
        for (const [k, sel] of Object.entries(PARTS)) parts[k] = document.querySelectorAll(sel).length;
        return {
          over: document.documentElement.scrollWidth - document.documentElement.clientWidth,
          ng: NG.filter(s => html.includes(s)),
          attrs: imgs.filter(i => !i.hasAttribute('alt') || !i.getAttribute('width') || !i.getAttribute('height')).map(i => i.src.split('/').pop()),
          broken: imgs.filter(i => !i.src.includes('felmat') && i.complete && i.naturalWidth === 0).map(i => i.src.split('/').pop()),
          localRefs: imgs.map(i => i.getAttribute('src')).filter(s => !/^https?:/.test(s)),
          radar: document.querySelectorAll('.yk-radar').length, radarSvg: document.querySelectorAll('.yk-radar svg').length,
          parts,
        };
      }, [NG, PARTS]);
      const tag = `${w}px ${n}`;
      if (r.over > 0) fails.push(`${tag}: 横はみ出し ${r.over}px`);
      if (r.ng.length) fails.push(`${tag}: 見本・仮の文字が残っている ${r.ng.join(' ')}`);
      if (r.attrs.length) fails.push(`${tag}: alt/width/heightのない画像 ${r.attrs.join(' ')}`);
      if (r.broken.length) fails.push(`${tag}: 読めない画像 ${r.broken.join(' ')}`);
      if (r.radar !== r.radarSvg) fails.push(`${tag}: レーダーが描けていない ${r.radarSvg}/${r.radar}`);
      for (const [k, v] of Object.entries(r.parts)) found[k] = (found[k] || 0) + v;
      // 横スクロール内の画像（lazy）は表示前なので、ファイルの有無はローカルで確かめる
      for (const s of r.localRefs) {
        const f = path.resolve(__dirname, '..', 'ranking', s);
        if (!require('fs').existsSync(f)) fails.push(`${tag}: 画像ファイルがない ${s}`);
      }
      if (n === 'index') {
        if (r.radarSvg !== 6) fails.push(`${tag}: レーダーは6社ぶん必要（${r.radarSvg}）`);
        // FVの見出しは画面に見えるH1（広告の品質：キーワードと見出しの一致）。1つだけ・見えている・キーワードを含む
        const h1 = await p.evaluate(() => { const hs = [...document.querySelectorAll('h1')]; const h = hs[0]; const r = h && h.getBoundingClientRect(); return { n: hs.length, w: r ? r.width : 0, text: h ? h.innerText.replace(/\s+/g, '') : '' }; });
        if (h1.n !== 1 || h1.w < 100 || !/発達障害.*オンライン家庭教師.*ランキング/.test(h1.text)) fails.push(`${tag}: 見えるH1がない・キーワード不足 ${JSON.stringify(h1)}`);
        await p.selectOption('#finder select[name=concern]', 'focus');
        await p.selectOption('#finder select[name=length]', 'short');
        await p.click('#finder button[type=submit]');
        const res = await p.evaluate(() => { const o = document.getElementById('finder-result'); return { hidden: o.hidden, first: (o.querySelector('li b') || {}).textContent || '', links: [...o.querySelectorAll('a')].map(a => a.getAttribute('href')) }; });
        if (res.hidden || !/ソウガク/.test(res.first) || res.links.length !== 2) fails.push(`${tag}: 診断の結果が出ない・想定と違う ${JSON.stringify(res)}`);
        await p.click('label[for=cmp1-more]');
        const rows = await p.evaluate(() => document.querySelectorAll('#cmp1-more ~ .yk-fold__body tr').length);
        if (rows !== 7) fails.push(`${tag}: 比較表の行数 ${rows}（見出し＋6社）`);
      }
    }
    if (errs.length) fails.push(`${w}px: スクリプトのエラー ${errs.join(' / ')}`);
    await p.close();
  }
  for (const [k, v] of Object.entries(found)) if (!v) fails.push(`パーツ未使用：${k}`);
  await b.close();
  console.log(`パーツ使用数（全ページ・2幅の合計）：${Object.entries(found).map(([k, v]) => `${k.split(' ')[0]}=${v / 2}`).join(' ')}`);
  if (fails.length) { console.log('NG\n  ' + fails.join('\n  ')); process.exit(1); }
  console.log(`OK（${PAGES.length}ページ × 375/1280px）`);
})();

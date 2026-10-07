/* ソウガクLPの公開前チェック（王道LP・サブLPの全ページ）
 *   NODE_PATH=$(npm root -g) node src/check_pages.cjs
 * 13_LP_台本版/ をローカルで配信し、スマホ（375×667）とPC（1280×800）で次を確認する。
 *   - 比較表（#compare）より前にCTA・リンクがない（追従CTAは除く）
 *   - 追従CTAは、最初にスクロールした時点では出ず、比較表を過ぎてから出る
 *   - 画像切れ・横はみ出し・JSエラーがない
 *   - 大見出し（h2.mt-h2）がスマホで2行以内
 *   - サブLPに「3つのポイント」「3つの選定基準」が残っていない
 * 1つでも引っかかれば終了コード1。
 */
const http = require('http');
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const PAGES = ['index.html', 'lp02/index.html', 'lp03/index.html'].filter(p => fs.existsSync(path.join(ROOT, p)));
const SIZES = [[375, 667], [1280, 800]];
const TYPES = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml' };
const CHROME = fs.existsSync('/opt/pw-browsers/chromium-1194/chrome-linux/chrome') ? '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' : undefined;

const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]);
  if (p.endsWith('/')) p += 'index.html';
  const f = path.join(ROOT, p);
  if (!f.startsWith(ROOT) || !fs.existsSync(f)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
});

(async () => {
  await new Promise(r => server.listen(0, r));
  const base = `http://localhost:${server.address().port}/`;
  const browser = await chromium.launch({ executablePath: CHROME });
  const ng = [];
  for (const page of PAGES) {
    const sub = page !== 'index.html';
    for (const [w, h] of SIZES) {
      const p = await browser.newPage({ viewport: { width: w, height: h } });
      const errs = [];
      p.on('pageerror', e => errs.push(e.message));
      await p.goto(base + page.replace('index.html', ''), { waitUntil: 'load' });
      await p.waitForTimeout(300);
      // 追従CTA：600pxずつホイールでスクロールし、比較表より前では出ず、最初のCTA（#cta-first）を過ぎたら出るか
      const pos = await p.evaluate(() => { const y = id => { const e = document.getElementById(id); return e ? e.getBoundingClientRect().top + scrollY : 0; }; return { cy: y('compare'), ctaY: y('cta-first'), H: document.documentElement.scrollHeight }; });
      let early = false, late = false;
      for (let yy = 0; yy < pos.H; yy += 600) {
        await p.mouse.wheel(0, 600); await p.waitForTimeout(120);
        const st = await p.evaluate(() => ({ y: scrollY, s: document.querySelector('.mt-sticky')?.classList.contains('is-show') }));
        if (st.y + h < pos.cy && st.s) early = true;
        if (st.y > pos.ctaY + 300 && st.s) late = true;
      }
      await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(300);
      // 遅延読み込みの画像も読ませるため、最後までスクロールしてから戻る
      await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo(0, y); await new Promise(r => setTimeout(r, 30)); } scrollTo(0, 0); });
      await p.waitForTimeout(500);
      const r = await p.evaluate((sub) => {
        const top = el => el.getBoundingClientRect().top + scrollY;
        const cmp = document.getElementById('compare');
        const cy = cmp ? top(cmp) : 0;
        const sticky = document.querySelector('.mt-sticky');
        const links = [...document.querySelectorAll('a')].filter(a => a.offsetParent && !(sticky && sticky.contains(a)) && top(a) < cy)
          .map(a => a.textContent.trim().slice(0, 20));
        const broken = [...document.images].filter(i => i.complete && i.naturalWidth === 0 && !/felmat/.test(i.src)).map(i => i.src);
        const lines = el => { const g = document.createRange(); g.selectNodeContents(el); return new Set([...g.getClientRects()].map(x => Math.round(x.top))).size; };
        const longH2 = [...document.querySelectorAll('h2.mt-h2')].filter(e => e.offsetParent && lines(e) > 2).map(e => e.textContent.trim());
        const text = document.body.innerText;
        const pts = sub ? ['3つのポイント', '3つの選定基準'].filter(s => text.includes(s)) : [];
        return { hasCompare: !!cmp, links, broken, over: document.documentElement.scrollWidth - innerWidth, longH2, pts, screens: cmp ? +(cy / innerHeight).toFixed(1) : null };
      }, sub);
      const tag = `${page} ${w}px`;
      const fail = [];
      if (!r.hasCompare) fail.push('#compare がない');
      if (r.links.length) fail.push('比較表より前のリンク: ' + r.links.join(' / '));
      if (r.broken.length) fail.push('画像切れ: ' + r.broken.join(' '));
      if (r.over > 0) fail.push('横はみ出し ' + r.over + 'px');
      if (w < 600 && r.longH2.length) fail.push('H2が3行以上: ' + r.longH2.join(' / '));
      if (r.pts.length) fail.push('残っている文言: ' + r.pts.join(' / '));
      if (early) fail.push('追従CTAが比較表より前に出る');
      if (!late) fail.push('追従CTAが比較表のあとに出ない');
      if (errs.length) fail.push('JSエラー: ' + errs.join(' / '));
      console.log((fail.length ? 'NG ' : 'OK ') + tag + (w < 600 ? `（比較表まで ${r.screens} 画面）` : '') + (fail.length ? '\n   - ' + fail.join('\n   - ') : ''));
      if (fail.length) ng.push(tag);
      await p.close();
    }
  }
  await browser.close();
  server.close();
  if (ng.length) { console.log(`\n${ng.length}件NG`); process.exit(1); }
  console.log('\nすべてOK');
})().catch(e => { console.error(e); process.exit(1); });

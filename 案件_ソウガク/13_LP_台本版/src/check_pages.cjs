/* ソウガクLPの公開前チェック（王道LP・サブLPの全ページ）
 *   NODE_PATH=$(npm root -g) node src/check_pages.cjs
 * 13_LP_台本版/ をローカルで配信し、スマホ（375×667）とPC（1280×800）で次を確認する。
 *   - 比較表（#compare）より前にCTA・リンクがない（追従CTAは除く）
 *   - 追従CTAは、最初にスクロールした時点では出ず、比較表を過ぎてから出る
 *   - 画像切れ・横はみ出し・JSエラーがない
 *   - 大見出し（h2.mt-h2）がスマホで2行以内
 *   - サブLPに「3つのポイント」「3つの選定基準」が残っていない
 *   - KW・学年の差し替え（VARIANTS）も同じ項目を確認し、URLパラメータで実際に差し替わるか
 *   - 差し替えた文言が見えているか、ほかの出し分けの文言が残っていないか、表示中のヒーロー画像が想定どおりか（EXPECT）
 * 1つでも引っかかれば終了コード1。
 */
const http = require('http');
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const PAGES = ['index.html', ...fs.readdirSync(ROOT).filter(d => /^lp\d+$/.test(d)).sort().map(d => d + '/index.html')].filter(p => fs.existsSync(path.join(ROOT, p)));
// KW・学年の差し替え（URLパラメータ）も1つずつ確認する。文字量が変わって崩れるケースを拾うため。
// サブLPに差し替え条件を足したら、ここにも足す。
const VARIANTS = {
  'lp02/index.html': ['?kw=online', '?grade=sho', '?grade=chu', '?grade=ko', '?kw=online&grade=sho', '?kw=online&grade=chu', '?kw=online&grade=ko'],
  'lp03/index.html': ['?kw=method'],
  'lp04/index.html': ['?kw=math', '?kw=english'],
  'lp05/index.html': ['?kw=individual', '?kw=concern', '?kw=subject'],
  'lp07/index.html': ['?kw=online', '?exam=junior'],
  'lp08/index.html': ['?kw=online'],
};
// 差し替えた文言が実際に見えているか（must）／ほかのKW向けの文言が見えていないか（never）。
// 「どれか1つ差し替わった」だけでは、入れ子の出し分けで文が消える不具合（例：LP02 の ?kw=online&grade=…）を拾えないため。
const EXPECT = {
  'lp02/index.html': { hero: 'lp02_hero.webp', must: ['発達特性のあるお子さまの家庭教師は、『1対1』', '学校や塾が合わなくて', '訪問型とオンライン、うちの子に合うのは？', 'どちらが合うかは、お子さんによって違います'], never: ['発達障害・グレーゾーンの子のオンライン家庭教師は、『1対1』', 'オンラインの家庭教師も考えているんです', 'この3つで比べる'] },
  'lp02/index.html?kw=online': { hero: 'lp02_hero_online.webp', must: ['発達障害・グレーゾーンの子のオンライン家庭教師は、『1対1』', 'オンラインの家庭教師も考えているんです', 'オンライン家庭教師は、この3つで比べる', '画面越しでも取り組めそうか'], never: ['発達特性のあるお子さまの家庭教師は、『1対1』', '訪問型とオンライン、うちの子に合うのは？', 'こんなお子さんなら、オンラインも候補に'] },
  'lp02/index.html?grade=sho': { hero: 'lp02_hero.webp', must: ['発達特性のあるお子さまの家庭教師は、『1対1』', '宿題になかなか取りかかれなくて'], never: ['学校や塾が合わなくて', 'オンラインの家庭教師も考えているんです'] },
  'lp02/index.html?kw=online&grade=sho': { hero: 'lp02_hero_online.webp', must: ['発達障害・グレーゾーンの子のオンライン家庭教師は、『1対1』', '宿題になかなか取りかかれなくて', 'オンラインの家庭教師も考えているんです', 'この3つで比べる'], never: ['発達特性のあるお子さまの家庭教師は、『1対1』', '学校や塾が合わなくて'] },
  'lp02/index.html?kw=online&grade=chu': { hero: 'lp02_hero_online.webp', must: ['発達障害・グレーゾーンの子のオンライン家庭教師は、『1対1』', '定期テストに提出物', 'オンラインの家庭教師も考えているんです'], never: ['発達特性のあるお子さまの家庭教師は、『1対1』', '学校や塾が合わなくて'] },
  'lp02/index.html?kw=online&grade=ko': { hero: 'lp02_hero_online.webp', must: ['発達障害・グレーゾーンの子のオンライン家庭教師は、『1対1』', '学習計画まで自分で立てる', 'オンラインの家庭教師も考えているんです'], never: ['発達特性のあるお子さまの家庭教師は、『1対1』', '学校や塾が合わなくて'] },
  'lp02/index.html?grade=chu': { hero: 'lp02_hero.webp', must: ['発達特性のあるお子さまの家庭教師は、『1対1』', '定期テストに提出物'], never: ['発達障害・グレーゾーンの子のオンライン家庭教師は、『1対1』', 'オンラインの家庭教師も考えているんです'] },
  'lp02/index.html?grade=ko': { hero: 'lp02_hero.webp', must: ['発達特性のあるお子さまの家庭教師は、『1対1』', '学習計画まで自分で立てる'], never: ['発達障害・グレーゾーンの子のオンライン家庭教師は、『1対1』', 'オンラインの家庭教師も考えているんです'] },
  'lp03/index.html?kw=method': { must: ['いろいろ勉強法を試している', '勉強法より前に見ておきたいこと'], never: ['宿題をやらないんです'] },
  'lp04/index.html': { must: ['漢字を何度書いても', 'ノートや書いた字'], never: ['計算の途中', '書いた英文'] },
  'lp04/index.html?kw=math': { must: ['計算を何度やっても', '算数が苦手なら', 'ノートや計算の途中', '文章を式にするところか、どこで'], never: ['漢字を何度書いても', '英語が苦手なら'] },
  'lp04/index.html?kw=english': { must: ['英単語を覚えても', '英語が苦手なら', 'ノートや書いた英文', '文字と音か、単語か'], never: ['漢字を何度書いても', '算数が苦手なら'] },
  'lp05/index.html?kw=concern': { must: ['塾に断られたり', '受け入れてもらえるかは、申込前に', '周りに迷惑をかけないかが心配なら'], never: ['やっぱり個別指導の方がいい'] },
  'lp05/index.html?kw=subject': { must: ['英語など特定の教科で探しているなら', '対応教科は教室・サービスごとに違う'], never: ['周りに迷惑をかけないかが心配なら'] },
  'lp07/index.html?kw=online': { must: ['受験に向けてオンラインの家庭教師を探している', '過去問への対応範囲や先生の体制はサービスごとに違います'], never: ['住んでいる地域に関係なく先生を探せます'] },
  'lp08/index.html': { hero: 'lp08_hero_v5.webp', must: ['『勉強を教えてくれるか』だけで決めないでください', '始める前に確かめたいこと', '最初は保護者だけで相談できるか'], never: ['オンラインも考えているんですが'] },
  // LP09 はヒーローが「文字なし背景画像＋見えるHTMLのH1」（lp-hero--text）。h1Text はH1が実際に画面に見えているかも確認する
  'lp09/index.html': { hero: 'lp09_hero.webp', h1Text: '学習障害で「書くのが苦手」な子、どう教える？', must: ['漢字が書けない、作文が進まない、板書が追いつかない。', '「書けない」にも、いろいろな困り方があります', '家で教えるのが難しいときは', '先生を選ぶなら、ここを確認', 'ここからは、発達特性への対応や授業の進め方も含めて、オンライン家庭教師3社を比べます。'], never: [] },
  'lp08/index.html?kw=online': { hero: 'lp08_hero_v5.webp', must: ['『勉強を教えてくれるか』だけで決めないでください', 'オンラインも考えているんですが', '最初は保護者だけで相談できるか'], never: ['家に人を迎えることが負担になりそうなら'] },
};
const TARGETS = PAGES.flatMap(p => [[p, ''], ...(VARIANTS[p] || []).map(q => [p, q])]);
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
  for (const [page, query] of TARGETS) {
    const sub = page !== 'index.html';
    for (const [w, h] of SIZES) {
      const p = await browser.newPage({ viewport: { width: w, height: h } });
      const errs = [];
      p.on('pageerror', e => errs.push(e.message));
      await p.goto(base + page.replace('index.html', '') + query, { waitUntil: 'load' });
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
      const r = await p.evaluate(([sub, query, EXP]) => {
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
        // 差し替え：?名前=X なら、data-kw / data-v / data-grade / data-名前 が X の要素が表示されているか（&でつないだ複数指定は1つずつ）
        const switched = [...new URLSearchParams(query)].every(([k, v]) =>
          [...document.querySelectorAll(`[data-kw="${v}"],[data-v="${v}"],[data-grade="${v}"],[data-${k}="${v}"]`)].some(e => !e.hidden && e.offsetParent));
        const exp = EXP || { must: [], never: [] };
        const heroes = [...document.querySelectorAll('.lp-hero img')].filter(i => i.offsetParent && i.getBoundingClientRect().height > 0).map(i => i.currentSrc || i.src);
        // srcset の縮小版（build_pages.py が作る「元の名前-幅.webp」）が選ばれていても、同じ画像なら OK
        const heroNg = exp.hero ? !(heroes.length === 1 && heroes[0].replace(/-\d+(\.webp)$/, '$1').endsWith('/' + exp.hero) && document.querySelector('.lp-hero img[src$="' + exp.hero + '"]').naturalWidth > 0) : false;
        // H1は1ページに1つ。h1Text があるページは、その文がH1として画面に見えているか（隠しテキストではないか）
        const h1s = [...document.querySelectorAll('h1')];
        const h1 = h1s[0];
        const h1Rect = h1 ? h1.getBoundingClientRect() : null;
        const h1Ng = h1s.length !== 1 || (exp.h1Text ? !(h1.textContent.replace(/\s+/g, '') === exp.h1Text && h1.checkVisibility() && h1Rect.width > 100 && h1Rect.height > 30 && parseFloat(getComputedStyle(h1).fontSize) >= 16) : false);
        const missing = exp.must.filter(t => !text.includes(t));
        const leaked = exp.never.filter(t => text.includes(t));
        return { missing, leaked, heroNg, heroes, h1Ng, h1Count: h1s.length, hasCompare: !!cmp, links, broken, over: document.documentElement.scrollWidth - innerWidth, longH2, pts, switched, screens: cmp ? +(cy / innerHeight).toFixed(1) : null };
      }, [sub, query, EXPECT[page + query] || null]);
      const tag = `${page}${query} ${w}px`;
      const fail = [];
      if (!r.hasCompare) fail.push('#compare がない');
      if (r.links.length) fail.push('比較表より前のリンク: ' + r.links.join(' / '));
      if (r.broken.length) fail.push('画像切れ: ' + r.broken.join(' '));
      if (r.over > 0) fail.push('横はみ出し ' + r.over + 'px');
      if (w < 600 && r.longH2.length) fail.push('H2が3行以上: ' + r.longH2.join(' / '));
      if (r.pts.length) fail.push('残っている文言: ' + r.pts.join(' / '));
      if (!r.switched) fail.push('URLパラメータで差し替わっていない');
      if (r.missing.length) fail.push('見えていない文言: ' + r.missing.join(' / '));
      if (r.heroNg) fail.push('ヒーロー画像が想定と違う: ' + r.heroes.join(' '));
      if (r.h1Ng) fail.push('H1が1つでない、または見えていない（H1の数 ' + r.h1Count + '）');
      if (r.leaked.length) fail.push('ほかの出し分けの文言が見えている: ' + r.leaked.join(' / '));
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

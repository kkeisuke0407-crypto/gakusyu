const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const source = fs.readFileSync('lp-measurement.js', 'utf8');
function boot({ path = '/lp08/', optout = false, gpc = false } = {}) {
  const listeners = {}, intervals = [], observers = [], timeouts = new Map();
  let clock = 10000, timerId = 0;
  const cta = { href: 'https://t.felmat.net/fmcl?ak=C12158L.1.I1680104.D1416296&pb=', dataset: { ctaId: 'first' }, hasAttribute: k => k === 'data-cta' };
  const section = { dataset: { sectionId: 'comparison' } };
  const faq = { dataset: { faqId: 'faq_1' }, open: true, addEventListener: (n,f) => listeners.faq = f };
  const document = { hidden: false, referrer: 'https://example.com/path?email=secret@example.com',
    documentElement: { scrollHeight: 10000 }, hasFocus: () => true,
    head: { appendChild: n => document.loaded = n.src }, createElement: () => ({}),
    querySelectorAll: s => s === '[data-section-id]' ? [section] : s === 'a[data-cta-id]' ? [cta] : s === 'details[data-faq-id]' ? [faq] : [],
    addEventListener: (n,f) => (listeners[n] ||= []).push(f) };
  const window = { scrollY: 0, innerHeight: 1000, addEventListener: (n,f) => (listeners[n] ||= []).push(f) };
  const context = { window, document, location: { pathname:path, origin:'https://online-tutor.navolio.net', search:'?utm_source=google&gclid=test&email=secret@example.com' },
    navigator: { globalPrivacyControl: gpc }, localStorage: { getItem: () => optout ? '1' : null },
    URL, URLSearchParams, Map, Set, WeakMap, Date: class extends Date { static now() { return clock; } }, performance: { now: () => clock },
    setTimeout: f => { timeouts.set(++timerId,f); return timerId; }, clearTimeout: id => timeouts.delete(id),
    setInterval: f => intervals.push(f), requestAnimationFrame: f => f() };
  context.IntersectionObserver = window.IntersectionObserver = class {
    constructor(cb) { this.cb=cb; observers.push(this); } observe() {} unobserve() {}
  };
  vm.runInNewContext(source, context);
  function events(name) { return (window.dataLayer || []).filter(x => x[0] === 'event' && x[1] === name); }
  return { window, document, cta, section, faq, context, events, observers, intervals,
    emit: (name,e={}) => (listeners[name] || []).forEach(f => f(e)),
    click: (link=cta, type='click',button=0) => (listeners[type] || []).forEach(f => f({ type,button,target:{closest:()=>link} })),
    flush: () => { [...timeouts.values()].forEach(f=>f()); timeouts.clear(); },
    advance: n => clock += n, faqToggle: () => listeners.faq() };
}
const t=boot();
assert.equal(t.window.dataLayer.filter(x=>x[0]==='config' && x[1]==='G-FQS2SK5HNF').length,1);
const config=t.window.dataLayer.find(x=>x[0]==='config' && x[1]==='G-FQS2SK5HNF')[2];
assert(!config.page_location.includes('email=')); assert(!config.page_referrer.includes('?'));
assert.equal(config.allow_google_signals,false);
t.click(); t.click(); assert.equal(t.events('sougaku_mcv').length,1); assert.equal(t.events('conversion').length,1);
assert.equal(t.events('sougaku_mcv')[0][2].lp_id,'LP08');
assert.equal(t.events('conversion')[0][2].send_to,'AW-18494858300/Mt8tCJijlZQdELzIhPNE');
t.advance(1500);t.click(t.cta,'auxclick',1);assert.equal(t.events('conversion').length,2);
t.click({href:'https://tintle.net/',hasAttribute:()=>false});assert.equal(t.events('conversion').length,2);assert.equal(t.events('lp_other_service_click').length,1);
t.click({...t.cta,href:'https://t.felmat.net/fmcl?ak=OTHER'});assert.equal(t.events('conversion').length,2);
t.window.scrollY=6500;t.emit('scroll');t.emit('scroll');assert.equal(t.events('lp_scroll').length,3);
t.window.scrollY=9000;t.emit('scroll');assert.equal(t.events('lp_scroll').length,5);
t.observers[0].cb([{target:t.section,isIntersecting:true,intersectionRatio:1}]);t.flush();assert.equal(t.events('lp_section_view').length,1);
t.document.hidden=true;t.observers[1].cb([{target:t.cta,isIntersecting:true,intersectionRatio:1}]);t.flush();assert.equal(t.events('lp_cta_view').length,0);
t.document.hidden=false;t.observers[1].cb([{target:t.cta,isIntersecting:true,intersectionRatio:1}]);t.flush();assert.equal(t.events('lp_cta_view').length,1);
t.faqToggle();assert.equal(t.events('lp_faq_open').length,1);
for(let i=0;i<30;i++){t.advance(1000);t.intervals[0]();}assert.equal(t.events('lp_active_read').length,1);
t.document.hidden=true;for(let i=0;i<60;i++){t.advance(1000);t.intervals[0]();}assert.equal(t.events('lp_active_read').length,1);
vm.runInNewContext(source,t.context);assert.equal(t.window.dataLayer.filter(x=>x[0]==='js').length,1);
assert.equal(boot({optout:true}).document.loaded,undefined);assert.equal(boot({gpc:true}).document.loaded,undefined);
for(const path of ['index.html',...Array.from({length:7},(_,i)=>`lp0${i+2}/index.html`)]) {
  const html=fs.readFileSync(path,'utf8');
  assert.equal((html.match(/lp-measurement\.js/g)||[]).length,1,path);
  assert.equal((html.match(/data-cta-id=/g)||[]).length,9,path);
  assert.equal((html.match(/data-faq-id=/g)||[]).length,8,path);
}
console.log('PASS: matching, click deduplication, middle-click, scroll milestones, visibility, active time, privacy, single initialization, all 8 pages.');

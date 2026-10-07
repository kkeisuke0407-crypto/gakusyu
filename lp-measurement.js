/* Shared measurement for LP01–LP08. No form data or unrestricted URL parameters. */
(function () {
  'use strict';
  if (window.__souMeasurement) return;
  window.__souMeasurement = true;
  var GA = 'G-FQS2SK5HNF';
  var ADS = 'AW-18494858300';
  var MCV = ADS + '/Mt8tCJijlZQdELzIhPNE';
  var path = location.pathname;
  var match = path.match(/^\/lp(0[2-8])\/(?:index\.html)?$/);
  var lp = match ? 'LP' + match[1] : 'LP01';
  var query = new URLSearchParams(location.search);
  var debug = query.get('measurement_debug') === '1';
  var disabled = false;
  try { disabled = localStorage.getItem('sou_measurement_optout') === '1'; } catch (_) {}
  if (disabled || navigator.globalPrivacyControl === true) return;

  var page = new URL(location.origin + path);
  ['utm_source', 'utm_medium', 'utm_campaign', 'utm_id', 'utm_content', 'gclid', 'gbraid', 'wbraid'].forEach(function (key) {
    var value = query.get(key);
    if (value && /^[a-zA-Z0-9_.~+\-]{1,200}$/.test(value)) page.searchParams.set(key, value);
  });
  var referrer = '';
  try { var ref = new URL(document.referrer); referrer = ref.origin + ref.pathname; } catch (_) {}
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  var gtag = window.gtag;
  gtag('consent', 'default', { ad_user_data: 'denied', ad_personalization: 'denied' });
  gtag('consent', 'default', {
    region: ['AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR','DE','GR','HU','IS','IE','IT','LV','LI','LT','LU','MT','NL','NO','PL','PT','RO','SK','SI','ES','SE','GB','CH'],
    ad_storage: 'denied', analytics_storage: 'denied'
  });
  gtag('js', new Date());
  gtag('set', { lp_id: lp, measurement_mode: debug ? 'debug' : 'live' });
  gtag('config', GA, {
    page_location: page.href, page_referrer: referrer,
    page_title: 'わが子の学び方ガイド | ' + lp,
    send_page_view: true, allow_google_signals: false,
    allow_ad_personalization_signals: false, debug_mode: debug
  });
  gtag('config', ADS, { page_location: page.href, page_referrer: referrer,
    page_title: 'わが子の学び方ガイド | ' + lp, allow_ad_personalization_signals: false });
  var loader = document.createElement('script');
  loader.async = true;
  loader.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA;
  document.head.appendChild(loader);

  function event(name, parameters) {
    gtag('event', name, Object.assign({ send_to: GA, lp_id: lp,
      measurement_mode: debug ? 'debug' : 'live', page_location: page.href,
      page_title: 'わが子の学び方ガイド | ' + lp }, parameters || {}));
  }
  function isSougaku(link) {
    try {
      var url = new URL(link.href);
      return link.hasAttribute('data-cta') && url.hostname === 't.felmat.net' &&
        url.pathname === '/fmcl' && url.searchParams.get('ak') === 'C12158L.1.I1680104.D1416296';
    } catch (_) { return false; }
  }
  var recentlyClicked = new WeakMap();
  function onClick(e) {
    if (e.type === 'auxclick' && e.button !== 1) return;
    var link = e.target.closest && e.target.closest('a[href]');
    if (!link) return;
    if (isSougaku(link)) {
      var now = Date.now();
      if (now - (recentlyClicked.get(link) || 0) < 1200) return;
      recentlyClicked.set(link, now);
      var cta = link.dataset.ctaId || 'unclassified';
      event('sougaku_mcv', { cta_id: cta, destination: 'sougaku' });
      gtag('event', 'conversion', { send_to: MCV, value: 0, currency: 'JPY' });
      // Preserve native target=_blank, keyboard and modified-click navigation.
    } else {
      try {
        var host = new URL(link.href).hostname;
        if (host === 'tintle.net' || host === 'coaching01.com')
          event('lp_other_service_click', { destination: host });
      } catch (_) {}
    }
  }
  document.addEventListener('click', onClick);
  document.addEventListener('auxclick', onClick);

  function observe(selector, name, key) {
    if (!('IntersectionObserver' in window)) return;
    var timers = new Map();
    var seen = new Set();
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        var node = entry.target;
        if (seen.has(node)) return;
        if (!entry.isIntersecting || entry.intersectionRatio < 0.5 || document.hidden) {
          clearTimeout(timers.get(node)); timers.delete(node); return;
        }
        if (timers.has(node)) return;
        timers.set(node, setTimeout(function () {
          timers.delete(node);
          if (document.hidden) return;
          var params = {}; params[key] = node.dataset[key === 'cta_id' ? 'ctaId' : 'sectionId'];
          seen.add(node); event(name, params); observer.unobserve(node);
        }, 1000));
      });
    }, { threshold: [0, 0.5] });
    document.querySelectorAll(selector).forEach(function (node) { observer.observe(node); });
    document.addEventListener('visibilitychange', function () {
      timers.forEach(clearTimeout); timers.clear();
      if (!document.hidden) document.querySelectorAll(selector).forEach(function (node) {
        if (!seen.has(node)) { observer.unobserve(node); observer.observe(node); }
      });
    });
  }
  observe('[data-section-id]', 'lp_section_view', 'section_id');
  observe('a[data-cta-id]', 'lp_cta_view', 'cta_id');
  var scrollSent = new Set();
  var scrollPending = false;
  function scrollCheck() {
    scrollPending = false;
    if (document.hidden) return;
    var height = document.documentElement.scrollHeight;
    var percent = Math.min(100, Math.floor((window.scrollY + window.innerHeight) / height * 100));
    [25, 50, 75, 90, 100].forEach(function (threshold) {
      if (percent >= threshold && !scrollSent.has(threshold)) {
        scrollSent.add(threshold); event('lp_scroll', { scroll_percent: threshold });
      }
    });
  }
  window.addEventListener('scroll', function () {
    if (!scrollPending) { scrollPending = true; requestAnimationFrame(scrollCheck); }
  }, { passive: true });
  window.addEventListener('load', scrollCheck, { once: true });
  document.querySelectorAll('details[data-faq-id]').forEach(function (node) {
    node.addEventListener('toggle', function () {
      if (node.open) event('lp_faq_open', { faq_id: node.dataset.faqId });
    });
  });
  var activeSeconds = 0;
  var lastTick = performance.now();
  var activeSent = new Set();
  function tick() {
    var now = performance.now();
    if (!document.hidden && document.hasFocus()) activeSeconds += Math.min((now - lastTick) / 1000, 2);
    lastTick = now;
    [30, 60, 120].forEach(function (seconds) {
      if (activeSeconds >= seconds && !activeSent.has(seconds)) {
        activeSent.add(seconds); event('lp_active_read', { read_seconds: seconds });
      }
    });
  }
  setInterval(tick, 1000);
  document.addEventListener('visibilitychange', function () { lastTick = performance.now(); });
})();

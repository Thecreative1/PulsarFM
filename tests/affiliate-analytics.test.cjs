/* Isolated analytics contract tests: no requests reach GA4 or the affiliate store. */
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../assets/affiliate-analytics.js'), 'utf8');

function setup({ consent = null, blocked = false, writeBlocked = false, existingTag = false, debug = false, market = 'PT' } = {}) {
  const events = {}, windowEvents = {}, appended = [], entries = [], logs = [];
  const button = choice => ({ dataset: { consentChoice: choice }, addEventListener(_, fn) { this.click = fn; }, focus() {} });
  const accept = button('granted'), reject = button('denied');
  const banner = { hidden: true, querySelector() { return accept; } };
  const settings = { hidden: true, focus() {}, addEventListener(_, fn) { this.click = fn; } };
  const storage = {
    getItem() { if (blocked) throw Error('blocked'); return consent; },
    setItem(_, value) { if (blocked || writeBlocked) throw Error('blocked'); consent = value; }
  };
  const document = {
    querySelector(selector) { return selector === '[data-consent-banner]' ? banner : settings; },
    querySelectorAll(selector) { return selector === '[data-consent-choice]' ? [accept, reject] : []; },
    addEventListener(type, fn) { events[type] = fn; },
    createElement() { return {}; },
    head: { append(value) { appended.push(value); } }
  };
  const window = {
    location: { pathname: market === 'ES' ? '/es/recomendaciones/auriculares-bluetooth-calidad-precio/' : '/recomendacoes/melhores-auscultadores/', search: debug ? '?affiliate_debug=1&email=private' : '' },
    addEventListener(type, fn) { windowEvents[type] = fn; }
  };
  if (existingTag) window.gtag = (...args) => entries.push(args);
  vm.runInNewContext(source, { window, document, localStorage: storage, URLSearchParams, console: { info(...args) { logs.push(args); } } });
  const link = {
    href: 'https://www.amazon.es/dp/B0BTJD6LCL/?tag=' + (market === 'ES' ? 'pulsarfmes-21' : 'pulsarfm-21'),
    dataset: { affiliatePlatform: 'amazon', market, language: market === 'ES' ? 'es-ES' : 'pt-PT', productId: 'sony-wh-ch520', merchant: 'amazon-es', trackingId: market === 'ES' ? 'pulsarfmes-21' : 'pulsarfm-21', productName: 'Sony WH-CH520',
      productCategory: 'Auscultadores', position: 'recommendation-1' }
  };
  const target = { closest: () => link };
  const click = (type = 'click', button = 0, extras = {}) => events[type]({ type, button, target, ...extras });
  const affiliateEvents = () => (window.dataLayer || entries).filter(item => item[0] === 'event' && item[1] === 'affiliate_click');
  return { window, banner, settings, accept, reject, click, affiliateEvents, appended, logs,
    storageChange(value) { consent = value; windowEvents.storage({ key: 'pulsarfm-consent' }); } };
}

test('no consent and denied consent send no affiliate events or GA requests', () => {
  for (const consent of [null, 'denied']) {
    const state = setup({ consent });
    state.click();
    assert.equal(state.affiliateEvents().length, 0);
    assert.equal(state.appended.length, 0);
    assert.equal(state.banner.hidden, consent === 'denied');
  }
});

test('accepted click sends the Amazon parameters and one event; page query is excluded', () => {
  const state = setup({ consent: 'granted', debug: true });
  state.click();
  const events = state.affiliateEvents();
  assert.equal(events.length, 1);
  assert.deepEqual(JSON.parse(JSON.stringify(events[0][2])), {
    market: 'PT', language: 'pt-PT', article_slug: 'melhores-auscultadores', product_id: 'sony-wh-ch520', merchant: 'amazon-es', link_position: 'recommendation-1',
    affiliate_platform: 'amazon', tracking_id: 'pulsarfm-21', product_name: 'Sony WH-CH520',
    product_category: 'Auscultadores', page_path: '/recomendacoes/melhores-auscultadores/',
    destination_url: 'https://www.amazon.es/dp/B0BTJD6LCL/?tag=pulsarfm-21',
    position: 'recommendation-1', transport_type: 'beacon', debug_mode: true
  });
  assert.equal(state.appended.length, 1);
  assert.equal(state.logs.length, 1);
});

test('keyboard/primary and middle clicks work, secondary and cancelled clicks do not', () => {
  const state = setup({ consent: 'granted' });
  state.click('click', 0); // Keyboard-generated anchor activation also has button 0.
  state.click('auxclick', 1);
  state.click('auxclick', 2);
  state.click('click', 0, { defaultPrevented: true });
  state.click('click', 0, { target: { closest: () => null } });
  assert.equal(state.affiliateEvents().length, 2);
});

test('acceptance, revocation and changes in another tab take effect immediately', () => {
  const state = setup();
  state.accept.click();
  state.click();
  state.settings.click();
  assert.equal(state.banner.hidden, false);
  state.reject.click();
  state.click();
  state.storageChange('granted');
  state.click();
  state.storageChange(null);
  state.click();
  assert.equal(state.affiliateEvents().length, 2);
  assert.equal(state.appended.length, 1);
  assert.equal(state.banner.hidden, false);
});

test('blocked storage defaults denied and permits an explicit session-only choice', () => {
  const state = setup({ blocked: true });
  state.click();
  assert.equal(state.affiliateEvents().length, 0);
  state.accept.click();
  state.click();
  assert.equal(state.affiliateEvents().length, 1);
  state.reject.click();
  state.click();
  assert.equal(state.affiliateEvents().length, 1);
});

test('reuse existing gtag without duplicate initialization; failures never cancel navigation', () => {
  const state = setup({ consent: 'granted', existingTag: true });
  state.click();
  assert.equal(state.affiliateEvents().length, 1);
  assert.equal(state.appended.length, 0);
  state.window.gtag = () => { throw Error('analytics unavailable'); };
  assert.doesNotThrow(() => state.click());
});

test('storage write failure still honors a new explicit choice for this session', () => {
  const state = setup({ consent: 'denied', writeBlocked: true });
  state.accept.click();
  state.click();
  assert.equal(state.banner.hidden, true);
  assert.equal(state.affiliateEvents().length, 1);
  state.reject.click();
  state.click();
  assert.equal(state.affiliateEvents().length, 1);
});

test('Spanish market uses its confirmed ID and respects consent without duplicate events', () => {
  const state = setup({ market: 'ES' });
  state.click();
  assert.equal(state.affiliateEvents().length, 0);
  state.accept.click();
  state.click();
  const events = state.affiliateEvents();
  assert.equal(events.length, 1);
  const p = events[0][2];
  assert.equal(p.market, 'ES');
  assert.equal(p.language, 'es-ES');
  assert.equal(p.tracking_id, 'pulsarfmes-21');
  assert.equal(p.article_slug, 'auriculares-bluetooth-calidad-precio');
  assert.equal(p.product_id, 'sony-wh-ch520');
  assert.equal(p.merchant, 'amazon-es');
  assert.equal(p.link_position, 'recommendation-1');
  assert.ok(!p.page_path.includes('?'));
  state.reject.click();
  state.click();
  assert.equal(state.affiliateEvents().length, 1);
});

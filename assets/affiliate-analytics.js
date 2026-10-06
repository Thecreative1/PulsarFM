/* Progressive enhancement only: affiliate URLs, content and disclosure are static HTML. */
(() => {
  'use strict';
  const consentKey = 'pulsarfm-consent';
  const measurementId = 'G-YRD1BYXB78';
  const ownsTag = typeof window.gtag !== 'function';
  let memoryConsent = null;
  let sessionOnlyConsent = false;
  let tagRequested = !ownsTag;
  const banner = document.querySelector('[data-consent-banner]');
  const settings = document.querySelector('[data-consent-settings]');

  function readConsent() {
    if (sessionOnlyConsent) return memoryConsent;
    try { return localStorage.getItem(consentKey); }
    catch (_) { return memoryConsent; }
  }

  const consentState = choice => ({
    analytics_storage: choice,
    ad_storage: choice,
    ad_user_data: choice,
    ad_personalization: choice
  });

  if (ownsTag) {
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('consent', 'default', { ...consentState('denied'), wait_for_update: 500 });
  }

  function syncConsent() {
    const choice = readConsent();
    window.gtag('consent', 'update', consentState(choice === 'granted' ? 'granted' : 'denied'));
    if (banner) banner.hidden = choice === 'granted' || choice === 'denied';
    // Reuse the existing site's preference. On editorial pages GA loads only after acceptance.
    if (choice === 'granted' && !tagRequested) {
      tagRequested = true;
      window.gtag('js', new Date());
      window.gtag('config', measurementId);
      const script = document.createElement('script');
      script.async = true;
      script.src = 'https://www.googletagmanager.com/gtag/js?id=' + measurementId;
      document.head.append(script);
    }
  }

  document.querySelectorAll('[data-consent-choice]').forEach(button => {
    button.addEventListener('click', () => {
      memoryConsent = button.dataset.consentChoice;
      try {
        localStorage.setItem(consentKey, memoryConsent);
        sessionOnlyConsent = false;
      } catch (_) { sessionOnlyConsent = true; }
      syncConsent();
      if (settings) settings.focus();
    });
  });
  if (settings && banner) {
    settings.hidden = false;
    settings.addEventListener('click', () => {
      banner.hidden = false;
      banner.querySelector('button').focus();
    });
  }
  window.addEventListener('storage', event => {
    if (event.key === consentKey || event.key === null) {
      sessionOnlyConsent = false;
      syncConsent();
    }
  });
  syncConsent();

  function trackAffiliateClick(event) {
    if (event.defaultPrevented || (event.type === 'auxclick' ? event.button !== 1 : event.button !== 0)) return;
    const link = event.target.closest?.('a[data-affiliate-link]');
    if (!link || readConsent() !== 'granted') return;
    const { affiliatePlatform, trackingId, productName, productCategory, position } = link.dataset;
    if (!affiliatePlatform || !productName || !position) return;
    const parameters = {
      affiliate_platform: affiliatePlatform,
      product_name: productName,
      product_category: productCategory || '',
      page_path: window.location.pathname, // Deliberately excludes query strings and personal identifiers.
      destination_url: link.href,
      position,
      transport_type: 'beacon'
    };
    if (trackingId) parameters.tracking_id = trackingId;
    if (new URLSearchParams(window.location.search).get('affiliate_debug') === '1') {
      parameters.debug_mode = true;
      console.info('[PulsarFM] affiliate_click', parameters);
    }
    try { window.gtag('event', 'affiliate_click', parameters); }
    catch (_) { /* Analytics failure must never prevent the native link action. */ }
  }
  document.addEventListener('click', trackAffiliateClick);
  document.addEventListener('auxclick', trackAffiliateClick);

  document.querySelectorAll('[data-product-image]').forEach(img => {
    const fallback = () => {
      if (img.dataset.fallback) return;
      img.dataset.fallback = 'true';
      img.src = '/img/gear-editorial.svg';
      img.alt = 'Ilustração de equipamento de áudio; fotografia do produto indisponível';
    };
    img.addEventListener('error', fallback);
    if (img.complete && img.naturalWidth === 0) fallback();
  });

  function hideStalePrices() {
    document.querySelectorAll('[data-price-checked]').forEach(element => {
      const checked = Date.parse(element.dataset.priceChecked + 'T00:00:00Z');
      const ageInDays = Math.floor(Date.now() / 86400000) - Math.floor(checked / 86400000);
      element.hidden = !Number.isFinite(ageInDays) || ageInDays < 0 || ageInDays > 7;
    });
  }
  hideStalePrices();
  document.addEventListener('visibilitychange', hideStalePrices);
})();

/* Locale and market preferences stay on this device; explicit links win. */
(() => {
  const language = document.documentElement.lang.startsWith('es') ? 'es' : document.documentElement.lang.startsWith('en') ? 'en' : 'pt';
  const params = new URLSearchParams(location.search);
  let storedMarket = null;
  try { storedMarket = localStorage.getItem('pulsarfm-market'); } catch (_) {}
  const requestedMarket = params.get('return_lang');
  const market = language !== 'en' ? language : ['pt','es'].includes(requestedMarket) ? requestedMarket : storedMarket === 'es' ? 'es' : 'pt';
  try {
    localStorage.setItem('pulsarfm-lang', language);
    localStorage.setItem('pulsarfm-market', market);
  } catch (_) {}
  for (const link of document.querySelectorAll('a[href]')) {
    const url = new URL(link.href, location.href);
    if (url.origin !== location.origin) continue;
    if (url.pathname.startsWith('/en/') && market === 'es') url.searchParams.set('return_lang','es');
    if (language === 'en' && url.pathname === '/' && link.lang !== 'pt-PT' && url.searchParams.get('lang') !== 'pt') {
      url.searchParams.set('lang','en');
      if (market === 'es') url.searchParams.set('return_lang','es');
    }
    if (link.lang === 'pt-PT' && url.pathname === '/') url.searchParams.set('lang','pt');
    link.href = url.pathname + url.search + url.hash;
  }
})();

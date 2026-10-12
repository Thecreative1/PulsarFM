/* Locale preference stays on this device; links always determine navigation. */
(() => {
  const language = document.documentElement.lang.startsWith('es') ? 'es' : document.documentElement.lang.startsWith('en') ? 'en' : 'pt';
  try { localStorage.setItem('pulsarfm-lang', language); } catch (_) {}
})();

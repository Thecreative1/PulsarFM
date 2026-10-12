/* Country detection runs only on a fresh visit to the neutral homepage.
 * Read only the country code; never store or send the returned IP to analytics.
 * A URL language or saved preference always wins. Failures leave the radio usable.
 */
(() => {
  const region = window.PulsarRadioRegion = { country: Promise.resolve(null), manualChoice: false };
  const explicit = new URLSearchParams(location.search).get('lang');
  let saved = null;
  try { saved = localStorage.getItem('pulsarfm-lang'); } catch (_) {}
  if (location.pathname !== '/' || ['pt','es','en'].includes(explicit) || ['pt','es','en'].includes(saved)) return;
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 2000);
  region.country = fetch('https://api.country.is/', {
    signal: controller.signal, credentials: 'omit', referrerPolicy: 'no-referrer', cache: 'no-store'
  }).then(response => response.ok ? response.json() : null)
    .then(data => data && data.country === 'ES' ? 'es' : null)
    .catch(() => null)
    .finally(() => clearTimeout(timeout));
})();

/* Radio locale labels only. Webamp, audio and Milkdrop remain owned by index.html. */
(() => {
  const i18n = window.PulsarRadioI18n;
  // A blocked preference store must not stop language selection or the player.
  i18n.storage = {
    getItem(key) { try { return localStorage.getItem(key); } catch (_) { return null; } },
    setItem(key, value) { try { localStorage.setItem(key, value); } catch (_) {} },
    removeItem(key) { try { localStorage.removeItem(key); } catch (_) {} }
  };
  // Localize presentation only; station names/URLs used by playback stay intact.
  let stationCopyObserver;
  const applySpanishStationCopy = () => {
    if (document.documentElement.lang !== 'es-ES') return;
    for (const [original, label] of Object.entries(i18n.es.stationLabels || {})) {
      for (const node of document.querySelectorAll('#radio-groups h3, #dock-station, #resume-chip')) {
        if (node.textContent.includes(original)) node.textContent = node.textContent.replace(original, label);
      }
      for (const star of document.querySelectorAll('#radio-groups .fav-btn[aria-label]')) {
        const text = star.getAttribute('aria-label');
        if (text.includes(original)) star.setAttribute('aria-label', text.replace(original, label));
      }
    }
  };
  i18n.applyControls = lang => {
    const logo = document.querySelector('.hero-logo');
    if (logo) logo.alt = lang === 'es' ? i18n.es.logoAlt : 'Logótipo Pulsar FM';
    if (lang === 'es') {
      if (!document.getElementById('radio-es-copy-fit')) {
        const style = document.createElement('link');
        style.id = 'radio-es-copy-fit';
        style.rel = 'stylesheet';
        style.href = '/assets/radio-es.css?v=20261012-es-linguistica';
        document.head.appendChild(style);
      }
      if (!stationCopyObserver) {
        stationCopyObserver = new MutationObserver(applySpanishStationCopy);
        for (const id of ['radio-groups', 'dock-station', 'resume-chip']) {
          const node = document.getElementById(id);
          if (node) stationCopyObserver.observe(node, { childList: true, subtree: true });
        }
      }
      applySpanishStationCopy();
    }
    const t = i18n.controls[lang];
    for (const [id, key] of [['scan-btn','scan'], ['skin-btn','skin'], ['trip-btn','trip'], ['share-btn','share']]) {
      const button = document.getElementById(id);
      button.textContent = t[key];
      button.setAttribute('aria-label', t[key + 'Label']);
    }
    document.getElementById('gear-btn').textContent = t.gear;
    const mode = document.body.classList.contains('player-floating') ? 'dock' : 'float';
    document.getElementById('player-lock-btn').textContent = t[mode];
    document.getElementById('player-lock-btn').setAttribute('aria-label', t[mode + 'Label']);
    const sleep = document.getElementById('sleep-btn');
    if (!/\d+m/.test(sleep.textContent)) sleep.textContent = t.sleep;
    sleep.setAttribute('aria-label', t.sleepLabel);
    const modal = document.querySelector('.trip-modal');
    modal.querySelector('h2').textContent = t.tripTitle;
    modal.querySelector('p').textContent = t.tripIntro;
    modal.querySelector('ol').innerHTML = t.tripSteps.map(text => '<li>' + text + '</li>').join('');
    modal.querySelector('.trip-note').textContent = t.tripNote;
    document.getElementById('trip-close').textContent = t.close;
    document.getElementById('trip-esc-hint').textContent = t.exit;
  };
})();

/* Radio locale labels only. Webamp, audio and Milkdrop remain owned by index.html. */
(() => {
  const i18n = window.PulsarRadioI18n;
  // A blocked preference store must not stop language selection or the player.
  i18n.storage = {
    getItem(key) { try { return localStorage.getItem(key); } catch (_) { return null; } },
    setItem(key, value) { try { localStorage.setItem(key, value); } catch (_) {} },
    removeItem(key) { try { localStorage.removeItem(key); } catch (_) {} }
  };
  i18n.applyControls = lang => {
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

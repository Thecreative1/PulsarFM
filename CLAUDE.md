# PulsarFM — AI Assistant Guide

Neon retro web radio: single-page app with the Webamp player (Winamp clone) +
Butterchurn (Milkdrop) visualizer. 40 curated live stations in 8 genres, PT/EN
bilingual, hosted on **GitHub Pages**. The owner's goal is to monetize (AdSense)
while preserving the neon/synthwave aesthetic.

**Read this whole file before editing.** This codebase looks simple (static
HTML) but has several non-obvious traps, all documented below. Every bug listed
here was hit at least once — do not reintroduce them.

## Golden rules

1. **Canonical host is `https://pulsarfm.eu` — NO www.** The CNAME is the apex
   domain; `www` 301-redirects to it. Never write `www.pulsarfm.eu` in any URL
   (canonical, OG, JSON-LD, sitemap, robots.txt, share links, genre pages).
2. **Never add a station without verifying its stream first** (see below).
   Stream URLs rot constantly. HTTPS only — mixed content is blocked.
3. **Station data lives in THREE places** that must stay in sync:
   - the `radios` JS object in `index.html`
   - the static `<article class="radio-card">` fallback cards in `index.html`
     (SEO fallback; replaced by JS on load)
   - the genre landing pages — regenerate them, don't hand-edit (see below)
4. **Keep the neon vibe.** Colors come from CSS variables in `:root`
   (`--line-primary` cyan, `--neon-pink`, `--neon-purple`, `--neon-green`).
   New UI must use them. Font is 'Share Tech Mono'. Favorites use gold
   `#ffd93b` as a deliberate warm accent — the only non-palette color.
5. **The owner commits and pushes himself** (terse messages like "2", "3").
   Leave changes in the working tree unless he asks you to commit.
6. **Deploy = push to `main`.** GitHub Pages builds in ~1–2 min, but the CDN
   caches pages for 10 min AND browsers cache aggressively. When the owner
   says "still broken" right after a deploy, suspect cache first — tell him to
   hard-refresh (Ctrl+Shift+R) before debugging anything.

## File map

```
index.html            — the whole app: CSS + HTML + JS in one file
privacidade.html      — privacy policy (GDPR), standalone neon page
radios-*/index.html   — 8 SEO genre landing pages (GENERATED — do not hand-edit)
tools/gen_genre_pages.py — generator for the genre pages (run: python tools/gen_genre_pages.py)
sitemap.xml           — 10 URLs; bump <lastmod> when pages change
robots.txt            — points to the sitemap (apex domain)
manifest.webmanifest  — PWA manifest
img/                  — pulsar-logo.webp/png (hero), pulsar-og.jpg (social), icon-*.png (PWA)
skins/                — Winamp .wsz skins for the SKINS drawer
.claude/launch.json   — preview server config (python -m http.server 4173)
```

## Webamp traps (the #1 source of bugs)

Webamp is loaded from unpkg (`webamp@2.3.1/built/webamp.bundle.min.js`).
Butterchurn + presets also from unpkg. Pinned versions — don't bump casually.

- **Webamp does NOT render into the node you pass.** It creates `#webamp`
  directly under `<body>`. Selectors like `#winamp > div` match nothing.
  The `#winamp` div is only used by Webamp to compute initial centering,
  and by us as the visual "dock panel" (fixed, opaque, `z-index: 999`).
- **z-index layering (dock mode):** dock panel `#winamp` = 999, `#webamp`
  (player) = 1000 (via the `zIndex` constructor option + CSS `!important`),
  `#container` = 1001 (so corner buttons stay clickable). Consequence: any
  fixed overlay (skin drawer, modals) needs **z-index > 1001** or it opens
  BEHIND the content panel when docked. Skin drawer = 1600, consent = 2000.
- **`windowLayout` constructor option is unreliable**: it is ignored for the
  Milkdrop window (registers after the constructor runs). Layout is instead
  applied post-render by `layoutPlayerWindows()`, which dispatches directly
  on the internal store:
  `webampInstance.store.dispatch({type:"UPDATE_WINDOW_POSITIONS", positions:{main:{x,y},...}, absolute:true})`
  and `{type:"WINDOW_SIZE_CHANGED", windowId:"milkdrop", size:[w,h]}`.
- **Resize units are SEGMENTS, not pixels**: width unit = 25px, height unit =
  29px added to the 275×116 base. Milkdrop desktop size `[7, 8]` = 450×348.
- **`layoutPlayerWindows()` must be called** after render, on window resize
  (debounced, skipped in trip mode), and when re-docking from float mode —
  otherwise dragged windows stay stuck behind `#container`.
- **Two canvases exist inside `#webamp`**: a tiny oscilloscope canvas in the
  main window and the real Milkdrop canvas. Always select the Milkdrop one
  with `#webamp .gen-window canvas` — never bare `#webamp canvas`.
- **Inline transforms trap `position: fixed`** (even identity transforms).
  Webamp window wrappers all have inline `transform: translate(...)`. Trip
  mode neutralizes the Milkdrop ancestor chain with
  `body.trip-active #webamp div:has(.gen-window), body.trip-active #webamp .gen-window { transform: none !important; }`.
  If a fixed element inside `#webamp` renders in a weird offset position,
  this is why.
- The dock/float toggle works by toggling `body.player-floating`; in dock
  mode `#webamp` itself is `position: fixed`. Player windows keep their store
  coordinates across the toggle — hence the re-layout on dock.
- `webamp.onClose()` re-opens the player after 300ms (intentional: the player
  IS the product, closing it would strand the user).

## Adding / replacing a station

1. Verify the stream (Python, from repo root):
   ```python
   import urllib.request
   req = urllib.request.Request(URL, headers={"User-Agent":"Mozilla/5.0","Icy-MetaData":"1","Range":"bytes=0-1023"})
   urllib.request.urlopen(req, timeout=8)   # want 200/206 + audio/* content type
   ```
   Reject: 4xx, SSL errors, timeouts, `http://` URLs.
2. Update the `radios` object in `index.html` (name + URL).
3. Update the matching static `<article class="radio-card"><h3>Name</h3></article>` in `index.html`.
4. Update `GENRES` in `tools/gen_genre_pages.py` (name + one-line PT
   description) and run `python tools/gen_genre_pages.py`.
5. If the total station count changed, update "40 estações/40 live stations"
   in: hero intro (static + both translations), og:description, JSON-LD
   description, `manifest.webmanifest`.
6. Bump `<lastmod>` in `sitemap.xml`.

## Layout rules learned the hard way

- Genre grid: `grid-template-columns: repeat(N, minmax(0, 1fr))` — the
  `minmax(0, …)` is required; plain `1fr` lets long station names blow the
  grid out of the container at mid viewports.
- Single-genre filter view: `#radio-groups.single-genre` makes the visible
  group full-width with a responsive station grid (`auto-fill, minmax(220px, 1fr)`).
  The class is toggled in `updateFilterState()`.
- Corner buttons (SCAN/SKINS/FLOAT left; PT-EN/TRIP/SHARE/SLEEP right) are
  absolute in `#container`, base rule `.scan-btn, .lang-switcher` sets
  `top:16px` and `z-index:2` (must stay above the hero logo or mobile taps
  fail). A new corner button needs `.scan-btn.<yourclass>` specificity to
  override `top`, and goes at top 16/52/88/124…
- Breakpoints: **760px** is the player breakpoint (desktop cluster is 725px
  wide: 275 column + 450 milkdrop). `isMobile` in JS uses `< 760` for the
  initial `windowLayout` (eq/playlist start closed on mobile);
  `layoutPlayerWindows()` re-checks `window.innerWidth` live. `--stack-height`:
  380px desktop, 300px below 760px. 820px/560px queries handle content only.
- In `applyLanguage()`, `updateFilterState()` must run AFTER
  `renderStations()` (rendering recreates the groups unhidden).

## i18n

All user-facing strings live in the `translations` object (`pt` / `en`) in
`index.html`. `applyLanguage()` re-renders everything and must update any new
translatable element — add your element's update line there. Static HTML holds
the PT version (also the SEO fallback). Genre pages are PT-only by design.

## localStorage keys

`pulsarfm-lang` (pt|en) · `pulsarfm-skin` (skin file path) ·
`pulsarfm-floating` (bool) · `pulsarfm-consent` (granted|denied) ·
`pulsarfm-favs` (JSON array of stream URLs) · `pulsarfm-last` (JSON {url,name})

## GDPR / monetization (the reason this site exists)

- GA4 (`G-YRD1BYXB78`) runs with **Consent Mode v2, default all-denied**, on
  every page. The consent banner lives only on index; a stored "granted"
  choice is honored everywhere. Never add a tracker outside this mechanism.
- The AdSense slot is **commented out** in `index.html` (search "Ad slot") with
  instructions — it needs the owner's approved `ca-pub` ID. The neon-framed
  `.ad-slot` CSS is ready. One slot between the radio grid and SEO blocks;
  do not add ads above the player.
- Ko-fi float button (bottom right) and footer link: `https://ko-fi.com/pfm80`.
- Privacy contact e-mail is in `privacidade.html`.

## Verifying changes locally

- Preview: the `pulsarfm` config in `.claude/launch.json` serves the repo at
  `http://localhost:4173` (`python -m http.server 4173`).
- Browser caches this site hard — when re-testing after an edit, load
  `/?v=<timestamp>` to cache-bust.
- Headless screenshots may time out while Butterchurn's WebGL canvas is
  animating — verify with DOM queries (getBoundingClientRect, elementFromPoint)
  instead of pixels.
- Deep links to test: `/?genre=rock` (filter), `/?genre=favs` (favorites).
- Fullscreen (trip mode) cannot be triggered headlessly; validate by adding
  `document.body.classList.add('trip-active')` and measuring the
  `.gen-window canvas` rect against the viewport.

## Feature inventory (so you don't rebuild what exists)

Genre filter bar + favorites filter · per-card favorite stars · SCAN (random
station) · SKINS drawer (10 .wsz, persisted) · dock/float player modes ·
TRIP mode (fullscreen visualizer) · SLEEP timer (15/30/60 min → pause) ·
resume-last-station chip · SHARE button (Web Share API + clipboard fallback) ·
PT/EN switch · consent banner · PWA manifest · 8 SEO genre pages ·
`?genre=` deep links with URL sync.

# Existing PulsarFM design

The editorial area extends the existing radio site. Listeners may open a guide beside the radio in a dim room or on a phone; preserve its dark background, readable pale text and restrained neon accents.

- Background: `--bg-base: #031317`; panel background near dark teal.
- Text: `--text-primary: #ecfffb`, `--text-muted: #9ad9d3`.
- Accents: `--line-primary: #00ffcc`, `--line-secondary: #00ccff`, `--neon-pink: #ff2d9b`, `--neon-purple: #c044ff`.
- Typography: existing Share Tech Mono with Courier New / monospace fallback.
- Shape: rounded panels, thin borders, subtle glow. Avoid adding decorative animation to reading surfaces.
- Editorial body measure: about 68 characters. Generous heading spacing, smaller metadata.
- Recommendations: image and copy in a horizontal row, stacked on phones, with a single affiliate CTA. Disclosure (owner's choice, 06/10/2026): a short "Contém links de afiliado" note in the date line at the top — always before the first store link — linking to the full disclosure box at the end of the article (`#divulgacao`). Never drop the top note: Amazon and EU advertising rules want it visible before the links.
- Home integration: a neon GEAR corner button (left column, under FLOAT) plus the bilingual footer link, both opening the editorial section in another tab so playback continues. Each genre page also has a GEAR box linking to its matching guide.

## Neon on the frame, calm on the text

Rule agreed with the owner (29/09/2026): the editorial pages must feel like part of PulsarFM, but neon never touches reading surfaces. Too little neon makes the section look like another site; too much tires the eyes and makes recommendations look like ads.

Neon allowed on the page frame (all in `assets/recommendations.css`, "Brand edges" block):

- Header bottom line: purple → cyan → pink gradient with glow (same as the radio's dock separator).
- Brand name and hub `h1`: soft cyan text glow.
- Hub illustration: cyan border with outer glow. `img/gear-editorial.svg` animates itself with CSS inside the SVG (record spins, tonearm sways, headphones bob, cable dash flows, EQ bars, LED pulse). Transform/opacity only, no JS, disabled under `prefers-reduced-motion`. Never put `<` inside its CSS comments: it breaks parsing if the SVG is ever inlined in HTML.
- Guide list: on hover/focus only, a cyan→pink bar on the left and a glowing pink number. At rest it stays flat. Each hub entry also shows its category illustration (150px, from the article's `illustration`) before the arrow: dimmed (opacity .8) at rest, full with a cyan glow on hover; hidden below 520px. The related-guides list at the end of each guide has no thumbnails.
- Policy panel: faint purple border.
- Product badges: pink pill with a faint glow.
- Body background: the same faint radial glows as the radio home page (purple top-left, pink top-right, blue bottom).

Keep calm: article body text, checklists, product cards, the comparison table and FAQs — no glow, no animation. Transitions respect `prefers-reduced-motion`.

**Exception agreed with the owner (06/10/2026): product illustrations pulse.** Amazon photos can't be used (Associates terms), so each card shows its category illustration from `img/gear/` (auscultadores, colunas, soundbars, gira-discos, home-studio, acessorios — mapped in `categoryImages` in `data/affiliates.json`). They follow the hub illustration's rules: 480×360, same palette and background, CSS animation inside the SVG with transform/opacity only, subtle (bob, spin, ripple, EQ bars), and `prefers-reduced-motion` turns them off. The card frame, text and CTA stay static.

**Category bar** (`.guide-nav`, under the header on every `/recomendacoes/` page, added 06/10/2026 at the owner's request): the six guides as neon pills (emoji `navIcon` + short `navLabel`), styled exactly like the genre filter buttons on the radio home page: solid cyan, pink glow on hover, neon green with glow for the current guide (it is frame, not reading surface). On desktop the pills wrap onto more rows (like the radio's genre filter) so no guide is ever hidden; below 900px they stay on one row that scrolls sideways with a fade on the right, and `affiliate-analytics.js` centres the current guide on load. No hamburger menu.

**Quick picks** (`.quick-picks`, after the disclosure): a calm panel (`--bg-panel`, thin border, no glow) with a pink uppercase label, the product name linking to its card and an inline Amazon link. Comparison tables put the store link under the model name in the first column, so it stays visible when the table scrolls sideways.

## Creating a new illustration

Every guide and product category has its own neon illustration in `img/gear/`. A new one must look like it belongs to the same set. Start from `templates/illustration.svg`.

- **Canvas:** `480×360`, `viewBox="0 0 480 360"`, background rect `#061D22` with `rx="20"`, and the faint grid line `M0 300H480M44 0V360M436 0V360` at `#9AD9D3`, opacity .09. Never change these.
- **One object, centred,** drawn as a dark panel (`#08292F` / `#0C3C43` / `#041015`) with a 2–3px cyan (`#00FFCC`) or blue (`#00CCFF`) outline, inside roughly x 64–416 and y 40–300. Simple, flat shapes — the same drawing language as the turntable and headphones: rounded rects, circles, thick round strokes.
- **Palette only:** cyan `#00FFCC`, blue `#00CCFF`, pink `#FF2D9B` (the "hot" detail: record label, speaker cone, EQ bars, REC light), purple `#C044FF` (secondary waves, Bluetooth), pale `#9AD9D3` at low opacity for inner lines, `#ECFFFB` for metal/needles. No gradients except the soundbar's synthwave sun; no text.
- **Motion:** 1–2 subtle loops via CSS inside the SVG — spin, bob (≤5px), pulse (scale ≤1.1), ripple, dashed signal flow, EQ bars, LED blink. `transform`/`opacity` only, `transform-box: fill-box` for scaling parts, and keep `@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }`.
- **Accessibility:** a `<title>` describing the object ("… nas cores néon da PulsarFM"). In product cards the `alt` comes from `categoryImages`; in the hub list the image is decorative (`alt=""`).
- **Never** put a less-than sign inside the SVG's CSS comments (breaks parsing if the SVG is ever inlined).
- **Check it alone** in the browser at full size and at 150px (hub thumbnail size) before wiring it up. If the object isn't recognisable at a glance, redraw — early drafts here produced a speaker that read as a robot face and RCA plugs that read as scissors.
- Wire it up: `categoryImages` in `data/affiliates.json` (product cards) and `illustration` on the article (hub list). The generator fails if a guide's illustration file is missing or a published product's category has no illustration.

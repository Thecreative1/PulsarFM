# Existing PulsarFM design

The editorial area extends the existing radio site. Listeners may open a guide beside the radio in a dim room or on a phone; preserve its dark background, readable pale text and restrained neon accents.

- Background: `--bg-base: #031317`; panel background near dark teal.
- Text: `--text-primary: #ecfffb`, `--text-muted: #9ad9d3`.
- Accents: `--line-primary: #00ffcc`, `--line-secondary: #00ccff`, `--neon-pink: #ff2d9b`, `--neon-purple: #c044ff`.
- Typography: existing Share Tech Mono with Courier New / monospace fallback.
- Shape: rounded panels, thin borders, subtle glow. Avoid adding decorative animation to reading surfaces.
- Editorial body measure: about 68 characters. Generous heading spacing, smaller metadata.
- Recommendations: image and copy in a horizontal row, stacked on phones, with a single affiliate CTA and nearby disclosure.
- Home integration: a neon GEAR corner button (left column, under FLOAT) plus the bilingual footer link, both opening the editorial section in another tab so playback continues. Each genre page also has a GEAR box linking to its matching guide.

## Neon on the frame, calm on the text

Rule agreed with the owner (29/09/2026): the editorial pages must feel like part of PulsarFM, but neon never touches reading surfaces. Too little neon makes the section look like another site; too much tires the eyes and makes recommendations look like ads.

Neon allowed on the page frame (all in `assets/recommendations.css`, "Brand edges" block):

- Header bottom line: purple → cyan → pink gradient with glow (same as the radio's dock separator).
- Brand name and hub `h1`: soft cyan text glow.
- Hub illustration: cyan border with outer glow. `img/gear-editorial.svg` animates itself with CSS inside the SVG (record spins, tonearm sways, headphones bob, cable dash flows, EQ bars, LED pulse). Transform/opacity only, no JS, disabled under `prefers-reduced-motion`. Never put `<` inside its CSS comments: it breaks parsing if the SVG is ever inlined in HTML.
- Guide list: on hover/focus only, a cyan→pink bar on the left and a glowing pink number. At rest it stays flat.
- Policy panel: faint purple border.
- Product badges: pink pill with a faint glow.
- Body background: the same faint radial glows as the radio home page (purple top-left, pink top-right, blue bottom).

Keep calm: article body text, checklists, product cards, the comparison table and FAQs — no glow, no animation. Transitions respect `prefers-reduced-motion`.

**Exception agreed with the owner (06/10/2026): product illustrations pulse.** Amazon photos can't be used (Associates terms), so each card shows its category illustration from `img/gear/` (auscultadores, colunas, soundbars, gira-discos, home-studio, acessorios — mapped in `categoryImages` in `data/affiliates.json`). They follow the hub illustration's rules: 480×360, same palette and background, CSS animation inside the SVG with transform/opacity only, subtle (bob, spin, ripple, EQ bars), and `prefers-reduced-motion` turns them off. The card frame, text and CTA stay static.

**Category bar** (`.guide-nav`, under the header on every `/recomendacoes/` page, added 06/10/2026 at the owner's request): the six guides by their short `navLabel`, muted text; the current guide is cyan with an underline and a soft glow (it is frame, not reading surface). Below 900px it scrolls sideways with a fade on the right, and `affiliate-analytics.js` centres the current guide on load. No hamburger menu.

**Quick picks** (`.quick-picks`, after the disclosure): a calm panel (`--bg-panel`, thin border, no glow) with a pink uppercase label, the product name linking to its card and an inline Amazon link. Comparison tables put the store link under the model name in the first column, so it stays visible when the table scrolls sideways.

# -*- coding: utf-8 -*-
import os, json

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GENRES = {
 "radios-rock": {
  "genre":"rock","emoji":"\U0001F3B8","nome":"Rock / Alternativo",
  "title":"Rádios Rock Online Grátis — Ouvir em Direto | Pulsar FM",
  "desc":"Ouve rádios rock e alternativo em direto, grátis e sem instalar nada. Radio Paradise, Rock Antenne e mais — com visualizador retro estilo Winamp.",
  "h1":"Rádios Rock Online",
  "intro":"Do rock clássico ao alternativo moderno — cinco estações escolhidas a dedo, em direto e sem interrupções. Carrega no play e deixa o Milkdrop dançar.",
  "stations":[
   ("Radio Paradise - Rock Mix","Mistura eclética de rock com curadoria humana, direto da Califórnia."),
   ("Rock Antenne","A grande rádio rock alemã — do clássico ao moderno, sem pausas."),
   ("KEXP Seattle","A lendária rádio independente de Seattle — curadoria de culto."),
   ("Virgin Radio Italy","Rock clássico e moderno, direto de Itália."),
   ("M80 Rádio","Os clássicos que marcaram gerações, direto de Portugal.")]},
 "radios-jazz": {
  "genre":"jazz","emoji":"\U0001F3B7","nome":"Jazz",
  "title":"Rádios Jazz Online Grátis — Ouvir em Direto | Pulsar FM",
  "desc":"Ouve rádios jazz em direto e grátis: TSF Jazz de Paris, Smooth Jazz e Radio Swiss Jazz. Com visualizador retro estilo Winamp no browser.",
  "h1":"Rádios Jazz Online",
  "intro":"De Paris à Suíça, jazz 24 horas por dia. Suave, elegante e em direto — a banda sonora perfeita para qualquer hora.",
  "stations":[
   ("TSF Jazz","A rádio de referência do jazz em Paris, emissão 24h."),
   ("Smooth Jazz","Smooth jazz em alta qualidade (320 kbps), perfeito para relaxar."),
   ("Radio Swiss Jazz","Jazz selecionado sem publicidade, da rádio pública suíça."),
   ("Jazz Radio France","A grande rede francesa de jazz — do swing ao soul."),
   ("SomaFM Sonic Universe","Jazz de vanguarda e sons experimentais.")]},
 "radios-chill": {
  "genre":"chill","emoji":"\U0001F33F","nome":"Chill / Ambiente",
  "title":"Rádios Chill e Ambient Online Grátis | Pulsar FM",
  "desc":"Rádios chill e ambient em direto: SomaFM Drone Zone, Mission Control e Nightwave Plaza. Grátis, no browser, com visuais psicadélicos.",
  "h1":"Rádios Chill Online",
  "intro":"Ambient, drones espaciais e vaporwave — cinco estações para desligar do mundo e flutuar. Fecha os olhos ou deixa o visualizador hipnotizar-te.",
  "stations":[
   ("SomaFM Drone Zone","Ambient e drones espaciais para desligar completamente."),
   ("Chillout-style Jazz","Chill com comunicações espaciais da NASA à mistura."),
   ("Nightwave Plaza","Vaporwave e estética retro — a internet dos anos 90 em áudio."),
   ("SomaFM Lush","Vozes suaves sobre eletrónica de sonho."),
   ("Ibiza Global Radio","Balearic chill e house, direto de Ibiza.")]},
 "radios-pop": {
  "genre":"pop","emoji":"\U0001F3B6","nome":"Pop",
  "title":"Rádios Pop Online Grátis — Hits em Direto | Pulsar FM",
  "desc":"Ouve os hits do momento em direto: RFM, Rádio Comercial, Capital FM de Londres e NRJ. Grátis e sem instalar nada.",
  "h1":"Rádios Pop Online",
  "intro":"Os hits do momento, de Portugal a Londres e Paris. Cinco estações pop em direto para manter a energia em alta.",
  "stations":[
   ("RFM Pop Rock","Os êxitos pop rock de Portugal, pela RFM."),
   ("Rádio Comercial","A rádio mais ouvida de Portugal — hits e boa disposição."),
   ("Capital FM UK","Os hits do momento, direto de Londres."),
   ("NRJ France","Hit music only — os êxitos direto de França."),
   ("I Love Radio DE","Charts e hits para a geração digital, da Alemanha.")]},
 "radios-study": {
  "genre":"study","emoji":"\U0001F4BB","nome":"Study / Lo-Fi",
  "title":"Rádios para Estudar — Lo-Fi e Foco em Direto | Pulsar FM",
  "desc":"Música para estudar e trabalhar: SomaFM Groove Salad, clássica sem interrupções e chillhop lo-fi. Grátis, em direto, no browser.",
  "h1":"Rádios para Estudar",
  "intro":"Lo-fi, downtempo e clássica — cinco estações testadas e aprovadas para sessões longas de estudo ou trabalho profundo. Zero distrações.",
  "stations":[
   ("SomaFM Groove Salad","Downtempo e chill para manter o foco horas a fio."),
   ("Radio Swiss Classic","Música clássica sem interrupções nem publicidade."),
   ("I Love Chillhop","Lo-fi e chillhop — o clássico do estudo, em rádio."),
   ("SomaFM Deep Space One","Ambient espacial profundo para concentração máxima."),
   ("Venice Classic Radio","Clássica intemporal, de Itália com amor.")]},
 "radios-electronica": {
  "genre":"electro","emoji":"⚡","nome":"Electrónica / Dance",
  "title":"Rádios de Música Electrónica Online Grátis | Pulsar FM",
  "desc":"Rádios de electrónica e dance em direto: TechnoBase.FM, HouseTime.FM e Frisky Radio. Techno, house e progressive, grátis no browser.",
  "h1":"Rádios Electrónicas Online",
  "intro":"Techno, house e progressive em direto, 24 horas por dia. Sobe o volume, ativa o Milkdrop e transforma o quarto numa pista.",
  "stations":[
   ("TechnoBase.FM DE","Techno e hands up direto da Alemanha, com comunidade enorme."),
   ("HouseTime.FM","House 24 horas por dia, da mesma família do TechnoBase."),
   ("Frisky Radio EUA","Deep house e progressive com DJs residentes."),
   ("Sunshine Live","A maior rádio de eletrónica da Alemanha — sets e festivais."),
   ("Hirschmilch Electronic","Eletrónica alemã sem interrupções.")]},
 "radios-psytrance": {
  "genre":"psy","emoji":"\U0001F500","nome":"Goa / Psytrance",
  "title":"Rádios Psytrance e Goa Online Grátis | Pulsar FM",
  "desc":"Psytrance e goa trance em direto: Goa-Base, Hirschmilch Psy e BOM Psytrance. Grátis, no browser, com visuais psicadélicos Milkdrop.",
  "h1":"Rádios Psytrance Online",
  "intro":"Goa old school e psytrance moderno em direto. Combina com o modo TRIP do Pulsar FM — o visualizador em ecrã inteiro — e boa viagem.",
  "stations":[
   ("Goa-Base Trance","Goa trance old school, direto da Alemanha."),
   ("Hirschmilch Psy","Psytrance em alta qualidade, sem interrupções."),
   ("BOM Psytrance","Psytrance sem parar, da rede 1.FM."),
   ("Psyndora Psytrance","Psytrance e progressive da cena grega."),
   ("Hirschmilch Progressive","Progressive psy hipnótico, horas a fio.")]},
 "radios-synthwave": {
  "genre":"synthwave","emoji":"\U0001F306","nome":"Synthwave / Retrowave",
  "title":"Rádios Synthwave e Retrowave Online Grátis | Pulsar FM",
  "desc":"Synthwave e retrowave em direto: Nightride FM, ChillSynth FM e SomaFM Digitalis. Neon, nostalgia e visualizador Winamp no browser.",
  "h1":"Rádios Synthwave Online",
  "intro":"Neon, nostalgia e sintetizadores dos anos 80 que nunca existiram. É o género que define a vibe do Pulsar FM — em cinco estações.",
  "stations":[
   ("Nightride FM","Synthwave e retrowave para conduzir à noite (mesmo sem carro)."),
   ("ChillSynth FM","Chillsynth suave — neon em modo calmo."),
   ("SomaFM Digitalis","Eletrónica indie com alma digital."),
   ("Nightride Datawave","Datawave — sintetizadores para navegar a noite digital."),
   ("SomaFM Underground 80s","Synthpop e new wave underground dos anos 80.")]},
}

GA = '''  <!-- Google tag (gtag.js) with Consent Mode v2 - default: everything denied -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-YRD1BYXB78"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('consent', 'default', {
      ad_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied',
      analytics_storage: 'denied',
      wait_for_update: 500
    });
    if (localStorage.getItem('pulsarfm-consent') === 'granted') {
      gtag('consent', 'update', {
        ad_storage: 'granted',
        ad_user_data: 'granted',
        ad_personalization: 'granted',
        analytics_storage: 'granted'
      });
    }
    gtag('js', new Date());
    gtag('config', 'G-YRD1BYXB78');
  </script>'''

def page(slug, g):
    others = "\n".join(
        '          <a href="/{}/" class="genre-filter-link">{} {}</a>'.format(s, d["emoji"], d["nome"])
        for s, d in GENRES.items() if s != slug)
    cards = "\n".join('''      <article class="radio-card">
        <h3>{}</h3>
        <p>{}</p>
        <a class="play-cta" href="/?genre={}">\U0001F3A7 Ouvir no player</a>
      </article>'''.format(name, desc, g["genre"]) for name, desc in g["stations"])
    stations_ld = ",\n      ".join(
        '{{ "@type": "ListItem", "position": {}, "item": {{ "@type": "RadioStation", "name": {}, "description": {} }} }}'.format(
            i + 1, json.dumps(name, ensure_ascii=False), json.dumps(desc, ensure_ascii=False))
        for i, (name, desc) in enumerate(g["stations"]))
    return '''<!DOCTYPE html>
<html lang="pt">
<head>
{GA}

  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="icon" href="/favicon.ico" type="image/x-icon">

  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <link rel="canonical" href="https://pulsarfm.eu/{slug}/" />
  <meta name="theme-color" content="#031317" />

  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://pulsarfm.eu/{slug}/" />
  <meta property="og:title" content="{h1} | Pulsar FM" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:image" content="https://pulsarfm.eu/img/pulsar-og.jpg" />
  <meta property="og:site_name" content="Pulsar FM" />
  <meta property="og:locale" content="pt_PT" />

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "ItemList",
    "name": "{h1}",
    "itemListElement": [
      {stations_ld}
    ]
  }}
  </script>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "Pulsar FM", "item": "https://pulsarfm.eu/" }},
      {{ "@type": "ListItem", "position": 2, "name": "{h1}", "item": "https://pulsarfm.eu/{slug}/" }}
    ]
  }}
  </script>

  <style>
    :root {{
      --line-primary: #00ffcc;
      --line-secondary: #00ccff;
      --neon-pink: #ff2d9b;
      --neon-green: #39ff14;
      --text-primary: #ecfffb;
      --text-muted: #9ad9d3;
      --text-dim: rgba(236, 255, 251, 0.72);
    }}

    html {{ color-scheme: dark; }}

    body {{
      min-height: 100vh;
      margin: 0;
      padding: 32px 16px 60px;
      display: flex;
      flex-direction: column;
      align-items: center;
      background:
        radial-gradient(circle at top left,  rgba(192, 68, 255, 0.13), transparent 40%),
        radial-gradient(circle at top right, rgba(255, 45, 155, 0.10), transparent 38%),
        linear-gradient(180deg, #02080b 0%, #031317 48%, #010507 100%);
      color: var(--text-primary);
      font-family: 'Share Tech Mono', 'Courier New', monospace;
    }}

    main {{
      width: min(860px, 100%);
      background-color: rgba(0, 10, 14, 0.78);
      border: 2px solid var(--line-primary);
      border-radius: 24px;
      padding: 36px 28px;
      box-sizing: border-box;
      box-shadow:
        0 0 25px rgba(0, 255, 204, 0.22),
        0 0 28px rgba(255, 45, 155, 0.18);
      backdrop-filter: blur(8px);
    }}

    .breadcrumb {{
      font-size: 0.78rem;
      margin: 0 0 18px;
      color: var(--text-dim);
    }}

    .breadcrumb a {{ color: var(--line-secondary); text-decoration: none; }}
    .breadcrumb a:hover {{ color: var(--line-primary); }}

    h1 {{
      margin: 0 0 10px;
      color: var(--line-primary);
      font-size: clamp(1.5rem, 4vw, 2.3rem);
      text-shadow:
        0 0 18px rgba(0, 255, 204, 0.35),
        0 0 40px rgba(255, 45, 155, 0.20);
    }}

    .intro {{
      color: var(--text-muted);
      line-height: 1.75;
      font-size: 0.95rem;
      margin: 0 0 26px;
    }}

    .station-list {{
      display: grid;
      gap: 16px;
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
      margin-bottom: 30px;
    }}

    .radio-card {{
      background-color: rgba(0, 0, 0, 0.72);
      border: 1px solid var(--line-secondary);
      border-radius: 16px;
      padding: 18px;
      display: flex;
      flex-direction: column;
      box-shadow: 0 0 16px rgba(0, 204, 255, 0.18);
      transition: transform 0.18s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }}

    .radio-card:hover {{
      transform: translateY(-2px);
      border-color: var(--neon-pink);
      box-shadow: 0 0 18px rgba(255, 45, 155, 0.30);
    }}

    .radio-card h3 {{
      margin: 0 0 8px;
      color: var(--line-secondary);
      font-size: 1.05rem;
    }}

    .radio-card p {{
      margin: 0 0 14px;
      color: var(--text-dim);
      font-size: 0.85rem;
      line-height: 1.6;
      flex: 1;
    }}

    .play-cta {{
      align-self: flex-start;
      background-color: var(--line-secondary);
      color: #001114;
      text-decoration: none;
      padding: 9px 16px;
      border-radius: 999px;
      font-weight: bold;
      font-size: 0.85rem;
      transition: background-color 0.2s ease, transform 0.14s ease, box-shadow 0.2s ease;
    }}

    .play-cta:hover {{
      background-color: var(--neon-green);
      color: #001a00;
      transform: translateY(-1px);
      box-shadow: 0 0 14px rgba(57, 255, 20, 0.5);
    }}

    h2 {{
      color: var(--text-muted);
      font-size: 0.9rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin: 30px 0 12px;
    }}

    .genre-links {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 26px;
    }}

    .genre-filter-link {{
      display: inline-block;
      padding: 8px 14px;
      border-radius: 999px;
      text-decoration: none;
      background: rgba(0, 204, 255, 0.12);
      border: 1px solid rgba(0, 204, 255, 0.25);
      color: var(--line-secondary);
      font-size: 0.82rem;
      transition: all 0.2s ease;
    }}

    .genre-filter-link:hover {{
      background: rgba(255, 45, 155, 0.22);
      border-color: rgba(255, 45, 155, 0.5);
      color: var(--neon-pink);
      transform: translateY(-2px);
    }}

    .home-cta {{
      display: inline-block;
      background: var(--neon-green);
      color: #001a00;
      text-decoration: none;
      font-weight: bold;
      padding: 12px 24px;
      border-radius: 999px;
      font-size: 0.9rem;
      letter-spacing: 0.06em;
      box-shadow: 0 0 16px rgba(57, 255, 20, 0.4);
      transition: box-shadow 0.2s ease, transform 0.14s ease;
    }}

    .home-cta:hover {{
      transform: translateY(-2px);
      box-shadow: 0 0 24px rgba(57, 255, 20, 0.6);
    }}

    footer {{
      margin-top: 26px;
      font-size: 0.78rem;
      color: rgba(0, 255, 204, 0.6);
    }}

    footer a {{ color: var(--text-muted); }}
  </style>
</head>
<body>
  <main>
    <nav class="breadcrumb"><a href="/">Pulsar FM</a> › {emoji} {nome}</nav>

    <h1>{emoji} {h1}</h1>
    <p class="intro">{intro}</p>

    <div class="station-list">
{cards}
    </div>

    <a class="home-cta" href="/?genre={genre}">▶ OUVIR TUDO NO PULSAR FM</a>

    <h2>Outros géneros</h2>
    <div class="genre-links">
{others}
    </div>

    <footer>Pulsar FM — rádio online grátis com visualizador retro estilo Winamp · <a href="/privacidade.html">Privacidade &amp; Cookies</a></footer>
  </main>
</body>
</html>
'''.format(GA=GA, slug=slug, cards=cards, others=others, stations_ld=stations_ld,
           title=g["title"], desc=g["desc"], h1=g["h1"], intro=g["intro"],
           emoji=g["emoji"], nome=g["nome"], genre=g["genre"])

for slug, g in GENRES.items():
    d = os.path.join(OUT, slug)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(page(slug, g))
    print("OK", slug)

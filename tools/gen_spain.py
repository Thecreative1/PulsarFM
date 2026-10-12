"""Build Spanish static content, reusing the radio and editorial components.
No network, npm dependencies or client-side translation service required.
"""
from datetime import date
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit
from gen_recommendations import esc, json_ld, page as pt_page, read_json, SITE, SLUG, ASIN, https_url
from market_config import market_config
from site_i18n import alternates, language_switch

ROOT = Path(__file__).resolve().parent.parent
BASE = "/es/recomendaciones/"
AMAZON_STATEMENT = "En calidad de Afiliado de Amazon, obtengo ingresos por las compras adscritas que cumplen los requisitos aplicables."


def page(title, description, path, content, nav="", article=False, category=""):
    html = pt_page(title, description, path, content, article, nav, category=category)
    html = html.replace(language_switch(path), language_switch(path, "es"))
    replacements = {
        '<html lang="pt-PT"': '<html lang="es-ES"', 'content="pt_PT"': 'content="es_ES"',
        'class="editorial-page"': 'class="editorial-page es-page"',
        'data-market="PT"': 'data-market="ES"', 'data-language="pt-PT"': 'data-language="es-ES"',
        'Saltar para o conteúdo': 'Saltar al contenido',
        'Pulsar FM, página da rádio': 'Pulsar FM, página de radio',
        'href="/"': 'href="/es/"', 'Ouvir rádio': 'Escuchar radio', '(nova aba)': '(nueva pestaña)',
        'Pulsar FM · Música primeiro.': 'Pulsar FM · La música primero.',
        'href="/recomendacoes/"': 'href="/es/recomendaciones/"',
        '>Recomendações<': '>Recomendaciones<', 'href="/privacidade.html"': 'href="/es/privacidad/"',
        'Privacidade &amp; Cookies': 'Privacidad y cookies', 'Preferências de cookies': 'Preferencias de cookies',
        'Usamos o Google Analytics para perceber que conteúdos são úteis. Aceitas cookies de análise?':
            'Usamos Google Analytics para saber qué contenidos resultan útiles. ¿Aceptas las cookies de análisis y las opciones de publicidad de Google?',
        'Saber mais': 'Más información', '>Aceitar<': '>Aceptar<', '>Recusar<': '>Rechazar<',
    }
    # Transform only the shared chrome. The content is already written in Spanish.
    for old, new in replacements.items():
        html = html.replace(old, new)
    # Restore PT links in locale navigation after root-path chrome replacements.
    html = re.sub(r'<nav class="locale-nav".*?</nav>', language_switch(path, "es"), html, flags=re.S)
    return html


def crumbs(items):
    visible = '<nav class="breadcrumbs" aria-label="Ruta de navegación">' + ' <span aria-hidden="true">›</span> '.join(
        f'<a href="{esc(path)}">{esc(name)}</a>' if i < len(items)-1 else f'<span aria-current="page">{esc(name)}</span>'
        for i, (name, path) in enumerate(items)) + '</nav>'
    return visible + json_ld({"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": name, "item": SITE + path} for i, (name, path) in enumerate(items, 1)]})


def category_path(category):
    return BASE + "categorias/" + category["slug"] + "/"


def guide_link(article, category, number=None):
    prefix = f'<span class="guide-number" aria-hidden="true">{number:02}</span>' if number else ''
    image = (f'<span class="guide-thumb"><img src="{esc(article.get("illustration", category["illustration"]))}" alt="" width="480" height="360" loading="lazy"></span>' if number else '')
    return (f'<a class="guide-link" href="{BASE}{esc(article["slug"])}/">{prefix}<span>'
            f'<span class="guide-category">{esc(article.get("categoryLabel", category["name"]))}</span><span class="guide-title">{esc(article["title"])}</span>'
            f'<span class="guide-summary">{esc(article["summary"])}</span></span>{image}<span class="guide-arrow" aria-hidden="true">↗</span></a>')


def nav(articles, current=None):
    primary = [a for a in articles if not a.get("secondary")]
    return '<nav class="guide-nav" aria-label="Guías de equipo"><ul>' + ''.join(
        f'<li><a href="{BASE}{esc(a["slug"])}/"' + (' aria-current="page"' if a["slug"] == current else '') +
        f'><span aria-hidden="true">{esc(a["navIcon"])}</span> {esc(a["navLabel"])}</a></li>' for a in primary) + '</ul></nav>'


def disclosure(tag):
    if tag:
        return ('<aside class="affiliate-disclosure" id="divulgacion"><p><strong>Publicidad: enlaces de afiliado.</strong> '
                'Si compras a través de ellos, PulsarFM puede recibir una comisión sin coste adicional para ti.</p>'
                f'<p>{esc(AMAZON_STATEMENT)}</p><p>No hemos probado estos productos. Las comparaciones se basan en las fichas y la documentación enlazadas. '
                '<a href="/es/privacidad/#afiliados">Privacidad y afiliación</a>.</p></aside>')
    return '<aside class="affiliate-disclosure" id="divulgacion"><p>Enlaces comerciales directos a Amazon.es, sin identificador de afiliado para este mercado.</p></aside>'


def product_link(product, original, article_slug, position, label="Ver en Amazon.es", inline=False, config=None):
    settings = market_config("ES", config)
    asin = original.get("asin", "")
    if not ASIN.fullmatch(asin):
        raise ValueError("Spanish products must reuse a verified ASIN")
    href = f'https://{settings["marketplace"]}/dp/{asin}/'
    tag = settings.get("trackingId")
    if tag:
        href += "?tag=" + tag
    https_url(href, {"www.amazon.es"})
    data = (f' data-affiliate-link data-affiliate-platform="amazon" data-tracking-id="{esc(tag)}"'
            f' data-market="ES" data-language="es-ES" data-article-slug="{esc(article_slug)}"'
            f' data-product-id="{esc(product["id"])}" data-product-name="{esc(product["name"])}"'
            f' data-merchant="amazon-es" data-product-category="{esc(product["category"])}" data-position="{esc(position)}"') if tag else ''
    css = 'affiliate-inline' if inline else 'affiliate-cta'
    return (f'<a class="{css}" href="{esc(href)}" target="_blank" rel="sponsored nofollow noopener noreferrer"{data}>'
            f'{esc(label)} <span aria-hidden="true">↗</span><span class="sr-only"> (enlace comercial, nueva pestaña)</span></a>')


def validate(editorial, catalog):
    if editorial.get("schemaVersion") != 1:
        raise ValueError("Unsupported Spanish editorial schema")
    originals = {p["id"]: p for p in catalog["products"]}
    products = {p["id"]: p for p in editorial["products"]}
    categories = {cat["slug"]: cat for cat in editorial["categories"]}
    articles = {a["slug"]: a for a in editorial["articles"]}
    if len(products) != len(editorial["products"]) or len(articles) != len(editorial["articles"]) or len(categories) != len(editorial["categories"]):
        raise ValueError("Unique products/articles/categories required")
    portuguese = read_json(ROOT / "data/recommendations.json")["articles"]
    primary = [a for a in articles.values() if not a.get("secondary")]
    if [a.get("ptSlug") for a in primary] != [a["slug"] for a in portuguese]:
        raise ValueError("Spanish navigation must mirror the ordered Portuguese guides")
    for a, original in zip(primary, portuguese):
        if a["productIds"] != original["productIds"] or a.get("illustration") != original["illustration"]:
            raise ValueError("Spanish guide must retain the Portuguese selection and illustration")
        if not a.get("navLabel") or len(a["navLabel"]) > 20 or a.get("navIcon") != original["navIcon"]:
            raise ValueError("Spanish guide needs the corresponding navigation label/icon")
        for field in ("comparison", "badges"):
            if not a.get(field):
                raise ValueError("Mirrored guides need comparison and badges")
        table = a["comparison"]
        if table["rowProducts"] != a["productIds"] or len(table["rows"]) != len(a["productIds"]) or any(len(row) != len(table["columns"]) for row in table["rows"]):
            raise ValueError("Comparison rows must cover every selected product")
        if [q["productId"] for q in a["quickPicks"]] != [q["productId"] for q in original["quickPicks"]]:
            raise ValueError("Spanish quick picks must retain the Portuguese selection")
        for source in a.get("sources", []):
            https_url(source["url"])
    for category in categories.values():
        if not SLUG.fullmatch(category["slug"]) or not (ROOT / category["illustration"].lstrip('/')).is_file():
            raise ValueError("Category requires safe slug and existing illustration")
        if not any(a["category"] == category["slug"] for a in articles.values()):
            raise ValueError("Empty Spanish category")
    for p in products.values():
        if p["id"] not in originals or originals[p["id"]]["status"] != "published":
            raise ValueError("Spanish products must reuse published verified catalog entries")
        if p["name"] != originals[p["id"]]["name"] or p["listingReference"] != originals[p["id"]]["source"]["referenceUrl"]:
            raise ValueError("Product identity/reference changed without verification")
        if p["category"] not in categories or not p["pros"] or not p["cons"]:
            raise ValueError("Products need category and documented advantages/limitations")
        if not p.get("profile") or not p.get("description"):
            raise ValueError("Products need complete localized copy")
        if p.get("illustration") and not (ROOT / p["illustration"].lstrip('/')).is_file():
            raise ValueError("Product illustration must exist")
        if p["listingCheckedAt"] != originals[p["id"]]["source"]["checkedAt"]:
            raise ValueError("Localization must preserve the original listing verification date")
        if p.get("sourceKind") == "catalog" and (p["sourceUrl"] != p["listingReference"] or p["specsCheckedAt"] != p["listingCheckedAt"]):
            raise ValueError("Catalog-only references must not claim a fresh manufacturer verification")
        https_url(p["sourceUrl"])
        for source in p.get("sourceUrls", []):
            https_url(source)
        for field in ("listingCheckedAt", "specsCheckedAt"):
            date.fromisoformat(p[field])
        if p.get("price") is not None:
            raise ValueError("Never publish static Amazon prices")
    inbound = dict.fromkeys(articles, 0)
    for a in articles.values():
        if not SLUG.fullmatch(a["slug"]) or a["category"] not in categories:
            raise ValueError("Invalid Spanish article route/category")
        for field in ("title", "summary", "intro", "metaDescription", "closing"):
            if not a.get(field):
                raise ValueError("Spanish articles need complete editorial text")
        if len(a["metaDescription"]) > 160 or len(a["productIds"]) < 2 or len(set(a["productIds"])) != len(a["productIds"]):
            raise ValueError("Articles need unique comparisons and concise metadata")
        if not set(a["productIds"]) <= products.keys() or not a.get("quickPicks") or not a.get("faq"):
            raise ValueError("Incomplete Spanish comparisons")
        if not {p["productId"] for p in a["quickPicks"]} <= set(a["productIds"]) or len({p["productId"] for p in a["quickPicks"]}) != len(a["quickPicks"]):
            raise ValueError("Quick picks must reference distinct products in the article")
        if len(a["sections"]) < 2 or not any(s.get("checklist") for s in a["sections"]):
            raise ValueError("Articles need objective criteria")
        if len(set(a["related"])) != 2 or a["slug"] in a["related"] or not set(a["related"]) <= articles.keys():
            raise ValueError("Invalid related guides")
        for slug in a["related"]:
            inbound[slug] += 1
        for field in ("publishedAt", "updatedAt"):
            date.fromisoformat(a[field])
    if not all(inbound.values()):
        raise ValueError("Orphan Spanish article")
    return products, originals, categories, articles


def render_article(a, products, originals, categories, articles, settings):
    path = BASE + a["slug"] + "/"
    cat = categories[a["category"]]
    content = crumbs([("Pulsar FM", "/es/"), ("Recomendaciones", BASE), (cat["name"], category_path(cat)), (a["title"], path)])
    note = "Publicidad: contiene enlaces de afiliado" if settings.get("trackingId") else "Contiene enlaces comerciales directos"
    content += (f'<article class="guide"><header class="guide-header"><p class="eyebrow">{esc(cat["name"])}</p><h1>{esc(a["title"])}</h1>'
                f'<p class="article-meta">Actualizado el <time datetime="{a["updatedAt"]}">{date.fromisoformat(a["updatedAt"]).strftime("%d/%m/%Y")}</time>'
                f' · <a href="#divulgacion">{note}</a></p><p class="lead">{esc(a["intro"])}</p></header>')
    content += '<section class="quick-picks" aria-labelledby="eleccion"><h2 id="eleccion">Elección rápida por uso</h2><ol>'
    for i, pick in enumerate(a["quickPicks"], 1):
        p = products[pick["productId"]]
        content += (f'<li><span class="pick-label">{esc(pick["label"])}</span><span class="pick-copy"><a class="pick-name" href="#product-{p["id"]}">{esc(p.get("localizedName", p["name"]))}</a>'
                    f'<span class="pick-note">{esc(pick["note"])}</span></span>' + product_link(p, originals[p["id"]], a["slug"], f"quick-{i}", inline=True) + '</li>')
    content += '</ol></section><div class="guide-body">'
    for section in a["sections"]:
        content += '<section><h2>' + esc(section["heading"]) + '</h2>' + ''.join('<p>' + esc(p) + '</p>' for p in section.get("paragraphs", []))
        if section.get("checklist"):
            content += '<ul class="guide-checklist">' + ''.join('<li>' + esc(s) + '</li>' for s in section["checklist"]) + '</ul>'
        content += '</section>'
    if a.get("sources"):
        content += '<section><h2>Fuentes de esta guía</h2><p>' + ' · '.join(f'<a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["label"])}</a>' for s in a["sources"]) + '</p></section>'
    content += '</div><section class="guide-comparison"><h2>Comparación para decidir</h2><div class="table-scroll" tabindex="0" role="region" aria-label="Comparación de productos"><table><caption class="sr-only">Funciones y límites documentados</caption><thead><tr><th scope="col">Modelo</th><th scope="col">Para quién</th><th scope="col">A favor</th><th scope="col">Qué confirmar</th></tr></thead><tbody>'
    for i, pid in enumerate(a["productIds"], 1):
        p = products[pid]
        content += (f'<tr><th scope="row">{esc(p.get("localizedName", p["name"]))}<span class="table-cta">' + product_link(p, originals[pid], a["slug"], f"table-{i}", inline=True) + '</span></th>'
                    f'<td>{esc(p["profile"])}</td><td>{esc(p["pros"][0])}</td><td>{esc(p["cons"][0])}</td></tr>')
    content += '</tbody></table></div></section><section class="product-selection"><h2>Productos para comparar</h2><p class="article-meta">No mostramos precios ni disponibilidad: confirma el modelo, el vendedor y las condiciones en Amazon.es. Las imágenes son ilustraciones de categoría, no fotografías de producto.</p>'
    for i, pid in enumerate(a["productIds"], 1):
        p = products[pid]
        image = p.get("illustration", categories[p["category"]]["illustration"])
        content += (f'<article class="product-recommendation" id="product-{pid}"><div class="product-image"><img src="{image}" width="480" height="360" loading="lazy" data-product-image alt="Ilustración de equipo de audio en los colores de PulsarFM"></div><div class="product-copy">'
                    f'<p class="product-merchant">Amazon.es · Publicidad</p><p class="product-badge">{esc(a.get("badges", {}).get(pid, p["profile"]))}</p><h3>{esc(p.get("localizedName", p["name"]))}</h3><p>{esc(p["description"])}</p><h4>A favor</h4><ul class="product-facts">' + ''.join('<li>' + esc(item) + '</li>' for item in p["pros"]) + '</ul><h4>Limitaciones</h4><ul class="product-facts">' + ''.join('<li>' + esc(item) + '</li>' for item in p["cons"]) + '</ul>'
                    '<p class="product-source">' + ' · '.join(
                        f'<a href="{esc(url)}" target="_blank" rel="noopener">{label}</a>'
                        for url, label in zip(p.get("sourceUrls") or [p["sourceUrl"]], ["Ficha del catálogo" if p.get("sourceKind") == "catalog" else "Documentación del fabricante", "Más documentación"])) +
                    f' · {"Referencia registrada" if p.get("sourceKind") == "catalog" else "Consultada"} el {date.fromisoformat(p["specsCheckedAt"]).strftime("%d/%m/%Y")}</p>' + (f'<p class="article-meta">{esc(p["sourceNote"])}</p>' if p.get("sourceNote") else "") + product_link(p, originals[pid], a["slug"], f"recommendation-{i}") + '</div></article>')
    content += '</section><section class="guide-faq"><h2>Preguntas frecuentes</h2>' + ''.join(f'<div class="faq-item"><h3>{esc(item["q"])}</h3><p>{esc(item["a"])}</p></div>' for item in a["faq"]) + '</section>'
    content += f'<div class="guide-closing"><p>{esc(a["closing"])}</p></div>' + disclosure(settings.get("trackingId")) + '</article>'
    content += '<section class="related-guides"><h2>Más guías para tu próxima sesión</h2>' + ''.join(guide_link(articles[slug], categories[articles[slug]["category"]]) for slug in a["related"]) + '</section>'
    organization = {"@type": "Organization", "name": "PulsarFM", "url": SITE + "/"}
    content += json_ld({"@type": "Article", "headline": a["title"], "description": a["metaDescription"], "inLanguage": "es-ES", "datePublished": a["publishedAt"], "dateModified": a["updatedAt"], "author": organization, "publisher": organization, "image": SITE + "/img/pulsar-og.jpg", "mainEntityOfPage": SITE + path})
    return page(a["seoTitle"], a["metaDescription"], path, content, nav(articles.values(), a["slug"]), True, category=cat["slug"])


def render_hub(editorial, categories, articles, settings):
    content = ('<section class="editorial-hero"><div><p class="eyebrow">Gear / Tecnología</p><h1>Recomendaciones PulsarFM</h1><p class="lead">La música es el punto de partida.<br>El equipo viene después.</p><p>Guías para escuchar mejor, montar tu rincón y empezar a crear. Sin jerga de folleto ni prisas por venderte nada: primero entiendes, después eliges.</p><a class="text-link" href="#guias">Explorar las guías ↓</a></div><figure><img src="/img/gear-editorial.svg" width="720" height="520" alt="Ilustración de tocadiscos y auriculares en los colores de PulsarFM"><figcaption>Del primer play al último lado B.</figcaption></figure></section>')
    primary = [a for a in articles.values() if not a.get("secondary")]
    content += '<section id="guias" class="guides-index"><h2>Encuentra tu frecuencia</h2>' + ''.join(guide_link(a, categories[a["category"]], i) for i, a in enumerate(primary, 1)) + '</section>'
    content += '<section class="related-guides"><h2>Más guías para profundizar</h2>' + ''.join(guide_link(a, categories[a["category"]]) for a in articles.values() if a.get("secondary")) + '</section>'
    content += '<aside class="editorial-policy"><h2>Cómo elegimos</h2><p>Selecciones editoriales basadas en fichas y documentación enlazadas. No hemos probado estos productos ni medido su sonido. Publicamos las fuentes y explicamos las limitaciones. Las recomendaciones se organizan por uso y conexiones. Compara el precio actual del equipo completo antes de decidir.</p></aside>' + disclosure(settings.get("trackingId"))
    content += json_ld({"@type": "CollectionPage", "name": editorial["title"], "inLanguage": "es-ES", "url": SITE + BASE})
    return page(editorial["title"], editorial["description"], BASE, content, nav(articles.values()))


def render_category(cat, categories, articles):
    path = category_path(cat)
    subset = [a for a in articles.values() if a["category"] == cat["slug"]]
    content = crumbs([("Pulsar FM", "/es/"), ("Recomendaciones", BASE), (cat["name"], path)])
    content += f'<section class="guide-header"><p class="eyebrow">Equipo PulsarFM</p><h1>{esc(cat["name"])}</h1><p class="lead">{esc(cat["intro"])}</p></section><section class="guides-index"><h2>Guías de {esc(cat["name"].lower())}</h2>'
    content += ''.join(guide_link(a, cat, i) for i, a in enumerate(subset, 1)) + '</section><p class="article-meta">Selecciones editoriales con fuentes oficiales. Las guías identifican la publicidad antes de los enlaces comerciales.</p>'
    content += '<aside class="editorial-policy"><h2>También puede interesarte</h2><p>' + ' · '.join(f'<a href="{category_path(other)}">{esc(other["name"])}</a>' for other in categories.values() if other["slug"] != cat["slug"]) + '</p></aside>'
    content += json_ld({"@type": "CollectionPage", "name": cat["name"], "url": SITE + path, "inLanguage": "es-ES"})
    return page(cat["name"] + ": guías para elegir", cat["intro"], path, content, nav(articles.values()), category=cat["slug"])


def render_privacy(settings):
    content = crumbs([("Pulsar FM", "/es/"), ("Privacidad y cookies", "/es/privacidad/")])
    content += '''<article class="guide"><header class="guide-header"><h1>Privacidad y cookies</h1><p class="article-meta">Actualizado el 12/10/2026</p><p class="lead">PulsarFM es un proyecto independiente de radio online. Estas son las preferencias que guardamos y los servicios a los que conecta tu navegador.</p></header><div class="guide-body"><section><h2>Google Analytics y consentimiento</h2><p>Usamos Google Analytics 4 (G-YRD1BYXB78) para conocer las visitas, los contenidos y los clics. Consent Mode v2 empieza con el almacenamiento de análisis y publicidad denegado. En las guías, Google Analytics se carga después de aceptar y respeta la elección guardada. La radio y las páginas de géneros usan la integración existente de Consent Mode, que puede enviar señales sin cookies antes de aceptar.</p><p>La elección se guarda en pulsarfm-consent. Puedes cambiarla en «Preferencias de cookies» en el pie de esta página y de las guías. La elección se reutiliza al abrir otras páginas de PulsarFM en el mismo navegador. Aceptar autoriza las opciones de análisis y publicidad de Google configuradas en este aviso; rechazar las deniega. Rechazar impide los eventos comerciales propios de PulsarFM; no impide seguir voluntariamente un enlace externo.</p><p><a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">Cómo utiliza Google los datos de los sitios que usan sus servicios</a>.</p></section><section><h2>Preferencias en tu dispositivo</h2><p>Guardamos la elección de idioma (PT, ES o EN), skin, modo del player, favoritos, última emisora y consentimiento en localStorage. Son preferencias de este navegador, no requieren cuenta. La URL y el idioma guardado tienen prioridad sobre la detección de país. Puedes cambiar el idioma con el selector.</p><ul class="guide-checklist"><li>pulsarfm-lang: idioma.</li><li>pulsarfm-market: versión PT o ES a la que volver desde inglés.</li><li>pulsarfm-skin y pulsarfm-floating: aspecto y posición del player.</li><li>pulsarfm-favs y pulsarfm-last: favoritos y última emisora.</li><li>pulsarfm-consent: tu elección de cookies.</li></ul></section><section><h2>Idioma inicial por país</h2><p>En una primera visita al inicio, sin idioma explícito ni preferencia guardada, el navegador consulta <a href="https://country.is/" target="_blank" rel="noopener">Country.is</a> mediante api.country.is. El servicio recibe tu IP al atender la solicitud. PulsarFM lee solo el código de país, sin guardar la IP ni añadirla a Google Analytics. Si el país es España, abre la versión ES; si no puede obtener respuesta en dos segundos, mantiene PT. No solicita ubicación GPS ni coordenadas. La elección manual siempre tiene prioridad y la radio sigue disponible aunque la consulta falle.</p></section><section><h2>Radio en directo y servicios externos</h2><p>Al escuchar una emisora, el navegador conecta directamente con su servidor, que puede recibir tu dirección IP. El reproductor y el visualizador se cargan desde unpkg; la tipografía desde Google Fonts. Estos servicios reciben las solicitudes necesarias para servir esos recursos. El botón de apoyo abre Ko-fi, con su propia política de privacidad.</p><p><a href="https://more.ko-fi.com/privacy" target="_blank" rel="noopener">Privacidad de Ko-fi</a>.</p></section><section id="afiliados"><h2>Publicidad y afiliación Amazon</h2><p>Las guías identifican los enlaces de afiliado antes de la primera salida a la tienda. Una compra elegible puede generar una comisión para PulsarFM sin coste adicional para ti. Amazon.es se abre directamente, sin redirección intermedia ni scripts de Amazon en el sitio. Usamos ilustraciones propias, no fotografías descargadas de Amazon.</p>'''
    content += f'<p>{esc(AMAZON_STATEMENT)}</p>'
    content += '''<p>Los enlaces de la versión portuguesa mantienen su ID y los españoles usan el ID confirmado para España. Amazon recibe ese identificador para atribuir compras. El tratamiento de datos en el destino depende de Amazon: <a href="https://www.amazon.es/gp/help/customer/display.html?nodeId=201909010" target="_blank" rel="noopener">aviso de privacidad de Amazon.es</a>.</p><p>Con consentimiento de análisis, el evento affiliate_click incluye mercado, idioma, identificador del artículo y del producto, nombre y categoría del producto, tienda, posición del enlace, ID de afiliado, ruta de la página sin parámetros y URL del producto. No añadimos nombres, correos ni datos de compradores a estos parámetros. Los clics no son ventas: pedidos y comisiones se consultan en los informes de Amazon.</p></section><section><h2>Contacto y tus derechos</h2><p>Para consultas sobre acceso, rectificación o eliminación de datos, escribe a <a href="mailto:flavio.martins@gmail.com">flavio.martins@gmail.com</a>. Puedes borrar las preferencias locales desde los ajustes de tu navegador y retirar el consentimiento con el botón de este pie.</p></section></div></article>'''
    return page("Privacidad y cookies", "Privacidad de PulsarFM: consentimiento de Google Analytics, preferencias locales, streams de radio y enlaces comerciales de Amazon.es.", "/es/privacidad/", content)


def set_element(html, element_id, text):
    pattern = re.compile(r'(<([a-z][a-z0-9]*)\b[^>]*\bid="' + re.escape(element_id) + r'"[^>]*>).*?(</\2>)', re.S)
    html, count = pattern.subn(lambda m: m[1] + text + m[3], html, count=1)
    if count != 1:
        raise ValueError("Missing static radio element: " + element_id)
    return html


def render_home():
    source = (ROOT / "index.html").read_text(encoding="utf-8")
    dictionary = read_json(ROOT / "data/radio.es.json")
    t, c = dictionary["translation"], dictionary["controls"]["es"]
    head, sep, rest = source.partition('\n<body>')
    if not sep:
        raise ValueError("Radio body boundary missing")
    body, scripts = rest.split('<script src="https://unpkg.com/webamp', 1)
    head = head.replace('<html lang="pt">', '<html lang="es-ES">').replace('<html lang="pt-PT">', '<html lang="es-ES">')
    head = head.replace('<head>', '<head>\n  <!-- Generated from index.html and data/radio.es.json by tools/gen_spain.py. -->')
    head = re.sub(r'<title>.*?</title>', '<title>' + esc(t["pageTitle"]) + '</title>', head)
    head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m[1] + esc(t["metaDesc"]), head)
    head = head.replace('rel="canonical" href="https://pulsarfm.eu/"', 'rel="canonical" href="https://pulsarfm.eu/es/"')
    for prop, value in (("og:title", t["pageTitle"]), ("og:description", t["metaDesc"]), ("og:url", SITE + "/es/"), ("og:locale", "es_ES")):
        head = re.sub(r'(<meta property="' + prop + r'"\s+content=")[^"]*', lambda m: m[1] + esc(value), head)
    for prop, value in (("twitter:title", t["pageTitle"]), ("twitter:description", t["metaDesc"])):
        head = re.sub(r'(<meta name="' + prop + r'"\s+content=")[^"]*', lambda m: m[1] + esc(value), head)
    head = re.sub(r'(<meta name="keywords" content=")[^"]*', r'\1radio online gratis, radio en directo, Winamp, Milkdrop, radio rock, radio jazz, radio electrónica, radio synthwave', head)
    head = head.replace('content="pt_BR"', 'content="pt_PT"')
    def localized_ld(match):
        data = json.loads(match[1])
        if data["@type"] == "WebSite":
            data.update(url=SITE + "/es/", description=t["metaDesc"], inLanguage="es-ES")
        elif data["@type"] == "ItemList":
            data["name"] = "Radio online por género"
            genre_routes = read_json(ROOT / "data/genres.es.json")
            for item, g in zip(data["itemListElement"], genre_routes.values()):
                item["name"], item["url"] = g["h1"], SITE + "/es/" + g["slug"] + "/"
        return json_ld({k: v for k, v in data.items() if k != "@context"})
    head = re.sub(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', localized_ld, head, flags=re.S)
    fields = {"hero-h1": "h1", "hero-intro": "intro", "footer-line1": "footer1", "footer-line2": "footer2", "privacy-link": "privacyLink", "recommendations-link": "recommendationsLink", "kofi-float": "kofiFloat", "consent-title": "consentTitle", "consent-text": "consentText", "consent-accept": "consentAccept", "consent-reject": "consentReject", "favs-empty": "favsEmpty"}
    for element_id, key in fields.items():
        body = set_element(body, element_id, t[key])
    for element_id, key in (("scan-btn", "scan"), ("skin-btn", "skin"), ("gear-btn", "gear"), ("trip-btn", "trip"), ("share-btn", "share"), ("sleep-btn", "sleep"), ("player-lock-btn", "float"), ("trip-close", "close"), ("trip-esc-hint", "exit")):
        body = set_element(body, element_id, esc(c[key]))
    body = re.sub(r'(<a href="/\?lang=pt" data-radio-language="pt"[^>]*?) aria-current="page"', r'\1', body)
    body = body.replace('data-radio-language="es" lang="es-ES"', 'data-radio-language="es" aria-current="page" lang="es-ES"')
    body = body.replace('href="recomendacoes/"', 'href="/es/recomendaciones/"').replace('href="privacidade.html"', 'href="/es/privacidad/"')
    body = body.replace('aria-label="Recomendações PulsarFM (nova aba)"', 'aria-label="Recomendaciones PulsarFM (nueva pestaña)"').replace('aria-label="Gear: guias de equipamento de som (nova aba)"', 'aria-label="Equipo: guías de audio (nueva pestaña)"')
    body = body.replace('🎧 Ouvir agora', esc(t["playBtn"])).replace('⌛ A carregar player', esc(t["loadingBtn"]))
    for genre, name in t["genreNames"].items():
        body = re.sub(r'(<section class="radio-group" data-genre="' + genre + r'">\s*<div class="group-heading">\s*<h2>).*?(</h2>)', lambda m: m[1] + esc(name) + m[2], body, flags=re.S)
    for item in t["filters"]:
        body = re.sub(r'(<button[^>]*data-genre="' + item["genre"] + r'"[^>]*>).*?(</button>)', lambda m: m[1] + esc(item["label"]) + m[2], body, flags=re.S)
    genre_routes = {g["genre"]: "/es/" + g["slug"] + "/" for g in localized_genres().values()}
    seo = ''
    for card in t["seo"]:
        links = '<div class="genre-links">' + ''.join(f'<a href="{genre_routes[l["genre"]]}" class="genre-filter-link" data-genre="{l["genre"]}">{esc(l["label"])}</a>' for l in card.get("links", [])) + '</div>' if card.get("links") else ''
        seo += f'<article class="seo-card"><h2>{esc(card["h2"])}</h2><p>{card["p"]}</p>{links}</article>'
    body = re.sub(r'<div class="seo-blocks" id="seo-blocks">.*?(?=\s*<footer class="site-footer">)', '<div class="seo-blocks" id="seo-blocks">' + seo + '</div>\n', body, flags=re.S)
    body = re.sub(r'(<div class="trip-modal">).*?(</div>)', lambda m: m[1] + '<h2>' + esc(c["tripTitle"]) + '</h2><p>' + esc(c["tripIntro"]) + '</p><ol>' + ''.join('<li>' + s + '</li>' for s in c["tripSteps"]) + '</ol><p class="trip-note">' + esc(c["tripNote"]) + '</p><button class="trip-close" id="trip-close">' + esc(c["close"]) + '</button>' + m[2], body, flags=re.S)
    # Translate static dock labels; scripts will keep their existing live updates.
    for old, new in (("A tocar", "Sonando"), ("Escolhe uma estação ↓", "Elige una emisora ↓"), ("Hora local", "Hora local"), ("64 estações · 24/7", "64 emisoras · 24/7")):
        body = body.replace(old, new)
    return head + sep + body + '<script src="https://unpkg.com/webamp' + scripts


def localized_genres():
    import ast
    tree = ast.parse((ROOT / "tools/gen_genre_pages.py").read_text(encoding="utf-8"))
    originals = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "GENRES")
    return {slug: {**originals[slug], **data} for slug, data in read_json(ROOT / "data/genres.es.json").items()}


def generate():
    editorial = read_json(ROOT / "data/recommendations.es.json")
    catalog = read_json(ROOT / "data/affiliates.json")
    settings = market_config("ES")
    products, originals, categories, articles = validate(editorial, catalog)
    pages = {"es/index.html": render_home(), "es/privacidad/index.html": render_privacy(settings), "es/recomendaciones/index.html": render_hub(editorial, categories, articles, settings)}
    for cat in categories.values():
        pages[category_path(cat).strip('/') + "/index.html"] = render_category(cat, categories, articles)
    for a in articles.values():
        pages[BASE.strip('/') + "/" + a["slug"] + "/index.html"] = render_article(a, products, originals, categories, articles, settings)
    return pages


def update_sitemap(pages):
    path = ROOT / "sitemap.xml"
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", ns)
    tree = ET.parse(path)
    root = tree.getroot()
    for item in list(root):
        if item.findtext(f"{{{ns}}}loc", "").startswith(SITE + "/es/"):
            root.remove(item)
    # Locale navigation and metadata also change the modification date of existing pages.
    for item in root:
        lastmod = item.find(f"{{{ns}}}lastmod")
        if lastmod is not None:
            lastmod.text = "2026-10-12"
    urls = set(pages) | {"es/" + g["slug"] + "/index.html" for g in localized_genres().values()}
    for filename in sorted(urls):
        item = ET.SubElement(root, f"{{{ns}}}url")
        for key, value in (("loc", SITE + "/" + filename.removesuffix("index.html")), ("lastmod", "2026-10-12"), ("changefreq", "monthly")):
            ET.SubElement(item, f"{{{ns}}}{key}").text = value
    ET.indent(tree, space="  ")
    tree.write(path, encoding="UTF-8", xml_declaration=True)


def main():
    pages = generate()  # Validate the entire Spanish edition before writing.
    data = read_json(ROOT / "data/radio.es.json")
    locale_js = '/* Generated from data/radio.es.json by tools/gen_spain.py. */\nwindow.PulsarRadioI18n = ' + json.dumps({"es": data["translation"], "controls": data["controls"]}, ensure_ascii=False) + ';\n'
    for filename, content in {**pages, "assets/radio-locales.js": locale_js}.items():
        destination = ROOT / filename
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")
    update_sitemap(pages)
    print(f"Generated {len(pages)} Spanish pages, locale data and sitemap (plus 8 genre pages)")


if __name__ == "__main__":
    main()

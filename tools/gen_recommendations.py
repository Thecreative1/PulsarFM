"""Generate editorial HTML for GitHub Pages using only the Python standard library.

Edit data/ and templates/, then run python tools/gen_recommendations.py.
No affiliate account credentials, network access or JS build pipeline required.
"""
from datetime import date
from decimal import Decimal, InvalidOperation
from html import escape
import json
from pathlib import Path
import re
from string import Template
from urllib.parse import parse_qs, urlencode, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates" / "recommendations"
AWIN_HOSTS = {"awin1.com", "www.awin1.com", "tidd.ly"}
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
PRICE_MAX_AGE_DAYS = 7
# The only Amazon Associates tag allowed on PulsarFM (never another site's tag).
AMAZON_TRACKING_ID = "pulsarfm-21"
ASIN = re.compile(r"[A-Z0-9]{10}\Z")
# Amazon images need PA-API or Amazon-provided links; until then cards use the local illustration.
DEFAULT_IMAGE = "/img/gear-editorial.svg"
DEFAULT_IMAGE_ALT = "Ilustração de equipamento de áudio nas cores néon da PulsarFM"
NETWORKS = ("awin", "amazon")
AMAZON_STATEMENT = "Como Afiliado da Amazon, a PulsarFM recebe por compras elegíveis."
SITE = "https://pulsarfm.eu"  # Apex domain, never www.


def esc(value):
    return escape(str(value), quote=True)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def template(filename, **values):
    return Template((TEMPLATES / filename).read_text(encoding="utf-8")).substitute(values)


def https_url(value, hosts=None):
    """Validate before HTML escaping; reject credentials and ambiguous URLs."""
    if not isinstance(value, str) or re.search(r"[\s\\\x00-\x1f]", value):
        raise ValueError("URL must be HTTPS and contain no whitespace or backslashes")
    parsed = urlsplit(value)
    if (parsed.scheme != "https" or not parsed.hostname or parsed.username or
            parsed.password or parsed.port not in (None, 443)):
        raise ValueError("URL must be HTTPS, without credentials or custom ports")
    if hosts is not None and parsed.hostname not in hosts:
        raise ValueError("URL host is not allowed for this merchant/network")
    return value


def image_url(value):
    if isinstance(value, str) and re.fullmatch(r"/img/[a-zA-Z0-9_./-]+", value) and ".." not in value:
        return value
    return https_url(value)


def positive_id(value):
    return bool(re.fullmatch(r"[1-9][0-9]*", str(value)))


def is_affiliate(product):
    return product.get("linkType", "affiliate") == "affiliate"


def product_url(catalog, product):
    if is_affiliate(product):
        return affiliate_url(catalog, product)
    merchant = catalog["merchants"][product["merchant"]]
    if product.get("affiliateUrl"):
        raise ValueError("Direct products must not contain affiliateUrl")
    return https_url(product.get("destinationUrl", ""), merchant["allowedDestinationHosts"])


def amazon_url(merchant, product):
    """Build the link from the ASIN so every Amazon URL carries the PulsarFM tag."""
    if merchant.get("trackingId") != AMAZON_TRACKING_ID:
        raise ValueError("Amazon merchants must use the PulsarFM tracking ID " + AMAZON_TRACKING_ID)
    asin = product.get("asin", "")
    if not isinstance(asin, str) or not ASIN.fullmatch(asin):
        raise ValueError("Amazon products need a 10-character ASIN")
    url = f'https://{merchant["allowedDestinationHosts"][0]}/dp/{asin}/?tag={AMAZON_TRACKING_ID}'
    return https_url(url, merchant["allowedDestinationHosts"])


def affiliate_url(catalog, product):
    merchant = catalog["merchants"][product["merchant"]]
    if merchant["network"] == "amazon":
        return amazon_url(merchant, product)
    if merchant["network"] != "awin":
        raise ValueError("Unsupported affiliate network")
    ready_link = product.get("affiliateUrl", "")
    if ready_link:
        https_url(ready_link, AWIN_HOSTS)
        parsed = urlsplit(ready_link)
        if parsed.hostname != "tidd.ly":
            params = parse_qs(parsed.query)
            if parsed.path == "/cread.php":
                if not all(positive_id(params.get(key, [""])[0]) for key in ("awinmid", "awinaffid")):
                    raise ValueError("Awin deep link must contain valid advertiser and publisher IDs")
                destination = params.get("ued", params.get("p", [""]))[0]
                https_url(destination, merchant["allowedDestinationHosts"])
                for field, expected in (("awinmid", merchant.get("advertiserId")),
                                        ("awinaffid", catalog["awin"].get("publisherId"))):
                    if expected and params[field][0] != str(expected):
                        raise ValueError("Awin deep link IDs do not match the configured account/merchant")
            elif parsed.path != "/pclick.php" or not all(
                    positive_id(params.get(key, [""])[0]) for key in ("p", "a", "m")):
                raise ValueError("Use an Awin Link Builder link, product-feed pclick link or tidd.ly link")
            else:
                for field, expected in (("m", merchant.get("advertiserId")),
                                        ("a", catalog["awin"].get("publisherId"))):
                    if expected and params[field][0] != str(expected):
                        raise ValueError("Awin feed link IDs do not match the configured account/merchant")
        elif not parsed.path.strip("/"):
            raise ValueError("Awin short link needs its generated path")
        # Preserve all existing tracking parameters, including clickref.
        return ready_link
    publisher = catalog["awin"].get("publisherId", "")
    advertiser = merchant.get("advertiserId", "")
    if not positive_id(publisher) or not positive_id(advertiser):
        raise ValueError("Configure Awin publisherId and advertiserId, or supply affiliateUrl")
    destination = https_url(product.get("destinationUrl", ""), merchant["allowedDestinationHosts"])
    return "https://www.awin1.com/cread.php?" + urlencode({
        "awinmid": advertiser, "awinaffid": publisher,
        "clickref": "pulsarfm-" + product["id"], "ued": destination,
    })


def validate_catalog(catalog):
    if catalog.get("schemaVersion") != 1:
        raise ValueError("Unsupported catalog schemaVersion")
    for key, merchant in catalog["merchants"].items():
        if not SLUG.fullmatch(key) or not merchant.get("name"):
            raise ValueError("Merchants need a slug ID and a name")
        if merchant.get("network") not in NETWORKS or not merchant.get("allowedDestinationHosts"):
            raise ValueError("Configure network and destination hosts for each merchant")
    for category, illustration in catalog.get("categoryImages", {}).items():
        image_url(illustration.get("src"))
        if not isinstance(illustration.get("alt"), str) or not illustration["alt"].strip():
            raise ValueError(f"Category image for {category} needs alt text")
    products = {}
    for product in catalog["products"]:
        product_id = product.get("id", "")
        if not SLUG.fullmatch(product_id) or product_id in products:
            raise ValueError("Products need unique slug IDs")
        if product.get("status") not in ("draft", "published"):
            raise ValueError("Product status must be draft or published")
        if product.get("linkType", "affiliate") not in ("direct", "affiliate"):
            raise ValueError("Product linkType must be direct or affiliate")
        if product.get("merchant") not in catalog["merchants"]:
            raise ValueError("Unknown merchant: " + str(product.get("merchant")))
        if product["status"] == "published":
            required = ["name", "description"]
            if product.get("image"):
                required.append("imageAlt")  # Without an image the local illustration is used.
            if catalog["merchants"][product["merchant"]]["network"] == "amazon":
                required.append("category")
            for field in required:
                if not isinstance(product.get(field), str) or not product[field].strip():
                    raise ValueError(f"Published product {product_id} needs {field}")
            if product.get("image"):
                image_url(product["image"])
            # Editorial notes kept in the data only; never rendered.
            if not isinstance(product.get("bestFor", ""), str):
                raise ValueError(f"Product {product_id}: bestFor must be text")
            for field in ("pros", "cons"):
                items = product.get(field, [])
                if not isinstance(items, list) or not all(isinstance(item, str) for item in items):
                    raise ValueError(f"Product {product_id}: {field} must be a list of text")
            product_url(catalog, product)
            if product.get("price") is not None:
                validate_price(product["price"])
        products[product_id] = product
    return products


def validate_price(price):
    try:
        amount = Decimal(str(price["amount"]))
        if not amount.is_finite() or amount < 0:
            raise ValueError("Price must be a finite non-negative number")
        if not re.fullmatch(r"[A-Z]{3}", price["currency"]):
            raise ValueError("Price currency must be an ISO currency code")
        checked = date.fromisoformat(price["checkedAt"])
        return amount, checked
    except (KeyError, InvalidOperation, TypeError) as error:
        raise ValueError("Price needs amount, currency and checkedAt (YYYY-MM-DD)") from error


def render_affiliate_link(catalog, product, position, label=None, css_class="affiliate-cta"):
    url = product_url(catalog, product)
    merchant = catalog["merchants"][product["merchant"]]
    label = label or merchant.get("cta") or "Ver oferta"
    if not is_affiliate(product):
        return (f'<a class="{esc(css_class)}" href="{esc(url)}" target="_blank" rel="noopener" '
                f'data-product-link="direct">{esc(label)} <span aria-hidden="true">↗</span>'
                '<span class="sr-only"> (abre numa nova aba)</span></a>')
    tracking = f' data-tracking-id="{esc(merchant["trackingId"])}"' if merchant.get("trackingId") else ""
    return (f'<a class="{esc(css_class)}" href="{esc(url)}" target="_blank" '
            f'rel="sponsored nofollow noopener noreferrer" data-affiliate-link '
            f'data-affiliate-platform="{esc(merchant["network"])}"{tracking} '
            f'data-merchant="{esc(product["merchant"])}" data-product-name="{esc(product["name"])}" '
            f'data-product-category="{esc(product.get("category", ""))}" '
            f'data-position="{esc(position)}">{esc(label)} <span aria-hidden="true">↗</span>'
            '<span class="sr-only"> (link de afiliado, abre numa nova aba)</span></a>')


def render_price(price, today=None):
    if price is None:
        return ""
    amount, checked = validate_price(price)
    today = today or date.today()
    # Old or future-dated prices must not look like current offers.
    if not 0 <= (today - checked).days <= PRICE_MAX_AGE_DAYS:
        return ""
    value = f"{amount:,.2f}".replace(",", " ").replace(".", ",")
    currency = "€" if price["currency"] == "EUR" else esc(price["currency"])
    return (f'<div class="product-price" data-price-checked="{checked.isoformat()}">'
            f'<p>{value} {currency}</p><small>Consultado em {checked.strftime("%d/%m/%Y")}. '
            'Preço e disponibilidade podem mudar. Confirma na loja.</small></div>')


def product_image(catalog, product):
    """Own image if authorised, else the category illustration, else the generic one."""
    if product.get("image"):
        return image_url(product["image"]), product["imageAlt"]
    illustration = catalog.get("categoryImages", {}).get(product.get("category", ""))
    if illustration:
        return image_url(illustration["src"]), illustration["alt"]
    return DEFAULT_IMAGE, DEFAULT_IMAGE_ALT


def render_product(catalog, product, position, today=None, badge=""):
    badge_html = f'<p class="product-badge">{esc(badge)}</p>' if badge else ""
    image, image_alt = product_image(catalog, product)
    return template("product.html", id=esc(product["id"]), badge=badge_html,
                    image=esc(image), image_alt=esc(image_alt),
                    name=esc(product["name"]),
                    merchant=esc(catalog["merchants"][product["merchant"]]["name"]),
                    description=esc(product["description"]), price=render_price(product.get("price"), today),
                    link=render_affiliate_link(catalog, product, position))


def guide_link(article, index=None):
    number = f'<span class="guide-number" aria-hidden="true">{index:02}</span>' if index else ""
    return (f'<a class="guide-link" href="/recomendacoes/{esc(article["slug"])}/">{number}<span>'
            f'<span class="guide-category">{esc(article["category"])}</span>'
            f'<span class="guide-title">{esc(article["title"])}</span>'
            f'<span class="guide-summary">{esc(article["summary"])}</span></span>'
            '<span class="guide-arrow" aria-hidden="true">↗</span></a>')


def page(title, description, path, content, article=False):
    return template("page.html", title=esc(title), description=esc(description), path=esc(path),
                    og_type="article" if article else "website", content=content)


def json_ld(data):
    data = {"@context": "https://schema.org", **data}
    # Never let the content close the script tag early.
    return ('<script type="application/ld+json">' +
            json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + '</script>')


def render_comparison(comparison, catalog=None, products=None):
    """Optional table: {"caption", "columns": [...], "rows": [[...], ...]}; plain escaped text.

    Optional "rowProducts" (one product ID or null per row) adds a store link under each model name,
    in the first column so it stays visible when the table scrolls sideways.
    """
    columns = comparison["columns"]
    rows = comparison["rows"]
    if any(len(row) != len(columns) for row in rows):
        raise ValueError("Every comparison row needs one cell per column")
    row_products = comparison.get("rowProducts")
    if row_products is not None and len(row_products) != len(rows):
        raise ValueError("rowProducts needs one entry (product ID or null) per comparison row")
    links = [""] * len(rows)
    if row_products:
        for i, product_id in enumerate(row_products, 1):
            if product_id and products[product_id]["status"] == "published":
                product = products[product_id]
                label = catalog["merchants"][product["merchant"]].get("shortCta", "Ver na loja")
                links[i - 1] = render_affiliate_link(catalog, product, f"table-{i}", label, "affiliate-inline")
    head = "".join(f'<th scope="col">{esc(col)}</th>' for col in columns)
    body = "".join('<tr><th scope="row">' + esc(row[0]) +
                   (f'<span class="table-cta">{link}</span>' if link else "") + '</th>' +
                   "".join(f'<td>{esc(cell)}</td>' for cell in row[1:]) + '</tr>'
                   for row, link in zip(rows, links))
    note = f'<p class="article-meta">{esc(comparison["note"])}</p>' if comparison.get("note") else ""
    return ('<section class="guide-comparison" aria-labelledby="comparacao">'
            f'<h2 id="comparacao">{esc(comparison.get("heading", "Comparação rápida"))}</h2>'
            f'<div class="table-scroll" tabindex="0"><table><caption class="sr-only">{esc(comparison["caption"])}</caption>'
            f'<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>{note}</section>')


def render_faq(faq):
    """Optional FAQ: visible section + FAQPage JSON-LD built from the same text."""
    items = "".join(f'<div class="faq-item"><h3>{esc(item["q"])}</h3><p>{esc(item["a"])}</p></div>'
                    for item in faq)
    ld = json_ld({"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": item["q"],
         "acceptedAnswer": {"@type": "Answer", "text": item["a"]}} for item in faq]})
    return ('<section class="guide-faq" aria-labelledby="faq"><h2 id="faq">Perguntas frequentes</h2>'
            f'{items}</section>{ld}')


def render_quick_picks(article, catalog, products):
    """Short "for people in a hurry" list near the top; each pick links to its card and the store."""
    items = []
    for i, pick in enumerate(article.get("quickPicks", []), 1):
        if pick["productId"] not in article["productIds"]:
            raise ValueError("Quick pick for a product that is not in this article: " + pick["productId"])
        product = products[pick["productId"]]
        if product["status"] != "published":
            continue
        items.append(f'<li><span class="pick-label">{esc(pick["label"])}</span>'
                     f'<span class="pick-copy"><a class="pick-name" href="#product-{esc(product["id"])}">'
                     f'{esc(product["name"])}</a><span class="pick-note">{esc(pick["note"])}</span></span>'
                     + render_affiliate_link(catalog, product, f"quick-{i}", css_class="affiliate-inline")
                     + '</li>')
    if not items:
        return ""
    return ('<section class="quick-picks" aria-labelledby="escolhas"><h2 id="escolhas">Escolhas rápidas</h2>'
            '<p class="article-meta">Para quem já sabe o que procura. O porquê de cada escolha está mais abaixo.</p>'
            f'<ol>{"".join(items)}</ol></section>')


def article_json_ld(article, selected, description):
    url = f'{SITE}/recomendacoes/{article["slug"]}/'
    organization = {"@type": "Organization", "name": "PulsarFM", "url": SITE + "/",
                    "logo": {"@type": "ImageObject", "url": SITE + "/img/icon-512.png"}}
    parts = [
        json_ld({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Pulsar FM", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Recomendações", "item": SITE + "/recomendacoes/"},
            {"@type": "ListItem", "position": 3, "name": article["title"], "item": url}]}),
        json_ld({"@type": "Article", "headline": article["title"], "description": description,
                 "datePublished": article.get("publishedAt", article["updatedAt"]),
                 "dateModified": article["updatedAt"], "inLanguage": "pt-PT",
                 "image": SITE + "/img/pulsar-og.jpg", "mainEntityOfPage": url,
                 "author": organization, "publisher": organization}),
    ]
    if selected:
        parts.append(json_ld({"@type": "ItemList", "name": "Produtos para comparar: " + article["title"],
                              "itemListElement": [
                                  {"@type": "ListItem", "position": i, "name": product["name"],
                                   "url": f'{url}#product-{product["id"]}'}
                                  for i, product in enumerate(selected, 1)]}))
    return "".join(parts)


def uses_amazon(catalog, products):
    return any(is_affiliate(product) and
               catalog["merchants"][product["merchant"]]["network"] == "amazon" for product in products)


def disclosure(catalog, products):
    amazon = f'<p>{AMAZON_STATEMENT}</p>' if uses_amazon(catalog, products) else ""
    return template("disclosure.html", amazon=amazon)


def render_article(article, articles, catalog, products):
    selected = []
    for product_id in article["productIds"]:
        product = products[product_id]  # Unknown references fail the build instead of disappearing.
        if product["status"] == "published":
            selected.append(product)
    sections = []
    linked = list(selected)
    has_affiliates = any(is_affiliate(product) for product in selected)
    for index, section in enumerate(article["sections"], 1):
        parts = [f'<section><h2>{esc(section["heading"])}</h2>']
        parts.extend(f'<p>{esc(text)}</p>' for text in section.get("paragraphs", []))
        if section.get("checklist"):
            parts.append('<ul class="guide-checklist">' + "".join(
                f'<li>{esc(text)}</li>' for text in section["checklist"]) + '</ul>')
        # Optional editorial text links reference the same central product IDs as cards.
        for link_index, link in enumerate(section.get("productLinks", []), 1):
            product = products[link["productId"]]
            if product["status"] == "published":
                linked.append(product)
                has_affiliates = has_affiliates or is_affiliate(product)
                parts.append('<p>' + render_affiliate_link(catalog, product,
                             f"inline-{index}-{link_index}", link.get("label"), "affiliate-inline") + '</p>')
        parts.append('</section>')
        sections.append("\n".join(parts))
    product_html = ""
    badges = article.get("badges", {})
    for product_id in badges:
        if product_id not in article["productIds"]:
            raise ValueError("Badge for a product that is not in this article: " + product_id)
    if selected:
        cards = "\n".join(render_product(catalog, product, f"recommendation-{i}",
                                         badge=badges.get(product["id"], ""))
                          for i, product in enumerate(selected, 1))
        product_html = ('<section class="product-selection" aria-labelledby="selecao">'
                        '<h2 id="selecao">Produtos para comparar</h2>' +
                        ('<p class="article-meta">Não mostramos preços: mudam várias vezes por dia. '
                         'Confirma o preço, a disponibilidade e o vendedor na loja.</p>'
                         if any(is_affiliate(product) for product in selected) else
                         '<p class="article-meta">Links diretos para a loja, sem comissão para a PulsarFM. '
                         'Confirma o preço, a disponibilidade e o vendedor na loja; pode tratar-se de uma oferta Marketplace.</p>') +
                        cards + '</section>')
    updated = date.fromisoformat(article["updatedAt"])
    by_slug = {item["slug"]: item for item in articles}
    if article.get("related"):
        others = [by_slug[slug] for slug in article["related"]]  # Unknown slugs fail the build.
    else:
        others = [item for item in articles if item["slug"] != article["slug"]][:2]
    description = article.get("metaDescription") or article["summary"]
    quick_picks = render_quick_picks(article, catalog, products)
    comparison = (render_comparison(article["comparison"], catalog, products)
                  if article.get("comparison") else "")
    for product_id in (article.get("comparison") or {}).get("rowProducts") or []:
        if product_id:
            linked.append(products[product_id])
    content = template("article.html", category=esc(article["category"]), title=esc(article["title"]),
                       intro=esc(article["intro"]), updated_at=updated.isoformat(),
                       updated_label=updated.strftime("%d/%m/%Y"),
                       disclosure=disclosure(catalog, linked) if has_affiliates else "",
                       quick_picks=quick_picks,
                       sections="\n".join(sections), products=product_html,
                       extras=comparison + (render_faq(article["faq"]) if article.get("faq") else "") +
                              article_json_ld(article, selected, description),
                       closing=esc(article["closing"]), related="\n".join(guide_link(item) for item in others))
    return page(article.get("seoTitle") or article["title"], description,
                f'/recomendacoes/{article["slug"]}/', content, True)


def render_hub(editorial, catalog):
    published = [product for product in catalog['products'] if product['status'] == 'published']
    has_affiliates = any(is_affiliate(product) for product in published)
    link_note = ('Alguns links nos guias são links de afiliado. Se comprares através deles, '
                 'a PulsarFM pode receber uma pequena comissão, sem custo adicional para ti.'
                 if has_affiliates else 'Os produtos apresentados usam links diretos para a loja. A PulsarFM não recebe comissão por estas compras.')
    if uses_amazon(catalog, published):
        link_note += ' ' + AMAZON_STATEMENT
    content = ('<section class="editorial-hero"><div><p class="eyebrow">Gear / Tecnologia</p>'
               f'<h1>{esc(editorial["title"])}</h1>'
               '<p class="lead">A música é o ponto de partida.<br>O equipamento vem a seguir.</p>'
               '<p>Guias para ouvir melhor, montar o teu canto e começar a criar. '
               'Sem jargão de folheto nem pressa de te vender nada: primeiro percebes, depois escolhes.</p>'
               '<a class="text-link" href="#guias">Explorar os guias <span aria-hidden="true">↓</span></a></div>'
               '<figure><img src="/img/gear-editorial.svg" width="720" height="520" '
               'alt="Ilustração de um gira-discos, auscultadores e um disco, nas cores néon da PulsarFM">'
               '<figcaption>Do primeiro play ao último lado B.</figcaption></figure></section>'
               '<section id="guias" class="guides-index"><h2>Encontra a tua frequência</h2>' +
               "\n".join(guide_link(article, i) for i, article in enumerate(editorial["articles"], 1)) +
               '</section><aside class="editorial-policy"><h2>Conteúdo primeiro. Sempre.</h2>'
               '<p>Os nossos guias ajudam-te a comparar formatos, ligações e necessidades. '
               'Quando incluímos produtos, explicamos a escolha e identificamos os links de afiliado. '
               'Só apresentamos um produto como testado quando existe um teste da redação.</p>'
               '<p>' + link_note + ' <a href="/privacidade.html#afiliados">Saber mais</a>.</p></aside>' +
               json_ld({"@type": "BreadcrumbList", "itemListElement": [
                   {"@type": "ListItem", "position": 1, "name": "Pulsar FM", "item": SITE + "/"},
                   {"@type": "ListItem", "position": 2, "name": "Recomendações", "item": SITE + "/recomendacoes/"}]}) +
               json_ld({"@type": "ItemList", "name": editorial["title"], "itemListElement": [
                   {"@type": "ListItem", "position": i, "name": article["title"],
                    "url": f'{SITE}/recomendacoes/{article["slug"]}/'}
                   for i, article in enumerate(editorial["articles"], 1)]}))
    return page(editorial.get("seoTitle") or editorial["title"],
                editorial.get("metaDescription") or editorial["description"], "/recomendacoes/", content)


def generate(catalog, editorial):
    products = validate_catalog(catalog)
    if editorial.get("schemaVersion") != 1:
        raise ValueError("Unsupported editorial schemaVersion")
    pages = {"recomendacoes/index.html": render_hub(editorial, catalog)}
    slugs = set()
    for article in editorial["articles"]:
        slug = article["slug"]
        if not SLUG.fullmatch(slug) or slug in slugs:
            raise ValueError("Articles need unique safe slugs")
        if len(set(article["productIds"])) != len(article["productIds"]):
            raise ValueError("Do not repeat a product card in the same article")
        slugs.add(slug)
        pages[f"recomendacoes/{slug}/index.html"] = render_article(article, editorial["articles"], catalog, products)
    return pages


def update_sitemap(editorial):
    path = ROOT / "sitemap.xml"
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", ns)
    tree = ET.parse(path)
    root = tree.getroot()
    for item in list(root):
        if item.findtext(f"{{{ns}}}loc", "").startswith("https://pulsarfm.eu/recomendacoes/"):
            root.remove(item)
    urls = [("/recomendacoes/", editorial["updatedAt"])] + [
        (f'/recomendacoes/{article["slug"]}/', article["updatedAt"]) for article in editorial["articles"]]
    for url, updated in urls:
        date.fromisoformat(updated)
        item = ET.SubElement(root, f"{{{ns}}}url")
        for key, value in (("loc", "https://pulsarfm.eu" + url), ("lastmod", updated),
                           ("changefreq", "monthly"), ("priority", "0.60")):
            ET.SubElement(item, f"{{{ns}}}{key}").text = value
    ET.indent(tree, space="  ")
    tree.write(path, encoding="UTF-8", xml_declaration=True)


def main():
    catalog = read_json(ROOT / "data" / "affiliates.json")
    editorial = read_json(ROOT / "data" / "recommendations.json")
    pages = generate(catalog, editorial)  # Validate every page before writing anything.
    for name, content in pages.items():
        path = ROOT / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    update_sitemap(editorial)
    print(f"Generated {len(pages)} editorial pages and updated sitemap.xml")


if __name__ == "__main__":
    main()

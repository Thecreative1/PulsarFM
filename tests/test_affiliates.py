import copy
import json
import re
from datetime import date, timedelta
from html.parser import HTMLParser
from pathlib import Path
import sys
import unittest
from urllib.parse import parse_qs, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import gen_recommendations as gen
from import_awin_feed import import_rows, normalize_row


def fixture():
    """Awin catalog used to keep the generic Awin support covered; the live catalog is Amazon-only."""
    catalog = copy.deepcopy(gen.read_json(gen.ROOT / 'data/affiliates.json'))
    catalog['awin'] = {'publisherId': '123'}
    catalog['merchants']['worten-pt'] = {
        'name': 'Worten', 'network': 'awin', 'advertiserId': '456',
        'allowedDestinationHosts': ['www.worten.pt', 'worten.pt'], 'cta': 'Ver na Worten'}
    product = {
        'id': 'produto-exemplo', 'status': 'published', 'linkType': 'affiliate', 'merchant': 'worten-pt',
        'name': 'Auscultadores de teste <A&B>', 'description': 'Descrição editorial curta.',
        'image': '/img/gear-editorial.svg', 'imageAlt': 'Ilustração de equipamento de áudio',
        'destinationUrl': 'https://www.worten.pt/produtos/teste?color=preto&size=M',
        'affiliateUrl': '', 'price': None}
    catalog['products'] = [product]
    return catalog, product


def strip_products(editorial):
    """Drop every real product reference so a fixture catalog can be rendered alone."""
    for article in editorial['articles']:
        article['productIds'] = []
        article.pop('badges', None)
        article.pop('quickPicks', None)
        if article.get('comparison'):
            article['comparison'].pop('rowProducts', None)
        for item in article.get('faq', []):
            item.pop('productIds', None)
        for section in article['sections']:
            section.pop('productLinks', None)
    return editorial


def headphones(editorial):
    """The headphones guide, found by slug: the hub order changes (seasonal guides go first)."""
    return next(a for a in editorial['articles'] if a['slug'] == 'melhores-auscultadores')


def use_product(article, product):
    """Put a fixture product in a guide, with the quick pick every guide with products needs."""
    article['productIds'] = [product['id']]
    article['quickPicks'] = [{'label': 'Teste', 'productId': product['id'], 'note': 'Escolha de teste.'}]


def amazon_fixture():
    catalog = copy.deepcopy(gen.read_json(gen.ROOT / 'data/affiliates.json'))
    product = gen.read_json(gen.ROOT / 'templates/product.json')
    product.update(status='published', name='Auscultadores <A&B>')
    catalog['products'] = [product]
    return catalog, product


class HTMLInventory(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.ids, self.links, self.images = [], [], []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a':
            self.links.append(attrs)
        if tag == 'img':
            self.images.append(attrs)


class AffiliateTests(unittest.TestCase):
    def setUp(self):
        self.catalog, self.product = fixture()
        # The fixture catalog only has one product: drop every real reference.
        self.editorial = strip_products(copy.deepcopy(gen.read_json(gen.ROOT / 'data/recommendations.json')))

    def test_badge_comparison_and_faq(self):
        article = headphones(self.editorial)
        use_product(article, self.product)
        article['badges'] = {self.product['id']: 'Até 50€ <b>'}
        article['comparison'] = {'caption': 'Tabela', 'columns': ['Modelo', 'Nota'],
                                 'rows': [['A', 'x < y']]}
        article['faq'] = [{'q': 'Pergunta?', 'a': 'Resposta </script> segura'}]
        html = gen.generate(self.catalog, self.editorial)['recomendacoes/melhores-auscultadores/index.html']
        self.assertIn('<p class="product-badge">Até 50€ &lt;b&gt;</p>', html)
        self.assertIn('<td>x &lt; y</td>', html)
        self.assertIn('"@type": "FAQPage"', html)
        self.assertNotIn('Resposta </script>', html)
        article['comparison']['rows'] = [['A']]
        with self.assertRaises(ValueError):
            gen.generate(self.catalog, self.editorial)
        article.pop('comparison')
        article['badges'] = {'not-in-article': 'x'}
        with self.assertRaises(ValueError):
            gen.generate(self.catalog, self.editorial)

    def test_deep_link_roundtrip_and_clickref(self):
        url = gen.affiliate_url(self.catalog, self.product)
        params = parse_qs(urlsplit(url).query)
        self.assertEqual(params['ued'], [self.product['destinationUrl']])
        self.assertEqual(params['awinmid'], ['456'])
        self.assertEqual(params['awinaffid'], ['123'])
        self.assertEqual(params['clickref'], ['pulsarfm-produto-exemplo'])

    def test_ready_links_keep_tracking_parameters(self):
        self.product['affiliateUrl'] = 'https://www.awin1.com/pclick.php?p=99&a=123&m=456&clickref=editorial'
        self.assertEqual(gen.affiliate_url(self.catalog, self.product), self.product['affiliateUrl'])

    def test_direct_product_needs_no_awin_and_is_not_sponsored(self):
        self.product['linkType'] = 'direct'
        self.catalog['awin']['publisherId'] = ''
        self.catalog['merchants']['worten-pt']['advertiserId'] = ''
        gen.validate_catalog(self.catalog)
        link = HTMLInventory(gen.render_product(self.catalog, self.product, 'recommendation-1')).links[0]
        self.assertEqual(link['href'], self.product['destinationUrl'])
        self.assertEqual(link['rel'], 'noopener')
        self.assertEqual(link['target'], '_blank')
        self.assertNotIn('data-affiliate-link', link)
        use_product(headphones(self.editorial), self.product)
        html = gen.generate(self.catalog, self.editorial)['recomendacoes/melhores-auscultadores/index.html']
        self.assertNotIn('affiliate-disclosure', html)
        self.assertIn('sem comissão', html)

    def test_direct_links_validate_destination_and_require_explicit_conversion(self):
        self.product['linkType'] = 'direct'
        with self.assertRaises(ValueError):
            gen.product_url(self.catalog, dict(self.product, destinationUrl='https://evil.test/'))
        with self.assertRaises(ValueError):
            gen.product_url(self.catalog, dict(self.product, affiliateUrl='https://tidd.ly/test'))
        self.assertEqual(gen.product_url(self.catalog, self.product), self.product['destinationUrl'])
        self.product['linkType'] = 'affiliate'
        self.assertIn('awin1.com', gen.product_url(self.catalog, self.product))
        self.product['affiliateUrl'] = 'https://tidd.ly/test-link'
        self.assertEqual(gen.affiliate_url(self.catalog, self.product), self.product['affiliateUrl'])

    def test_unsafe_and_incomplete_urls_fail_closed(self):
        for value in ('javascript:alert(1)', 'http://www.worten.pt/x',
                      'https://www.worten.pt.evil.test/x', 'https://user@www.worten.pt/x',
                      'https://www.worten.pt\\@evil.test/x', 'https://www.worten.pt:8080/x'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                gen.affiliate_url(self.catalog, dict(self.product, destinationUrl=value))
        for value in ('https://www.worten.pt/x', 'https://www.awin1.com/cread.php',
                      'https://www.awin1.com/pclick.php?p=99&a=999&m=456', 'https://tidd.ly/'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                gen.affiliate_url(self.catalog, dict(self.product, affiliateUrl=value))

    def test_missing_credentials_require_a_ready_link(self):
        self.catalog['awin']['publisherId'] = ''
        with self.assertRaises(ValueError):
            gen.validate_catalog(self.catalog)
        self.product['affiliateUrl'] = 'https://tidd.ly/test-link'
        gen.validate_catalog(self.catalog)

    def test_product_html_is_safe_and_accessible(self):
        self.product['description'] = '<img src=x onerror=alert(1)>'
        html = gen.render_product(self.catalog, self.product, 'recommendation-1')
        parsed = HTMLInventory(html)
        link = parsed.links[0]
        self.assertEqual(link['rel'], 'sponsored nofollow noopener noreferrer')
        self.assertEqual(link['target'], '_blank')
        self.assertEqual(link['data-product-name'], self.product['name'])
        self.assertEqual(link['data-merchant'], 'worten-pt')
        self.assertEqual(link['data-position'], 'recommendation-1')
        self.assertNotIn('<img src=x', html)
        self.assertEqual(len(parsed.images), 1)
        self.assertIn('nova aba', html)
        self.assertNotIn('product-price', html)

    def test_optional_price_freshness_and_validation(self):
        today = date(2026, 9, 29)
        price = {'amount': 129.99, 'currency': 'EUR', 'checkedAt': today.isoformat()}
        self.assertIn('129,99 €', gen.render_price(price, today))
        for delta in (-1, 8):
            price['checkedAt'] = (today - timedelta(days=delta)).isoformat()
            self.assertEqual(gen.render_price(price, today), '')
        for amount in ('NaN', 'Infinity', -1):
            with self.assertRaises(ValueError):
                gen.validate_price(dict(price, amount=amount))

    def test_article_cards_inline_links_and_disclosure(self):
        article = headphones(self.editorial)
        use_product(article, self.product)
        article['sections'][0]['productLinks'] = [{'productId': self.product['id'], 'label': 'Ver este modelo'}]
        html = gen.generate(self.catalog, self.editorial)['recomendacoes/melhores-auscultadores/index.html']
        parsed = HTMLInventory(html)
        links = [link for link in parsed.links if 'data-affiliate-link' in link]
        self.assertEqual(len(links), 3)
        self.assertEqual({link['data-position'] for link in links}, {'quick-1', 'inline-1-1', 'recommendation-1'})
        self.assertIn('sem custo adicional para ti', html)
        self.assertEqual(len(parsed.ids), len(set(parsed.ids)))

    def test_drafts_are_not_public(self):
        self.product['status'] = 'draft'
        self.product['affiliateUrl'] = ''
        self.catalog['awin']['publisherId'] = ''
        headphones(self.editorial)['productIds'] = [self.product['id']]
        html = gen.generate(self.catalog, self.editorial)['recomendacoes/melhores-auscultadores/index.html']
        self.assertNotIn('data-affiliate-link', html)
        self.assertNotIn('Auscultadores de teste', html)
        self.assertNotIn('affiliate-disclosure', html)

    def test_duplicate_ids_unknown_references_and_unsafe_slugs_fail(self):
        self.catalog['products'].append(copy.deepcopy(self.product))
        with self.assertRaises(ValueError):
            gen.generate(self.catalog, self.editorial)
        self.catalog['products'].pop()
        headphones(self.editorial)['productIds'] = ['unknown-product']
        with self.assertRaises(KeyError):
            gen.generate(self.catalog, self.editorial)
        headphones(self.editorial)['slug'] = '../escape'
        with self.assertRaises(ValueError):
            gen.generate(self.catalog, self.editorial)

    def test_public_pages_have_working_local_links_and_unique_ids(self):
        catalog = gen.read_json(gen.ROOT / 'data/affiliates.json')
        self.editorial = gen.read_json(gen.ROOT / 'data/recommendations.json')
        pages = gen.generate(catalog, self.editorial)
        self.assertEqual(len(pages), 1 + len(self.editorial['articles']))
        for path, html in pages.items():
            parsed = HTMLInventory(html)
            self.assertEqual(len(parsed.ids), len(set(parsed.ids)), path)
            self.assertEqual((gen.ROOT / path).read_text(encoding='utf-8'), html)
            for link in parsed.links:
                url = urlsplit(link.get('href', ''))
                if not url.scheme and url.path:
                    target = gen.ROOT / url.path.lstrip('/')
                    self.assertTrue(target.exists(), str(target))
        home = HTMLInventory((gen.ROOT / 'index.html').read_text(encoding='utf-8'))
        self.assertEqual(home.ids.count('recommendations-link'), 1)


class AmazonTests(unittest.TestCase):
    def setUp(self):
        self.catalog, self.product = amazon_fixture()

    def test_link_is_built_from_asin_with_the_pulsarfm_tag(self):
        url = gen.product_url(self.catalog, self.product)
        self.assertEqual(url, f'https://www.amazon.es/dp/{self.product["asin"]}/?tag=pulsarfm-21')
        link = HTMLInventory(gen.render_product(self.catalog, self.product, 'recommendation-1')).links[0]
        self.assertEqual(link['href'], url)
        self.assertEqual(link['rel'], 'sponsored nofollow noopener noreferrer')
        self.assertEqual(link['target'], '_blank')
        self.assertEqual(link['data-affiliate-platform'], 'amazon')
        self.assertEqual(link['data-tracking-id'], 'pulsarfm-21')
        self.assertEqual(link['data-product-category'], self.product['category'])
        self.assertEqual(link['data-product-name'], 'Auscultadores <A&B>')

    def test_other_tags_and_invalid_asins_fail_closed(self):
        merchant = self.catalog['merchants']['amazon-es']
        for tag in ('ondecortar-21', '', None):
            merchant['trackingId'] = tag
            with self.subTest(tag=tag), self.assertRaises(ValueError):
                gen.product_url(self.catalog, self.product)
        merchant['trackingId'] = 'pulsarfm-21'
        for asin in ('', 'b0btjd6lcl', 'B0BTJD6LC', 'B0BTJD6LCL/?tag=x', None):
            with self.subTest(asin=asin), self.assertRaises(ValueError):
                gen.product_url(self.catalog, dict(self.product, asin=asin))

    def test_category_required_and_image_uses_local_category_illustration(self):
        self.product.pop('image', None)
        html = gen.render_product(self.catalog, self.product, 'recommendation-1')
        image = HTMLInventory(html).images[0]
        self.assertEqual(image['src'], '/img/gear/auscultadores.svg')
        self.assertTrue((gen.ROOT / image['src'].lstrip('/')).exists())
        self.assertNotIn('amazon.com/images', html)
        self.product['category'] = 'Categoria sem ilustração'
        html = gen.render_product(self.catalog, self.product, 'recommendation-1')
        self.assertEqual(HTMLInventory(html).images[0]['src'], gen.DEFAULT_IMAGE)
        self.product['category'] = ''
        with self.assertRaises(ValueError):
            gen.validate_catalog(self.catalog)
        self.product['category'] = 'Auscultadores'
        self.product['pros'] = 'not a list of text'
        with self.assertRaises(ValueError):
            gen.validate_catalog(self.catalog)

    def test_notes_stay_in_data_and_disclosure_is_shown(self):
        self.product.update(pros=['Pró editorial único'], cons=['Contra editorial único'],
                            bestFor='Uso ideal editorial único')
        editorial = strip_products(gen.read_json(gen.ROOT / 'data/recommendations.json'))
        use_product(headphones(editorial), self.product)
        html = gen.generate(self.catalog, editorial)['recomendacoes/melhores-auscultadores/index.html']
        for note in ('Pró editorial único', 'Contra editorial único', 'Uso ideal editorial único'):
            self.assertNotIn(note, html)
        self.assertIn('pode receber uma pequena comissão, sem custo adicional para ti', html)
        self.assertIn(gen.AMAZON_STATEMENT, html)
        self.assertIn('Ver preço na Amazon', html)

    def test_published_pages_only_link_to_amazon_es_with_the_pulsarfm_tag(self):
        catalog = gen.read_json(gen.ROOT / 'data/affiliates.json')
        pages = gen.generate(catalog, gen.read_json(gen.ROOT / 'data/recommendations.json'))
        self.assertIn(gen.AMAZON_STATEMENT, pages['recomendacoes/index.html'])
        for path, html in pages.items():
            self.assertNotIn('não recebe comissão', html, path)
            self.assertNotIn('sem comissão', html, path)
            for link in HTMLInventory(html).links:
                if 'data-affiliate-link' in link:
                    url = urlsplit(link['href'])
                    self.assertEqual(url.hostname, 'www.amazon.es', path)
                    self.assertEqual(parse_qs(url.query), {'tag': ['pulsarfm-21']}, path)
                    self.assertEqual(link['rel'], 'sponsored nofollow noopener noreferrer', path)


class SeoAndConversionTests(unittest.TestCase):
    def setUp(self):
        self.catalog = gen.read_json(gen.ROOT / 'data/affiliates.json')
        self.editorial = gen.read_json(gen.ROOT / 'data/recommendations.json')
        self.pages = gen.generate(self.catalog, self.editorial)

    def json_ld(self, html):
        return [json.loads(block) for block in
                re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)]

    def test_titles_descriptions_and_structured_data(self):
        for article in self.editorial['articles']:
            html = self.pages[f'recomendacoes/{article["slug"]}/index.html']
            self.assertIn(f'<title>{gen.esc(article["seoTitle"])} | Pulsar FM</title>', html)
            self.assertIn(f'<h1>{gen.esc(article["title"])}</h1>', html)  # H1 unchanged
            self.assertIn(f'content="{gen.esc(article["metaDescription"])}"', html)
            types = {block['@type'] for block in self.json_ld(html)}
            self.assertTrue({'BreadcrumbList', 'Article', 'ItemList'} <= types, article['slug'])
            self.assertNotIn('www.pulsarfm.eu', html)
        hub = self.json_ld(self.pages['recomendacoes/index.html'])
        self.assertEqual({block['@type'] for block in hub}, {'BreadcrumbList', 'ItemList'})

    def test_quick_picks_and_table_links_are_tracked_affiliate_links(self):
        for article in self.editorial['articles']:
            html = self.pages[f'recomendacoes/{article["slug"]}/index.html']
            links = [link for link in HTMLInventory(html).links if 'data-affiliate-link' in link]
            positions = {link['data-position'] for link in links}
            self.assertEqual({p for p in positions if p.startswith('quick-')},
                             {f'quick-{i}' for i in range(1, len(article['quickPicks']) + 1)})
            rows = (article.get('comparison') or {}).get('rowProducts') or []
            self.assertEqual({p for p in positions if p.startswith('table-')},
                             {f'table-{i}' for i in range(1, len(rows) + 1)})
            for pick in article['quickPicks']:
                self.assertIn(f'href="#product-{pick["productId"]}"', html)
                self.assertIn(f'id="product-{pick["productId"]}"', html)

    def test_related_guides_follow_the_editorial_map_and_fail_closed(self):
        inbound = {article['slug']: 0 for article in self.editorial['articles']}
        for article in self.editorial['articles']:
            self.assertNotIn(article['slug'], article['related'])
            for slug in article['related']:
                inbound[slug] += 1
        self.assertTrue(all(count >= 1 for count in inbound.values()), inbound)
        headphones(self.editorial)['related'] = ['nao-existe']
        with self.assertRaises(ValueError):
            gen.generate(self.catalog, self.editorial)

    def test_short_note_before_the_first_store_link_and_full_disclosure_at_the_end(self):
        for article in self.editorial['articles']:
            html = self.pages[f'recomendacoes/{article["slug"]}/index.html']
            note = html.index('<a href="#divulgacao">Contém links de afiliado</a>')
            first_store_link = html.index('data-affiliate-link')
            box = html.index('id="divulgacao"')
            self.assertLess(note, first_store_link, article['slug'])
            self.assertGreater(box, html.index('class="guide-closing"'), article['slug'])
            self.assertEqual(html.count('class="affiliate-disclosure"'), 1, article['slug'])
            self.assertIn(gen.AMAZON_STATEMENT, html[box:])

    def test_faq_answers_link_to_the_store_but_json_ld_stays_plain(self):
        for article in self.editorial['articles']:
            html = self.pages[f'recomendacoes/{article["slug"]}/index.html']
            expected = {f'faq-{i}-{j}' for i, item in enumerate(article.get('faq', []), 1)
                        for j, _ in enumerate(item.get('productIds', []), 1)}
            links = [l for l in HTMLInventory(html).links if l.get('data-position', '').startswith('faq-')]
            self.assertEqual({l['data-position'] for l in links}, expected, article['slug'])
            for block in self.json_ld(html):
                if block['@type'] == 'FAQPage':
                    for question in block['mainEntity']:
                        self.assertNotIn('<a', question['acceptedAnswer']['text'])
        broken = copy.deepcopy(self.editorial)
        headphones(broken)['faq'][0]['productIds'] = ['jbl-go-5']  # not one of the headphones guide's products
        with self.assertRaisesRegex(ValueError, 'FAQ links to jbl-go-5'):
            gen.generate(self.catalog, broken)

    def test_category_bar_links_every_guide_and_marks_the_current_one(self):
        slugs = [article['slug'] for article in self.editorial['articles']]
        for path, html in self.pages.items():
            nav = re.search(r'<nav class="guide-nav"[^>]*>(.*?)</nav>', html, re.S).group(1)
            self.assertEqual(re.findall(r'href="/recomendacoes/([^/"]+)/"', nav), slugs, path)
            current = re.findall(r'href="/recomendacoes/([^/"]+)/" aria-current="page"', nav)
            self.assertEqual(current, [] if path == 'recomendacoes/index.html' else [path.split('/')[1]])

    def test_a_guide_without_its_look_fails_with_a_clear_message(self):
        cases = [
            ('navIcon', None, 'needs navIcon'),
            ('navLabel', 'Um nome demasiado comprido', 'navLabel must be short'),
            ('metaDescription', 'x' * 161, 'over 160'),
            ('illustration', '/img/gear/nao-existe.svg', 'existing neon illustration'),
            ('illustration', '/img/pulsar-og.jpg', 'existing neon illustration'),
            ('related', ['soundbars'], '2 distinct related'),
            ('quickPicks', [], 'needs quickPicks'),
        ]
        for field, value, message in cases:
            editorial = copy.deepcopy(self.editorial)
            article = headphones(editorial)
            if value is None:
                article.pop(field)
            else:
                article[field] = value
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, message):
                gen.generate(self.catalog, editorial)

    def test_orphan_guides_and_categories_without_illustration_fail(self):
        editorial = copy.deepcopy(self.editorial)
        for article in editorial['articles']:  # nobody points at the first guide any more
            article['related'] = [s for s in article['related'] if s != 'melhores-auscultadores'] + \
                [s for s in ('soundbars', 'gira-discos', 'home-studio')
                 if s != article['slug'] and s not in article['related']]
            article['related'] = article['related'][:2]
        with self.assertRaisesRegex(ValueError, 'melhores-auscultadores'):
            gen.generate(self.catalog, editorial)
        catalog = copy.deepcopy(self.catalog)
        del catalog['categoryImages']['Auscultadores']
        with self.assertRaisesRegex(ValueError, 'no illustration'):
            gen.generate(catalog, self.editorial)

    def test_bad_quick_picks_and_row_products_fail(self):
        article = headphones(self.editorial)
        article['quickPicks'].append({'label': 'X', 'productId': 'jbl-go-5', 'note': 'fora do guia'})
        with self.assertRaises(ValueError):
            gen.generate(self.catalog, self.editorial)
        article['quickPicks'].pop()
        article['comparison']['rowProducts'] = article['comparison']['rowProducts'][:-1]
        with self.assertRaises(ValueError):
            gen.generate(self.catalog, self.editorial)


class FeedTests(unittest.TestCase):
    def setUp(self):
        self.catalog, _ = fixture()
        self.row = {'merchant_id': '456', 'merchant_product_id': 'sku-10', 'aw_product_id': '99',
                    'product_name': 'Produto de teste', 'description': '<p>Som &amp; música</p>',
                    'merchant_image_url': 'https://example.com/photo.jpg',
                    'aw_deep_link': 'https://www.awin1.com/pclick.php?p=99&a=123&m=456',
                    'search_price': '59.90', 'currency': 'EUR', 'last_updated': '2026-09-20 12:00:00',
                    'in_stock': '0'}

    def test_feed_mapping_preserves_source_and_never_publishes(self):
        product = normalize_row(self.row, 'worten-pt', self.catalog)
        self.assertEqual(product['status'], 'draft')
        self.assertEqual(product['affiliateUrl'], self.row['aw_deep_link'])
        self.assertEqual(product['description'], 'Som & música')
        self.assertEqual(product['price']['checkedAt'], '2026-09-20')
        self.assertEqual(product['source']['inStock'], '0')
        self.assertEqual(product['source']['merchantProductId'], 'sku-10')

    def test_no_feed_timestamp_means_no_claimed_price(self):
        self.row['last_updated'] = ''
        self.assertIsNone(normalize_row(self.row, 'worten-pt', self.catalog)['price'])

    def test_wrong_merchant_missing_link_and_duplicates_are_rejected(self):
        with self.assertRaises(ValueError):
            import_rows([dict(self.row, merchant_id='789')], 'worten-pt', self.catalog)
        with self.assertRaises(ValueError):
            import_rows([dict(self.row, aw_deep_link='')], 'worten-pt', self.catalog)
        with self.assertRaises(ValueError):
            import_rows([self.row, self.row], 'worten-pt', self.catalog)


if __name__ == '__main__':
    unittest.main()

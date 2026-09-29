import copy
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
    catalog = copy.deepcopy(gen.read_json(gen.ROOT / 'data/affiliates.json'))
    catalog['awin']['publisherId'] = '123'
    catalog['merchants']['worten-pt']['advertiserId'] = '456'
    product = gen.read_json(gen.ROOT / 'templates/product.json')
    product.update(status='published', name='Auscultadores de teste <A&B>',
                   destinationUrl='https://www.worten.pt/produtos/teste?color=preto&size=M')
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
        self.editorial = copy.deepcopy(gen.read_json(gen.ROOT / 'data/recommendations.json'))
        for article in self.editorial['articles']:
            article['productIds'] = []

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
        self.editorial['articles'][0]['productIds'] = [self.product['id']]
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
        self.assertEqual(link['rel'], 'sponsored nofollow noopener')
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
        article = self.editorial['articles'][0]
        article['productIds'] = [self.product['id']]
        article['sections'][0]['productLinks'] = [{'productId': self.product['id'], 'label': 'Ver este modelo'}]
        html = gen.generate(self.catalog, self.editorial)['recomendacoes/melhores-auscultadores/index.html']
        parsed = HTMLInventory(html)
        links = [link for link in parsed.links if 'data-affiliate-link' in link]
        self.assertEqual(len(links), 2)
        self.assertEqual({link['data-position'] for link in links}, {'inline-1-1', 'recommendation-1'})
        self.assertIn('sem custo adicional para ti', html)
        self.assertEqual(len(parsed.ids), len(set(parsed.ids)))

    def test_drafts_are_not_public(self):
        self.product['status'] = 'draft'
        self.product['affiliateUrl'] = ''
        self.catalog['awin']['publisherId'] = ''
        self.editorial['articles'][0]['productIds'] = [self.product['id']]
        html = gen.generate(self.catalog, self.editorial)['recomendacoes/melhores-auscultadores/index.html']
        self.assertNotIn('data-affiliate-link', html)
        self.assertNotIn('Auscultadores de teste', html)
        self.assertNotIn('affiliate-disclosure', html)

    def test_duplicate_ids_unknown_references_and_unsafe_slugs_fail(self):
        self.catalog['products'].append(copy.deepcopy(self.product))
        with self.assertRaises(ValueError):
            gen.generate(self.catalog, self.editorial)
        self.catalog['products'].pop()
        self.editorial['articles'][0]['productIds'] = ['unknown-product']
        with self.assertRaises(KeyError):
            gen.generate(self.catalog, self.editorial)
        self.editorial['articles'][0]['slug'] = '../escape'
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

import copy
import json
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import unittest
from urllib.parse import urljoin, urlsplit, parse_qs
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import gen_spain as gen
from market_config import market_config

class HTML(HTMLParser):
    def __init__(self, content):
        super().__init__()
        self.links, self.ids, self.ld, self.lang, self.canonical = [], [], [], None, None
        self.collect = False
        self.buffer = ''
        self.feed(content)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html': self.lang = attrs.get('lang')
        if 'id' in attrs: self.ids.append(attrs['id'])
        if tag in ('a', 'link'): self.links.append(attrs)
        if tag == 'link' and attrs.get('rel') == 'canonical': self.canonical = attrs['href']
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.collect, self.buffer = True, ''
    def handle_data(self, data):
        if self.collect: self.buffer += data
    def handle_endtag(self, tag):
        if tag == 'script' and self.collect:
            self.ld.append(json.loads(self.buffer))
            self.collect = False

def local_path(url):
    p = urlsplit(url).path
    return ROOT / (p.lstrip('/') + 'index.html' if p.endswith('/') else p.lstrip('/'))

class SpainTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = gen.generate()
        cls.parsed = {name: HTML(content) for name, content in cls.pages.items()}

    def test_static_pages_are_complete_and_deterministic(self):
        self.assertEqual(len(self.pages), 18)
        for name, content in self.pages.items():
            with self.subTest(page=name):
                self.assertEqual((ROOT / name).read_text(encoding='utf-8'), content)
                html = self.parsed[name]
                self.assertEqual(html.lang, 'es-ES')
                self.assertEqual(html.canonical, gen.SITE + '/' + name.removesuffix('index.html'))
                self.assertEqual(len(html.ids), len(set(html.ids)))
                self.assertIn('<h1', content)
                self.assertTrue(html.ld)
                self.assertNotIn('aggregateRating', content)
                self.assertNotIn('"@type": "Review"', content)

    def test_internal_links_and_fragments_resolve(self):
        for name, html in self.parsed.items():
            for link in html.links:
                href = link.get('href', '')
                if not href or href.startswith(('mailto:', 'https:', 'http:')): continue
                # Spanish home uses base / to keep exactly the original player assets.
                base = gen.SITE + ('/' if name == 'es/index.html' else '/' + name.removesuffix('index.html'))
                target = urljoin(base, href)
                file = local_path(target)
                with self.subTest(page=name, href=href):
                    self.assertTrue(file.is_file(), target)
                    fragment = urlsplit(target).fragment
                    if fragment:
                        self.assertIn(fragment, HTML(file.read_text(encoding='utf-8')).ids)

    def test_equivalent_hreflang_is_reciprocal(self):
        pairs = gen.read_json(ROOT / 'data/locale-routes.json')['pairs']
        for pair in pairs:
            for path in pair.values():
                html = HTML(local_path(path).read_text(encoding='utf-8'))
                actual = {l.get('hreflang'): l['href'] for l in html.links if l.get('hreflang') and l.get('rel') == 'alternate'}
                self.assertEqual(actual['pt-PT'], gen.SITE + pair['pt'])
                self.assertEqual(actual['es-ES'], gen.SITE + pair['es'])
        for name in ('auriculares-cancelacion-ruido-trabajar', 'microfonos-usb-podcast-streaming', 'equipos-hi-fi-empezar', 'auriculares-bluetooth-calidad-precio', 'altavoces-bluetooth-casa', 'accesorios-audio'):
            html = HTML(self.pages['es/recomendaciones/' + name + '/index.html'])
            self.assertFalse(any(l.get('rel') == 'alternate' for l in html.links))

    def test_affiliate_market_ids_and_disclosures(self):
        count = 0
        for name, html in self.parsed.items():
            content = self.pages[name]
            for link in html.links:
                if 'data-affiliate-link' not in link: continue
                count += 1
                self.assertEqual(urlsplit(link['href']).hostname, 'www.amazon.es')
                self.assertEqual(parse_qs(urlsplit(link['href']).query), {'tag': ['pulsarfmes-21']})
                self.assertEqual(link['data-market'], 'ES')
                self.assertEqual(link['data-language'], 'es-ES')
                self.assertTrue(link['data-product-id'])
                self.assertTrue(link['data-article-slug'])
                self.assertIn('sponsored', link['rel'].split())
                self.assertLess(content.index('Publicidad: contiene enlaces de afiliado'), content.index('data-affiliate-link'))
                self.assertIn(gen.AMAZON_STATEMENT, content)
        self.assertGreater(count, 50)
        self.assertEqual(market_config('PT')['trackingId'], 'pulsarfm-21')
        config = gen.read_json(ROOT / 'data/affiliate-markets.json')
        config['markets']['PT']['trackingId'] = 'changed-21'
        with self.assertRaises(ValueError): market_config('PT', config)
        config = gen.read_json(ROOT / 'data/affiliate-markets.json')
        config['markets']['ES']['validated'] = False
        with self.assertRaises(ValueError): market_config('ES', config)

    def test_missing_spanish_tag_never_leaks_portuguese_tag(self):
        config = gen.read_json(ROOT / 'data/affiliate-markets.json')
        config['markets']['ES']['trackingId'] = None
        editorial = gen.read_json(ROOT / 'data/recommendations.es.json')
        original = gen.read_json(ROOT / 'data/affiliates.json')['products'][0]
        product = next(p for p in editorial['products'] if p['id'] == original['id'])
        link = gen.product_link(product, original, 'example', 'quick-1', config=config)
        self.assertNotIn('?tag=', link)
        self.assertNotIn('data-affiliate-link', link)

    def test_sitemap_covers_every_spanish_page_and_preserves_existing_routes(self):
        tree = ET.parse(ROOT / 'sitemap.xml')
        urls = [e.text for e in tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        self.assertEqual(len(urls), len(set(urls)))
        for filename in self.pages:
            self.assertIn(gen.SITE + '/' + filename.removesuffix('index.html'), urls)
        for g in gen.localized_genres().values():
            self.assertIn(gen.SITE + '/es/' + g['slug'] + '/', urls)
        for url in urls: self.assertTrue(local_path(url).is_file(), url)
        self.assertIn(gen.SITE + '/recomendacoes/', urls)
        self.assertIn(gen.SITE + '/en/rock-radio/', urls)

    def test_original_radio_data_and_player_dependencies_are_preserved(self):
        original = (ROOT / 'index.html').read_text(encoding='utf-8')
        spanish = self.pages['es/index.html']
        pattern = r'const radios = (.*?);\s*const translations'
        self.assertEqual(re.search(pattern, original, re.S)[1], re.search(pattern, spanish, re.S)[1])
        for library in ('webamp@2.3.1', 'butterchurn@2.6.7', 'butterchurn-presets@2.4.7'):
            self.assertIn(library, spanish)
        self.assertEqual(spanish.count('class="radio-card"'), 64)

if __name__ == '__main__': unittest.main()

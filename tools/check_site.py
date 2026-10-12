"""Static SEO/content lint without external packages or network requests."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parent.parent
SITE = 'https://pulsarfm.eu'

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.nodes, self.ids = [], []
        self.script, self.buffer = False, ''
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.nodes.append((tag, attrs))
        if 'id' in attrs: self.ids.append(attrs['id'])
        if tag == 'script' and attrs.get('type') == 'application/ld+json': self.script, self.buffer = True, ''
    def handle_data(self, text):
        if self.script: self.buffer += text
    def handle_endtag(self, tag):
        if tag == 'script' and self.script:
            json.loads(self.buffer)
            self.script = False

def file_for(url):
    path = urlsplit(url).path
    return ROOT / (path.lstrip('/') + 'index.html' if path.endswith('/') else path.lstrip('/'))

def main():
    ns = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
    urls = [e.text for e in ET.parse(ROOT / 'sitemap.xml').findall('.//' + ns + 'loc')]
    assert len(urls) == len(set(urls)), 'Duplicate sitemap entries'
    titles, descriptions, spanish = set(), set(), 0
    links_checked = 0
    for url in urls:
        file = file_for(url)
        assert file.is_file(), 'Missing sitemap page: ' + url
        text = file.read_text(encoding='utf-8')
        page = Page(text)
        canonicals = [a['href'] for tag, a in page.nodes if tag == 'link' and a.get('rel') == 'canonical']
        assert canonicals == [url], 'Canonical mismatch: ' + url
        assert len(page.ids) == len(set(page.ids)), 'Duplicate HTML IDs: ' + url
        assert '<h1' in text, 'Missing heading: ' + url
        assert 'www.pulsarfm.eu' not in text, 'Wrong canonical host: ' + url
        for tag, attrs in page.nodes:
            if tag == 'link' and attrs.get('rel') == 'alternate':
                target = file_for(attrs['href'])
                assert target.is_file(), 'Missing alternate: ' + attrs['href']
                assert url in target.read_text(encoding='utf-8'), 'Nonreciprocal alternate: ' + url
            if tag != 'a' or not attrs.get('href'): continue
            href = attrs['href']
            if href.startswith(('mailto:', 'https:', 'http:')): continue
            base = SITE + '/' if '<base href="/">' in text else url
            target_url = urljoin(base, href)
            target_file = file_for(target_url)
            assert target_file.is_file(), 'Broken internal link: ' + url + ' -> ' + href
            if urlsplit(target_url).fragment:
                target_page = Page(target_file.read_text(encoding='utf-8'))
                assert urlsplit(target_url).fragment in target_page.ids, 'Missing anchor: ' + target_url
            links_checked += 1
        if '/es/' in url:
            spanish += 1
            assert next(a['lang'] for tag, a in page.nodes if tag == 'html') == 'es-ES', 'Wrong Spanish locale'
            title = re.search(r'<title>(.*?)</title>', text, re.S)[1]
            description = next(a['content'] for tag, a in page.nodes if tag == 'meta' and a.get('name') == 'description')
            assert title not in titles and description not in descriptions, 'Duplicate Spanish metadata'
            titles.add(title); descriptions.add(description)
            assert not any('noindex' in a.get('content', '') for tag, a in page.nodes if tag == 'meta' and a.get('name') == 'robots')
    assert spanish == 26, 'Expected 26 complete Spanish pages'
    print(f'Static site lint passed: {len(urls)} indexable pages, {spanish} Spanish, {links_checked} internal links')

if __name__ == '__main__': main()


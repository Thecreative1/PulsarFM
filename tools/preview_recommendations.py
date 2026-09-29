"""Local-only product demo. Synthetic links and analytics never contact Awin or Google.

python tools/preview_recommendations.py
Open http://127.0.0.1:4174/__preview__/?affiliate_debug=1
"""
from datetime import date
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

from gen_recommendations import ROOT, affiliate_url, generate, read_json, esc


def demo_page():
    catalog = read_json(ROOT / 'data/affiliates.json')
    editorial = read_json(ROOT / 'data/recommendations.json')
    # Synthetic IDs are used only in memory and the generated link is replaced below.
    catalog['awin']['publisherId'] = '123'
    catalog['merchants']['worten-pt']['advertiserId'] = '456'
    product = read_json(ROOT / 'templates/product.json')
    product.update(status='published', name='Produto de demonstração',
                   description='Exemplo visual do componente. Substitui por um produto revisto pela redação, com fotografia e link Awin reais.',
                   destinationUrl='https://www.worten.pt/',
                   price={'amount': '99.90', 'currency': 'EUR', 'checkedAt': date.today().isoformat()})
    catalog['products'] = [product]
    # Keep the demo independent of any real product selections added later.
    for guide in editorial['articles']:
        guide['productIds'] = []
        for section in guide['sections']:
            section['productLinks'] = []
    article = editorial['articles'][0]
    article['productIds'] = [product['id']]
    article['sections'][0]['productLinks'] = [{'productId': product['id'], 'label': 'Experimentar o link no texto'}]
    html = generate(catalog, editorial)['recomendacoes/melhores-auscultadores/index.html']
    html = html.replace(esc(affiliate_url(catalog, product)), '/__preview__/destino')
    html = html.replace('<meta name="viewport"', '<meta name="robots" content="noindex,nofollow"><meta name="viewport"')
    # Existing gtag is an in-memory sink, so affiliate-analytics.js never loads Google.
    sink = """<script>
      window.dataLayer = [];
      window.gtag = function () {
        window.dataLayer.push(arguments);
        if (arguments[0] === 'event') {
          document.getElementById('demo-events').textContent = JSON.stringify({event: arguments[1], ...arguments[2]}, null, 2);
        }
      };
    </script>"""
    html = html.replace('<script src="/assets/affiliate-analytics.js"', sink + '<script src="/assets/affiliate-analytics.js"')
    notice = """<aside class="affiliate-disclosure"><h2>Demonstração local</h2>
      <p>Produto e preço fictícios, apenas para testar o componente. Os botões abrem um destino local.
      Aceita os cookies e clica num link para ver o evento abaixo. Nenhum evento é enviado à Google ou à Awin.</p>
      <pre id="demo-events" style="white-space:pre-wrap;overflow-wrap:anywhere">Ainda sem eventos.</pre></aside>"""
    return html.replace('<article class="guide">', notice + '<article class="guide">')


class PreviewHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        path = urlsplit(self.path).path
        if path.rstrip('/') == '/__preview__':
            content = demo_page()
        elif path == '/__preview__/destino':
            content = '<!doctype html><html lang="pt"><meta charset="utf-8"><title>Destino de teste</title><h1>Link de demonstração aberto</h1><p>Não foi feita nenhuma ligação à Awin ou à Worten. Podes fechar esta aba.</p></html>'
        else:
            return super().do_GET()
        body = content.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == '__main__':
    server = ThreadingHTTPServer(('127.0.0.1', 4174), partial(PreviewHandler, directory=str(ROOT)))
    print('Demo: http://127.0.0.1:4174/__preview__/?affiliate_debug=1', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

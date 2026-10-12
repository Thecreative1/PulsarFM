"""Only reviewed equivalent pages receive reciprocal hreflang."""
import json
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://pulsarfm.eu"

def equivalent(path):
    pairs = json.loads((ROOT / "data/locale-routes.json").read_text(encoding="utf-8"))["pairs"]
    return next((pair for pair in pairs if path in pair.values()), None)

def alternates(path):
    pair = equivalent(path)
    if not pair:
        return ""
    return "\n".join(f'<link rel="alternate" hreflang="{lang}" href="{SITE}{escape(pair[key], quote=True)}">' for key, lang in (("pt", "pt-PT"), ("es", "es-ES")))

def language_switch(path, language="pt"):
    pair = equivalent(path) or {"pt": "/recomendacoes/", "es": "/es/recomendaciones/"}
    links = []
    for key, lang in (("pt", "pt-PT"), ("es", "es-ES")):
        current = ' aria-current="page"' if key == language else ""
        target = pair[key] + ("?lang=pt" if key == "pt" and pair[key] == "/" else "")
        links.append(f'<a href="{escape(target, quote=True)}" lang="{lang}" data-site-language="{key}"{current}>{key.upper()}</a>')
    return '<nav class="locale-nav" aria-label="Idioma">' + ' <span aria-hidden="true">|</span> '.join(links) + '</nav>'

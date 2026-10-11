# -*- coding: utf-8 -*-
"""Tell Bing (and the other IndexNow engines) which pages changed.

Run AFTER the push is live on GitHub Pages (~1-2 min), from the repo root:

  python tools/indexnow.py                 # pages changed in the last commit
  python tools/indexnow.py --since HEAD~3  # pages changed since a given commit
  python tools/indexnow.py --all           # every URL in sitemap.xml
  python tools/indexnow.py https://pulsarfm.eu/recomendacoes/soundbars/

The key file (<KEY>.txt at the site root) must stay deployed, or Bing rejects
the submissions. Only submit pages that really changed: spamming unchanged URLs
gets the key ignored.
"""
import os, re, sys, json, subprocess, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "pulsarfm.eu"
KEY = "50e4b7991507f63207a14e80de566032"
ENDPOINT = "https://api.indexnow.org/indexnow"


def sitemap_urls():
    with open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8") as f:
        return re.findall(r"<loc>([^<]+)</loc>", f.read())


def changed_urls(since):
    out = subprocess.run(["git", "diff", "--name-only", since, "HEAD"],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout
    known = set(sitemap_urls())
    urls = []
    for path in out.split():
        if path == "index.html":
            url = "https://%s/" % HOST
        elif path.endswith("/index.html"):
            url = "https://%s/%s" % (HOST, path[:-len("index.html")])
        elif path.endswith(".html"):
            url = "https://%s/%s" % (HOST, path)
        else:
            continue
        if url in known and url not in urls:
            urls.append(url)
    return urls


def submit(urls):
    body = json.dumps({
        "host": HOST,
        "key": KEY,
        "keyLocation": "https://%s/%s.txt" % (HOST, KEY),
        "urlList": urls,
    }).encode("utf-8")
    req = urllib.request.Request(ENDPOINT, data=body, method="POST",
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code


def main(args):
    if "--all" in args:
        urls = sitemap_urls()
    elif "--since" in args:
        urls = changed_urls(args[args.index("--since") + 1])
    elif args:
        urls = [a for a in args if a.startswith("https://%s/" % HOST)]
    else:
        urls = changed_urls("HEAD~1")
    if not urls:
        print("Nothing to submit (no sitemap pages changed).")
        return 0
    for u in urls:
        print("  " + u)
    status = submit(urls)
    # 200 = accepted, 202 = accepted while the key is still being validated
    print("IndexNow: HTTP %s for %d URL(s)" % (status, len(urls)))
    return 0 if status in (200, 202) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

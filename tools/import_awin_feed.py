"""Offline Awin CSV -> reviewable drafts. Never downloads or publishes a feed.

Usage: python tools/import_awin_feed.py feed.csv --merchant worten-pt --output drafts.json
"""
import argparse
import csv
from datetime import date, datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import re

from gen_recommendations import ROOT, affiliate_url, image_url, positive_id, read_json, validate_price


class PlainText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_data(self, value):
        self.parts.append(value)


def plain_text(value):
    parser = PlainText()
    parser.feed(value or "")
    return " ".join(" ".join(parser.parts).split())


def normalize_row(row, merchant_id, catalog):
    merchant = catalog["merchants"][merchant_id]
    if not positive_id(merchant.get("advertiserId")):
        raise ValueError("Configure the merchant advertiserId before importing a feed")
    if row.get("merchant_id", "").strip() != str(merchant["advertiserId"]):
        raise ValueError("Feed merchant_id must match the configured advertiserId")
    source_id = (row.get("merchant_product_id") or row.get("aw_product_id") or "").strip()
    slug = re.sub(r"[^a-z0-9]+", "-", source_id.lower()).strip("-")
    name = plain_text(row.get("product_name"))
    if not slug or not name:
        raise ValueError("Feed row needs a product ID and product_name")
    image = (row.get("merchant_image_url") or row.get("aw_image_url") or "").strip()
    image_url(image)
    updated = (row.get("last_updated") or "").strip()
    price = None
    if row.get("search_price") and row.get("currency") and updated:
        # Feed timestamp, not import time: do not turn stale offers into fresh prices.
        try:
            checked = date.fromisoformat(updated[:10])
        except ValueError:
            checked = None
        if checked:
            price = {"amount": row["search_price"].strip(), "currency": row["currency"].strip().upper(),
                     "checkedAt": checked.isoformat()}
            validate_price(price)
    product = {
        "id": f"{merchant_id}-{slug}", "status": "draft", "merchant": merchant_id,
        "name": name,
        "description": plain_text(row.get("product_short_description") or row.get("description"))[:320],
        "image": image, "imageAlt": name,
        "destinationUrl": (row.get("merchant_deep_link") or "").strip(),
        "affiliateUrl": (row.get("aw_deep_link") or "").strip(),
        "price": price,
        "source": {
            "type": "awin-feed", "merchantProductId": row.get("merchant_product_id", ""),
            "awinProductId": row.get("aw_product_id", ""), "updatedAt": updated,
            "importedAt": datetime.now(timezone.utc).isoformat(),
            "inStock": row.get("in_stock", ""), "isForSale": row.get("is_for_sale", ""),
        },
    }
    if not product["affiliateUrl"]:
        raise ValueError("Feed row needs aw_deep_link; do not replace it with a shop URL")
    affiliate_url(catalog, product)
    return product


def import_rows(rows, merchant_id, catalog):
    products, seen = [], set()
    for line, row in enumerate(rows, 2):
        try:
            product = normalize_row(row, merchant_id, catalog)
            if product["id"] in seen:
                raise ValueError("Duplicate product ID after normalization")
            seen.add(product["id"])
            products.append(product)
        except (ValueError, KeyError) as error:
            raise ValueError(f"CSV line {line}: {error}") from error
    if not products:
        raise ValueError("Feed contains no product rows")
    return products


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--merchant", required=True)
    parser.add_argument("--output", required=True, type=Path, help="New JSON draft file; existing files are never overwritten")
    parser.add_argument("--delimiter", default=",")
    args = parser.parse_args()
    catalog = read_json(ROOT / "data" / "affiliates.json")
    try:
        with args.input.open(encoding="utf-8-sig", newline="") as handle:
            products = import_rows(csv.DictReader(handle, delimiter=args.delimiter), args.merchant, catalog)
        with args.output.open("x", encoding="utf-8") as handle:
            json.dump(products, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
    except (ValueError, KeyError, OSError) as error:
        parser.exit(1, f"Import failed: {error}\n")
    print(f"Imported {len(products)} draft products. Review before adding to data/affiliates.json.")


if __name__ == "__main__":
    main()

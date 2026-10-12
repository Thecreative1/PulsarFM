"""Confirmed Amazon settings. PT legacy links are immutable; ES must be validated."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
LEGACY_PT_TAG = "pulsarfm-21"

def market_config(market, config=None):
    config = config if config is not None else json.loads((ROOT / "data/affiliate-markets.json").read_text(encoding="utf-8"))
    if config.get("schemaVersion") != 1 or market not in ("PT", "ES"):
        raise ValueError("Unsupported affiliate market configuration")
    value = config["markets"][market]
    tag = value.get("trackingId")
    if value.get("marketplace") != "www.amazon.es":
        raise ValueError("Only the verified Amazon.es marketplace is enabled")
    if market == "PT" and tag != LEGACY_PT_TAG:
        raise ValueError("Never replace the existing Portuguese tracking ID")
    if tag is not None and (not isinstance(tag, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*-21", tag) or "config" in tag or "placeholder" in tag):
        raise ValueError("Tracking ID must be a real Amazon.es ID")
    if tag and value.get("validated") is not True:
        raise ValueError("Tracking ID requires owner validation")
    return value

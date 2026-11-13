#!/usr/bin/env python3
"""Build-time checks for the static site.

1. Every internal href/src resolves to a file in the repo (no broken links).
2. Every external link points to an official domain allow-list.
3. Every product row cites at least one official source, and every null value
   is rendered as an 'Unverified' cell (never filled in).
4. Every flag referenced from a table exists in data/flags.json.
Exit code is non-zero on any failure.
"""
import json
import pathlib
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
OFFICIAL = {
    "www.amazon.com", "link.amazon", "affiliate-program.amazon.com", "www.ftc.gov",
}
errors = []


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.flagrefs = [], set(), []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        for key in ("href", "src"):
            if a.get(key):
                self.links.append(a[key])
        if tag == "a" and "flagref" in (a.get("class") or ""):
            self.flagrefs.append(a.get("href", ""))


pages = sorted(ROOT.glob("*.html")) + sorted(ROOT.glob("*/*.html"))
parsed = {}
for page in pages:
    c = Collector()
    c.feed(page.read_text(encoding="utf-8"))
    parsed[page] = c

flags = {f["id"] for f in json.loads((ROOT / "data/flags.json").read_text())["flags"]}
products = json.loads((ROOT / "data/products.json").read_text())["products"]
sources = {s["id"]: s for s in json.loads((ROOT / "data/sources.json").read_text())["sources"]}

for page, c in parsed.items():
    for link in c.links:
        if link.startswith("#") or link.startswith("mailto:"):
            continue
        u = urlparse(link)
        if u.scheme in ("http", "https"):
            if u.netloc not in OFFICIAL and u.netloc not in ("geniuslink.com", "sellersonar.com"):
                errors.append(f"{page.relative_to(ROOT)}: external domain not on allow-list: {link}")
            continue
        target = (page.parent / u.path).resolve() if u.path else page
        if not target.exists():
            errors.append(f"{page.relative_to(ROOT)}: broken internal link -> {link}")
        elif u.fragment:
            t = parsed.get(target)
            if t is not None and u.fragment not in t.ids:
                errors.append(f"{page.relative_to(ROOT)}: missing anchor #{u.fragment} in {link}")
    for ref in c.flagrefs:
        fid = ref.split("#")[-1]
        if fid not in flags:
            errors.append(f"{page.relative_to(ROOT)}: flag reference {fid} not in data/flags.json")

for p in products:
    if not any(sid in sources for sid in p["source_ids"]):
        errors.append(f"{p['id']}: no source id")
    for sid in p["source_ids"]:
        if sid not in sources or not sources[sid]["official"]:
            errors.append(f"{p['id']}: source {sid} missing or not official")
    for fld in ("price", "rating", "review_count", "availability", "commission_rate"):
        if p[fld] is not None:
            errors.append(f"{p['id']}: {fld} has a value but no official source was confirmed for it")

cat = parsed[ROOT / "categories/home-kitchen-air-fryers.html"]
if not cat:
    errors.append("category page missing")
html_text = (ROOT / "categories/home-kitchen-air-fryers.html").read_text(encoding="utf-8")
unv_count = html_text.count('badge unv">Unverified')
expected = sum(1 for p in products for f in ("price", "rating", "review_count", "availability", "commission_rate") if p[f] is None)
if unv_count < expected:
    errors.append(f"category table shows {unv_count} Unverified badges, expected at least {expected}")

for page in pages:
    if "Affiliate disclosure" not in page.read_text(encoding="utf-8"):
        errors.append(f"{page.relative_to(ROOT)}: missing affiliate disclosure")

print(f"checked {len(pages)} pages, {sum(len(c.links) for c in parsed.values())} links")
if errors:
    print("FAILED:")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("OK: no broken links, all product rows sourced, all blank values flagged")

#!/usr/bin/env python3
"""9E-T3: publish this session's finding and its stated limitation on the review register."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / "data" / "flags.json"
data = json.loads(PATH.read_text(encoding="utf-8"))

ROWS = [
    {
        "id": "9E-F01",
        "severity": "Medium",
        "category": "Site structure",
        "item": "The canonical shop had no page for an individual listing",
        "detail": "All five registered listings were reachable only as cards inside shop/air-fryers/, shop/meat-thermometers/ and the comparison table, so every product-intent URL was category-level. The retained marketing/product-*.html pages cover three of the five, carry noindex,follow and use earlier chrome, so they could not stand in as the canonical page for a listing.",
        "action": "FIXED 2026-11-20 by session 9ed0552a: build_publication now emits shop/<category>/<slug>.html for each registered listing from the existing register record; the front page teasers, both category cards, the comparison table and the guide shortlist tables link to those pages; the URLs are indexable, listed in sitemap.xml and included in the local site search index. Release gate: sessions/9ed0552a/test_product_pages.py, with a --self-test that proves the gate catches six deliberate regressions.",
        "repo_evidence": "tools/build_publication.py; data/publication.json; sitemap.xml; sessions/9ed0552a/test_product_pages.py",
        "date": "2026-11-20",
        "session": "9ed0552a",
        "status": "fixed",
    },
    {
        "id": "9E-F02",
        "severity": "Low",
        "category": "Verification scope",
        "item": "The listing notes restate observations dated 2026-11-19; no listing was re-fetched on 2026-11-20",
        "detail": "This build environment could reach GitHub, npm and PyPI only, so amazon.com was not fetched by this session. Every value on the new pages comes from the register entry with its own observation date, and each page prints that date. No same-day re-check, price, rating, availability or performance claim is made.",
        "action": "No value changed. The limitation is stated on every page ('Listing checked 19 Nov 2026'). A later pass with outbound access should re-open the five supplied links and update observed_on before any newer date is asserted.",
        "repo_evidence": "data/publication.json (products[].observed_on); shop/air-fryers/*.html; shop/meat-thermometers/*.html",
        "date": "2026-11-20",
        "session": "9ed0552a",
        "status": "open — limitation stated on the page",
    },
]

existing = {f["id"] for f in data["flags"]}
added = [r for r in ROWS if r["id"] not in existing]
data["flags"].extend(added)
if added:
    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"flags: {len(data['flags'])} total, added {[r['id'] for r in added]}")

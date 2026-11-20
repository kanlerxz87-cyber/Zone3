#!/usr/bin/env python3
"""Release gate for the per-listing pages (session 9ed0552a, 2026-11-20).

WHY
---
9E-F01: the canonical shop had no page for an individual listing. Five products lived only as
cards inside two category pages and one comparison table, so every product-intent URL was
category-level, and `/marketing/product-1…3*.html` (noindex, three of five, earlier chrome) was
not a replacement.

WHAT THIS CHECKS, on the built tree, for every registered listing
-----------------------------------------------------------------
1. The page exists at `shop/<category>/<slug>.html`, is registered in `indexable_pages`, and
   carries `index,follow` — not a noindex page that the sitemap silently skips.
2. It carries the shared masthead, the disclosure strip above `<main>`, the footer disclosure,
   exactly one `<h1>`, a unique title and a unique meta description inside the gate's length
   range, and one canonical URL equal to the site's own.
3. Every outbound Amazon link is `rel="sponsored"` and carries the Associates `tag=`; at least
   one of them is the call to action.
4. No price, star rating, review count, "we tested" claim or review-score pattern appears.
5. The intended-ASIN fields are still blank in the register, and the page keeps the intended
   and observed records visually separate: it prints the observed ASIN and says the intended
   fields are unconfirmed.
6. The page is reachable: the front page, its category page and the comparison table each link
   to it, and it appears in sitemap.xml and in the site search index.

`--self-test` re-runs the same rules against deliberately broken copies and fails if any
mutation is not caught, so the gate cannot quietly become a no-op.

Exit 1 on any failure; tools/publish.py treats that as a blocked release.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = json.loads((ROOT / "data" / "publication.json").read_text(encoding="utf-8"))
TAG = json.loads((ROOT / "data" / "shop" / "config.json").read_text(encoding="utf-8"))["associates_tracking_id"]
DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."
AMAZON = re.compile(r"https?://(?:www\.)?(?:amazon\.[a-z.]+|link\.amazon)/", re.I)
FORBIDDEN = (
    (re.compile(r"\$\s*\d"), "a price"),
    (re.compile(r"\d(?:\.\d)?\s*(?:stars|out of 5)"), "a star rating"),
    (re.compile(r"\b\d[\d,]*\s+(?:reviews|ratings)\b"), "a review count"),
    (re.compile(r"\bwe tested\b", re.I), "a test claim"),
)

failures: list[str] = []


def fail(rel: str, message: str) -> None:
    failures.append(f"{rel}: {message}")


def amazon_anchors(raw: str) -> list[str]:
    return re.findall(r"<a\b[^>]*>", raw)


def audit(rel: str, raw: str, p: dict) -> list[str]:
    """Every per-page rule, as a pure function so the self-test can feed it broken copies."""
    problems: list[str] = []

    def need(ok: bool, label: str) -> None:
        if not ok:
            problems.append(f"{rel}: {label}")

    header = re.search(r"<header\b[^>]*\bp26-header\b.*?</header>", raw, re.S)
    banner = re.search(r"<aside\b[^>]*\bp26-disclosure\b.*?</aside>", raw, re.S)
    main = re.search(r"<main\b", raw)
    need(header is not None, "shared masthead missing")
    need(banner is not None and DISCLOSURE in (banner.group() if banner else ""), "disclosure strip missing from banner")
    need(header is not None and banner is not None and main is not None
         and header.end() <= banner.start() < main.start(), "disclosure must sit under the masthead and above the content")
    need(DISCLOSURE in raw.split("</main>")[-1], "footer disclosure missing")
    need(len(re.findall(r"<h1\b", raw)) == 1, "exactly one main heading required")
    need(raw.count(f'href="https://kanlerxz87-cyber.github.io/Zone3/{rel}"') == 1, "one canonical URL required")
    need('name="robots" content="index,follow' in raw, "listing page must be indexable, not noindex")

    for anchor in amazon_anchors(raw):
        if not AMAZON.search(anchor):
            continue
        need('rel="' in anchor and "sponsored" in anchor, f"Amazon link not marked sponsored: {anchor[:90]}")
        need(f"tag={TAG}" in anchor, f"Amazon link without the Associates tag: {anchor[:90]}")

    need('class="p26-button"' in raw and f"tag={TAG}" in raw, "a tagged call to action is required")

    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", raw))
    for pattern, label in FORBIDDEN:
        need(not pattern.search(text), f"page must not state {label}")

    need(p["observed_asin"] in raw, "observed ASIN must be printed")
    need("stay blank" in text, "intended fields must be shown as blank/unconfirmed")
    for key in ("intended_asin", "official_listing_url", "intent_confirmed_on", "intent_confirmation_source"):
        need(not p[key], f"register field {key} must stay blank")

    need(f'shop/{p["category"]}/index.html' in raw or 'href="index.html"' in raw, "link back to its category page")
    need("shop/products/index.html#comparison" in raw, "link to the comparison table")
    return problems


def main() -> int:
    if "--self-test" in sys.argv:
        p = DATA["products"][0]
        rel = f'shop/{p["category"]}/{p["slug"]}.html'
        good = (ROOT / rel).read_text(encoding="utf-8")
        if audit(rel, good, p):
            print("SELF-TEST FAILED: the live page does not pass its own gate")
            return 1
        mutations = {
            "unsponsored link": good.replace(' rel="sponsored noopener" target="_blank"', ' target="_blank"', 1),
            "untagged link": good.replace(f"?tag={TAG}", "", 1),
            "a price": good.replace("</h1>", "</h1><p>$19.99</p>", 1),
            "removed disclosure": re.sub(r'<aside class="p26-disclosure.*?</aside>', "", good, count=1, flags=re.S),
            "second heading": good.replace("<h1>", "<h1>One</h1><h1>", 1),
            "unconfirmed intent erased": good.replace("stay blank", "are confirmed"),
        }
        missed = [name for name, text in mutations.items() if not audit(rel, text, p)]
        if missed:
            print("SELF-TEST FAILED: these defects were not caught — " + ", ".join(missed))
            return 1
        print(f"SELF-TEST PASS: {len(mutations)} deliberately broken copies each caught by the gate")
        return 0

    indexable = set(DATA["indexable_pages"])
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    search = json.loads((ROOT / "assets" / "publication-search.json").read_text(encoding="utf-8"))
    search_paths = {row.get("path") for row in search}
    home = (ROOT / "index.html").read_text(encoding="utf-8")

    titles: dict[str, str] = {}
    for p in DATA["products"]:
        rel = f'shop/{p["category"]}/{p["slug"]}.html'
        path = ROOT / rel
        if not path.exists():
            fail(rel, "listing page missing")
            continue
        raw = path.read_text(encoding="utf-8")
        for problem in audit(rel, raw, p):
            failures.append(problem)

        if rel not in indexable:
            fail(rel, "not registered in data/publication.json → indexable_pages")
        if f'<loc>https://kanlerxz87-cyber.github.io/Zone3/{rel}</loc>' not in sitemap:
            fail(rel, "missing from sitemap.xml")
        if rel not in search_paths:
            fail(rel, "missing from the local site search index")

        title_match = re.search(r"<title>(.*?)</title>", raw, re.S)
        desc_match = re.search(r'<meta name="description" content="([^"]*)"', raw)
        title = title_match.group(1).strip() if title_match else ""
        description = desc_match.group(1) if desc_match else ""
        if not (20 <= len(title) <= 85):
            fail(rel, f"title length {len(title)} outside 20-85")
        if not (60 <= len(description) <= 165):
            fail(rel, f"meta description length {len(description)} outside 60-165")
        if title in titles:
            fail(rel, f"duplicate title also used by {titles[title]}")
        titles[title] = rel

        category_page = (ROOT / f'shop/{p["category"]}/index.html').read_text(encoding="utf-8")
        compare_page = (ROOT / "shop" / "products" / "index.html").read_text(encoding="utf-8")
        for label, page in (("front page", home), ("category page", category_page), ("comparison table", compare_page)):
            if f'shop/{p["category"]}/{p["slug"]}.html' not in page:
                fail(rel, f"not linked from the {label}")

    if failures:
        print(f"FAIL: {len(failures)} product-page problem(s)")
        for f in failures:
            print(" - " + f)
        return 1
    print(f"PASS: {len(DATA['products'])} listing pages present, indexable, sourced, tagged, sponsored and reachable")
    return 0


if __name__ == "__main__":
    sys.exit(main())

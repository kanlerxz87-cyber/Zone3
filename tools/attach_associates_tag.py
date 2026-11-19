#!/usr/bin/env python3
"""4B0-T2 — put the owner-supplied Associates ID on every product-detail link.

Why this exists
--------------
Amazon Associates Program Policies (read live 2026-11-19, page stamped "Updated:
April 14, 2026"), Participation Requirements 2(b), verbatim:

    "All Special Links must be accessed directly from your Site. For example,
     you must include your Associates ID or "tag" (appearing as XXXXX-##, or such
     other format as we may designate) as a parameter in the URL of each link you
     place on your Site to an Amazon Site."

and 2(a): "Special Links must use the Associates ID we have assigned to you."

On 2026-11-19 this tree had 1,491+ Amazon product-detail links and only eight of
them carried the tag, on two legacy pages. tools/build_shop.py actively *failed*
the build if a `tag=` appeared, so the omission was enforced by the build.

What it does
------------
Adds `?tag=<value>` (or `&tag=<value>` when a query string already exists) to
every <a href> that points at a product-detail page on www.amazon.com/amazon.com
and does not already carry a tag. It never touches:

  * the five submitted link.amazon short links (FLG-003; status unresolved,
    and the brief forbids calling them invalid);
  * /dp/<9-character> links, which are the page-not-found evidence links (a
    9-character token is not an ASIN: Creators API GetItems, ItemIdType=ASIN);
  * Amazon browse/search/Best-Sellers pages and Amazon or Associates help pages
    (cited sources, not product promotions — see 4B0-F-02);
  * any link that already carries a *different* tag; that is reported, not
    overwritten.

It also leaves `rel="sponsored"` alone: scripts/mark_sponsored.py owns that
token and runs later in the same chain.

Run position: after every HTML builder, before scripts/mark_sponsored.py, so
the rebuilt tree is tagged and checked by scripts/check_site.py.

    python3 tools/attach_associates_tag.py            # rewrite in place
    python3 tools/attach_associates_tag.py --check    # exit 1 if anything would change
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit, parse_qs

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "data" / "links" / "associates-links.json"
SKIP_DIRS = {".git", "archive", "node_modules", ".venv", "venv"}

ANCHOR_RE = re.compile(r"<a\b[^>]*>", re.I)
HREF_RE = re.compile(r'href="([^"]+)"', re.I)
TAG_PARAM_RE = re.compile(r"[?&](?:tag|ascsubtag|linkCode)=([^&\"#]*)", re.I)
PRODUCT_PATH_RE = re.compile(r"/(?:dp|gp/product)/([A-Za-z0-9]{9,10})(?:[/?#]|$)")
SLUG_DP_RE = re.compile(r"/dp/([A-Za-z0-9]{9,10})(?:[/?#]|$)")
AMAZON_HOSTS = {"www.amazon.com", "amazon.com"}
# A 9-character token is a submission token, not an ASIN. Those links are the
# page-not-found evidence; tagging them would send readers to an error page.
ASIN_LEN = 10


def load_tag() -> str:
    data = json.loads(REGISTER.read_text(encoding="utf-8"))
    tag = data["tag"]["value"]
    if not tag:
        raise SystemExit("associates-links.json has no tag value")
    return tag


def classify(href: str) -> tuple[str, str | None]:
    """Return (kind, asin). kind is one of: not-amazon, not-product, product, token-link."""
    if not href.startswith(("http://", "https://")):
        return "not-amazon", None
    parts = urlsplit(href)
    host = parts.netloc.lower()
    if host not in AMAZON_HOSTS:
        return "not-amazon", None
    m = PRODUCT_PATH_RE.search(parts.path) or SLUG_DP_RE.search(parts.path)
    if not m:
        return "not-product", None
    asin = m.group(1)
    if len(asin) != ASIN_LEN:
        return "token-link", asin
    return "product", asin


def with_tag(href: str, tag: str) -> str:
    if "?" not in href:
        return f"{href}?tag={tag}"
    if href.endswith("?") or href.endswith("&"):
        return f"{href}tag={tag}"
    return f"{href}&tag={tag}"


def rewrite_anchor(anchor: str, tag: str) -> tuple[str, str]:
    """Return (new_anchor, outcome). outcome: unchanged | tagged | foreign-tag."""
    m = HREF_RE.search(anchor)
    if not m:
        return anchor, "unchanged"
    href = m.group(1)
    kind, _asin = classify(href)
    if kind != "product":
        return anchor, "unchanged"
    existing = TAG_PARAM_RE.search(href)
    if existing:
        if existing.group(1) == tag:
            return anchor, "unchanged"
        return anchor, "foreign-tag"
    new_href = with_tag(href, tag)
    return anchor[: m.start(1)] + new_href + anchor[m.end(1):], "tagged"


def process(text: str, tag: str, stats: dict) -> str:
    def repl(m: re.Match) -> str:
        new, outcome = rewrite_anchor(m.group(0), tag)
        stats[outcome] = stats.get(outcome, 0) + 1
        return new

    return ANCHOR_RE.sub(repl, text)


def apply_to_text(text: str, tag: str | None = None) -> str:
    """Same rules as the file pass, for a generator that compares in memory.

    Builders whose `--check` compares freshly rendered HTML with the post-processed
    file on disk (build_brief_status, build_cba81fa5_site, build_publication) call
    this so their comparison stays exact instead of becoming permanently stale.
    """
    return process(text, tag or load_tag(), {})


def iter_pages() -> list[Path]:
    pages = []
    for path in sorted(ROOT.rglob("*.html")):
        if path.relative_to(ROOT).parts[0] in SKIP_DIRS:
            continue
        pages.append(path)
    return pages


def main(argv: list[str]) -> int:
    check_only = "--check" in argv
    tag = load_tag()
    stats: dict[str, int] = {}
    changed_files = 0
    foreign: list[str] = []
    for path in iter_pages():
        original = path.read_text(encoding="utf-8")
        updated = process(original, tag, stats)
        if updated != original:
            changed_files += 1
            if not check_only:
                path.write_text(updated, encoding="utf-8")
        for m in ANCHOR_RE.finditer(updated):
            h = HREF_RE.search(m.group(0))
            if not h:
                continue
            if classify(h.group(1))[0] == "product":
                ex = TAG_PARAM_RE.search(h.group(1))
                if ex and ex.group(1) != tag:
                    foreign.append(f"{path.relative_to(ROOT)}: {h.group(1)}")
    tagged = stats.get("tagged", 0)
    if check_only:
        if tagged:
            print(f"FAIL: {tagged} product link(s) across {changed_files} page(s) are missing tag={tag}")
            return 1
        print(f"OK: every product-detail link carries tag={tag} "
              f"({stats.get('unchanged', 0)} links inspected; foreign tags: {len(foreign)})")
        return 0
    print(f"tagged {tagged} product link(s) across {changed_files} page(s); "
          f"{stats.get('unchanged', 0)} left as they were")
    if foreign:
        print("NOTE: links carrying a different tag were left untouched:")
        for f in foreign[:20]:
            print("  " + f)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

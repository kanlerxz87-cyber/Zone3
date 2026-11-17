#!/usr/bin/env python3
"""Mark every outbound product link rel="sponsored" across the published pages (ded63349, 2026-11-17).

Brief requirement: "Keep every outbound product link marked as sponsored." Google's link-qualification
guidance asks for rel="sponsored" on paid or affiliate links. Today the Amazon links on this site are
untagged evidence links, but the site's declared purpose is Associates promotion, so every product link
is marked sponsored now, and the same rule keeps working the day a Associates tag is added to them.

Rule applied, idempotently, to every published HTML page (archive/, sessions/ and docs/ are audit
snapshots and are skipped, as are redirect stubs):

  An <a> whose href points at an Amazon product page — amazon.*/dp/…, amazon.*/gp/product/…, or the
  submitted link.amazon short links — gets rel="sponsored" added to its rel attribute (keeping
  noopener noreferrer, which stays). Policy pages (affiliate-program.amazon.com/help/…) are
  documentation links, not product links, and are deliberately left unmarked.

Run order: after every page generator, before scripts/build_sitemap.py.

    python3 tools/apply_sponsored.py            # rewrite in place
    python3 tools/apply_sponsored.py --check    # exit 1 if any product link lacks rel="sponsored"
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

SKIP_DIRS = {".git", "archive", "sessions", "docs", "__pycache__", ".github",
             "node_modules", ".arena", ".cache"}

# Product-page URLs only: /dp/ and /gp/product/ on any amazon host, and the submitted
# link.amazon short links. Browse-node, search and help pages are not product links.
PRODUCT_HREF = re.compile(
    r'https?://[^"\']*(?:amazon\.[a-z]{2,3})?/[^"\']*(?:/dp/[A-Z0-9]{10}|/gp/product/[A-Z0-9]{10})[^"\']*'
    r'|https?://link\.amazon/[^"\']*', re.I)

ANCHOR_RE = re.compile(r'<a\b[^>]*>', re.I)
HREF_RE = re.compile(r'href="([^"]*)"')
REL_RE = re.compile(r'rel="([^"]*)"')

REL_ORDER = ["sponsored", "noopener", "noreferrer"]


def normalize_rel(tokens: list[str]) -> str:
    seen: list[str] = []
    for t in REL_ORDER:
        if t in tokens or (t == "sponsored"):
            if t not in seen:
                seen.append(t)
    for t in tokens:
        if t and t not in seen:
            seen.append(t)
    return " ".join(seen)


def fix_anchor(tag: str) -> tuple[str, bool]:
    """Return (new_tag, changed). Adds 'sponsored' to a product-link anchor's rel."""
    href_m = HREF_RE.search(tag)
    if not href_m or not PRODUCT_HREF.search(href_m.group(1)):
        return tag, False
    rel_m = REL_RE.search(tag)
    if rel_m:
        tokens = rel_m.group(1).split()
        if "sponsored" in tokens:
            return tag, False
        new_rel = normalize_rel(tokens)
        return tag[:rel_m.start(1)] + new_rel + tag[rel_m.end(1):], True
    # No rel attribute: insert one before the closing bracket, keeping noopener/noreferrer.
    return tag[:-1].rstrip() + ' rel="sponsored noopener noreferrer">', True


def iter_pages() -> list[pathlib.Path]:
    pages = []
    for p in ROOT.rglob("*.html"):
        rel_parts = p.relative_to(ROOT).parts
        if any(part in SKIP_DIRS for part in rel_parts):
            continue
        pages.append(p)
    return pages


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    problems: list[str] = []
    touched: list[str] = []
    for p in iter_pages():
        raw = p.read_text(encoding="utf-8")
        out = []
        last = 0
        changed = False
        for m in ANCHOR_RE.finditer(raw):
            out.append(raw[last:m.start()])
            new, ch = fix_anchor(m.group(0))
            out.append(new)
            changed = changed or ch
            if a.check and not ch and "sponsored" not in m.group(0):
                href = HREF_RE.search(m.group(0))
                if href and PRODUCT_HREF.search(href.group(1)):
                    problems.append(f"{p.relative_to(ROOT).as_posix()}: unmarked product link {href.group(1)[:80]}")
            last = m.end()
        out.append(raw[last:])
        if changed and not a.check:
            p.write_text("".join(out), encoding="utf-8")
            touched.append(p.relative_to(ROOT).as_posix())
    if a.check:
        if problems:
            print(f"SPONSORED CHECK FAILED — {len(problems)} product link(s) without rel=\"sponsored\":")
            for x in problems:
                print("  " + x)
            return 1
        print("SPONSORED CHECK PASS — every product link carries rel=\"sponsored\"")
        return 0
    print(f"apply_sponsored: rewrote {len(touched)} page(s)")
    for x in touched:
        print("  " + x)
    return 0


if __name__ == "__main__":
    sys.exit(main())

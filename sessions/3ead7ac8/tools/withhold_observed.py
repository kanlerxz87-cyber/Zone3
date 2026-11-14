#!/usr/bin/env python3
"""Session 3ead7ac8 — withhold observed price / rating / review-count values.

Why
---
Amazon Associates Program Participation Requirements 2(b) and 6(t)
(affiliate-program.amazon.com/help/operating/policies, re-read verbatim on
2026-11-14 by this session) say:

  2(b) "your Site may only show prices and availability if: (a) we serve the
        link in which that price and availability data are displayed, or
        (b) you obtain Product pricing and availability data via Creators API
        or PA API ..."

  6(t) "You will not display or otherwise use any of our customer reviews or
        star ratings, in part or in whole, on your Site unless you have
        obtained a link to that customer review or star rating through
        Creators API or PA API ..."

The canonical product tables on this site therefore leave those cells blank
(FLG-022, FLG-023, FLG-029).  Some hand-maintained pages still rendered the
dated observations as product facts.  This script replaces only those exact
table cells, and leaves prose, flag descriptions and source-register
descriptions untouched.

It is idempotent: a cell that already carries the withheld marker is skipped.

Usage:  python3 sessions/3ead7ac8/tools/withhold_observed.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

# ---------------------------------------------------------------- cells to change
# Exact, tag-free text of the <td> cells that present an observed value as a
# product fact.  Each entry was enumerated by reading the rendered tables.
OBSERVED_CELLS = [
    # prices / list prices / other offers / discounts
    "$79.93", "$79.93 Limited time deal", "$79.93 deal", "USD 79.93 (observed 2026-11-14; list USD 99.99)",
    "$149.99", "$149.99 Early Black Friday Deal", "$149.99 deal", "USD 149.99 (observed 2026-11-14; list USD 209.99)",
    "$79.91", "$79.91 Limited time deal", "$79.91 deal", "USD 79.91 (observed 2026-11-14; list USD 119.99)",
    "$99.99", "$209.99", "$119.99",
    "$57.45", "$57.45 (2+ offers)", "$92.99", "$92.99 (2+ offers)", "$49.54", "$49.54 (3+ offers)",
    "−20.1%", "−28.6%", "−33.4%", "20.1%", "28.6%", "33.4%",
    "$79.91 – $149.99",
    # star ratings
    "4.2 / 5", "4.3 / 5", "4.4 / 5",
    "4.2 out of 5 (observed 2026-11-14)", "4.3 out of 5 (observed 2026-11-14)", "4.4 out of 5 (observed 2026-11-14)",
    # review counts
    "4.8K", "18.3K", "16.8K",
    "4.8K as displayed (observed 2026-11-14)", "18.3K as displayed (observed 2026-11-14)",
    "16.8K as displayed (observed 2026-11-14)",
    # demand badges
    "1K+", "3K+", "4K+",
    "1K+ bought in past month", "3K+ bought in past month", "4K+ bought in past month",
]

# Cells whose text is a whole-line source-register description or a flag
# description: those quote the observation on purpose and are left alone.
KEEP_PREFIXES = (
    "Price $", "Discounts −", "Shown as", "Ratings counts are", "Displaying star ratings",
    "data/products.json keeps",
)

FIX_FILES = [
    "category/air-fryers.html",
    "docs/analysis.html",
    "docs/content.html",
    "docs/executive-summary.html",
    "docs/flagged.html",
    "docs/index.html",
    "docs/products.html",
]

MARKER = "withheld-3E"


def rel_flag(prefix: str, flag: str) -> str:
    return f'<a class="flagid" href="{prefix}flagged.html#{flag}">{flag}</a>'


def replacement(prefix: str) -> str:
    return (
        f'<span class="badge unv" data-note="{MARKER}">Withheld</span> '
        f'{rel_flag(prefix, "FLG-022")} {rel_flag(prefix, "FLG-023")}'
    )


def cell_text(inner: str) -> str:
    import html as _html
    return _html.unescape(re.sub(r"<[^>]+>", "", inner)).strip()


def scrub(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    prefix = "../" if "/" in path.relative_to(ROOT).as_posix() else ""
    n = 0

    def sub(m: re.Match) -> str:
        nonlocal n
        open_tag, inner = m.group(1), m.group(2)
        txt = cell_text(inner)
        if txt not in OBSERVED_CELLS:
            return m.group(0)
        if txt.startswith(KEEP_PREFIXES):
            return m.group(0)
        if MARKER in inner:
            return m.group(0)
        n += 1
        return f"<{open_tag}>{replacement(prefix)}</td>"

    new = re.sub(r"<(td\b[^>]*)>(.*?)</td>", sub, text, flags=re.S)
    if n:
        path.write_text(new, encoding="utf-8")
    return n


# ------------------------------------------------------------ session banners
BANNER = """
<div class="callout" style="border-left:4px solid #b45309;background:#fffbeb">
  <p><strong>Compliance notice (added 2026-11-14, session <code>3ead7ac8</code>).</strong>
  This page is a historical session work product and is kept verbatim under the
  <a href="{pre}COORDINATION.md">cross-session convention</a>. Where it shows a price, a star
  rating, a review count or a &ldquo;bought in past month&rdquo; figure, that value is a
  dated <em>observation</em> of an Amazon page, recorded as research evidence.
  It is <strong>not</strong> a compliant product display: Associates Program
  <a href="https://affiliate-program.amazon.com/help/operating/policies" target="_blank" rel="noopener noreferrer">Participation
  Requirements 2(b) and 6(t)</a> allow price, availability, star-rating and review display only
  where Amazon serves the link or the data comes from Creators API / PA API &mdash; neither applies
  here. See <a href="{pre}flagged.html#3E-F-02">3E-F-02</a> and
  <a href="{pre}flagged.html#FLG-022">FLG-022</a>. The canonical, blank-field tables are on
  <a href="{pre}products.html">Products</a> and <a href="{pre}pricing.html">Pricing &amp; commission</a>.</p>
</div>
"""

BANNER_FILES = [
    "sessions/03bbd050/index.html",
    "sessions/3c886b62/analysis.html",
    "sessions/3c886b62/categories.html",
    "sessions/3c886b62/category-home-kitchen.html",
    "sessions/3c886b62/commission.html",
    "sessions/3c886b62/comparison.html",
    "sessions/3c886b62/index.html",
    "sessions/3c886b62/product-chefman-6qt-dual-basket-air-fryer.html",
    "sessions/3c886b62/product-chefman-8qt-turbofry-air-fryer.html",
    "sessions/3c886b62/product-emeril-lagasse-26qt-french-door-air-fryer-oven.html",
    "sessions/3c886b62/products.html",
    "sessions/3c886b62/verification.html",
]


def add_banner(rel: str) -> bool:
    path = ROOT / rel
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    if "Compliance notice (added 2026-11-14" in text:
        return False
    pre = "../" * rel.count("/")
    banner = BANNER.format(pre=pre)
    m = re.search(r"<main[^>]*>", text)
    if not m:
        return False
    text = text[: m.end()] + banner + text[m.end():]
    path.write_text(text, encoding="utf-8")
    return True


CORRECTION = """
<div class="callout" style="border-left:4px solid #1d4ed8;background:#eff6ff">
  <p><strong>Correction notice (added 2026-11-14, session <code>3ead7ac8</code>).</strong>
  This page states that the Associates commission rate schedule is sign-in-only and therefore
  unverifiable. That is <strong>no longer accurate</strong>. The Standard Commission Income
  Statement, <a href="https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ"
  target="_blank" rel="noopener noreferrer">Table 1</a>, and the Onsite statement,
  <a href="https://affiliate-program.amazon.com/help/node/topic/G4ARBJC7Z2NK48CA"
  target="_blank" rel="noopener noreferrer">Table A</a>, both render without a sign-in; this session
  re-read Table 1 on 2026-11-14 and it matches the published category rows (Kitchen 4.50%,
  All Other Categories 4.00%). Only the per-account <code>/help/operating/schedule</code> rate card is
  gated. What remains unresolvable is <em>which</em> rate category each listing falls in, so no rate is
  attached to a product row anywhere on this site. See
  <a href="{pre}flagged.html#3E-F-04">3E-F-04</a> and <a href="{pre}flagged.html#FLG-021">FLG-021</a>.</p>
</div>
"""

CORRECTION_FILES = [
    "docs/analysis.html",
    "docs/executive-summary.html",
    "docs/flagged.html",
    "docs/index.html",
    "docs/products.html",
    "docs/sources.html",
]


def add_correction(rel: str) -> bool:
    path = ROOT / rel
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    if "Correction notice (added 2026-11-14" in text:
        return False
    pre = "../" * rel.count("/")
    note = CORRECTION.format(pre=pre)
    m = re.search(r"<main[^>]*>", text)
    if not m:
        return False
    text = text[: m.end()] + note + text[m.end():]
    path.write_text(text, encoding="utf-8")
    return True


def main() -> int:
    total = 0
    print("== withhold observed-value cells (compliance fix 3E-F-01 / 3E-F-03)")
    for rel in FIX_FILES:
        p = ROOT / rel
        if not p.exists():
            print(f"   skip (missing): {rel}")
            continue
        n = scrub(p)
        print(f"   {n:>3} cells  {rel}")
        total += n
    print("== compliance banner on retained session pages (3E-F-02)")
    for rel in BANNER_FILES:
        ok = add_banner(rel)
        print(f"   {'banner' if ok else 'skip  '}  {rel}")
    print("== correction notice on /docs/ pages that still say rates are sign-in-only (3E-F-04)")
    for rel in CORRECTION_FILES:
        ok = add_correction(rel)
        print(f"   {'notice' if ok else 'skip  '}  {rel}")
    print(f"total cells withheld: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

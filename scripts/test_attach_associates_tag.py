#!/usr/bin/env python3
"""Tests for tools/attach_associates_tag.py (4B0-T2).

Each case is a rule the Associates Program Policies or this repository's own
register states, so a regression fails loudly instead of quietly dropping the
owner's tag or tagging something that must stay untagged.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("aat", ROOT / "tools" / "attach_associates_tag.py")
aat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(aat)

TAG = "shopnow047c-20"
FAILS: list[str] = []


def check(name: str, got, want) -> None:
    if got != want:
        FAILS.append(f"{name}: got {got!r}, want {want!r}")


def one(html: str) -> tuple[str, str]:
    stats: dict = {}
    out = aat.process(html, TAG, stats)
    outcomes = [k for k, v in stats.items() if v]
    return out, (outcomes[0] if len(outcomes) == 1 else ",".join(sorted(outcomes)))


# 1. /dp/ product link gains the tag.
out, kind = one('<a href="https://www.amazon.com/dp/B0CDY277D3" rel="sponsored">x</a>')
check("dp link tagged", out, f'<a href="https://www.amazon.com/dp/B0CDY277D3?tag={TAG}" rel="sponsored">x</a>')
check("dp outcome", kind, "tagged")

# 2. Product-slug path (/Name/dp/ASIN) is still a product page.
out, _ = one('<a href="https://www.amazon.com/Ninja-AF141/dp/B0CSZ7WBYW">x</a>')
check("slug path tagged", f'tag={TAG}' in out, True)

# 3. An existing query string uses &, not a second ?.
out, _ = one('<a href="https://www.amazon.com/dp/B0CDY277D3?th=1">x</a>')
check("existing query", out, f'<a href="https://www.amazon.com/dp/B0CDY277D3?th=1&tag={TAG}">x</a>')

# 4. gp/product form is a product page.
out, _ = one('<a href="https://www.amazon.com/gp/product/B08DKYBTPH">x</a>')
check("gp/product tagged", f'tag={TAG}' in out, True)

# 5. Idempotent: a correctly tagged link is left byte-identical.
src = f'<a href="https://www.amazon.com/dp/B09B7SB46R?tag={TAG}" rel="sponsored noopener">x</a>'
out, kind = one(src)
check("already tagged unchanged", out, src)
check("already tagged outcome", kind, "unchanged")

# 6. A foreign tag is never overwritten (register conflict_rule).
src = '<a href="https://www.amazon.com/dp/B09B7SB46R?tag=someoneelse-20">x</a>'
out, kind = one(src)
check("foreign tag preserved", out, src)
check("foreign tag outcome", kind, "foreign-tag")

# 7. The submitted link.amazon short links stay untouched (FLG-003).
src = '<a href="https://link.amazon/B04G1MEwY" rel="sponsored noopener">View</a>'
out, kind = one(src)
check("short link untouched", out, src)
check("short link outcome", kind, "unchanged")

# 8. A 9-character /dp/ token is evidence, not a product: no tag.
src = '<a href="https://www.amazon.com/dp/B04G1MEwY" rel="sponsored">S08</a>'
out, kind = one(src)
check("9-char token not tagged", out, src)
check("9-char outcome", kind, "unchanged")

# 9. Browse / search / Best-Sellers pages are citations, not products.
for u in (
    "https://www.amazon.com/Best-Sellers-Kitchen-Dining-Air-Fryers/zgbs/kitchen/17659096011/",
    "https://www.amazon.com/s?k=air+fryer",
    "https://www.amazon.com/Air-Fryers/b/ref=dp_bc_5?ie=UTF8&node=17659096011",
):
    out, kind = one(f'<a href="{u}">x</a>')
    check(f"non-product untouched {u[:40]}", out, f'<a href="{u}">x</a>')

# 10. Associates help / agreement pages are sources, not products.
src = '<a href="https://affiliate-program.amazon.com/help/operating/policies">S02</a>'
out, _ = one(src)
check("help page untouched", out, src)

# 11. Internal and non-Amazon links untouched.
for u in ("index.html", "https://developers.google.com/search/docs", "mailto:a@b.c", "#main"):
    src = f'<a href="{u}">x</a>'
    out, _ = one(src)
    check(f"untouched {u}", out, src)

# 12. Amazon.ca / other marketplaces are not silently tagged with a .com tag
#     (Schedule 1 lists only the United States Amazon Site).
src = '<a href="https://www.amazon.ca/dp/B0CDY277D3">x</a>'
out, _ = one(src)
check("other marketplace untouched", out, src)

# 13. Anchor without href does not crash.
out, _ = one('<a name="x">y</a>')
check("nameless anchor", out, '<a name="x">y</a>')

# 14. Uppercase tag/mixed-case attributes still work.
out, _ = one('<A HREF="https://www.amazon.com/dp/B0DZFD6R9Z">x</A>')
check("uppercase anchor", f'tag={TAG}' in out, True)

# 15. The stale-claim gate must fire on a page that says the tag is absent, in each of the
#     phrasings this repository has actually published, and must not fire on the corrected
#     wording (session 4b0e3c7e; the defect below shipped live once before the gate existed).
import tempfile

STALE = [
    "The tracking ID shopnow047c-20 is not embedded in any link.",
    "The selected tracking ID shopnow047c-20 was, until 2026-11-19, not embedded in any link.",
    "The tag is NOT embedded in any link, because the links were used as supplied.",
    "The tracking ID was not added to any URL, to avoid writing a tag into unvalidated links.",
]
FINE = [
    "Until 2026-11-19 the tracking ID appeared in no link on this site. From that date it is carried by every product-detail link.",
    "Every product-detail link carries tag=shopnow047c-20. Account ownership is not verified.",
]


def _stale_for(html: str) -> list[str]:
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, dir=ROOT) as fh:
        fh.write(f"<html><body><p>{html}</p></body></html>")
        name = fh.name
    try:
        return aat.stale_claims(Path(name))
    finally:
        Path(name).unlink()


for phrase in STALE:
    check(f"stale claim caught: {phrase[:40]!r}", bool(_stale_for(phrase)), True)
for phrase in FINE:
    check(f"corrected wording allowed: {phrase[:40]!r}", _stale_for(phrase), [])

if FAILS:
    print("FAIL")
    for f in FAILS:
        print("  " + f)
    sys.exit(1)
print("OK: 15 rules, all attach_associates_tag cases pass (incl. the stale-claim gate)")

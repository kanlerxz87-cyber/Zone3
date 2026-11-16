#!/usr/bin/env python3
"""Regression test: no Python repr may reach a published page (session cba81fa5, 2026-11-16).

Raised as CBA-F-06. `scripts/build_site.py` collected the three home-page product cards into a list
and interpolated the *list* into an f-string, so the published home page shipped about a kilobyte of
escaped Python repr inside the hero:

    <div class="product-cards">['<div class="pcard">&#8230;', '&#8230;']</div>

Every gate stayed green: the disclosure sentence was present, the links resolved, the HTML parsed, one
h1, no placeholder token. Nothing asked the one question that mattered — is there markup-shaped text
in the output? This test asks it, across every page the site publishes.

Three signatures of a joined repr:
    OPEN    a bracket immediately followed by a quoted tag      ['<div   [("<p    [<span
    SEP     a quoted tag after a comma-quote pair               ', '<div
    CLOSE   a quoted tag closed by a bracket before a tag end   ']</div>

Inline <script>/<style>, <pre>/<code> and <span class="mono"> are stripped first: JS object literals
legitimately look like `[{title:'x'}]`, and a code sample may quote markup on purpose.

Usage:
    python3 scripts/cba81fa5_test_no_repr_output.py [--root DIR] [--selftest]
Exit 0 = clean; exit 1 = at least one page carries repr-shaped text (or the selftest fails).
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

LT = r"(?:&lt;|<)"
OPEN = re.compile(r"[\[({]\s*['\"]" + LT + r"[a-zA-Z/]")
SEP = re.compile(r"['\"]\s*,\s*['\"]" + LT + r"[a-zA-Z]")
CLOSE = re.compile(r"['\"]" + LT + r"\s*[\])]\s*" + LT + r"/")
STRIP = re.compile(
    r"<(script|style)\b.*?</\1>|<pre\b.*?</pre>|<code\b.*?</code>"
    r"|<span class=\"mono\">.*?</span>",
    re.S | re.I,
)
SKIP_DIRS = {".git", "archive", "node_modules", "__pycache__", ".github"}

BAD = ('<div class="product-cards">[\'<div class="pcard"><b>Chefman</b></div>\', '
       '\'<div class="pcard">x</div>\']</div>')
GOOD = ('<div class="product-cards"><div class="pcard"><b>Chefman</b></div>'
        '<div class="pcard"><b>Emeril</b></div></div>'
        '<script>var rows = [{title:"x", asin:"B08DKYBTPS"}];</script>'
        '<p>JSON shape: <span class="mono">[{"asin":"B0CDY277D3"}]</span></p>')


def scan(html: str):
    """Return (signature, snippet) for the first repr pattern found, else None."""
    body = STRIP.sub(" ", html)
    for name, rx in (("open-bracket repr", OPEN), ("comma-joined repr", SEP),
                     ("closing-bracket repr", CLOSE)):
        m = rx.search(body)
        if m:
            start = max(0, m.start() - 30)
            return name, re.sub(r"\s+", " ", body[start:m.end() + 60]).strip()
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(pathlib.Path(__file__).resolve().parent.parent))
    ap.add_argument("--selftest", action="store_true", help="prove the detector works, then exit")
    a = ap.parse_args()

    if a.selftest:
        bad, good = scan(BAD), scan(GOOD)
        if bad is None:
            print("SELFTEST FAIL: the detector missed a known joined-repr pattern")
            return 1
        if good is not None:
            print(f"SELFTEST FAIL: the detector flagged clean markup -> {good[1][:80]}")
            return 1
        print(f"SELFTEST PASS · caught: {bad[0]}")
        return 0

    root = pathlib.Path(a.root).resolve()
    hits, checked = [], 0
    for path in sorted(root.rglob("*.html")):
        rel = path.relative_to(root)
        if SKIP_DIRS & set(rel.parts):
            continue
        checked += 1
        found = scan(path.read_text(encoding="utf-8", errors="replace"))
        if found:
            hits.append(f"{rel.as_posix()}: {found[0]} -> {found[1][:150]}")

    for h in hits:
        print("REPR-SHAPED TEXT", h)
    print(f"{'FAIL' if hits else 'PASS'} · {checked} pages checked · {len(hits)} page(s) with repr-shaped text")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())

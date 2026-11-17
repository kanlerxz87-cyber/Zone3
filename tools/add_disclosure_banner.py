#!/usr/bin/env python3
"""Put the Associates disclosure above the fold on every published page (ded63349, 2026-11-17).

Brief requirement: "Keep the disclosure above the fold on every page, including this one."
The reader layer under site/ already ships a disclosure banner that precedes the navigation
(enforced by tools/i2_gate.py G1/G2). The older flat pages — the dashboard surfaces, the
marketing pages, the Research Desk articles, the audit build — carry the exact §5 sentence
in their footers, which satisfies the Operating Agreement's "on your Site" wording but is
weaker than the FTC's placement guidance ("Disclosures are likely to be missed if they appear
only … at the end of posts"). That gap is published as proposal D-07; the brief instructs it
be closed, so this pass adds a compact, non-dismissable banner immediately after <body> on
every page whose disclosure currently sits at or below <main>.

The banner is a separate pass, not an edit to each generator: the generators belong to other
sessions, and this keeps their output untouched while making the published result compliant.
It is idempotent, so the documented generator chain can run twice.

    python3 tools/add_disclosure_banner.py            # insert where missing
    python3 tools/add_disclosure_banner.py --check    # exit 1 if any page lacks it

A page is considered compliant when the exact §5 sentence appears before its <main>
(before its <nav> for pages without <main>), or when a .disclose-bar banner already exists.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."

SKIP_DIRS = {".git", "archive", "sessions", "docs", "__pycache__", ".github",
             "node_modules", ".arena", ".cache"}

BANNER = (
    '<div class="disclose-bar" role="note" '
    'style="background:#132b26;color:#f0f5f1;padding:10px 18px;'
    'font:600 13.5px/1.55 system-ui,-apple-system,\'Segoe UI\',Roboto,sans-serif">'
    '<div style="max-width:1180px;margin:0 auto">'
    '<strong>Affiliate disclosure:</strong> ' + DISCLOSURE + ' '
    '<span style="font-weight:400">Links to Amazon on this page are evidence links while a '
    'tracking tag is unavailable, so they earn nothing yet.</span></div></div>'
)

BODY_OPEN_RE = re.compile(r"<body[^>]*>")


def first_fold_target(raw: str) -> int:
    """Position the disclosure must precede: <main>, falling back to the first <nav."""
    m_main = re.search(r"<main\b", raw)
    if m_main:
        return m_main.start()
    m_nav = re.search(r"<nav\b", raw)
    return m_nav.start() if m_nav else len(raw)


def is_compliant(raw: str) -> bool:
    body = BODY_OPEN_RE.search(raw)
    start = body.end() if body else 0
    p = raw.find(DISCLOSURE, start)
    if p == -1:
        return False  # no disclosure at all — always needs the banner
    return p < first_fold_target(raw)


def iter_pages() -> list[pathlib.Path]:
    pages = []
    for p in ROOT.rglob("*.html"):
        if any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
            continue
        pages.append(p)
    return pages


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    missing: list[str] = []
    touched: list[str] = []
    for p in iter_pages():
        raw = p.read_text(encoding="utf-8")
        if is_compliant(raw):
            continue
        rel = p.relative_to(ROOT).as_posix()
        missing.append(rel)
        m = BODY_OPEN_RE.search(raw)
        if not m:
            print(f"add_disclosure_banner: {rel} has no <body> tag — skipped", file=sys.stderr)
            continue
        new = raw[:m.end()] + "\n" + BANNER + raw[m.end():]
        if not a.check:
            p.write_text(new, encoding="utf-8")
            touched.append(rel)
    if a.check:
        if missing:
            print(f"DISCLOSURE CHECK FAILED — {len(missing)} page(s) without an above-the-fold disclosure:")
            for x in missing:
                print("  " + x)
            return 1
        print("DISCLOSURE CHECK PASS — every published page states the §5 disclosure above the fold")
        return 0
    print(f"add_disclosure_banner: inserted banner on {len(touched)} page(s)")
    for x in touched:
        print("  " + x)
    return 0


if __name__ == "__main__":
    sys.exit(main())

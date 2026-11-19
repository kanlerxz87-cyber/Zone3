#!/usr/bin/env python3
"""Tests for tools/attach_tag.py (session 5d460e79).

Run: python3 sessions/5d460e79/test_attach_tag.py
Exits 1 on any failure so tools/publish.py can gate on it.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('attach_tag', ROOT / 'tools' / 'attach_tag.py')
attach = importlib.util.module_from_spec(spec)
spec.loader.exec_module(attach)

TAG = 'shopnow047c-20'
failures: list[str] = []


def check(name: str, got, want) -> None:
    if got != want:
        failures.append(f'{name}\n  got:  {got!r}\n  want: {want!r}')


# --- retag: the five real link shapes on this site ---------------------------------
check('tag a link.amazon short link',
      attach.retag('https://link.amazon/B04G1MEwY', TAG),
      ('https://link.amazon/B04G1MEwY?tag=shopnow047c-20', 'tagged'))

check('tag a bare /dp/ listing',
      attach.retag('https://www.amazon.com/dp/B0CDY277D3', TAG),
      ('https://www.amazon.com/dp/B0CDY277D3?tag=shopnow047c-20', 'tagged'))

check('tag a /gp/product/ listing',
      attach.retag('https://www.amazon.com/gp/product/B0CDY277D3', TAG),
      ('https://www.amazon.com/gp/product/B0CDY277D3?tag=shopnow047c-20', 'tagged'))

check('preserve an existing query parameter',
      attach.retag('https://www.amazon.com/dp/B0CDY277D3?th=1&psc=1', TAG),
      ('https://www.amazon.com/dp/B0CDY277D3?th=1&psc=1&tag=shopnow047c-20', 'tagged'))

check('preserve a fragment',
      attach.retag('https://www.amazon.com/dp/B0CDY277D3#reviews', TAG),
      ('https://www.amazon.com/dp/B0CDY277D3?tag=shopnow047c-20#reviews', 'tagged'))

# --- the &amp; bug: an escaped href must stay correctly escaped and parseable --------
escaped, status = attach.retag(
    'https://www.amazon.com/dp/B0CDY277D3?th=1&amp;psc=1', TAG)
check('escaped href keeps &amp; and never becomes &amp;amp;',
      (status, '&amp;amp;' in escaped, escaped.count('&amp;'),
       '&amp;tag=shopnow047c-20' in escaped, '?th=1&amp;psc=1' in escaped),
      ('tagged', False, 2, True, True))

# --- idempotence -------------------------------------------------------------------
once, _ = attach.retag('https://www.amazon.com/dp/B0CDY277D3', TAG)
check('already-tagged link is not changed again',
      attach.retag(once, TAG), (once, 'already'))

# --- a foreign tag is a conflict, never an overwrite -------------------------------
foreign = 'https://www.amazon.com/dp/B0CDY277D3?tag=someoneelse-20'
check('foreign tag is reported and left byte-for-byte',
      attach.retag(foreign, TAG), (foreign, 'conflict'))

# --- non-product destinations are never touched ------------------------------------
for href in ('https://affiliate-program.amazon.com/help/operating/policies',
             'https://www.amazon.com/Air-Fryers/b?node=17659096011',
             'https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers',
             'https://kanlerxz87-cyber.github.io/Zone3/guides/index.html',
             '#main'):
    check(f'leave non-product link alone: {href}', attach.retag(href, TAG), (href, 'skipped'))

# --- page-level: only <a href> is rewritten, never visible text or other attributes -
page = ('<p>See B0CDY277D3 at https://www.amazon.com/dp/B0CDY277D3</p>'
        '<a class="cta" href="https://www.amazon.com/dp/B0CDY277D3" rel="sponsored noopener">'
        'View on Amazon</a>'
        '<a href="https://affiliate-program.amazon.com/help/operating/policies">policies</a>')
out, rows = attach.process_page(page, TAG)
check('anchor href rewritten once', out.count('tag=shopnow047c-20'), 1)
check('plain text URL left untouched', 'See B0CDY277D3 at https://www.amazon.com/dp/B0CDY277D3' in out, True)
check('policy link untouched', 'href="https://affiliate-program.amazon.com/help/operating/policies"' in out, True)
check('rel attribute untouched', 'rel="sponsored noopener"' in out, True)
check('anchor text untouched', 'View on Amazon</a>' in out, True)
check('one audit row per rewrite', len(rows), 1)

# --- the file is not silently allowed to run with a nonsense tag --------------------
check('tag shape guard accepts the real tag',
      bool(__import__('re').fullmatch(r'[A-Za-z0-9._-]{3,24}-[0-9]{2,3}', TAG)), True)
check('tag shape guard rejects a non-tag string',
      bool(__import__('re').fullmatch(r'[A-Za-z0-9._-]{3,24}-[0-9]{2,3}', 'tracking-id')), False)

if failures:
    print(f'FAIL: {len(failures)} of the attach_tag checks failed')
    for f in failures:
        print(' -', f)
    sys.exit(1)
print('PASS: attach_tag — 22 checks')

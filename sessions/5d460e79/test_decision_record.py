#!/usr/bin/env python3
"""Gate: the suggestions surface must close the loop from choice to dated decision.

Session 5d460e79, 2026-11-19. Fixes audit finding 5D4-F10.

WHY
---
The brief asks for "a section dedicated for suggestions so someone can review
suggestions and choose the best path before implementing any changes." Before this
session the page offered 32 evidence questions, 21 proposals, 6 paths and a 4-way
<select> on every card — and no way to finish. A reviewer could choose and export,
but nothing told them what a decision must contain, and no place existed to record one.
The choosing half was a dead end.

WHAT THIS CHECKS
----------------
1. The decision-record section exists and names the five required fields.
2. The template is a real copy target: the id matches a data-copy-from button, and the
   copy handler in assets/publication.js reads textContent (so a <pre> keeps newlines).
3. Every row of the fields table carries an official https source, because the page
   asserts a rule and must show where the rule comes from.
4. The review export still states implementation: none, so the record cannot be
   mistaken for an action.

Run: python3 sessions/5d460e79/test_decision_record.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / 'suggestions' / 'index.html'
JS = ROOT / 'assets' / 'publication.js'
failures: list[str] = []

if not PAGE.exists():
    print('FAIL: suggestions/index.html is missing; run tools/build_publication.py')
    sys.exit(1)

html = PAGE.read_text(encoding='utf-8')
js = JS.read_text(encoding='utf-8')

# --- 1. the section and its five fields -----------------------------------------
start = html.find('id="decision-record"')
if start < 0:
    failures.append('no #decision-record section')
    section = ''
else:
    section = html[start:html.find('</section>', start)]

FIELDS = ('Decision', 'Date', 'Decided by', 'Evidence', 'What would change it')
for field in FIELDS:
    if field not in section:
        failures.append(f'the decision record does not name the "{field}" field')

# --- 2. the template is a working copy target ------------------------------------
if 'id="p26-decision-template"' not in section:
    failures.append('the copy template #p26-decision-template is missing')
if 'data-copy-from="p26-decision-template"' not in section:
    failures.append('no button is wired to copy the template')
if 'function plainText' not in js or 'textContent' not in js:
    failures.append('the copy handler no longer reads textContent, so a <pre> template would lose newlines')
if '<pre' not in section:
    failures.append('the template is not a <pre>, so line breaks would collapse in the copied text')
for line in ('Decision:', 'Date:', 'Decided by:', 'Evidence:', 'What would change it:'):
    if line not in section:
        failures.append(f'the template omits the "{line}" line')

# --- 3. every table row in the section carries an official source ----------------
rows = re.findall(r'<tr>(.*?)</tr>', section, re.S)
body_rows = [r for r in rows if '<td>' in r]
if not body_rows:
    failures.append('the fields table has no body rows')
for row in body_rows:
    if not re.search(r'href="https://', row):
        label = re.sub(r'<[^>]+>', '', row)[:40].strip()
        failures.append(f'fields-table row without an https source: {label}')

# --- 4. the export still declares that it implements nothing --------------------
if "implementation: 'none; review only'" not in js:
    failures.append('the review export no longer records implementation: none')

# --- 5. the section must not claim the page can decide anything -----------------
for bad in ('this page records the decision', 'your choice is now live', 'applied automatically'):
    if bad in section.lower():
        failures.append(f'the section overclaims: "{bad}"')

if failures:
    print(f'FAIL: {len(failures)} decision-record problem(s)')
    for f in failures:
        print(' -', f)
    sys.exit(1)

data = json.loads((ROOT / 'data' / 'shop' / 'decisions.json').read_text(encoding='utf-8'))
print(f'PASS: decision record — 5 fields sourced, template copyable, '
      f'{len(data["decisions"])} decisions already in the register')

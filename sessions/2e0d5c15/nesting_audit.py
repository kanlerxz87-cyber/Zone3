#!/usr/bin/env python3
"""Read-only HTML nesting audit for the published tree (session 2e0d5c15, 2026-11-20).

Reproduces the measurement behind flag 2E0-F02. It parses every published HTML page
outside archive/, docs/ and sessions/ with Python's standard-library html.parser and
reports two things per page:

  * stray end tags — a closing tag whose element is not the one currently open;
  * elements still open at end of file.

Scope note. This is a nesting check, not a validator. html.parser does not implement the
HTML5 tree-construction rules (implied end tags for <p>, <li>, table sections), so a page
that a browser would repair silently is reported here too. That is why the finding is
scoped to pages that are noindex and outside the reader set, and why no rendering defect
is claimed: none was measured in a browser.

    python3 sessions/2e0d5c15/nesting_audit.py            # human-readable report
    python3 sessions/2e0d5c15/nesting_audit.py --json     # machine-readable report
"""
from __future__ import annotations

import json
import pathlib
import sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[2]
SKIP_DIRS = {'archive', 'docs', 'sessions', '.git', 'node_modules', '__pycache__'}
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta',
        'param', 'source', 'track', 'wbr'}


class Nesting(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.stray: list[str] = []
        self.duplicate_attrs: list[str] = []

    def handle_starttag(self, tag, attrs):
        names = [name for name, _ in attrs]
        duplicates = {name for name in names if names.count(name) > 1}
        if duplicates:
            self.duplicate_attrs.append(f'{tag}: {sorted(duplicates)}')
        if tag not in VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack and self.stack[-1] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.stray.append(f'</{tag}> (open: {self.stack[-3:]})')


def pages() -> list[pathlib.Path]:
    out = []
    for path in ROOT.rglob('*.html'):
        rel = path.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        out.append(path)
    return sorted(out)


def audit() -> dict:
    report = {'checked': 0, 'flagged': []}
    for path in pages():
        rel = path.relative_to(ROOT).as_posix()
        parser = Nesting()
        parser.feed(path.read_text(encoding='utf-8', errors='replace'))
        parser.close()
        report['checked'] += 1
        if parser.stray or parser.stack or parser.duplicate_attrs:
            text = path.read_text(encoding='utf-8', errors='replace')
            report['flagged'].append({
                'page': rel,
                'robots': ('noindex' if 'noindex' in (text.split('name="robots"')[1][:80]
                                                      if 'name="robots"' in text else '') else 'indexable'),
                'stray_end_tags': parser.stray[:5],
                'unclosed_at_eof': parser.stack[-5:],
                'duplicate_attributes': parser.duplicate_attrs[:5],
            })
    return report


if __name__ == '__main__':
    result = audit()
    if '--json' in sys.argv:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"nesting audit: {result['checked']} published pages checked, "
              f"{len(result['flagged'])} reported")
        for row in result['flagged']:
            print(f"  {row['page']}  [{row['robots']}]")
            for item in row['stray_end_tags']:
                print(f"      stray end tag: {item}")
            if row['unclosed_at_eof']:
                print(f"      unclosed at EOF: {row['unclosed_at_eof']}")
            for item in row['duplicate_attributes']:
                print(f"      duplicate attribute: {item}")

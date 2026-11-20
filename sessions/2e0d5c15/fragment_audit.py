#!/usr/bin/env python3
"""Read-only in-page fragment audit for the published tree (session 2e0d5c15, 2026-11-20).

Every internal link that carries a '#fragment' is resolved against the file it points at,
and the fragment is checked against the ids that file actually declares. This is the class
of broken link a URL checker misses, because the file exists and returns 200; only the
anchor is missing.

    python3 sessions/2e0d5c15/fragment_audit.py           # human-readable
    python3 sessions/2e0d5c15/fragment_audit.py --json    # machine-readable

Scope: published pages only (archive/, docs/ and sessions/ are excluded). Absolute http(s)
links are out of scope; they are checked by scripts/check_all_links.py.
"""
from __future__ import annotations

import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SKIP_DIRS = {'archive', 'docs', 'sessions', '.git', 'node_modules', '__pycache__'}
_ids: dict[pathlib.Path, set[str]] = {}


def ids_of(path: pathlib.Path) -> set[str]:
    if path not in _ids:
        text = path.read_text(encoding='utf-8', errors='replace')
        _ids[path] = set(re.findall(r'\bid="([^"]+)"', text))
    return _ids[path]


def pages() -> list[pathlib.Path]:
    return sorted(p for p in ROOT.rglob('*.html')
                  if not any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts))


def audit() -> dict:
    checked = 0
    broken: list[dict] = []
    for page in pages():
        text = page.read_text(encoding='utf-8', errors='replace')
        for match in re.finditer(r'href="([^"]*#[^"]+)"', text):
            target = html.unescape(match.group(1))
            if target.startswith(('http', '//')):
                continue
            checked += 1
            path_part, _, fragment = target.partition('#')
            resolved = (pathlib.Path(str(page.parent / path_part)).resolve() if path_part
                        else page.resolve())
            if resolved.is_dir():
                resolved = resolved / 'index.html'
            if not resolved.exists():
                broken.append({'page': page.relative_to(ROOT).as_posix(), 'href': target,
                               'reason': 'target file missing'})
                continue
            if resolved.suffix != '.html':
                continue
            if fragment not in ids_of(resolved):
                broken.append({'page': page.relative_to(ROOT).as_posix(), 'href': target,
                               'reason': 'fragment not declared in target'})
    return {'links_checked': checked, 'broken': broken}


if __name__ == '__main__':
    result = audit()
    if '--json' in sys.argv:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"fragment audit: {result['links_checked']} in-page links checked, "
              f"{len(result['broken'])} broken")
        for row in result['broken']:
            print(f"  {row['page']} -> {row['href']}  ({row['reason']})")

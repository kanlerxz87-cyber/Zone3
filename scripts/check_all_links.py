#!/usr/bin/env python3
"""Audit every published HTML page in the repo for broken internal links.

Standard library only. Run from the repository root:

    python3 scripts/check_all_links.py

Scope: all .html files except archive/ (historical, not published on Pages...
actually archive/ IS published too, but it is a frozen record; report-only).
For each page: every relative href must resolve to an existing file; every
#fragment must exist as an id in the target file. External links are listed
but not fetched (this runner's network is limited to GitHub hosts).
"""
from __future__ import annotations

import pathlib
from html.parser import HTMLParser
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if "name" in a and tag == "a":
            self.ids.add(a["name"])
        if tag in ("a", "link") and "href" in a:
            self.hrefs.append(a["href"])
        if tag == "script" and "src" in a:
            self.hrefs.append(a["src"])


def main() -> int:
    pages = sorted(p for p in ROOT.rglob("*.html") if ".git" not in p.parts)
    parsed: dict[pathlib.Path, P] = {}
    for p in pages:
        parser = P()
        try:
            parser.feed(p.read_text(encoding="utf-8"))
        except Exception as ex:  # unreadable file
            print(f"READ-FAIL {p.relative_to(ROOT)}: {ex}")
            continue
        parsed[p] = parser

    errors = 0
    external: set[str] = set()
    for p, parser in parsed.items():
        rel = p.relative_to(ROOT)
        in_archive = rel.parts and rel.parts[0] == "archive"
        for href in parser.hrefs:
            u = urlparse(href)
            if u.scheme in ("http", "https", "mailto", "tel"):
                external.add(href)
                continue
            if u.scheme:
                continue
            target = (p.parent / (u.path or p.name)).resolve()
            try:
                target.relative_to(ROOT)
            except ValueError:
                if not in_archive:
                    print(f"OUTSIDE {rel}: {href}")
                    errors += 1
                continue
            if not target.exists():
                if in_archive:
                    continue  # frozen record; report only at the end
                print(f"BROKEN FILE {rel}: {href}")
                errors += 1
                continue
            if u.fragment and target.suffix == ".html":
                tp = parsed.get(target)
                if tp is None:
                    tp = P()
                    tp.feed(target.read_text(encoding="utf-8"))
                    parsed[target] = tp
                if u.fragment not in tp.ids:
                    if in_archive:
                        continue
                    print(f"BROKEN ANCHOR {rel}: {href}")
                    errors += 1
    print(f"checked {len(pages)} html pages, {len(external)} distinct external URLs, {errors} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

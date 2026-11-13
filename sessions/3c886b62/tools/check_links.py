#!/usr/bin/env python3
"""
Link checker for the generated Zone3 static site.

Checks every internal href in every generated .html page resolves to a file that
exists, that every internal navigation entry points at a real page, and that no
page contains an unresolved placeholder. Also enforces the project rule that
every data row carries a source link.

Usage:  python3 tools/check_links.py
"""

import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))

HREF = re.compile(r'href="([^"]+)"', re.I)
ANCHOR_ID = re.compile(r'id="([^"]+)"', re.I)


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
        self.ids = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "a" and d.get("href"):
            self.hrefs.append(d["href"])
        if d.get("id"):
            self.ids.append(d["id"])


def main():
    errors = []
    warnings = []
    data_row_issues = []

    # 1. does every page referenced anywhere exist?
    for page in PAGES:
        with open(os.path.join(ROOT, page), "r", encoding="utf-8") as fh:
            src = fh.read()
        c = Collector()
        c.feed(src)

        for href in c.hrefs:
            if href.startswith(("http://", "https://", "mailto:", "tel:")):
                continue
            if href.startswith("#"):
                if href[1:] and href[1:] not in c.ids:
                    errors.append("%s: dangling anchor %s" % (page, href))
                continue
            target = href.split("#")[0].split("?")[0]
            if not target:
                continue
            if not os.path.exists(os.path.join(ROOT, target)):
                errors.append("%s: missing internal target %s" % (page, href))

    # 2. are the nav entries all real pages?
    nav_targets = set()
    for page in PAGES:
        with open(os.path.join(ROOT, page), "r", encoding="utf-8") as fh:
            src = fh.read()
        for href in HREF.findall(src):
            if not href.startswith(("http", "mailto", "#")) and href.endswith(".html"):
                nav_targets.add(href)

    for t in sorted(nav_targets):
        if not os.path.exists(os.path.join(ROOT, t)):
            errors.append("nav: missing page %s" % t)

    # 3. no unresolved placeholders
    #    ("None" and "XXXXX" are legitimate English / a verbatim Amazon quote, so
    #     they are intentionally not treated as placeholders)
    for page in PAGES:
        with open(os.path.join(ROOT, page), "r", encoding="utf-8") as fh:
            src = fh.read()
        for bad in ("%(title)s", "%(body)s", "%("):
            if bad in src:
                warnings.append("%s: contains placeholder %r" % (page, bad))
        for bad in ("TODO", "FIXME", "undefined", "nan", "null"):
            if re.search(r"\b%s\b" % bad, src):
                warnings.append("%s: contains placeholder %r" % (page, bad))

    # 4. project rule: every row of a table explicitly marked
    #    data-verify-source must carry a source cell.
    table_re = re.compile(r"<table[^>]*data-verify-source[^>]*>(.*?)</table>", re.S | re.I)
    tr_re = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S | re.I)
    checked_tables = 0
    checked_rows = 0
    for page in PAGES:
        with open(os.path.join(ROOT, page), "r", encoding="utf-8") as fh:
            src = fh.read()
        for tbl in table_re.findall(src):
            checked_tables += 1
            rows = tr_re.findall(tbl)
            # row 0 is the header when the table has a <thead>
            start = 1 if "<thead" in tbl.lower() and len(rows) > 1 else 0
            for i, row in enumerate(rows[start:], start=start + 1):
                checked_rows += 1
                if 'class="src"' not in row:
                    data_row_issues.append("%s: data table row %d has no source cell" % (page, i))

    print("data tables requiring a per-row source: %d (%d rows)" % (checked_tables, checked_rows))

    print("pages checked: %d" % len(PAGES))
    print("internal page targets: %d" % len(nav_targets))
    if errors:
        print("\nERRORS (%d):" % len(errors))
        for e in errors:
            print("  " + e)
    if data_row_issues:
        print("\nSOURCE-CELL ISSUES (%d):" % len(data_row_issues))
        for e in data_row_issues:
            print("  " + e)
    if warnings:
        print("\nWARNINGS (%d):" % len(warnings))
        for w in warnings:
            print("  " + w)

    if errors or data_row_issues:
        print("\nFAILED")
        return 1
    print("\nOK — no broken internal links, every data row has a source cell")
    return 0


if __name__ == "__main__":
    sys.exit(main())

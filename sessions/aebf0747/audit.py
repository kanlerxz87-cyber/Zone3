#!/usr/bin/env python3
"""Measures the publication markup over every published HTML file (session aebf0747).

    python3 sessions/aebf0747/audit.py [ROOT]      # prints JSON

Uses the same definitions as publish_pass.py: the disclosure must sit within 2,500 characters
after the top masthead; a product link is an Amazon retail or short-link host, excluding the
Associates policy pages. archive/ is excluded, as in publish_pass.py.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import publish_pass as pp  # noqa: E402


def measure(root: pathlib.Path) -> dict:
    stats = dict(pages=0, disclosure_above_fold=0, disclosure=0, footer_disclosure=0,
                 title=0, description=0, rss=0, amazon_links=0, amazon_links_sponsored=0,
                 amazon_links_missing_sponsored=0)
    for p, rel in pp.targets(root):
        t = p.read_text(encoding="utf-8", errors="replace")
        stats["pages"] += 1
        if pp.DISCLOSURE in t:
            stats["disclosure"] += 1
        try:
            end = pp.top_masthead_end(t)
            if pp.DISCLOSURE in t[end:end + 2500]:
                stats["disclosure_above_fold"] += 1
        except ValueError:
            pass
        footers = re.findall(r"<footer\b.*?</footer>|<!-- z3:footer -->.*?<!-- /z3:footer -->", t, re.S | re.I)
        if any(pp.DISCLOSURE in f for f in footers):
            stats["footer_disclosure"] += 1
        stats["title"] += int(bool(re.search(r"<title>[^<]+</title>", t, re.I)))
        stats["description"] += int(bool(re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=', t, re.I)))
        stats["rss"] += int("application/rss+xml" in t)
        for a in re.findall(r"<a\b[^>]*>", t, re.I):
            href = re.search(r"""\shref\s*=\s*(["'])(.*?)\1""", a, re.I)
            if not href:
                continue
            host_m = re.match(r"^(?:https?:)?//([^/?#]+)", href.group(2).strip(), re.I)
            if not host_m:
                continue
            host = host_m.group(1).lower().split(":")[0]
            if any(host == h or host.endswith("." + h) for h in pp.NON_PRODUCT_HOSTS):
                continue
            if not pp.PRODUCT_HOST.match(host):
                continue
            stats["amazon_links"] += 1
            rel_m = re.search(r"""\srel\s*=\s*(["'])(.*?)\1""", a, re.I)
            if rel_m and "sponsored" in rel_m.group(2).split():
                stats["amazon_links_sponsored"] += 1
            else:
                stats["amazon_links_missing_sponsored"] += 1
    return stats


if __name__ == "__main__":
    root = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else pp.ROOT
    print(json.dumps(measure(root), indent=1))

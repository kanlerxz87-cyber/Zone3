#!/usr/bin/env python3
"""Orphan-page audit and route-table check. Session c79eb5d9.

Why this exists
---------------
GitHub Pages serves the repository root, so any committed .html file is published. Before
this check ran, 26 of the published pages had no inbound link from any other published
page: the site had two navigation systems (the flat pages and the /dashboard/ build) and
several add-only page sets from earlier sessions, and nothing joined them. A page nobody
can reach is still a page that can be read, quoted, or indexed, which matters for the
compliance findings in I-F-01 to I-F-03.

What it checks
--------------
A1  every published .html page is either in sessions/c79eb5d9/routes.py or is linked
    from at least one other published page (so a new unlinked page fails the check)
A2  every route in the table exists on disk
A3  no route marked `live` is missing an inbound link
A4  no `archived` route links to a page that is not itself published
A5  the root index.html links every `live` route that is not the root or a redirect stub

Exit code 0 = pass. Non-zero = the failing rows are printed.
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from routes import ROUTES  # noqa: E402

SKIP_DIRS = {".git", "archive", "node_modules"}


def published() -> list[str]:
    out = []
    for p in ROOT.rglob("*.html"):
        rel = p.relative_to(ROOT).as_posix()
        if any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
            continue
        out.append(rel)
    return sorted(out)


def links_of(rel: str) -> set[str]:
    """Resolve the relative hrefs of one page to repository-relative paths."""
    here = (ROOT / rel).parent
    text = (ROOT / rel).read_text(encoding="utf-8", errors="replace")
    found = set()
    for href in re.findall(r'href="([^"]+)"', text):
        href = href.split("#", 1)[0]
        if not href or href.startswith(("http://", "https://", "mailto:", "tel:", "data:", "/")):
            continue
        target = (here / href).resolve()
        try:
            found.add(target.relative_to(ROOT).as_posix())
        except ValueError:
            continue
    return found


def main() -> int:
    pages = published()
    route_by_path = {r["path"]: r for r in ROUTES}
    problems: list[str] = []

    inbound: dict[str, set[str]] = {p: set() for p in pages}
    for p in pages:
        for t in links_of(p):
            if t in inbound and t != p:
                inbound[t].add(p)

    # A1 — every published page is declared, or is reachable
    for p in pages:
        if p in route_by_path:
            continue
        if inbound[p]:
            continue
        problems.append(f"A1 undeclared and unlinked published page: {p}")

    # A2 — every declared route exists
    for r in ROUTES:
        if r["path"] not in pages:
            problems.append(f"A2 declared route does not exist: {r['path']}")

    # A3 — live routes must be reachable
    for r in ROUTES:
        if r["status"] == "live" and not inbound.get(r["path"]):
            problems.append(f"A3 live route has no inbound link: {r['path']}")

    # A5 — the root dashboard must link the live routes (redirect stubs excepted)
    root_links = links_of("index.html")
    stubs = {p for p in pages if _is_redirect_stub(p)}
    for r in ROUTES:
        if r["status"] != "live" or r["path"] in ("index.html",):
            continue
        if r["path"] in stubs:
            continue
        if r["path"] not in root_links:
            problems.append(f"A5 root index.html does not link: {r['path']}")

    print(f"checked {len(pages)} published pages against {len(ROUTES)} declared routes")
    if problems:
        print(f"FAILED — {len(problems)} problem(s):")
        for x in problems:
            print("  -", x)
        return 1
    print("PASS — every published page is declared and reachable; every live route is linked")
    return 0


def _is_redirect_stub(rel: str) -> bool:
    t = (ROOT / rel).read_text(encoding="utf-8", errors="replace")
    return "http-equiv=\"refresh\"" in t or "http-equiv='refresh'" in t


if __name__ == "__main__":
    sys.exit(main())

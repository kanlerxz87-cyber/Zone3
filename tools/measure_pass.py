#!/usr/bin/env python3
"""Add the measurement script tags to every published HTML page (build 38650305).

Inserts, just before </head> and inside markers:
    <!-- z3:measure --><script src="<prefix>assets/measure-config.js"></script>
    <script src="<prefix>assets/measure.js" defer></script><!-- /z3:measure -->
Idempotent: an existing block is replaced, not stacked. Skips archive/, docs/, sessions/ and .git/,
the same set as the publish pass. Both scripts are first-party files in assets/.

    python3 tools/measure_pass.py           # apply
    python3 tools/measure_pass.py --check   # exit 1 if a rerun would change any page

Run after any generator that rewrites HTML, and after sessions/aebf0747/publish_pass.py.
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKIP_TOP = {".git", "archive", "docs", "sessions", "node_modules", "__pycache__"}
RE_BLOCK = re.compile(r"<!-- z3:measure -->.*?<!-- /z3:measure -->\n?", re.S)


def block(prefix: str) -> str:
    return (
        "<!-- z3:measure -->"
        f'<script src="{prefix}assets/measure-config.js"></script>'
        f'<script src="{prefix}assets/measure.js" defer></script>'
        "<!-- /z3:measure -->\n"
    )


def apply(html: str, rel: str) -> str:
    depth = rel.count("/")
    prefix = "../" * depth
    html = RE_BLOCK.sub("", html)
    # Inside <head>, before </head>. The publish pass places its strip under the masthead and its
    # footer before </body>, and adds head markup only once, so this position is stable on reruns.
    if re.search(r"</head\s*>", html, re.I):
        return re.sub(r"</head\s*>", lambda _m: block(prefix) + "</head>", html, count=1, flags=re.I)
    return block(prefix) + html


def run(write: bool) -> tuple[int, int]:
    pages = changed = 0
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT).as_posix()
        if rel.split("/")[0] in SKIP_TOP:
            continue
        pages += 1
        old = p.read_text(encoding="utf-8", errors="replace")
        new = apply(old, rel)
        if new != old:
            changed += 1
            if write:
                p.write_text(new, encoding="utf-8")
    return pages, changed


if __name__ == "__main__":
    check = "--check" in sys.argv
    pages, changed = run(write=not check)
    print(f"measure pass: {pages} pages, {changed} {'would change' if check else 'changed'}")
    sys.exit(1 if (check and changed) else 0)

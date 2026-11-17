#!/usr/bin/env python3
"""Internal link check over the published tree (session aebf0747). Reports relative href/src
targets that do not exist as files. External links are not fetched here.

    python3 sessions/aebf0747/link_check.py [ROOT] [--only-new]
"""
from __future__ import annotations
import pathlib, re, sys, urllib.parse
ROOT = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else pathlib.Path(__file__).resolve().parents[2]
SKIP = {".git", "archive"}
broken = []
for p in sorted(ROOT.rglob("*.html")):
    rel = p.relative_to(ROOT).as_posix()
    if rel.split("/")[0] in SKIP:
        continue
    t = p.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"""\s(?:href|src)\s*=\s*["']([^"']+)["']""", t, re.I):
        u = m.group(1).strip()
        if not u or u.startswith(("#", "http://", "https://", "mailto:", "tel:", "data:", "javascript:", "${")):
            continue
        path = urllib.parse.unquote(u.split("#")[0].split("?")[0])
        if not path:
            continue
        target = (p.parent / path) if not path.startswith("/") else (ROOT / path.lstrip("/"))
        if target.is_dir():
            target = target / "index.html"
        if not target.exists():
            broken.append((rel, u))
print(f"broken internal links: {len(broken)}")
for src, u in broken[:200]:
    print(f"  {src}  ->  {u}")

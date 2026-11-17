#!/usr/bin/env python3
"""One-off (ded63349): wire mark_sponsored into tools/build_cba81fa5_site.py writes.

The regex used by the emitted helper is copied verbatim from tools/apply_sponsored.py
(the canonical enforcer), so the two definitions cannot drift.
"""
import pathlib
import re as _re

ROOT = pathlib.Path(__file__).resolve().parent.parent
AP = (ROOT / "tools" / "apply_sponsored.py").read_text(encoding="utf-8")
m = _re.search(r"PRODUCT_HREF = re\.compile\(\n(.*?)re\.I\)\n", AP, _re.S)
assert m, "PRODUCT_HREF block not found in apply_sponsored.py"
PATTERN_BLOCK = m.group(0).replace("PRODUCT_HREF", "MARK_PRODUCT_HREF", 1)

helper = (
    "# ---------------------------------------------------------------------------\n"
    "# Sponsored rel (session ded63349, 2026-11-17; proposal D-19). The regions this\n"
    "# integrator writes contain product links (the fd-card listings); they are marked\n"
    "# here so a cba rebuild equals the post-pass tree that tools/apply_sponsored.py\n"
    "# --check and tools/i2_gate.py G11 expect. The pattern below is copied verbatim\n"
    "# from tools/apply_sponsored.py, which stays the canonical enforcer.\n"
    + PATTERN_BLOCK
    + "MARK_ANCHOR_RE = re.compile(r'<a\\b[^>]*>', re.I)\n"
    "\n"
    "\n"
    "def mark_sponsored(html: str) -> str:\n"
    "    def fix(m):\n"
    "        tag = m.group(0)\n"
    "        href = re.search(r'href=\"([^\"]*)\"', tag)\n"
    "        if not href or not MARK_PRODUCT_HREF.search(href.group(1)):\n"
    "            return tag\n"
    "        rel = re.search(r'rel=\"([^\"]*)\"', tag)\n"
    "        if rel:\n"
    "            if \"sponsored\" in rel.group(1).split():\n"
    "                return tag\n"
    "            tokens = [t for t in (\"sponsored\",) if t not in rel.group(1).split()]\n"
    "            return tag[:rel.start(1)] + \" \".join(tokens + rel.group(1).split()) + tag[rel.end(1):]\n"
    "        return tag[:-1].rstrip() + ' rel=\"sponsored noopener noreferrer\">'\n"
    "    return MARK_ANCHOR_RE.sub(fix, html)\n"
)

p = ROOT / "tools" / "build_cba81fa5_site.py"
raw = p.read_text(encoding="utf-8")

anchor = "def is_short_link(url: str) -> bool:"
assert anchor in raw and "def mark_sponsored" not in raw
raw = raw.replace(anchor, helper + "\n\n" + anchor, 1)

subs = [
    ('                path.write_text(want, encoding="utf-8")',
     '                path.write_text(mark_sponsored(want), encoding="utf-8")'),
    ('                root_index.write_text(want, encoding="utf-8")',
     '                root_index.write_text(mark_sponsored(want), encoding="utf-8")'),
    ('                fl.write_text(want, encoding="utf-8")',
     '                fl.write_text(mark_sponsored(want), encoding="utf-8")'),
]
for old, new in subs:
    assert old in raw, old
    raw = raw.replace(old, new, 1)

p.write_text(raw, encoding="utf-8")
print("build_cba81fa5_site: mark_sponsored wired on 3 write sites")

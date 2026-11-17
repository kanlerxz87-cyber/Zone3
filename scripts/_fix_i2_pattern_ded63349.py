#!/usr/bin/env python3
"""One-off (ded63349): replace MARK_PRODUCT_HREF in tools/build_i2_site.py with the
verbatim pattern from tools/apply_sponsored.py."""
import pathlib
import re as _re

ROOT = pathlib.Path(__file__).resolve().parent.parent
AP = (ROOT / "tools" / "apply_sponsored.py").read_text(encoding="utf-8")
m = _re.search(r"PRODUCT_HREF = re\.compile\(\n(.*?)re\.I\)\n", AP, _re.S)
PATTERN_BLOCK = m.group(0).replace("PRODUCT_HREF", "MARK_PRODUCT_HREF", 1)

p = ROOT / "tools" / "build_i2_site.py"
raw = p.read_text(encoding="utf-8")
start = raw.index("MARK_PRODUCT_HREF = re.compile(")
end = raw.index("re.I)", start) + len("re.I)")
raw = raw[:start] + PATTERN_BLOCK.rstrip("\n") + raw[end:]
p.write_text(raw, encoding="utf-8")
print("build_i2_site: MARK_PRODUCT_HREF replaced with canonical pattern")

#!/usr/bin/env python3
"""One-off fix (ded63349): correct the product-link pattern in apply_sponsored.py and i2_gate.py.

The first draft required /<something>/dp/ (two slashes), which missed the direct
amazon.com/dp/<ASIN> form used by most evidence links. This patch replaces the pattern
in both tools with one that matches:
  * link.amazon short links (any token),
  * amazon.<tld>/dp/<10-char ASIN> (with or without a slug prefix, with any query),
  * amazon.<tld>/gp/product/<10-char ASIN>.
Nine-character dp probes (Page-Not-Found evidence) deliberately do not match.
"""
import pathlib

BS = chr(92)
ROOT = pathlib.Path(__file__).resolve().parent.parent

NEW = (
    "PRODUCT_HREF = re.compile(\n"
    "    r'https?://[^" + BS + '"' + BS + "']*link" + BS + ".amazon/[^" + BS + '"' + BS + "']*'\n"
    "    r'|https?://[^" + BS + '"' + BS + "']*(?:amazon" + BS + ".[a-z]{2,3})/[^" + BS + '"' + BS + "']*(?:/dp/[A-Z0-9]{10}|/gp/product/[A-Z0-9]{10})[^" + BS + '"' + BS + "']*', re.I)\n"
)

OLD_HEAD = "PRODUCT_HREF = re.compile("
for rel in ("tools/apply_sponsored.py", "tools/i2_gate.py"):
    p = ROOT / rel
    raw = p.read_text(encoding="utf-8")
    start = raw.index(OLD_HEAD)
    end = raw.index("re.I)", start) + len("re.I)")
    raw = raw[:start] + NEW + raw[end:]
    p.write_text(raw, encoding="utf-8")
    print(f"{rel}: pattern replaced")

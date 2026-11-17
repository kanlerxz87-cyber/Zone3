#!/usr/bin/env python3
"""One-off patch (ded63349): insert PRODUCT_HREF constant + G11 rule into tools/i2_gate.py."""
import pathlib

P = pathlib.Path(__file__).resolve().parent.parent / "tools" / "i2_gate.py"
raw = P.read_text(encoding="utf-8")

BS = chr(92)  # backslash

PRODUCT_HREF_BLOCK = (
    "# Product-page URLs only (ded63349): /dp/ and /gp/product/ on any amazon host and the\n"
    "# submitted link.amazon short links. Browse-node, search and help pages are not product\n"
    "# links, so they are deliberately left out of this rule.\n"
    "PRODUCT_HREF = re.compile(\n"
    "    r'https?://[^" + BS + '"' + BS + "']*?(?:amazon" + BS + ".[a-z]{2,3})?/[^" + BS + '"' + BS + "']*(?:/dp/[A-Z0-9]{10}|/gp/product/[A-Z0-9]{10})[^" + BS + '"' + BS + "']*'\n"
    "    r'|https?://link" + BS + ".amazon/[^" + BS + '"' + BS + "']*', re.I)\n\n"
)

G11_BLOCK = (
    "        # ---- G11 sponsored rel on product links (ded63349, 2026-11-17; proposal D-19)\n"
    "        # Every outbound link to an Amazon product page must carry rel=\"sponsored\":\n"
    "        # the site's declared purpose is Associates promotion, so the relationship\n"
    "        # markup travels with the link even while no Associates tag exists. Policy\n"
    "        # and documentation links are not product links and stay unmarked.\n"
    "        for m_tag in ANCHOR_RE.finditer(raw):\n"
    "            atag = m_tag.group(0)\n"
    "            href_m = re.search(r'href=\"([^\"]*)\"', atag)\n"
    "            if not href_m:\n"
    "                continue\n"
    "            href = href_m.group(1)\n"
    "            if not PRODUCT_HREF.search(href):\n"
    "                continue\n"
    "            rel_m = re.search(r'rel=\"([^\"]*)\"', atag)\n"
    "            if not rel_m or \"sponsored\" not in rel_m.group(1).split():\n"
    "                errs.append(f\"G11 {rel}: product link without rel=\" + BS + '\"sponsored\"' + BS + '\" -> {href[:80]}\")\n\n"
)

anchor_const = "OFFICIAL_HOSTS = re.compile("
assert "PRODUCT_HREF" not in raw, "PRODUCT_HREF already present"
raw = raw.replace(anchor_const, PRODUCT_HREF_BLOCK + anchor_const, 1)

anchor_g8 = "        # ---- G8 internal links and anchors"
assert anchor_g8 in raw
raw = raw.replace(anchor_g8, G11_BLOCK + anchor_g8, 1)

# docstring: extend the check list
raw = raw.replace(
    "  G9  no placeholder marker (TODO/FIXME/TBD/lorem/XXXX)",
    "  G9  no placeholder marker (TODO/FIXME/TBD/lorem/XXXX)\n"
    "  G11 every outbound product link carries rel=\"sponsored\" (proposal D-19)",
    1,
)

P.write_text(raw, encoding="utf-8")
print("patched:", "PRODUCT_HREF" in P.read_text(), "G11 present:", "G11 {rel}" in P.read_text())

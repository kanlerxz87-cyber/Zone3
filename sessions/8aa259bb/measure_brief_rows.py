#!/usr/bin/env python3
"""Re-measure the brief's S-04..S-25 and SG-27..SG-30 rows against this checkout (session 8aa259bb).

Read-only. Prints JSON facts; nothing is written here. Definitions:
- "published page": any *.html under the repo root, excluding archive/, docs/, sessions/, node_modules/, .git/.
- Each measurement names its rule so the register text can cite it.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[2]
EXCL = ("archive/", "docs/", "sessions/", "node_modules/", ".git/")
DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases"


def pages() -> list[pathlib.Path]:
    out = []
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT).as_posix()
        if any(rel.startswith(e) for e in EXCL):
            continue
        out.append(p)
    return out


def rd(p: pathlib.Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def main() -> int:
    ps = pages()
    rels = [p.relative_to(ROOT).as_posix() for p in ps]
    facts: dict = {"published_pages": len(ps)}

    no_title, no_desc = [], []
    for p, rel in zip(ps, rels):
        t = rd(p)
        if not re.search(r"<title>\s*[^<\s][^<]*</title>", t, re.I):
            no_title.append(rel)
        if not re.search(r'<meta\s+name="description"\s+content="[^"]+"', t, re.I):
            no_desc.append(rel)
    facts["pages_missing_title"] = no_title
    facts["pages_missing_meta_description"] = no_desc

    amz_links = 0
    amz_unsponsored = []
    pages_with_amz = 0
    for p, rel in zip(ps, rels):
        t = rd(p)
        n_page = 0
        for m in re.finditer(r"<a\b[^>]*href=\"(https?://(?:[a-z0-9.-]*\.)?(?:amazon\.[a-z.]+|link\.amazon[^\"]*))[^\"]*\"[^>]*>", t, re.I):
            tag = m.group(0)
            n_page += 1
            if not re.search(r'rel="[^"]*sponsored', tag, re.I):
                amz_unsponsored.append(rel)
        amz_links += n_page
        pages_with_amz += bool(n_page)
    facts["amazon_anchor_links"] = amz_links
    facts["pages_with_amazon_links"] = pages_with_amz
    facts["amazon_links_without_rel_sponsored"] = len(amz_unsponsored)
    facts["amazon_links_without_rel_sponsored_pages"] = sorted(set(amz_unsponsored))[:20]

    facts["pages_with_disclosure_sentence"] = sum(DISCLOSURE in rd(p) for p in ps)
    facts["pages_with_og_image"] = sum(bool(re.search(r'property="og:image"', rd(p))) for p in ps)
    facts["pages_with_json_ld"] = sum(bool(re.search(r'application/ld\+json', rd(p))) for p in ps)
    facts["pages_mentioning_trending"] = sum(bool(re.search(r"\btrending\b", rd(p), re.I)) for p in ps)
    facts["pages_with_which_one_is_for_you"] = sum("which one is for you" in rd(p).lower() for p in ps)
    facts["pages_with_per_centimetre_or_per_cm"] = [
        rel for p, rel in zip(ps, rels) if re.search(r"per (centi)?met(re|er)|per cm\b", rd(p), re.I)
    ]
    facts["pages_with_working_name"] = sum("working name" in rd(p).lower() for p in ps)

    guides = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "guides").glob("*.html") if p.name != "index.html")
    articles = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "articles").glob("*.html") if p.name != "index.html")
    facts["guides_question_led_pages"] = guides
    facts["articles_pages"] = articles

    # Internal links per article/guide: buying guide, category pillar, comparison/products.
    def links_of(rel: str) -> set[str]:
        t = rd(ROOT / rel)
        return set(re.findall(r'href="([^"#?]+)', t))

    facts["guide_to_shop_or_category_links"] = {}
    for rel in guides + articles:
        L = links_of(rel)
        facts["guide_to_shop_or_category_links"][rel] = sorted(
            x for x in L if re.search(r"shop/(products|air-fryers|meat-thermometers)|category/|/products", x)
        )

    feed = ROOT / "feed.xml"
    if feed.exists():
        root = ET.parse(feed).getroot()
        items = root.findall(".//item")
        facts["feed_items"] = len(items)
    sm = ET.parse(ROOT / "sitemap.xml").getroot()
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    facts["sitemap_urls"] = len(sm.findall("s:url", ns))

    facts["design_prompt_md_exists"] = (ROOT / "DESIGN_PROMPT.md").exists()
    facts["design_prompt_md_bracket_placeholders"] = len(re.findall(r"\[[^\]]{2,80}\]", rd(ROOT / "DESIGN_PROMPT.md"))) if (ROOT / "DESIGN_PROMPT.md").exists() else None
    facts["ai_generated_image_labels"] = sorted(
        rel for p, rel in zip(ps, rels) if "AI-generated" in rd(p)
    )[:40]
    facts["ai_generated_pages_count"] = sum("AI-generated" in rd(p) for p in ps)
    facts["assets_img"] = sorted(x.name for x in (ROOT / "assets" / "img").glob("*"))
    facts["chooser_mentions"] = sorted(rel for p, rel in zip(ps, rels) if re.search(r"chooser", rd(p), re.I))
    facts["question_router_or_chooser_ids"] = sorted(
        rel for p, rel in zip(ps, rels) if re.search(r'id="(chooser|router|question-router)"', rd(p))
    )
    json.dump(facts, sys.stdout, indent=1, ensure_ascii=False, default=str)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

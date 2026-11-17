#!/usr/bin/env python3
"""One-shot integration edits for session 2f181cd9 on scripts/build_site.py.

Targeted string replacements only. Each replacement is asserted, so a future edit that
changes the surrounding copy fails loudly instead of silently dropping the fix.
"""
from __future__ import annotations

import pathlib

P = pathlib.Path("scripts/build_site.py")
t = P.read_text(encoding="utf-8")

EDITS: list[tuple[str, str, str]] = [
    # 1. Product cards: the two new products get a brief link and a one-liner.
    (
        "brief_slugs",
        '        "P3": "marketing/product-3-chefman-8-quart-turbofry.html",\n    }',
        '        "P3": "marketing/product-3-chefman-8-quart-turbofry.html",\n'
        '        # Added by session 2f181cd9 (2026-11-17): P4 and P5 have no product brief yet. They point at\n'
        '        # the intake register row, which is the only page that states what is known about them.\n'
        '        "P4": "sessions/2f181cd9/intake.html#P4",\n'
        '        "P5": "sessions/2f181cd9/intake.html#P5",\n    }',
    ),
    (
        "one_lines",
        '        "P3": "An 8-quart single-basket fryer with a TurboFry 4-in-1 function set (air fry, bake, dehydrate, frozen) and an XL nonstick dishwasher-safe basket.",\n    }',
        '        "P3": "An 8-quart single-basket fryer with a TurboFry 4-in-1 function set (air fry, bake, dehydrate, frozen) and an XL nonstick dishwasher-safe basket.",\n'
        '        # Added by session 2f181cd9 (2026-11-17). Both lines are read from the destination listing\n'
        '        # title only; no specification beyond the title is claimed.\n'
        '        "P4": "An instant-read digital meat thermometer with NIST and NSF certification, an auto-rotating bright LED screen and a waterproof body, in the Thermometers and Timers category.",\n'
        '        "P5": "A smart wireless meat thermometer with three ultra-thin probes, WiFi unlimited range and five sensors, sold as the CHEF iQ Sense Gen3.",\n    }',
    ),
    # 2. The per-card fetch date comes from the product record, not from a hard-coded date.
    (
        "card_date",
        """            f'<p class="small">Observed destination of {e(p["submitted_url"])}, re-fetched '
            f'2026-11-16 ({src_links([ro["source"]])} &middot; {src_links([ro.get("title_source", ro["source"])])}). '""",
        """            f'<p class="small">Observed destination of {e(p["submitted_url"])}, re-fetched '
            f'{e(ro.get("observed_on", "2026-11-16"))} ({src_links([ro["source"]])} &middot; {src_links([ro.get("title_source", ro["source"])])}). '""",
    ),
    # 3. Content status per product: P4 and P5 have no brief, comparison or buying guide.
    (
        "content_status",
        """    for p in PRODUCTS:
        pid = p["id"]
        rows.append([
            e(p["label"]),
            badge("Published", "ok") + ' <a href="marketing/briefs.html">brief</a>',
            badge("Published", "ok") + ' <a href="marketing/comparison.html">comparison</a>',
            badge("Published", "ok") + ' <a href="marketing/buying-guide.html">buying guide</a>',""",
        """    for p in PRODUCTS:
        pid = p["id"]
        # Session 2f181cd9 (2026-11-17): P4 and P5 were added to the register without any marketing
        # content, so the status is read from the product record instead of being hard-coded as
        # published. Adding a product must not silently claim content that does not exist.
        cs = p.get("content_status") or {
            "brief": "Published", "comparison": "Published", "buying_guide": "Published",
        }
        def _cell(state: str, href: str, label: str) -> str:
            kind = "ok" if state == "Published" else "warn"
            return badge(state, kind) + (f' <a href="{href}">{label}</a>' if state == "Published" else "")
        rows.append([
            e(p["label"]),
            _cell(cs["brief"], "marketing/briefs.html", "brief"),
            _cell(cs["comparison"], "marketing/comparison.html", "comparison"),
            _cell(cs["buying_guide"], "marketing/buying-guide.html", "buying guide"),""",
    ),
    # 4. Hero and lead copy: five links, two categories.
    (
        "hero_link",
        '<a href="marketing/comparison.html">Compare the three listings</a>',
        '<a href="marketing/comparison.html">Compare the air-fryer listings</a>',
    ),
    (
        "research_status",
        """  <p><strong>Research status (re-verified 2026-11-16):</strong> all three supplied Amazon short links resolve to live product listings.""",
        """  <p><strong>Research status (re-verified 2026-11-17):</strong> all five supplied Amazon short links resolve to live product listings. Three open air fryers; the two added on 2026-11-17 open meat thermometers, so the site's air-fryer framing is now narrower than the link set (<a class="flagid" href="flagged.html#F-2F-01">F-2F-01</a>) and the scope is published as an owner decision on <a href="sessions/2f181cd9/decision-lab.html">the Decision Lab</a>.""",
    ),
    (
        "tracks_heading",
        "<h2>The three listings this site tracks</h2>",
        "<h2>The five listings this site tracks</h2>",
    ),
    (
        "breadcrumb_sentence",
        """    <p class="small">Category breadcrumb as served by the three destination listings (captured 2026-11-16 by session f132f462, kept from their trending section): Home &amp; Kitchen &gt; Kitchen &amp; Dining &gt; Small Appliances &gt; Fryers &gt; Air Fryers &middot; node 17659096011 &middot; {src_links(["S14", "S15", "S16"])}</p>""",
        """    <p class="small">Category breadcrumb as served by the three air-fryer destinations (captured 2026-11-16 by session f132f462): Home &amp; Kitchen &gt; Kitchen &amp; Dining &gt; Small Appliances &gt; Fryers &gt; Air Fryers &middot; node 17659096011 &middot; {src_links(["S14", "S15", "S16"])}. The two links added on 2026-11-17 sit in a different branch: Home &amp; Kitchen &gt; Kitchen &amp; Dining &gt; Kitchen Utensils &amp; Gadgets &gt; Thermometers &amp; Timers &gt; Meat &middot; node 289810 &middot; {src_links(["S72", "S73"])} (<a class="flagid" href="flagged.html#F-2F-01">F-2F-01</a>).</p>""",
    ),
    (
        "reverify_intro",
        """<p>Every load-bearing claim on the flat pages was checked again against the official page it cites &mdash; on 2026-11-14 by session b8beb448, and the three submitted links, the three destinations and the policy pages again on 2026-11-16 by session <a href="sessions/5a56c084/index.html">5a56c084</a>.""",
        """<p>Every load-bearing claim on the flat pages was checked again against the official page it cites &mdash; on 2026-11-14 by session b8beb448, and the three submitted links, the three destinations and the policy pages again on 2026-11-16 by session <a href="sessions/5a56c084/index.html">5a56c084</a>, and all five links, both new destinations and the policy pages again on 2026-11-17 by session <a href="sessions/2f181cd9/index.html">2f181cd9</a>.""",
    ),
    (
        "meta_desc",
        "comparisons, buying guides and affiliate-programme research for three Amazon air-fryer listings, with every published claim linked to the official page it came from.",
        "comparisons, buying guides and affiliate-programme research for five Amazon listings (three air fryers and two kitchen thermometers), with every published claim linked to the official page it came from.",
    ),
    (
        "exec_headline",
        """  <p><strong>Headline:</strong> the three submitted short links each open a live Amazon product page.""",
        """  <p><strong>Headline:</strong> all five submitted short links each open a live Amazon product page, three of them air fryers and two of them meat thermometers.""",
    ),
    (
        "exec_finding",
        """    <li><strong>The three short links each open a live Amazon product page.</strong> The destinations were read on 2026-11-13 and 2026-11-14 {src_links(['S11', 'S12', 'S13', 'S14', 'S15', 'S16'])}.""",
        """    <li><strong>All five short links each open a live Amazon product page.</strong> The first three destinations were read on 2026-11-13 and 2026-11-14 {src_links(['S11', 'S12', 'S13', 'S14', 'S15', 'S16'])} and re-read on 2026-11-17 {src_links(['S76', 'S77', 'S78'])}; the two links added on 2026-11-17 were read that day {src_links(['S70', 'S71', 'S72', 'S73'])} and open meat thermometers rather than air fryers {flag_links(['F-2F-01'])}.""",
    ),
    (
        "owner_action_asin",
        """    <li>Give the intended product URL or 10-character ASIN for each of the three products (FLG-001).</li>""",
        """    <li>Give the intended product URL or 10-character ASIN for each of the five products (FLG-001), and confirm whether the two meat-thermometer links were meant to be part of this site at all (F-2F-01). The register to fill in is on <a href="sessions/2f181cd9/intake.html">the five-link intake page</a>.</li>""",
    ),
    (
        "owner_action_category",
        """    <li>Confirm which Amazon product category each of the three listings is in, so the public Table 1 rate can be applied to it (FLG-005, FLG-021). The category rates themselves are already published and verified.</li>""",
        """    <li>Confirm which Amazon product category each of the five listings is in, so the public Table 1 rate can be applied to it (FLG-005, FLG-021, F-2F-04). The category rates themselves are already published and verified; what is missing is the mapping from a listing's browse node to a Table 1 category.</li>""",
    ),
    (
        "products_lead",
        'lead="The three product links from the brief, checked line by line against official Amazon pages. Nothing is shown as a verified product until its identifier resolves."',
        'lead="The five product links from the brief, checked line by line against official Amazon pages: three open air-fryer listings and two open meat-thermometer listings. Nothing is shown as a verified product until its identifier resolves, and the intended product is recorded separately from the observed destination."',
    ),
    (
        "products_howto",
        """    <li>&ldquo;Observed redirect&rdquo; is the page the short link opened on 2026-11-13. It is not treated as the submitted product, because the submitted identifier does not resolve to it.</li>""",
        """    <li>&ldquo;Observed redirect&rdquo; is the page the short link opened when it was fetched. It is not treated as the submitted product, because the submitted identifier does not resolve to it. The intended product is a separate field and stays empty until the owner confirms it: see <a href="sessions/2f181cd9/intake.html">the five-link intake register</a>.</li>""",
    ),
    (
        "competition_callout",
        """'({flag_links(["FLG-025"])}). This is the category of the three <em>observed redirect targets</em>, '""",
        """'({flag_links(["FLG-025"])}). This is the category of the three air-fryer <em>observed redirect targets</em> '""",
    ),
    (
        "briefs_lead",
        'lead="SEO product briefs, a comparison and a buying guide for the three listings the submitted links open. Written from verified listing facts only."',
        'lead="SEO product briefs, a comparison and a buying guide for the three air-fryer listings the submitted links open. The two links added on 2026-11-17 open meat thermometers and are not covered here; they are recorded on the five-link intake register instead. Written from verified listing facts only."',
    ),
    (
        "verification_coverage",
        """        "<li>All three submitted links were re-fetched, and all three direct <code>/dp/&lt;id&gt;</code> checks were re-run. The results are unchanged from 2026-11-13.</li>\"""",
        """        "<li>All five submitted links were re-fetched, and all five direct <code>/dp/&lt;id&gt;</code> checks were re-run: the first three on 2026-11-14 and 2026-11-16, all five on 2026-11-17. The results are unchanged from 2026-11-13.</li>\"""",
    ),
    # 5. Navigation and site map: this session's pages.
]

for name, old, new in EDITS:
    if old not in t:
        raise SystemExit(f"EDIT FAILED (not found): {name}\n---\n{old[:200]}")
    if t.count(old) != 1:
        raise SystemExit(f"EDIT FAILED ({t.count(old)} matches): {name}")
    t = t.replace(old, new)
    print(f"applied: {name}")

P.write_text(t, encoding="utf-8")
print("build_site.py patched")

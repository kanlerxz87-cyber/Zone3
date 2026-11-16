#!/usr/bin/env python3
"""Session 1dddf8c0 — 1dd-T3 remediation.

Removes Amazon-restricted product values (observed prices, list prices, unit
prices, star ratings, review counts, demand signals, promotion badges and
values derived from them) from every public page and record in this repository,
per Amazon Associates Program Policies Participation Requirements 2(b) and 6(t).

Official basis:
  https://affiliate-program.amazon.com/help/operating/policies
    2(b) — prices/availability only if Amazon serves the link or via Creators/PA API
    6(t) — customer reviews / star ratings only via Creators/PA API

Method: values are replaced with an explicit "Withheld" marker; row labels,
source links and flag references are preserved so every row keeps its official
source link. The archive generator (sessions/3c886b62/tools/build.py) is patched
so regeneration cannot restore the values, and the underlying session JSON is
withheld at the data layer.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

WITHHELD = "Withheld"
NOTE = ("Withheld from public display per Amazon Associates Program Policies "
        "Participation Requirements 2(b)/6(t) (session 1dddf8c0 remediation, 2026-11-16).")

# ---------------------------------------------------------------------------
# Part A — withhold restricted fields in the session archive data layer
# ---------------------------------------------------------------------------
RESTRICTED_FIELDS = {
    "current_price", "list_price", "unit_price", "deal_badge",
    "other_offers_low", "rating", "ratings_count_display", "demand_signal",
}

def withhold_json():
    p = ROOT / "sessions/3c886b62/data/products.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    changed = 0
    for prod in d.get("products", []):
        for name, fld in prod.get("fields", {}).items():
            if name in RESTRICTED_FIELDS:
                old = fld.get("value")
                if old not in (None, WITHHELD):
                    fld["value"] = WITHHELD
                    fld["status"] = "withheld"
                    fld["note"] = NOTE
                    changed += 1
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[A] products.json: {changed} restricted field values withheld")

# ---------------------------------------------------------------------------
# Part B — patch the archive generator so it can never render the values again
# ---------------------------------------------------------------------------
def patch_build_py():
    p = ROOT / "sessions/3c886b62/tools/build.py"
    s = p.read_text(encoding="utf-8")
    orig = s

    # 1. money() renders the withheld marker
    s = s.replace(
        'def money(v):\n    return "&mdash;" if v is None else "$%0.2f" % v',
        'WITHHELD_BADGE = \'<span class="badge unv" title="Withheld per Amazon Program Policies 2(b)/6(t)">Withheld</span>\'\n\n\n'
        'def money(v):\n    if v == "Withheld":\n        return WITHHELD_BADGE\n    return "&mdash;" if v is None else "$%0.2f" % v',
    )

    # 2. discount_depth() guards against non-numeric (withheld) values
    s = s.replace(
        '    if cur is None or lst is None or not lst:\n        return None',
        '    if not isinstance(cur, (int, float)) or not isinstance(lst, (int, float)) or not lst:\n        return None',
    )

    # 3. product_row numeric cells tolerate the withheld marker
    s = s.replace(
        '\'<td class="num" data-v="%s">%s</td>\' % ("" if cur is None else cur, money(cur)),',
        '\'<td class="num" data-v="%s">%s</td>\' % ("" if cur in (None, "Withheld") else cur, money(cur)),',
    )
    s = s.replace(
        '\'<td class="num" data-v="%s">%s</td>\' % ("" if lst is None else lst, money(lst)),',
        '\'<td class="num" data-v="%s">%s</td>\' % ("" if lst in (None, "Withheld") else lst, money(lst)),',
    )

    # 4. rating cell in product_row
    s = s.replace(
        '"&mdash;" if fv(p, "rating")["value"] is None else "%0.1f / 5" % fv(p, "rating")["value"]),',
        'WITHHELD_BADGE if fv(p, "rating")["value"] == "Withheld" else (\'&mdash;\' if fv(p, "rating")["value"] is None else "%0.1f / 5" % fv(p, "rating")["value"])),',
    )

    # 5. page_category price range ignores withheld values
    s = s.replace(
        'prices = [fv(p, "current_price")["value"] for p in items if fv(p, "current_price")["value"]]',
        'prices = [fv(p, "current_price")["value"] for p in items\n                if isinstance(fv(p, "current_price")["value"], (int, float))]',
    )

    # 6. page_comparison metric lambdas
    s = s.replace(
        '("Star rating", lambda p: "%0.1f / 5" % fv(p, "rating")["value"],',
        '("Star rating", lambda p: WITHHELD_BADGE if fv(p, "rating")["value"] == "Withheld" else "%0.1f / 5" % fv(p, "rating")["value"],',
    )
    s = s.replace(
        '("Discount depth (derived)", lambda p: "%0.1f%%" % discount_depth(p) if discount_depth(p) is not None else "&mdash;",',
        '("Discount depth (derived)", lambda p: WITHHELD_BADGE if discount_depth(p) is None else "%0.1f%%" % discount_depth(p),',
    )

    # 7. page_analysis rating cell
    s = s.replace(
        '\'<td class="num">%s</td>\' % ("%0.1f / 5" % fv(p, "rating")["value"])',
        '\'<td class="num">%s</td>\' % (WITHHELD_BADGE if fv(p, "rating")["value"] == "Withheld" else "%0.1f / 5" % fv(p, "rating")["value"])',
    )

    if s == orig:
        raise SystemExit("build.py patch failed: no replacement applied")
    p.write_text(s, encoding="utf-8")
    print("[B] build.py patched (withheld-safe renderers)")

# ---------------------------------------------------------------------------
# Part C — redact markdown records
# ---------------------------------------------------------------------------
GLOBAL_REPLACEMENTS = [
    # observed prices and derived estimates
    "$79.93", "$79.91", "$149.99", "$99.99", "$209.99", "$119.99",
    "$57.45", "$92.99", "$49.54", "$39.97", "$89.99", "$99.95", "$129.95",
    "$57.91", "$39.99", "$199.95", "$69.97", "$130", "$97.49", "$51.94",
    "$2.40", "$3.60", "$6.75", "$4.50",
    # ratings
    "4.2★", "4.3★", "4.4★", "4.2 / 5", "4.3 / 5", "4.4 / 5",
    "4.2 out of 5", "4.3 out of 5", "4.4 out of 5",
    # review counts
    "4.8K", "18.3K", "16.8K", "39.9K",
    "10,984", "22,768", "4,015", "7,552", "52,301",
    "4,859", "18,320", "16,863", "392",
    # demand signals
    "1K+", "3K+", "4K+", "8K+",
    # promotion badges
    "Limited time deal", "Early Black Friday Deal",
    # derived discount depths
    "33.4%", "28.6%", "20.1%",
]

MD_FILES = [
    "docs/executive-summary-c4e71983.md",
    "docs/executive-summary.md",
    "docs/repo-review-9fef7647.md",
    "research/21acd3c0-repo-review.md",
    "research/21acd3c0-verification-log.md",
    "research/252122ff-verification-log.md",
    "research/3d359c23-verification-log.md",
    "research/54ce6a2b-repo-review.md",
    "research/54ce6a2b-verification-log.md",
    "research/c4e71983-commercial-snapshot.md",
    "research/c4e71983-niche-competition.md",
    "research/c4e71983-verification-log.md",
    "research/a86f1d09-verification-log.md",
    "sessions/03bbd050/findings.md",
    "sessions/03bbd050/verification.md",
    "sessions/3c886b62/EXECUTIVE_SUMMARY.md",
    "sessions/3c886b62/docs/FLAGGED.md",
    "sessions/3c886b62/docs/REQUIREMENTS.md",
    "sessions/3c886b62/docs/RESEARCH.md",
    "sessions/3c886b62/docs/VERIFICATION.md",
    "sessions/3c886b62/docs/content/analysis-competition.md",
    "sessions/3c886b62/docs/content/analysis-reviews.md",
    "sessions/3c886b62/docs/content/buying-guide-air-fryers.md",
    "sessions/3c886b62/docs/content/commission-modelled.md",
    "sessions/3c886b62/docs/content/comparison-read.md",
    "sessions/3c886b62/docs/content/dashboard-findings.md",
    "sessions/3c886b62/docs/content/dashboard-unverified.md",
    "sessions/3c886b62/docs/content/executive-summary.md",
    "sessions/f2102efa/repo-review.md",
]

# Sentence-level rewrites (applied before the global value replacement so the
# rewritten text does not contain restricted values). Keyed by file.
SENTENCE_REWRITES = {
    "docs/executive-summary-c4e71983.md": [
        ("The band above $130 is the thinnest part of the captured top six — and it is where the $149.99 unit sits.",
         "The upper price band is the thinnest part of the captured top six, and the premium unit sits in it."),
        ("economics are thin per unit — $3.60 to $6.75 at the published Kitchen rate — so this only works with\nvolume, with Prime bounties, or by steering traffic toward the $149.99 unit.",
         "economics are thin per unit at the published Kitchen rate, so this only works with\nvolume, with Prime bounties, or by steering traffic toward the premium unit."),
    ],
    "docs/executive-summary.md": [
        ("| $79.93 (list $99.99), 4.2★, ~4.8K reviews", "| price, list price, rating and review count withheld (2(b)/6(t))"),
        ("| $149.99 (list $209.99), 4.3★, ~18.3K reviews", "| price, list price, rating and review count withheld (2(b)/6(t))"),
        ("| $79.91 (list $119.99), 4.4★, ~16.8K reviews", "| price, list price, rating and review count withheld (2(b)/6(t))"),
    ],
    "research/21acd3c0-verification-log.md": [
        ("`grep` for `79.93`, `99.99`, `4.2 out`, `4.8K` in `marketing/*.html`",
         "`grep` for price, rating and review-count literals in `marketing/*.html`"),
        ("`dp/B0CDY277D3` at **$69.97**, while the register's snapshot for P1 records **$79.93** (deal) /\n  list $99.99 earlier on 2026-11-14.",
         "`dp/B0CDY277D3` at one price, while the register's snapshot for P1 records another (deal /\n  list price) earlier on 2026-11-14."),
        ("  $199.95, Cosori B0C33CHG99 $99.99). They were ignored, exactly as H-F-01 records.",
         "  competitor list prices). They were ignored, exactly as H-F-01 records."),
    ],
    "research/21acd3c0-repo-review.md": [
        ("Live page widgets showed a price ($69.97) for `dp/B0CDY277D3` that differs from the register's same-day snapshot ($79.93).",
         "Live page widgets showed a price for `dp/B0CDY277D3` that differs from the register's same-day snapshot."),
    ],
    "research/3d359c23-verification-log.md": [
        ("**4.4-star / 392-review / $69.97** entry whose own link points at `dp/B0B7C327LK`",
         "**rating / review-count / price** entry whose own link points at `dp/B0B7C327LK`"),
    ],
    "research/54ce6a2b-repo-review.md": [
        ('"Fetched 2026-11-14. Result 1 for B0CDY277D3 as displayed: 4.2 out of 5 stars, (4.8K)\n> reviews, 1K+ bought in past month, price USD 79.93 (deal; List: USD 99.99) …"',
         '"Fetched 2026-11-14. Result 1 for B0CDY277D3 as displayed: rating, review count, demand signal and price all withheld (2(b)/6(t)) …"'),
    ],
    "research/c4e71983-commercial-snapshot.md": [
        ("products rate 4.2, 4.3 and 4.4. Yet the $149.99 unit — the most expensive thing in the comparison —",
         "products rate within a narrow band. Yet the premium unit — the most expensive thing in the comparison —"),
        ("shows the strongest velocity signal of the three (4K+ bought in past month).",
         "shows the strongest velocity signal of the three."),
        ("The category leader on volume (rank 6, 52,301 ratings) is a",
         "The category leader on volume is a"),
        ("126 ratings. The promoted $149.99 unit has 18.3K ratings shown.",
         "a thin sample. The promoted premium unit has a large rating count shown."),
        ("**Two products are priced identically.** At $79.91 and $79.93 they are two cents apart despite list",
         "**Two products are priced almost identically.** Despite list"),
        ("prices $20 apart. On the captured data the 8 Qt unit (4.4 stars, 16.8K ratings) is the stronger of",
         "prices apart. On the captured data the 8 Qt unit is the stronger of"),
        ("about $3.60 for either Chefman and about $6.75 for the Emeril Lagasse unit.",
         "a thin per-unit commission for either Chefman and a higher figure for the Emeril Lagasse unit."),
        ("All three products were discounted at capture, two with a *Limited time deal* badge and one with an\n*Early Black Friday Deal* badge.",
         "All three products were discounted at capture and all three carried promotion badges at capture time."),
    ],
    "research/c4e71983-niche-competition.md": [
        ("The volume leader (52,301 ratings) and two of the top six are **Chefman**",
         "The volume leader and two of the top six are **Chefman**"),
        ("thinnest part of the captured set — and the $149.99 promoted unit sits in it.",
         "thinnest part of the captured set — and the promoted premium unit sits in it."),
        ("deal* badge and one an *Early Black Friday Deal* badge.",
         "promotion badges at capture time."),
    ],
    "sessions/03bbd050/findings.md": [
        ("with observed values ($79.93 / $149.99 / $79.91 — all three re-confirmed by me today, see `verification.md` §A);",
         "with observed values (all three re-confirmed by me today, see `verification.md` §A);"),
        ("`category/air-fryers.html` renders `USD 79.93 (observed 2026-11-14; list USD 99.99)`-style co",
         "`category/air-fryers.html` renders an observed-price-style co"),
        ('describes the sub-site\'s figures as "displays prices ($79.93, $149.99, $79.91)".',
         'describes the sub-site\'s figures as "displays prices".'),
        ("status notes quote `USD 79.93 (deal; List: USD 99.99)` and friends.",
         "status notes quote observed price values."),
    ],
    "sessions/3c886b62/docs/FLAGGED.md": [
        ("Amazon displays '4.8K', '18.3K' and '16.8K' rather than exact counts. These are Amazon's own rounded figures, recorded verbatim, not exact integers.",
         "Amazon displays rounded counts rather than exact integers. The observed rounded figures are withheld per 6(t)."),
    ],
    "sessions/3c886b62/EXECUTIVE_SUMMARY.md": [
        ("large review bases. The Emeril Lagasse unit is the standout on volume: 18.3K ratings and 4K+ units bought\nin the past month, against 4.8K ratings and 1K+ for the CHEFMAN dual basket and 16.8K ratings and 3K+ for\nthe Chefman 8 quart. It also carries the highest price at $149.99 against $79.93 and $79.91 for the other",
         "large review bases. The Emeril Lagasse unit is the standout on volume: the largest rating count and\ndemand signal of the three, against smaller figures for the CHEFMAN dual basket and the Chefman 8 quart.\nIt also carries the highest price of the three"),
        ("Second, **section 6(t)** says the same for customer reviews and star ratings. The 4.2, 4.3 and 4.4 star",
         "Second, **section 6(t)** says the same for customer reviews and star ratings. The observed star"),
    ],
    "sessions/3c886b62/docs/VERIFICATION.md": [
        ("Shown as $79.93 on Amazon's search-results rendering of this ASIN.",
         "Observed on Amazon's search-results rendering of this ASIN (value withheld, 2(b))."),
        ("Shown as 'List: $99.99'.", "Observed on the same rendering (value withheld, 2(b))."),
        ("Shown as '($39.97/count)'.", "Observed on the same rendering (value withheld, 2(b))."),
        ("Shown as 'List: $209.99'.", "Observed on the same rendering (value withheld, 2(b))."),
        ("Shown as 'List: $119.99'.", "Observed on the same rendering (value withheld, 2(b))."),
        ("Amazon's rounded display value, not an exact count.",
         "Amazon's rounded display value (value withheld, 6(t)), not an exact count."),
    ],
    "sessions/3c886b62/docs/content/analysis-reviews.md": [
        ("- CHEFMAN 6 quart dual basket: 4.2 out of 5 on 4.8K ratings.",
         "- CHEFMAN 6 quart dual basket: rating and rating count withheld (6(t))."),
        ("- Emeril Lagasse 26QT: 4.3 out of 5 on 18.3K ratings.",
         "- Emeril Lagasse 26QT: rating and rating count withheld (6(t))."),
        ("- Chefman 8 quart TurboFry: 4.4 out of 5 on 16.8K ratings.",
         "- Chefman 8 quart TurboFry: rating and rating count withheld (6(t))."),
        ("perception. What does differ is the size of the evidence base. 18.3K and 16.8K ratings are large enough\nthat the average is stable; 4.8K is a materially thinner sample.",
         "perception. What does differ is the size of the evidence base. The two larger rating counts are large enough\nthat the average is stable; the smallest is a materially thinner sample."),
    ],
    "sessions/3c886b62/docs/content/buying-guide-air-fryers.md": [
        ("At capture the two Chefman units were both just under $80, at $79.93 and $79.91, while the Emeril Lagasse\nwas $149.99 against a $209.99 list price. All three were discounted, and all three had cheaper used or\nnew offers available: $57.45, $49.54 and $92.99 respectively. Prices move, and the values here are a",
         "At capture the two Chefman units were priced in the same low tier, while the Emeril Lagasse unit\nwas in a distinctly higher tier against a higher list price. All three were discounted, and all three had\ncheaper used or new offers available. Prices move, and the values here are a"),
        ("The three sit within 0.2 stars of each other: 4.2 out of 5 on 4.8K ratings for the CHEFMAN dual basket,\n4.3 out of 5 on 18.3K ratings for the Emeril Lagasse, and 4.4 out of 5 on 16.8K ratings for the Chefman",
         "The three sit within a narrow band of each other: rating and rating count withheld (6(t)) for the\nCHEFMAN dual basket, the Emeril Lagasse, and the Chefman"),
        ("A 4.4 on 16.8K ratings is a different evidence base from a 4.2 on 4.8K ratings. The larger sample is",
         "The rating counts differ enough that the evidence bases are not the same. The larger sample is"),
    ],
    "sessions/3c886b62/docs/content/comparison-read.md": [
        ("**Price splits into two tiers.** The two Chefman units are within two cents of each other at $79.93 and\n$79.91, while the Emeril Lagasse sits at $149.99, close to double. That is the single clearest",
         "**Price splits into two tiers.** The two Chefman units are priced in the same low tier, while the\nEmeril Lagasse sits in a distinctly higher tier, close to double. That is the single clearest"),
        ("**Discount depth runs the other way.** The Chefman 8 quart has the deepest discount at 33.4% off its\n$119.99 list, the Emeril Lagasse is next at 28.6% off $209.99, and the CHEFMAN dual basket is shallowest\nat 20.1% off $99.99. A deeper discount is not automatically a better deal; it often means the list price",
         "**Discount depth runs the other way.** The Chefman 8 quart has the deepest discount of the three, the\nEmeril Lagasse is next, and the CHEFMAN dual basket is shallowest. A deeper discount is not automatically\na better deal; it often means the list price"),
        ("**Volume is the real separator.** 18.3K and 3K+ monthly purchases for the Emeril Lagasse, 16.8K and 3K+\nfor the Chefman 8 quart, 4.8K and 1K+ for the CHEFMAN dual basket. Two products are moving at roughly",
         "**Volume is the real separator.** The Emeril Lagasse leads on rating count and monthly purchases, the\nChefman 8 quart is next, and the CHEFMAN dual basket trails on both. Two products are moving at roughly"),
    ],
    "sessions/3c886b62/docs/content/dashboard-findings.md": [
        ("**The Emeril Lagasse unit leads on every demand signal.** It has 18.3K ratings and 4K+ units bought in\nthe past month, against 16.8K and 3K+ for the Chefman 8 quart and 4.8K and 1K+ for the CHEFMAN dual\nbasket. It is also the most expensive at $149.99, so it is the highest-value click if the commission",
         "**The Emeril Lagasse unit leads on every demand signal.** It has the largest rating count and demand\nsignal of the three, with the Chefman 8 quart next and the CHEFMAN dual basket last. It is also the most\nexpensive of the three, so it is the highest-value click if the commission"),
        ("the Emeril unit's volume, and it has the smallest review base at 4.8K ratings. It also has the lowest",
         "the Emeril unit's volume, and it has the smallest review base of the three. It also has the lowest"),
        ("**Every product was discounted at capture.** Discount depth ranges from 20.1% off list for the CHEFMAN\ndual basket to 33.4% for the Chefman 8 quart, with the Emeril unit at 28.6%. Two carry a *Limited time\ndeal* badge and one an *Early Black Friday Deal* badge, so all three promotion references have an expiry",
         "**Every product was discounted at capture.** Discount depth varies across the three, and all three\ncarried promotion badges at capture, so every promotion reference has an expiry"),
        ("price on all three: $57.45 against $79.93, $92.99 against $149.99, and $49.54 against $79.91. A reviewer",
         "price on all three: a cheaper used or new offer below the Amazon price on every listing. A reviewer"),
    ],
    "sessions/3c886b62/docs/content/executive-summary.md": [
        ("large review bases. The Emeril Lagasse unit is the standout on volume: 18.3K ratings and 4K+ units bought\nin the past month, against 4.8K ratings and 1K+ for the CHEFMAN dual basket and 16.8K ratings and 3K+ for\nthe Chefman 8 quart. It also carries the highest price at $149.99 against $79.93 and $79.91 for the other",
         "large review bases. The Emeril Lagasse unit is the standout on volume: the largest rating count and\ndemand signal of the three, against smaller figures for the CHEFMAN dual basket and the Chefman 8 quart.\nIt also carries the highest price of the three"),
    ],
    "sessions/3c886b62/docs/content/commission-modelled.md": [
        ("On these numbers the Emeril Lagasse unit is worth roughly 1.9 times a Chefman conversion at either rate,\nbecause the commission is a percentage of a price that is nearly double.",
         "On these numbers the Emeril Lagasse unit is worth roughly twice a Chefman conversion at either rate,\nbecause the commission is a percentage of a price that is nearly double."),
    ],
}

def redact_markdown():
    total = 0
    for rel in MD_FILES:
        p = ROOT / rel
        if not p.exists():
            print(f"  [skip] missing {rel}")
            continue
        s = p.read_text(encoding="utf-8")
        orig = s
        for old, new in SENTENCE_REWRITES.get(rel, []):
            if old in s:
                s = s.replace(old, new)
            else:
                print(f"  [warn] sentence rewrite not found in {rel}: {old[:60]}...")
        for v in GLOBAL_REPLACEMENTS:
            s = s.replace(v, WITHHELD)
        if s != orig:
            p.write_text(s, encoding="utf-8")
            total += 1
            print(f"[C] redacted {rel}")
    print(f"[C] {total} markdown files redacted")

# ---------------------------------------------------------------------------
# Part D — direct edits to hand-written root HTML pages
# ---------------------------------------------------------------------------
HTML_REWRITES = {
    "docs/analysis.html": [
        ("<td class=\"num\">−$20.06</td>", "<td class=\"num\"><span class=\"badge unv\">Withheld</span></td>"),
        ("<td class=\"num\">−$60.00</td>", "<td class=\"num\"><span class=\"badge unv\">Withheld</span></td>"),
        ("<td class=\"num\">−$40.08</td>", "<td class=\"num\"><span class=\"badge unv\">Withheld</span></td>"),
        ("The portfolio naturally segments into budget ($79.91–$79.93), mid ($149.99), with used/new alternatives at $49.54–$92.99. That supports",
         "The portfolio naturally segments into a budget tier and a mid tier, with used/new alternatives below the Amazon price (values withheld per Amazon Policies 2(b)/6(t)). That supports"),
        ("All three clear the 4.2★ threshold with four- to five-figure review counts, and Amazon itself displayed \"1K+/3K+/4K+ bought in past month\".",
         "All three clear a high rating threshold with large review counts, and Amazon itself displayed demand badges at capture (values withheld per Amazon Policies 2(b)/6(t))."),
        ("<li><strong>Velocity concentration:</strong> Amazon displayed 8K+ units/month combined (\"bought in past month\" badges) — the Emeril unit alone showed 4K+ (source: same search pages).</li>",
         "<li><strong>Velocity concentration:</strong> Amazon displayed combined demand badges at capture — the Emeril unit led the set (source: same search pages; values withheld per 2(b)/6(t)).</li>"),
        ("<li><strong>Price-point spread:</strong> $79.91–$149.99 observed covers \"under $100\" and \"splurge\" intents — supports two distinct SEO landing angles from one niche.</li>",
         "<li><strong>Price-point spread:</strong> the observed range covers \"under $100\" and \"splurge\" intents — supports two distinct SEO landing angles from one niche (values withheld per 2(b)).</li>"),
    ],
    "docs/content.html": [
        ("<li><strong>Observed rating:</strong> 4.2★ with 4.8K reviews (Amazon, 2026-11-13).</li>",
         "<li><strong>Observed rating:</strong> withheld per Amazon Policies 6(t) (observed at capture 2026-11-13; source linked).</li>"),
        ("<li><strong>Observed price:</strong> $79.93 (list $99.99, \"Limited time deal\" at capture).</li>",
         "<li><strong>Observed price:</strong> withheld per Amazon Policies 2(b) (observed at capture 2026-11-13; source linked).</li>"),
        ("<li><strong>Observed rating:</strong> 4.3★ with 18.3K reviews (Amazon, 2026-11-13) — the largest review base in this set.</li>",
         "<li><strong>Observed rating:</strong> withheld per Amazon Policies 6(t) (observed at capture 2026-11-13; source linked) — the largest review base in this set at capture.</li>"),
        ("<li><strong>Observed price:</strong> $149.99 (list $209.99, \"Early Black Friday Deal\" at capture).</li>",
         "<li><strong>Observed price:</strong> withheld per Amazon Policies 2(b) (observed at capture 2026-11-13; source linked).</li>"),
        ("<li><strong>Observed rating:</strong> 4.4★ with 16.8K reviews (Amazon, 2026-11-13) — highest rating of the three.</li>",
         "<li><strong>Observed rating:</strong> withheld per Amazon Policies 6(t) (observed at capture 2026-11-13; source linked) — highest rating of the three at capture.</li>"),
        ("<li><strong>Observed price:</strong> $79.91 (list $119.99, \"Limited time deal\" at capture).</li>",
         "<li><strong>Observed price:</strong> withheld per Amazon Policies 2(b) (observed at capture 2026-11-13; source linked).</li>"),
        ("<tr><td class=\"num\">Rating</td><td class=\"num\">4.2★</td><td class=\"num\">4.3★</td><td class=\"num\">4.4★</td>",
         "<tr><td class=\"num\">Rating</td><td class=\"num\"><span class=\"badge unv\">Withheld</span></td><td class=\"num\"><span class=\"badge unv\">Withheld</span></td><td class=\"num\"><span class=\"badge unv\">Withheld</span></td>"),
        ("<li><strong>Best rating-per-dollar simplicity:</strong> Chefman TurboFry 8 Qt — highest rating (4.4★), 8 qt single basket, deepest observed discount (−33.4%).</li>",
         "<li><strong>Best rating-per-dollar simplicity:</strong> Chefman TurboFry 8 Qt — highest rating of the three, 8 qt single basket, deepest observed discount of the set (values withheld per 2(b)/6(t)).</li>"),
    ],
    "docs/executive-summary.html": [
        ("<li><strong>High-trust inventory.</strong> Ratings 4.2–4.4★ across 39.9K combined reviews; Amazon displayed 8K+ units bought in the past month across the three.</li>",
         "<li><strong>High-trust inventory.</strong> Observed ratings clustered in a narrow high band across a large combined review base; Amazon displayed demand badges across the three (values withheld per Amazon Policies 2(b)/6(t)).</li>"),
        ("<li><strong>Ready-made price ladder.</strong> $79.91 / $79.93 budget twins vs a $149.99 premium unit (20–33% off list at capture) enables honest \"under $100 vs premium\" comparison content.</li>",
         "<li><strong>Ready-made price ladder.</strong> Two units in the same low tier vs a distinctly higher-priced premium unit at capture enables honest \"under $100 vs premium\" comparison content (values withheld per Amazon Policies 2(b)).</li>"),
    ],
    "docs/index.html": [
        ("<div class=\"card\"><div class=\"k\">Price range (observed)</div><div class=\"v\">$79.91–$149.99</div><div class=\"sub\">List prices $99.99–$209.99</div></div>",
         "<div class=\"card\"><div class=\"k\">Price range (observed)</div><div class=\"v\">Withheld (2(b))</div><div class=\"sub\">List prices withheld (2(b))</div></div>"),
        ("<td class=\"num\">4.2★</td>", "<td class=\"num\"><span class=\"badge unv\">Withheld</span></td>"),
        ("<td class=\"num\">4.3★</td>", "<td class=\"num\"><span class=\"badge unv\">Withheld</span></td>"),
        ("<td class=\"num\">4.4★</td>", "<td class=\"num\"><span class=\"badge unv\">Withheld</span></td>"),
        ("<li><strong>Strong social proof:</strong> 4.2–4.4★ with 4.8K–18.3K reviews; combined 8K+ units bought in the past month.</li>",
         "<li><strong>Strong social proof:</strong> observed ratings in a narrow high band with large review counts; combined demand badges at capture (values withheld per Amazon Policies 2(b)/6(t)).</li>"),
    ],
    "docs/sources.html": [
        ("<td>Price $79.93 · list $99.99 · 4.2★ · 4.8K reviews · 1K+ bought/month · deal badge · other offer $57.45</td>",
         "<td>Price withheld (2(b)) · list withheld · rating withheld (6(t)) · review count withheld (6(t)) · demand badge observed · deal badge withheld · other offer withheld (2(b))</td>"),
        ("<td>Price $149.99 · list $209.99 · 4.3★ · 18.3K reviews · 4K+ bought/month · deal badge · other offer $92.99</td>",
         "<td>Price withheld (2(b)) · list withheld · rating withheld (6(t)) · review count withheld (6(t)) · demand badge observed · deal badge withheld · other offer withheld (2(b))</td>"),
        ("<td>Price $79.91 · list $119.99 · 4.4★ · 16.8K reviews · 3K+ bought/month · deal badge · other offer $49.54</td>",
         "<td>Price withheld (2(b)) · list withheld · rating withheld (6(t)) · review count withheld (6(t)) · demand badge observed · deal badge withheld · other offer withheld (2(b))</td>"),
    ],
    "sessions/03bbd050/index.html": [
        ("<td>$79.93 · In Stock · “$39.97 per count”</td>",
         "<td>Price and availability withheld (2(b)); observed at capture</td>"),
        ("<td>$149.99 · In Stock · free delivery Thu 19 Nov</td>",
         "<td>Price and availability withheld (2(b)); observed at capture</td>"),
        ("<td>$79.91 · In Stock</td>",
         "<td>Price and availability withheld (2(b)); observed at capture</td>"),
    ],
}

def redact_html():
    for rel, pairs in HTML_REWRITES.items():
        p = ROOT / rel
        s = p.read_text(encoding="utf-8")
        orig = s
        for old, new in pairs:
            if old in s:
                s = s.replace(old, new)
            else:
                print(f"  [warn] HTML rewrite not found in {rel}: {old[:60]}...")
        if s != orig:
            p.write_text(s, encoding="utf-8")
            print(f"[D] redacted {rel}")

if __name__ == "__main__":
    withhold_json()
    patch_build_py()
    redact_markdown()
    redact_html()
    print("done")

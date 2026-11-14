#!/usr/bin/env python3
"""Build the session 25513d33 verification record page.

    python3 sessions/25513d33/build_record.py

Source URLs are read from data/sources.json at build time, so a source label
rendered on this page can never drift from the URL it points at. Every row on
this page was produced by a live fetch performed on 2026-11-14 by this session
alone; nothing here is copied from another session's record.

Scope discipline (see COORDINATION.md, Part "session 25513d33"): this generator
writes only sessions/25513d33/index.html. It does not touch data/*.json,
scripts/build_site.py or any other shared output.
"""
from __future__ import annotations

import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
OUT = ROOT / "sessions" / "25513d33" / "index.html"

SOURCES = {s["id"]: s for s in json.loads(
    (ROOT / "data" / "sources.json").read_text(encoding="utf-8"))["sources"]}


def src(*ids: str) -> str:
    """Render source IDs as links, with the register title as the visible label."""
    parts = []
    for i in ids:
        s = SOURCES.get(i)
        if s is None:
            raise SystemExit(f"unknown source id {i!r} — add it to data/sources.json first")
        parts.append(
            f'<a href="{html.escape(s["url"])}" target="_blank" rel="noopener noreferrer" '
            f'title="{html.escape(s["title"])}">{i}</a>'
        )
    return " &middot; ".join(parts)


BADGE_OK = '<span class="badge ok">Confirmed verbatim</span>'
BADGE_OK_P = '<span class="badge ok">Confirmed</span>'
BADGE_NEW = '<span class="badge warn">New observation</span>'

# (claim, result badge, what was observed, source ids)
POLICY_ROWS = [
    ("Program Policies page is the current version",
     BADGE_OK_P,
     'Header reads &ldquo;Updated: April 14, 2026&rdquo;.',
     ("S02",)),
    ("Prices and availability may be shown only if Amazon serves the link, or the data comes via "
     "Creators API / PA API &mdash; Participation Requirements 2(b)",
     BADGE_OK,
     "&ldquo;your Site may only show prices and availability if: (a) we serve the link in which that "
     "price and availability data are displayed, or (b) you obtain Product pricing and availability "
     "data via Creators API or PA API and you comply with the requirements regarding use of Creators "
     "API or PA API in the License.&rdquo;",
     ("S02",)),
    ("Star ratings and customer reviews may be shown only via Creators API / PA API &mdash; 6(t)",
     BADGE_OK,
     "&ldquo;You will not display or otherwise use any of our customer reviews or star ratings, in part "
     "or in whole, on your Site unless you have obtained a link to that customer review or star rating "
     "through Creators API or PA API and you comply with the requirements for Creators API and PA API "
     "described in the License.&rdquo;",
     ("S02",)),
    ("Link shorteners must not obscure the Amazon destination &mdash; 6(w)",
     BADGE_OK,
     "&ldquo;You will not use a link shortening service, button, hyperlink or other ad placement in a "
     "manner that makes it unclear that you are linking to an Amazon Site.&rdquo;",
     ("S02",)),
    ("No artificially generated clicks or Sessions &mdash; 6(s)",
     BADGE_OK,
     "&ldquo;You will not artificially generate clicks or impressions on your Site or create Sessions "
     "on an Amazon Site, whether by way of a robot or software program or otherwise.&rdquo;",
     ("S02",)),
    ("No price tracking or price-alerting functionality &mdash; 6(y)",
     BADGE_OK,
     "&ldquo;Unless otherwise agreed by Amazon, your Site must not have price tracking and/or price "
     "alerting functionality.&rdquo;",
     ("S02",)),
    ("Every Special Link must carry the Associates tag &mdash; 2(b)",
     BADGE_OK,
     "&ldquo;you must include your Associates ID or &lsquo;tag&rsquo; (appearing as XXXXX-##, or such "
     "other format as we may designate) as a parameter in the URL of each link you place on your Site "
     "to an Amazon Site.&rdquo;",
     ("S02",)),
    ("Commission session, cart and ship windows &mdash; Commission Income Statement 1(b)",
     BADGE_OK,
     "&ldquo;(x) 24 hours elapse from that click &hellip; (i) &hellip; completing the order for that "
     "Product no later than 89 days after their initial click-through &hellip; (iii) within 180 days of "
     "the purchase, the Product is shipped to, streamed or downloaded by, and paid for by the "
     "customer&rdquo;",
     ("S02",)),
    ("Payment timing &mdash; Commission Income Statement 6",
     BADGE_OK,
     "&ldquo;We will pay Standard Commission Income and Special Commission Income in the default "
     "currency for an Amazon Site approximately 60 days following the end of each calendar month in "
     "which they were earned&rdquo;",
     ("S02",)),
    ("Payment Minimum Chart (US): deposit 10 USD; gift card 10 USD minimum / 2,000 USD maximum; "
     "cheque 100 USD; cheque processing fee 15 USD",
     '<span class="badge ok">Confirmed row for row</span>',
     "Table rows as served: Option 1 (Deposit) 10 USD &middot; Option 2 (Gift Card) 10 USD / 2000 USD "
     "&middot; Option 3 (Check) 100 USD &middot; Check Processing Fee 15 USD.",
     ("S02",)),
    ("Standard Commission Income Statement Table 1 &mdash; &ldquo;Physical Books, Kitchen, "
     "Automotive&rdquo; = 4.50%",
     BADGE_OK,
     "Row reads exactly &ldquo;Physical Books, Kitchen, Automotive | 4.50%&rdquo;.",
     ("S25",)),
    ("Standard Commission Income Statement Table 1 &mdash; &ldquo;All Other Categories&rdquo; = 4.00%",
     BADGE_OK,
     "Row reads exactly &ldquo;All Other Categories | 4.00%&rdquo;.",
     ("S25",)),
    ("Onsite Commission Income Statement Table A &mdash; Kitchen sits in the 1.25% band, and it "
     "applies to Onsite Content only",
     BADGE_OK,
     "Row reads &ldquo;Digital Music, Physical Music, Handmade, Digital Videos, Health &amp; Personal "
     "Care, Sports, Kitchen, Automotive | 1.25%&rdquo;, and the page defines Onsite Content as "
     "&ldquo;Publisher Content or Influencer Content, as applicable, used by Amazon within the Amazon "
     "Site.&rdquo;",
     ("S26",)),
    ("FTC: disclosure placement for affiliate links",
     BADGE_OK,
     "&ldquo;As for where to place a disclosure, the guiding principle is that it has to be clear and "
     "conspicuous. The closer the disclosure is to your recommendation, the better.&rdquo;",
     ("S44",)),
    ("FTC: &ldquo;affiliate link&rdquo; alone is not an adequate disclosure",
     BADGE_OK,
     "&ldquo;Consumers might not understand that &lsquo;affiliate link&rsquo; means that the person "
     "placing the link is getting paid for purchases made through the link. Similarly, a &lsquo;buy "
     "now&rsquo; button would not be adequate.&rdquo;",
     ("S44",)),
    ("FTC: Endorsement Guides were revised in 2023",
     BADGE_OK_P,
     "The FTC topic page recommends reading &ldquo;the latest version of the Endorsement Guides, which "
     "were revised in 2023 with new or revised principles, examples, and definitions, including a new "
     "definition of &lsquo;clearly and conspicuously.&rsquo;&rdquo;",
     ("S44", "S24")),
]

LINK_ROWS = [
    ("https://link.amazon/B04G1MEwY", "B04G1MEwY", "9",
     "https://www.amazon.com/dp/B0CDY277D3", "B0CDY277D3",
     "Amazon.com: CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, "
     "Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double "
     "Air Fryer - Black : Home &amp; Kitchen",
     ("S11", "S14")),
    ("https://link.amazon/B02NbDxp3", "B02NbDxp3", "9",
     "https://www.amazon.com/dp/B09B7SB46R", "B09B7SB46R",
     "Amazon.com: Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven | 26QT air "
     "fryer oven with French doors, 24 cooking functions, dual-speed fan and rotisserie for easy "
     "family meals. : Home &amp; Kitchen",
     ("S12", "S15")),
    ("https://link.amazon/B00hJ57DV", "B00hJ57DV", "9",
     "https://www.amazon.com/dp/B08DKYBTPH", "B08DKYBTPH",
     "Amazon.com: Chefman Air Fryer 8 Qt | TurboFry&reg; 4-in-1 with 450&deg;F Hi-Fry Option for "
     "Crispier Results | Bake, Dehydrate, Frozen | XL Nonstick Dishwasher-Safe Basket | Stainless "
     "Steel : Home &amp; Kitchen",
     ("S13", "S16")),
]

DIRECT_ROWS = [
    ("https://www.amazon.com/dp/B04G1MEwY",
     "Page Not Found &mdash; &ldquo;Sorry! We couldn't find that page.&rdquo;", ("S08",)),
    ("https://www.amazon.com/dp/B02NbDxp3",
     "Page Not Found &mdash; &ldquo;Sorry! We couldn't find that page.&rdquo;", ("S09",)),
    ("https://www.amazon.com/dp/B00hJ57DV",
     "Page Not Found &mdash; &ldquo;Sorry! We couldn't find that page.&rdquo;", ("S10",)),
]

REPO_ROWS = [
    ("Sitemap coverage",
     '<span class="badge ok">Resolved &mdash; no defect</span>',
     "<code>python3 scripts/build_sitemap.py --check</code> exits 0 and reports &ldquo;sitemap.xml "
     "covers every live page (65 pages checked, 0 extra entries)&rdquo;. "
     "(<code>repo:scripts/build_sitemap.py</code> &middot; <code>repo:sitemap.xml</code>.) "
     "The five pages named in "
     "C3-F-01 are meta-refresh redirect stubs, which the generator excludes on purpose "
     "(<code>analysis.html</code>, <code>disclosure.html</code>, "
     "<code>categories/home-kitchen-air-fryers.html</code>, <code>flagged-for-review.html</code>, "
     "<code>marketing.html</code>), and <code>index.html</code> is emitted as the site root URL "
     "<code>/Zone3/</code>. See 25-F-02.",
     ()),
    ("Internal link integrity (files and anchors)",
     '<span class="badge ok">0 problems</span>',
     "A full crawl of the live tree resolved 2,351 internal <code>href</code>/<code>src</code> "
     "references across 70 pages. No missing file, no missing fragment, no reference escaping the "
     "site root. The crawl excluded <code>archive/</code>, which holds byte-for-byte snapshots of "
     "other sessions' sites. (<code>repo:sessions/25513d33/build_record.py</code> &middot; "
     "<code>repo:tools/verify_site.py</code>.)",
     ()),
    ("Orphan pages",
     '<span class="badge ok">2, both intentional</span>',
     "<code>404.html</code> is the GitHub Pages custom error page, and <code>marketing.html</code> is "
     "a meta-refresh stub to <code>marketing/index.html</code>. Neither should appear in "
     "navigation. (<code>repo:404.html</code> &middot; <code>repo:marketing.html</code>.)",
     ()),
    ("Generator idempotence",
     '<span class="badge ok">Stable fixpoint</span>',
     "<code>scripts/build_site.py</code>, <code>tools/build_site.py</code>, "
     "<code>scripts/build_marketing.py</code>, <code>tools/build_record.py</code> and this generator "
     "were each run twice; a <code>diff -rq</code> against a pre-run copy of the tree showed no "
     "differences. (<code>repo:scripts/build_site.py</code> &middot; "
     "<code>repo:tools/build_site.py</code> &middot; <code>repo:sessions/25513d33/build_record.py</code>.)",
     ()),
]

IRREGULARITIES = [
    ("25-F-01", "Info",
     "All three destination listings carry the same Amazon browse breadcrumb &mdash; "
     "<em>Home &amp; Kitchen &rsaquo; Kitchen &amp; Dining &rsaquo; Small Appliances &rsaquo; Fryers "
     "&rsaquo; Air Fryers</em>, node <code>17659096011</code> &mdash; read from the pages Amazon "
     "served on 2026-11-14. The repository records that breadcrumb only for product 1 "
     "(<code>data/products.json</code> &rarr; <code>observed_2026_11_14.category_path</code>). "
     "Published cells are unaffected: a browse node is a <em>category</em> fact, and the per-product "
     "commission rate still cannot be tied to a rate without the account's own rate card, so the rate "
     "cells stay blank (FLG-013, FLG-021).",
     ("S11", "S12", "S13", "S25")),
    ("25-F-02", "Info",
     "C3-F-01 (sitemap drift, session c3dbcc40) is a false positive. The five named pages are "
     "redirect stubs the sitemap generator excludes on purpose, and <code>index.html</code> is "
     "present as the site root URL. No change to <code>sitemap.xml</code> is needed. Recorded here "
     "so the integration owner can close that item rather than regenerate a file that is already "
     "correct.",
     ("S56",)),
]


def render() -> str:
    def rows(items):
        return "".join(
            f"<tr><td>{a}</td><td>{b}</td><td>{c}</td>"
            f"<td>{src(*d) if d else '&mdash;'}</td></tr>"
            for a, b, c, d in items
        )

    link_rows = "".join(
        f'<tr><td><a href="{html.escape(sub)}" target="_blank" rel="noopener noreferrer">'
        f'{html.escape(sub)}</a></td><td><code>{html.escape(code)}</code></td><td>{n}</td>'
        f'<td><a href="{html.escape(dest)}" target="_blank" rel="noopener noreferrer">'
        f'<code>{html.escape(asin)}</code></a></td><td>{title}</td>'
        f'<td>{src(*s)}</td></tr>'
        for sub, code, n, dest, asin, title, s in LINK_ROWS
    )
    direct_rows = "".join(
        f'<tr><td><code>{html.escape(u)}</code></td><td>{r}</td><td>{src(*s)}</td></tr>'
        for u, r, s in DIRECT_ROWS
    )

    flags = "".join(
        f'<div class="card"><h3 id="{fid}"><span class="flagid">{fid}</span> '
        f'<span class="badge warn">{sev}</span></h3><p>{detail}</p>'
        f'<p class="muted">Sources: {src(*s) if s else "&mdash;"}</p></div>'
        for fid, sev, detail, s in IRREGULARITIES
    )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Session 25513d33 verification record | Zone3</title>
<meta name="description" content="Independent line-by-line verification record, session 25513d33, 2026-11-14.">
<link rel="stylesheet" href="../../assets/style.css">
</head>
<body>
<header class="topbar">
  <div class="brand"><a href="../../index.html">Zone3</a><span>Amazon affiliate dashboard</span></div>
  <nav><a href="../../index.html">Dashboard</a><a href="../../executive-summary.html">Executive summary</a><a href="../../products.html">Products</a><a href="../../verification.html">Verification log</a><a href="../../flagged.html">Flagged for review</a><a href="../../sources.html">Sources</a></nav>
</header>
<main>
<h1>Session 25513d33 &mdash; independent verification record</h1>
<p class="lead">Every row below was produced by a fetch this session performed on 2026-11-14 against the
official page named in its Source cell. Nothing here is copied from another session's record, and no
third-party page is used as evidence. A value that could not be confirmed from an official source is
not shown.</p>

<div class="callout">
  <p><strong>Result.</strong> All three submitted <code>link.amazon</code> short links were re-fetched and
  land on the same three listings the repository already records. All three raw 9-character tokens return
  Amazon's &ldquo;Page Not Found&rdquo; page when used directly as an ASIN, so the tokens are short-link
  IDs and not ASINs. Twelve load-bearing policy and disclosure statements were re-read and match the
  repository's stored wording verbatim. Two repository-integrity checks were run; one open item from an
  earlier session (C3-F-01) is resolved as a false positive, and one new observation is recorded
  (25-F-01). Nothing load-bearing was found to be wrong.</p>
</div>

<h2>1. Submitted links, re-fetched 2026-11-14</h2>
<div class="table-wrap"><table>
<thead><tr><th>Submitted link</th><th>Code</th><th>Chars</th><th>Resolves to (ASIN)</th><th>Page title as served by Amazon</th><th>Source</th></tr></thead>
<tbody>{link_rows}</tbody>
</table></div>

<h2>2. Control &mdash; the raw token used directly as an ASIN</h2>
<p>Each submitted code is 9 characters. Amazon defines an ASIN as a
<code>10-Character alphanumeric unique identifier</code>
({src("S31")}) and, on its own selling blog, as
&ldquo;a unique 10-character alphanumeric code assigned to every product listed in the Amazon store&rdquo;
({src("S45")}). Using the raw token where an ASIN belongs:</p>
<div class="table-wrap"><table>
<thead><tr><th>URL fetched</th><th>Result</th><th>Source</th></tr></thead>
<tbody>{direct_rows}</tbody>
</table></div>
<p>The three listings above are reachable only through the short links; the positive control is that the
same fetch method returns a full product page for each destination ASIN (column 4 of section 1).</p>

<h2>3. Policy and disclosure statements, re-read 2026-11-14</h2>
<div class="table-wrap"><table>
<thead><tr><th>Claim</th><th>Result</th><th>Wording on the official page</th><th>Source</th></tr></thead>
<tbody>{rows(POLICY_ROWS)}</tbody>
</table></div>
<p><strong>Why this matters for the blank cells.</strong> Clauses 2(b) and 6(t) above are the reason this
site leaves price, star-rating and review-count cells empty. This session reached that conclusion
independently from the official text: displaying a price scraped off a rendered Amazon page breaches 2(b)
even where the number is read correctly, and the same is true of a star rating under 6(t). No Associates
tag and no API credentials exist for this project, so neither permitted route is available.</p>

<h2>4. Repository integrity checks</h2>
<div class="table-wrap"><table>
<thead><tr><th>Check</th><th>Result</th><th>What was run</th><th>Source</th></tr></thead>
<tbody>{rows(REPO_ROWS)}</tbody>
</table></div>

<h2>5. Irregularities raised by this session</h2>
<p>Neither item blocks the merge. Both are informational.</p>
{flags}

<h2>6. Limits of this record</h2>
<ul>
  <li>Whether the three observed destination listings are the products the requester intended is
  <strong>not</strong> established by any official source. Only the redirect destination is verified.
  That item stays open on the <a href="../../flagged.html">Flagged for review</a> page.</li>
  <li>Whether a <code>link.amazon</code> redirect counts as a <em>Redirecting Link</em> (purchases
  through which are disqualified, Commission Income Statement 2(e)) can only be tested inside a
  logged-in Associates account. It was not tested here.</li>
  <li>The Amazon pages fetched do display prices and star ratings to a browser. Those values are
  deliberately <strong>not</strong> reproduced anywhere on this site, for the 2(b) and 6(t) reasons in
  section 3.</li>
</ul>

<p><a href="../../index.html">&larr; Back to the dashboard</a></p>
</main>
<footer>
  <p class="disclosure"><strong>Disclosure:</strong> As an Amazon Associate I earn from qualifying purchases.</p>
  <p class="muted">Session 25513d33 verification record, 2026-11-14. Generated by
  <code>sessions/25513d33/build_record.py</code>; source URLs are read from
  <code>data/sources.json</code> at build time so a label cannot drift from its link.</p>
</footer>
</body>
</html>
"""


if __name__ == "__main__":
    OUT.write_text(render(), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")

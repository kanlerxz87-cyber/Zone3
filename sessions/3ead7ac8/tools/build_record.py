#!/usr/bin/env python3
"""Session 3ead7ac8 — build this session's verification record page.

Every row below was produced by fetching the official page named in its Source
cell during this session on 2026-11-14. No value in this record came from
another session's notes, from a search snippet, or from inference: a row exists
only because the quoted text or the observed response was on the page when it
was fetched. Source URLs are read from data/sources.json so a label can never
drift from the URL it points at.

    python3 sessions/3ead7ac8/tools/build_record.py
"""

from __future__ import annotations

import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]

SRCS = {s["id"]: s for s in json.loads((ROOT / "data/sources.json").read_text(encoding="utf-8"))["sources"]}

# (claim, result, what was observed, [source ids])
ROWS: list[tuple[str, str, str, list[str]]] = [
    ("The three submitted identifiers are 9 characters, not 10",
     "Confirmed",
     "Counted directly: B04G1MEwY = 9, B02NbDxp3 = 9, B00hJ57DV = 9. Amazon defines an ASIN as a "
     "10-character alphanumeric unique identifier.",
     ["S31", "S45", "S08", "S09", "S10"]),

    ("amazon.com/dp/&lt;submitted id&gt; does not resolve for any of the three",
     "Confirmed",
     "All three fetched in this session; each returned Amazon's &ldquo;Page Not Found&rdquo; page. "
     "This is the expected result for a short-link token and is not evidence that the short link fails.",
     ["S08", "S09", "S10"]),

    ("Each link.amazon short link opens a different live listing",
     "Confirmed",
     "B04G1MEwY &rarr; B0CDY277D3, &ldquo;CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View "
     "Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying "
     "Baskets, Digital Double Air Fryer - Black&rdquo;. "
     "B02NbDxp3 &rarr; B09B7SB46R, &ldquo;Emeril Lagasse 26QT French Door Multi-Function Air Fryer "
     "Toaster Oven&rdquo;. "
     "B00hJ57DV &rarr; B08DKYBTPH, &ldquo;Chefman Air Fryer 8 Qt | TurboFry&reg; 4-in-1 with "
     "450&deg;F Hi-Fry Option for Crispier Results&rdquo;. Same three targets recorded on 2026-11-13.",
     ["S11", "S12", "S13", "S14", "S15", "S16"]),

    ("Operating Agreement header and &sect;5 disclosure wording",
     "Confirmed verbatim",
     "Header still reads &ldquo;Updated: October 15, 2025&rdquo;. &sect;5: &ldquo;You must clearly and "
     "prominently state the following &hellip; &lsquo;As an Amazon Associate I earn from qualifying "
     "purchases.'&rdquo;",
     ["S01"]),

    ("&sect;6: breaching &sect;5 is a material breach",
     "Confirmed verbatim",
     "&ldquo;For the avoidance of doubt &hellip; any violation of Section 5 &hellip; will be deemed a "
     "material breach of this Agreement.&rdquo;",
     ["S01"]),

    ("Opening paragraph: compensated customer reviews are prohibited",
     "Confirmed verbatim",
     "&ldquo;Content you post on the Amazon.com website must abide by Amazon's Community Guidelines, "
     "including the prohibition of customer reviews that are created, edited, or removed in exchange "
     "for compensation.&rdquo; Recorded as PF-53; the earlier withdrawal of PF-14 said this text was "
     "not found, which is why flag 3E-F-06 was raised.",
     ["S01"]),

    ("Participation Requirements 2(b): the Associates tag must be in every link URL",
     "Confirmed verbatim",
     "&ldquo;For example, you must include your Associates ID or &lsquo;tag' (appearing as XXXXX-##, "
     "or such other format as we may designate) as a parameter in the URL of each link you place on "
     "your Site to an Amazon Site.&rdquo;",
     ["S02"]),

    ("Participation Requirements 2(b): prices and availability",
     "Confirmed verbatim",
     "&ldquo;your Site may only show prices and availability if: (a) we serve the link in which that "
     "price and availability data are displayed, or (b) you obtain Product pricing and availability "
     "data via Creators API or PA API and you comply with the requirements regarding use of Creators "
     "API or PA API in the License.&rdquo; This is the rule that 3E-F-01 and 3E-F-02 enforce.",
     ["S02"]),

    ("Participation Requirements 2(b): no misleading claims; comparison-price rule",
     "Confirmed verbatim",
     "&ldquo;You must not make inaccurate, overbroad, deceptive or otherwise misleading claims about "
     "any Product &hellip;&rdquo; and, for comparison formats, both the lowest &ldquo;new&rdquo; and "
     "(if provided) lowest &ldquo;used&rdquo; Amazon price must be shown.",
     ["S02"]),

    ("Participation Requirements 6(s), 6(t), 6(v), 6(w), 6(y), 6(z)",
     "Confirmed verbatim",
     "6(s) no artificially generated clicks or Sessions; 6(t) no customer reviews or star ratings "
     "unless obtained through Creators API or PA API; 6(v) no cloaking or hiding the URL or user "
     "agent; 6(w) no link shortening that makes it unclear you are linking to an Amazon Site; 6(y) no "
     "price tracking or price alerting functionality; 6(z) Program Content only for products on an "
     "Amazon Site.",
     ["S02"]),

    ("Participation Requirements &sect;5: no machine-learning models from Special Links or Program Content",
     "Confirmed verbatim",
     "&ldquo;You will not, without or express prior written approval, use, or allow any third party "
     "to use, any Special Links or Program Content to develop machine learning models or related "
     "technology.&rdquo; (&ldquo;without or&rdquo; is as printed on the page.)",
     ["S02"]),

    ("IP License &sect;1: no data mining, robots or similar extraction tools",
     "Confirmed verbatim",
     "&ldquo;This license does not include any downloading, copying or other use of Program Content "
     "for the benefit of any third party, or any use of data mining, robots, or similar data "
     "gathering and extraction tools.&rdquo;",
     ["S02"]),

    ("IP License &sect;1: no large language or machine learning models from Program Content",
     "Confirmed verbatim",
     "&ldquo;&hellip; will not allow any third party to, use Program Content to, directly or "
     "indirectly, develop or improve large language or multimodal models, machine learning models or "
     "related technology.&rdquo;",
     ["S02"]),

    ("IP License 2(b): credentials and Associates tag required for API calls",
     "Confirmed verbatim",
     "&ldquo;You must use both a unique public key/private key pair (each key pair, an &lsquo;Account "
     "Identifier') and an Associates tag parameter &hellip;&rdquo;",
     ["S02"]),

    ("IP License 2(e): no aggregation, analysis or model training without written approval",
     "Confirmed verbatim",
     "The sentence ends &ldquo;&hellip; or in the direct training or fine-tuning of a machine "
     "learning and/or foundational model.&rdquo; PF-23 on this site stops mid-sentence and omits that "
     "clause; recorded in full as PF-55, and the truncation raised as 3E-F-07.",
     ["S02"]),

    ("IP License 2(h), 2(i), 2(j), 2(k): caching, date stamp, size limit, disclaimer",
     "Confirmed verbatim",
     "24-hour cache limit and ASINs storable until termination (2(h)); date/time stamp next to price "
     "or availability, refreshed at least hourly (2(i)); no files greater than 40KB (2(j)); the "
     "CERTAIN CONTENT THAT APPEARS &hellip; COMES FROM AMAZON disclaimer (2(k)).",
     ["S02"]),

    ("Agent Terms 4(c): agents must identify themselves in the user-agent string",
     "Confirmed verbatim",
     "&ldquo;In all HTTP/HTTPS requests, identify that the request is from an Agent and disclose the "
     "name of the Agent by including the following in the request's user agent string: "
     "&lsquo;Agent/[agent name]'&rdquo;, and agents must not conceal that access is automated or "
     "circumvent CAPTCHAs.",
     ["S02"]),

    ("Commission Income Statement 2: disqualifications and the session window",
     "Confirmed verbatim",
     "24-hour session, 89-day cart window; &ldquo;any Product order where a cancellation, return, or "
     "refund has been initiated&rdquo;; and the Redirecting Link disqualification in 2(e).",
     ["S02"]),

    ("Commission Income Statement 6: payment timing and minimums",
     "Confirmed verbatim",
     "&ldquo;approximately 60 days following the end of each calendar month&rdquo;; Payment Minimum "
     "Chart: Deposit 10 USD, Gift Card 10 USD (max 2000 USD), Check 100 USD, Check Processing Fee "
     "15 USD.",
     ["S02"]),

    ("Influencer Program Policy 3(c): endorsement wording example",
     "Confirmed verbatim",
     "&ldquo;&hellip; including those described in the FTC Endorsement Guides (such as by using the "
     "text &lsquo;#Ad' or &lsquo;#Sponsored').&rdquo;",
     ["S02"]),

    ("Standard Commission Income Statement, Table 1, renders without a sign-in",
     "Confirmed, row for row",
     "Luxury Beauty / Luxury Stores Beauty / Amazon Explore 10.00%; Physical Books, Kitchen, "
     "Automotive 4.50%; All Other Categories 4.00%; Gift Cards and the named exclusions 0.00%. Only "
     "the per-account /help/operating/schedule rate card is gated.",
     ["S25", "S03"]),

    ("Creators API GetItems, ItemIdType parameter: ASIN length",
     "Confirmed verbatim",
     "&ldquo;ASIN | Amazon Standard Identification Number: 10-Character alphanumeric unique "
     "identifier assigned by Amazon.&rdquo;",
     ["S31", "S06"]),

    ("Sell on Amazon: a second official statement of ASIN length",
     "Confirmed verbatim",
     "&ldquo;It's a unique 10-character alphanumeric code assigned to every product listed in the "
     "Amazon store.&rdquo; Article dated Jun 4, 2025.",
     ["S45"]),

    ("PA-API 5 is deprecated",
     "Confirmed verbatim",
     "&ldquo;The Amazon Product Advertising API 5.0 (PA-API 5) has been deprecated and is being "
     "replaced by the Creators API.&rdquo; Calls return HTTP 403 with an AccessDeniedException.",
     ["S05"]),

    ("FTC Disclosures 101 (dated November 2019 on the page)",
     "Confirmed verbatim",
     "&ldquo;Disclose when you have any financial, employment, personal, or family relationship with "
     "a brand.&rdquo; &ldquo;Place it so it's hard to miss.&rdquo; &ldquo;You can't talk about your "
     "experience with a product you haven't tried.&rdquo;",
     ["S07"]),

    ("FTC: the Endorsement Guides were revised in 2023",
     "Confirmed",
     "&ldquo;&hellip; read the latest version of the Endorsement Guides, which were revised in 2023 "
     "with new or revised principles, examples, and definitions, including a new definition of "
     "&lsquo;clearly and conspicuously.'&rdquo;",
     ["S44"]),

    ("FTC: affiliate-link disclosure standard",
     "Confirmed verbatim",
     "&ldquo;You should disclose your relationship to the retailer clearly and conspicuously on your "
     "site &hellip;&rdquo;; &ldquo;The closer the disclosure is to your recommendation, the "
     "better.&rdquo;; and &ldquo;Consumers might not understand that &lsquo;affiliate link' means "
     "&hellip; Similarly, a &lsquo;buy now' button would not be adequate.&rdquo;",
     ["S44"]),

    ("Associates Help, Account Dormancy: 180 days to refer a sale",
     "Confirmed verbatim",
     "&ldquo;Once you've applied, you have 180 days to refer a sale through one of your Associates "
     "links.&rdquo; &ldquo;Your application can be withdrawn if there were not enough qualifying "
     "sales for 180 days after your application was submitted.&rdquo; The page also states that three "
     "qualifying sales trigger review, and that after 3 years with no commission income a maintenance "
     "fee of the lesser of $10 or the unpaid balance may be charged.",
     ["S28"]),

    ("Associates Help, application review: three qualifying sales in 180 days",
     "Confirmed verbatim",
     "&ldquo;&hellip; once you've driven qualified sales (we require at least three within the first "
     "180 days). Please note that personal orders do not qualify.&rdquo;",
     ["S29"]),

    ("Best Sellers in Air Fryers (browse node 17659096011) is live and positions 1&ndash;6 were read",
     "Confirmed",
     "The official Best Sellers page loaded and returned the ranked list. Positions shift between "
     "captures, which is why the published benchmark is dated and why FLG-025 exists.",
     ["S43"]),
]

# (field, status, why, [source ids], [flag ids])
NOT_VERIFIED: list[tuple[str, str, str, list[str], list[str]]] = [
    ("Which commission rate category each listing falls in",
     "Not resolvable from any official page",
     "Table 1 is public, but no official page ties a category to these three listings, so no rate is "
     "attached to a product row anywhere on this site.",
     ["S25"], ["FLG-021"]),
    ("Price, star rating and review count for the three listings",
     "Deliberately not displayed",
     "Observed on Amazon pages on 2026-11-14 and kept as research evidence, but 2(b) and 6(t) bar "
     "displaying them without an Amazon-served link or Creators API / PA API data. This session "
     "withheld 90 cells that had been rendered as product facts.",
     ["S02"], ["FLG-022", "FLG-023", "3E-F-01", "3E-F-02"]),
    ("Clicks, conversions and revenue",
     "No data exists yet",
     "No campaign is live and Amazon reports these in-account only, so the ledger is empty by design.",
     ["S02"], ["FLG-011"]),
]


def e(s: str) -> str:
    return html.escape(s, quote=False)


def src_links(ids: list[str]) -> str:
    out = []
    for sid in ids:
        s = SRCS.get(sid)
        if not s:
            raise SystemExit(f"unknown source id {sid}")
        out.append(
            f'<a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer" '
            f'title="{e(s.get("title", ""))}">{sid}</a>'
        )
    return " &middot; ".join(out)


def flag_links(ids: list[str]) -> str:
    return " ".join(
        f'<a class="flagid" href="../../flagged.html#{fid}">{fid}</a>' for fid in ids)


def row(cells: list[str]) -> str:
    return "<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>"


def table(headers: list[str], rows: list[list[str]]) -> str:
    th = "".join(f"<th>{e(h)}</th>" for h in headers)
    tb = "".join(row(r) for r in rows)
    return f'<div class="table-wrap"><table><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>'


NAV = [
    ("../../index.html", "Dashboard"),
    ("../../executive-summary.html", "Executive summary"),
    ("../../products.html", "Products"),
    ("../../flagged.html", "Flagged for review"),
    ("../../sources.html", "Sources"),
    ("../../verification.html", "Verification log"),
    ("../../docs/index.html", "Reference (/docs/)"),
    ("../../dashboard/index.html", "Full audit (16 pages)"),
]


def build() -> str:
    nav_parts = []
    for href, label in NAV:
        cls = ' class="active"' if href.startswith("index") else ""
        nav_parts.append(f'<a href="{href}"{cls}>{e(label)}</a>')
    nav = "".join(nav_parts)
    verified = "".join(
        row([e(c), f'<span class="badge ok">{r}</span>' if "verbatim" not in r and "row for row" not in r
             else f'<span class="badge ok">{r}</span>', o, src_links(s)])
        for c, r, o, s in ROWS
    )
    notver = "".join(
        row([f"<strong>{e(a)}</strong>", f'<span class="badge unv">{e(b)}</span>', e(c),
             (src_links(s) + " " if s else "") + flag_links(f)])
        for a, b, c, s, f in NOT_VERIFIED)

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Verification record — session 3ead7ac8 | Zone3 Amazon affiliate dashboard</title>
<meta name="description" content="Line-by-line re-verification of every load-bearing claim on the Zone3 site, re-read from the official pages on 2026-11-14 by session 3ead7ac8.">
<link rel="stylesheet" href="../../assets/style.css">
</head>
<body>
<header class="topbar">
  <div class="brand"><a href="../../index.html">Zone3</a><span>Amazon affiliate dashboard</span></div>
  <nav>{nav}</nav>
</header>
<main>
<h1>Verification record — session <code>3ead7ac8</code></h1>
<p class="lead">Every row below was produced by fetching the official page named in its Source cell
during this session, on 2026-11-14. Nothing here is quoted from another session's notes, from a
search snippet, or from memory. Where a row says <em>Confirmed verbatim</em>, the quoted wording was
on the page when it was fetched.</p>

<div class="callout">
  <p><strong>Scope of this page.</strong> Branch <code>arena/3ead7ac8-zone3</code>, base
  <code>4fd8bd6</code>. This session re-read 13 official pages, re-resolved all three submitted short
  links, and compared the result against what the site publishes. Findings that did not match, or that
  were missing, are published as <code>3E-F-01</code> to <code>3E-F-09</code> on the
  <a href="../../flagged.html">Flagged for review</a> page.</p>
</div>

<h2>Claims re-read from the official pages</h2>
<div class="table-wrap"><table class="reverify"><thead><tr><th>Claim</th><th>Result</th><th>What was on the official page</th><th>Source</th></tr></thead><tbody>{verified}</tbody></table></div>

<h2>Deliberately left blank</h2>
<p>These are the fields a reader would most expect to see. Each is blank for a stated reason, not for
want of trying, and none of them was filled in by inference.</p>
<div class="table-wrap"><table><thead><tr><th>Field</th><th>Status</th><th>Why it is blank</th><th>Source</th></tr></thead><tbody>{notver}</tbody></table></div>

<h2>Official pages fetched by this session</h2>
<ul class="findings">
  <li>Operating Agreement &mdash; {src_links(['S01'])} (chunks 0&ndash;2 of 4)</li>
  <li>Program Policies &mdash; {src_links(['S02'])} (chunks 1&ndash;9 of 11; chunk 10 not read)</li>
  <li>Standard Commission Income Statement, Table 1 &mdash; {src_links(['S25'])}</li>
  <li>Commission schedule, per-account rate card &mdash; {src_links(['S03'])} (returns a sign-in redirect; no value taken from it)</li>
  <li>Creators API GetItems &mdash; {src_links(['S06'])} &middot; {src_links(['S31'])}</li>
  <li>PA-API 5 deprecation notice &mdash; {src_links(['S05'])}</li>
  <li>Associates Help: Account Dormancy &mdash; {src_links(['S28'])}; Application review &mdash; {src_links(['S29'])}</li>
  <li>Best Sellers in Air Fryers &mdash; {src_links(['S43'])}</li>
  <li>Sell on Amazon, ASIN guide &mdash; {src_links(['S45'])}</li>
  <li>FTC Disclosures 101 &mdash; {src_links(['S07'])}; FTC Endorsement Guides FAQ &mdash; {src_links(['S44'])}; FTC topic hub &mdash; {src_links(['S24'])}</li>
  <li>The three submitted short links &mdash; {src_links(['S11', 'S12', 'S13'])} and their destinations {src_links(['S14', 'S15', 'S16'])}</li>
  <li>Direct <code>/dp/</code> checks for the three submitted codes &mdash; {src_links(['S08', 'S09', 'S10'])}</li>
</ul>
<p class="small">No third-party page was used as evidence for any row on this page.</p>
</main>
<footer>
  <p class="disclosure"><strong>Disclosure:</strong> As an Amazon Associate I earn from qualifying purchases.</p>
  <p class="muted">Recorded 2026-11-14 by session <code>3ead7ac8</code>. Built by
  <code>sessions/3ead7ac8/tools/build_record.py</code>; source URLs are read from
  <code>data/sources.json</code> at build time.</p>
</footer>
</body>
</html>
"""


def main() -> None:
    out = ROOT / "sessions" / "3ead7ac8" / "index.html"
    out.write_text(build(), encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({len(ROWS)} verified rows, {len(NOT_VERIFIED)} blank-field rows)")


if __name__ == "__main__":
    main()

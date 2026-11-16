#!/usr/bin/env python3
"""Build the static GitHub Pages site from data/*.json.

Standard library only. Run from the repository root:

    python3 scripts/build_site.py

Writes index.html, executive-summary.html, products.html, pricing.html,
reviews.html, content.html, campaigns.html, flagged.html, sources.html,
assets/style.css and .nojekyll in the repository root. Every table cell is
generated from a record in data/*.json. A null value renders as a blank cell
labelled "Unverified". Nothing is filled in by hand.
"""
from __future__ import annotations

import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = "https://github.com/kanlerxz87-cyber/Zone3"
DATA = ROOT / "data"
ASSETS = ROOT / "assets"
BUILT = "2026-11-16"
DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."


def load(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


SRC = load("sources.json")
SOURCES = {s["id"]: s for s in SRC["sources"]}
PRODUCTS = load("products.json")["products"]
FACTS = {f["id"]: f for f in load("policy_facts.json")["facts"]}
FLAGS = load("flags.json")["flags"]
TOPICS = load("topics.json")
SUGGESTIONS = load("suggestions.json")
<<<<<<< HEAD
DESIGN = load("design-brief.json")
QUEUE = load("decision-queue.json")
=======
# Added by session 5a56c084 (2026-11-16): the Research Desk articles, used by the
# landing page's editorial section. Generated into articles/ by build_5a56c084.py.
ARTICLES = load("articles.json")
>>>>>>> origin/main


def e(value) -> str:
    return html.escape(str(value), quote=True)


def src_links(ids) -> str:
    if not ids:
        return '<span class="muted">no source</span>'
    parts = []
    for sid in ids:
        s = SOURCES[sid]
        parts.append(
            f'<a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer" '
            f'title="{e(s["title"])}">{e(sid)}</a>'
        )
    return " &middot; ".join(parts)


def flag_links(ids) -> str:
    return " ".join(f'<a class="flagid" href="flagged.html#{e(i)}">{e(i)}</a>' for i in ids) or "&mdash;"


def unv() -> str:
    return '<span class="badge unv">Unverified</span>'


def val(v) -> str:
    return unv() if v is None else e(v)


def badge(text: str, kind: str) -> str:
    return f'<span class="badge {e(kind)}">{e(text)}</span>'


def sev(text: str) -> str:
    # "Info" is used for correction/annotation entries (V-F1, V-F2 added 2026-11-14).
    kind = {"Critical": "bad", "High": "warn", "Medium": "info", "Low": "muted",
            "Info": "muted"}[text]
    return badge(text, kind)


def table(headers, rows, cls: str = "") -> str:
    th = "".join(f"<th>{e(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return (
        f'<div class="table-wrap"><table class="{e(cls)}"><thead><tr>{th}</tr></thead>'
        f"<tbody>{body}</tbody></table></div>"
    )


NAV_PRIMARY = [
    ("index.html", "Home"),
    ("marketing/comparison.html", "Compare"),
    ("marketing/buying-guide.html", "Buying guide"),
    # Added by session 5a56c084 (2026-11-16): the Research Desk article hub
    # (proposals SUG-02/SUG-03 implemented; decision log on suggestions.html).
    ("articles/index.html", "Research Desk"),
    ("decision-center.html", "Decision Center"),
<<<<<<< HEAD
    # Added by integration session 3d359c23 (2026-11-14): the editorial topic plan the brief
    # asks for ("catchy trendy articles and topics"). Every topic row carries the official
    # source of the fact it rests on; no trend or volume claim is made.
    ("content-topics.html", "Content topics"),
    # Added by session 4f83ee7b (2026-11-15): the suggestions and decision framework the brief
    # asks for. Proposals are labelled as proposals; every factual row carries an official
    # source. Nothing here is implemented by this session — it is published for review.
    ("suggestions.html", "Suggestions &amp; decisions"),
    # Added by session 757efebc (2026-11-16): the redesign brief with the copy-paste
    # prompt, and the console where every proposal is reviewed before implementation.
    ("design-brief.html", "Design brief"),
    ("decision-queue.html", "Review console"),
    ("campaigns.html", "Campaigns &amp; tracking"),
    ("flagged.html", "Flagged for review"),
    ("sources.html", "Sources"),
    # Added by integration session edbd56a1 (2026-11-14): one row per published claim,
    # each linked to the official page it was read from.
    ("verification.html", "Verification log"),
    # Added by integration session 3ead7ac8 (2026-11-14): this session's line-by-line record.
    # Every row links the official page it was read from; source URLs come from data/sources.json.
    ("sessions/3ead7ac8/index.html", "Verification (3ead7ac8)"),
    # Added by session 25513d33 (2026-11-14): this session's independent record. Every row
    # was produced by a fetch performed by this session; labels read from data/sources.json.
    ("sessions/25513d33/index.html", "Verification (25513d33)"),
    # Added by session ab3ed329 (2026-11-16): independent re-verification of the three short links,
    # the Associates policy clauses and the commission table, plus the exposure check (AB-F-01).
    ("sessions/ab3ed329/index.html", "Verification (ab3ed329)"),
    # Added by session 5b425c74 (2026-11-16): this session's independent re-verification record.
    # Every row was produced by a fetch performed by this session on 2026-11-16.
    ("sessions/5b425c74/index.html", "Verification (5b425c74)"),
    # Added by integration session edbd56a1 (2026-11-14): /docs/ returned HTTP 200 but had
    # no inbound link from any dashboard, so a browsing visitor could not reach it (flag V-F3).
    ("docs/index.html", "Reference (/docs/)"),
    # Added by session 588693c9 (2026-11-14): the marketing section generated by
    # scripts/build_marketing.py from data/marketing.json. Linked from the flat
    # site nav so product pages, comparison and buying guide are reachable.
    ("marketing/index.html", "Marketing (2026-11-14 brief set)"),
    # Added on integration 2026-11-14 (session b90c5685): product briefs page kept from PR #26
    # (session 9fef7647), rewritten to the no-inference/no-price rules and re-homed under marketing/.
    ("marketing/briefs.html", "Marketing briefs"),
    # Added by integration session 3c6cba43: the second site generation in this repo,
    # rendered by tools/build_site.py from data/z3/*.json. Linked here so the two halves of
    # the merged site are one navigable product instead of two disconnected trees.
    ("dashboard/index.html", "Full audit (16 pages)"),
    # Added by session 145b8df7 (2026-11-16): the editorial marketing layer this project
    # builds from data/editorial.json (read/), generated by scripts/build_read.py. It is a
    # SECOND reader-facing surface, produced in parallel with session 59d84c55's /site/
    # ("Air Fryer Field Notes"); neither session knew of the other before landing. Both are
    # published, neither is deleted, and the overlap is raised for the owner to resolve
    # (Z14-F-04 on the Flagged for review page).
    ("read/index.html", "Marketing site: The Crisp Report"),
=======
>>>>>>> origin/main
    # Added by integration session 59d84c55 (2026-11-16): the reader-facing marketing
    # site built by tools/build_i2_site.py from data/i2/*.json.
    # Added by session 145b8df7 (2026-11-16): the read/ editorial layer ("The Crisp
    # Report"), generated by scripts/build_read.py from data/editorial.json.
    ("read/index.html", "The Crisp Report"),
]

# Grouped under the "More" menu; every destination that was previously in the flat
# 20-link top navigation stays reachable (check_site crawls internal links, so a
# link lost here would fail the build).
NAV_MORE = [
    ("Guides & research", [
        ("marketing/index.html", "Marketing hub"),
        ("marketing/briefs.html", "Marketing briefs"),
        ("products.html", "Products"),
        ("air-fryers.html", "Category: Air Fryers"),
        ("pricing.html", "Pricing & commission"),
        ("reviews.html", "Reviews & competition"),
        ("content-topics.html", "Content topics"),
        ("content.html", "Content & compliance"),
    ]),
    ("Governance", [
        ("executive-summary.html", "Executive summary"),
        ("suggestions.html", "Suggestions & decisions"),
        ("campaigns.html", "Campaigns & tracking"),
        ("sources.html", "Sources"),
        ("verification.html", "Verification log"),
        ("sessions/3ead7ac8/index.html", "Verification (3ead7ac8)"),
        ("sessions/25513d33/index.html", "Verification (25513d33)"),
        ("sessions/5a56c084/index.html", "Verification (2026-11-16)"),
        # Added by session ab3ed329 (2026-11-16) alongside the other verification tiles.
        ("sessions/ab3ed329/index.html", "Verification (session ab3ed329)"),
        # Added by session ab3ed329 (2026-11-16): independent re-verification of the three
        # short links, the policy clauses and the commission table (AB Part on the board).
        ("sessions/ab3ed329/index.html", "Verification (ab3ed329)"),
        # Added by session 5b425c74 (2026-11-16): independent re-fetch of the three links,
        # both commission tables and the policy pages (5B42 Part on the board).
        ("sessions/5b425c74/index.html", "Verification (5b425c74)"),
        ("flagged.html", "Flagged for review"),
        ("docs/index.html", "Reference (/docs/)"),
        ("dashboard/index.html", "Full audit (16 pages)"),
    ]),
]


def page(filename: str, title: str, body: str, lead: str = "",
         description: str = "") -> None:
    """Render one page through the shared template.

    Session 5a56c084 (2026-11-16): the header now carries the Associates
    disclosure on every page as its own strip (Operating Agreement section 5,
    "clearly and prominently"; FTC: hard to miss), the primary navigation is
    five links with the rest grouped under a "More" menu, and the footer adds
    the Amazon content disclaimer and trademark note.
    """
    primary = []
    for href, label in NAV_PRIMARY:
        cls = ' class="active"' if href == filename else ""
        primary.append(f'<a href="{href}"{cls}>{label}</a>')
    groups = []
    for group, items in NAV_MORE:
        rendered = []
        for href, label in items:
            cls = ' class="active"' if href == filename else ""
            rendered.append(f'<a href="{href}"{cls}>{label}</a>')
        groups.append(f'<div class="nav-group"><b>{group}</b>{"".join(rendered)}</div>')
    nav = "".join(primary) + (
        '<details class="nav-more"><summary>More pages</summary>'
        f'<div class="nav-menu">{"".join(groups)}</div></details>'
    )
    lead_html = f'<p class="lead">{lead}</p>' if lead else ""
    desc = description or (
        "Zone3: verified Amazon affiliate product data, analysis and flags. "
        f"Status as of {BUILT}."
    )
    canonical = "https://kanlerxz87-cyber.github.io/Zone3/" + (
        "" if filename == "index.html" else filename
    )
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} | Zone3 — Air Fryer Research Desk</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canonical}">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="topbar">
  <div class="brand"><a href="index.html">Zone3</a><span>Air Fryer Research Desk</span></div>
  <nav>{nav}</nav>
</header>
<div class="disclose"><p><strong>Disclosure:</strong> As an Amazon Associate I earn from qualifying purchases.</p></div>
<main>
<h1>{e(title)}</h1>
{lead_html}
{body}
</main>
<footer>
  <div class="foot-grid">
    <div>
      <p class="disclosure"><strong>Disclosure:</strong> As an Amazon Associate I earn from qualifying purchases.</p>
      <p class="foot-disclaimer">CERTAIN CONTENT THAT APPEARS ON THIS SITE COMES FROM AMAZON. THIS CONTENT IS PROVIDED 'AS IS' AND IS SUBJECT TO CHANGE OR REMOVAL AT ANY TIME.</p>
      <p class="muted">Zone3 is independent and is not affiliated with, endorsed or sponsored by Amazon. Amazon, Amazon Associates and ASIN are trademarks of Amazon.com, Inc. or its affiliates.</p>
    </div>
    <div class="foot-links">
      <a href="articles/index.html">Research Desk</a><a href="sources.html">Sources</a><a href="flagged.html">Flagged for review</a><a href="verification.html">Verification log</a><a href="suggestions.html">Suggestions &amp; decisions</a><a href="landing-prior.html">Previous landing page</a><a href="https://github.com/kanlerxz87-cyber/Zone3">Repository</a>
    </div>
  </div>
  <p class="small foot-note">Data verified as of {BUILT} (re-verified 2026-11-14 and 2026-11-16; per-session records under <code>sessions/</code>). A cell marked <span class="badge unv">Unverified</span> has no official source yet and is left blank on purpose. Built by <code>scripts/build_site.py</code> and <code>scripts/build_5a56c084.py</code> from <code>data/*.json</code>. Source IDs (S01 and so on) link to the official page; see the <a href="sources.html">Sources</a> page.</p>
</footer>
</body>
</html>
"""
    if "/" in filename:
        # Page lives in a subdirectory: prefix every relative href/src so nav, stylesheet and
        # footer links resolve from there. Kept from PR #26 (session 9fef7647); without it a
        # subdirectory page's links 404 in the browser although they exist at the repo root.
        # Session 5a56c084 (2026-11-16): the prefix is now depth-aware ("../" per directory
        # level) - the first two-level page built through this template
        # (sessions/5a56c084/index.html) showed that the previous single "../" broke any page
        # nested more than one level deep.
        import re as _re

        depth = filename.count("/")
        prefix = "../" * depth

        def _up(m):
            attr, value = m.group(1), m.group(2)
            if value.startswith(("#", "http://", "https://", "mailto:", "tel:", "/", "\${", "data:")):
                return m.group(0)
            return f'{attr}{prefix}{value}"'

        doc = _re.sub(r'(href=")([^"]+)"', _up, doc)
        doc = _re.sub(r'(src=")([^"]+)"', _up, doc)

    (ROOT / filename).parent.mkdir(parents=True, exist_ok=True)
    (ROOT / filename).write_text(doc, encoding="utf-8")


def css() -> str:
    """Design system, rebuilt 2026-11-16 (session 5a56c084).

    Editorial "research desk" look: warm paper ground, deep evergreen primary,
    copper accents, serif display headings, system-ui text. No external fonts,
    no images, no JavaScript required. Every class used by any generated page
    (flat pages, marketing pages, the session record pages) is covered here.
    """
    return '''
:root{--ink:#24291f;--muted:#6d7264;--line:#e4dfcf;--line-soft:#edeadb;--bg:#f7f4ec;--card:#fffdf8;
--accent:#1e6b47;--accent-dark:#17402e;--accent-deep:#0f2f22;--copper:#b35a2a;--copper-bg:#f7e8dc;
--ok:#1d6b3f;--okbg:#e7f2e6;--warn:#8a5a00;--warnbg:#fdf1d2;--bad:#a03c30;--badbg:#fbe7e2;
--info:#275e8e;--infobg:#e6eef7;--grey:#efecdf;
--serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,"Times New Roman",serif;
--sans:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;font:15.5px/1.6 var(--sans);color:var(--ink);background:var(--bg)}
a{color:var(--accent)}
a:hover{color:var(--accent-dark)}
code{background:var(--grey);padding:1px 5px;border-radius:4px;font-size:.88em;word-break:break-all;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
h1,h2,h3{font-family:var(--serif);letter-spacing:-.01em}
h1{font-size:clamp(26px,4vw,34px);margin:6px 0 6px;line-height:1.15}
h2{font-size:clamp(20px,2.6vw,25px);margin:34px 0 12px;line-height:1.2}
h3{font-size:17px;margin:0 0 8px}

/* ---------- top bar ---------- */
.topbar{background:var(--card);border-bottom:1px solid var(--line);padding:10px 22px;display:flex;flex-wrap:wrap;gap:10px 22px;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:40}
.brand a{font-family:var(--serif);font-weight:800;font-size:21px;color:var(--accent-dark);text-decoration:none;margin-right:10px;letter-spacing:-.02em}
.brand span{color:var(--muted);font-size:13px}
.topbar nav{display:flex;flex-wrap:wrap;gap:4px;align-items:center}
.topbar nav a{padding:6px 11px;border-radius:8px;color:var(--ink);text-decoration:none;font-size:14px;font-weight:550}
.topbar nav a:hover{background:var(--grey)}
.topbar nav a.active{background:var(--accent);color:#fff}
.nav-more{position:relative}
.nav-more summary{list-style:none;cursor:pointer;padding:6px 11px;border-radius:8px;font-size:14px;font-weight:550;background:var(--grey)}
.nav-more summary::-webkit-details-marker{display:none}
.nav-more summary::after{content:" \\25BE";margin-left:5px;color:var(--muted)}
.nav-more[open] summary{background:var(--accent);color:#fff}
.nav-more[open] summary::after{color:#fff}
.nav-menu{position:absolute;right:0;top:calc(100% + 8px);background:var(--card);border:1px solid var(--line);border-radius:12px;box-shadow:0 18px 40px rgba(30,42,25,.16);padding:14px;display:grid;grid-template-columns:1fr 1fr;gap:4px 22px;min-width:430px;z-index:50}
.nav-group b{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.09em;color:var(--muted);margin:6px 0 4px}
.nav-group a{display:block;padding:5px 8px;border-radius:6px;font-size:13.5px;font-weight:400}
.nav-group a.active{background:var(--accent);color:#fff}
@media (max-width:720px){.nav-menu{grid-template-columns:1fr;min-width:min(92vw,430px);right:auto;left:0;position:fixed;top:96px;bottom:0;overflow:auto}}

/* ---------- disclosure strip ---------- */
.disclose{background:var(--warnbg);border-bottom:1px solid #ecd9a8;color:#6b4d0e;font-size:13px}
.disclose p{margin:0;padding:7px 22px;max-width:1180px;margin:0 auto}

/* ---------- layout ---------- */
main{max-width:1180px;margin:0 auto;padding:26px 22px 46px}
.lead{color:var(--muted);margin:2px 0 20px;max-width:900px;font-size:16px}
.small{font-size:13px;color:var(--muted)}
.muted{color:var(--muted)}

/* ---------- hero ---------- */
.hero{background:linear-gradient(118deg,var(--accent-deep),var(--accent-dark) 55%,#2e6b4a 90%);color:#fff;border-radius:20px;padding:44px clamp(22px,4.5vw,54px);margin:6px 0 24px;position:relative;overflow:hidden;box-shadow:0 22px 44px rgba(23,52,35,.22)}
.hero::after{content:"";position:absolute;inset:0;background:radial-gradient(680px 300px at 88% -12%,rgba(179,90,42,.28),transparent 62%),radial-gradient(520px 260px at -6% 108%,rgba(255,255,255,.09),transparent 60%);pointer-events:none}
.hero>*{position:relative;z-index:1}
.hero .eyebrow,.desk-intro .eyebrow,.kitchen-now .eyebrow,.decision-banner .eyebrow{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#e8d9be;font-weight:700;margin:0 0 12px}
.hero h2{font-size:clamp(30px,4.6vw,50px);line-height:1.08;max-width:820px;margin:0 0 14px;color:#fff}
.hero p{max-width:780px;color:#e9f0e8;margin:0 0 22px;font-size:16.5px}
.hero-actions{display:flex;gap:10px;flex-wrap:wrap}
.btn{display:inline-block;background:#fff;color:var(--accent-dark);border:1px solid #fff;border-radius:9px;padding:10px 16px;font-weight:650;text-decoration:none;font-size:14.5px}
.btn:hover{background:#f1efe6;color:var(--accent-deep)}
.btn.ghost{background:transparent;color:#fff;border-color:rgba(255,255,255,.55)}
.btn.ghost:hover{background:rgba(255,255,255,.12);color:#fff}
.hero-actions a:not(.btn){display:inline-block;border:1px solid rgba(255,255,255,.5);border-radius:9px;padding:10px 16px;color:#fff;text-decoration:none;font-weight:600}
.hero-actions a:first-child{background:#fff;color:var(--accent-dark);border-color:#fff}

/* ---------- status callout ---------- */
.callout{border:1px solid #f0dfb6;border-left:5px solid var(--warn);background:var(--warnbg);padding:14px 18px;border-radius:10px;margin:0 0 22px}
.callout.ok{border-color:#cfe4d2;border-left-color:var(--ok);background:var(--okbg)}
.callout p{margin:0}
.callout p+p{margin-top:8px}

/* ---------- stats ---------- */
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(185px,1fr));gap:14px;margin:0 0 26px}
.stat{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px 18px 15px;box-shadow:0 1px 3px rgba(36,41,31,.05)}
.stat .n{font-family:var(--serif);font-size:32px;font-weight:800;line-height:1.05;letter-spacing:-.01em}
.stat .l{color:var(--muted);font-size:13px;margin-top:6px}
.stat.bad .n{color:var(--bad)}
.stat.warn .n{color:var(--warn)}

/* ---------- product + article cards ---------- */
.product-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;margin:0 0 10px}
.pcard{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px;display:flex;flex-direction:column;gap:9px;box-shadow:0 1px 3px rgba(36,41,31,.05)}
.pcard-brand{font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--copper);font-weight:750}
.pcard b,.acard b{font-family:var(--serif);font-size:18.5px;line-height:1.3;color:var(--ink)}
.pcard .spec{color:var(--muted);font-size:14px;margin:0}
.pcard-actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:2px}
.pcard-actions .btn{background:var(--accent);color:#fff;border-color:var(--accent)}
.pcard-actions .btn:hover{background:var(--accent-dark)}
.pcard-actions .btn.ghost{background:transparent;color:var(--accent-dark);border-color:#c9c3b0}
.pcard-actions .btn.ghost:hover{background:var(--grey);color:var(--accent-deep)}
.pcard .small{margin:2px 0 0}
.acards{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:16px;margin:0 0 10px}
.acard{display:flex;flex-direction:column;gap:8px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px;text-decoration:none;color:var(--ink);box-shadow:0 1px 3px rgba(36,41,31,.05);transition:transform .12s ease,box-shadow .12s ease}
.acard:hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(36,41,31,.10);color:var(--ink)}
.acard-meta{font-size:12px;color:var(--copper);font-weight:650;letter-spacing:.02em}
.acard b{font-size:18px}
.acard span{color:var(--muted);font-size:13.5px}
.acard-go{color:var(--accent)!important;font-weight:650;margin-top:auto}
.more-link{margin:6px 2px 20px}

/* ---------- kitchen-now / decision-banner ---------- */
.kitchen-now,.decision-banner{display:flex;gap:20px;align-items:center;justify-content:space-between;flex-wrap:wrap;border-radius:16px;padding:26px clamp(20px,3.5vw,40px);margin:30px 0}
.kitchen-now{background:var(--copper-bg);border:1px solid #ecd6bd}
.kitchen-now h2{margin:0 0 8px;font-size:clamp(20px,2.6vw,26px)}
.kitchen-now p{margin:0;max-width:640px;color:#6d5638}
.kitchen-now .btn{background:var(--copper);border-color:var(--copper);color:#fff}
.kitchen-now .btn:hover{background:#99491e}
.trending{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:22px 24px;margin:30px 0}
.trending h2{font-size:clamp(20px,2.6vw,25px);margin:0 0 8px}
.decision-banner{background:linear-gradient(118deg,var(--accent-deep),var(--accent-dark));color:#fff}
.decision-banner h2{margin:0 0 8px;color:#fff}
.decision-banner p{margin:0;max-width:640px;color:#dfece2}
.decision-banner .banner-actions{display:flex;gap:10px;flex-wrap:wrap}
.decision-banner .btn{background:#fff;color:var(--accent-dark)}
.decision-banner .btn.ghost{background:transparent;color:#fff;border-color:rgba(255,255,255,.55)}

/* ---------- trust ---------- */
.trust-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;margin:0 0 8px}
.trust-card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px;border-top:4px solid var(--accent)}
.trust-card b{font-family:var(--serif);font-size:17px;display:block;margin-bottom:7px}
.trust-card p{margin:0;color:var(--muted);font-size:14px}
.desk-intro{margin:6px 0 22px}
.desk-intro h2{margin:0 0 10px;font-size:clamp(24px,3.4vw,34px)}

/* ---------- research desk boxes ---------- */
.tldr{background:var(--okbg);border:1px solid #cfe4d2;border-left:5px solid var(--ok);border-radius:12px;padding:16px 20px;margin:0 0 24px}
.tldr-h{margin:0 0 8px;font-weight:800;font-family:var(--serif);font-size:16px}
.tldr ul{margin:0}
.article-sec{margin:0 0 26px;max-width:860px}
.article-sec h2{margin:26px 0 10px}
.article-sec p{margin:0 0 13px;max-width:80ch}
.vbox{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 20px;margin:0 0 18px;max-width:900px}
.vbox.ok{border-color:#cfe4d2;border-left:5px solid var(--ok);background:var(--okbg)}
.vbox.warn{border-color:#f0dfb6;border-left:5px solid var(--warn);background:var(--warnbg)}
.vbox .box-h{margin:0 0 8px;font-weight:800;font-family:var(--serif);font-size:15.5px}
.vbox .box-sub{margin:10px 0 6px;font-weight:700;font-size:13px;color:var(--muted)}
.vbox ul.findings{margin:0}
.adisclose{background:var(--infobg);border:1px solid #cfdff0;border-radius:10px;padding:12px 16px;margin:22px 0;font-size:13.5px;color:#2c4a68}
.adisclose p{margin:0}

/* ---------- decision center legacy ---------- */
.decision-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}
.decision-card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:17px;box-shadow:0 1px 3px rgba(36,41,31,.05)}
.decision-card h3{margin:0 0 8px;font-size:16px}.decision-card p{margin:7px 0}.decision-card .status{font-size:12px;color:var(--muted);font-weight:700;text-transform:uppercase;letter-spacing:.06em}
.decision-card select{width:100%;padding:9px;border:1px solid #c9c3b0;border-radius:7px;background:#fff;color:var(--ink);font:inherit;margin-top:7px}
.decision-tools{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:12px 0 20px}.decision-tools button{background:var(--accent-dark);color:#fff;border:0;border-radius:7px;padding:9px 13px;font:inherit;cursor:pointer}.decision-tools output{color:var(--muted);font-size:13px}
.suggestion{border-left:4px solid var(--accent);padding:4px 0 4px 14px;margin:16px 0}.suggestion h3{margin:0 0 5px;font-size:17px}.suggestion p{margin:5px 0}

/* ---------- tiles (dashboard sections) ---------- */
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}
.tile{display:block;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:17px;text-decoration:none;color:var(--ink);box-shadow:0 1px 3px rgba(36,41,31,.05)}
.tile:hover{border-color:var(--accent);color:var(--ink)}
.tile b{display:block;margin-bottom:5px;color:var(--accent-dark);font-family:var(--serif);font-size:16.5px}
.tile span{color:var(--muted);font-size:13px}

/* ---------- tables ---------- */
.table-wrap{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:12px;margin:0 0 20px;box-shadow:0 1px 3px rgba(36,41,31,.05)}
table{border-collapse:collapse;width:100%;font-size:14px}
th,td{text-align:left;padding:10px 13px;border-bottom:1px solid var(--line-soft);vertical-align:top}
th{background:var(--grey);font-size:11.5px;text-transform:uppercase;letter-spacing:.06em;color:#565b4e;position:sticky;top:0;font-family:var(--sans)}
tr:last-child td{border-bottom:none}
tbody tr:hover td{background:#faf7ee}
td a{word-break:break-word}
.badge{display:inline-block;padding:2.5px 9px;border-radius:999px;font-size:12px;font-weight:700;white-space:nowrap}
.badge.unv{background:var(--warnbg);color:var(--warn)}
.badge.ok{background:var(--okbg);color:var(--ok)}
.badge.bad{background:var(--badbg);color:var(--bad)}
.badge.warn{background:var(--warnbg);color:var(--warn)}
.badge.info{background:var(--infobg);color:var(--info)}
.badge.muted{background:var(--grey);color:var(--muted)}
.flagid{font-weight:700;text-decoration:none;margin-right:4px;white-space:nowrap}
ul.findings{padding-left:20px;margin:0}
ul.findings li{margin:0 0 8px}
<<<<<<< HEAD
.callout{border-left:4px solid var(--bad);background:var(--badbg);padding:12px 14px;border-radius:6px;margin:0 0 18px}
.callout.ok{border-color:var(--ok);background:var(--okbg)}
.callout p{margin:0}
.promptbox{background:#101c2e;color:#e7eef8;border-radius:12px;padding:20px 22px;overflow-x:auto;font:13px/1.65 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;white-space:pre-wrap;word-break:break-word;margin:0 0 18px}
.promptbox b{color:#ffd9c2}

@media (max-width:640px){main{padding:16px 12px}.topbar{padding:10px 12px}}
"""

=======
.sitemap{columns:2;column-gap:34px;padding-left:20px;margin:0 0 8px}
@media (max-width:720px){.sitemap{columns:1}}
.sitemap li{margin:0 0 6px;break-inside:avoid}
.sitemap-details summary{cursor:pointer;font-weight:650;font-family:var(--serif);font-size:16px;color:var(--accent-dark);padding:9px 0}
.sitemap-details[open] summary{margin-bottom:10px}
>>>>>>> origin/main

/* ---------- footer ---------- */
footer{background:var(--accent-deep);color:#c9d6c6;margin-top:34px;padding:30px 22px 34px;font-size:13px}
.foot-grid{max-width:1180px;margin:0 auto;display:grid;grid-template-columns:1.5fr 1fr;gap:26px;align-items:start}
footer .disclosure{color:#fff;margin:0 0 10px}
footer p{margin:0 0 9px;max-width:92ch}
.foot-disclaimer{color:#a9bda9;font-size:12px}
.foot-links{display:flex;gap:8px 16px;flex-wrap:wrap;justify-content:flex-end;align-content:start}
footer a{color:#e4e9dc}
footer .small{color:#a9bda9;margin-top:6px;max-width:1180px}
@media (max-width:720px){.foot-grid{grid-template-columns:1fr}.foot-links{justify-content:flex-start}}
@media (max-width:640px){main{padding:18px 14px 36px}.topbar{padding:10px 12px}}
@media print{.topbar,.disclose{display:none}footer{background:#fff;color:#222}.hero{box-shadow:none}}
'''
def count_verified(field: str) -> int:
    return sum(1 for p in PRODUCTS if p.get(field) is not None)


def sev_count(level: str) -> int:
    return sum(1 for f in FLAGS if f["severity"] == level)


N = len(PRODUCTS)


# ---------------------------------------------------------------- Dashboard

def reverify_table() -> str:
    """Rows re-checked on 2026-11-14. Source ids resolve through sources.json."""
    rows = [
        ("The three submitted identifiers are 9 characters, not 10", "Confirmed",
         "Each id counted: B04G1MEwY=9, B02NbDxp3=9, B00hJ57DV=9. Amazon defines an ASIN as a 10-character alphanumeric id.", ["S31", "S08"]),
        ("amazon.com/dp/&lt;id&gt; returns Page Not Found for all three", "Confirmed",
         "All three fetched 2026-11-14; each returned Amazon&rsquo;s &ldquo;Page Not Found&rdquo; page.", ["S08", "S09", "S10"]),
        ("Each link.amazon short link opens a different real listing", "Confirmed",
         "B04G1MEwY&rarr;B0CDY277D3 (CHEFMAN 6 Qt dual basket), B02NbDxp3&rarr;B09B7SB46R (Emeril Lagasse 26QT), B00hJ57DV&rarr;B08DKYBTPH (Chefman TurboFry 8 Qt). Same three targets as 2026-11-13.", ["S11", "S12", "S13", "S14", "S15", "S16"]),
        ("Operating Agreement &sect;5 disclosure wording", "Confirmed verbatim",
         "&ldquo;As an Amazon Associate I earn from qualifying purchases.&rdquo; Header still reads Updated: October 15, 2025. Schedule 1 still lists the United States / amazon.com only.", ["S01"]),
        ("Participation Requirements 6(t), 6(w), 6(y), 2(b) and CIS 2(e)", "Confirmed verbatim",
         "Star-rating and review display limited to API-sourced data; link shorteners must not obscure an Amazon destination; no price tracking or alerting; prices/availability only if Amazon serves them or via the API; purchases via a Redirecting Link are disqualified.", ["S02", "S30"]),
        ("PA-API 5 is deprecated; Creators API is the successor", "Confirmed",
         "Deprecation notice re-read: PA-API 5 calls return HTTP 403 AccessDeniedException. Creators API prerequisites include at least 10 qualifying sales in the past 30 days.", ["S05", "S04"]),
        ("IP License: no ML training on Program Content; API use needs prior written approval for analysis", "Confirmed verbatim",
         "&sect;1 bars using Program Content to develop or improve LLMs or ML models; &sect;2(e) bars aggregating, analyzing, extracting or repurposing Product Advertising Content without express prior written approval; Agent Terms &sect;4 require an &ldquo;Agent/[name]&rdquo; user agent.", ["S02"]),
        ("Commission Table 1 (Standard) and Table A (Onsite) are readable without a sign-in", "Corrected",
         "The earlier site text implied all rate data was sign-in gated. Only /help/operating/schedule is gated (and it returns a per-account custom rate card). Table 1 and Table A render publicly. See V-F1; per-product rates remain blank.", ["S25", "S26", "S03"]),
        ("ASIN is a 10-character identifier", "Confirmed",
         "Creators API GetItems, ItemIdType parameter, quoted verbatim; the same 10-character rule is stated on Amazon&rsquo;s own selling blog (S45, read 2026-11-14).", ["S31", "S45", "S08"]),
        ("FTC disclosure standard", "Confirmed, source updated",
         "The 2019 brochure is still live but the Endorsement Guides were revised in 2023; the current FTC topic hub is cited alongside it.", ["S07", "S24"]),
    ]
    out = []
    for claim, verdict, note, srcs in rows:
        cls = "bad" if verdict.startswith("Corrected") else "ok"
        out.append([claim, badge(verdict, cls), note, src_links(srcs)])
    return table(["Claim re-checked", "Result", "What was observed on 2026-11-14", "Source"],
                 out, "reverify")



SITEMAP_GROUPS = [
    # Added by session 145b8df7 (2026-11-16): the read/ editorial layer.
    ("The Crisp Report (read/)", [
        ("read/index.html", "The Crisp Report: start here"),
        ("read/compare.html", "The 13-attribute comparison"),
        ("read/buying-guide.html", "The five-question buying guide"),
        ("read/capacity.html", "Capacity, explained"),
        ("read/cleaning.html", "Cleaning and care"),
        ("read/features.html", "Feature claims, read carefully"),
        ("read/listing-titles.html", "How to read a listing title"),
        ("read/bestseller.html", "Best sellers, point in time"),
        ("read/getting-paid.html", "How getting paid works"),
        ("read/method.html", "The method"),
        ("read/category/air-fryers.html", "Category hub: Air Fryers"),
    ]),
    # Added by integration session 59d84c55 (2026-11-16): the reader-facing site.
    ("Marketing site", [
        ("site/index.html", "Marketing site: start here"),
        ("site/products.html", "Marketing site: the three air fryers"),
        ("site/guides/index.html", "Marketing site: buying guides"),
        ("site/evidence.html", "Marketing site: how we know"),
        ("site/decisions.html", "Marketing site: suggestions &amp; decisions"),
        ("site/flagged.html", "Marketing site: flagged for review"),
        ("site/front-door.html", "Marketing site: where the rest lives"),
    ]),
    ("Overview", [
        ("executive-summary.html", "Executive summary"),
        ("dashboard/index.html", "Full audit dashboard (16 pages)"),
        ("executive-summary/index.html", "Audit build: Executive summary"),
    ]),
    ("Research", [
        ("products.html", "Products"),
        ("air-fryers.html", "Category: Air Fryers"),
        ("category/air-fryers.html", "Category mirror: Air Fryers"),
        ("pricing.html", "Pricing &amp; commission"),
        ("reviews.html", "Reviews &amp; competition"),
        ("products/index.html", "Audit build: Products"),
        ("niches/index.html", "Audit build: Niches"),
        ("pricing/index.html", "Audit build: Pricing"),
        ("commission/index.html", "Audit build: Commission"),
        ("reviews/index.html", "Audit build: Reviews"),
    ]),
    ("Marketing output", [
        ("decision-center.html", "Decision Center: open questions and suggestions"),
        ("marketing/index.html", "Marketing hub"),
        ("marketing/briefs.html", "Marketing briefs"),
        ("marketing/comparison.html", "Comparison article"),
        ("marketing/buying-guide.html", "Buying guide"),
        ("marketing/product-1-chefman-6-quart-dual-basket.html", "Product brief 1"),
        ("marketing/product-2-emeril-lagasse-26qt-french-door.html", "Product brief 2"),
        ("marketing/product-3-chefman-8-quart-turbofry.html", "Product brief 3"),
        ("content-topics.html", "Content topics"),
        ("suggestions.html", "Suggestions &amp; decisions"),
        ("content.html", "Content &amp; compliance"),
        # Added by session 757efebc (2026-11-16).
        ("design-brief.html", "Design brief and prompt pack"),
        ("decision-queue.html", "Review console: proposals and open questions"),
        ("campaigns.html", "Campaigns &amp; tracking"),
        ("content/index.html", "Audit build: Content"),
        ("campaigns/index.html", "Audit build: Campaigns"),
    ]),
    ("Governance", [
        ("sources.html", "Sources"),
        ("sources/index.html", "Audit build: Sources"),
        ("verification.html", "Verification log"),
        # Added by integration session 3ead7ac8 (2026-11-14) alongside the dashboard tile.
        ("sessions/3ead7ac8/index.html", "Verification (session 3ead7ac8)"),
        # Added by session 25513d33 (2026-11-14) alongside the dashboard tile.
        ("sessions/25513d33/index.html", "Verification (session 25513d33)"),
        ("requirements/index.html", "Requirements traceability"),
        ("repo-review/index.html", "Repository review"),
        ("compliance/index.html", "Compliance register"),
        ("agent-terms/index.html", "Agent terms"),
        ("methodology/index.html", "Methodology"),
    ]),
    ("Open items", [
        ("flagged.html", "Flagged for review (flat pages)"),
        ("flagged/index.html", "Flagged for review (audit build)"),
    ]),
    ("Kept for provenance (not current)", [
        ("docs/index.html", "2026-11-13 /docs/ build"),
        ("sessions/3c886b62/index.html", "Session 3c886b62 archive"),
        ("sessions/03bbd050/index.html", "Session 03bbd050 archive"),
    ]),
]


def build_sitemap_html() -> str:
    # Rendered as link lists, not a table: this site's rule is that every *table* row carries a
    # source link or a flag, and a navigation entry has neither. Keeping it out of a table keeps
    # the row-provenance check honest instead of teaching it to ignore rows.
    out = []
    for group, items in SITEMAP_GROUPS:
        links = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in items)
        out.append(f'<h3>{group}</h3><ul class="sitemap">{links}</ul>')
    return "".join(out)


def build_index() -> None:
    """Landing page, rebuilt 2026-11-16 (session 5a56c084).

    Implements the unblocked subset of the published design proposals
    (suggestions.html): SUG-01 hero and product-led structure, SUG-06 trust
    section, SUG-08 point-in-time trend module. The decision log on
    suggestions.html records what was implemented, deferred or left blocked.
    Every number below is computed from data/*.json; every Amazon link is a
    labelled source link; no price, rating or review count appears anywhere.
    """
    stats = [
        ("Product links submitted", str(N), ""),
        ("Submitted links with a confirmed ASIN", f"{count_verified('asin')} of {N}", "bad"),
        ("Prices verified", f"{count_verified('price')} of {N}", "warn"),
        ("Commission rates verified", f"{count_verified('commission_rate')} of {N}", "warn"),
        ("Critical flags open", str(sev_count("Critical")), "bad"),
        ("Official sources cited", str(len(SOURCES)), ""),
    ]
    stat_html = "".join(
        f'<div class="stat {k}"><div class="n">{e(v)}</div><div class="l">{e(l)}</div></div>'
        for l, v, k in stats
    )
<<<<<<< HEAD
    tiles = [
        # Added by integration session 59d84c55 (2026-11-16): leads with the reader-facing
        # marketing site. The audit tiles below it are unchanged.
        ("site/index.html", "Marketing site (new)",
         "The reader-facing site: three air fryers compared on what their listings state, buying "
         "guides, the source register, and a decision board where each proposal can be accepted, "
         "rejected or deferred before anything is implemented."),
        ("read/index.html", "Marketing site — The Crisp Report",
         "Six sourced articles, a 13-attribute comparison, a five-question buying guide with an FAQ, "
         "an Air Fryers category hub and a method page. Same verified data as this dashboard; "
         "a second reader-facing surface, parallel to <a href=\"site/index.html\">/site/</a> (see Z14-F-04)."),
        ("executive-summary.html", "Executive summary", "Bottom line, findings, what was built, what is blocked."),
        ("products.html", "Products", "The 3 submitted links, identifier checks, redirect results."),
        ("pricing.html", "Pricing &amp; commission", "Price and commission fields, plus the verified commission rules."),
        ("reviews.html", "Reviews &amp; competition", "Ratings and competitor fields, a dated category benchmark, plus the verified review rules."),
        ("content.html", "Content &amp; compliance", "Article status and the Associates and FTC checklist."),
        ("decision-center.html", "Decision Center", "Sourced answers, open questions, ranked suggestions and reviewable paths."),
        # Added by integration session 3d359c23 (2026-11-14): the editorial topic plan.
        ("content-topics.html", "Content topics",
         "The planned article topics, the verified fact each one is built on, and what it may not state."),
        # Added by session 4f83ee7b (2026-11-15): design and marketing proposals plus the
        # open questions to answer before any of them is implemented.
        ("suggestions.html", "Suggestions &amp; decisions",
         "Design and marketing proposals for the affiliate site, the open questions to answer "
         "before a decision, and how to discover the missing information. Proposals only — "
         "nothing here is implemented yet."),
        ("campaigns.html", "Campaigns &amp; tracking", "Click and conversion ledger. Empty until data exists."),
        # Added by session 757efebc (2026-11-16): the redesign brief and the review
        # console, so both are reachable from the landing page as well as the nav.
        ("design-brief.html", "Design brief",
         "Why the site reads as generated, and the prompt, design system, editorial plan "
         "and anti-slop checklist to fix it. Proposals only."),
        ("decision-queue.html", "Review console",
         "Every proposal with a recommendation and decision state, plus what the project "
         "has, what it does not have, and how to get it."),
        ("flagged.html", "Flagged for review", "Every irregularity and unverified item, with its source links."),
        ("sources.html", "Sources", "The official source registry with retrieval status."),
        # Added by integration session edbd56a1 (2026-11-14): these sections were in the
        # navigation but missing from the dashboard tiles, so a visitor landing on the
        # dashboard could not see them.
        ("air-fryers.html", "Category: Air Fryers",
         "The one verified category: browse path and a six-position bestseller benchmark."),
        ("marketing/index.html", "Marketing",
         "Product briefs, comparison and buying guide. No prices or ratings are published."),
        ("verification.html", "Verification log",
         "One row per published claim, with the wording its official page carries."),
        # Added by integration session 3ead7ac8 (2026-11-14): the page was in the top
        # navigation but not in the dashboard tiles, so it was invisible from the landing page.
        ("sessions/3ead7ac8/index.html", "Verification (session 3ead7ac8)",
         "30 load-bearing claims re-read from the official pages on 2026-11-14, each linked to "
         "the page it came from, plus the fields deliberately left blank and why."),
        # Added by session 25513d33 (2026-11-14): same reason as the tile above. This record
        # re-fetches and re-reads every load-bearing claim independently of the one above.
        ("sessions/25513d33/index.html", "Verification (session 25513d33)",
         "Independent re-fetch of all three submitted links and 12 policy and disclosure "
         "statements, re-read verbatim on 2026-11-14, each row linked to the page it came from."),
        # Added by session ab3ed329 (2026-11-16): same reason as the tile above.
        ("sessions/ab3ed329/index.html", "Verification (session ab3ed329)",
         "Live re-read of the three short links, their destination listings, the Operating Agreement, "
         "Program Policies 2(a), 2(b), 6(g), 6(t), 6(v), 6(w), 6(y), the commission table and the "
         "Creators API ASIN rule on 2026-11-16, plus a sweep that removed observed price and rating values from public data (AB-F-01)."),
        # Added by session 5b425c74 (2026-11-16): same reason as the tiles above. This record
        # independently re-fetches the three links and re-reads 22 policy, commission, API and
        # FTC statements verbatim on 2026-11-16.
        ("sessions/5b425c74/index.html", "Verification (session 5b425c74)",
         "Independent re-fetch of all three submitted links, both commission rate tables, the "
         "Operating Agreement, Program Policies, Creators API and FTC pages on 2026-11-16, each "
         "row linked to the official page it came from."),
        ("docs/index.html", "Archived 2026-11-13 build (/docs/) — flagged",
         "An earlier build, kept for provenance. It still displays price and star-rating cells that "
         "this site's rule and Amazon's policy prohibit; see I-F-02 on the Flagged for review page. "
         "Do not treat its figures as current."),
    ]
    tile_html = "".join(
        f'<a class="tile" href="{h}"><b>{t}</b><span>{d}</span></a>' for h, t, d in tiles
=======

    brief_slugs = {
        "P1": "marketing/product-1-chefman-6-quart-dual-basket.html",
        "P2": "marketing/product-2-emeril-lagasse-26qt-french-door.html",
        "P3": "marketing/product-3-chefman-8-quart-turbofry.html",
    }
    one_lines = {
        "P1": "Two independent 3-quart baskets with a sync-finish control, auto shutoff and easy-view windows, in a 6-quart dual-basket oven format.",
        "P2": "A 26-quart french-door multi-function oven: air fryer and convection cooking with 24 one-touch presets and six accessories included.",
        "P3": "An 8-quart single-basket fryer with a TurboFry 4-in-1 function set (air fry, bake, dehydrate, frozen) and an XL nonstick dishwasher-safe basket.",
    }
    product_cards = []
    for p in PRODUCTS:
        ro = p["redirect_observed"]
        title = ro.get("page_title", "")
        title = title.replace("Amazon.com: ", "").replace(" : Home & Kitchen", "")
        product_cards.append(
            f'<div class="pcard">'
            f'<span class="pcard-brand">{e(ro.get("brand", ""))} &middot; {e(ro.get("capacity", ""))}</span>'
            f"<b>{e(title)}</b>"
            f'<p class="spec">{e(one_lines.get(p["id"], ""))}</p>'
            f'<div class="pcard-actions">'
            f'<a class="btn" href="{e(brief_slugs.get(p["id"], "marketing/index.html"))}">Read the brief</a>'
            f'<a class="btn ghost" href="https://www.amazon.com/dp/{e(ro.get("page_id", ""))}" '
            f'target="_blank" rel="noopener noreferrer">Official listing</a>'
            f"</div>"
            f'<p class="small">Observed destination of {e(p["submitted_url"])}, re-fetched '
            f'2026-11-16 ({src_links([ro["source"]])} &middot; {src_links([ro.get("title_source", ro["source"])])}). '
            'Not confirmed as the submitted product <a class="flagid" href="flagged.html#FLG-002">FLG-002</a>. '
            'Price, rating and review cells are blank by policy until an approved Amazon data path is connected.</p>'
            f"</div>"
        )

    article_cards = "".join(
        f'<a class="acard" href="articles/{e(a["slug"])}">'
        f'<span class="acard-meta">{e(ARTICLES["desk"])} &middot; {e(ARTICLES["published"])}'
        f' &middot; {a["reading_minutes"]} min read</span>'
        f"<b>{e(a['title'])}</b>"
        f"<span>{e(a['dek'])}</span>"
        f'<span class="acard-go">Read the article &rarr;</span></a>'
        for a in ARTICLES["articles"]
>>>>>>> origin/main
    )

    sitemap_html = build_sitemap_html()
    reverify_html = reverify_table()
    body = f"""
<section class="hero">
  <p class="eyebrow">Zone3 &middot; Evidence-first air-fryer research</p>
  <h2>Air-fryer research you can actually check.</h2>
  <p>Three Amazon listings, every published claim traced to the official page it came from, and every gap marked instead of papered over. Browse the comparison, read the Research Desk, and see exactly what was verified &mdash; and what was not.</p>
  <div class="hero-actions">
    <a href="marketing/comparison.html">Compare the three listings</a>
    <a href="articles/index.html">Read the Research Desk</a>
    <a href="verification.html">How we verify</a>
  </div>
</section>
<div class="callout">
  <p><strong>Research status (re-verified 2026-11-16):</strong> all three supplied Amazon short links resolve to live product listings. The nine-character tokens are short-link IDs, not ASINs; direct /dp/&lt;token&gt; Page Not Found responses are expected and do not indicate short-link failure. Product identities are documented with official listing links, and whether they match the requester's intent remains open for the owner (<a class="flagid" href="flagged.html#FLG-002">FLG-002</a>). Static price offers and unverified analytics are not published.</p>
</div>
<div class="grid">{stat_html}</div>

<h2>The three listings this site tracks</h2>
<p class="small">Each card is the observed destination of one submitted link, with the attribute brief built from its listing title. Every Amazon link on this page is a labelled source link: no conversion-oriented CTA is published while the Associates tag every Special Link must carry is unknown (open question Q1 on the Decision Center).</p>
<div class="product-cards">{product_cards}</div>

<h2>From the Research Desk</h2>
<div class="acards">{article_cards}</div>
<p class="small more-link">More from the desk: <a href="marketing/buying-guide.html">the buying guide</a> &middot; <a href="marketing/comparison.html">the attribute-by-attribute comparison</a> &middot; <a href="content-topics.html">the full twelve-topic plan</a></p>

<section class="kitchen-now">
  <div>
    <p class="eyebrow">In the kitchen now</p>
    <h2>What the category's official shelf looks like.</h2>
    <p>Amazon publishes one official popularity surface for this category: the Best Sellers page for Air Fryers, browse node 17659096011. Our benchmark is a point-in-time read of that page &mdash; six positions, captured 2026-11-14 &mdash; with the date attached, because ranks move and a rank without a date is decoration, not data.</p>
    <p class="small">Category breadcrumb as served by the three destination listings (captured 2026-11-16 by session f132f462, kept from their trending section): Home &amp; Kitchen &gt; Kitchen &amp; Dining &gt; Small Appliances &gt; Fryers &gt; Air Fryers &middot; node 17659096011 &middot; {src_links(["S14", "S15", "S16"])}</p>
  </div>
  <a class="btn" href="air-fryers.html">See the dated benchmark</a>
</section>

<h2>Why this site is different</h2>
<div class="trust-grid">
  <div class="trust-card"><b>Every value has a source</b><p>Each published cell traces to an official page &mdash; amazon.com, Amazon's Associates documentation, or ftc.gov &mdash; linked in the table itself. <a href="sources.html">The source register &rarr;</a></p></div>
  <div class="trust-card"><b>Blank beats invented</b><p>Prices, ratings and review counts stay empty until an approved Amazon data path serves them. Empty cells are a policy, not an oversight. <a href="flagged.html">What is open &rarr;</a></p></div>
  <div class="trust-card"><b>Verified in the open</b><p>Every load-bearing claim has been re-read from its official page by independent sessions &mdash; 2026-11-14 and again 2026-11-16 &mdash; with the observations published each time. <a href="verification.html">The verification log &rarr;</a></p></div>
</div>

<section class="decision-banner">
  <div>
    <p class="eyebrow">Decision Center</p>
    <h2>Ten questions decide what ships next.</h2>
    <p>The design and marketing proposals for this site are published, with the ten owner questions that must be answered before each one is implemented and the ways to discover the missing information. The decision log records what has now been implemented, deferred or left blocked &mdash; and nothing blocked was implemented.</p>
  </div>
  <div class="banner-actions"><a class="btn" href="decision-center.html">Open the Decision Center</a><a class="btn ghost" href="suggestions.html">Review the suggestions</a></div>
</section>

<h2>Site map</h2>
<details class="sitemap-details">
<summary>Every page published from this repository</summary>
<p>Every page that is published from this repository, so nothing here is reachable only by guessing a URL.
Pages kept for provenance are listed separately and are marked as such; the <code>/docs/</code> set and the
<code>/sessions/</code> archives are published because they are committed, not because they are current, and
they are <a href="flagged.html#I-F-02">flagged for review</a>.</p>
{sitemap_html}
</details>

<h2>Re-verification record</h2>
<p>Every load-bearing claim on the flat pages was checked again against the official page it cites &mdash; on 2026-11-14 by session b8beb448, and the three submitted links, the three destinations and the policy pages again on 2026-11-16 by session <a href="sessions/5a56c084/index.html">5a56c084</a>. The result, per claim, is below. Nothing in this table was inferred; each row links the page that was read.</p>
{reverify_html}
<p class="small">Where a row says <em>corrected</em>, the earlier text on this site was wrong or overstated and has
been rewritten in the same commit that added the row. Corrections are listed on the
<a href="flagged.html">Flagged for review</a> page as V-F1 and V-F2, so the change is auditable rather than silent.</p>
"""
    page("index.html", "Home", body,
         lead=f"Status as of {BUILT}. The site shows verified data only. Blank cells are unverified and listed on the Flagged for review page.",
         description="Zone3 Air Fryer Research Desk: comparisons, buying guides and affiliate-programme research for three Amazon air-fryer listings, with every published claim linked to the official page it came from. Prices and ratings stay blank until an approved Amazon data path is connected.")


# ---------------------------------------------------------- Executive summary
def build_exec() -> None:
    body = f"""
<section class="card">
  <h2>Bottom line</h2>
  <p><strong>Headline:</strong> the three submitted short links each open a live Amazon product page. Their nine-character codes are not ASINs, and the destinations are not confirmed as the submitted products {flag_links(['FLG-001', 'FLG-002', 'FLG-027'])}. Product name, brand, price and rating for the submitted links are left blank.</p>
  <p>Price display, API-derived reviews, link-model-specific earnings, traffic, clicks, conversions and niche profitability are not represented as live or established. Point-in-time observations are kept in the research log. Any value not confirmed through an eligible official route remains blank and is flagged.</p>
</section>

<section class="card">
  <h2>Key findings</h2>
  <ul class="findings">
    <li><strong>The three short links each open a live Amazon product page.</strong> The destinations were read on 2026-11-13 and 2026-11-14 {src_links(['S11', 'S12', 'S13', 'S14', 'S15', 'S16'])}. The nine-character codes are not in the 10-character ASIN form {src_links(['S06'])}, and the direct amazon.com/dp pages for them return Page Not Found {src_links(['S08', 'S09', 'S10'])}. The destinations are not confirmed as the submitted products {flag_links(['FLG-001', 'FLG-002', 'FLG-027'])}.</li>
    <li><strong>The short links resolve to other products.</strong> Each link ended on a different product page, with the parameters <code>lv=shuf</code> and <code>plpRedirect=mhFallback</code>. The mapping was the same on two fetches on 2026-11-13 and again on 2026-11-14. These are recorded as observed only {flag_links(['FLG-002'])} {src_links(['S11', 'S12', 'S13'])}.</li>
    <li><strong>Applying the shortener rules to link.amazon needs a judgement call.</strong> The policies say a shortener must not make the Amazon destination unclear {src_links(['S02'])} (PF-06), a link must not be cloaked or obscured (6(v)), and purchases through a link that sends users on indirectly, without an affirmative click, are disqualified as a Redirecting Link {src_links(['S30'])} (CIS 2(e)). No document names <code>link.amazon</code>; what its redirects actually do is a behaviour observation, and it has to be tested in a logged-in Associates account {flag_links(['FLG-003'])}.</li>
    <li><strong>Category rates are public; per-product rates are not assignable.</strong> Amazon&rsquo;s Standard Commission Income Statement, Table 1, is readable without a sign-in (Kitchen 4.50&nbsp;%, Home 3.00&nbsp;%, All Other Categories 4.00&nbsp;%) {src_links(['S25', 'S26'])}, and was re-read on 2026-11-14. The per-product rate cannot be stated, because the listing&rsquo;s category is unverified and the account-specific rate card route redirects to sign-in {src_links(['S03'])} {flag_links(['FLG-005'])}.</li>
    <li><strong>A category page now exists.</strong> <a href="air-fryers.html">Air Fryers</a> shows the verified category path and a six-position bestseller benchmark, each row linked to its official page {src_links(['S43'])}. Prices and ratings are withheld under the display rules {flag_links(['FLG-022', 'FLG-025'])}.</li>
    <li><strong>Automated product data needs Creators API access.</strong> The official prerequisite is &ldquo;at least 10 qualifying sales within the past 30 days&rdquo; {src_links(['S04'])}. Prices and reviews may be shown only through a Special Link or the API {src_links(['S02'])} (PF-04, PF-05, PF-44, PF-45) {flag_links(['FLG-006', 'FLG-022', 'FLG-023'])}.</li>
    <li><strong>The AI layer needs written approval from Amazon.</strong> The Creators API terms bar analysing, aggregating or repurposing its data, and bar using Program Content to develop or train machine learning or language models, without express prior written approval {src_links(['S02'])} (PF-23, PF-24, PF-25) {flag_links(['FLG-016'])}.</li>
    <li><strong>Eligibility for a Norway-based owner is not stated.</strong> Schedule 1 of the Operating Agreement lists only the United States site, amazon.com {src_links(['S01'])} (PF-35) {flag_links(['FLG-015'])}.</li>
    <li><strong>PA-API 5 is deprecated.</strong> The official notice says it is being replaced by the Creators API and that calls now return HTTP 403 <code>AccessDeniedException</code> {src_links(['S05'])} (PF-17), re-read on 2026-11-14. Another session branch cites PA-API 5 as the sanctioned source {flag_links(['FLG-007'])}.</li>
    <li><strong>Disclosure is on every page.</strong> The required wording is quoted from the Operating Agreement, Section 5 {src_links(['S01'])} (PF-01). Placement for FTC purposes still needs owner review {flag_links(['FLG-013'])}.</li>
  </ul>
</section>

<section class="card">
  <h2>What was built</h2>
  <ul class="findings">
    <li>A GitHub Pages site (this site) with a landing dashboard and category pages: Products, Pricing &amp; commission, Reviews &amp; competition, Content &amp; compliance, Campaigns &amp; tracking.</li>
    <li>A Flagged for review page with {len(FLAGS)} items, each with its evidence sources and the action needed.</li>
    <li>The earlier session&rsquo;s site from PR #1 is merged in. Its scripts, data and HTML are archived under <code>archive/26634cd5/</code>, and its old <code>analysis.html</code> and category URLs redirect to the pages that replace them.</li>
    <li>A Sources page that lists each official page used, its retrieval status, and what it supports.</li>
    <li>A data layer (<code>data/*.json</code>) with a generator (<code>scripts/build_site.py</code>) and a checker (<code>scripts/check_site.py</code>). The checker fails if a table row has no official source link, or if a value appears without a source.</li>
    <li><strong>An independent re-verification pass on 2026-11-14</strong> (this session): {len(SRC['sources'])} official sources, every load-bearing claim re-fetched and compared. Two earlier statements were found overstated and corrected rather than quietly dropped &mdash; see V-F1 and V-F2 on the Flagged for review page.</li>
  </ul>
</section>

<section class="card">
  <h2>What is not done, and why</h2>
  <ul class="findings">
    <li><strong>Product research, niche identification, competition and commission-potential analysis.</strong> These need product data, which needs verified identifiers (FLG-001) and Creators API access (FLG-006). Nothing was estimated.</li>
    <li><strong>SEO articles, comparisons and buying guides.</strong> Product claims must be accurate (PF-10), and the first-hand experience the FTC describes (PF-21) has not happened. These are blocked (FLG-012).</li>
    <li><strong>Click and conversion tracking.</strong> Figures come from the owner&rsquo;s Associates reports. No tag has been supplied (FLG-010), and no reports were available (FLG-011).</li>
    <li><strong>Automated optimisation.</strong> There is no data to optimise. The generator can rebuild the site once verified data is added.</li>
  </ul>
</section>

<section class="card">
  <h2>Owner items (flagged; they do not block the merge)</h2>
  <ul class="findings">
    <li>Give the intended product URL or 10-character ASIN for each of the three products (FLG-001).</li>
    <li>Test each submitted link in a logged-in Associates account and report whether clicks are tracked (FLG-002, FLG-003).</li>
    <li>Confirm which Amazon product category each of the three listings is in, so the public Table 1 rate can be applied to it (FLG-005, FLG-021). The category rates themselves are already published and verified.</li>
    <li>Confirm Associates enrolment and supply the Associates tag, not a password or token (FLG-010).</li>
  </ul>
</section>
"""
    page("executive-summary.html", "Executive summary", body,
         lead="A plain-language summary of what can and cannot be verified today. Each finding links to its official source.")


# -------------------------------------------------------------- Products
def build_products() -> None:
    rows = []
    for p in PRODUCTS:
        ro = p["redirect_observed"]
        d = p["direct_check"]
        rows.append([
            e(p["label"]),
            f'<a href="{e(p["submitted_url"])}" target="_blank" rel="noopener noreferrer">{e(p["submitted_url"])}</a>',
            f'{e(p["link_id"])} <span class="muted">({p["link_id_length"]} chars)</span>',
            val(p["asin"]),
            f'<a href="{e(d["url"])}" target="_blank" rel="noopener noreferrer">{e(d["result"])}</a>',
            f'<a href="{e(ro["final_url"])}" target="_blank" rel="noopener noreferrer">{e(ro["page_id"])}</a> {badge("Not confirmed as submitted", "warn")}',
            val(p["product_name"]),
            e(p["status"]),
            flag_links(p["flags"]),
            src_links(p["sources"]),
        ])
    body = table(
        ["#", "Submitted link", "Identifier (length)", "ASIN", "amazon.com/dp check", "Observed redirect (not used as this product)", "Product name", "Status", "Flags", "Source"],
        rows,
    )
    body += f"""
<section class="card">
  <h2>How to read this table</h2>
  <ul class="findings">
    <li>Each row is one product link from the brief. An identifier is counted only when a product page under that identifier exists and matches it.</li>
    <li>&ldquo;Observed redirect&rdquo; is the page the short link opened on 2026-11-13. It is not treated as the submitted product, because the submitted identifier does not resolve to it.</li>
    <li>Product name, brand, price, rating and availability are blank because they cannot be confirmed (see <a href="pricing.html">Pricing</a> and <a href="reviews.html">Reviews</a>).</li>
  </ul>
</section>
"""
    page("products.html", "Products", body,
         lead="The three product links from the brief, checked line by line against official Amazon pages. Nothing is shown as a verified product until its identifier resolves.")


# ------------------------------------------------------------- Pricing
def build_pricing() -> None:
    rows = []
    for p in PRODUCTS:
        rows.append([
            e(p["label"]),
            val(p["price"]),
            val(p["commission_rate"]),
            badge("Blocked: no product record", "bad") + " " + badge("Listing category not confirmed", "warn"),
            flag_links(["FLG-004", "FLG-005", "FLG-021", "FLG-022"]),
            src_links(["S25", "S02", p["direct_check"]["source"]]),
        ])
    body = "<h2>Price and commission fields</h2>" + table(
        ["Product", "Price", "Commission rate", "Status", "Flags", "Source"], rows)

    rules = [
        ["Commission window (session)", FACTS["PF-12"]["quote"], "A click-to-sale record needs the click time, a 24-hour session, and the 89-day cart window.", src_links(["S02"])],
        ["Cancelled, returned or refunded orders", FACTS["PF-13"]["quote"], "Conversion counts must exclude these orders.", src_links(["S02"])],
        ["Redirecting Links disqualify purchases", FACTS["PF-07"]["quote"], "Relevant to the link.amazon question (FLG-003).", src_links(["S02"])],
        ["Prices shown only via link or API", FACTS["PF-04"]["quote"], "Price cells stay blank until one of these two routes is available.", src_links(["S02"])],
        ["Comparison-price display", FACTS["PF-11"]["quote"], "Any future comparison table must show lowest new and used prices from Amazon.", src_links(["S02"])],
    ]
    rules_html = table(["Rule", "Verified wording (quoted)", "What it means here", "Source"], rules)
    body += f'<h2>Verified commission and pricing rules</h2>{rules_html}'
    ref_rows = [
        ["Kitchen (Standard Commission, Table 1)", "4.50%", "Reference only. Applies only if a listing is in the Kitchen category, which is not verified (FLG-021).", FACTS["PF-38"]["quote"], src_links(["S25"]) + " " + flag_links(["FLG-021"])],
        ["Kitchen (Onsite Commission, Table A)", "1.25%", "Not a rate for links on this site. It applies to Onsite Content used by Amazon within the Amazon Site.", FACTS["PF-39"]["quote"], src_links(["S26"]) + " " + flag_links(["FLG-021"])],
    ]
    body += "<h2>Category reference rates (not product values)</h2>" + table(["Category and table", "Rate", "What it means here", "Verified wording (quoted)", "Source"], ref_rows)
    page("pricing.html", "Pricing &amp; commission", body,
         lead="Price and commission fields are blank. A price can be shown only through an Amazon-served link or the Creators API (FLG-022, FLG-023). The commission rate for a listing is blank until its rate-card category is confirmed (FLG-021). The rules below are verified.")


# ------------------------------------------------------------- Reviews
def build_reviews() -> None:
    rows = []
    for p in PRODUCTS:
        rows.append([
            e(p["label"]),
            val(p["rating"]),
            val(p["review_count"]),
            val(p["competitor_count"]),
            val(p["best_seller_rank"]),
            flag_links(["FLG-004", "FLG-006"]),
            src_links(["S02", "S04", p["direct_check"]["source"]]),
        ])
    body = "<h2>Rating, review and competition fields</h2>" + table(
        ["Product", "Rating", "Review count", "Competing listings", "Best-seller rank", "Flags", "Source"], rows)
    rules = [
        ["Reviews and star ratings", FACTS["PF-05"]["quote"], "Ratings and review counts are blank. They can only come from the API.", src_links(["S02"])],
        ["No inaccurate or misleading product claims", FACTS["PF-10"]["quote"], "Competition statements cannot be made until product data is verified.", src_links(["S02"])],
        ["Original content and third-party material", FACTS["PF-15"]["quote"], "Pages must add analysis to any product data they use.", src_links(["S02"])],
    ]
    body += "<h2>Verified review and content rules</h2>" + table(
        ["Rule", "Verified wording (quoted)", "What it means here", "Source"], rules)
    body += build_benchmark()
    page("reviews.html", "Reviews &amp; competition", body,
         lead="Ratings, review counts and competition data for the submitted links are blank. No review or star rating from Amazon is shown on this site (PF-05). A dated category benchmark is published below from the official Best Sellers page, with prices and ratings withheld by policy.")


# ------------------------------------------------------------- Competition benchmark
def build_benchmark() -> str:
    """Competition benchmark on the Reviews page (integration session ecbfe91b, E-T5).

    Rendered from data/competition.json — the same file as the Air Fryers category page
    (air-fryers.html, session 51fcb80d) so the two views can never drift apart. The data is
    Amazon's official Best Sellers page for Air Fryers (S43), read 2026-11-14; an earlier
    2026-11-13 capture (data/c4e71983-competitors.json) ordered positions 2-3 differently
    (FLG-025), so every rank is a dated observation. Price, star rating and review count are
    withheld by policy (Program Policies 2(b), PF-04/PF-05) and published as flags instead of
    values (FLG-022).
    """
    comp = load("competition.json")
    rows = []
    for b in comp["rows"]:
        rows.append([
            e(b["rank"]),
            f'<a href="{e(b["url"])}" target="_blank" rel="noopener noreferrer" '
            f'title="Official Amazon product page">{e(b["asin"])}</a>',
            e(b["title"]),
            badge("Not displayed (policy)", "warn"),
            badge("Not displayed (policy)", "warn"),
            badge("Not displayed (policy)", "warn"),
            flag_links(["FLG-022", "FLG-025"]),
            src_links(["S43"]),
        ])
    intro = (
        '<div class="callout"><p><strong>How to read this table.</strong> '
        "Same data as the <a href=\"air-fryers.html\">Air Fryers category page</a>, read "
        f'2026-11-14 from Amazon&rsquo;s official Best Sellers page {src_links(["S43"])}; an earlier '
        "2026-11-13 capture ordered positions 2&ndash;3 differently, so ranks are dated observations "
        f'({flag_links(["FLG-025"])}). This is the category of the three <em>observed redirect targets</em>, '
        "which are not confirmed as the submitted products "
        f'{flag_links(["FLG-002"])} &middot; {src_links(["S11"])}&ndash;{src_links(["S13"])}. '
        "Prices, star ratings and review counts are withheld by policy (Program Policies 2(b) and PF-05) "
        f'{src_links(["S02"])} {flag_links(["FLG-022"])}; the captured values stay in '
        "<code>data/c4e71983-competitors.json</code> and <code>data/z3-51fcb80d-snapshot.json</code> "
        "for internal analysis only. Every row links to its official Amazon product page and to the "
        "capture source.</p></div>"
    )
    return intro + "<h2>Competition benchmark &mdash; Air Fryers best sellers (dated snapshot)</h2>" + table(
        ["Rank (2026-11-14)", "ASIN", "Product", "Price", "Rating", "Review count", "Flags", "Source"],
        rows)


# ------------------------------------------------------------- Content
def build_content() -> None:
    rows = []
    for p in PRODUCTS:
        pid = p["id"]
        rows.append([
            e(p["label"]),
            badge("Published", "ok") + ' <a href="marketing/briefs.html">brief</a>',
            badge("Published", "ok") + ' <a href="marketing/comparison.html">comparison</a>',
            badge("Published", "ok") + ' <a href="marketing/buying-guide.html">buying guide</a>',
            "The copy describes the listing this link currently opens, not a product the submitted "
            "code is documented to identify. Product name, price, rating and review count stay "
            "blank (FLG-001, FLG-002, FLG-004).",
            "Planned topics for this product: " + ", ".join(
                t["id"] for t in TOPICS["topics"] if pid in t["products"]) or "&mdash;",
            flag_links(["FLG-002", "FLG-029", "FLG-030"]),
            src_links(["S02", "S07"]),
        ])
    body = "<h2>Content status</h2>" + table(
        ["Product", "SEO product brief", "Comparison", "Buying guide", "What the copy does and does not say",
         "Planned topics", "Flags", "Source"], rows)
    body += (
        '<p class="small"><strong>Correction (session 3d359c23, 2026-11-14).</strong> This table '
        'previously showed &ldquo;Not written&rdquo; for every product. That was true when it was '
        'written and stopped being true when the <code>/marketing/</code> section was published: '
        'three product briefs, a comparison and a buying guide are live and linked from the '
        'navigation. The table now shows what is published. The editorial plan for the remaining '
        'articles is on the <a href="content-topics.html">Content topics</a> page. Recorded as '
        '<a class="flagid" href="flagged.html#3D-F-01">3D-F-01</a>.</p>'
    )

    checklist = [
        ["Disclosure wording", FACTS["PF-01"]["quote"], badge("On every page (footer)", "ok"), src_links(["S01"])],
        ["Disclosure placed where it can be seen", FACTS["PF-20"]["quote"], badge("Owner review needed", "warn") + " " + flag_links(["FLG-013"]), src_links(["S07"])],
        ["Link shorteners must be clear", FACTS["PF-06"]["quote"], badge("Unresolved", "bad") + " " + flag_links(["FLG-003"]), src_links(["S02"])],
        ["No Special Links in print, ebooks or offline use", FACTS["PF-09"]["quote"], badge("None created", "ok"), src_links(["S02"])],
        ["No cloaking or hidden destinations", FACTS["PF-08"]["quote"], badge("Met (no hidden redirects on this site)", "ok"), src_links(["S02"])],
        ["No claims about products not tried", FACTS["PF-21"]["quote"], badge("No experience claimed", "ok"), src_links(["S07"])],
    ]
    body += "<h2>Associates and FTC checklist</h2>" + table(
        ["Requirement", "Verified wording (quoted)", "Status on this site", "Source"], checklist)
    page("content.html", "Content &amp; compliance", body,
         lead="Three product briefs, a comparison and a buying guide are published under /marketing/, "
              "and the editorial plan for the rest is on the Content topics page. The checklist below "
              "records what any content must meet before it is published.")


# ------------------------------------------------------------- Content topics
def build_topics() -> None:
    """The editorial topic plan (session 3d359c23).

    Every row carries the official source of the fact it rests on. Nothing here is
    described as trending, popular or high-converting: no official Amazon endpoint
    publishes those figures to affiliates (FLG-033), so no such claim is made.
    """
    rows = []
    for t in TOPICS["topics"]:
        ready = t["status"] == "ready"
        rows.append([
            e(t["id"]),
            f'<strong>{e(t["title"])}</strong>',
            e(t["intent"]),
            e(t["stage"]),
            e(", ".join(t["products"]) if t["products"] else "Category-wide"),
            e(t["facts"]),
            badge("Ready to draft" if ready else "Blocked: identity unconfirmed",
                  "ok" if ready else "warn"),
            flag_links(t["flags"]) if t["flags"] else "&mdash;",
            src_links(t["sources"]),
        ])
    body = (
        '<div class="callout"><p><strong>What this page is.</strong> The article topics this site '
        'should publish for the three submitted Amazon links, and the reason each one is worth '
        'writing. Every topic is built only on facts printed on an Amazon listing or published in '
        'Amazon&rsquo;s own programme documents, and every row links the page the fact was read from. '
        'The titles below are working SEO titles, not published articles.</p></div>'
        + "<h2>How each topic was derived</h2>"
        + "<ol class=\"findings\">"
        + "".join(f"<li>{e(step)}</li>" for step in TOPICS["method"])
        + "</ol>"
        + "<h2>Editorial topic plan</h2>" + table(
            ["ID", "Working title", "Intent", "Funnel stage", "Products", "Verified facts it is built on",
             "Status", "Flags", "Source"], rows)
        + '<p class="small"><strong>Ready to draft</strong> &mdash; '
        + e(TOPICS["statuses"]["ready"])
        + ' <strong>Blocked: identity unconfirmed</strong> &mdash; '
        + e(TOPICS["statuses"]["blocked"]) + "</p>"
    )

    rules = []
    for t in TOPICS["topics"]:
        for m in t["must_not_state"]:
            rules.append([
                e(t["id"]),
                e(t["title"]),
                e(m["text"]),
                e(m["rule"]),
                src_links([m["source"]]),
            ])
    body += "<h2>What each topic may not state</h2>" + table(
        ["ID", "Topic", "Must not state", "Rule", "Source"], rules)

    pub = []
    for t in TOPICS["topics"]:
        pub.append([
            e(t["id"]),
            f'<a href="{e(t["published"])}">{e(t["published"])}</a>',
            e(t["facts"]),
            src_links(t["sources"]),
        ])
    body += "<h2>Where these facts are already published</h2>" + table(
        ["ID", "Page", "Verified facts the page already carries", "Source"], pub)

    np_rows = []
    for item in TOPICS["not_planned"]:
        np_rows.append([
            e(item["item"]),
            e(item["why"]),
            src_links([item["source"]]),
        ])
    body += "<h2>Topics deliberately not planned</h2>" + table(
        ["Not planned", "Why", "Source"], np_rows)

    body += f"""
<section class="card">
  <h2>Why no topic is called trending</h2>
  <ul class="findings">
    <li>The brief asks for &ldquo;catchy trending articles and topics&rdquo;. Amazon publishes no
      endpoint that gives an affiliate search volume, keyword difficulty, trend direction or
      conversion rate {src_links(['S02'])}; the only official popularity surface is the category
      Best Sellers page, which is point-in-time and moves between captures
      {src_links(['S43'])} (FLG-025, FLG-033).</li>
    <li>So every topic above is anchored to a fact that is printed on the listing itself, and the
      plan says which fact. A topic that cannot be anchored is not written down as if it could.</li>
    <li>Nothing here states a price, a star rating or a review count: Participation Requirements
      2(b) and 6(t) allow those on a site only when Amazon serves the link or they come from the
      Creators API or PA API {src_links(['S02'])} (FLG-022).</li>
    <li>No topic describes the site&rsquo;s own experience of the products: the FTC states you cannot
      talk about your experience with a product you have not tried {src_links(['S07'])}.</li>
  </ul>
</section>
"""
    page("content-topics.html", "Content topics", body,
         lead="The planned article topics for the three submitted links, each anchored to the verified "
              "Amazon fact it is built on, with the rule that governs what it may not say.")


# --------------------------------------------------------- Suggestions & decisions
def build_suggestions() -> None:
    """The suggestions and decision framework (session 4f83ee7b, 2026-11-15).

    Published for review before any change: design and marketing proposals to make the
    site read like a polished marketing affiliate website, the open questions that must
    be answered before a decision, and the ways to discover missing information. Every
    factual row links the official page it was read from; every proposal is labelled as
    a proposal.

    Session 5a56c084 (2026-11-16): a Decision log section is now rendered from each
    suggestion's "implementation" record. Only proposals whose decision is
    "implemented" appear as implemented; blocked proposals stay blocked; open
    questions Q1-Q10 remain unanswered by inference - the log records implementation
    decisions, it does not invent owner inputs.
    """
    s = SUGGESTIONS
    body = (
        '<div class="callout"><p><strong>What this page is.</strong> Design and marketing '
        'proposals for making this site read like a polished marketing affiliate website — '
        'catchy, topic-driven articles, honest trend sections and conversion-ready pages — '
        'together with the questions that must be answered, and the ways to discover the '
        'missing information, before any proposal is implemented. Every statement of fact '
        'below links the official page it was read from; every proposal is labelled '
        '<span class="badge info">Proposal</span> and is not a verified fact. '
        'Session 4f83ee7b published this page for review before any change. The '
        '<strong>Decision log</strong> below records what the follow-up session '
        '(5a56c084, 2026-11-16) implemented, deferred or left blocked: only unblocked '
        'proposals were implemented, and no open question was answered by inference.</p></div>'
    )

    body += "<h2>Verified basis</h2>" + '<p class="small">The facts the proposals rest on, re-verified 2026-11-15 and re-checked 2026-11-16 (session record: <a href="sessions/5a56c084/index.html">5a56c084</a>).</p>'
    rows = []
    for v in s["verified_basis"]:
        rows.append([
            e(v["id"]),
            f'<strong>{e(v["item"])}</strong>',
            e(v["value"]),
            src_links(v["source"]),
        ])
    body += table(["ID", "Verified fact", "What the official source says", "Source"], rows)

    sug_rows = []
    impl_rows = []
    for g in s["suggestions"]:
        blocker = (
            f'<div class="muted">Blocked: {e(g["blocker"])}</div>' if g.get("blocker") else ""
        )
        comp = "<ul class=\"findings\">" + "".join(
            f"<li>{e(c['text'])} {src_links(c['source'])}</li>" for c in g["compliance"]
        ) + "</ul>"
        sug_rows.append([
            e(g["id"]),
            f'<strong>{e(g["title"])}</strong>',
            f'<div>{e(g["what"])}</div>{blocker}',
            f'<div>{e(g["why"])}</div>{comp}',
            badge("Proposal", "info") if g["status"] == "proposed"
            else badge("Blocked", "warn") if g["status"] == "blocked"
            else badge("Accepted", "ok"),
        ])
        # Session 5a56c084 merge (2026-11-16): "implementation" is now a list of records,
        # one per deciding session - f132f462 implemented its own versions of SUG-01/04/08
        # in parallel, and both sessions' records are kept and rendered.
        for impl in (g.get("implementation") or []):
            badge_html = {
                "implemented": '<span class="badge ok">Implemented</span>',
                "partially implemented": '<span class="badge ok">Implemented (partial)</span>',
                "deferred": '<span class="badge info">Deferred</span>',
                "blocked": '<span class="badge warn">Still blocked</span>',
            }.get(impl.get("status", ""), '<span class="badge muted">Recorded</span>')
            evidence = " ".join(
                f'<a href="{e(h)}">{e(t)}</a>' for h, t in impl.get("evidence", [])
            ) or "&mdash;"
            impl_rows.append([
                e(g["id"]),
                f"<strong>{e(g['title'])}</strong>",
                f"{e(impl.get('by', ''))}",
                badge_html,
                e(impl.get("note", "")),
                f"{e(impl.get('date', ''))}",
                evidence,
                src_links(impl.get("basis", ["S01"])),
            ])
    body += "<h2>Design and marketing suggestions</h2>" + table(
        ["ID", "Suggestion", "What it is", "Why it helps / compliance", "Status"], sug_rows)

    if impl_rows:
        body += (
            '<div class="callout ok"><p><strong>Decision log.</strong> For each proposal '
            '(SUG-01 to SUG-10) the implementing sessions recorded accept / defer / hold with a '
            'reason, exactly as the workflow below asks. Every implemented item respects its '
            'compliance basis: no tagged conversion CTAs (SUG-05 stays blocked pending Q1), '
            'no price or rating display (2(b)/6(t)), no invented metrics anywhere. Two sessions '
            'worked this page in parallel (5a56c084 and f132f462) and both records are kept; '
            'change requests that touch another session&#8217;s scope are logged in '
            'COORDINATION.md instead of acted on.</p></div>'
        )
        body += "<h2>Decision log (recorded 2026-11-16, sessions 5a56c084 and f132f462)</h2>" + table(
            ["ID", "Proposal", "Decided by", "Decision", "What was done / why it waits", "Recorded", "Evidence on this site", "Basis"],
            impl_rows)

    q_rows = []
    for q in s["questions"]:
        q_rows.append([
            e(q["id"]),
            f'<strong>{e(q["question"])}</strong>',
            e(q["what_we_know"]) + f" {src_links(q['source'])}",
            e(q["what_we_dont_know"]),
            e(q["why_it_matters"]),
            e(q["how_to_discover"]),
        ])
    body += "<h2>Open questions: what must be answered before a decision</h2>" + table(
        ["ID", "Question", "What we already know (sourced)", "What we do not know",
         "Why it matters for the decision", "How to discover it"], q_rows)

    d_rows = []
    for d in s["discovery"]:
        d_rows.append([
            e(d["id"]),
            f'<strong>{e(d["action"])}</strong>',
            e(d["discovers"]),
            src_links(d["source"]),
        ])
    body += "<h2>Suggestions for discovering the missing information</h2>" + table(
        ["ID", "Action", "What it discovers", "Source"], d_rows)

    body += "<h2>How to use this page</h2><ol class=\"findings\">" + "".join(
        f"<li>{e(step)}</li>" for step in s["workflow"]
    ) + "</ol>"

    page("suggestions.html", "Suggestions & decisions", body,
         lead="Design and marketing proposals for the affiliate site, the open questions that "
              "must be answered before any decision, and how to discover the missing "
              "information. Proposals are labelled as proposals; every fact carries its "
              "source; the decision log records what has been implemented, deferred or "
              "left blocked.")


# ------------------------------------------- Design brief (session 757efebc, 2026-11-16)
STATE_KIND = {
    "do-now": "ok",
    "do-next": "info",
    "blocked": "warn",
    "defer": "muted",
    "do-not-do": "bad",
    "proposal": "info",
    "recommended": "ok",
}


def repo_link(path: str, label: str) -> str:
    """Link a file in this repository. Used where a row describes repository state."""
    return (f'<a href="{REPO}/blob/main/{e(path)}" target="_blank" '
            f'rel="noopener noreferrer">{e(label)}</a>')


def basis(rec: dict) -> str:
    """Evidence cell for a row: official sources first, then the repository reference."""
    parts = []
    if rec.get("src"):
        parts.append(src_links(rec["src"]))
    if rec.get("repo"):
        parts.append(repo_link(rec["repo"], "this repo: " + rec["repo"]))
    return " &middot; ".join(parts) or '<span class="muted">no source</span>'


def build_design_brief() -> None:
    """The redesign brief and prompt pack (session 757efebc, 2026-11-16).

    The concrete answer to "it reads like AI slop": a critique of what the site does now,
    a copy-and-paste prompt for the redesign, a design system, a twelve-article editorial
    plan, a traffic architecture, a conversion architecture and an anti-slop checklist.
    Every factual row links the official page it was read from, or the file in this
    repository it describes. Published for review; nothing here is implemented.
    """
    d = DESIGN
    body = (
        '<div class="callout"><p><strong>What this page is.</strong> The redesign brief for '
        'this site. It names what makes the current pages read as machine output, then gives '
        'a copy-and-paste prompt, a design system, a twelve-article editorial plan, a traffic '
        'architecture and an anti-slop checklist. Every factual row carries the official source '
        'it rests on, or the file in this repository it describes. <strong>Nothing on this page '
        'is implemented</strong>: it exists so the path is chosen before anything is built. '
        'The reviewable version of every proposal is on the '
        '<a href="decision-queue.html">Review console</a>. This session&rsquo;s verification log and repository review are in the <a href="sessions/757efebc/index.html">session record</a>.</p></div>'
        + '<div class="suggestion"><h3>How this relates to the /site/ marketing site</h3>'
        f'<p>{e(d["relationship_note"])}</p>'
        '<p><a href="site/index.html">Marketing site</a> &middot; '
        '<a href="site/decisions.html">Marketing site: suggestions &amp; decisions</a></p></div>'
    )

    rows = [[e(r["id"]), f'<strong>{e(r["point"])}</strong>', e(r["detail"]), basis(r)]
            for r in d["executive_summary"]]
    body += ("<h2>Executive summary</h2>"
             '<p class="small">The eight things that decide everything else, each with the '
             "source it rests on.</p>") + table(
        ["ID", "Point", "Detail", "Source"], rows)

    rows = [[e(c["id"]), f'<strong>{e(c["area"])}</strong>', e(c["observed"]),
             e(c["slop"]), e(c["fix"]), basis(c)] for c in d["critique"]]
    body += ("<h2>Why it reads as generated: ten findings</h2>"
             '<p class="small">Each row names something actually present in this repository '
             "today, why it reads the way it does, and the fix. The observations are about "
             "this site's own files, so they cite the file.</p>") + table(
        ["ID", "Area", "What is there now", "Why it reads as generated", "Fix", "Basis"], rows)

    blocks = [f'{b["label"].upper()}\n\n{b["text"]}' for b in d["prompt"]]
    prompt_text = "\n" + ("\n\n" + ("-" * 64) + "\n\n").join(blocks) + "\n"
    body += (
        "<h2>The prompt</h2>"
        f'<p class="small">{e(d["prompt_intro"])}</p>'
        '<div class="decision-tools"><button type="button" id="copy-prompt">Copy the prompt</button>'
        '<output id="copy-status" aria-live="polite"></output></div>'
        f'<pre class="promptbox" id="prompt-block">{e(prompt_text)}</pre>'
        '<script>(function(){var b=document.getElementById("copy-prompt");'
        'if(!b){return;}var out=document.getElementById("copy-status");'
        'b.addEventListener("click",function(){'
        'var t=document.getElementById("prompt-block").innerText;'
        'if(navigator.clipboard&&navigator.clipboard.writeText){'
        'navigator.clipboard.writeText(t).then(function(){out.textContent="Copied to clipboard.";},'
        'function(){out.textContent="Copy failed - select the text by hand.";});}'
        'else{out.textContent="Copy unavailable in this browser - select the text by hand.";}});})();</script>'
    )

    rows = [[e(r["id"]), f'<strong>{e(r["element"])}</strong>', e(r["spec"]), e(r["why"]),
             basis(r)] for r in d["design_system"]]
    body += ("<h2>Design system</h2>"
             '<p class="small">Concrete values, with the current value or the rule that '
             "constrains it.</p>") + table(
        ["ID", "Element", "Specification", "Why", "Basis"], rows)

    rows = []
    for r in d["ia"]:
        rows.append([e(r["id"]), badge(e(r["surface"]), "info" if r["surface"] == "Reader" else "muted"),
                     f'<strong>{e(r["page"])}</strong>', e(r["job"]), e(r["cta"]),
                     badge(e(r["status"]), STATE_KIND.get(r["status"], "muted")), basis(r)])
    body += ("<h2>Information architecture</h2>"
             '<p class="small">Two surfaces: the reader site, and the evidence layer that '
             "makes it trustworthy. They are linked by one page, How we verify.</p>") + table(
        ["ID", "Surface", "Page", "Job", "Primary action", "State", "Basis"], rows)

    rows = []
    for r in d["editorial"]:
        rows.append([e(r["id"]), f'<strong>{e(r["title"])}</strong>',
                     f'<div>{e(r["hook"])}</div><div class="muted">{e(r["angle"])}</div>',
                     e(r["format"]), e(r["fact"]), e(r["rule"]), basis(r)])
    body += ("<h2>Editorial plan: twelve articles</h2>"
             '<p class="small">Catchy, shareable titles, each anchored to a fact read from '
             "the live listing and each with the thing it must not claim. No article may "
             "state a price, a rating or a test result.</p>") + table(
        ["ID", "Working title", "Hook and angle", "Format", "Verified fact it rests on",
         "What it must not say", "Source"], rows)

    rows = [[e(r["id"]), f'<strong>{e(r["action"])}</strong>', e(r["what"]), e(r["why"]),
             e(r["constraint"]), basis(r)] for r in d["traffic"]]
    body += ("<h2>Organic traffic architecture</h2>"
             '<p class="small">How the site earns visitors, and the programme rules that '
             "bound each move.</p>") + table(
        ["ID", "Move", "What it is", "Why it works", "Constraint", "Source"], rows)

    rows = [[e(r["id"]), f'<strong>{e(r["element"])}</strong>', e(r["spec"]), e(r["why"]),
             basis(r)] for r in d["conversion"]]
    body += ("<h2>Conversion architecture</h2>"
             "<p class=\"small\">Where the money is made, lawfully.</p>") + table(
        ["ID", "Element", "Specification", "Why", "Basis"], rows)

    rows = [[e(r["id"]), e(r["tell"]), e(r["fix"]), basis(r)] for r in d["anti_slop"]]
    body += ("<h2>Anti-slop checklist</h2>"
             '<p class="small">Ten tells, and what to do instead. Run a page against this '
             "before it ships.</p>") + table(
        ["ID", "The tell", "What to do instead", "Basis"], rows)

    body += "<h2>How to use this brief</h2><ol class=\"findings\">" + "".join(
        f"<li>{e(step)}</li>" for step in d["workflow"]) + "</ol>"

    page("design-brief.html", "Design brief", body,
         lead="Why the site reads as generated, and the prompt, design system, editorial plan "
              "and checklists to fix it. Proposals only, each with its source. Nothing here is "
              "implemented yet.")


def build_decision_queue() -> None:
    """The review console (session 757efebc, 2026-11-16).

    Every proposal in one place with a recommendation, a priority, an effort estimate, a
    risk, the question that blocks it and a decision state; then the information we already
    have, the information we do not have, and how to go and get it.
    """
    q = QUEUE
    body = (
        '<div class="callout"><p><strong>What this page is.</strong> The section to review '
        'before anything is implemented. Every proposal from this session and from session '
        '4f83ee7b sits in one queue with a recommendation and a decision state. Below it is '
        'the information this project already has, the information it does not have, and the '
        'actions that would get it. Nothing on this page implements anything: the point is to '
        'choose the path first. The design rationale behind these rows is on the '
        '<a href="design-brief.html">Design brief</a>. This session&rsquo;s verification log and repository review are in the <a href="sessions/757efebc/index.html">session record</a>.</p></div>'
        + '<div class="suggestion"><h3>How this relates to /site/decisions.html</h3>'
        f'<p>{e(q["relationship_note"])}</p>'
        '<p><a href="site/decisions.html">Marketing site: suggestions &amp; decisions</a> &middot; '
        '<a href="site/index.html">Marketing site home</a></p></div>'
    )

    # Rendered as a definition list, not a table. This site's rule is that every *table* row
    # carries a source link or a flag; these rows are this project's own workflow vocabulary
    # and cite nothing, so putting them in a table would either fake a source or trip the
    # row-provenance gate. A legend is not data.
    legend = "".join(
        f'<div class="suggestion"><h3>{badge(e(k), STATE_KIND.get(k, "muted"))}</h3>'
        f"<p>{e(v)}</p></div>" for k, v in q["states"].items()
    )
    body += ("<h2>What the decision states mean</h2>" + legend
             + f'<p class="small">{e(q["columns_note"])}</p>')

    rows = []
    for s in q["suggestions"]:
        sizing = (f'<div><strong>{e(s["recommendation"])}</strong></div>'
                  f'<div class="muted">{e(s["priority"])} &middot; effort {e(s["effort"])} '
                  f'&middot; risk {e(s["risk"])}</div>')
        blocked = (" &middot; ".join(
            f'<a class="flagid" href="#{e(b)}">{e(b)}</a>' for b in s["blocked_by"]
        ) or '<span class="muted">nothing</span>')
        rows.append([
            # The id is the anchor the "Blocks" column of the questions table links to, so a
            # reviewer can jump from a question to every proposal it gates.
            f'<strong id="{e(s["id"])}">{e(s["id"])}</strong><div class="muted">{e(s["origin"])}</div>',
            f'<strong>{e(s["title"])}</strong><div class="muted">{e(s["area"])}</div>',
            e(s["what"]),
            sizing,
            blocked,
            badge(e(s["status"]), STATE_KIND.get(s["status"], "muted")),
            basis(s),
        ])
    body += ("<h2>The queue</h2>"
             '<p class="small">22 proposals. Blocked-by links jump to the question that '
             "unblocks the row.</p>") + table(
        ["ID and origin", "Proposal", "What it is", "Recommendation and sizing",
         "Blocked by", "State", "Basis"], rows)

    rows = [[e(r["id"]), f'<strong>{e(r["item"])}</strong>', e(r["value"]), basis(r)]
            for r in q["have"]]
    body += ("<h2>What we already have</h2>"
             '<p class="small">Everything on this list was read from the official page named '
             "in its Source cell. Nothing here is inferred.</p>") + table(
        ["ID", "Information", "What it says", "Source"], rows)

    rows = []
    for r in q["missing"]:
        rows.append([e(r["id"]), f'<strong>{e(r["item"])}</strong>', e(r["needed_for"]),
                     sev(e(r["severity"])), e(r["how"]), basis(r)])
    body += ("<h2>What we do not have</h2>"
             '<p class="small">Every gap that stands between this repository and a working '
             "affiliate site, with the way to close it. No value on this page is filled in "
             "from anywhere but an official source, so these cells stay empty until one "
             "exists.</p>") + table(
        ["ID", "Missing information", "What it blocks", "Severity", "How to get it", "Source"], rows)

    rows = []
    for r in q["questions"]:
        blocks = (" &middot; ".join(
            f'<a class="flagid" href="#{e(b)}">{e(b)}</a>' for b in r["blocks"]
        ) or '<span class="muted">none directly</span>')
        rows.append([
            f'<strong id="{e(r["id"])}">{e(r["id"])}</strong>',
            f'<strong>{e(r["question"])}</strong>',
            e(r["have"]),
            e(r["missing"]),
            e(r["why"]),
            e(r["how"]),
            blocks,
            basis(r),
        ])
    body += ("<h2>Questions that must be answered first</h2>"
             '<p class="small">Split into what we can already source and what we cannot. '
             "A decision made before these are answered is a guess.</p>") + table(
        ["ID", "Question", "What we have (sourced)", "What we do not have",
         "Why it matters", "How to answer it", "Blocks", "Source"], rows)

    rows = [[e(r["id"]), f'<strong>{e(r["action"])}</strong>', e(r["discovers"]),
             e(r["effort"]), basis(r)] for r in q["discovery"]]
    body += ("<h2>How to discover the missing information</h2>"
             "<p class=\"small\">Concrete actions, each one closing a named gap.</p>\"") + table(
        ["ID", "Action", "What it discovers", "Effort", "Source"], rows)

    body += "<h2>How to run the review</h2><ol class=\"findings\">" + "".join(
        f"<li>{e(step)}</li>" for step in q["workflow"]) + "</ol>"

    page("decision-queue.html", "Review console", body,
         lead="Every proposal, the recommendation against it, the question that blocks it, and "
              "the information this project has and does not have. Review and decide before "
              "anything is built.")


# ------------------------------------------------------------- Campaigns
def build_campaigns() -> None:
    rows = []
    for p in PRODUCTS:
        rows.append([
            e(p["label"]),
            val(p["associates_tag"]),
            badge("Not created", "bad"),
            val(p["clicks"]),
            val(p["conversions"]),
            flag_links(["FLG-010", "FLG-011"]),
            src_links(["S02", "S19"]),
        ])
    body = "<h2>Click and conversion ledger</h2>" + table(
        ["Product", "Associates tag", "Special Link", "Clicks", "Conversions", "Flags", "Source"], rows)
    body += f"""
<section class="card">
  <h2>What this ledger records</h2>
  <ul class="findings">
    <li>Clicks and conversions are blank. No click or conversion figure exists from an official source (FLG-011).</li>
    <li>A conversion counts only if it meets the 89-day cart window and is not cancelled, returned or refunded {src_links(['S02'])} (PF-12, PF-13).</li>
    <li>Special Links must carry the Associates tag (PF-03). No tag has been supplied, so no Special Link has been created (FLG-010).</li>
  </ul>
</section>
"""
    page("campaigns.html", "Campaigns &amp; tracking", body,
         lead="Empty by design. Figures appear here only after they come from the owner's Associates reports.")


# ------------------------------------------------------------- Flagged
def build_flagged() -> None:
    rows = []
    for f in FLAGS:
        rows.append([
            f'<a id="{e(f["id"])}"></a><strong>{e(f["id"])}</strong>',
            sev(f["severity"]),
            e(f["category"]),
            e(f["item"]),
            e(f["detail"]),
            e(f["action"]),
            src_links(f["sources"]) if f.get("sources") else
            f'<a href="{REPO}" target="_blank" rel="noopener noreferrer">repo</a> <span class="muted">&mdash; observed in this repository, so no external source is cited</span>',
        ])
    body = (
        '<div class="callout"><p><strong>Flagged for review.</strong> These items do not block the merge. '
        "Each one has its evidence source links and the action needed. Send any change request by replying to the owner; the site will be rebuilt from the data files.</p></div>"
        + "<h2>All flags</h2>"
        + table(["ID", "Severity", "Category", "Item", "Detail", "Action needed", "Source"], rows)
    )
    obs = []
    for p in PRODUCTS:
        ro = p["redirect_observed"]
        obs.append([
            f'<a href="{e(p["submitted_url"])}" target="_blank" rel="noopener noreferrer">{e(p["label"])} ({e(p["link_id"])})</a>',
            f'<a href="{e(ro["final_url"])}" target="_blank" rel="noopener noreferrer">{e(ro["page_id"])}</a>',
            e(ro["page_title"]),
            badge("No: not the submitted product", "warn"),
            src_links([ro["source"], ro["title_source"]]),
        ])
    body += (
        "<h2>Observed redirect targets (full titles as read, not confirmed)</h2>"
        "<p class=\"muted\">Identity table published as the E-T2 addendum for FLG-035 "
        "(session f1b7da46's request, session f118dddd, 2026-11-14): each submitted short link "
        "with the page it currently opens. The short-link column is the observation source; the "
        "page title is read from the destination. Whether a destination is the product the "
        "submitter meant is not documented by any official source (FLG-002, FLG-035).</p>"
        + table(
            ["Submitted link (observed)", "Page ID", "Page title as read", "Confirmed?", "Source"], obs)
    )
    page("flagged.html", "Flagged for review", body,
         lead=(f"{len(FLAGS)} entries: {sev_count('Critical')} critical, {sev_count('High')} high, "
               f"{sev_count('Medium')} medium, {sev_count('Low')} low, {sev_count('Info')} info "
               "(info entries record a correction made to this site, not a problem with a product)."))


# ------------------------------------------------------------- Sources
def build_sources() -> None:
    rows = []
    for s in SRC["sources"]:
        status = {
            "verified": badge("Verified", "ok"),
            "observed": badge("Observed", "info"),
            "not-accessible": badge("Not accessible", "warn"),
            "third-party": badge("Third-party (not verified)", "bad"),
        }[s["status"]]
        rows.append([
            f'<strong>{e(s["id"])}</strong>',
            e(s["title"]),
            f'<a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer">{e(s["url"])}</a>',
            status,
            e(s["status_note"]),
            e(s["used_for"]),
        ])
    body = (
        f'<p class="muted">Retrieved {e(SRC["retrieved"])}. Official = Amazon Associates, Amazon.com (including Sell on Amazon), Amazon Seller Central, or the U.S. FTC. '
        "Third-party sources appear only to raise flags.</p>"
        + table(["ID", "Source", "Link", "Status", "Note", "Used for"], rows)
    )
    page("sources.html", "Sources", body,
         lead="Every official page used to verify this site, with the status it had when read.")


# ------------------------------------------------------------- Category
COMP = load("competition.json")


def build_marketing() -> None:
    """Marketing content page.

    INTEGRATION NOTE (session b90c5685, 2026-11-14). PR #26 (session 9fef7647) wrote this page
    from product_name/brand/price/rating fields that it had filled with values read off each
    short link's redirect destination. Those fields are blank on main by design: the submitted
    code is not an ASIN, so no official source ties the destination's attributes to the
    submitted link (FLG-001, FLG-002, FLG-035, FLG-038). The page is kept, but every product
    claim is now attributed to the listing the link opens, never to the submitted link, and no
    price, star rating or review count is printed (PF-04, PF-05; FLG-022, FLG-029).
    The listing titles/feature summaries below are the destination page titles, which main
    already records verbatim in products.json -> redirect_observed.page_title (S14/S15/S23).
    """
    briefs = [
        ("P1", "Two-basket cooking for families who cook two foods at once",
         ["Two independent 3-quart baskets with Sync Finish, as stated in the listing title",
          "Easy-view windows and a digital touchscreen, as stated in the listing title",
          "Hi-Fry option and auto shutoff, as stated in the listing title"],
         "https://link.amazon/B04G1MEwY", "S14"),
        ("P2", "An all-in-one oven replacement",
         ["26-quart air-fryer toaster oven with French doors, as stated in the listing title",
          "24 cooking functions, a dual-speed fan and a rotisserie, as stated in the listing title",
          "Family-size capacity, as stated in the listing title"],
         "https://link.amazon/B02NbDxp3", "S15"),
        ("P3", "A large single-basket air fryer",
         ["8-quart XL nonstick, dishwasher-safe basket, as stated in the listing title",
          "TurboFry 4-in-1: bake, dehydrate and cook from frozen, as stated in the listing title",
          "450-degree Hi-Fry option, as stated in the listing title"],
         "https://link.amazon/B00hJ57DV", "S23"),
    ]
    parts = []
    for pid, angle, bullets, url, title_src in briefs:
        p = next(x for x in PRODUCTS if x["id"] == pid)
        ro = p["redirect_observed"]
        li = "".join(f"<li>{e(b)}</li>" for b in bullets)
        facts = table(
            ["Attribute (of the listing the link opens)", "As stated on the Amazon listing", "Source"],
            [
                ["Listing title, as read", e(ro["page_title"]), src_links([title_src])],
                ["Listing ID (ASIN of the destination page)", e(ro["page_id"]), src_links([title_src])],
                ["Submitted code", f'{e(p["link_id"])} <span class="muted">({p["link_id_length"]} characters: not an ASIN)</span>',
                 src_links(["S06"]) + " " + flag_links(["FLG-001"])],
                ["Price, rating and review count", unv() + " " + badge("Not shown: display rule", "info"),
                 src_links(["S02"]) + " " + flag_links(["FLG-022", "FLG-029", "FLG-036"])],
            ],
        )
        parts.append(f"""
<section class="card">
  <h2>{e(p["label"])}: {e(angle)}</h2>
  <p>Every claim below describes <strong>the Amazon listing that this submitted link currently opens</strong>,
  not a product the submitted code is documented to identify. Nothing here is based on hands-on testing:
  nobody on this project has used these products.</p>
  <ul class="findings">{li}</ul>
  <p><a href="{e(url)}" target="_blank" rel="noopener noreferrer">Open the submitted link on Amazon</a>
  &mdash; check the current price and availability there. This page states none, because a price or rating
  may only be displayed when Amazon serves the link that shows it, or when it comes from the Creators API.</p>
  {facts}
</section>""")

    comp_rows = [
        ["Listing the link opens", e(PRODUCTS[0]["redirect_observed"]["page_id"]),
         e(PRODUCTS[1]["redirect_observed"]["page_id"]), e(PRODUCTS[2]["redirect_observed"]["page_id"]),
         src_links(["S14", "S15", "S23"])],
        ["Form factor (from the listing title)", "Dual-basket air fryer oven", "French-door air fryer toaster oven",
         "Single XL-basket air fryer", src_links(["S14", "S15", "S23"])],
        ["Capacity (from the listing title)", "6 quart (2 &times; 3 qt)", "26 quart", "8 quart",
         src_links(["S14", "S15", "S23"])],
        ["Standout listed features", "Sync Finish, Hi-Fry, easy-view windows", "24 functions, rotisserie, dual-speed fan",
         "450F Hi-Fry, bake, dehydrate, frozen", src_links(["S14", "S15", "S23"])],
        ["Price and rating", badge("Not stated (PF-04, PF-05)", "info"), badge("Not stated (PF-04, PF-05)", "info"),
         badge("Not stated (PF-04, PF-05)", "info"), src_links(["S02"])],
    ]
    comp = table(["Attribute", "Submitted link 1", "Submitted link 2", "Submitted link 3", "Source"], comp_rows)

    guide = f"""
<section class="card">
  <h2>Buying guide: choosing between the three listings</h2>
  <p>Amazon shows all three destinations in the same breadcrumb
  Home &amp; Kitchen &rsaquo; Kitchen &amp; Dining &rsaquo; Small Appliances &rsaquo; Fryers &rsaquo; Air Fryers
  {src_links(['S14', 'S15', 'S23'])} but their listing titles describe different jobs. Every product fact
  below is read from the listing title and linked.</p>
  <ul class="findings">
    <li><strong>Do you cook two foods at once?</strong> Only the first listing states two independent baskets with
    a synchronised finish {src_links(["S14"])}. The other two titles describe single-chamber designs
    {src_links(["S15", "S23"])}.</li>
    <li><strong>Are you replacing a countertop oven?</strong> The second listing states French doors, 24 cooking
    functions, a rotisserie and a 26-quart cavity {src_links(["S15"])}.</li>
    <li><strong>Is easy cleanup the priority?</strong> The first and third listings both state nonstick,
    dishwasher-safe baskets {src_links(["S14", "S23"])}.</li>
    <li><strong>Do you want high-temperature crisping?</strong> The first and third listings both state a Hi-Fry
    option (the third states 450 degrees) {src_links(["S14", "S23"])}.</li>
    <li><strong>Compare current prices yourself.</strong> This guide states no prices or ratings: they are volatile
    and their display is restricted for Associates sites {src_links(["S02"])} {flag_links(["FLG-022", "FLG-029", "FLG-036"])}.</li>
    <li><strong>Read the return policy and warranty on the listing before buying.</strong> Terms are set by Amazon
    and can change {src_links(["S01"])}.</li>
  </ul>
</section>
<section class="card">
  <h2>How this content meets the rules</h2>
  <ul class="findings">
    <li>Every product claim is attributed to the listing it was read from and carries a source link
    (Participation Requirements 2(b): no inaccurate or misleading claims) {src_links(["S02"])}.</li>
    <li>No first-hand experience is claimed; nobody on this project has tested these products
    (FTC Disclosures 101) {src_links(["S07"])}.</li>
    <li>The affiliate relationship is disclosed on every page, with the exact wording required by
    Operating Agreement Section 5 {src_links(["S01"])}.</li>
    <li>No prices, star ratings or review counts appear in this content {src_links(["S02"])}
    {flag_links(["FLG-022", "FLG-029", "FLG-036"])}.</li>
    <li>The outbound links are the owner-submitted short links. Whether they carry an Associates tag is
    unverified, and short-link compliance is open {flag_links(["FLG-003", "FLG-010"])}.</li>
    <li>Which product each submitted code was meant to identify is still unconfirmed, so no page here calls
    the destination "the submitted product" {flag_links(["FLG-002", "FLG-035", "FLG-038"])}.</li>
  </ul>
</section>"""

    body = ('<div class="callout ok"><p><strong>Facts-only marketing content.</strong> Three SEO product briefs, '
            "one comparison and one buying guide, written from what each Amazon listing states, with a source link "
            "for every claim. No prices or ratings are quoted and no first-hand experience is claimed.</p></div>"
            + "".join(parts)
            + "<h2>Comparison: the three listings side by side</h2>"
            + comp
            + guide)
    page("marketing/briefs.html", "Marketing content: product briefs", body,
         lead="SEO product briefs, a comparison and a buying guide for the three listings the submitted links open. Written from verified listing facts only.")



def build_category() -> None:
    """Category subpage: Air Fryers (Amazon browse node 17659096011).

    Only verified fields are shown. Prices, ratings and review counts are NOT shown
    (Participation Requirements 2(b) and 6(t); see FLG-022)."""
    path_rows = []
    nodes = ["1055398", "284507", "289913", "17659095011", "17659096011"]
    for i, (name, node) in enumerate(zip(COMP["category_path"], nodes), start=1):
        path_rows.append([str(i), e(name), e(node),
                          src_links(["S14", "S15", "S16"]) + (" &middot; " + src_links(["S43"]) if i == 5 else "")])
    body = "<h2>Verified category path</h2>" + table(
        ["Level", "Category", "Browse node", "Source"], path_rows)

    sub_rows = [
        ['<td colspan="6" style="background:#fff8e6"><strong>Price, star rating and review count are not '
         'shown in this table.</strong> Participation Requirements 2(b) and 6(t) permit prices, availability, '
         'star ratings and customer reviews only where Amazon serves the link that displays them, or where the '
         'data is obtained through Creators API or PA API and used under the License. This project has no '
         'Associates tag and no Creators API credentials, so no permitted path exists: the values are withheld '
         'rather than transcribed from a rendered page. The observation notes are kept for context with their '
         'own source links: ' + src_links(["S46", "S47", "S48"]) + '. Regulation: ' + src_links(["S02"]) +
         '. Flagged as <a class="flagid" href="flagged.html#I-F-01">I-F-01</a>.</td>']
    ]
    for p in PRODUCTS:
        ro = p["redirect_observed"]
        sub_rows.append([
            e(p["label"]),
            f'<a href="{e(p["submitted_url"])}" target="_blank" rel="noopener noreferrer">{e(p["link_id"])}</a>',
            f'<a href="{e(ro["final_url"])}" target="_blank" rel="noopener noreferrer">{e(ro["page_id"])}</a> {badge("Not confirmed as submitted", "warn")}',
            e(ro["page_title"]),
            flag_links(p["flags"]),
            src_links([ro["title_source"], ro["source"]]),
        ])
    body += "<h2>Submitted links in this category</h2>" + table(
        ["Product", "Submitted link", "Observed destination", "Destination page title (as read)", "Flags", "Source"], sub_rows)

    bs_rows = []
    for r in COMP["rows"]:
        bs_rows.append([
            f'<strong>#{r["rank"]}</strong>',
            f'<a href="{e(r["url"])}" target="_blank" rel="noopener noreferrer">{e(r["asin"])}</a>',
            e(r["title"]),
            src_links([COMP["source"]]) + " " + flag_links(["FLG-022", "FLG-025"]),
        ])
    body += ("<h2>Competition benchmark: Best Sellers in Air Fryers (positions 1&ndash;6)</h2>"
             f'<p class="muted">Read {e(COMP["read_on"])}. Positions 7 and below are not used. Rank changes between captures (FLG-025).</p>'
             + table(["Rank", "ASIN (link)", "Title as shown on the official page", "Source"], bs_rows))

    body += "<h2>Commission reference (not applied)</h2>" + table(
        ["Rate-card category", "Standard rate", "Status", "Source"],
        [["Kitchen (Standard Commission, Table 1)", "4.50%",
          "Reference only. Whether it applies to these listings is not confirmed (FLG-021).",
          src_links(["S25"]) + " " + flag_links(["FLG-021"])]])
    body += """
<section class="card">
  <h2>What this page does and does not show</h2>
  <ul class="findings">
    <li>The category path and the six bestseller positions were read from official Amazon pages on 2026-11-14.</li>
    <li>The submitted identifiers do not resolve to a product page under their own code (see <a href="products.html">Products</a>, FLG-001). The observed destinations are not treated as the submitted products (FLG-002).</li>
    <li>Prices, ratings and review counts are blank here. They can be shown only through an approved Amazon data path (FLG-022, FLG-023).</li>
    <li>No claim is made about competitors beyond position 6, because that part of the list was not read.</li>
  </ul>
</section>
"""
    page("air-fryers.html", "Category: Air Fryers", body,
         lead="Amazon browse node 17659096011. The category path, the submitted links that fall in it, and a six-position bestseller benchmark, each linked to its official page.")


def build_assets() -> None:
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "style.css").write_text(css(), encoding="utf-8")
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")


# ------------------------------------------------------- Verification log page
# Added by the final integration session edbd56a1 (2026-11-14). Every row below was read
# from the official page it cites on 2026-11-14 by that session, independently of the
# sessions that first recorded it. Nothing here is inferred; a row exists only because
# the quoted text or the observed response was on the page when it was fetched.

VERIFY_ROWS: list[tuple[str, str, str, str, list[str]]] = [
    ("Submitted link 1 resolves", "Products, Air Fryers",
     "https://link.amazon/B04G1MEwY lands on amazon.com/dp/B0CDY277D3 \u2014 \u201cCHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows\u2026\u201d",
     "Observed", ["S11", "S14"]),
    ("Submitted link 2 resolves", "Products, Air Fryers",
     "https://link.amazon/B02NbDxp3 lands on amazon.com/dp/B09B7SB46R \u2014 \u201cEmeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven\u201d",
     "Observed", ["S12", "S15"]),
    ("Submitted link 3 resolves", "Products, Air Fryers",
     "https://link.amazon/B00hJ57DV lands on amazon.com/dp/B08DKYBTPH \u2014 \u201cChefman Air Fryer 8 Qt | TurboFry\u00ae 4-in-1\u2026\u201d",
     "Observed", ["S13", "S23"]),
    ("Direct /dp/<id> for link 1", "Products, Pricing",
     "amazon.com/dp/B04G1MEwY returns Amazon\u2019s \u201cPage Not Found\u201d page (title: Page Not Found)",
     "Observed", ["S08"]),
    ("Direct /dp/<id> for link 2", "Products, Pricing",
     "amazon.com/dp/B02NbDxp3 returns Amazon\u2019s \u201cPage Not Found\u201d page",
     "Observed", ["S09"]),
    ("Direct /dp/<id> for link 3", "Products, Pricing",
     "amazon.com/dp/B00hJ57DV returns Amazon\u2019s \u201cPage Not Found\u201d page",
     "Observed", ["S10"]),
    ("Category breadcrumb of the three destinations", "Air Fryers",
     "Home & Kitchen (1055398) \u203a Kitchen & Dining (284507) \u203a Small Appliances (289913) \u203a Fryers (17659095011) \u203a Air Fryers (17659096011), read in each destination page",
     "Observed", ["S14", "S15", "S16"]),
    ("Operating Agreement \u00a75 disclosure sentence", "Content & compliance, every footer",
     "\u201cAs an Amazon Associate I earn from qualifying purchases.\u201d",
     "Verbatim", ["S01"]),
    ("Operating Agreement \u00a76 \u2014 breach of \u00a75", "Content & compliance",
     "\u201cany violation of Section 5 \u2026 will be deemed a material breach of this Agreement\u201d",
     "Verbatim", ["S01"]),
    ("Operating Agreement Schedule 1", "Flagged (FLG-015)",
     "United States | Amazon.com Services LLC | amazon.com \u2014 the only row in the schedule",
     "Verbatim", ["S01"]),
    ("Participation Requirements 2(b) \u2014 tag", "Products, Campaigns",
     "\u201cyou must include your Associates ID or \u201ctag\u201d (appearing as XXXXX-## \u2026) as a parameter in the URL\u201d",
     "Verbatim", ["S02"]),
    ("Participation Requirements 2(b) \u2014 prices", "Pricing, Flagged (FLG-022)",
     "\u201cyour Site may only show prices and availability if: (a) we serve the link \u2026 or (b) you obtain Product pricing and availability data via Creators API or PA API\u201d",
     "Verbatim", ["S02"]),
    ("Participation Requirements 2(b) \u2014 no misleading claims", "Content",
     "\u201cYou must not make inaccurate, overbroad, deceptive or otherwise misleading claims about any Product\u2026\u201d",
     "Verbatim", ["S02"]),
    ("Participation Requirements 2(b) \u2014 comparison prices", "Pricing",
     "a comparison format must display both the lowest \u201cnew\u201d price and the lowest \u201cused\u201d price",
     "Verbatim", ["S02"]),
    ("Participation Requirements \u00a74 \u2014 offline promotion ban", "Content",
     "\u201cYou will not engage in any Promotional Activities in any offline manner\u2026\u201d",
     "Verbatim", ["S02"]),
    ("Participation Requirements \u00a75 \u2014 machine learning", "Flagged (FLG-016)",
     "using, or allowing a third party to use, Special Links or Program Content \u201cto develop machine learning models or related technology\u201d is prohibited without prior written approval",
     "Verbatim", ["S02"]),
    ("Participation Requirements 1 \u2014 original content", "Reviews",
     "\u201cYour Site(s) must contain original content and be publicly available\u2026\u201d",
     "Verbatim", ["S02"]),
    ("Participation Requirements 6(s) \u2014 artificial clicks", "Campaigns",
     "\u201cYou will not artificially generate clicks or impressions on your Site or create Sessions on an Amazon Site\u2026\u201d",
     "Verbatim", ["S02"]),
    ("Participation Requirements 6(t) \u2014 reviews and star ratings", "Reviews, Flagged (FLG-022)",
     "\u201cYou will not display or otherwise use any of our customer reviews or star ratings \u2026 unless you have obtained a link \u2026 through Creators API or PA API\u201d",
     "Verbatim", ["S02"]),
    ("Participation Requirements 6(v) \u2014 cloaking", "Content, Flagged (FLG-003)",
     "\u201cYou will not cloak, hide, spoof, or otherwise obscure the URL of your Site containing Special Links (including by use of Redirecting Links)\u2026\u201d",
     "Verbatim", ["S02"]),
    ("Participation Requirements 6(w) \u2014 link shorteners", "Content, Flagged (FLG-003)",
     "\u201cYou will not use a link shortening service, button, hyperlink or other ad placement in a manner that makes it unclear that you are linking to an Amazon Site.\u201d",
     "Verbatim", ["S02"]),
    ("Participation Requirements 6(y) \u2014 price tracking", "Pricing",
     "\u201cUnless otherwise agreed by Amazon, your Site must not have price tracking and/or price alerting functionality.\u201d",
     "Verbatim", ["S02"]),
    ("Participation Requirements 6(z) \u2014 other retailers", "Content",
     "\u201cYou will not display on your Site \u2026 any Program Content to advertise or promote any products that are offered on any site that is not an Amazon Site\u201d",
     "Verbatim", ["S02"]),
    ("Commission Income Statement \u00a71 \u2014 session window", "Pricing",
     "a Session ends on the first of: 24 hours elapsing from the click, the customer placing a non-digital order, or a click through another Special Link",
     "Verbatim", ["S02"]),
    ("Commission Income Statement \u00a71 \u2014 89-day cart", "Pricing, Campaigns",
     "\u201ccompleting the order for that Product no later than 89 days after their initial click-through of the Special Link\u201d",
     "Verbatim", ["S02"]),
    ("Commission Income Statement \u00a71 \u2014 180-day ship and pay", "Pricing",
     "\u201cwithin 180 days of the purchase, the Product is shipped to, streamed or downloaded by, and paid for by the customer\u201d",
     "Verbatim", ["S02"]),
    ("Commission Income Statement 2(b) \u2014 refunds", "Campaigns",
     "\u201cany Product order where a cancellation, return, or refund has been initiated\u201d is disqualified",
     "Verbatim", ["S02"]),
    ("Commission Income Statement 2(e) \u2014 Redirecting Link", "Pricing, Flagged (FLG-003)",
     "\u201cany Product purchased by a customer who is referred to an Amazon Site by a link that sends users indirectly to an Amazon Site via an intermediate site \u2026 (a \u201cRedirecting Link\u201d)\u201d is disqualified",
     "Verbatim", ["S02"]),
    ("Commission Income Statement \u00a76 \u2014 payment timing", "Pricing",
     "\u201capproximately 60 days following the end of each calendar month in which they were earned\u201d",
     "Verbatim", ["S02"]),
    ("Payment Minimum Chart (US)", "Pricing",
     "Direct deposit 10 USD minimum; Amazon gift card 10 USD minimum, 2,000 USD maximum; check 100 USD minimum; check processing fee 15 USD",
     "Verbatim", ["S02"]),
    ("IP License \u00a71 \u2014 data mining and model training", "Flagged (FLG-016, FLG-019)",
     "using Program Content \u201cto, directly or indirectly, develop or improve large language or multimodal models, machine learning models or related technology\u201d is prohibited",
     "Verbatim", ["S02"]),
    ("IP License 2(b) \u2014 credentials", "Flagged (FLG-006)",
     "\u201cYou must use both a unique public key/private key pair \u2026 and an Associates tag parameter \u2026 to identify your account\u201d",
     "Verbatim", ["S02"]),
    ("IP License 2(e) \u2014 aggregation and analysis", "Flagged (FLG-016)",
     "\u201cYou will not, without our express prior written approval, access or use Creators API, PA API or Data Feeds for the purpose of aggregating, analyzing, extracting, or repurposing any Product Advertising Content \u2026 or in the direct training or fine-tuning of a machine learning and/or foundational model.\u201d",
     "Verbatim", ["S02"]),
    ("IP License 2(h) \u2014 caching", "Pricing",
     "images may not be stored or cached; other Product Advertising Content up to 24 hours; ASINs may be stored indefinitely until the License ends",
     "Verbatim", ["S02"]),
    ("IP License 2(i) \u2014 date and time stamp", "Pricing",
     "a date/time stamp is required next to pricing or availability when the data comes from Data Feeds or is refreshed less often than hourly",
     "Verbatim", ["S02"]),
    ("IP License 2(j) \u2014 request size", "Pricing",
     "\u201cyou will not send files to or from Creators API or PA API that are greater than 40KB without our prior written approval.\u201d",
     "Verbatim", ["S02"]),
    ("IP License 2(k) \u2014 text disclaimer", "Content",
     "\u201cCERTAIN CONTENT THAT APPEARS [IN THIS APPLICATION or ON THIS SITE, as applicable] COMES FROM AMAZON \u2026\u201d",
     "Verbatim", ["S02"]),
    ("Agent Terms 4(c) \u2014 agent identification", "agent-terms/, Flagged (FLG-019)",
     "requests must carry \u201cAgent/[agent name]\u201d in the user-agent string and must not complete or circumvent CAPTCHAs",
     "Verbatim", ["S02"]),
    ("Influencer Program Policy 3(c)", "Content",
     "material connections must follow the FTC Endorsement Guides \u201c(such as by using the text \u201c#Ad\u201d or \u201c#Sponsored\u201d)\u201d",
     "Verbatim", ["S02"]),
    ("Standard Commission Table 1", "Pricing, Air Fryers",
     "Physical Books, Kitchen, Automotive | 4.50% \u2014 also Luxury Beauty 10.00%, Toys/Home/Pets 3.00%, All Other Categories 4.00%. Read without a sign-in.",
     "Verbatim", ["S25"]),
    ("Onsite Commission Table A", "Pricing",
     "Digital Music, Physical Music, Handmade, Digital Videos, Health & Personal Care, Sports, Kitchen, Automotive | 1.25%",
     "Verbatim", ["S26"]),
    ("Commission schedule route is sign-in gated", "Flagged (FLG-005, V-F1)",
     "/help/operating/schedule redirects to an Amazon sign-in page for a per-account custom rate card. No rate is taken from it.",
     "Negative evidence", ["S03"]),
    ("Creators API prerequisites", "Flagged (FLG-006, FLG-023)",
     "four operations (SearchItems, GetItems, GetVariations, GetBrowseNodes); \u201cHave at least 10 qualifying sales within the past 30 days to access the PA API through the Creators API\u201d",
     "Verbatim", ["S04"]),
    ("PA-API 5 deprecation", "Flagged (FLG-007)",
     "\u201cThe Amazon Product Advertising API 5.0 (PA-API 5) has been deprecated and is being replaced by the Creators API.\u201d Calls still made to it return HTTP 403 AccessDeniedException.",
     "Verbatim", ["S05"]),
    ("ASIN definition (Creators API)", "Products, Flagged (FLG-001)",
     "\u201cASIN | Amazon Standard Identification Number: 10-Character alphanumeric unique identifier assigned by Amazon.\u201d",
     "Verbatim", ["S06"]),
    ("ASIN definition (second official Amazon source)", "Products, Flagged (FLG-001)",
     "\u201cIt\u2019s a unique 10-character alphanumeric code assigned to every product listed in the Amazon store.\u201d (Sell on Amazon, article dated Jun 4, 2025)",
     "Verbatim", ["S45"]),
    ("Best Sellers in Air Fryers, positions 1\u20136", "Air Fryers",
     "#1 Ninja B0CSZ7WBYW \u00b7 #2 bella B0CYJDVT31 \u00b7 #3 Cosori B0C33CHG99 \u00b7 #4 Chefman B0CNY1F31S \u00b7 #5 Cuisinart B0GVVJZDQV \u00b7 #6 Chefman B0GTBN7CS2",
     "Observed", ["S43"]),
    ("Account dormancy \u2014 180 days", "Content",
     "\u201cOnce you\u2019ve applied, you have 180 days to refer a sale through one of your Associates links.\u201d",
     "Verbatim", ["S28"]),
    ("Application review \u2014 three qualifying sales", "Content",
     "\u201cwe require at least three within the first 180 days\u201d; \u201cpersonal orders do not qualify\u201d; a good rule of thumb is \u201cat least 10 posts\u201d",
     "Verbatim", ["S29"]),
    ("FTC Endorsement Guides revision", "Content, Flagged (FLG-017)",
     "the Guides \u201cwere revised in 2023 with new or revised principles, examples, and definitions, including a new definition of \u2018clearly and conspicuously.\u2019\u201d",
     "Verbatim", ["S44", "S24"]),
    ("FTC affiliate disclosure standard", "Content & compliance",
     "\u201cYou should disclose your relationship to the retailer clearly and conspicuously on your site \u2026 The closer the disclosure is to your recommendation, the better.\u201d",
     "Verbatim", ["S44"]),
    ("FTC: \u201caffiliate link\u201d alone is not enough", "Content & compliance",
     "\u201cConsumers might not understand that \u2018affiliate link\u2019 means that the person placing the link is getting paid \u2026 Similarly, a \u2018buy now\u2019 button would not be adequate.\u201d",
     "Verbatim", ["S44"]),
    ("FTC: disclosure must be hard to miss", "Content & compliance",
     "\u201cPlace it so it\u2019s hard to miss.\u201d and \u201cYou can\u2019t talk about your experience with a product you haven\u2019t tried.\u201d (Disclosures 101, dated November 2019)",
     "Verbatim", ["S07"]),
]


def build_verification() -> None:
    """Line-by-line verification log for the final integration session edbd56a1."""
    rows = []
    for n, (claim, used_on, observed, result, srcs) in enumerate(VERIFY_ROWS, start=1):
        cls = "ok" if result in ("Verbatim", "Observed") else "info"
        rows.append([str(n), e(claim), e(used_on), observed, badge(result, cls), src_links(srcs)])
    body = (
        "<h2>What this log is</h2>"
        '<p>Every claim this site publishes, re-read against the official page it cites on '
        "<strong>2026-11-14</strong> by the final integration session <code>edbd56a1</code>, "
        "independently of the sessions that first recorded it. A row is here because the quoted "
        "text or the observed response was on the page when it was fetched. Nothing is inferred, "
        "and no value that could not be confirmed is filled in.</p>"
        "<h2>How to read the Result column</h2>"
        "<ul>"
        "<li><strong>Verbatim</strong> \u2014 the text in the \u201cwhat the official page says\u201d column is copied from the page.</li>"
        "<li><strong>Observed</strong> \u2014 a live page result recorded as it was returned (a redirect destination, a title, or a Page Not Found). It is a fact about the response, not proof about the submitted product.</li>"
        "<li><strong>Negative evidence</strong> \u2014 the page could not be read, so nothing is taken from it.</li>"
        "</ul>"
        + table(["#", "Claim", "Where it is used on this site", "What the official page says (2026-11-14)",
                 "Result", "Source"], rows, "verify")
        + "<h2>Coverage and limits</h2>"
        "<ul>"
        "<li>Every policy fact in <code>data/policy_facts.json</code> was re-checked against its source page in this session; the rows above are the ones the site actually renders.</li>"
        "<li>All three submitted links were re-fetched, and all three direct <code>/dp/&lt;id&gt;</code> checks were re-run. The results are unchanged from 2026-11-13.</li>"
        "<li>Prices, star ratings and review counts are deliberately absent from every page, so there is no row for them (FLG-022).</li>"
        "<li>The sandbox this site is built in can reach only github.com, npm and PyPI directly, so official pages were read through the fetch tool rather than by an automated HTTP client. No source was checked with <code>--online</code>.</li>"
        "</ul>"
    )
    page("verification.html", "Verification log", body,
         lead="Line-by-line re-verification of every claim this site publishes, against the official source that backs it. Read on 2026-11-14 by the final integration session.")


def build_legacy_stubs() -> None:
    """Old URLs from PR #1 (session 26634cd5). They redirect to the pages that replace them."""
    stubs = {
        "analysis.html": "executive-summary.html",
        "disclosure.html": "content.html",
        "categories/home-kitchen-air-fryers.html": "products.html",
        "flagged-for-review.html": "flagged.html",
        "marketing.html": "marketing/index.html",
    }
    for name, target in stubs.items():
        path = ROOT / name
        path.parent.mkdir(parents=True, exist_ok=True)
        rel = "../" + target if "/" in name else target
        path.write_text(
            '<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta http-equiv="refresh" content="0; url={rel}">'
            '<link rel="canonical" href="' + rel + '">'
            '<title>Moved</title></head><body>'
            f'<p>This page has moved to <a href="{rel}">{rel}</a>.</p></body></html>\n',
            encoding="utf-8",
        )



def build_decision_center() -> None:
    """Decision support. Recommendations are proposals; sources support factual claims only."""
    policy = src_links(["S02"])
    asin = src_links(["S31", "S45"])
    api = src_links(["S04", "S05"])
    rates = src_links(["S03", "S25", "S26"])
    disclosure = src_links(["S01", "S07", "S24"])
    body = f"""
<style>
.decision-intro{{background:linear-gradient(120deg,#0f2f22,#17402e);color:#fff;border-radius:16px;padding:26px clamp(18px,4vw,38px);margin:8px 0 20px}}
.decision-intro .eyebrow{{text-transform:uppercase;letter-spacing:.12em;font-size:12px;font-weight:700;color:#e8d9be}}
.decision-intro h2{{font-size:clamp(24px,4vw,36px);line-height:1.15;margin:5px 0 10px;max-width:760px}}
.decision-intro p{{color:#e9f0e8;max-width:800px}}
.decision-section{{margin:28px 0}}
.question-grid,.choice-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:13px}}
.question,.choice{{background:#fffdf8;border:1px solid #e4dfcf;border-radius:12px;padding:16px}}
.question h3,.choice h3{{font-size:16px;margin:0 0 7px}}
.question p,.choice p{{margin:7px 0}}
.answer{{border-left:3px solid #198754;padding-left:10px}}
.missing{{border-left:3px solid #c37a00;padding-left:10px}}
.choice label{{font-weight:700;font-size:13px;display:block;margin-top:12px}}
.choice select{{width:100%;padding:9px;border-radius:7px;border:1px solid #cbd3df;font:inherit;background:#fff}}
.savebar{{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:12px 0}}
.savebar button{{background:#17402e;color:#fff;border:0;border-radius:7px;padding:9px 13px;font:inherit;cursor:pointer}}
.savebar output{{color:#5b6474;font-size:13px}}
.proposal{{border-left:4px solid #1e6b47;padding:2px 0 2px 14px;margin:17px 0}}
.proposal h3{{margin:0 0 5px;font-size:17px}}
.pill{{display:inline-block;border-radius:999px;background:#e7f2ec;color:#1e5c3f;padding:3px 9px;font-size:12px;font-weight:700}}
</style>
<section class="decision-intro">
  <p class="eyebrow">Decision Center · prepared 2026-11-15</p>
  <h2>Decide what to verify before the next page goes live.</h2>
  <p>This is a sourced decision brief, not a claim that every automation feature is already built. It separates known facts from missing inputs, ranks practical next steps, and offers a review queue. The factual source register was last re-verified on 2026-11-14; this page does not claim a fresh live re-check of Amazon data.</p>
  <p><a href="executive-summary.html" style="color:#fff">Executive summary</a> · <a href="flagged.html" style="color:#fff">All flagged items</a> · <a href="sources.html" style="color:#fff">Official source register</a></p>
</section>

<section class="decision-section">
  <h2>Executive readout</h2>
  <div class="question-grid">
    <article class="question"><span class="pill">Known</span><h3>Three supplied links; product intent is not confirmed</h3><p>The project register records three short-link tokens and leaves product identity for the submitted identifiers unconfirmed. Amazon's API reference defines ASINs as ten-character identifiers. {asin} See <a href="products.html">Products</a> and <a href="flagged.html#FLG-001">FLG-001 / FLG-002</a>.</p></article>
    <article class="question"><span class="pill">Blocked input</span><h3>API and performance data are not connected</h3><p>Amazon's Creators API documentation states an eligibility prerequisite of at least 10 qualifying sales in the past 30 days; the repository has no verified account eligibility or live account report. {api} See <a href="campaigns.html">Campaigns &amp; tracking</a> and <a href="flagged.html#FLG-006">FLG-006</a>.</p></article>
    <article class="question"><span class="pill">Recommendation</span><h3>Keep product-specific monetized claims on hold</h3><p>Publish useful evergreen buying education now; do not turn observed redirect destinations into assumed product intent. Reopen product-specific recommendations after the intended ASINs and permitted tracking links have been confirmed. This is a risk-control recommendation, not an Amazon quote.</p></article>
  </div>
</section>

<section class="decision-section">
  <h2>What we know, what is missing, and how to discover it</h2>
  <p>Answers below are limited to the repository's sourced record and official program documents. “Unknown” means the current evidence does not settle it; it is not a guess.</p>
  <div class="question-grid">
    <article class="question"><h3>1 · Which exact three products should be promoted?</h3><p class="answer"><strong>Known:</strong> The supplied link codes are nine characters; the official Amazon API reference describes ASIN identifiers as ten characters. {asin}</p><p class="missing"><strong>Missing:</strong> Owner-confirmed intended listing / ASIN mapping. Redirect observations do not establish intent. <a href="flagged.html#FLG-001">FLG-001</a> · <a href="flagged.html#FLG-002">FLG-002</a></p><p><strong>Discovery:</strong> Resolve the short-link owner/source, obtain the intended Amazon product URLs directly from the campaign brief, and compare each to the intended product before writing product-specific claims.</p></article>
    <article class="question"><h3>2 · Can the platform fetch product content automatically?</h3><p class="answer"><strong>Known:</strong> Creators API documentation lists eligibility prerequisites, including at least 10 qualifying sales in the prior 30 days. The PA-API 5 deprecation notice and Creators API introduction are in the source register. {api}</p><p class="missing"><strong>Missing:</strong> Associates enrollment, qualifying-sales status, API access approval, marketplace, credentials and an authorized data-use path. <a href="flagged.html#FLG-006">FLG-006</a></p><p><strong>Discovery:</strong> Check Associates Central eligibility and API access; use a secrets manager for credentials. Never place keys in this public static repository. The answer is not assumed by this build.</p></article>
    <article class="question"><h3>3 · Which facts may appear beside affiliate links?</h3><p class="answer"><strong>Known:</strong> Amazon policy sets conditions for displaying price/availability and customer ratings/reviews; see sections 2(b) and 6(t) in the policies. {policy}</p><p class="missing"><strong>Missing:</strong> An approved data route for each live product and a verified match between each fact and the intended ASIN. <a href="pricing.html">Pricing</a> · <a href="reviews.html">Reviews</a></p><p><strong>Discovery:</strong> Keep volatile price, rating, review count and rank fields blank until the exact product and policy-permitted source path are verified. Do not convert old screenshots or snapshots into live offers.</p></article>
    <article class="question"><h3>4 · Are the submitted links suitable for affiliate attribution?</h3><p class="answer"><strong>Known:</strong> Amazon policy says links must not obscure that they lead to Amazon; the commission statement defines “Redirecting Link” and its consequence. {policy}</p><p class="missing"><strong>Missing:</strong> Whether these particular short links meet the applicable link and attribution requirements, and whether a valid Associates tracking tag is attached. <a href="flagged.html#FLG-003">FLG-003</a></p><p><strong>Discovery:</strong> Prefer tested Special Links generated in Associates Central; validate destination clarity and tracked-click reporting before publication. This is a prudent recommendation; applicability of policy to the given links remains flagged.</p></article>
    <article class="question"><h3>5 · What commission and revenue can be forecast?</h3><p class="answer"><strong>Known:</strong> Amazon publishes standard and onsite category tables, while the account schedule is a separate source. The current record does not assign a per-product rate. {rates}</p><p class="missing"><strong>Missing:</strong> Confirmed product category, account-specific rate, eligible sessions, qualifying orders, cancellations and actual commission reports. <a href="flagged.html#FLG-005">FLG-005</a> · <a href="campaigns.html">Campaign ledger</a></p><p><strong>Discovery:</strong> Obtain the rate applicable to the intended ASIN and a date-bounded performance report. Do not fabricate a “potential earnings” number from category averages.</p></article>
    <article class="question"><h3>6 · Which niche or article is actually trending?</h3><p class="answer"><strong>Known:</strong> No verified trend or search-volume evidence is included in this project's approved inputs. An article title is an editorial hypothesis, not demand proof.</p><p class="missing"><strong>Missing:</strong> Audience geography, first-party queries, search impressions/clicks, seasonality window, competitor set and conversion performance.</p><p><strong>Discovery:</strong> Connect the publisher's own search-performance export and Associates reports, date and preserve each measurement, then rank topics against observed demand. No score is assigned while inputs are absent.</p></article>
    <article class="question"><h3>7 · Which commission marketplace and disclosure apply?</h3><p class="answer"><strong>Known:</strong> Operating Agreement Schedule 1 lists United States / Amazon.com for its listed program entity. The Associates disclosure statement and FTC endorsement resources are in the cited register. {disclosure}</p><p class="missing"><strong>Missing:</strong> Publisher location, audience locations, enrolled marketplace(s), legal entity and channel-specific disclosure placement.</p><p><strong>Discovery:</strong> Confirm those account and audience details before expanding beyond Amazon.com. Keep the Associate disclosure clear and proximate to recommendations; confirm local legal requirements for each market.</p></article>
    <article class="question"><h3>8 · What can safely publish before inputs arrive?</h3><p class="answer"><strong>Known:</strong> Source-backed buying education can explain comparison criteria without asserting unsupported product performance. Amazon policy and FTC resources remain the relevant compliance anchors. {policy} {disclosure}</p><p class="missing"><strong>Missing:</strong> First-party audience evidence to validate which topic deserves priority.</p><p><strong>Discovery:</strong> Publish an evergreen checklist only after editorial review; record impressions and clicks once a compliant measurement route exists. Product-specific price/rating copy stays out until the evidence gate passes.</p></article>
  </div>
</section>

<section class="decision-section">
  <h2>Suggestions to review before implementation</h2>
  <p>Priority is based on resolving blockers and reducing unsupported claims, not on assumed conversion lift. Editorial topic labels below are not verified trend rankings.</p>
  <div class="proposal"><span class="pill">Priority 1 · unblock identity</span><h3>Build a product-intent confirmation record</h3><p>For each submitted link, store the intended ASIN, official listing URL, confirmation date, and source. Keep observed redirect targets in a separate field. Do not merge the two fields. Rationale: Amazon's ASIN definition provides a checkable identifier format. {asin}</p></div>
  <div class="proposal"><span class="pill">Priority 2 · attribution safety</span><h3>Replace ambiguous outbound links with validated Special Links</h3><p>Test one link per product in the enrolled Associates workflow and confirm destination and tracking report before scaling. Do not claim that the supplied short links are invalid; their exact compliance status is unresolved in <a href="flagged.html#FLG-003">FLG-003</a>. {policy}</p></div>
  <div class="proposal"><span class="pill">Priority 3 · editorial value</span><h3>Lead with useful, human-sounding buyer questions</h3><p>Suggested editorial hypotheses: “Basket or oven-style air fryer: what should you compare?”, “A no-hype checklist for comparing air fryer capacity”, “How to assess cleanup and counter-space trade-offs”, and “Questions to ask before buying a multi-function kitchen appliance.” These are working titles—not claims about popularity, search volume or product superiority.</p></div>
  <div class="proposal"><span class="pill">Priority 4 · evidence-based iteration</span><h3>Measure before automating optimization</h3><p>Start with an empty but well-defined campaign ledger; add timestamp, source, channel, eligible sessions, clicks and reported orders only when obtained from authorized first-party reports. Keep a dated provenance trail. No conversion score or revenue forecast is presented here.</p></div>
  <div class="proposal"><span class="pill">Priority 5 · compliance gate</span><h3>Put disclosures and API policy checks in the publishing workflow</h3><p>Keep the Associates statement visible and review disclosure placement and endorsement context against the Operating Agreement and FTC guidance. {disclosure}</p></div>
</section>

<section class="decision-section" id="review-choices">
  <h2>Reviewable paths</h2>
  <p>Choose a path for discussion before implementation. Choices are stored only in this browser's local storage; they are not submitted to the site, repository, or project owner. No option triggers a code or content change.</p>
  <div class="savebar"><button type="button" id="clear-choices">Clear local choices</button><output id="choice-status" aria-live="polite">No path selected yet.</output></div>
  <div class="choice-grid">
    <article class="choice"><h3>A · Product content gate</h3><p><strong>Recommended:</strong> confirm the intended ASINs first; publish category-level evergreen content in the meantime.</p><label for="path-products">Path for review</label><select id="path-products" data-choice><option value="">No choice yet</option><option value="confirm">Confirm exact products, then write product-specific copy</option><option value="evergreen">Publish only general buying education until confirmed</option><option value="hold">Hold all new marketing pages</option></select><p>Evidence: ASIN definition {asin} · open item <a href="flagged.html#FLG-001">FLG-001</a>.</p></article>
    <article class="choice"><h3>B · Product data source</h3><p><strong>Recommended:</strong> verify API eligibility and approved access before building automated product-data refresh.</p><label for="path-data">Path for review</label><select id="path-data" data-choice><option value="">No choice yet</option><option value="api">Check eligibility and pursue Creators API access</option><option value="editorial">Keep product fields blank; use sourced static editorial claims</option><option value="reports">First connect the publisher's approved campaign reports</option></select><p>Evidence: Creators API prerequisites {api} · open item <a href="flagged.html#FLG-006">FLG-006</a>.</p></article>
    <article class="choice"><h3>C · Affiliate links</h3><p><strong>Recommended:</strong> validate and test Associates-generated Special Links before publishing conversion CTAs.</p><label for="path-links">Path for review</label><select id="path-links" data-choice><option value="">No choice yet</option><option value="special">Use tested Associates-generated Special Links</option><option value="investigate">Investigate current links before deciding</option><option value="hold">Hold outbound CTAs pending review</option></select><p>Evidence: Amazon link clarity and redirecting-link policy {policy} · open item <a href="flagged.html#FLG-003">FLG-003</a>.</p></article>
    <article class="choice"><h3>D · Editorial launch</h3><p><strong>Recommended:</strong> start with one evergreen comparison checklist, then review first-party performance before expanding.</p><label for="path-editorial">Path for review</label><select id="path-editorial" data-choice><option value="">No choice yet</option><option value="checklist">One evergreen comparison checklist</option><option value="guide">A category buying guide plus topic cluster</option><option value="wait">Wait for audience and search data first</option></select><p>These are proposed workflows, not measured performance claims.</p></article>
  </div>
</section>

<section class="decision-section">
  <h2>Implementation gate</h2>
  <ol>
    <li>Record intended product identifiers and account marketplace. Link each claim to an official listing or policy page.</li>
    <li>Confirm an eligible, approved data-access route before importing price, availability, review, or rating information. {policy} {api}</li>
    <li>Test link behavior and reporting; document any unresolved policy ambiguity rather than treating an observation as approval. {policy}</li>
    <li>Publish a disclosure alongside recommendations. {disclosure}</li>
    <li>Only then build ranking and optimization from actual dated reports. Until then, keep conversion and revenue values blank.</li>
  </ol>
  <p>See the <a href="flagged.html">Flagged for review</a> register for the open evidence gaps, <a href="products.html">product audit</a> for the intake status, and <a href="executive-summary.html">executive summary</a> for the full project status.</p>
</section>
<script>
(()=>{{
 const key='zone3-decision-center-v1';
 const controls=[...document.querySelectorAll('[data-choice]')];
 const output=document.getElementById('choice-status');
 const read=()=>{{try{{return JSON.parse(localStorage.getItem(key)||'{{}}')}}catch(e){{return {{}}}}}};
 const saved=read();
 controls.forEach(el=>{{el.value=saved[el.id]||'';el.addEventListener('change',()=>{{const next=read();if(el.value)next[el.id]=el.value;else delete next[el.id];try{{localStorage.setItem(key,JSON.stringify(next))}}catch(e){{}};update()}})}});
 function update(){{const n=controls.filter(el=>el.value).length;output.textContent=n?`${{n}} of ${{controls.length}} paths selected in this browser only.`:'No path selected yet.'}}
 document.getElementById('clear-choices').addEventListener('click',()=>{{try{{localStorage.removeItem(key)}}catch(e){{}};controls.forEach(el=>el.value='');update()}});
 update();
}})();
</script>
"""
    page("decision-center.html", "Decision Center", body,
         lead="A sourced decision brief: current answers, missing information, discovery steps, editorial suggestions and paths to review before implementation.")



def main() -> None:
    build_assets()
    build_index()
    build_decision_center()
    build_exec()
    build_products()
    build_pricing()
    build_reviews()
    build_marketing()
    build_content()
    build_topics()
    build_suggestions()
    build_design_brief()
    build_decision_queue()
    build_campaigns()
    build_flagged()
    build_category()
    build_sources()
    build_verification()
    build_legacy_stubs()
    # Session 5a56c084 (2026-11-16): the Research Desk (articles/) and this session's
    # verification record are generated from data/articles.json and
    # sessions/5a56c084/verification-2026-11-16.json by scripts/build_5a56c084.py,
    # which imports this module's template. Run here so one command rebuilds
    # everything and no gate can pass with a stale article layer.
    import build_5a56c084
    build_5a56c084.main()
    print("built site in", ROOT)


if __name__ == "__main__":
    main()

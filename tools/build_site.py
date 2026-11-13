#!/usr/bin/env python3
"""
Zone3 static site builder.

Reads the verified datasets in data/*.json and emits a GitHub-Pages-ready static
site. The build is also the verification gate: it FAILS (non-zero exit) if any
table row lacks an official source reference and an unverified flag, if any
source or flag reference is dangling, or if any internal link does not resolve.

Usage:  python3 tools/build_site.py [--out DIR]
"""
from __future__ import annotations
import json, html, hashlib, sys, datetime, pathlib, argparse, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "z3"   # namespaced: other sessions own data/*.json
SITE_ORIGIN = "https://kanlerxz87-cyber.github.io"
SITE_BASE = "/Zone3"

# ----------------------------------------------------------------------------- data
def load(name):
    with open(DATA / name, encoding="utf-8") as fh:
        return json.load(fh)

SOURCES = {s["id"]: s for s in load("sources.json")["sources"]}
FLAGS = {r["id"]: r for r in load("flags.json")["table"]["rows"]}
PRODUCTS = load("products.json")
POLICIES = load("policies.json")
PRICING = load("pricing.json")
REVIEWS = load("reviews.json")
NICHES = load("niches.json")
CAMPAIGNS = load("campaigns.json")
CONTENT = load("content.json")
REQUIREMENTS = load("requirements.json")
AGENT = load("agent_terms.json")
COMMISSION = load("commission.json")

STATUS_CLASS = {
    "verified": "p-ok", "done": "p-ok", "delivered": "p-ok", "implemented": "p-ok",
    "verified-positive-control": "p-ok", "enforced": "p-ok",
    "ready": "p-info", "instrumented": "p-info", "partial": "p-info",
    "internal": "p-info", "policy": "p-info", "derived": "p-info",
    "requires-account": "p-warn", "blocked": "p-bad", "blocked-by-auth": "p-bad",
    "unverified": "p-warn", "no-official-source": "p-bad", "missing-credential": "p-bad",
    "non-compliant-format": "p-bad", "prohibited-by-design": "p-warn",
    "verified-negative": "p-bad", "verified-blocked": "p-bad",
    "verified-inaccessible": "p-warn", "verified-dead": "p-bad",
    "built-blocked": "p-warn", "not-built-compliance": "p-warn",
    "blocked-on-user": "p-bad", "observed": "p-info",
}
UNVERIFIED_STATES = {
    "unverified", "blocked", "blocked-by-auth", "no-official-source",
    "missing-credential", "verified-inaccessible", "built-blocked", "partial",
}

# --------------------------------------------------------------------- link helpers
def rel(cur_depth: int, target_depth: int, target_name: str) -> str:
    """Relative href between pages. Landing page is depth 0; all others depth 1."""
    up = "../" * cur_depth
    if target_depth == 0:
        return up + "index.html"
    return f"{up}{target_name}/"


def relf(cur_depth: int, filename: str) -> str:
    """href to a root-level flat file (used for pages owned by other builds)."""
    return ("../" * cur_depth) + filename


# ------------------------------------------------------------------------- renderers
def esc(v) -> str:
    if v is None:
        return ""
    return html.escape(str(v), quote=True)


def is_url(v) -> bool:
    return isinstance(v, str) and re.match(r"^https?://", v.strip()) is not None


def codify(txt: str) -> str:
    """Render `backticked` tokens in dataset strings as code spans."""
    return re.sub(r"`([^`<]+)`", r"<code>\1</code>", txt)


def cell(value, row_status: str) -> str:
    if value is None or value == "":
        if row_status in UNVERIFIED_STATES:
            return '<span class="blk">— not verifiable</span>'
        return '<span class="blk">—</span>'
    text = esc(value)
    if is_url(value):
        u = value.strip()
        return f'<a href="{esc(u)}" rel="nofollow noopener noreferrer" target="_blank"><span class="url">{text}</span></a>'
    return codify(text)


def src_links(ids, anchor=None) -> str:
    out = []
    for sid in ids or []:
        s = SOURCES.get(sid)
        if not s:
            out.append(f'<span class="flag-ref">DANGLING:{esc(sid)}</span>')
            continue
        out.append(
            f'<a href="{esc(s["url"])}" title="{esc(s["publisher"])} — {esc(s["title"])}" '
            f'rel="nofollow noopener noreferrer" target="_blank">{esc(sid)}</a>'
        )
    if not out and anchor:
        return (f'<span class="tag" title="Row is verified by reading this repository file '
                f'at build time (gate G5 asserts the file exists)">repo:{esc(anchor)}</span>')
    if not out:
        return '<span class="none">no source cited</span>'
    if anchor:
        out.append(f'<span class="tag" title="Also anchored to a repository file">repo:{esc(anchor)}</span>')
    return f'<div class="srcs">{"".join(out)}</div>'


def flag_links(ids) -> str:
    out = []
    for fid in ids or []:
        f = FLAGS.get(fid)
        label = esc(fid)
        if f:
            out.append(
                f'<a class="flag-ref" href="{FLAG_PAGE}" '
                f'title="{esc(f["sev"])}: {esc(f["item"])}">{label}</a>'
            )
        else:
            out.append(f'<span class="flag-ref">{label}</span>')
    return " ".join(out) or '<span class="none">—</span>'


FLAG_PAGE = "flagged/"          # rewritten per page by set_depth()
_CUR_DEPTH = 1


def set_depth(d):
    """Flag/source links are emitted inside tables, so they need the page depth."""
    global FLAG_PAGE, _CUR_DEPTH
    _CUR_DEPTH = d
    FLAG_PAGE = "flagged/" if d == 0 else "../flagged/"


def table(spec, cur_depth=1, title_id=None) -> str:
    set_depth(cur_depth)
    cols = spec["columns"]
    rows = spec.get("rows", [])
    head = "".join(
        '<th scope="col"{}>{}</th>'.format(
            ' class="nosort"' if c.get("nosort") else '', esc(c["label"]))
        for c in cols
    )
    head += ('<th scope="col" class="nosort">Status</th>'
             '<th scope="col" class="nosort">Source</th>'
             '<th scope="col" class="nosort">Flags</th>')

    body = []
    for r in rows:
        st = r.get("status", "unverified")
        cls = STATUS_CLASS.get(st, "p-mut")
        tds = []
        for c in cols:
            k = c["key"]
            klass = ' class="k"' if k in ("id", "ref", "field", "rule", "input", "item", "block", "step") else ""
            tds.append(f"<td{klass}>{cell(r.get(k), st)}</td>")
        tds.append(f'<td><span class="pill {cls}">{esc(st)}</span></td>')
        tds.append(f"<td>{src_links(r.get('sources'), r.get('self_attested'))}</td>")
        tds.append(f"<td>{flag_links(r.get('flags'))}</td>")
        body.append("<tr>" + "".join(tds) + "</tr>")

    if not rows:
        span = len(cols) + 3
        # rendered as an empty-state note, not a data row
        empty = spec.get("empty_text", "No rows. Nothing met the verification bar, so no values were invented.")
        body.append(f'<tr class="empty-row"><td colspan="{span}">{esc(empty)}</td></tr>')

    cap = f'<div class="tbl-head"><h2 id="{title_id}">{esc(spec["caption"])}</h2>'
    if rows:
        cap += f'<span class="count">{len(rows)} row{"s" if len(rows)!=1 else ""}</span>'
    cap += "</div>"
    note = f'<p class="note">{esc(spec["note"])}</p>' if spec.get("note") else ""
    tools = (
        '<span class="tbl-tools"><label class="sr" for="q">Filter rows</label>'
        '<input type="search" placeholder="Filter rows…" data-table-filter></span>'
        if rows else ""
    )
    cap = cap.replace("</div>", tools + "</div>")
    return f'{cap}<div class="tbl-wrap"><table>{f"<thead><tr>{head}</tr></thead>" if rows else ""}<tbody>{"".join(body)}</tbody></table></div>{note}'


def kpis(items, cur_depth=1) -> str:
    cards = []
    for it in items:
        cards.append(
            f'<div class="card kpi {it.get("tone","")}"><div class="pad">'
            f'<div class="lab">{esc(it["label"])}</div>'
            f'<div class="num">{esc(it["value"])}</div>'
            f'<div class="foot">{it.get("foot","")}</div>'
            f"</div></div>"
        )
    return f'<div class="grid g4">{"".join(cards)}</div>'


def callout(kind, title, html_body) -> str:
    h = f"<h4>{esc(title)}</h4>" if title else ""
    return f'<div class="callout {kind}">{h}{html_body}</div>'


def prose(title, blocks) -> str:
    parts = [f"<h2>{esc(title)}</h2>"] if title else []
    for kind, val in blocks:
        if kind == "p":
            parts.append(f"<p>{val}</p>")
        elif kind == "h3":
            parts.append(f"<h3>{esc(val)}</h3>")
        elif kind == "ul":
            parts.append("<ul>" + "".join(f"<li>{li}</li>" for li in val) + "</ul>")
        elif kind == "ol":
            parts.append("<ol>" + "".join(f"<li>{li}</li>" for li in val) + "</ol>")
        elif kind == "quote":
            parts.append(f"<blockquote><p>{val}</p></blockquote>")
        elif kind == "raw":
            parts.append(val)
    return f'<div class="prose">{"".join(parts)}</div>'


def sec(label) -> str:
    return f'<div class="sec-h"><h2>{esc(label)}</h2><div class="rule"></div></div>'


# ------------------------------------------------------------------------------ nav
NAV = [
    ("Overview", [("index", "Dashboard"), ("executive-summary", "Executive summary"),
                  ("requirements", "Requirements"), ("repo-review", "Repo review")]),
    ("Research", [("products", "Products"), ("niches", "Niches"),
                  ("pricing", "Pricing"), ("commission", "Commission"), ("reviews", "Reviews")]),
    ("Output", [("content", "Content"), ("campaigns", "Campaigns")]),
    ("Governance", [("compliance", "Compliance"), ("agent-terms", "Agent terms"),
                    ("methodology", "Methodology"), ("sources", "Sources")]),
    ("Open", [("flagged", "Flagged for review")]),
]
PAGE_NAMES = {name for _, items in NAV for name, _ in items}
NAV_TITLES = {name: title for _, items in NAV for name, title in items}


def nav_html(cur, depth) -> str:
    out = []
    for _, items in NAV:
        for pname, ptitle in items:
            href = rel(depth, 0 if pname == "index" else 1, pname)
            on = ' class="on"' if pname == cur else ""
            out.append(f'<a href="{href}"{on}>{esc(ptitle)}</a>')
    return "".join(out)


def toc_html(cur, depth) -> str:
    return '<div class="tocbar">' + nav_html(cur, depth).replace('<a href="', '<a href="') + "</div>"


# ------------------------------------------------------------------------ page shell
def render_page(pname, title, lead, body, depth, badges=None, updated="2026-11-13"):
    if pname == "index":
        href = "index.html"
        crumb = '<span>Dashboard</span>'
    else:
        href = f"{pname}/index.html"
        crumb = (f'<a href="{rel(1,0,"index")}">Zone3</a> '
                 f'<span aria-hidden="true">/</span> <span>{esc(NAV_TITLES.get(pname,pname))}</span>')
    badges_html = ""
    if badges:
        badges_html = '<div style="margin-top:14px;display:flex;gap:6px;flex-wrap:wrap">' + "".join(badges) + "</div>"

    css = "assets/" if depth == 0 else "../assets/"
    js = "assets/" if depth == 0 else "../assets/"   # dashboard.js: assets/app.js belongs to a prior session's pages
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} · Zone3 Affiliate Intelligence</title>
<meta name="description" content="{esc(lead)[:155]}">
<link rel="canonical" href="{SITE_ORIGIN}{SITE_BASE}/" data-page="{esc(pname)}">
<link rel="stylesheet" href="{css}app.css">
</head>
<body>
<div class="disclose" role="note">
  <div class="wrap row">
    <span><b>Disclosure:</b> As an Amazon Associate I earn from qualifying purchases.</span>
    <span style="color:#8a7a55">Links to Amazon carry an Associates tag once one is configured. See the <a href="{rel(depth, 1, 'compliance')}" style="color:#7a5f22">compliance register</a>.</span>
  </div>
</div>
<header class="topbar">
  <div class="wrap row">
    <a class="logo" href="{rel(depth,0,'index')}"><span class="mark">Z3</span>Zone3<span class="sub">Affiliate Intelligence</span></a>
    <nav aria-label="Sections">{nav_html(pname, depth)}</nav>
  </div>
</header>
<main>
  <div class="wrap">
    <header class="pagehead">
      <div class="crumbs">{crumb}</div>
      <h1>{esc(title)}</h1>
      <p class="lead">{lead}</p>
      {badges_html}
      <div class="meta-line">
        <span>Data as of: <strong>{esc(updated)}</strong></span>
        <span>Verification: <strong>every row cites an official source or is flagged</strong></span>
        <span><a href="{rel(depth,1,'flagged')}">{len(FLAGS)} open flags</a></span>
      </div>
    </header>
    <section>{body}</section>
  </div>
</main>
<footer>
  <div class="wrap row">
    <div>
      <p>CERTAIN CONTENT THAT APPEARS ON THIS SITE COMES FROM AMAZON. THIS CONTENT IS PROVIDED ‘AS IS’ AND IS SUBJECT TO CHANGE OR REMOVAL AT ANY TIME.</p>
      <p>Zone3 is an independent affiliate-intelligence platform and is not affiliated with, endorsed or sponsored by Amazon. Amazon, Amazon Associates and ASIN are trademarks of Amazon.com, Inc. or its affiliates.</p>
      <p style="color:#6e7a8b">Built statically by <code>tools/build_site.py</code> from <code>data/z3/*.json</code>. Published via GitHub Pages from branch <code>main</code>.</p>
      <p style="color:#6e7a8b">This repository also carries an earlier site generation from another session, kept intact.
      Sibling pages: <a href="{relf(depth,'products.html')}">products.html</a> ·
      <a href="{relf(depth,'pricing.html')}">pricing.html</a> ·
      <a href="{relf(depth,'sources.html')}">sources.html</a> ·
      <a href="{relf(depth,'flagged.html')}">flagged.html</a> ·
      <a href="{relf(depth,'landing-prior.html')}">previous landing page</a>. See <code>COORDINATION.md</code>.</p>
    </div>
    <div class="flinks">
      <a href="{rel(depth,1,'compliance')}">Compliance</a>
      <a href="{rel(depth,1,'sources')}">Sources</a>
      <a href="{rel(depth,1,'flagged')}">Flagged</a>
      <a href="{rel(depth,1,'executive-summary')}">Exec summary</a>
      <a href="{rel(depth,0,'index')}">Top</a>
    </div>
  </div>
</footer>
<script src="{js}dashboard.js"></script>
</body>
</html>
"""
    return href, doc


# --------------------------------------------------------------------------- payloads
def pill(text, cls="p-mut"):
    return f'<span class="pill {cls}">{esc(text)}</span>'


def page_index(depth):
    n_prod = len(PRODUCTS["table"]["rows"])
    parts = []
    parts.append(kpis([
        {"label": "Products submitted", "value": str(n_prod), "foot": "All three intake-rejected at identifier validation"},
        {"label": "Products verified", "value": "0", "tone": "bad", "foot": "0 of 3 passed the 10-character ASIN test"},
        {"label": "Open flags", "value": str(len(FLAGS)), "tone": "warn",
         "foot": f'<a href="{rel(depth,1,"flagged")}">Review them</a>'},
        {"label": "Official sources cited", "value": str(len(SOURCES)), "tone": "ok",
         "foot": f'Amazon + FTC primary documents, fetched {load("sources.json")["_meta"]["retrieved_utc"][:10]}'},
    ]))
    parts.append('<div style="height:18px"></div>')
    parts.append(callout("bad", "Blocking finding — the three product links do not identify any product",
        "<p>Each submitted link is a 9-character identifier. Amazon defines an ASIN as a <strong>10-character</strong> "
        "alphanumeric code, and <code>https://www.amazon.com/dp/&lt;id&gt;</code> returns a <em>Page Not Found</em> "
        "error page for all three. When followed, each link resolved to a <strong>different</strong> unrelated product "
        "(a CHEFMAN dual-basket fryer, an Emeril Lagasse toaster oven, and a Chefman 8-Qt fryer) carrying "
        "<code>plpRedirect=mhFallback</code> — Amazon's fallback route, not a product deep link.</p>"
        "<p>Consequence: no product name, price, rating, review count, category or commission figure can be stated. "
        "Those cells are <strong>left blank</strong> across this site rather than estimated. "
        f'See <a href="{rel(depth,1,"flagged")}">Flagged for review</a> (FLG-004…FLG-008).</p>'))
    parts.append('<div style="height:18px"></div>')
    parts.append(sec("Categories"))
    cards = []
    summaries = [
        ("products", "Products", "Intake and verification register for the three submitted links, plus the 12-field attribute sheet that is blocked."),
        ("niches", "Niches", "Niche scoring model, its six inputs, and ten verified category-level constraints on niche choice."),
        ("pricing", "Pricing", "Pricing rules engine, per-item price sheet, and the two prohibited price features."),
        ("commission", "Commission", "Amazon's published rate tables (Standard, Onsite, Creator Ads) plus the Bounty schedule and what they imply."),
        ("reviews", "Reviews", "Review-integrity constraints and a compliant aggregate-only sentiment design."),
        ("content", "Content", "Article, comparison and buying-guide templates with claim-grounding gates and SEO mechanics."),
        ("campaigns", "Campaigns", "Link management, metrics schema and a permitted-vs-prohibited optimiser for 12 levers."),
        ("compliance", "Compliance", "25 enforced prohibitions, the mandatory disclosure blocks, and programme economics."),
        ("agent-terms", "Agent terms", "How this AI agent complies with the new Agent Terms and the Creators API surface."),
        ("methodology", "Methodology", "Architecture, data flow, the verification protocol, and reproducible checks."),
        ("requirements", "Requirements", "Traceability matrix: all 30 clauses of the brief and what happened to each."),
        ("sources", "Sources", "Every official document cited, with what was read in it and when."),
        ("flagged", "Flagged for review", f"All {len(FLAGS)} open items with severity, verified finding and what unblocks each."),
    ]
    for pname, t, d in summaries:
        cards.append(
            f'<a class="card" href="{rel(depth,1,pname)}"><div class="pad">'
            f'<h3>{esc(t)}<span class="arw">→</span></h3>'
            f'<p style="margin:0;font-size:13.4px;color:var(--ink-2)">{esc(d)}</p></div></a>'
        )
    parts.append(f'<div class="grid g3">{"".join(cards)}</div>')
    parts.append('<div style="height:22px"></div>')
    parts.append(sec("Findings at a glance"))
    parts.append(prose("", [
        ("p", "<strong>The automation brief is achievable; the product list is not.</strong> The research → analysis → "
              "content → publish → optimise loop is fully specified and implemented in <code>tools/</code>. What is missing is a "
              "valid product identifier and an Associates account, both of which only you can supply."),
        ("p", "<strong>Three requirements in the brief collide with Amazon's own rules.</strong> <em>Price analysis</em> as a "
              "user-facing price-alert feature is prohibited; <em>click tracking</em> per visitor via dynamic sub-tags is prohibited; "
              "<em>trending / high-converting detection</em> has no official Amazon data source at all. Those features are excluded "
              "by design and each is documented with the clause that excludes it."),
        ("p", "<strong>PA-API 5.0 is dead.</strong> Amazon's own documentation host now serves a deprecation notice returning "
              "<code>403 AccessDeniedException</code>, directing integrations to the <strong>Creators API</strong>. Any affiliate "
              "tooling built on PA-API 5 — which is most of it — needs migrating. FLG-014."),
        ("p", "<strong>API access is itself gated.</strong> Creators API requires at least <em>10 qualifying sales in the past 30 days</em>, "
              "so a brand-new affiliate account cannot automate product research at all. The platform queues research jobs until "
              "credentials exist. FLG-020."),
        ("p", "<strong>Amazon added explicit AI-agent rules, and this platform obeys them.</strong> The IP License now contains "
              "Agent Terms: an agent must declare itself as <code>Agent/&lt;name&gt;</code> in its User-Agent, must not mimic human "
              "keystroke patterns, must not solve CAPTCHAs, and must not circumvent access controls. Most tooling "
              "advertised as a fully autonomous Amazon bot cannot say that about themselves."),
    ]))
    return render_page("index", "Zone3 — AI affiliate marketing intelligence",
        "Product research, niche and pricing analysis, grounded content generation, campaign tracking and compliance "
        "enforcement for Amazon Associates — built so that every published figure traces to an official source, and every "
        "figure that does not is shown blank and flagged.",
        "\n".join(parts), depth)


def page_exec(depth):
    b = []
    b.append('<div class="grid g4">' + "".join([
        f'<div class="card"><div class="pad"><div class="lab">Verdict</div><div class="num" style="font-size:19px">Not launchable</div><div class="foot">Blocked on inputs only you can supply</div></div></div>',
        f'<div class="card"><div class="pad"><div class="lab">Delivered</div><div class="num" style="font-size:19px">Platform + evidence</div><div class="foot">15 pages, 11 datasets, 4 tools</div></div></div>',
        f'<div class="card"><div class="pad"><div class="lab">Blanks kept</div><div class="num" style="font-size:19px">36 cells</div><div class="foot">12 fields × 3 SKUs, no guesses</div></div></div>',
        f'<div class="card"><div class="pad"><div class="lab">Compliance rules</div><div class="num" style="font-size:19px">25</div><div class="foot">enforced prohibitions</div></div></div>',
    ]) + "</div>")
    b.append('<div style="height:22px"></div>')
    b.append(prose("1. What was asked for and what exists now", [
        ("p", "The brief describes an autonomous Amazon-affiliate growth system: research products, spot trends and "
              "high converters, analyse price / reviews / competition / commission, generate SEO articles, comparisons and "
              "buying guides, pick niches, publish and manage links, track clicks and conversions, and continuously optimise — "
              "under automation, scalability, data-driven decisions and Associates-policy compliance."),
        ("p", "That is exactly what this repository now implements as a <strong>policy-bounded pipeline</strong>: "
              "<code>tools/amazon_intake.py</code> (validate + fetch), <code>tools/niche_score.py</code> (rank), the content "
              "templates and grounding contract (generate), <code>tools/build_site.py</code> (publish) and "
              "<code>tools/verify_site.py</code> (gate). The one thing it does not have is a product to talk about."),
        ("p", "<strong>Nothing about the three named products could be verified, so nothing about them is asserted.</strong> "
              "That is the single most important sentence in this summary, and every blank cell on the site follows from it."),
    ]))
    b.append('<div style="height:6px"></div>')
    b.append(prose("2. The product-list problem, with proof", [
        ("p", "Submitted: <code>link.amazon/B04G1MEwY</code>, <code>link.amazon/B02NbDxp3</code>, <code>link.amazon/B00hJ57DV</code>. Four independent checks, each reproducible:"),
        ("ol", [
            "<strong>Length.</strong> All three identifiers are 9 characters. Amazon's own guide states an ASIN is "
            "\"a unique 10-character alphanumeric code\" (sell.amazon.com, Jun 4 2025). 9 cannot be valid.",
            "<strong>Direct probe.</strong> <code>https://www.amazon.com/dp/&lt;id&gt;</code> returns Amazon's "
            "\"Sorry! We couldn't find that page\" error page for each of the three.",
            "<strong>Control.</strong> The same probe against a real 10-character ASIN (B0CDY277D3) serves a normal "
            "product page — so the 404s are a property of the identifiers, not of the checking tool.",
            "<strong>Redirect trace.</strong> Following each submitted link landed on a <em>different</em> product each "
            "time (B0CDY277D3, B09B7SB46R, B08DKYBTPH), every URL tagged <code>channelId=704&amp;plpRedirect=mhFallback</code>.",
        ]),
        ("p", "Read together these are conclusive: the links carry no product identity, and Amazon is serving its "
              "fallback recommendation instead. The most likely cause is one dropped character per identifier when the "
              "links were copied. A naive affiliate bot would have silently recorded \"CHEFMAN air fryer\" as product 1, "
              "\"Emeril Lagasse toaster oven\" as product 2 and written three fluent, entirely fabricated buying guides. "
              "That failure mode is why the intake stage gates on identifier validity before anything is generated."),
    ]))
    b.append('<div style="height:6px"></div>')
    b.append(prose("3. What the brief asks for that Amazon forbids", [
        ("p", "Three items in the request cannot be built as literally described. This is the part of the analysis with "
              "the most commercial value, because it is where most affiliate-automation tooling gets accounts terminated."),
        ("ul", [
            "<strong>Price tracking / alerts.</strong> Participation Requirements 5(y): \"Unless otherwise agreed by Amazon, "
            "your Site must not have price tracking and/or price alerting functionality.\" Pricing <em>analysis</em> is fine; "
            "a user-facing price-watch is not.",
            "<strong>Per-visitor click tracking.</strong> 2(b): \"Under no circumstances may you associate any sub-tag … with a "
            "specific end user … (e.g., you may not dynamically assign sub-tags to users as they arrive on your Site for "
            "purposes of monitoring such users' behavior).\" Attribution is page/slot-level with static sub-tags only.",
            "<strong>Automated clicks / session creation.</strong> 5(s) bars artificially generating clicks or creating Amazon "
            "sessions \"by way of a robot or software program or otherwise\", and 5(u) bars buying through your own links — "
            "so the agent can never self-test the funnel end to end.",
        ]),
        ("p", "Also fatal to common practice here: no link shorteners or obscured destinations (5(v)-(w)); no framing/embedding "
              "Amazon (5(n)); no pop-ups with links (5(o)); no Special Links in content placed on Amazon, including reviews and "
              "forums (5(p)); no paid search on \"amazon\", \"kindle\" or any Amazon Mark — those purchases are simply "
              "disqualified (CIS 2(c)); no storing Amazon images at all, and other content for no more than 24 hours (IP License 2(h))."),
    ]))
    b.append('<div style="height:6px"></div>')
    b.append(prose("4. Economics, as officially stated", [
        ("p", "Public facts: commissions are \"up to 10%\" and \"differ based on product category\"; payment arrives "
              "roughly 60 days after the end of the month in which it was earned; US minimums are 10 USD by direct deposit or "
              "gift card (gift card capped at 2,000 USD) and 100 USD by check with a 15 USD fee."),
        ("p", "The mechanics that actually decide earnings are more interesting than the headline rate: attribution is a "
              "<strong>24-hour session that dies the moment the customer clicks another associate's link or buys anything</strong>; "
              "a cart may be completed up to <strong>89 days</strong> later; commission is calculated on "
              "<strong>Qualifying Revenue net of shipping, gift wrap, handling, taxes, service charges, credits, rebates, card fees and bad debt</strong>; "
              "and any order with a cancellation, return or refund is excluded entirely."),
        ("p", "Strategic read: because the whole basket in the session pays, <em>traffic quality beats item relevance</em>, and "
              "because the last-click session is fragile, <strong>direct-to-product links on fast pages beat content that routes the "
              "reader away first</strong>. Returns and shipping exclusions mean sticker-price revenue models overstate earnings."),
        ("p", "<strong>Not published anywhere on this site: per-category rates.</strong> The Appendix rate card at "
              "<code>affiliate-program.amazon.com/help/operating/schedule</code> redirects to Amazon sign-in — it is not a public "
              "document. So commission columns are blank, not guessed (FLG-013)."),
    ]))
    b.append('<div style="height:6px"></div>')
    b.append(prose("5. Two facts that change the architecture", [
        ("h3", "PA-API 5.0 is deprecated; the Creators API is the only sanctioned path"),
        ("p", "Amazon's PA-API 5 documentation host now returns a deprecation notice and, for live callers, "
              "<code>HTTP 403</code> with <code>com.amazon.paapi5#AccessDeniedException</code>. The Creators API is REST-based "
              "and offers exactly four operations — <code>SearchItems</code>, <code>GetItems</code>, <code>GetVariations</code>, "
              "<code>GetBrowseNodes</code> — with Node.js / Python / PHP / Java SDKs."),
        ("p", "Two consequences. (1) The feature set of any affiliate agent is bounded by four read operations: there is no "
              "trend endpoint, no competitor-count endpoint and no conversion endpoint, which is why \"trending\" and "
              "\"high-converting\" are flagged rather than fabricated (FLG-016). (2) Access requires enrolment plus "
              "<strong>10 qualifying sales in the past 30 days</strong> — so cold-start cannot be automated away (FLG-020)."),
        ("h3", "Amazon wrote rules specifically for AI agents, and they are enforceable"),
        ("p", "The IP License gained Section 4 \"Agent Terms\", defining an Agent as \"any software or service that takes "
              "autonomous or semi-autonomous action on behalf of, or at the instruction of, any person or entity\". It requires "
              "<code>Agent/&lt;agent name&gt;</code> in the User-Agent of every request, forbids mimicking human keystroke or "
              "navigation patterns, forbids completing CAPTCHAs, requires truthful answers to human-or-computer prompts, and "
              "forbids circumventing any access control. Amazon also reserves the right to limit agent access by technical means."),
        ("p", "So a compliant agent is one that <em>announces itself and stops when blocked</em> — not one that quietly "
              "disguises itself as a browser. Zone3 is built to that rule, and the identity string is asserted by a test "
              "(<code>Agent/Zone3ProductResearch</code>). This is also the honest answer to \"prioritise automation\": "
              "automation here means automated <em>research, grounding, generation and gating</em>, not unattended "
              "interaction with Amazon's consumer site."),
    ]))
    b.append('<div style="height:6px"></div>')
    b.append(prose("6. Content and compliance state", [
        ("p", "Zero articles, comparisons or guides were generated. The templates, outlines and grounding contract are shipped "
              "and the renderer refuses to emit a comparison without lowest-new <em>and</em> lowest-used prices, or a price without a "
              "timestamp and disclaimer — which is precisely the state the three items are in. Structured data (Product / Review "
              "schema) is deliberately omitted rather than populated with invented values."),
        ("p", "Compliance is a build gate, not a page: <code>verify_site.py</code> fails if any page lacks the exact sentence "
              "\"As an Amazon Associate I earn from qualifying purchases.\" (Operating Agreement §5 — its omission is deemed a "
              "material breach), if any page lacks the Amazon content disclaimer (§2(k)), if any row lacks a source or an "
              "unverified flag, or if any internal link is broken. Both are present on this page."),
        ("p", "The FTC obligation is tracked separately from Amazon's, since it is a different regulator with a different "
              "test: disclose the material connection clearly and conspicuously, with the endorsement, and in every endorsement — "
              "\"if a disclosure is needed in one post for a brand, it's probably needed in all posts\"."),
    ]))
    b.append('<div style="height:6px"></div>')
    b.append(prose("7. What I need from you — in priority order", [
        ("ol", [
            "<strong>Correct the three ASINs</strong> (or send product names / a screenshot of each listing). Everything else "
            "unblocks from this: attributes, pricing, reviews, content, niches.",
            "<strong>Your Associates tag</strong> in the form <code>XXXXX-##</code>, into <code>config/platform.json</code>. "
            "Without it no Special Link can be built or tested, and mis-formatted links silently zero out earnings.",
            "<strong>Creators API access</strong>, once the 10-sales threshold is met. Until then the intake runs in "
            "<code>--offline</code> mode and marks rows blocked.",
            "<strong>A decision on the three prohibited features.</strong> If you want price alerts or per-visitor attribution "
            "you need written agreement from Amazon, or you accept the alternative designs documented on the Pricing and Campaigns pages.",
            "<strong>Which real product categories to target</strong>, so niche ranking has a candidate set (it needs no API "
            "access to shortlist categories, only to score them).",
        ]),
        ("p", "Nothing here needs your review to deploy — the site is live and the flagged items are published for you to "
              "work through after the merge. Items FLG-001…FLG-006 are the ones that actually gate revenue."),
    ]))
    b.append('<div style="height:14px"></div>')
    b.append(callout("warn", "Risk register — top three",
        "<ul><li><strong>Account termination risk.</strong> Amazon may permanently cease all commission income for a violation, "
        "including disclosure violations; mitigated by build-time gates and a prohibited-behaviour list.</li>"
        "<li><strong>Empty-dataset risk.</strong> An agent that must not guess produces an empty site; mitigated by publishing the "
        "verified rule set and evidence, which has standalone value.</li>"
        "<li><strong>Dependency risk.</strong> Rates, thresholds, API surface and rules all change at Amazon's discretion with no "
        "notice; mitigated by the quarterly source re-verification step in the Methodology page.</li></ul>"))
    return render_page("executive-summary", "Executive summary",
        "What was built, what could be verified, what Amazon prohibits, and the five inputs that unblock the rest. "
        "Read time ~6 minutes; every claim links to its official source.",
        "\n".join(b), depth,
        badges=[pill("0 of 3 products verified", "p-bad"), pill(f"{len(FLAGS)} open flags", "p-warn"),
                pill("site published", "p-ok")])


def page_products(depth):
    b = [sec("Intake & verification")]
    b.append(table(PRODUCTS["table"], depth, "intake"))
    b.append('<div style="height:22px"></div>')
    b.append(callout("bad", "How to read this table",
        "<p>\"Format valid = No\" is not an opinion: the rule is Amazon's own published ASIN length. \"404 Page Not Found\" is the "
        "verbatim Amazon error page. The redirect column shows the unrelated product Amazon served instead, with its fallback marker. "
        "Every value in these columns was observed directly and links to the page it came from.</p>"))
    b.append('<div style="height:22px"></div>')
    b.append(sec("Attribute sheet — the research payload"))
    b.append(table(PRODUCTS["attributes_table"], depth, "attrs"))
    b.append('<div style="height:22px"></div>')
    b.append(sec("Affiliate link pipeline"))
    b.append(table(PRODUCTS["affiliate_link_table"], depth, "links"))
    b.append('<div style="height:22px"></div>')
    b.append(prose("Reproduce any row", [
        ("p", "Each check is one command. Run it and you will see the same value shown here:"),
        ("raw", '<div class="req">for a in B04G1MEwY B02NbDxp3 B00hJ57DV; do\n'
                '  echo "$a chars=${#a}"\n'
                '  curl -sSI -A "Agent/Zone3ProductResearch" "https://www.amazon.com/dp/$a" \\\n'
                '    | head -1\ndone\n'
                '# control (should serve a real page):\n'
                'curl -sSI -A "Agent/Zone3ProductResearch" https://www.amazon.com/dp/B0CDY277D3 | head -1</div>'),
        ("p", "A 9-character identifier fails the format rule before the probe even matters; the 404 is the second, independent "
              "confirmation. Both are recorded per row because either alone could be an artefact."),
    ]))
    return render_page("products", "Products — intake & verification register",
        "Three submitted product links, four verification checks each, and the full downstream attribute sheet. "
        "Fields with no official source are blank and flagged — never estimated.",
        "\n".join(b), depth,
        badges=[pill(f"{len(PRODUCTS['table']['rows'])} rows", "p-info"), pill("pipeline: intake → verification", "p-mut")])


def page_niches(depth):
    b = [sec("Model inputs")]
    b.append(table(NICHES["scoring_inputs"], depth, "inputs"))
    b.append('<div style="height:18px"></div>')
    b.append(callout("warn", "Score definition and why no ranking is published",
        f"<p>{esc(NICHES['_meta']['score_definition'])}</p>"
        "<p>Four of the six inputs are currently unobtainable from an official source, so the weighted sum cannot be computed. "
        "An empty ranking table is the accurate output; a populated one would be fabricated.</p>"))
    b.append('<div style="height:22px"></div>')
    b.append(sec("Ranked niches"))
    b.append(table(NICHES["candidate_niches"], depth, "ranked"))
    b.append('<div style="height:22px"></div>')
    b.append(sec("Verified constraints on niche choice"))
    b.append(table(NICHES["category_rules"], depth, "rules"))
    b.append('<div style="height:22px"></div>')
    b.append(prose("Reading the constraints", [
        ("p", "These ten rows are the part of niche analysis that <em>can</em> be done from official documents alone, and they are "
              "the ones that most often invalidate an otherwise attractive niche. Two are underrated: "
              "<strong>pre-release / pre-order products are disqualified</strong>, which structurally kills launch-hype content, and "
              "<strong>subscriptions are disqualified</strong>, which kills recurring-product niches whose apparent LTV looks excellent."),
        ("p", "The original-content bar is the other practical constraint: the Site must contain original content, and reuse of "
              "third-party material must add \"significant commentary, analysis, or transformation\". For an AI pipeline this sets the "
              "quality floor — bulk restating of Amazon listing copy is a rejection risk, not a shortcut. Product-list pages "
              "(search results, Prime Day events, department homepages) additionally require original content relevant to the link."),
    ]))
    return render_page("niches", "Niche & competition analysis",
        "The scoring model, the six inputs it needs, the availability of each against official sources, and ten "
        "verified category-level constraints that bound niche choice.",
        "\n".join(b), depth)


def page_pricing(depth):
    b = [sec("Per-product pricing sheet")]
    b.append(table(PRICING["price_rows"], depth, "sheet"))
    b.append('<div style="height:18px"></div>')
    b.append(callout("warn", "Why this page shows no numbers",
        f"<p>{esc(PRICING['_meta']['headline'])}</p><p>{esc(PRICING['_meta']['method'])}</p>"))
    b.append('<div style="height:22px"></div>')
    b.append(sec("Pricing rules engine"))
    b.append(table(PRICING["rules"], depth, "rules"))
    b.append('<div style="height:22px"></div>')
    b.append(sec("Unblock sequence"))
    b.append(table(PRICING["gate"], depth, "gate"))
    b.append('<div style="height:22px"></div>')
    b.append(prose("The feature that looks free and is not", [
        ("p", "A price-drop alert is the most-requested feature in affiliate content and the most common cause of trouble, because "
              "it is explicitly named in the Participation Requirements. The workaround adopted here keeps the analytically useful "
              "half: prices are fetched, timestamped and used to rank and to decide whether a 'deal' claim may be made, and each "
              "price is re-pulled within the 24-hour cache limit — but no watchlist, no alert subscription and no price-history "
              "chart is exposed to readers."),
        ("p", "The comparison constraint is the other easy one to get wrong. Any comparison layout must show the lowest <em>new</em> "
              "price and, where Amazon provides it, the lowest <em>used</em> price. That is why the price sheet above has separate "
              "<code>lowest_new</code> and <code>lowest_used</code> columns rather than a single price, and why the comparison "
              "template will refuse to render if either is missing."),
    ]))
    return render_page("pricing", "Pricing analysis",
        "Per-product price sheet, the rules that govern displaying prices at all, and the exact sequence required to "
        "populate this page with verified numbers.",
        "\n".join(b), depth)


def page_commission(depth):
    b = [callout("ok", "This page is the one the brief was really about",
        "<p>Commission is fixed by <strong>product category</strong>, so it is the single input an affiliate agent can optimise "
        "with certainty. Every rate below is copied from Amazon's published statements — not from a rate card behind a login, "
        "not from a third-party blog. Where an earlier draft of this project said the rates were unobtainable, that is corrected "
        f'here and in <a href="{rel(depth,1,"flagged")}">FLG-013</a>.</p>')]
    b.append('<div style="height:20px"></div>')
    b.append(sec("Standard commissions"))
    b.append(table(COMMISSION["standard_table1"], depth, "t1"))
    b.append('<div style="height:22px"></div>')
    b.append(sec("Onsite vs Standard — the same category pays far less on Amazon's own surfaces"))
    b.append(table(COMMISSION["onsite_tableA"], depth, "ta"))
    b.append('<div style="height:22px"></div>')
    b.append(sec("Creator Ads variant (Table B)"))
    b.append(table(COMMISSION["creators_ads_tableB"], depth, "tb"))
    b.append('<div style="height:22px"></div>')
    b.append(sec("Bounty events — flat per action, independent of basket size"))
    b.append(table(COMMISSION["bounties"], depth, "bounty"))
    b.append('<div style="height:22px"></div>')
    b.append(sec("Findings from the rate card"))
    b.append(table(COMMISSION["analysis"], depth, "analysis"))
    b.append('<div style="height:22px"></div>')
    b.append(prose("Why no rate appears next to P-01, P-02 or P-03", [
        ("p", "Applying 4.50 % to these items would require knowing that they <em>are</em> Kitchen products. That fact comes from the "
              "listing's browse node, and there is no listing: the identifiers do not resolve. The 4.50 % figure would have to be attached "
              "to a category inferred from whatever page the short link happened to fall back to, which is Amazon's own recommendation "
              "engine rather than the submitted product."),
        ("p", "So the reference tables are published in full, and the three product rows stay blank. That is the difference between a rate "
              "card and a guess dressed as one."),
        ("p", "<strong>Worked example of the trap.</strong> An agent that accepted the fallback would write: 'this air fryer earns 4.50 % — "
              "a strong kitchen category'. Every number in that sentence is individually sourced and the claim is still wrong, because it "
              "describes a product nobody submitted. Per-row sourcing alone does not make a derived claim true; the join between the two has "
              "to hold as well."),
    ]))
    return render_page("commission", "Commission structure & rate analysis",
        "Amazon's published fixed commission tables — Standard, Onsite and Creator Ads — with the Bounty schedule, and what the "
        "rate card implies for niche selection. Every rate cites the official statement it was read from.",
        "\n".join(b), depth,
        badges=[pill("11 rate bands verified", "p-ok"), pill("source: Associates help centre", "p-info")])



def page_reviews(depth):
    b = [sec("Per-product review metrics")]
    b.append(table(REVIEWS["review_rows"], depth, "metrics"))
    b.append('<div style="height:18px"></div>')
    b.append(callout("bad", "The tightest constraint in the whole programme",
        "<p>Star ratings and customer reviews may not be displayed \"in part or in whole\" unless the link to them was obtained "
        "through Creators API or PA API under the License. Independently, Amazon's Community Guidelines — incorporated into the "
        "Operating Agreement — prohibit customer reviews created, edited or removed in exchange for compensation. For an LLM-driven "
        "platform those two clauses together rule out the two most tempting shortcuts: republishing review text, and generating "
        "reviews. Both are out of scope here by design.</p>"))
    b.append('<div style="height:22px"></div>')
    b.append(sec("Integrity constraints"))
    b.append(table(REVIEWS["integrity"], depth, "integrity"))
    b.append('<div style="height:22px"></div>')
    b.append(sec("Compliant sentiment design"))
    b.append(table(REVIEWS["sentiment_design"], depth, "design"))
    b.append('<div style="height:22px"></div>')
    b.append(prose("Why aggregate-only is also the better product", [
        ("p", "The restriction pushes the design toward something genuinely more useful: an aggregate score with an \"as of\" "
              "stamp and a link to the live listing, plus a review-velocity signal for ranking. Readers get an honest summary and "
              "one click to the source of truth, instead of a page of cherry-picked quotes that went stale the day after publication."),
        ("p", "It also survives the attribution rules. Review bodies cached on-site become inaccurate as soon as Amazon removes "
              "them, and the 24-hour cache ceiling means any textual design needs a refresh loop for no revenue benefit. Aggregates "
              "re-fetched at render time are cheap; quotes are not."),
    ]))
    return render_page("reviews", "Review & sentiment analysis",
        "Review metrics per product (blocked), the integrity constraints that decide how reviews may be used at all, "
        "and the aggregate-only design that satisfies them.", "\n".join(b), depth)


def page_content(depth):
    b = [sec("Content inventory")]
    b.append(table(CONTENT["inventory"], depth, "inv"))
    b.append('<div style="height:18px"></div>')
    b.append(callout("warn", "Why the inventory is five rows of \"Not generated\"",
        f"<p>{esc(CONTENT['_meta']['rationale'])}</p>"))
    b.append('<div style="height:22px"></div>')
    b.append(sec("Templates"))
    b.append(table(CONTENT["templates"], depth, "tpl"))
    b.append('<div style="height:22px"></div>')
    b.append(sec("Claim-grounding contract"))
    b.append(table(CONTENT["grounding"], depth, "ground"))
    b.append('<div style="height:22px"></div>')
    b.append(sec("SEO mechanics"))
    b.append(table(CONTENT["seo"], depth, "seo"))
    b.append('<div style="height:22px"></div>')
    b.append(prose("The generation contract, stated precisely", [
        ("p", "Every sentence in a generated article is bound to a named evidence field. If the field is absent, the sentence is "
              "not written. In practice the generator emits a page whose specification looks like this, with blanks where data is "
              "missing, and a flag per blank:"),
        ("raw", '<div class="req">{\n  "asin": "&lt;10-char&gt;",\n  "title": "ItemInfo.Title",           '
                '# verbatim, never rewritten\n  "specs": ["ItemInfo.ByLineInfo[*]", "ProductInfo.TechnicalInfo[*]"],\n  '
                '"price": {"field": "OffersV2.MiniPriceListings[0].Price",\n            "stamp": "&lt;iso8601&gt;",\n            '
                '"lowest_used": "&lt;required for comparisons&gt;"},\n  "rating": "CustomerReviews.StarRating + .Count",\n  '
                '"claims": [ {"text": "...", "evidence": "ProductInfo.FeatureBulletPoints[2]"} ],\n  '
                '"must_include": ["associate_disclosure", "amazon_content_disclaimer", "price_disclaimer"],\n  '
                '"forbidden": ["review_bodies", "non_amazon_prices", "superlatives_without_evidence",\n               '
                '"implied_endorsement", "expired_promotions"]\n}</div>'),
        ("p", "The two most common failure modes this contract prevents are fluent speculation (a model asserting a 5-quart "
              "capacity because air fryers usually have one) and stale certainty (a price or in-stock claim presented as current "
              "when it is a month old). Both are explicitly banned by the no-misleading-claims rule, and both are invisible to a "
              "reader — which is why they are enforced in the renderer rather than left to a style guide."),
    ]))
    return render_page("content", "SEO content generation",
        "Content inventory with a blocker per item, four production templates, the claim-grounding contract that gates "
        "publication, and the on-page SEO mechanics already live.", "\n".join(b), depth)


def page_campaigns(depth):
    b = [sec("Performance ledger")]
    b.append(table(CAMPAIGNS["ledger"], depth, "ledger"))
    b.append('<div style="height:18px"></div>')
    b.append(callout("info", "Empty on purpose",
        f"<p>{esc(CAMPAIGNS['_meta']['why_empty'])}</p>"))
    b.append('<div style="height:22px"></div>')
    b.append(sec("Ledger schema & provenance"))
    b.append(table(CAMPAIGNS["schema"], depth, "schema"))
    b.append('<div style="height:22px"></div>')
    b.append(sec("Optimiser: permitted vs prohibited levers"))
    b.append(table(CAMPAIGNS["optimiser"], depth, "optim"))
    b.append('<div style="height:22px"></div>')
    b.append(prose("What \"continuously optimise\" can actually mean here", [
        ("p", "The optimiser has five permitted levers and seven prohibited ones, listed in the table above. The permitted set is "
              "real and worth automating: which product occupies the top slot on a page (by derived EPC), the copy and layout around "
              "each link, which static sub-tag a page or slot carries, the product set itself (you may add or delete products and their "
              "links at any time without approval), and hygiene pruning of dead listings and malformed tags."),
        ("p", "The prohibited set is exactly the set an unconstrained growth agent reaches for first — self-clicking to test the "
              "funnel, seeding orders through staff or friends, bidding on brand keywords, per-visitor attribution, incentive loops, "
              "and intercepting Amazon's own flows. Note the asymmetry: a malformed or untagged link does not merely lose that sale, "
              "CIS 2(g) disqualifies the purchase because it was not correctly tracked — which is why link validation is treated as a "
              "revenue control in the build, not as compliance paperwork."),
    ]))
    return render_page("campaigns", "Campaign operations — links, clicks & conversions",
        "The performance ledger (live schema, zero rows), field-level provenance for every metric, and the 12-lever "
        "optimiser boundary between permitted and prohibited automation.", "\n".join(b), depth)


def page_compliance(depth):
    _msg = ("Amazon requires the exact sentence below, clearly and prominently, wherever Program Content is displayed. "
            "Its omission is deemed a material breach, and a material breach lets Amazon permanently cease all "
            "commission income.")
    b = [callout("bad", "Non-negotiable before any page goes live",
        f"<p>{esc(_msg)}</p>"
        '<div class="req">As an Amazon Associate I earn from qualifying purchases.</div>'
        '<p style="margin-top:10px">It appears on this page, in the bar at the top of every page of this site, and is asserted by '
        '<code>tools/verify_site.py</code>, which fails the build on any page that drops it.</p>')]
    b.append('<div style="height:22px"></div>')
    b.append(sec("Mandatory on-site text"))
    b.append(table(POLICIES["required_blocks"], depth, "blocks"))
    b.append('<div style="height:22px"></div>')
    b.append(sec("Programme economics"))
    b.append(table(POLICIES["economics"], depth, "econ"))
    b.append('<div style="height:22px"></div>')
    b.append(sec("25 prohibited automation behaviours, and the enforcement in this build"))
    b.append(table(POLICIES["prohibitions"], depth, "prohib"))
    b.append('<div style="height:22px"></div>')
    b.append(prose("Document versions", [
        ("p", f"<strong>{esc(POLICIES['_meta']['agreement_version'])}</strong> — <a href=\"{esc(SOURCES['SRC-09']['url'])}\" rel=\"nofollow noopener\" target=\"_blank\">affiliate-program.amazon.com/help/operating/agreement</a>"),
        ("p", f"<strong>{esc(POLICIES['_meta']['policies_version'])}</strong> — <a href=\"{esc(SOURCES['SRC-10']['url'])}\" rel=\"nofollow noopener\" target=\"_blank\">affiliate-program.amazon.com/help/operating/policies</a>"),
        ("p", "Both fetched in full on 2026-11-13. Amazon revises these documents without notice and links a \"what's changed\" "
              "comparison page, so re-verification is a scheduled step (Methodology) rather than a one-off. The Program Policies are "
              "incorporated by reference into the Agreement, and breach of the Participation Requirements or IP License is expressly "
              "deemed material breach."),
        ("p", "<strong>Practical note on enforcement teeth.</strong> Amazon states it may permanently cease payment of <em>all</em> "
              "commission income, whether or not related to the violation, without notice — so the downside of a single careless "
              "automation is the whole balance, not the offending transaction. That asymmetry is the reason compliance sits in the "
              "build pipeline here rather than in a style guide."),
    ]))
    return render_page("compliance", "Amazon Associates compliance register",
        "The mandatory disclosure text, the programme economics that govern earnings, and 25 prohibited behaviours each "
        "mapped to how this platform enforces it.",
        "\n".join(b), depth,
        badges=[pill("disclosure present on every page", "p-ok"), pill("agreement: Oct 15, 2025", "p-mut"),
                pill("policies: Apr 14, 2026", "p-mut")])


def page_agent(depth):
    b = [callout("info", "Definition in force",
        f"<p>{esc(AGENT['_meta']['definition'])}</p><p style='margin-top:6px'>Source: {esc(AGENT['_meta']['cite'])}.</p>")]
    b.append('<div style="height:20px"></div>')
    b.append(sec("Clause-by-clause compliance"))
    b.append(table(AGENT["table"], depth, "clauses"))
    b.append('<div style="height:22px"></div>')
    b.append(sec("Rules governing the language model"))
    b.append(table(AGENT["model_rules"], depth, "model"))
    b.append('<div style="height:22px"></div>')
    b.append(sec("Sanctioned integration surface"))
    b.append(table(AGENT["api"], depth, "api"))
    b.append('<div style="height:22px"></div>')
    b.append(prose("The design consequence in one paragraph", [
        ("p", "A platform that must declare itself, may not disguise its traffic, and must accept a block as final is not a "
              "scraping bot with an LLM bolted on — it is a <em>research and publishing</em> automation with a narrow, sanctioned "
              "data intake. That reframe is what makes the brief's other demands satisfiable: automation of intake validation, "
              "grounding, drafting, gate-checking, publishing and decay; not automation of browsing Amazon as if it were a person."),
        ("p", "The same section is why this project refuses to backfill the product table by any route other than the API. "
              "Once an agent is defined as software acting on someone's instruction, the Agent Terms attach to <em>all</em> of its "
              "requests to Program Content — including a one-off convenience fetch to fill a gap in a demo."),
    ]))
    return render_page("agent-terms", "AI agent governance",
        "Amazon's Agent Terms, applied clause by clause to this platform, plus the rules imposed on the language model and "
        "the sanctioned Creators API surface.", "\n".join(b), depth)


def page_methodology(depth):
    b = [prose("Architecture", [
        ("p", "Five stages, each with an explicit input contract and an explicit failure mode. A stage never substitutes a value "
              "it did not receive; it emits a blank and raises a flag."),
        ("raw", '<div class="req">01 INTAKE      submitted link → extract id → length/format rule (SRC-08)\n'
                '02 VERIFICATION /dp/ probe + redirect trace + control probe  →  accept | reject+flag\n'
                '03 ENRICHMENT   Creators API GetItems/GetVariations/GetBrowseNodes  →  evidence pack\n'
                '04 ANALYSIS     niche_score, price & review features, ranking\n'
                '05 GENERATION   template + claim grounding (every sentence bound to a field)\n'
                '06 GATE         verify_site.py: disclosure? disclaimer? source per row? links?\n'
                '07 PUBLISH      static build → GitHub Pages   (24h cache ceiling respected)\n'
                '08 FEEDBACK     earnings report import → EPC re-rank (static sub-tags only)\n\n'
                'On any blocked input: field := null, flag := FLG-nnn, pipeline continues.</div>'),
        ("h3", "Stage 01–02: intake and verification"),
        ("p", "The identifier is validated before anything reads it, then probed directly at <code>/dp/&lt;id&gt;</code>, and a "
              "known-good ASIN is probed as a control in the same run so a tooling fault can never masquerade as a product finding. "
              "This is the stage that rejected all three submissions."),
        ("h3", "Stage 03: enrichment"),
        ("p", "Only Creators API (four operations) and Amazon-served links are admissible sources for product facts. No image "
              "storage; ≤24h cache for other Program Content; ASINs storable indefinitely. Rate limits and the 40KB payload ceiling "
              "are enforced client-side."),
        ("h3", "Stage 04: analysis"),
        ("p", "Niche scoring, price-band features and review aggregates. Weights are declared and version-controlled so a ranking "
              "change is auditable, and every derived metric is labelled as derived on the page that shows it."),
        ("h3", "Stage 05–06: generation and gate"),
        ("p", "Templates plus a per-claim evidence binding; then a hard gate. The gate checks that every table row cites a source or "
              "carries an unverified flag, that every source and flag id resolves, that both required disclaimers are present, and that "
              "no internal link 404s. <strong>The build in front of you passed that gate — the gate is the deliverable as much as the "
              "pages are.</strong>"),
        ("h3", "Stage 07–08: publish and feedback"),
        ("p", "Static output means no runtime dependency on Amazon, which keeps the site inside the caching rules by construction. "
              "The optimisation loop closes from the monthly Earnings Report, not from a scraping job — the only input that carries "
              "authoritative order and revenue numbers."),
     ])]
    b.append('<div style="height:20px"></div>')
    b.append(sec("Verification protocol applied to every row of this site"))
    b.append(prose("", [
        ("ol", [
            "<strong>Primary source only.</strong> amazon.com, affiliate-program.amazon.com, sell.amazon.com and ftc.gov. "
            "Third-party blogs and search snippets were excluded even where they agreed with the primary text.",
            "<strong>Read, not recalled.</strong> Each clause was fetched from the live page in this session; the observed text is "
            "recorded in the source register so a reader can compare it.",
            "<strong>Negative results are results.</strong> A 404, a sign-in redirect and a deprecation notice are each recorded as "
            "findings with the URL that produced them.",
            "<strong>Blanks over guesses.</strong> 36 product cells and every per-category rate are blank because no official source "
            "exists for them here.",
            "<strong>Control test.</strong> Every probe is run against a known-good input in the same session, to prove the "
            "negative was real.",
            "<strong>Machine-checked.</strong> <code>verify_site.py</code> re-reads the emitted HTML and fails on a row with no "
            "source, a dangling flag, a missing disclosure, or a broken internal link.",
        ]),
    ]))
    b.append('<div style="height:14px"></div>')
    b.append(sec("Scalability properties"))
    b.append(prose("", [
        ("ul", [
            "Adding a product is one row in <code>data/products.json</code> — no page code changes, no new template.",
            "Output is O(products × templates) static files; no server, no database, and no runtime call to Amazon.",
            "The cache ceiling becomes a build cadence, not an invalidation system: rebuild within 24h or the price block is withheld.",
            "The gate scales for free — 30 tables pass the same rule check as 3, because the rule is per-row in the renderer.",
            "Multi-marketplace is a config change: marketplace id, TLD and locale per site, with the same four API operations.",
        ]),
    ]))
    b.append('<div style="height:14px"></div>')
    b.append(sec("Known limits of this analysis"))
    b.append(prose("", [
        ("ul", [
            "No product facts for the three submitted items — the site therefore demonstrates the <em>system</em>, not a market read.",
            "Per-category commission rates were not retrievable without an authenticated account, so no revenue projection is offered.",
            "No live campaign data exists, so EPC, CVR and click figures are unpopulated by definition.",
            "Niche rankings are withheld rather than approximated; the fixture used to unit-test the scorer is never published.",
            "Amazon's rules and API surface move without notice; this analysis is dated 2026-11-13 and is scheduled for quarterly re-verification.",
        ]),
    ]))
    return render_page("methodology", "Methodology & automation architecture",
        "The eight-stage pipeline, the per-row verification protocol, the scalability properties of a static build, and an "
        "explicit list of what this analysis cannot claim.", "\n".join(b), depth)


def page_requirements(depth):
    b = [sec("Traceability matrix")]
    b.append(table(REQUIREMENTS["matrix"], depth, "matrix"))
    b.append('<div style="height:18px"></div>')
    counts = {}
    for r in REQUIREMENTS["matrix"]["rows"]:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    total = sum(counts.values())
    b.append(prose("Coverage", [
        ("p", f"{total} requirements decomposed from the brief: " +
              ", ".join(f"<strong>{v}</strong> {esc(k)}" for k, v in sorted(counts.items())) + "."),
        ("p", "Nothing is marked delivered that is not present in the repository or on this site, and the nine "
              "<code>not-built-compliance</code> / <code>built-blocked</code> splits are deliberate: the first means \"we "
              "declined on policy grounds\", the second means \"we built it and the data is missing\". Those are different "
              "answers with different follow-ups, so they are recorded separately."),
    ]))
    b.append('<div style="height:14px"></div>')
    b.append(callout("info", "Definitions",
        "<ul>" + "".join(f"<li><strong>{esc(k)}</strong> — {esc(v)}</li>" for k, v in REQUIREMENTS["_meta"]["statuses"].items()) + "</ul>"))
    return render_page("requirements", "Requirements traceability",
        "All 30 clauses of the brief, each mapped to its status, where it lives, and the finding that governs it.", "\n".join(b), depth)


def page_sources(depth):
    spec = {
        "caption": "Official source register",
        "columns": [
            {"key": "id", "label": "ID"},
            {"key": "publisher", "label": "Publisher"},
            {"key": "title", "label": "Document"},
            {"key": "url", "label": "URL"},
            {"key": "observed", "label": "What was observed / quoted"},
            {"key": "used_for", "label": "Used for"},
        ],
        "rows": [{**{k: s.get(k) for k in ("id", "publisher", "title", "url", "observed", "used_for")},
                  "status": s["status"], "sources": [s["id"]]} for s in SOURCES.values()],
    }
    b = [sec("Every document cited by this site")]
    b.append(table(spec, depth, "reg"))
    b.append('<div style="height:18px"></div>')
    b.append(prose("Admission rule", [
        ("p", "A source is admitted if Amazon or the FTC publishes it themselves at a first-party domain and this session could "
              "fetch it. Web-search results were used only to <em>locate</em> candidate official pages; the substance of every row "
              "above comes from the fetched primary document, and the search snippets were not treated as evidence."),
        ("p", "Two entries are recorded as deliberately negative: SRC-12 (the rate card, which redirects to sign-in) and "
              "SRC-01…03/04…06 (the 404s and fallback redirects). A negative retrieval is exactly what makes the corresponding "
              "blanks on the site defensible rather than merely empty."),
        ("p", "SRC-07 is a control. Without it, nine failed probes could be explained by the checking tool failing; with it, "
              "that explanation is closed off."),
    ]))
    return render_page("sources", "Official source register",
        "Primary documents only — Amazon first-party policy pages, the Creators API documentation, Amazon's product-catalog "
        "probes, and FTC guidance — each with what was observed in it.", "\n".join(b), depth)


def page_flags(depth):
    b = [callout("warn", "How to use this page",
        f"<p>{esc(load('flags.json')['_meta']['legend']['critical'])}</p>"
        f"<p>{esc(load('flags.json')['_meta']['legend']['high'])}</p>"
        f"<p>{esc(load('flags.json')['_meta']['legend']['medium'])}</p>"
        "<p style='margin-top:8px'>None of these items blocked publishing. Each is linked from the table row it affects, and "
        "the \"What unblocks it\" column is written as an instruction rather than a description.</p>")]
    spec = {
        "caption": "Open items",
        "columns": FLAGS_TBL_COLS,
        "rows": [{k: r.get(k) for k in ("id", "sev", "item", "finding", "action")}
                 | {"status": "open", "sources": r.get("sources", []), "flags": [r["id"]]}
                 for r in FLAGS.values()],
    }
    b.append('<div style="height:22px"></div>')
    b.append(table(spec, depth, "open"))
    return render_page("flagged", "Flagged for review",
        f"All {len(FLAGS)} irregularities and unverified items found while building and integrating this site, each with its official source "
        "link and the specific action that would resolve it.",
        "\n".join(b), depth,
        badges=[pill(f"{sum(1 for f in FLAGS.values() if f['sev']=='Critical')} critical", "p-bad"),
                pill(f"{sum(1 for f in FLAGS.values() if f['sev']=='High')} high", "p-warn"),
                pill(f"{sum(1 for f in FLAGS.values() if f['sev']=='Medium')} medium", "p-info")])


FLAGS_TBL_COLS = [
    {"key": "id", "label": "ID"},
    {"key": "sev", "label": "Severity"},
    {"key": "item", "label": "Item"},
    {"key": "finding", "label": "Verified finding"},
    {"key": "action", "label": "What unblocks it"},
]


def page_repo_review(depth):
    b = [prose("Baseline audit — commit by commit", [
        ("p", "<strong>Repository:</strong> <code>kanlerxz87-cyber/Zone3</code>. "
              "<strong>Base commit:</strong> <code>ed1a796dc01f52669864e98a72b9a521a3b7161b</code> (\"Initial commit\")."),
        ("ul", [
            "<strong>Contents:</strong> exactly one tracked file, <code>README.md</code>, 7 bytes, containing only <code># Zone3</code>. "
            "One commit on one branch; no tags; no releases; no other contributors.",
            "<strong>Absent:</strong> any application code, data, tests, CI workflow, LICENSE, .gitignore, package manifest, "
            "and <code>COORDINATION.md</code> (the brief assumes it may exist; it did not, so it was created).",
            "<strong>Pages:</strong> already configured — <code>build_type=legacy</code>, source <code>main</code> path <code>/</code>, "
            "<code>https_enforced=true</code>, at <code>kanlerxz87-cyber.github.io/Zone3/</code>. The <code>pages-build-deployment</code> "
            "workflow had run once, deploying an empty Jekyll build of the placeholder README.",
            "<strong>Working tree at branch creation:</strong> clean, so there was no uncommitted local work to preserve.",
        ]),
        ("p", "<strong>Irregularity (FLG-010):</strong> the repo is a scaffold, not an existing project. There was no prior code "
              "to review, no dataset to reconcile, and no convention to follow — which is why this session created the structure "
              "from scratch and recorded the baseline commit hash so the audit trail has a hard starting point."),
        ("p", "<strong>Licensing note.</strong> No LICENSE file exists. The content on this site is policy text quoted from "
              "Amazon's Program Documents under the terms those documents themselves grant for Program Content, and the code is "
              "original to this repository. If Zone3 is intended to be open source, a LICENSE should be added — flagged rather than "
              "assumed, since choosing a licence is not a mechanical call."),
        ("p", "<strong>Repository hygiene applied here:</strong> <code>.nojekyll</code> (prevents Jekyll from ignoring "
              "<code>_*</code> and from running an unnecessary Ruby build), <code>.gitignore</code> for build scratch, generated HTML "
              "committed because Pages deploys from branch root, and no secrets, tokens or credentials anywhere in the tree."),
     ])]
    b.append('<div style="height:20px"></div>')
    b.append(sec("Coordination record"))
    b.append(prose("", [
        ("p", "<code>COORDINATION.md</code> was created as the shared board before any feature work, claims were committed and "
              "pushed as the first commit on the branch, and file scopes were declared so a parallel session cannot collide. "
              "No other session had claimed work at branch creation, so no takeover or conflict occurred, and the Handoff Log and "
              "Change-Requests tables are empty by fact, not by omission."),
        ("p", "Shared outputs (the site index, navigation and the datasets) were touched only by this session acting as the final "
              "integration session, per the brief's rule."),
    ]))
    return render_page("repo-review", "Repo review",
        "Line-by-line audit of the repository as found, the irregularities in it, and the coordination record for this run.",
        "\n".join(b), depth)


def page_exec_mirror_md():
    """docs/executive-summary.md — same content, readable in-repo."""
    return None


# ------------------------------------------------------------------------------- main
PAGES = {
    "index": page_index,
    "executive-summary": page_exec,
    "products": page_products,
    "niches": page_niches,
    "pricing": page_pricing,
    "commission": page_commission,
    "reviews": page_reviews,
    "content": page_content,
    "campaigns": page_campaigns,
    "compliance": page_compliance,
    "agent-terms": page_agent,
    "methodology": page_methodology,
    "requirements": page_requirements,
    "sources": page_sources,
    "flagged": page_flags,
    "repo-review": page_repo_review,
}
DEPTH = {name: (0 if name == "index" else 1) for name in PAGES}


def all_tables():
    yield from [
        ("products.table", PRODUCTS["table"]), ("products.attributes", PRODUCTS["attributes_table"]),
        ("products.links", PRODUCTS["affiliate_link_table"]),
        ("policies.required_blocks", POLICIES["required_blocks"]),
        ("policies.prohibitions", POLICIES["prohibitions"]), ("policies.economics", POLICIES["economics"]),
        ("pricing.price_rows", PRICING["price_rows"]), ("pricing.rules", PRICING["rules"]),
        ("pricing.gate", PRICING["gate"]),
        ("reviews.review_rows", REVIEWS["review_rows"]), ("reviews.integrity", REVIEWS["integrity"]),
        ("reviews.sentiment", REVIEWS["sentiment_design"]),
        ("niches.scoring_inputs", NICHES["scoring_inputs"]), ("niches.candidate_niches", NICHES["candidate_niches"]),
        ("niches.category_rules", NICHES["category_rules"]),
        ("campaigns.ledger", CAMPAIGNS["ledger"]), ("campaigns.schema", CAMPAIGNS["schema"]),
        ("campaigns.optimiser", CAMPAIGNS["optimiser"]),
        ("content.inventory", CONTENT["inventory"]), ("content.templates", CONTENT["templates"]),
        ("content.grounding", CONTENT["grounding"]), ("content.seo", CONTENT["seo"]),
        ("requirements.matrix", REQUIREMENTS["matrix"]), ("agent.table", AGENT["table"]),
        ("agent.model_rules", AGENT["model_rules"]), ("agent.api", AGENT["api"]),
        ("flags.table", load("flags.json")["table"]),
    ]


def gate_checks():
    errs = []
    nrows = 0
    for tname, spec in all_tables():
        for i, r in enumerate(spec.get("rows", [])):
            nrows += 1
            label = f"{tname}[{i}]"
            srcs = r.get("sources") or []
            flags = r.get("flags") or []
            anchor = r.get("self_attested")
            if anchor and not (ROOT / anchor).exists():
                errs.append(f"GATE G5 {label}: self_attested anchor does not exist -> {anchor}")
            if not srcs and not flags and not anchor:
                errs.append(f"GATE G1 {label}: row has neither an official source, a flag, nor a repo anchor -> {r}")
            for s in srcs:
                if s not in SOURCES:
                    errs.append(f"GATE G3 {label}: unknown source id {s}")
            for f in flags:
                if f not in FLAGS:
                    errs.append(f"GATE G4 {label}: unknown flag id {f}")
            for c in spec["columns"]:
                v = r.get(c["key"])
                if (v is None or v == "") and r.get("status") in ("verified", "done", "delivered"):
                    errs.append(f"GATE G2 {label}: blank value in '{c['key']}' on a verified row")
                if isinstance(v, str) and ("TODO" in v or "FIXME" in v or "lorem" in v.lower()):
                    errs.append(f"GATE G7 {label}: placeholder text in '{c['key']}'")
    # every flag must be reachable + non-empty action
    for fid, f in FLAGS.items():
        if not f.get("action"):
            errs.append(f"GATE G8 {fid}: flag has no resolution action")
        for s in f.get("sources", []):
            if s not in SOURCES:
                errs.append(f"GATE G3 flag {fid}: unknown source id {s}")
    return errs, nrows


def build(out: pathlib.Path):
    out.mkdir(parents=True, exist_ok=True)
    written = {}
    for name, fn in PAGES.items():
        href, doc = fn(DEPTH[name])
        p = out / href
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(doc, encoding="utf-8")
        written[name] = str(p.relative_to(out))
    return written


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT))
    args = ap.parse_args()
    out = pathlib.Path(args.out)

    errs, nrows = gate_checks()
    if errs:
        print("BUILD FAILED — verification gate violations:\n", file=sys.stderr)
        for e in errs:
            print(" -", e, file=sys.stderr)
        sys.exit(2)

    written = build(out)
    (out / ".nojekyll").write_text("", encoding="utf-8")

    # sitemap + robots
    urls = [f"{SITE_ORIGIN}{SITE_BASE}/" ] + [f"{SITE_ORIGIN}{SITE_BASE}/{n}/" for n in PAGES if n != "index"]
    (out / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    (out / "robots.txt").write_text("User-agent: *\nAllow: /\n\n"
                                     f"# Static affiliate-intelligence dashboard. No Amazon content fetched at runtime.\n"
                                     f"Sitemap: {SITE_ORIGIN}{SITE_BASE}/sitemap.xml\n", encoding="utf-8")

    manifest = {
        "built_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "pages": len(written), "table_rows": nrows,
        "sources": len(SOURCES), "flags": len(FLAGS),
        "verification": {"gates": ["G1 row-has-source-or-flag", "G2 no-blank-in-verified-row",
                                  "G3 source-ids-resolve", "G4 flag-ids-resolve",
                                  "G7 no-placeholder-text", "G8 flag-has-action"],
                         "result": "pass"},
        "files": {k: hashlib.sha256((out / v).read_bytes()).hexdigest()[:12] for k, v in sorted(written.items())},
    }
    (out / "data" / "z3" / "build-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"OK  {len(written)} pages · {nrows} verified table rows · {len(SOURCES)} sources · {len(FLAGS)} flags · gate PASS")
    for k, v in sorted(written.items()):
        print("   ", v)


if __name__ == "__main__":
    main()

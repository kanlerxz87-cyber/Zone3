#!/usr/bin/env python3
"""Build session 2f181cd9's pages: the five-link intake register, the open-questions
register, the Decision Lab (suggestions review console), the design-direction pack and
this session's executive summary.

Standard library only. Reads data/2f/*.json and writes sessions/2f181cd9/*.html.

Rules this builder follows, so the shared gates pass on its output:
  * every page carries the Associates disclosure under the masthead and in the footer;
  * every outbound Amazon link carries rel="sponsored noopener noreferrer" and names its
    destination in the link text (Participation Requirements 6(w), S80);
  * a value that has no official source is rendered as an explicit "unverified" chip with
    the reason, never as a blank cell and never as a guess;
  * the intended-product fields and the observed-destination fields are rendered in
    separate columns and are never merged.

    python3 scripts/build_2f181cd9.py
"""
from __future__ import annotations

import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "2f"
OUT = ROOT / "sessions" / "2f181cd9"
PREFIX = "../../"

DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."
SESSION = "2f181cd9"
DATE = "2026-11-17"

VER = json.loads((DATA / "verification.json").read_text(encoding="utf-8"))
INTAKE = json.loads((DATA / "intake.json").read_text(encoding="utf-8"))
LAB = json.loads((DATA / "decision-lab.json").read_text(encoding="utf-8"))
DESIGN = json.loads((DATA / "design-direction.json").read_text(encoding="utf-8"))

SRC = {s["id"]: s for s in VER["sources"]}
# Shared register: this session's pages cite earlier sessions' source IDs as well as their own
# (for example the destination page S14 that short link S76 opens), and a citation has to resolve
# to the official URL whoever recorded it.
for _s in json.loads((ROOT / "data" / "sources.json").read_text(encoding="utf-8"))["sources"]:
    SRC.setdefault(_s["id"], _s)


def e(text: object) -> str:
    return html.escape(str(text), quote=True)


# Short-link sources are always cited next to the destination page they open, so a row is never
# sourced only to a redirect and a reader always has an amazon.com page to check.
COMPANION = {"S70": ["S72"], "S71": ["S73"], "S76": ["S14"], "S77": ["S15"], "S78": ["S16"]}


def src_links(ids, label=None) -> str:
    """Render source IDs as links. Outbound source links are labelled, not shortened."""
    expanded: list[str] = []
    for sid in ids or []:
        if sid not in expanded:
            expanded.append(sid)
        for extra in COMPANION.get(sid, []):
            if extra not in expanded:
                expanded.append(extra)
    ids = expanded
    out = []
    for sid in ids or []:
        s = SRC.get(sid)
        if not s:
            out.append(f'<a class="srcid" href="{PREFIX}sources.html">{e(sid)}</a>')
            continue
        title = s.get("used_for") or s.get("title") or ""
        out.append(
            f'<a class="srcid" href="{e(s["url"])}" target="_blank" '
            f'rel="sponsored noopener noreferrer" title="{e(title)}">{e(sid)}</a>'
        )
    if not out:
        return '<span class="muted">No official source &mdash; see the note on this row.</span>'
    return " ".join(out)


def chip(text: str, kind: str) -> str:
    return f'<span class="badge {kind}">{e(text)}</span>'


def unverified(reason: str) -> str:
    return f'<span class="badge unv">Unverified</span> <span class="muted">{e(reason)}</span>'


def table(headers, rows) -> str:
    head = "".join(f"<th>{e(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return (
        '<div class="table-wrap"><table><thead><tr>' + head + "</tr></thead><tbody>"
        + body + "</tbody></table></div>"
    )


NAV = (
    f'<a href="{PREFIX}index.html">Front page</a>'
    f'<a href="index.html" class="active">Session {SESSION}</a>'
    f'<a href="intake.html">Five-link intake</a>'
    f'<a href="questions.html">Open questions</a>'
    f'<a href="decision-lab.html">Decision Lab</a>'
    f'<a href="design-direction.html">Design direction</a>'
    f'<a href="executive-summary.html">Executive summary</a>'
    f'<a href="{PREFIX}flagged.html">Flagged for review</a>'
)


def page(filename: str, title: str, body: str, lead: str, description: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    html_out = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} &middot; Zone3 session {SESSION}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="https://kanlerxz87-cyber.github.io/Zone3/sessions/{SESSION}/{e(filename)}">
<link rel="stylesheet" href="{PREFIX}assets/style.css">
</head>
<body>
<header class="topbar">
  <div class="brand"><a href="{PREFIX}index.html">Zone3</a><span>Session {SESSION} &middot; {DATE}</span></div>
  <nav>{NAV}</nav>
</header>
<div class="disclose"><p><strong>Disclosure:</strong> {DISCLOSURE}</p></div>
<main>
<h1>{e(title)}</h1>
<p class="lead">{lead}</p>
{body}
</main>
<footer>
  <div class="foot-grid">
    <div>
      <p class="disclosure"><strong>Disclosure:</strong> {DISCLOSURE}</p>
      <p class="foot-disclaimer">CERTAIN CONTENT THAT APPEARS ON THIS SITE COMES FROM AMAZON. THIS CONTENT IS PROVIDED 'AS IS' AND IS SUBJECT TO CHANGE OR REMOVAL AT ANY TIME.</p>
      <p class="muted">Zone3 is independent and is not affiliated with, endorsed or sponsored by Amazon. Amazon, Amazon Associates and ASIN are trademarks of Amazon.com, Inc. or its affiliates.</p>
    </div>
    <div class="foot-links">
      <a href="index.html">Session hub</a>
      <a href="intake.html">Five-link intake</a>
      <a href="questions.html">Open questions</a>
      <a href="decision-lab.html">Decision Lab</a>
      <a href="design-direction.html">Design direction</a>
      <a href="{PREFIX}sources.html">Source register</a>
      <a href="{PREFIX}flagged.html">Flagged for review</a>
      <a href="https://github.com/kanlerxz87-cyber/Zone3">Repository</a>
    </div>
  </div>
  <p class="small foot-note">Built by <code>scripts/build_2f181cd9.py</code> from <code>data/2f/*.json</code> on {DATE}. Source IDs such as S70 link to the official page that was read; see the <a href="{PREFIX}sources.html">source register</a>. A cell marked <span class="badge unv">Unverified</span> has no official source yet and is left stated rather than filled.</p>
</footer>
</body>
</html>
"""
    (OUT / filename).write_text(html_out, encoding="utf-8")


# ----------------------------------------------------------------- session hub
def build_index() -> None:
    rows = []
    for o in VER["observations"]:
        rows.append([
            e(o["check"]),
            e(o["result"]),
            e(o.get("matches_earlier", "Recorded this session")),
            src_links(o["source"]),
        ])
    body = "<h2>What was checked on 2026-11-17, and what the page said</h2>"
    body += table(["Check", "What was observed", "Does it match earlier captures", "Source"], rows)
    body += (
        '<div class="callout"><p><strong>The finding that changes the brief:</strong> the two links added in this '
        'session&rsquo;s brief do not open air fryers. <code>link.amazon/B0c8moW59</code> opens a ThermoMaven '
        'meat thermometer and <code>link.amazon/B0f3GKalj</code> opens a CHEF iQ Sense thermometer, both under '
        'Kitchen Utensils &amp; Gadgets &gt; Thermometers &amp; Timers &gt; Meat. Three of the five links open '
        'air fryers. The site is written for air fryers only, so scope is now an owner decision, not a detail. '
        f'({src_links(["S70", "S71", "S72", "S73"])})</p></div>'
    )
    body += f"""
<h2>This session's pages</h2>
<div class="acards">
<a class="acard" href="intake.html"><span class="acard-meta">Register &middot; {DATE}</span><b>The five-link intake register</b><span>Intended product and observed destination kept in separate columns, per link, with the fetch date and the page that was read.</span><span class="acard-go">Open the register &rarr;</span></a>
<a class="acard" href="questions.html"><span class="acard-meta">Decision support &middot; {DATE}</span><b>Open questions: what we have, what we do not, how to find out</b><span>Twelve questions, each with the evidence already in hand, the gap, what it blocks and the concrete route to closing it.</span><span class="acard-go">Read the questions &rarr;</span></a>
<a class="acard" href="decision-lab.html"><span class="acard-meta">Review console &middot; {DATE}</span><b>The Decision Lab</b><span>Thirteen suggestions with the paths available, the question that gates each one, and the source that makes the constraint real. Nothing here is implemented by publishing it.</span><span class="acard-go">Open the console &rarr;</span></a>
<a class="acard" href="design-direction.html"><span class="acard-meta">Design &middot; {DATE}</span><b>Design direction and prompt pack</b><span>Why the site currently reads as generated, and the system, templates, copy rules and prompt to change that.</span><span class="acard-go">Read the pack &rarr;</span></a>
<a class="acard" href="executive-summary.html"><span class="acard-meta">Summary &middot; {DATE}</span><b>Executive summary</b><span>The state of the project in one page: what is true, what is missing, what needs a decision.</span><span class="acard-go">Read the summary &rarr;</span></a>
</div>
"""
    body += "<h2>Policy pages re-read this session</h2>"
    body += (
        "<p class=\"small\">Every quote used on these pages was re-read on 2026-11-17, not copied from an earlier "
        "session&rsquo;s note. Where an earlier session recorded the same wording, the earlier date is kept "
        "alongside it rather than replaced.</p>"
    )
    srows = [
        [e(s["id"]), f'<a href="{e(s["url"])}" target="_blank" rel="sponsored noopener noreferrer">{e(s["title"])}</a>',
         e(s["status"]), e(s.get("used_for", "")),
         src_links([s["id"]])]
        for s in VER["sources"]
    ]
    body += table(["ID", "Page read", "Status", "What it is used for", "Source"], srows)
    body += (
        '<p class="small">The sandbox this session ran in could only reach the network through the page-fetch tool; '
        'command-line fetches to amazon.com and link.amazon were refused at the connection layer. Every observation '
        'above is a tool-fetch result and names the URL that was fetched, so each one can be repeated by hand.</p>'
    )
    page("index.html", f"Session {SESSION} — five links, two categories, and the decisions that follow", body,
         "A live re-verification of all five submitted links, the two-category finding it produced, and the review "
         "pages that turn that finding into owner decisions rather than unilateral changes.",
         "Live re-verification of five Amazon affiliate links on 2026-11-17: three air fryers and two meat "
         "thermometers, with the open questions and design direction that follow.")


# ----------------------------------------------------------------- intake
def build_intake() -> None:
    rows = []
    for l in INTAKE["links"]:
        intended = (
            f'{unverified("owner has not confirmed the intended product")}'
            if l["intended_asin"] is None else e(l["intended_asin"])
        )
        confirmed = (
            unverified("no confirmation date recorded")
            if l["intended_confirmed_on"] is None else e(l["intended_confirmed_on"])
        )
        o = l["observed"]
        rows.append([
            f'<a id="{e(l["id"])}"></a>{e(l["id"])}',
            f'<a href="{e(l["submitted_url"])}" target="_blank" rel="sponsored noopener noreferrer">{e(l["submitted_url"])}</a>',
            f'{e(l["link_id"])} <span class="muted">({l["link_id_length"]} characters)</span>',
            intended,
            confirmed,
            f'<a href="{e(l["direct_check"]["url"])}" target="_blank" rel="sponsored noopener noreferrer">{e(l["direct_check"]["result"])}</a>'
            f' <span class="muted">({e(l["direct_check"]["observed_on"])})</span>',
            f'<a href="{e(o["final_url"])}" target="_blank" rel="sponsored noopener noreferrer">{e(o["page_id"])}</a>'
            f'<br><span class="muted">{e(o["page_title"][:120])}</span>',
            e(o["observed_on"]),
            e(l["category_observed"]),
            e(l["status"]),
            " ".join(f'<a class="flagid" href="{PREFIX}flagged.html#{e(f)}">{e(f)}</a>' for f in l["flags"]),
            src_links(o["source"] + l["direct_check"]["source"]),
        ])
    body = "<h2>Five submitted links, intended and observed kept apart</h2>"
    body += table(
        ["#", "Submitted link", "Identifier", "Intended ASIN", "Intended confirmed on",
         "Direct /dp/ check on the identifier", "Observed destination (separate field)", "Observed on",
         "Category observed on the destination", "Status", "Flags", "Source"],
        rows,
    )
    body += f"""
<div class="callout"><p><strong>Why the two sides are never merged.</strong> An intended ASIN is a claim by the
owner about what they meant to submit. An observed destination is what a live link served on a particular date.
Copying one into the other would invent a fact, so the intended columns stay empty until the owner fills them, and
the observed columns carry their own fetch date. Amazon defines an ASIN as a ten-character identifier
({src_links(["S82"])}); all five submitted identifiers are nine characters, and the direct
<code>amazon.com/dp/&lt;identifier&gt;</code> URL returns Page Not Found for every one of them
({src_links(["S74", "S75"])}).</p></div>
"""
    body += "<h2>What this register cannot tell you</h2><ul class=\"findings\">"
    for item in INTAKE["what_this_register_cannot_tell_you"]:
        body += f'<li>{e(item)} {src_links(["S80"])}</li>'
    body += "</ul>"
    body += f"""
<h2>The category finding</h2>
<div class="grid">
  <div class="stat"><div class="n">3</div><div class="l">Links opening air fryers (node 17659096011)</div></div>
  <div class="stat warn"><div class="n">2</div><div class="l">Links opening meat thermometers (node 289810)</div></div>
  <div class="stat bad"><div class="n">0 of 5</div><div class="l">Intended products confirmed by the owner</div></div>
  <div class="stat bad"><div class="n">0 of 5</div><div class="l">Links carrying an Associates tag</div></div>
</div>
<p class="small">{e(VER["category_observation"]["note"])} Air fryers: {e(VER["category_observation"]["air_fryers"])}.
Thermometers: {e(VER["category_observation"]["thermometers"])}. {src_links(VER["category_observation"]["sources"])}</p>
"""
    page("intake.html", "Five-link intake register", body,
         "The product-intent confirmation record for every link supplied in the brief. Intended product and "
         "observed destination sit in separate columns and are never merged; a gap is stated, not filled.",
         "Product-intent confirmation record for five Amazon affiliate links, with intended and observed values "
         "recorded separately and every row sourced to an official page.")


# ----------------------------------------------------------------- questions
def build_questions() -> None:
    body = (
        '<div class="callout"><p><strong>How to use this page.</strong> Each question states what is already known '
        'with the page it was read from, what is missing, what decision it blocks, and the concrete route to '
        'closing it. The answer field is deliberately empty: an answer is only recorded when the owner supplies it '
        'and dates it.</p></div>'
    )
    order = {"blocking": 0, "important": 1, "useful": 2}
    qs = sorted(LAB["questions"], key=lambda q: (order.get(q["priority"], 3), q["id"]))
    for q in qs:
        blocks = "".join(f'<a class="flagid" href="decision-lab.html#{e(b)}">{e(b)}</a>' for b in q["why_it_blocks"].split()) if False else ""
        body += f"""
<section class="card" id="{e(q['id'])}">
  <h3>{e(q['id'])} &middot; {e(q['question'])}</h3>
  <p>{chip(q['priority'], 'bad' if q['priority'] == 'blocking' else ('warn' if q['priority'] == 'important' else 'ok'))}
     <span class="muted">Answer:</span> <strong>{e(q['answer'] or 'Not answered yet — owner to complete, with a date')}</strong></p>
  <dl class="qa">
    <dt>What we have</dt><dd>{e(q['what_we_have'])} {src_links(q['have_sources'])}</dd>
    <dt>What we do not have</dt><dd>{e(q['what_we_do_not_have'])}</dd>
    <dt>Why it blocks a decision</dt><dd>{e(q['why_it_blocks'])}</dd>
    <dt>How to discover the missing information</dt><dd>{e(q['how_to_discover'])}</dd>
  </dl>
</section>
"""
    REPO_LINK = ('<a class="srcid" href="https://github.com/kanlerxz87-cyber/Zone3" target="_blank" '
                 'rel="noopener noreferrer">repository</a>')
    have_rows = []
    for h in LAB["have"]:
        cited = src_links(h["sources"]) if h["sources"] else ""
        have_rows.append([
            e(h["item"]),
            cited or ('<span class="muted">Repository observation, no external source</span> ' + REPO_LINK),
            cited or REPO_LINK,
        ])
    body += "<h2>What is already in hand</h2>" + table(["Information", "Where it came from", "Source"], have_rows)
    miss_basis = {
        "The Associates tag": ["S80"],
        "Owner confirmation of the five intended products": ["S70", "S71"],
        "Account approval state and API access": ["S80", "S82"],
        "Browse-node to rate-category mapping": ["S81"],
        "Any traffic, click or order figure": ["S80"],
        "Product photography rights": ["S79", "S80"],
        "A brand name and a byline": ["S07", "S24"],
        "Canonical host decision": None,
        "Target market": ["S79"],
        "Publishing cadence and approver": None,
    }
    miss_rows = []
    for m in LAB["missing"]:
        basis = miss_basis.get(m["item"])
        cell = src_links(basis) if basis else (
            '<a class="srcid" href="https://github.com/kanlerxz87-cyber/Zone3" target="_blank" '
            'rel="noopener noreferrer">repository</a> <span class="muted">(the topic plan and page set live here; '
            'no official source governs this choice)</span>'
        )
        miss_rows.append([
            e(m["item"]),
            " ".join(f'<a class="flagid" href="decision-lab.html#{e(b)}">{e(b)}</a>' for b in m["blocks"]),
            e(m["route"]),
            cell,
        ])
    body += "<h2>What is missing, and the route to each gap</h2>" + table(
        ["Missing information", "Blocks", "How to discover it", "Source of the constraint"], miss_rows)
    page("questions.html", "Open questions: what we have, what we do not, how to find out", body,
         "Twelve questions that have to be answered before the suggestions in the Decision Lab can be sensibly "
         "chosen between. Each one carries the evidence already in hand and a concrete route to the missing piece.",
         "A decision-support register: the questions blocking scope, revenue and design decisions on an Amazon "
         "affiliate site, each with the evidence in hand and the route to the missing information.")


# ----------------------------------------------------------------- decision lab
BASIS = {
    "SUG-2F-01": ["S72", "S73", "S76"],
    "SUG-2F-02": ["S79", "S80"],
    "SUG-2F-03": ["S79"],
    "SUG-2F-04": ["S79", "S80"],
    "SUG-2F-05": ["S80"],
    "SUG-2F-06": ["S80", "S82"],
    "SUG-2F-07": ["S79"],
    "SUG-2F-08": ["S80"],
    "SUG-2F-09": ["S80", "S24"],
    "SUG-2F-10": None,
    "SUG-2F-11": ["S80"],
    "SUG-2F-12": ["S07", "S24"],
    "SUG-2F-13": ["S79"],
}


def build_lab() -> None:
    body = "<h2>How this console works</h2><ol class=\"workflow\">"
    for step in LAB["workflow"]:
        body += f"<li>{e(step)}</li>"
    body += "</ol>"
    body += (
        '<div class="callout"><p><strong>Nothing here is implemented by publishing it.</strong> A suggestion moves '
        'to scheduled only when the owner records a decision, names the path chosen and dates it. The statuses are: '
        + "; ".join(f"<strong>{e(k)}</strong> &mdash; {e(v)}" for k, v in LAB["statuses"].items())
        + ".</p></div>"
    )
    rows = []
    for s in LAB["suggestions"]:
        rows.append([
            f'<a href="decision-lab.html#{e(s["id"])}">{e(s["id"])}</a>',
            e(s["title"]),
            e(s["area"]),
            chip(s["status"], {"ready": "ok", "blocked": "bad", "proposed": "warn", "rejected": "grey"}.get(s["status"], "warn")),
            " ".join(f'<a class="flagid" href="questions.html#{e(q)}">{e(q)}</a>' for q in s["depends_on"]) or '<span class="muted">none</span>',
            src_links(BASIS.get(s["id"])) if BASIS.get(s["id"]) else (
                '<a class="srcid" href="https://github.com/kanlerxz87-cyber/Zone3" target="_blank" '
                'rel="noopener noreferrer">repository</a> <span class="muted">(internal choice; no official source governs it)</span>'),
        ])
    body += "<h2>Every suggestion at a glance</h2>" + table(
        ["ID", "Suggestion", "Area", "Status", "Blocking question", "Source of the constraint"], rows)
    body += "<h2>The suggestions, with the paths to choose between</h2>"
    for s in LAB["suggestions"]:
        ev = "".join(
            f'<li>{e(x["quote"])} <span class="muted">&mdash; {e(x["section"])}</span> {src_links(x["source"])}</li>'
            for x in s["evidence"]
        )
        paths = "".join(
            f'<div class="path"><b>{e(p["id"])} &middot; {e(p["label"])}</b>'
            f'<p>{e(p["detail"])}</p>'
            f'<p class="small"><em>Trade-off:</em> {e(p["tradeoff"])}</p></div>'
            for p in s["paths"]
        )
        deps = " ".join(f'<a class="flagid" href="questions.html#{e(q)}">{e(q)}</a>' for q in s["depends_on"]) or '<span class="muted">No blocking question &mdash; this one can be scheduled today.</span>'
        body += f"""
<section class="card" id="{e(s['id'])}">
  <h3>{e(s['id'])} &middot; {e(s['title'])}</h3>
  <p>{chip(s['area'], 'info')} {chip(s['status'], {'ready': 'ok', 'blocked': 'bad', 'proposed': 'warn', 'rejected': 'grey'}.get(s['status'], 'warn'))}
     <span class="muted">{e(s['status_reason'])}</span></p>
  <p><strong>What:</strong> {e(s['what'])}</p>
  <p><strong>Why:</strong> {e(s['why'])}</p>
  <p class="small"><strong>Blocking question:</strong> {deps}</p>
  <div class="paths">{paths}</div>
  <p class="small"><strong>Effort:</strong> {e(s['effort'])} &middot; <strong>Risk:</strong> {e(s['risk'])}</p>
  <p class="small"><strong>How we would know it worked:</strong> {e(s['verification'])}</p>
  <p class="small"><strong>Constraint this must respect:</strong> {src_links(BASIS.get(s['id'])) if BASIS.get(s['id']) else '<span class="muted">No Amazon or FTC constraint applies; this is an internal choice.</span>'}</p>
  <ul class="findings">{ev}</ul>
</section>
"""
    page("decision-lab.html", "Decision Lab: review the suggestions, then choose", body,
         "Thirteen proposals for the site, each with the paths available, the question that must be answered "
         "before a path can be chosen, and the source that makes the constraint real. Nothing on this page is "
         "implemented by publishing it.",
         "A suggestions review console for an Amazon affiliate site: thirteen proposals with paths, blocking "
         "questions and the official sources behind each constraint.")


# ----------------------------------------------------------------- design direction
def build_design() -> None:
    body = "<h2>The rules the design has to work inside</h2>"
    rows = [
        [e(r["rule"]), f'&ldquo;{e(r["quote"])}&rdquo; <span class="muted">&mdash; {e(r["section"])}</span>',
         e(r["design_consequence"]), src_links(r["source"])]
        for r in DESIGN["hard_rules"]
    ]
    body += table(["Rule", "Wording read from the official page", "What it forces in the design", "Source"], rows)
    body += (
        f'<p class="small">{e(DESIGN["constraint_line"])}</p>'
    )
    body += "<h2>Why it currently reads as generated</h2>"
    drows = []
    for d in DESIGN["diagnosis"]:
        link = (
            '<a class="srcid" href="https://github.com/kanlerxz87-cyber/Zone3" target="_blank" '
            'rel="noopener noreferrer">repository</a>'
        )
        drows.append([
            e(d["finding"]), e(d["detail"]), e(d["evidence"]),
            chip(d["severity"], {"high": "bad", "medium": "warn", "low": "ok"}.get(d["severity"], "warn")),
            link,
        ])
    body += table(["Finding", "Detail", "Evidence", "Severity", "Source"], drows)
    body += "<h2>Principles</h2><ol class=\"workflow\">"
    for p in DESIGN["principles"]:
        body += f"<li>{e(p)}</li>"
    body += "</ol>"
    ds = DESIGN["design_system"]
    body += f"""
<h2>One design system</h2>
<section class="card">
  <h3>Type</h3>
  <ul class="findings">
    <li>Display: {e(ds['type']['display'])}</li>
    <li>Body: {e(ds['type']['body'])}</li>
    <li>Weights: {e(ds['type']['weights'])}</li>
    <li>Rule: {e(ds['type']['rule'])}</li>
  </ul>
  <h3>Colour</h3>
  <ul class="findings">
    <li>Ink and paper: {e(ds['colour']['ink'])}</li>
    <li>Accents: {e(ds['colour']['accent'])}</li>
    <li>Surfaces: {e(ds['colour']['surfaces'])}</li>
    <li>Semantics: {e(ds['colour']['semantics'])}</li>
    <li>Rule: {e(ds['colour']['rule'])}</li>
  </ul>
  <h3>Grid</h3>
  <ul class="findings">
    <li>{e(ds['grid']['max_width'])}</li>
    <li>{e(ds['grid']['cards'])}</li>
    <li>{e(ds['grid']['radius'])}</li>
    <li>{e(ds['grid']['mobile'])}</li>
  </ul>
  <h3>Imagery</h3>
  <ul class="findings">
    <li>{e(ds['imagery']['rule'])}</li>
    <li>{e(ds['imagery']['ratio'])}</li>
    <li>{e(ds['imagery']['caption'])}</li>
  </ul>
</section>
"""
    body += "<h2>Page templates</h2>"
    trows = []
    for t in DESIGN["templates"]:
        trows.append([
            e(t["page"]),
            "<ol class=\"workflow\">" + "".join(f"<li>{e(b)}</li>" for b in t["blocks"]) + "</ol>",
            '<a class="srcid" href="https://github.com/kanlerxz87-cyber/Zone3" target="_blank" rel="noopener noreferrer">repository</a> <span class="muted">(editorial specification, not a sourced claim)</span>',
        ])
    body += table(["Page", "Blocks, in order", "Source"], trows)
    body += "<h2>Copy rules</h2><ol class=\"workflow\">"
    for c in DESIGN["copy_rules"]:
        body += f"<li>{e(c)}</li>"
    body += "</ol>"
    body += "<h2>Banned phrases</h2><p class=\"small\">Enforced by a build check, not by good intentions.</p><ul class=\"banned\">"
    for p in DESIGN["banned_phrases"]:
        body += f"<li>{e(p)}</li>"
    body += "</ul>"
    body += "<h2>Anti-slop checklist</h2><ol class=\"workflow\">"
    for c in DESIGN["anti_slop_checklist"]:
        body += f"<li>{e(c)}</li>"
    body += "</ol>"
    body += "<h2>What not to do</h2><ul class=\"findings\">"
    for c in DESIGN["what_not_to_do"]:
        body += f"<li>{e(c)}</li>"
    body += "</ul>"
    body += (
        '<h2>The prompt, ready to paste into a design tool</h2>'
        '<p class="small">Everything above, written as a single brief. It names the hard constraints first so a '
        'generated design cannot quietly break a rule.</p>'
        f'<pre class="prompt">{e(DESIGN["prompt"])}</pre>'
    )
    page("design-direction.html", "Design direction and prompt pack", body,
         "Why the published site reads as assembled rather than designed, and the system, templates, copy rules "
         "and prompt that would change that — inside the rules Amazon and the FTC set.",
         "A design direction and prompt pack for turning an Amazon affiliate audit site into a publication, with "
         "the Operating Agreement and Program Policies constraints quoted and sourced.")


# ----------------------------------------------------------------- executive summary
def build_summary() -> None:
    body = """
<h2>Where the project stands</h2>
<div class="grid">
  <div class="stat"><div class="n">5</div><div class="l">Submitted links, all opening live listings</div></div>
  <div class="stat warn"><div class="n">2 of 5</div><div class="l">Links opening a category the site is not written for</div></div>
  <div class="stat bad"><div class="n">0 of 5</div><div class="l">Links carrying an Associates tag, so none can earn</div></div>
  <div class="stat bad"><div class="n">0 of 5</div><div class="l">Intended products confirmed by the owner</div></div>
  <div class="stat"><div class="n">13</div><div class="l">Official pages read or re-read this session</div></div>
  <div class="stat"><div class="n">10</div><div class="l">Irregularities raised for review</div></div>
</div>
<h2>Key findings</h2>
<ul class="findings">
"""
    body += (
        '<li>The brief now carries five product links, not three. Three open air-fryer listings; the two added '
        'this session open meat-thermometer listings. The site\'s name, navigation and article plan are written '
        'for air fryers only, so scope is now an owner decision rather than a detail. '
        f'{src_links(["S70", "S71", "S72", "S73"])}</li>'
    )
    body += (
        '<li>All five mapping results are stable. The first three destinations are identical to every capture '
        f'since 2026-11-13; the two new ones were read for the first time on {DATE}. '
        f'{src_links(["S76", "S77", "S78"])}</li>'
    )
    body += (
        '<li>None of the five identifiers is an ASIN. Amazon defines an ASIN as a ten-character alphanumeric '
        'identifier; all five are nine characters and the direct /dp/ URL returns Page Not Found for every one. '
        f'{src_links(["S82", "S74", "S75"])}</li>'
    )
    body += (
        '<li>No link on the site can earn anything yet: every Special Link must carry the Associates tag as a URL '
        'parameter, and no tag has been supplied. ' + src_links(["S80"]) + '</li>'
    )
    body += (
        '<li>Prices, star ratings and review counts are blank by rule, not by omission: they may be shown only '
        'through an Amazon-served link or the API. ' + src_links(["S80"]) + '</li>'
    )
    body += (
        '<li>The published rate table gives Kitchen 4.50 per cent, Home 3.00 per cent and All Other Categories '
        '4.00 per cent, but no official page read in this project maps a browse node to a rate category, so no '
        'per-product rate can be stated. ' + src_links(["S81"]) + '</li>'
    )
    body += (
        '<li>The disclosure wording is unchanged and is read verbatim from the Operating Agreement: "As an Amazon '
        'Associate I earn from qualifying purchases." ' + src_links(["S79"]) + '</li>'
    )
    body += (
        '<li>The site builds clean: no broken links across the published page set, a sitemap that matches the '
        'placeholder text. The problem is not correctness, it is presentation. '
        '<a class="srcid" href="https://github.com/kanlerxz87-cyber/Zone3" target="_blank" rel="noopener noreferrer">repository</a></li>'
    )
    body += "</ul>"
    body += """
<h2>What needs a decision before anything is built</h2>
"""
    blocking = [q for q in LAB["questions"] if q["priority"] == "blocking"]
    rows = [
        [f'<a href="questions.html#{e(q["id"])}">{e(q["id"])}</a>', e(q["question"]),
         e(q["what_we_do_not_have"]), e(q["how_to_discover"]), src_links(q["have_sources"])]
        for q in blocking
    ]
    body += table(["ID", "Question", "The gap", "How to close it", "Source"], rows)
    body += """
<h2>What this session did and did not change</h2>
<ul class="findings">
  <li><strong>Did:</strong> re-verified all five links live; recorded the two new destinations and their category;
      re-read the Operating Agreement, the Program Policies, the rate table and the ASIN definition; published the
      intake register, the questions register, the Decision Lab and the design direction under this session's own
      directory.</li>
  <li><strong>Did not:</strong> rename the site, change the shared navigation beyond adding one link group,
      publish a price, rating or commission rate for any product, or implement any suggestion. Every suggestion is
      published for review with the paths available, and none is scheduled until the owner chooses one.</li>
</ul>
"""
    page("executive-summary.html", "Executive summary — five links, two categories, thirteen decisions", body,
         "The state of the Zone3 affiliate project on 2026-11-17: what is verified, what is missing, and the "
         "decisions that gate every suggested change.",
         "Executive summary of the Zone3 Amazon affiliate project: five product links across two categories, no "
         "Associates tag yet, and thirteen owner decisions published for review.")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    build_index()
    build_intake()
    build_questions()
    build_lab()
    build_design()
    build_summary()
    print(f"built {len(list(OUT.glob('*.html')))} pages in sessions/{SESSION}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

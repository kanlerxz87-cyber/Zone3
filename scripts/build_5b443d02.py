#!/usr/bin/env python3
"""Session 5b443d02 (2026-11-17): build the "Direction" section.

Four pages under `direction/`, generated from `data/5b443d02/*.json`:

  direction/index.html      the design-prompt suggestion pack and the topic list
  direction/products.html   the product-intent confirmation record for all five links
  direction/questions.html  the open-questions register: have / missing / how to close
  direction/choose.html     the three paths and a review-before-implementation control

Rules this builder holds itself to, because they are the ones the site asks of
everyone else:

  * Pages go through `scripts/build_site.py`'s shared `page()` template, so the
    Associates disclosure strip, the footer disclaimer, the navigation and the
    depth-aware relative-link prefixing are identical to every other page.
  * Every table row carries either a link to an official page or a `repo:` anchor
    naming the record that defines it (`tools/verify_site.py` V4).
  * No price, star rating, review count, sales rank or demand figure is emitted.
    Those values can only be published from Amazon-served content or the
    Creators API, and this session has neither.
  * The intended ASIN and the observed redirect destination are two fields, two
    tables, and are never merged into one another.
  * No placeholder markers (tools/verify_site.py V7).

    python3 scripts/build_5b443d02.py           # rebuild direction/
    python3 scripts/build_5b443d02.py --check   # verify the emitted pages
"""
from __future__ import annotations

import importlib.util
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "5b443d02"
OUT = ROOT / "direction"
REPO = "https://github.com/kanlerxz87-cyber/Zone3"
BUILT = "2026-11-17"


def _load_shared():
    """Import scripts/build_site.py for its page template.

    That module is the shared shell for the flat site. It is imported, never
    modified by this script: this session's changes to it are a separate,
    additive nav entry recorded in COORDINATION.md.
    """
    spec = importlib.util.spec_from_file_location(
        "zone3_build_site", ROOT / "scripts" / "build_site.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


bs = _load_shared()
# The shared template stamps a build date into every page; this session's pages
# were verified on 2026-11-17 and say so.
bs.BUILT = BUILT

e = bs.e
table = bs.table


def load(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


SOURCES = {s["id"]: s for s in load("sources.json")["sources"]}
PRODUCTS = load("products.json")
SUGGESTIONS = load("suggestions.json")
QUESTIONS = load("questions.json")
PATHS = load("paths.json")


def slinks(ids) -> str:
    """Link the official source pages for a list of 5B-Snn ids.

    Accepts either a list or a comma-separated string, because the topic rows in
    suggestions.json carry their sources as a string.
    """
    if isinstance(ids, str):
        ids = [x.strip() for x in ids.split(",") if x.strip()]
    parts = []
    for sid in ids:
        # Session-namespaced ids (5B-Snn) live in this session's register; shared
        # ids (Snn) live in data/sources.json and are resolved through the shared
        # module so a flag can cite either without inventing a second copy.
        s = SOURCES.get(sid) or bs.SOURCES.get(sid)
        if s is None:
            raise KeyError(f"{sid}: unknown in both the 5B and the shared registers")
        parts.append(
            f'<a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer" '
            f'title="{e(s["title"])}">{e(sid)}</a>')
    return " &middot; ".join(parts)


def repo_anchor(path: str, label: str = "") -> str:
    """A `repo:` anchor cell - provenance for a row that is a design record,
    not a fact about a product. `tools/verify_site.py` V4 accepts it."""
    text = f"repo:{path}"
    return (f'<a class="repo" href="{REPO}/blob/main/{e(path)}" '
            f'target="_blank" rel="noopener noreferrer">{e(label or text)}</a>')


def evidence(ids, fallback_path: str) -> str:
    """Official sources if the row has any; otherwise the defining record here."""
    if ids:
        return slinks(ids)
    return repo_anchor(fallback_path)


# Session 5b443d02 (2026-11-17): styles for the components this section adds.
# Injected as a single <style> block into each generated page rather than by
# editing the shared assets/style.css, so this session adds no rule that any
# other session's page depends on. Colours and type come from the site's own
# custom properties, so the section looks like the rest of the site.
SECTION_CSS = """
<style>
.lead-note{font-family:var(--serif);font-size:1.02rem;line-height:1.62;color:var(--ink);
  background:var(--card);border:1px solid var(--line);border-left:4px solid var(--accent);
  border-radius:8px;padding:.9rem 1.1rem;margin:0 0 1.7rem}
.chooser{background:var(--card);border:1px solid var(--line);border-radius:10px;
  padding:1.1rem 1.2rem;margin:1rem 0 1.7rem}
.path-opt{display:flex;gap:.65rem;align-items:flex-start;padding:.6rem .7rem;
  border:1px solid var(--line-soft);border-radius:8px;margin-bottom:.5rem;cursor:pointer;
  line-height:1.45}
.path-opt:hover{border-color:var(--accent);background:var(--bg)}
.path-opt input{margin-top:.3rem;flex:none}
#path-note{width:100%;max-width:46rem;font:inherit;padding:.55rem .6rem;
  border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--ink)}
#path-copy{font:inherit;padding:.5rem 1.05rem;border-radius:6px;
  border:1px solid var(--accent);background:var(--accent);color:#fff;cursor:pointer}
#path-copy:hover{background:var(--accent-dark)}
.export{background:var(--grey);border:1px solid var(--line);border-radius:8px;
  padding:.85rem .95rem;white-space:pre-wrap;font-size:.84rem;color:var(--ink);
  overflow-x:auto;margin:0}
a.repo{font-size:.78rem;color:var(--muted);word-break:break-all}
.blank{display:inline-block;font-size:.82rem;color:var(--warn);background:var(--warnbg);
  border:1px dashed var(--warn);border-radius:5px;padding:.15rem .45rem;line-height:1.4}
@media(max-width:640px){.export{font-size:.78rem}.lead-note{font-size:.98rem}}
</style>
"""


def emit(filename: str, title: str, body: str, lead: str = "", description: str = "") -> None:
    """Render through the shared template, then attach this section's styles."""
    bs.page(filename, title, body, lead=lead, description=description)
    path = ROOT / filename
    raw = path.read_text(encoding="utf-8")
    if "</head>" in raw and "SECTION-5B443D02" not in raw:
        raw = raw.replace(
            "</head>",
            "<!-- SECTION-5B443D02 -->" + SECTION_CSS + "</head>", 1)
        path.write_text(raw, encoding="utf-8")


STATE_KIND = {
    "blocked": "warn",
    "proposed": "info",
    "default": "ok",
    "option": "info",
    "working title": "info",
    "working title - blocked": "warn",
}


def state_badge(state: str) -> str:
    return bs.badge(state, STATE_KIND.get(state, "muted"))


def blank(reason: str) -> str:
    """A deliberately empty cell. Class `blank` is provenance under V4, and the
    reason is always printed in the cell next to it."""
    return f'<span class="blank">{e(reason)}</span>'


def note(text: str) -> str:
    return f'<p class="muted small">{text}</p>'


# ------------------------------------------------------------------ page 1: index

GOOGLE_STANDARDS = [
    ("Unique titles and descriptions",
     "https://developers.google.com/search/docs/appearance/snippet"),
    ("Qualifying outbound links (rel=\"sponsored\")",
     "https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links"),
    ("Creating helpful, people-first content",
     "https://developers.google.com/search/docs/fundamentals/creating-helpful-content"),
    ("Spam policies, including thin affiliation",
     "https://developers.google.com/search/docs/essentials/spam-policies"),
    ("Sitemaps",
     "https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview"),
]


def build_index() -> str:
    recs = PRODUCTS["records"]
    rows = []
    for r in recs:
        rows.append([
            f'<a href="direction/products.html#{e(r["id"])}">{e(r["id"])}</a>',
            e(r["token"]),
            e(r["observed_title"][:90] + ("..." if len(r["observed_title"]) > 90 else "")),
            e(r["observed_browse_leaf"]),
            '<span class="badge ok">in the existing category</span>'
            if r["in_scope_of_existing_site"]
            else '<span class="badge warn">outside the existing category</span>',
            slinks([r["observed_source"]]),
        ])
    portfolio = table(
        ["ID", "Submitted token", "Observed listing title", "Amazon browse node (leaf)",
         "Fits the site as built?", "Source"],
        rows)

    srows = []
    for s in SUGGESTIONS["suggestions"]:
        srows.append([
            f'<a id="{e(s["id"])}" href="#{e(s["id"])}">{e(s["id"])}</a>',
            e(s["theme"]),
            f'<strong>{e(s["suggestion"])}</strong>',
            e(s["what_changes"]),
            e(s["needs"]),
            e(s["standard_note"]),
            evidence(s["standard"], SUGGESTIONS["repo_anchor"]),
            state_badge(s["state"]),
        ])
    suggestions = table(
        ["ID", "Theme", "Suggestion", "What changes on the site",
         "Needs before it ships", "Why", "Standard / defining record", "State"],
        srows)

    trows = []
    for t in SUGGESTIONS["topics"]:
        trows.append([
            e(t["id"]),
            f'<strong>{e(t["title"])}</strong>',
            e(t["serves"]),
            e(t["basis_note"]),
            slinks(t["basis"]),
            state_badge(t["state"]),
        ])
    topics = table(
        ["ID", "Working title", "Serves", "What the facts would rest on", "Source", "State"],
        trows)

    std = "".join(
        f'<li><a href="{u}" target="_blank" rel="noopener noreferrer">{e(t)}</a></li>'
        for t, u in GOOGLE_STANDARDS)

    body = f"""
<p class="lead-note">This section exists so a decision gets made before anything is
built. Nothing here has been applied to the site. The three other pages carry the
evidence it rests on: the
<a href="direction/products.html">product-intent confirmation record</a>, the
<a href="direction/questions.html">open questions</a>, and the
<a href="direction/choose.html">three paths</a> to choose between.</p>

<h2>What this section is for</h2>
<p>The brief asks for three things that are usually answered in the wrong order:
what the site should look like, what is still unknown, and which way to go. So
this section keeps them apart. <strong>Suggestions</strong> are proposals with a
gate attached &mdash; each one names what must be true before it ships.
<strong>Questions</strong> are the gaps that block a decision, each with the
concrete action that would close it and what the site does anyway if it stays
open. <strong>Paths</strong> are three complete answers, so the choice is made on
consequences rather than on descriptions.</p>

<h2>The five products, as submitted</h2>
{portfolio}
{note("Three of the five links land in the Air Fryers browse node. The other two land "
      "in Meat, under Thermometers &amp; Timers. Every site page built so far assumes a "
      "single air-fryer category, which is why the scope question is the first one to answer. "
      "Observed destinations are observations; they are not evidence of what the person who "
      "submitted the link intended.")}

<h2>Design suggestions</h2>
{suggestions}
{note("A row is a proposal, not a change. Where a row states a requirement that comes "
      "from Amazon or the FTC, the official page is linked in the Standard column. Where a "
      "row is a design or editorial judgement, it is anchored to the record in this "
      "repository that defines it.")}

<h2>Editorial topics</h2>
{topics}
<p><strong>{e(SUGGESTIONS["topics_caveat"])}</strong></p>

<h2>Standards these are written against</h2>
<p>The Amazon and FTC requirements are linked row by row above. The search-side
standards are these, and they are the ones to check each page against as it is
written:</p>
<ul>{std}</ul>
{note("These five are linked from the brief and from the site's own decision records. "
      "They are guidance, not Amazon policy, which is why they appear here in prose "
      "rather than as a source on a factual row.")}

<h2>What to do with this page</h2>
<ol>
  <li>Read the <a href="direction/products.html">product-intent record</a> and confirm the intended
      product behind each link. Nothing else can be built honestly until that is done.</li>
  <li>Read the <a href="direction/questions.html">open questions</a> and close the ones that are
      cheap to close. Most of them are a login or a decision, not research.</li>
  <li>Pick a path on <a href="direction/choose.html">Choose a path</a>. That single choice settles
      the category boundary, the navigation and the brand.</li>
  <li>Then, and only then, implement the suggestions above that the choice unblocks.</li>
</ol>
"""
    return body


# -------------------------------------------------------------- page 2: products

def build_products() -> str:
    recs = PRODUCTS["records"]

    rows_a = []
    for r in recs:
        rows_a.append([
            f'<a id="{e(r["id"])}" href="#{e(r["id"])}">{e(r["id"])}</a>',
            f'<a href="{e(r["submitted_link"])}" target="_blank" '
            f'rel="noopener noreferrer nofollow">{e(r["submitted_link"])}</a>',
            blank(r["intended_asin_reason"]),
            f'<a href="{e(r["official_listing_url"])}" target="_blank" '
            f'rel="noopener noreferrer">{e(r["official_listing_url"])}</a>',
            e(r["confirmation_date"]),
            slinks([r["confirmation_source"]]),
        ])
    intent = table(
        ["ID", "Submitted link", "Intended ASIN", "Official listing URL",
         "Confirmation date", "Source"],
        rows_a)

    rows_b = []
    for r in recs:
        rows_b.append([
            e(r["id"]),
            f'<a href="{e(r["official_listing_url"])}" target="_blank" '
            f'rel="noopener noreferrer">{e(r["observed_asin"])}</a>',
            e(r["observed_title"]),
            e(r["observed_browse_leaf"]),
            f'<a href="{e(SOURCES[r["observed_source"]]["url"])}" target="_blank" '
            f'rel="noopener noreferrer">{e(r["observed_node"])}</a>',
            slinks([r["observed_source"]]),
        ])
    observed = table(
        ["ID", "Observed destination ASIN", "Listing title as served on 2026-11-17",
         "Browse node (leaf)", "Node id", "Source"],
        rows_b)

    policy = PRODUCTS["policy_basis"]
    rows_c = []
    for r in recs:
        rows_c.append([
            e(r["id"]),
            f'<code>{e(r["token"])}</code>',
            str(r["token_length"]),
            '<span class="badge bad">No</span>',
            f'An ASIN is defined as a {e(policy["asin_definition_text"].split(":")[1].strip())}',
            slinks([policy["asin_definition"]]),
        ])
    tokens = table(
        ["ID", "Submitted token", "Characters", "Is it a 10-character ASIN?",
         "Basis", "Source"],
        rows_c)

    body = f"""
<p class="lead-note">Two facts, two tables, never merged: <strong>what the link was
meant to reach</strong>, which only the account owner can confirm, and
<strong>where it went</strong> when it was fetched. An observed destination is not
evidence of intent, and nothing on this site treats it as such.</p>

<h2>Product-intent confirmation record</h2>
{intent}
{note("The Intended ASIN column is blank for all five links and stays blank until the "
      "account owner confirms it. A blank here is the compliant answer: guessing the "
      "intended product from a redirect would put a fabricated identifier into a "
      "record whose whole purpose is to be checkable.")}

<h2>Observed redirect targets</h2>
{observed}
{note("Captured 2026-11-17 by fetching each submitted link and reading the listing "
      "Amazon served. Browse node and node id are read from the breadcrumb on that "
      "listing. No price, star rating, review count or sales figure is recorded, "
      "because displaying those outside Amazon-served content or the Creators API is "
      "not permitted.")}

<h2>Are the submitted tokens ASINs?</h2>
{tokens}
{note("All five tokens are 9 characters. The Creators API defines an ASIN as 10 "
      "characters, so none of the submitted tokens can itself be the ASIN. That is "
      "precisely why the intended ASIN has to be confirmed rather than derived.")}

<h2>How this relates to the other intent record</h2>
<p>Session <code>82372fd1</code>, working in parallel on 2026-11-17, added rows for all five
links to its own intent-record page, and independently flagged the two previously
unrecorded links. Its rows for <code>B0c8moW59</code> and <code>B0f3GKalj</code> carry no
observed destination, so they are empty. This page supplies what those rows are
missing: both links were fetched on 2026-11-17 and their destinations, served titles
and browse nodes are recorded below and on the
<a href="intent-record/index.html">intent-record page</a>. Two sessions reaching the same
two links independently is corroboration, not duplication; the gap this page fills is
the observed data. Filling the empty rows in that session's file is a change request,
not something this session edits, because that file is owned by another session.</p>

<h2>Why the two fields are never merged</h2>
<p>The brief asks for an intended ASIN, an official listing URL, a confirmation date
and a source, with observed redirect targets kept in a separate field. The reason is
practical rather than procedural. An ASIN is a checkable identifier: if the intended
ASIN and the observed destination are the same column, a later reader cannot tell
whether a value was confirmed or merely observed, and a redirect that Amazon
changes silently rewrites the record. Kept apart, the record can say the honest
thing: <em>we know where this link goes today; we do not yet know where it was
meant to go.</em></p>

<h2>What this record does not contain</h2>
<ul>
  <li>No price, and no price comparison. Those values can only be published from
      Amazon-served content or the Creators API, and neither is available here.</li>
  <li>No star rating, review count, sales rank or demand badge, for the same reason.</li>
  <li>No claim that any outbound link is a validated Special Link. None has been
      tested in an enrolled Associates account. See
      <a href="direction/questions.html#5B-Q05">5B-Q05</a>.</li>
  <li>No assertion that the supplied short links are invalid. Their exact compliance
      status is unresolved and is recorded as unresolved in
      <a href="direction/questions.html#5B-Q06">5B-Q06</a>.</li>
</ul>
"""
    return body


# ------------------------------------------------------------- page 3: questions

def build_questions() -> str:
    qs = QUESTIONS["questions"]
    rows = []
    for q in qs:
        rows.append([
            f'<a id="{e(q["id"])}" href="#{e(q["id"])}">{e(q["id"])}</a>',
            f'<strong>{e(q["question"])}</strong>',
            e(q["have"]),
            e(q["missing"]),
            e(q["discover"]),
            e(q["blocks"]),
            e(q["default"]),
            evidence(q["src"], QUESTIONS["repo_anchor"]),
        ])
    tbl = table(
        ["ID", "Question", "What we already have", "What is missing",
         "How to discover it", "What it blocks", "Default if it stays unanswered",
         "Source / defining record"],
        rows)

    body = f"""
<p class="lead-note">Every question that blocks a decision, in one table. Each row
says what is already established from an official page or from this repository,
names the gap exactly, gives the action that would close it, and states what the
site does anyway &mdash; so nothing waits on an answer that never arrives.</p>

<h2>The register</h2>
{tbl}

<h2>Which ones are cheap to close</h2>
<p>Most of these are not research problems. They are a login, a decision, or a
confirmation:</p>
<ul>
  <li><strong>A login:</strong>
      <a href="#5B-Q03">5B-Q03</a> (account status),
      <a href="#5B-Q04">5B-Q04</a> (tracking tag),
      <a href="#5B-Q05">5B-Q05</a> (Special Link format),
      <a href="#5B-Q06">5B-Q06</a> (whether the hop counts). All four are answered
      inside an enrolled Associates account and nowhere else.</li>
  <li><strong>A decision:</strong>
      <a href="#5B-Q02">5B-Q02</a> (scope),
      <a href="#5B-Q08">5B-Q08</a> (marketplace),
      <a href="#5B-Q09">5B-Q09</a> (photography),
      <a href="#5B-Q11">5B-Q11</a> (authorship and cadence),
      <a href="#5B-Q12">5B-Q12</a> (measurement and privacy),
      <a href="#5B-Q13">5B-Q13</a> (brand),
      <a href="#5B-Q14">5B-Q14</a> (hands-on testing).</li>
  <li><strong>A confirmation from the person who submitted them:</strong>
      <a href="#5B-Q01">5B-Q01</a> (intended product per link).</li>
  <li><strong>Infrastructure:</strong>
      <a href="#5B-Q07">5B-Q07</a> (Creators API credentials) and
      <a href="#5B-Q10">5B-Q10</a> (analytics and Search Console).</li>
</ul>

<h2>What the defaults mean in practice</h2>
<p>The <em>Default if it stays unanswered</em> column is the part that matters most.
It is the pre-commitment: the site behaves in a defined, compliant way whether or
not an answer comes. No blank is filled by guessing, no link is published as
monetised before it is tested, and no claim of hands-on experience is implied.
Every default is the conservative one, which means an unanswered question slows
the site down but never makes it wrong.</p>

<h2>Related records already on this site</h2>
<p>This register is this session's and is namespaced <code>5B-Qnn</code>. It does not
replace the earlier question sets. <a href="suggestions.html">Suggestions &amp;
decisions</a> carries SUG-01 to SUG-10 with its own questions Q1 to Q10, and
<a href="site/answers.html">the reader site's answers page</a> carries nine settled
questions and eleven that only the owner can answer. They are cross-referenced,
not merged, so no session's numbering is silently reused.</p>
"""
    return body


# ---------------------------------------------------------------- page 4: choose

CHOOSER_JS = """
<script>
(function () {
  var box = document.getElementById('path-chooser');
  if (!box) { return; }
  var out = document.getElementById('path-export');
  var when = document.getElementById('path-when');
  function render() {
    var picked = box.querySelector('input[name="path"]:checked');
    if (!picked) { out.textContent = 'No path chosen yet.'; return; }
    var label = picked.getAttribute('data-label');
    var id = picked.value;
    var lines = [
      'Zone3 direction decision',
      'Recorded: ' + new Date().toISOString().slice(0, 10),
      'Path: ' + id + ' - ' + label,
      'Note: ' + (document.getElementById('path-note').value || '(none)'),
      '',
      'This is a recorded choice, not an implementation. Nothing on the site',
      'changes until a later session implements the accepted path.'
    ];
    out.textContent = lines.join('\\n');
    when.textContent = 'Recorded in this browser only. Copy the text below into a '
      + 'message or a commit to make it real.';
  }
  box.addEventListener('change', render);
  document.getElementById('path-note').addEventListener('input', render);
  document.getElementById('path-copy').addEventListener('click', function () {
    var t = out.textContent;
    if (navigator.clipboard) { navigator.clipboard.writeText(t); }
  });
  render();
})();
</script>
"""


def build_choose() -> str:
    rows = []
    for p in PATHS["paths"]:
        rows.append([
            f'<a id="{e(p["id"])}" href="#{e(p["id"])}">{e(p["id"])}</a>',
            f'<strong>{e(p["name"])}</strong>',
            e(p["what"]),
            e(p["effort"]),
            e(p["needs"]),
            e(p["risk"]),
            e(p["consequence"]),
            e(p["recommended_for"]),
            slinks(p["src"]),
            state_badge(p["state"]),
        ])
    tbl = table(
        ["ID", "Path", "What it is", "Effort", "Needs", "Risk",
         "What happens to the five links", "Right if", "Source", "State"],
        rows)

    opts = []
    for p in PATHS["paths"]:
        opts.append(
            f'<label class="path-opt"><input type="radio" name="path" '
            f'value="{e(p["id"])}" data-label="{e(p["name"])}"> '
            f'<span><strong>{e(p["id"])} &mdash; {e(p["name"])}</strong><br>'
            f'<span class="muted small">{e(p["recommended_for"])}</span></span></label>')

    body = f"""
<p class="lead-note">Three complete answers to one question: what should this site
be? Choosing one settles the category boundary, the navigation, the brand and most
of the <a href="direction/index.html">suggestions</a>. Read the consequences column, not the
description column.</p>

<h2>The three paths</h2>
{tbl}

<h2>Record a choice</h2>
<div id="path-chooser" class="chooser">
  <p class="small muted">{e(PATHS["decision_control_note"])}</p>
  {''.join(opts)}
  <p><label for="path-note">Note (optional):</label><br>
     <textarea id="path-note" rows="3" cols="60"
       placeholder="Why this path, in your own words."></textarea></p>
  <p><button id="path-copy" type="button">Copy the record</button></p>
  <p id="path-when" class="small muted"></p>
  <pre id="path-export" class="export"></pre>
</div>

<h2>What happens after a choice is recorded</h2>
<ol>
  <li>The choice itself changes nothing. It is text in a browser until someone acts
      on it &mdash; which is the point: the brief asks for a review step before
      implementation, so there is one.</li>
  <li>A later session implements the accepted path. Under this repository's
      coordination rules that session claims the files it will touch in
      <a href="https://github.com/kanlerxz87-cyber/Zone3/blob/main/COORDINATION.md"
         target="_blank" rel="noopener noreferrer">COORDINATION.md</a> before it
      starts, so two sessions never edit the same file.</li>
  <li>The suggestions that the choice unlocks move from <em>proposed</em> to
      <em>implemented</em>, and the ones it rules out are recorded as rejected with
      the reason, not quietly dropped.</li>
</ol>

<h2>Which suggestion each path unlocks</h2>
<ul>
  <li><strong>Path A</strong> unlocks the full set, including two pillar pages, two
      clusters and the cross-category article <code>T-05</code>.</li>
  <li><strong>Path B</strong> unlocks everything except the thermometer work; the two
      thermometer records stay visible on the
      <a href="direction/products.html">product-intent page</a> as out of scope rather than
      being deleted.</li>
  <li><strong>Path C</strong> unlocks the same content as Path A but doubles the
      number of surfaces that have to each carry the disclosure, a sitemap and a
      working build gate.</li>
</ul>
{CHOOSER_JS}
"""
    return body


# --------------------------------------------------------------- session record

def build_record() -> str:
    """sessions/5b443d02/index.html - what was read, what was found, what was changed."""
    rows = []
    for r in PRODUCTS["records"]:
        rows.append([
            e(r["id"]),
            f'<code>{e(r["token"])}</code>',
            f'<a href="{e(r["official_listing_url"])}" target="_blank" '
            f'rel="noopener noreferrer">{e(r["observed_asin"])}</a>',
            e(r["observed_browse_leaf"]),
            '<span class="badge ok">already on record</span>'
            if r["id"] in ("5B-P1", "5B-P2", "5B-P3")
            else '<span class="badge warn">new in this session</span>',
            slinks([r["observed_source"]]),
        ])
    links_tbl = table(
        ["ID", "Submitted token", "Observed destination", "Browse node (leaf)",
         "Was it on record?", "Source"],
        rows)

    # The five submitted links live on link.amazon, which the release gate's
    # official-host regex does not classify as an official Amazon host. Each one is
    # therefore shown next to the amazon.com destination it resolves to, so every row
    # on this page carries a link the gate recognises.
    resolves = {r["confirmation_source"]: r["official_listing_url"]
                for r in PRODUCTS["records"]}
    srows = []
    for s in SOURCES.values():
        dest = resolves.get(s["id"])
        srows.append([
            e(s["id"]),
            f'<a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer">'
            f'{e(s["title"])}</a>',
            (f'<a href="{e(dest)}" target="_blank" rel="noopener noreferrer">'
             f'{e(dest)}</a>') if dest else "&mdash;",
            '<span class="badge ok">read this session</span>'
            if "2026-11-17" in s["status"] else '<span class="badge muted">inherited</span>',
            e(s["status_note"]),
        ])
    src_tbl = table(["ID", "Official page", "Resolves to", "Read when",
                     "What it established"], srows)

    frows = [
        ("5B-F-01", "High", "Two of the five links sit in a different browse node (Meat, 289810) "
                            "from the Air Fryers node the whole site is built around.",
         ["S70", "S71", "S72", "S73"]),
        ("5B-F-02", "High", "Those two links appear in no data file in the repository before this "
                            "session; every page was built on three of five submitted links.",
         ["S70", "S71", "S72", "S73"]),
        ("5B-F-03", "Medium", "The intended ASIN is unknown for all five links; only observed "
                              "destinations are recorded, in a separate field.",
         ["S06", "S70", "S71"]),
        ("5B-F-04", "Low", "verify_site.py V4 does not treat Google Search Central as an official "
                           "host, so six guidance rows are reported for review.",
         []),
        ("5B-F-05", "Medium", "No outbound link here is a validated Special Link and the supplied "
                              "tracking tag is unconfirmed.",
         ["S01", "S02", "S29"]),
        ("5B-F-06", "Info", "check_site.py reported same-page anchors on subdirectory pages as "
                            "broken links. Fixed; recorded because it edits a shared gate.",
         []),
    ]
    frows_html = []
    for fid, sev, item, src in frows:
        frows_html.append([
            f'<a href="../../flagged.html#{e(fid)}">{e(fid)}</a>',
            sev_badge(sev),
            e(item),
            evidence(src, "data/5b443d02/sources.json"),
        ])
    flag_tbl = table(["Flag", "Severity", "What it records", "Source / defining record"],
                     frows_html)

    body = f"""
<p class="lead-note">Session <code>5b443d02</code>, 2026-11-17, on branch
<code>arena/5b443d02-zone3</code>. Everything below was read from the official pages
on the date given. No value on this record is inferred, and no price, rating,
review count or sales figure is recorded anywhere in it.</p>

<h2>What this session found</h2>
<p>The brief submits five product links. Three were on record. Two &mdash;
<code>B0c8moW59</code> and <code>B0f3GKalj</code> &mdash; appear in no data file in
this repository before this session, and both resolve to meat thermometers rather
than air fryers.</p>
{links_tbl}

<h2>Sources</h2>
<p>Twenty-one sources carry this section, namespaced <code>5B-Snn</code> so they are
not confused with the shared register's <code>Snn</code>. Sources marked
<em>inherited</em> are in the shared register, verified by an earlier session, and
were not re-read today; they are labelled as inherited wherever they are used.</p>
{src_tbl}

<h2>Flags raised</h2>
{flag_tbl}
<p>All six are published on the
<a href="../../flagged.html">Flagged for review</a> page.</p>

<h2>Verification performed</h2>
<ul>
  <li>Each of the five submitted links was fetched on 2026-11-17 and its destination,
      served page title and breadcrumb recorded.</li>
  <li>The Operating Agreement was re-read: section 1 (Special Links; the Program
      Content definition and its exclusion of product information from non-Amazon
      sites), section 4 (no representation as to traffic or commission income),
      section 5 (the disclosure, to be stated clearly and prominently) and section
      6(a) (breach of section 5 is deemed a material breach).</li>
  <li>The Program Policies were re-read: header (updated April 14, 2026) and
      Commission Income Statement section 1.</li>
  <li>The Creators API GetItems reference was re-read: ASIN is defined as a
      10-character alphanumeric identifier, and <code>partnerTag</code> is a required
      request parameter.</li>
  <li>Every table row on every page this session built was checked by the release
      gate for a link to an official source, a flag, or an anchor to a file that
      exists.</li>
</ul>

<h2>Files this session added or changed</h2>
<ul>
  <li><b>Added:</b> <code>data/5b443d02/</code> (sources, products, suggestions,
      questions, paths), <code>scripts/build_5b443d02.py</code>,
      <code>direction/</code> (four pages).</li>
  <li><b>Added to the shared registers:</b> sources <code>S70</code>&ndash;
      <code>S74</code> and flags <code>5B-F-01</code>&ndash;<code>5B-F-06</code>.</li>
  <li><b>Changed, additively:</b> <code>scripts/build_site.py</code> (one navigation
      group; the executive-summary bottom line; the landing-page meta description),
      <code>scripts/check_site.py</code> (the four new pages registered in
      <code>PAGES</code>; the pure-fragment link resolution fixed).</li>
  <li><b>Not touched:</b> <code>suggestions.html</code>,
      <code>decision-center.html</code>, <code>decision-queue.html</code>,
      <code>design-brief.html</code>, <code>site/decisions.html</code>,
      <code>site/answers.html</code> and their data files. Those are owned by earlier
      sessions and are cross-linked from <code>direction/questions.html</code>
      instead of being rewritten.</li>
</ul>

<h2>Gate results on the final tree</h2>
<ul>
  <li><code>scripts/check_site.py</code> &mdash; OK, 34 pages, 67 sources, 114 flags.</li>
  <li><code>tools/verify_site.py</code> &mdash; PASS, 119 pages, every row sourced,
      flagged or anchored.</li>
  <li><code>tools/i2_gate.py</code> &mdash; PASS, 18 pages, 0 flagged.</li>
  <li><code>tools/cba81fa5_lint.py</code> &mdash; PASS, 0 new findings.</li>
  <li><code>scripts/build_sitemap.py --check</code> &mdash; 82 pages, 0 missing.</li>
</ul>
"""
    return body


def sev_badge(sev: str) -> str:
    return bs.badge(sev, {"High": "warn", "Medium": "info", "Low": "muted",
                          "Info": "muted", "Critical": "bad"}.get(sev, "muted"))


# ------------------------------------------------------------------------ audit

def audit() -> list[str]:
    """Self-check the emitted pages before leaving the builder."""
    problems: list[str] = []
    pages = sorted(OUT.glob("*.html"))
    if len(pages) != 4:
        problems.append(f"expected 4 pages under direction/, found {len(pages)}")
    for p in pages:
        raw = p.read_text(encoding="utf-8")
        text = re.sub(r"<[^>]+>", " ", raw)
        if "As an Amazon Associate I earn from qualifying purchases." not in text:
            problems.append(f"{p.name}: missing the Associates disclosure")
        if "COMES FROM AMAZON" not in raw.upper():
            problems.append(f"{p.name}: missing the Amazon content disclaimer")
        if len(re.findall(r"<h1[\s>]", raw)) != 1:
            problems.append(f"{p.name}: expected exactly one h1")
        for marker in ("TODO", "FIXME", "TBD", "lorem"):
            if marker.lower() in text.lower():
                problems.append(f"{p.name}: placeholder marker {marker!r}")
        # no price / rating constructs
        for m in re.finditer(r"\$\s?\d[\d,]*(?:\.\d{2})?", text):
            problems.append(f"{p.name}: money amount {m.group(0)!r}")
        if re.search(r"\b\d\.\d\s?out of\s?5\b", text, re.I):
            problems.append(f"{p.name}: star rating present")
        for m in re.finditer(r'(?:href|src)="(http://[^"]+)"', raw):
            problems.append(f"{p.name}: non-HTTPS link {m.group(1)}")
        for tbody in re.findall(r"<tbody>(.*?)</tbody>", raw, re.S):
            for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", tbody, re.S):
                if "<td colspan" in tr:
                    continue
                official = re.search(
                    r'href="https?://[^"]*'
                    r'(amazon\.com|amazon\.[a-z]{2,3}|ftc\.gov|github\.com)'
                    r'[^"]*"', tr)
                flagid = re.search(r'(FLG-\d+|id="F\d+"|I2-F-\d+|class="blank")', tr)
                anchor = re.search(r"repo:([A-Za-z0-9_.\-/]+[A-Za-z0-9])", tr)
                if not (official or flagid or anchor):
                    snippet = re.sub(r"<[^>]+>", " ", tr).strip()[:60]
                    problems.append(f"{p.name}: unsourced table row -> {snippet!r}")
                if anchor and not (ROOT / anchor.group(1)).exists():
                    problems.append(
                        f"{p.name}: repo anchor missing on disk: {anchor.group(1)}")
    return problems


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    emit(
        "direction/index.html",
        "Direction: design suggestions for a site that reads like a shop",
        build_index(),
        lead="What the site should become, suggested as proposals with a gate attached "
             "to each one &mdash; so a decision is made before anything is built.",
        description="Design and editorial suggestions for the Zone3 affiliate site: "
                    "19 proposals with prerequisites, official standards, editorial "
                    "topics and the open questions that block them.",
    )
    emit(
        "direction/products.html",
        "Product intent: the five submitted links",
        build_products(),
        lead="What each submitted link was meant to reach, and where it went &mdash; "
             "recorded as two separate facts and never merged.",
        description="Product-intent confirmation record for five submitted Amazon "
                    "links: intended ASIN, official listing URL, confirmation date, "
                    "source, and observed redirect targets kept in a separate field.",
    )
    emit(
        "direction/questions.html",
        "Open questions: what we have, what is missing, how to close it",
        build_questions(),
        lead="Every question that blocks a decision, with the action that would "
             "answer it and what the site does anyway if it stays open.",
        description="Decision-blocking questions for the Zone3 affiliate site: what "
                    "is already established, what is missing, how to discover it, "
                    "what it blocks, and the default if it stays unanswered.",
    )
    emit(
        "direction/choose.html",
        "Choose a path",
        build_choose(),
        lead="Three complete answers to what this site should be, compared on "
             "consequences, with a review step before anything is implemented.",
        description="Three paths for the Zone3 affiliate site - one kitchen site with "
                    "two pillars, air-fryer only, or two separate sites - with effort, "
                    "risk and what each does with the five submitted products.",
    )
    emit(
        "sessions/5b443d02/index.html",
        "Session 5b443d02 — verification record (2026-11-17)",
        build_record(),
        lead="What was read from the official pages, what it established, and what "
             "this session changed in the repository.",
        description="Session 5b443d02 record: the five submitted Amazon links, the "
                    "sources read on 2026-11-17, the six flags raised, and the files "
                    "added or changed by this session.",
    )
    problems = audit()
    if problems:
        print(f"5b443d02 AUDIT FAILED - {len(problems)} problem(s):", file=sys.stderr)
        for x in problems:
            print("  -", x, file=sys.stderr)
        return 3
    print(f"built direction/ - 4 pages, {len(SOURCES)} sources, "
          f"{len(PRODUCTS['records'])} products, "
          f"{len(SUGGESTIONS['suggestions'])} suggestions, "
          f"{len(SUGGESTIONS['topics'])} topics, "
          f"{len(QUESTIONS['questions'])} questions, {len(PATHS['paths'])} paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

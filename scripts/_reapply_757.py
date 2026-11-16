#!/usr/bin/env python3
"""Re-apply session 757efebc's page builders onto scripts/build_site.py.

Session 145b8df7 restructured the generator (NAV -> NAV_PRIMARY + NAV_MORE, a rebuilt landing
page, a new articles layer), so the original insertions no longer apply cleanly. This script
takes the current file and re-inserts this session's additions against the current anchors.

Every insertion is additive: no existing line is removed or rewritten.
"""
from __future__ import annotations
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
T = ROOT / "scripts" / "build_site.py"

HELPERS = '''
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
        '<a href="decision-queue.html">Review console</a>.</p></div>'
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

    blocks = [f'{b["label"].upper()}\\n\\n{b["text"]}' for b in d["prompt"]]
    prompt_text = "\\n" + ("\\n\\n" + ("-" * 64) + "\\n\\n").join(blocks) + "\\n"
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
             '<p class="small">Where the money is made, lawfully.</p>') + table(
        ["ID", "Element", "Specification", "Why", "Basis"], rows)

    rows = [[e(r["id"]), e(r["tell"]), e(r["fix"]), basis(r)] for r in d["anti_slop"]]
    body += ("<h2>Anti-slop checklist</h2>"
             '<p class="small">Ten tells, and what to do instead. Run a page against this '
             "before it ships.</p>") + table(
        ["ID", "The tell", "What to do instead", "Basis"], rows)

    body += "<h2>How to use this brief</h2><ol class=\\"findings\\">" + "".join(
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
        '<a href="design-brief.html">Design brief</a>.</p></div>'
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
             '<p class="small">Concrete actions, each one closing a named gap.</p>') + table(
        ["ID", "Action", "What it discovers", "Effort", "Source"], rows)

    body += "<h2>How to run the review</h2><ol class=\\"findings\\">" + "".join(
        f"<li>{e(step)}</li>" for step in q["workflow"]) + "</ol>"

    page("decision-queue.html", "Review console", body,
         lead="Every proposal, the recommendation against it, the question that blocks it, and "
              "the information this project has and does not have. Review and decide before "
              "anything is built.")


'''


def sub(src: str, anchor: str, addition: str, label: str) -> str:
    n = src.count(anchor)
    if n != 1:
        raise SystemExit(f"anchor {label!r} occurs {n} times, expected 1")
    return src.replace(anchor, anchor + addition)


def main() -> int:
    s = T.read_text(encoding="utf-8")
    orig = s

    s = sub(s, 'ARTICLES = load("articles.json")\n',
            'DESIGN = load("design-brief.json")\nQUEUE = load("decision-queue.json")\n',
            "data loads")

    a = ('def flag_links(ids) -> str:\n'
         '    return " ".join(f\'<a class="flagid" href="flagged.html#{e(i)}">{e(i)}</a>\' for i in ids) or "&mdash;"\n')
    s = sub(s, a, HELPERS, "flag_links")

    a = "# ------------------------------------------------------------- Campaigns\n"
    s = s.replace(a, a, 1)
    # helpers block already ends with the two functions; ensure they sit before Campaigns
    if "def build_campaigns()" not in s:
        raise SystemExit("build_campaigns not found")

    # NAV_MORE: Governance group, after the suggestions entry. Note this literal uses a raw
    # "&" while the site-map group below uses the HTML entity "&amp;" - they are different
    # strings, and matching the wrong one silently edits the wrong list.
    a = '        ("suggestions.html", "Suggestions & decisions"),\n'
    s = sub(s, a,
            "        # Added by session 757efebc (2026-11-16): the redesign brief with the\n"
            "        # copy-paste prompt, and the console where every proposal is reviewed first.\n"
            '        ("design-brief.html", "Design brief"),\n'
            '        ("decision-queue.html", "Review console"),\n',
            "nav_more governance")

    # SITEMAP_GROUPS: Governance group, matched on the entity-escaped literal.
    a = '        ("suggestions.html", "Suggestions &amp; decisions"),\n'
    s = sub(s, a,
            "        # Added by session 757efebc (2026-11-16).\n"
            '        ("design-brief.html", "Design brief and prompt pack"),\n'
            '        ("decision-queue.html", "Review console: proposals and open questions"),\n',
            "sitemap governance")

    # main(): run the two builders.
    a = "    import build_5a56c084\n"
    s = sub(s, a, "    build_design_brief()\n    build_decision_queue()\n", "main")

    # CSS for the copy-paste prompt block.
    a = "\n@media (max-width:640px){main{padding:18px 14px 36px}.topbar{padding:10px 12px}}\n"
    s = sub(s, a,
            "\n"  # Added by session 757efebc (2026-11-16): the copy-paste prompt block.
            ".promptbox{background:#101c2e;color:#e7eef8;border-radius:12px;padding:20px 22px;"
            "overflow-x:auto;font:13px/1.65 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;"
            "white-space:pre-wrap;word-break:break-word;margin:0 0 18px}\n"
            ".promptbox b{color:#ffd9c2}\n", "css")

    if s == orig:
        print("no change", file=sys.stderr)
        return 1
    T.write_text(s, encoding="utf-8")
    print("re-applied 757efebc additions onto the current generator")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

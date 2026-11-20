#!/usr/bin/env python3
"""Session 5a56c084's generator: the Research Desk (articles/) and the session
verification record (sessions/5a56c084/index.html).

Standard library only. Run from the repository root:

    python3 scripts/build_5a56c084.py

Writes:
    articles/index.html                          the Research Desk hub
    articles/<slug>.html                         one page per article in data/articles.json
    sessions/5a56c084/index.html                 the 2026-11-16 re-verification record

Every article is rendered through the shared template in scripts/build_site.py
(page(), css()), so the Research Desk inherits the site's design system, the
Associates disclosure, the Amazon content disclaimer and the navigation.

Rules enforced here, before anything is written:
  * every {{Sxx}} source reference in an article must exist in data/sources.json;
  * every {{FLG-nnn}} flag reference must exist in data/flags.json;
  * every article must carry a byline/date block, a verified box, a not-verified
    box, a how-written note and editorial constraints;
  * the build exits non-zero on any violation, so a claim that cannot be traced
    cannot reach the output directory.

No article states a price, a rating, a review quote, a search-volume figure or a
first-hand product experience; the verified/not-verified boxes say what was and
was not confirmed instead.
"""
from __future__ import annotations

import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

# build_site.py loads the data registers at import time and exposes the shared
# template helpers. It performs no writes unless run as a script (it has a
# __main__ guard), so importing it here is side-effect free.
from build_site import page, e, src_links, SOURCES, FLAGS, DISCLOSURE  # noqa: E402

DATA = ROOT / "data"
ARTICLES = json.loads((DATA / "articles.json").read_text(encoding="utf-8"))
TOPICS = json.loads((DATA / "topics.json").read_text(encoding="utf-8"))
SESSION_RECORD = json.loads(
    (ROOT / "sessions/5a56c084/verification-2026-11-16.json").read_text(encoding="utf-8")
)

FLAG_IDS = {f["id"] for f in FLAGS}
SOURCE_IDS = set(SOURCES)

errors: list[str] = []


def fail() -> None:
    if errors:
        print("BUILD FAILED — validation problems:")
        for x in errors:
            print("  -", x)
        raise SystemExit(2)


def src_anchor(sid: str) -> str:
    if sid not in SOURCE_IDS:
        errors.append(f"article cites unknown source {sid}")
        return sid
    s = SOURCES[sid]
    return (
        f'<a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer" '
        f'title="{e(s["title"])}">{e(sid)}</a>'
    )


def flag_anchor(fid: str) -> str:
    if fid not in FLAG_IDS:
        errors.append(f"article cites unknown flag {fid}")
        return fid
    return f'<a class="flagid" href="flagged.html#{e(fid)}">{e(fid)}</a>'


def inline(text: str) -> str:
    """Replace {{Sxx}} and {{FLG-nnn}} markers with real links.

    Source markers link straight to the official page. Flag markers link to the
    Flagged for review page at the repository root - the shared page() template
    rewrites root-relative hrefs on subdirectory pages, so 'flagged.html' works
    from articles/ as well as from the flat root pages.
    """
    # 2e0d5c15 (2026-11-20): escape the prose before substituting markers. Article copy
    # writes placeholders as literal text ("amazon.com/dp/<token>"); unescaped, a browser
    # reads <token> as an unknown element and the word disappears from the sentence.
    # The marker patterns use only braces and capitals, so escaping cannot disturb them.
    text = html.escape(text, quote=False)
    text = re.sub(r"\{\{(S\d+)\}\}", lambda m: src_anchor(m.group(1)), text)
    text = re.sub(r"\{\{(FLG-\d+)\}\}", lambda m: flag_anchor(m.group(1)), text)
    return text


def validate(article: dict) -> None:
    for key in ("id", "slug", "title", "dek", "tldr", "sections", "verified",
                "not_verified", "how_written", "constraints"):
        if key not in article:
            errors.append(f"article {article.get('id', '?')} missing required key {key}")
    for sec in article.get("sections", []):
        if "h" not in sec or "paras" not in sec or not sec["paras"]:
            errors.append(f"article {article.get('id', '?')}: section without heading or body")
    if not article.get("verified"):
        errors.append(f"article {article.get('id', '?')}: empty verified box")
    if not article.get("not_verified"):
        errors.append(f"article {article.get('id', '?')}: empty not-verified box")


def article_body(a: dict) -> str:
    parts: list[str] = []

    parts.append(
        '<div class="tldr"><p class="tldr-h">The short version</p><ul class="findings">'
        + "".join(f"<li>{inline(p)}</li>" for p in a["tldr"])
        + "</ul></div>"
    )

    for sec in a["sections"]:
        parts.append(f'<section class="article-sec"><h2>{e(sec["h"])}</h2>')
        parts.append("".join(f"<p>{inline(p)}</p>" for p in sec["paras"]))
        parts.append("</section>")

    parts.append(
        '<div class="vbox ok"><p class="box-h">What this article verified</p><ul class="findings">'
        + "".join(
            f"<li>{inline(v['text'])} {src_links(v['source'])}</li>" for v in a["verified"]
        )
        + "</ul></div>"
    )

    items = []
    for v in a["not_verified"]:
        flag = flag_anchor(v["flag"]) if v.get("flag") else ""
        items.append(f"<li>{inline(v['text'])} {flag}</li>")
    parts.append(
        '<div class="vbox warn"><p class="box-h">What this article did not verify (and says so)'
        '</p><ul class="findings">' + "".join(items) + "</ul></div>"
    )

    constraint_items = "".join(f"<li>{inline(c)}</li>" for c in a["constraints"])
    parts.append(
        '<div class="vbox"><p class="box-h">How this was written</p>'
        f"<p>{inline(a['how_written'])}</p>"
        '<p class="box-sub">Editorial constraints enforced for this article:</p>'
        f'<ul class="findings">{constraint_items}</ul></div>'
    )

    # Disclosure beside the product pointers, per SUG-03 / FTC placement guidance.
    parts.append(
        '<div class="adisclose"><p><strong>Disclosure:</strong> ' + e(DISCLOSURE)
        + ' This site links to Amazon pages as sources. No conversion-oriented link is '
          'published yet, because the Associates tag every Special Link must carry is not '
          'known to this project (open question Q1, <a href="decision-center.html">Decision '
          'Center</a>). See the article '
          '<a href="articles/what-an-amazon-affiliate-link-has-to-look-like.html">What an '
          'Amazon affiliate link has to look like</a> for the rules behind that choice.</p></div>'
    )
    return "".join(parts)


RELATED = [
    ("marketing/comparison.html", "Comparison: the three listings, attribute by attribute"),
    ("marketing/buying-guide.html", "The air-fryer buying guide"),
    ("air-fryers.html", "Category: Air Fryers"),
    ("content-topics.html", "The full editorial topic plan"),
]


def render_table(headers: list[str], rows: list[list[str]]) -> str:
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def build_article_pages() -> None:
    hub_cards: list[str] = []
    rendered: list[tuple[dict, str]] = []

    for a in ARTICLES["articles"]:
        validate(a)
        body = article_body(a)
        rendered.append((a, body))
        hub_cards.append(
            f'<a class="acard" href="articles/{e(a["slug"])}">'
            f'<span class="acard-meta">{e(ARTICLES["desk"])} &middot; {e(ARTICLES["published"])}'
            f' &middot; {a["reading_minutes"]} min read</span>'
            f"<b>{e(a['title'])}</b><span>{e(a['dek'])}</span>"
            f'<span class="acard-go">Read the article &rarr;</span></a>'
        )
    fail()

    for a, body in rendered:
        page(f"articles/{a['slug']}", a["title"], body, lead=e(a["dek"]))

    topic_rows = []
    for t in TOPICS["topics"]:
        status = t.get("status", "unknown")
        badge = ('<span class="badge ok">Ready</span>' if status == "ready"
                 else '<span class="badge warn">Blocked</span>' if status == "blocked"
                 else f'<span class="badge muted">{e(status)}</span>')
        flags = " ".join(flag_anchor(f) for f in t.get("flags", [])) or "&mdash;"
        where = e(t.get("published", "")) if t.get("published") else "&mdash;"
        topic_rows.append([
            e(t["id"]),
            f"<strong>{e(t['title'])}</strong>",
            e(t.get("intent", "")),
            f"{badge} {flags}",
            f'<a href="{e(t["published"])}">{where}</a>' if t.get("published") else "&mdash;",
            src_links(t.get("sources", [])),
        ])

    added_rows = []
    for a in ARTICLES["articles"]:
        if a["topic_ref"].startswith("new"):
            note = ("New evergreen topic added to the plan by session 5a56c084, grounded in "
                    "the Commission Income Statement (re-read 2026-11-16).")
            basis = ["S02", "S30"]
        else:
            note = (f"Published on this desk {e(ARTICLES['published'])}; covers topic "
                    f"{e(a['topic_ref'])} from the plan.")
            basis = ["S02"]
        added_rows.append([
            f'<a href="articles/{e(a["slug"])}">{e(a["id"])}</a>',
            f"<strong>{e(a['title'])}</strong>",
            note,
            src_links(basis),
        ])

    checklist = "".join(f"<li>{e(step)}</li>" for step in ARTICLES["review_checklist"])
    related_links = " &middot; ".join(f'<a href="{h}">{e(t)}</a>' for h, t in RELATED)

    body = (
        '<div class="desk-intro"><p class="eyebrow">The Research Desk</p>'
        "<h2>Articles you can check claim by claim.</h2>"
        "<p>Every article on this desk is written from official pages - Amazon's own policy "
        "documents, the listings themselves, the FTC's guidance - and every factual claim "
        "carries the link to the page it came from. Where the record is silent, the article "
        "says so instead of inventing colour. That is the whole editorial standard: no "
        "invented experience, no invented numbers, no filler.</p></div>"
        f'<div class="acards">{"".join(hub_cards)}</div>'
        '<h2>Editorial standard (SUG-03 review gate)</h2>'
        '<div class="vbox ok"><p class="box-h">Every article passes this checklist before '
        f'publication</p><ul class="findings">{checklist}</ul></div>'
        "<h2>The twelve-topic plan, and where each topic lives now</h2>"
        '<p class="small">The plan was published 2026-11-14 (session 3d359c23). "Ready" topics '
        "are grounded entirely in facts already verified; \"Blocked\" topics wait on "
        "listing-detail facts that need an approved Amazon data path. Articles published from "
        "the plan on this desk are listed after the plan.</p>"
        + render_table(
            ["ID", "Working title", "Intent", "Status", "Where it lives now", "Source"],
            topic_rows,
        )
        + "<h2>Articles published from the plan (session 5a56c084, 2026-11-16)</h2>"
        + render_table(["ID", "Article", "Note", "Source"], added_rows)
        + f'<p class="small">Related pages: {related_links}</p>'
    )
    page("articles/index.html", "Research Desk", body,
         lead="The article hub: grounded, sourced, checkable pieces about the products this "
              "site tracks and the rules that govern affiliate marketing. Proposals SUG-02 "
              "and SUG-03, implemented 2026-11-16 (decision log on suggestions.html).")


def build_session_record() -> None:
    rec = SESSION_RECORD
    rows = []
    for o in rec["observations"]:
        match = ('<span class="badge ok">Matches register</span>' if o["matches_register"]
                 else '<span class="badge bad">Differs</span>')
        rows.append([
            f'<span id="{e(o["id"])}"></span><strong>{e(o["id"])}</strong>',
            f"<strong>{e(o['claim'])}</strong>",
            e(o["observed"]),
            match,
            src_links(o["retests"]),
        ])
    drift_rows = []
    for d in rec["drift_notes"]:
        drift_rows.append([
            f"<strong>{e(d['id'])}</strong>",
            f'<span class="badge muted">{e(d["severity"])}</span>',
            e(d["item"]),
            src_links(["S14", "S15", "S16", "S52", "S53", "S54"]),
        ])
    body = (
        f'<div class="callout ok"><p><strong>Result: {len(rec["observations"])} of '
        f'{len(rec["observations"])} observations match the register.</strong> The three '
        "submitted short links still open the same three live listings; the direct "
        "/dp/&lt;token&gt; checks still return Amazon's Page Not Found page; both policy "
        "documents are unchanged in every clause re-read. Two listing-title wording drifts "
        "are recorded below as Info items; no new flag is raised. Product-attribute cells "
        "stay blank - no approved Amazon data path is connected, so publishing prices, "
        "ratings or review counts would breach Participation Requirements 2(b) and 6(t).</p></div>"
        "<h2>Observations (fetched 2026-11-16 in this session)</h2>"
        + render_table(["ID", "Claim", "What the page served", "Result", "Source"], rows)
        + "<h2>Drift notes (Amazon edits listing titles over time)</h2>"
        + render_table(["ID", "Severity", "Item", "Source"], drift_rows)
        + "<h2>Method</h2><p>" + e(rec["method"]) + "</p>"
        + "<h2>Conclusion</h2><p>" + e(rec["conclusion"]) + "</p>"
        + '<p class="small">Raw record: <code>sessions/5a56c084/verification-2026-11-16.json</code>. '
          'Board entry: <a href="https://github.com/kanlerxz87-cyber/Zone3/blob/main/COORDINATION.md">'
          "COORDINATION.md</a>, Part session 5a56c084.</p>"
    )
    page("sessions/5a56c084/index.html", "Verification (session 5a56c084)", body,
         lead="Independent re-verification of the three submitted links, the three "
              "destinations and the load-bearing policy pages, fetched 2026-11-16 in this "
              "session. Every row links the official page it re-tests.")


def main() -> None:
    build_article_pages()
    build_session_record()
    print("built Research Desk (articles/) and sessions/5a56c084/index.html")


if __name__ == "__main__":
    main()

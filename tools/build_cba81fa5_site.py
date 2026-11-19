#!/usr/bin/env python3
"""Post-build integrator for the reader site (session cba81fa5, 2026-11-16).

Why this exists. The reader site under site/ is emitted by tools/build_i2_site.py (session
59d84c55). Two of those surfaces — the landing page and the buying-guides index — list guides
that this session published, and a plain rebuild of the reader site would silently drop them.
Rather than fork their generator, this script owns exactly two regions and regenerates them
from data/cba81fa5/guides.json, so the guide list is data-driven and a rebuild is repairable:

    python3 tools/build_i2_site.py && python3 tools/build_cba81fa5_site.py && python3 scripts/build_sitemap.py

Regions owned (replaced wholesale, everything else in the file is untouched):
  site/index.html          from "<h2>Buying guides</h2>" up to the "<h2>Side by side</h2>" anchor
  site/guides/index.html   from "<h2>The guide plan</h2>" up to "<h2>The rule every guide follows</h2>"
  site/site-index.json     every guide href in the register, plus the governance pages

Usage:  python3 tools/build_cba81fa5_site.py [--check]
        --check  exits 1 (and prints the diff size) if a rebuild would change anything.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
DATA = ROOT / "data" / "cba81fa5"

# 0C4-T3 (session 0c4c4cb6, 2026-11-17): generated regions must already carry
# rel="sponsored" on outbound product links, exactly as scripts/mark_sponsored.py
# would mark them. If they did not, the post-pass would rewrite this session's
# regions and --check would report them stale for ever. One implementation, imported.
import importlib.util as _ilu

_ms_spec = _ilu.spec_from_file_location("zone3_mark_sponsored", ROOT / "scripts" / "mark_sponsored.py")
_ms = _ilu.module_from_spec(_ms_spec)
_ms_spec.loader.exec_module(_ms)


def sponsored(html: str) -> str:
    return _ms.process(html)[0]

GUIDES = json.loads((DATA / "guides.json").read_text(encoding="utf-8"))
SOURCES = json.loads((DATA / "sources.json").read_text(encoding="utf-8"))
SRC = {s["id"]: s for s in SOURCES["sources"]}
for s in json.loads((ROOT / "data" / "i2" / "sources.json").read_text(encoding="utf-8")).get("sources", []):
    SRC.setdefault(s["id"], s)



def _rel_s(s) -> str:
    return _rel(s["url"])


def _rel_d(d) -> str:
    return _rel(SRC[d["source"]]["url"])


def _rel(url: str) -> str:
    """session aebf0747: Amazon product or short links are marked sponsored (Google qualify-outbound-links).
    Mirrors sessions/aebf0747/publish_pass.py: the Associates policy page is not a product link."""
    host = re.sub(r"^https?://", "", str(url)).split("/")[0].split(":")[0].lower()
    if "amazon." in host or host.startswith("link.amazon") or host.startswith("amzn.to") or host == "a.co":
        if host != "affiliate-program.amazon.com":
            return "noopener noreferrer sponsored"
    return "noopener noreferrer"


# ---------------------------------------------------------------------------
# Sponsored rel (session ded63349, 2026-11-17; proposal D-19). The regions this
# integrator writes contain product links (the fd-card listings); they are marked
# here so a cba rebuild equals the post-pass tree that tools/apply_sponsored.py
# --check and tools/i2_gate.py G11 expect. The pattern below is copied verbatim
# from tools/apply_sponsored.py, which stays the canonical enforcer.
MARK_PRODUCT_HREF = re.compile(
    r'https?://[^\"\']*link\.amazon/[^\"\']*'
    r'|https?://[^\"\']*amazon\.[a-z]{2,3}(?:/[^\"\']*)?/(?:dp/[A-Z0-9]{10}|gp/product/[A-Z0-9]{10})[^\"\']*', re.I)
MARK_ANCHOR_RE = re.compile(r'<a\b[^>]*>', re.I)


def _tag_pass(html: str) -> str:
    """4B0-T2: the release chain also tags product links; mirror it so --check is exact."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("attach_tag_cba", ROOT / "tools" / "attach_associates_tag.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.apply_to_text(html)


def mark_sponsored(html: str) -> str:
    def fix(m):
        tag = m.group(0)
        href = re.search(r'href="([^"]*)"', tag)
        if not href or not MARK_PRODUCT_HREF.search(href.group(1)):
            return tag
        rel = re.search(r'rel="([^"]*)"', tag)
        if rel:
            if "sponsored" in rel.group(1).split():
                return tag
            tokens = [t for t in ("sponsored",) if t not in rel.group(1).split()]
            return tag[:rel.start(1)] + " ".join(tokens + rel.group(1).split()) + tag[rel.end(1):]
        return tag[:-1].rstrip() + ' rel="sponsored noopener noreferrer">'
    return MARK_ANCHOR_RE.sub(fix, html)


def is_short_link(url: str) -> bool:
    """The three submitted link.amazon tokens: evidence to quote, never to click.

    Session f65d393b (2026-11-16): i2_gate G7 (and FLG-003, and Participation
    Requirements 6(w)/CIS 2(e)) — a submitted short link is rendered as text on
    this site; the official /dp/ destination beside it stays clickable.
    """
    return url.startswith("https://link.amazon/")


def src_tag(sid: str) -> str:
    s = SRC.get(sid)
    if not s:
        return f'<span class="mono">{sid}</span>'
    if is_short_link(s["url"]):
        return (f'<span class="src mono" title="{s.get("title", s["url"])} — shown as text, '
                f'not as a link (i2_gate G7; FLG-003)">\u2192 {sid}</span>')
    return (f'<a class="src" href="{s["url"]}" target="_blank" rel="{_rel_s(s)}" '
            f'title="{s.get("title", s["url"])}">{sid}</a>')


def src_row(ids) -> str:
    return " ".join(src_tag(i) for i in ids)


def landing_block() -> str:
    live = [g for g in GUIDES["guides"] if g["status"] == "live"]
    cards = "\n".join(
        f'  <a class="card" href="{g["href"]}"><b>{g["title"].split(":")[0] if len(g["title"]) > 46 else g["title"]}</b>'
        f'<span>{g["blurb"]}</span></a>'
        for g in live
    )
    snap = GUIDES["category_snapshot"]
    return (
        f'<h2>{GUIDES["landing_heading"]}</h2>\n'
        f'<p>{GUIDES["landing_intro"]}</p>\n'
        f'<div class="cards">\n{cards}\n'
        f'  <a class="card" href="guides/index.html"><b>All guides</b><span>The plan, what is live, and what stays unpublished and why.</span></a>\n'
        f'</div>\n\n'
        f'<h2>{snap["heading"]}</h2>\n'
        f'<p>{snap["body"]}\n{src_row(snap["sources"])}</p>\n\n'
    )


def note_and_rules(n_live: int, n_held: int) -> str:
    rules = "\n".join(f"  <li>{r}</li>" for r in GUIDES["rules"])
    return (
        f'<div class="note">\n  <h3>Why {n_live} {word(n_live)} live and {n_held} do not</h3>\n'
        '  <p>A guide goes live once every sentence in it traces to a listing or an official page, the house lint '
        'passes, and each source link has been re-read the same day. The {held} rows are held because the question '
        'needs either a number the listings do not state or a test nobody has run; a row marked &ldquo;will not '
        'publish&rdquo; is a topic this site is not permitted to write, and it stays listed here rather than being '
        'quietly dropped. Every page carries its reviewer note: an agent research desk, no human editor yet '
        '(question Q-5 on the <a href="../answers.html">open-questions register</a>, decision D-10 on the '
        '<a href="../decisions.html">board</a>).</p>\n</div>\n'
        '<h2>The rule every guide follows</h2>\n'
        f'<p class="small">{GUIDES["rules_intro"]}</p>\n'
        f'<ul>\n{rules}\n</ul>\n\n'
    )


def word(n: int) -> str:
    return "guide is" if n == 1 else "guides are"


def guides_index_block() -> str:
    gs = GUIDES["guides"]
    n_live = sum(1 for g in gs if g["status"] == "live")
    n_held = len(gs) - n_live
    rows = []
    for g in gs:
        if g["status"] == "live":
            rows.append(
                f'<tr><td class="lead-cell"><a href="{g["href"].split("/")[-1]}">{g["title"]}</a></td>'
                f'<td><span class="badge b-ok">Live</span> <span class="small">{g["published"]}</span></td>'
                f'<td>{src_row(g["sources"])}</td></tr>'
            )
        else:
            label = "Held" if g["status"] == "held" else "Will not publish"
            rows.append(
                f'<tr><td class="lead-cell">{g["title"]}</td>'
                f'<td><span class="badge b-mute">{label}</span></td>'
                f'<td><span class="blank"><span class="blank-dot"></span>{label}</span>'
                f'<span class="blank-why">{g["reason"]}</span></td></tr>'
            )
    tail = note_and_rules(n_live, n_held).format(held="Held" if n_held else "no")
    note = (f'<a id="cba81fa5-guide-plan" aria-hidden="true"></a>'
            f'<div class="note warn">\n  <p>{GUIDES["duplication_note"]}</p>\n</div>\n'
            if GUIDES.get("duplication_note") else "")
    return (
        note +
        '<div class="tablewrap"><table>\n<caption>The guide plan</caption>\n'
        '<div class="tablewrap"><table><caption>Every guide, published or not, with the register it was read from</caption>'
        '<thead><tr><th>Question this guide answers</th><th>Status</th><th>Provenance</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div>\n' + tail
    )


FRONT_DOOR_NOTE = "cba81fa5 front door — generated region, do not hand-edit"
FD_START = '<a id="cba81fa5-front-door" aria-hidden="true"></a>'
FD_END = '<a id="cba81fa5-front-door-end" aria-hidden="true"></a>'


def products_for_band():
    data = json.loads((ROOT / "data" / "products.json").read_text(encoding="utf-8"))
    out = []
    for prod in data["products"]:
        obs = prod.get("redirect_observed") or {}
        out.append({
            "label": prod.get("label", ""),
            "asin": obs.get("page_id") or "",
            "title": (obs.get("page_title") or "").replace("Amazon.com: ", "").split(" : Home")[0],
            "url": f'https://www.amazon.com/dp/{obs.get("page_id")}' if obs.get("page_id") else "",
        })
    return out


def dashboard_links() -> list[tuple[str, str]]:
    """Every flat dashboard surface, from the flat generator's own nav lists.

    Session ded63349 (2026-11-17): the brief asks that the publication front page keep
    'every dashboard surface reachable from the footer and a single navigation group'.
    The list is imported from scripts/build_site.py's NAV_PRIMARY/NAV_MORE (the canonical
    register of those surfaces) instead of being copied, so the two stay in sync. If the
    import fails, the band still builds with the core surfaces listed by hand.
    """
    try:
        import sys as _sys
        scripts_dir = str(ROOT / "scripts")
        if scripts_dir not in _sys.path:
            _sys.path.insert(0, scripts_dir)
        import build_site as flat  # module-level code only reads data files
        links: list[tuple[str, str]] = []
        for href, label in flat.NAV_PRIMARY:
            if href not in ("index.html",):
                links.append((href, label))
        for _group, items in flat.NAV_MORE:
            links.extend(items)
        if not any(h == "flagged.html" for h, _ in links):
            links.append(("flagged.html", "Flagged for review"))
        return links
    except Exception as exc:  # pragma: no cover - fallback keeps the band renderable
        print(f"build_cba81fa5_site: dashboard link import failed ({exc}); using fallback list")
        return [
            ("marketing/index.html", "Marketing hub"),
            ("products.html", "Products"),
            ("pricing.html", "Pricing & commission"),
            ("executive-summary.html", "Executive summary"),
            ("sources.html", "Sources"),
            ("flagged.html", "Flagged for review"),
            ("dashboard/index.html", "Full audit (16 pages)"),
        ]


def frontdoor_block() -> str:
    fd = GUIDES["front_door"]
    cards = "\n".join(
        f'      <a class="fd-card" href="{g["href"]}"><b>{g["title"]}</b><span>{g["line"]}</span></a>'
        for g in fd["guides"]
    )
    prods = "\n".join(
        f'      <a class="fd-card" href="{SRC[d["source"]]["url"]}" target="_blank" rel="{_rel_d(d)}">'
        f'<b>{html_escape(d["short"])}</b><span>{d["line"]}</span>'
        f'<span class="fd-asin">{d["asin"]} &middot; listing text read 2026-11-16</span></a>'
        for d in GUIDES["products_band"]
    )
    ctas = "\n".join(
        f'    <a class="fd-btn fd-btn-{c["kind"]}" href="{c["href"]}">{c["label"]}</a>' for c in fd["cta"]
    )
    return (
        f'{FD_START}<!-- {FRONT_DOOR_NOTE} -->\n'
        '<section class="fdoor">\n'
        f'  <p class="fd-eyebrow">{fd["eyebrow"]}</p>\n'
        f'  {{H1}}\n'
        f'  <p class="fd-lede">{fd["lede"]}</p>\n'
        '  <div class="fd-cta">\n'
        f'{ctas}\n'
        '  </div>\n'
        f'  <h2 class="fd-h2">{fd["guides_heading"]}</h2>\n'
        '  <div class="fd-cards">\n'
        f'{cards}\n'
        '  </div>\n'
        f'  <p class="fd-fine">{fd["guides_more"]}</p>\n'
        '  <h2 class="fd-h2">The three listings, as served</h2>\n'
        '  <div class="fd-cards">\n'
        f'{prods}\n'
        '  </div>\n'
        f'  <p class="fd-fine">{fd["fine"]} '
        f'<a href="{SRC["CBA-S09"]["url"]}" target="_blank" rel="noopener noreferrer" '
        f'title="{SRC["CBA-S09"]["title"]}">CBA-S09</a></p>\n'
        f'  <p class="fd-fine">How this site counts visits and clicks: '
        f'<a href="site/measure.html">How we measure</a> &middot; '
        f'<a href="site/intent-record.html">Product-intent record</a> &middot; '
        f'<a href="feed.xml">RSS feed</a></p>\n'
        '</section>\n\n'
        '<p class="fd-ops" style="font-size:12px;letter-spacing:.14em;text-transform:uppercase;'
        'font-weight:700;color:#767f8d;margin:28px 0 6px">Operations &middot; the audit behind the front door</p>\n'
        '<nav class="fd-ops-nav" aria-label="Dashboard surfaces" style="display:flex;flex-wrap:wrap;gap:6px 14px;margin:0 0 14px">\n'
        + "".join(f'<a href="{h}">{html_escape(lab)}</a>' for h, lab in dashboard_links())
        + '\n</nav>\n'
        f'{FD_END}'
    )


def render_frontdoor(raw: str) -> str:
    """Band text with the headline tag chosen for the page it is going into.

    The root page already carries an <h1> from scripts/build_site.py ("Dashboard"). Gate V3 and the
    lint both require exactly one h1 per page, so the band demotes its own headline to a styled
    paragraph in that case instead of deleting the heading that is already there. Nothing already
    on the page is removed by this function - the band is inserted, never substituted.
    """
    band = frontdoor_block()
    other = re.sub(re.escape(FD_START) + r".*?" + re.escape(FD_END), "", raw, flags=re.S)
    tag = "h1" if "<h1" not in other else "p"
    return band.replace("{H1}", f'<{tag} class="fd-h1">{GUIDES["front_door"]["h1"]}</{tag}>')


NAV_OPEN = '<nav aria-label="Main">'
NAV_MARK = ">Open questions</a>"
NAV_LINKS = [("answers.html", "Open questions"), ("style-guide.html", "Our rules")]


def ensure_reader_nav() -> list:
    """Keep the two governance pages in the reader nav of every page under site/.

    This session's lint and the guide register require those pages to be reachable, and the reader
    nav is regenerated by tools/build_i2_site.py from ITS OWN page list. Re-applying the two links
    after each rebuild is what keeps the reader set consistent (finding CBA-F-05: an injected region
    disappears when another generator runs). Absorbing these two entries into that generator's page
    list is the permanent fix, and is recorded on the board as a change request rather than done here.
    """
    touched = []
    for f in sorted((SITE).rglob("*.html")):
        raw = f.read_text(encoding="utf-8")
        if NAV_OPEN not in raw or NAV_MARK in raw:
            continue
        m = re.search(r'<a href="(?P<rel>(?:\.\./)*)decisions\.html">Suggestions', raw)
        if not m:
            continue
        rel = m.group("rel")
        links = "".join(f'<a href="{rel}{href}">{label}</a>' for href, label in NAV_LINKS)
        f.write_text(raw[:m.start()] + links + raw[m.start():], encoding="utf-8")
        touched.append(f.relative_to(ROOT).as_posix())
    return touched


def flagged_block() -> str:
    """Findings raised by this session, published on the reader site's Flagged for review page.

    Inserted as a region the integrator owns, between the sentinel and </main>, so a rebuild of
    the reader site (tools/build_i2_site.py) cannot drop the CBA-F rows and cannot duplicate them.
    """
    data = json.loads((DATA / "flags.json").read_text(encoding="utf-8"))
    sev = {"High": "b-bad", "Medium": "b-warn", "Low": "b-mute", "Info": "b-mute"}
    rows = []
    for f in data["flags"]:
        parts = []
        for s in f["sources"]:
            if is_short_link(s["url"]):
                parts.append(
                    f'<span class="src mono" title="{html_escape(s["label"])} — shown as text, '
                    f'not as a link (i2_gate G7; FLG-003)">{html_escape(s["label"])}</span>')
            else:
                parts.append(
                    f'<a class="src" href="{s["url"]}" target="_blank" rel="{_rel_s(s)}" title="{s["label"]}">'
                    f'{html_escape(s["label"])}</a>')
        src = " ".join(parts)
        rows.append(
            f'<tr id="{f["id"]}"><td class="lead-cell"><span class="mono">{f["id"]}</span><br>'
            f'{f["title"]}</td>'
            f'<td><span class="badge {sev.get(f["severity"], "b-mute")}">{f["severity"]}</span></td>'
            f'<td>{f["what"]}</td><td>{f["why_it_matters"]}</td><td>{f["action"]}</td>'
            f'<td>{src}</td></tr>'
        )
    return (
        '<a id="cba81fa5-flagged" aria-hidden="true"></a>\n'
        '<h2>Raised on 2026-11-16 by the second-source desk (session cba81fa5)</h2>\n'
        '<p class="small">Five findings, none of which blocks publishing. Each was checked against the page in '
        'its Source column on 2026-11-16. Two of them are about the machinery that is supposed to catch the '
        'other three, and that is the point of listing them here rather than fixing them quietly.</p>\n'
        '<div class="tablewrap"><table><caption>CBA-F-01&hellip;05 — what was found, why it matters, what to do</caption>'
        '<thead><tr><th>ID &amp; finding</th><th>Severity</th><th>What</th><th>Why it matters</th>'
        '<th>Action</th><th>Source</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div>\n\n'
    )


def html_escape(v: str) -> str:
    return (v.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def patch_text(t: str, start: str, end: str, new: str, back: str | None = None,
               include_end: bool = False) -> str:
    i, j = t.find(start), t.find(end)
    if back and i > 0:
        k = t.rfind(back, 0, i)
        if k > 0:
            i = k
    if i < 0:
        # Session f65d393b (2026-11-16), flag F65-F-05: a plain rebuild of the
        # reader site (tools/build_i2_site.py) drops this session's injected
        # region — including its start anchor — after which the replace raised
        # and the whole "build_i2_site && build_cba81fa5" chain failed from any
        # clean checkout. Self-heal: when the start anchor is gone but the end
        # anchor survives, insert the block immediately before the end anchor.
        # The block re-emits the start anchor, so the next run takes the replace
        # path again and the result stays idempotent.
        if j < 0:
            raise SystemExit(f"FAIL: anchors {start!r} / {end!r} not both found in the file")
        return t[:j] + new + t[j:]
    if j < 0 or j <= i:
        raise SystemExit(f"FAIL: anchors {start!r} / {end!r} not both found in the file")
    j += len(end) if include_end else 0
    return t[:i] + new + t[j:]


def patch(path: pathlib.Path, start: str, end: str, new: str, back: str | None = None) -> str:
    return patch_text(path.read_text(encoding="utf-8"), start, end, new, back)


def build_index_json() -> str:
    idx_path = SITE / "site-index.json"
    data = json.loads(idx_path.read_text(encoding="utf-8")) if idx_path.exists() else {"pages": []}
    want = set(data.get("pages", []))
    for g in GUIDES["guides"]:
        if g["href"]:
            want.add(g["href"])
    for extra in ("answers.html", "style-guide.html"):
        if (SITE / extra).exists():
            want.add(extra)
    data["pages"] = sorted(want)
    data["built"] = GUIDES["built"]
    return json.dumps(data, indent=1) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    targets = [
        (SITE / "index.html", "<h2>Buying guides</h2>", "<h2>Side by side</h2>", sponsored(landing_block()), None),
        (SITE / "guides" / "index.html",
         '<a id="cba81fa5-guide-plan"' if '<a id="cba81fa5-guide-plan"' in (SITE / "guides" / "index.html").read_text(encoding="utf-8") else "<caption>The guide plan</caption>",
         "</main>", sponsored(guides_index_block()), '<div class="tablewrap">'),
    ]
    changed = []
    for path, start, end, new, back in targets:
        # ded63349: compare like with like — the write applies mark_sponsored, so the
        # expected text must be marked before the comparison (otherwise --check always
        # reports a stale region on pages whose regions contain product links).
        want = _tag_pass(mark_sponsored(patch(path, start, end, new, back)))
        have = path.read_text(encoding="utf-8")
        if want != have:
            changed.append(path.relative_to(ROOT).as_posix())
            if not a.check:
                path.write_text(want, encoding="utf-8")

    root_index = ROOT / "index.html"
    # session aebf0747 guard: the publication front page owns index.html; do not re-inject the old band
    if root_index.exists() and "aebf0747-front" not in root_index.read_text(encoding="utf-8"):
        raw = root_index.read_text(encoding="utf-8")
        band = sponsored(render_frontdoor(raw))
        if FD_START in raw:
            # ded63349: mark before compare — the file on disk is post-sponsored, so the
            # expected text must be too (otherwise --check always reports a stale region).
            want = _tag_pass(mark_sponsored(patch_text(raw, FD_START, FD_END, band, include_end=True)))
        elif "<main>" in raw:
            want = raw.replace("<main>", "<main>\n" + band, 1)
        else:
            want = raw
        if 'assets/front-door.css' not in want:
            want = want.replace('<link rel="stylesheet" href="assets/style.css">',
                                '<link rel="stylesheet" href="assets/style.css">\n'
                                '<link rel="stylesheet" href="assets/front-door.css">')
        # ded63349 (2026-11-17): feed discovery on the publication front page.
        # Merge reconciliation 2026-11-17: canonical feed is the union RSS 2.0 feed.xml
        # (session 82372fd1); discovery links are type application/rss+xml, and this
        # injects only when no feed link of either type is present, so it never
        # duplicates the link sessions/aebf0747/publish_pass.py already adds.
        if 'application/atom+xml' not in want and 'application/rss+xml' not in want:
            want = want.replace('</head>',
                                '<link rel="alternate" type="application/rss+xml" '
                                'title="Air Fryer Field Notes \u2014 new guides and field notes" href="feed.xml">\n</head>', 1)
        if "Air Fryer Field Notes" not in want.split("<title>")[1].split("</title>")[0]:
            want = re.sub(r"<title>[^<]*</title>",
                          "<title>Air Fryer Field Notes — three air fryers, checked line by line</title>",
                          want, count=1)
            want = re.sub(r'<meta name="description" content="[^"]*">',
                          '<meta name="description" content="Three air fryers compared on what the Amazon '
                          'listings state, every claim linked to the page it came from, and the full '
                          'verification dashboard behind it.">', want, count=1)
        if want != raw:
            changed.append("index.html")
            if not a.check:
                root_index.write_text(want, encoding="utf-8")

    fl = SITE / "flagged.html"
    if fl.exists():
        raw = fl.read_text(encoding="utf-8")
        start = '<a id="cba81fa5-flagged"' if '<a id="cba81fa5-flagged"' in raw else None
        if start:
            want = _tag_pass(mark_sponsored(patch_text(raw, start, "</main>", flagged_block())))
        elif "</main>" in raw and "Raised on 2026-11-16 by the second-source desk" not in raw:
            want = raw.replace("</main>", sponsored(flagged_block()) + "</main>", 1)
        else:
            want = raw
        if want != raw:
            changed.append("site/flagged.html")
            if not a.check:
                fl.write_text(want, encoding="utf-8")

    nav_touched = [] if a.check else ensure_reader_nav()
    if nav_touched:
        changed.extend(nav_touched)

    idx_path = SITE / "site-index.json"
    want_idx = build_index_json()
    if idx_path.read_text(encoding="utf-8") != want_idx:
        changed.append("site/site-index.json")
        if not a.check:
            idx_path.write_text(want_idx, encoding="utf-8")

    if a.check:
        # a check run must also catch a nav that a rebuild dropped, without writing anything
        for f in sorted(SITE.rglob("*.html")):
            raw = f.read_text(encoding="utf-8")
            if NAV_OPEN in raw and NAV_MARK not in raw \
                    and re.search(r'<a href="(\.\./)*decisions\.html">Suggestions', raw):
                print(f"STALE: reader nav missing the governance links in {f.relative_to(ROOT).as_posix()}",
                      file=sys.stderr)
                return 1

    if a.check and changed:
        print("STALE: rebuild needed -> " + ", ".join(changed), file=sys.stderr)
        return 1
    print(("WOULD REWRITE " if a.check else "WROTE ") + (", ".join(changed) or "nothing (already current)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

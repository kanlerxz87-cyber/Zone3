#!/usr/bin/env python3
"""Build the editorial marketing layer (The Crisp Report) under read/.

Session 145b8df7, 2026-11-16. Implements the accepted direction from suggestions.html:
a polished, human-voiced marketing site whose every factual statement is a dated quote
from an official page. Standard library only.

    python3 scripts/build_read.py            # write the pages
    python3 scripts/build_read.py --check     # rebuild in memory and fail on drift

Design rules enforced here, in code, so they cannot drift:
  * every product attribute traces to a source ID present in data/sources.json;
  * every table row must end up carrying an official-host link (Amazon / FTC / GitHub) —
    the same rule tools/verify_site.py V4 applies, applied at generation time;
  * no price, star rating or review count may be rendered anywhere in the output (Program
    Policies 2(b) and 6(t)); a currency symbol or an "X out of 5 stars" pattern fails the build;
  * every page carries the Associates disclosure sentence (Operating Agreement SS5) and the
    Amazon content disclaimer, and exactly one <h1>;
  * no Amazon-hosted <img> (Program Content images may not be stored or served by us).
"""
from __future__ import annotations

import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "read"
DATA = ROOT / "data"

E = json.loads((DATA / "editorial.json").read_text(encoding="utf-8"))
SRC = {s["id"]: s for s in json.loads((DATA / "sources.json").read_text(encoding="utf-8"))["sources"]}
PRODUCTS = {p["id"]: p for p in E["products"]}
OFFICIAL_HOSTS = ("amazon.com", "amazon.co.uk", "ftc.gov", "github.com")

PRICE_RE = re.compile(r"\$\s?\d|\d+\.\d{2}\b(?=\s*(?:USD|per))|\bUSD\s?\d")
STAR_RE = re.compile(r"\d\.\d\s*(?:out of|/)\s*5|stars?\b(?!\s*-)\s*\d", re.I)
BANNED_WORDS = ("TODO", "FIXME", "TBD", "lorem", "XXXX")


def esc(v) -> str:
    return html.escape(str(v), quote=False)


def src_ref(token: str) -> str:
    """[[Sn]] -> superscript link; [[Sn|label]] -> labelled link. Raises if Sn is unknown."""
    sid, _, label = token.partition("|")
    sid = sid.strip()
    s = SRC.get(sid)
    if not s:
        raise SystemExit(f"editorial.json cites unknown source id {sid!r}")
    url = s["url"]
    text = label.strip() or sid
    return (f'<a class="src" href="{html.escape(url, quote=True)}" target="_blank" '
            f'rel="noopener noreferrer" title="{esc(s["title"])} — official page, captured '
            f'{esc(s.get("status_note","")[:90]) or "see register"}">{esc(text)}</a>')


def inline(text: str) -> str:
    """Escape first, then apply the tiny safe markup subset."""
    out = esc(text)

    def prod(m: re.Match) -> str:
        key = "P" + m.group(1)
        p = PRODUCTS.get(key)
        if not p:
            raise SystemExit(f"unknown product ref {m.group(0)!r}")
        return f'<a class="pref" href="{html.escape(p["url"], quote=True)}" target="_blank" rel="noopener noreferrer">{esc(p["short"])}</a>'

    out = re.sub(r"\{P([0-9])\}", prod, out)
    out = re.sub(r"\[\[([A-Za-z0-9-]+(?:\|[^\]]+)?)\]\]", lambda m: src_ref(m.group(1)), out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", out)
    return out


def table(block: dict) -> str:
    head = "".join(f"<th>{esc(h)}</th>" for h in block["headers"])
    rows = []
    for r in block["rows"]:
        cells = "".join(f"<td>{inline(c)}</td>" for c in r)
        rows.append(f"<tr>{cells}</tr>")
    cap = f'<figcaption>{inline(block["caption"])}</figcaption>' if block.get("caption") else ""
    return (f'<figure class="tbl"><table><thead><tr>{head}</tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table>{cap}</figure>')


# ---------------------------------------------------------------- page shell
def pre_for(rel: str) -> str:
    """Prefix that turns a read/-relative href into one valid from the page at rel."""
    return "../" * rel.count("/")


def page(rel: str, title: str, desc: str, body: str, *, canonical_slug: str,
         ld: list[dict], image: str | None = None) -> str:
    """rel: path under read/ e.g. 'index.html' or 'category/air-fryers.html'.

    Internal links inside `body` are written read/-relative and rewritten here, so a page
    moved a directory deeper never silently loses a link.
    """
    depth = rel.count("/")
    pre = pre_for(rel)
    up = pre + "../"                   # up to the repo root
    here = pre
    body = re.sub(r'(href=")(?!https?:|#|mailto:)([^"]+)"',
                  lambda m: m.group(1) + pre + m.group(2) + '"', body)
    body = re.sub(r'(src=")(?!https?:)([^"]+)"',
                  lambda m: m.group(1) + pre + m.group(2) + '"', body)

    def href_for(target: str) -> str:
        return up + target[3:] if target.startswith("../") else here + target

    nav = "".join(
        f'<a href="{href_for(l["href"])}"'
        f'{" class=on" if l["href"] == ("index.html" if rel == "index.html" else rel) else ""}">'
        f'{esc(l["label"])}</a>'
        for l in E["brand"]["links"]
    )
    og_image = image or "assets/img/hero-kitchen.jpg"
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    url = f'{E["site_base"]}/read/{rel}'

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · {esc(E["brand"]["name"])}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="{esc(E["brand"]["name"])}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{E["site_base"]}/{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="stylesheet" href="{up}assets/read.css">
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
{ld_html}
</head>
<body>
<div class="disclose"><div class="w"><strong>Disclosure:</strong> {esc(E["footer"]["disclosure"])} We have not tested these products; what follows is an analysis of the official listing copy, dated and linked.</div></div>
<header class="mast">
  <div class="w row">
    <a class="brand" href="{here}index.html"><span class="mk">CR</span><span class="bn">{esc(E["brand"]["name"])}</span><span class="bg">{esc(E["brand"]["kicker"])}</span></a>
    <nav>{nav}</nav>
  </div>
</header>
<main class="w">
{body}
</main>
<footer class="foot">
  <div class="w">
    <p class="disc">{esc(E["footer"]["disclosure"])}</p>
    <p>{esc(E["footer"]["disclaimer"])}</p>
    <p class="small">All product statements are dated captures of official Amazon pages ({esc(E["verified"])}); all prices, star ratings and review counts are withheld because Amazon's Program Policies 2(b) and 6(t) permit them only when Amazon or the Creators API serves them. Some content on this page comes from Amazon and is provided "AS IS".</p>
    <nav class="fl">{" · ".join(f'<a href="{href_for(l["href"])}">{esc(l["label"])}</a>' for l in E["footer"]["links"])}</nav>
    <p class="small muted">Built by <code>scripts/build_read.py</code> from <code>data/editorial.json</code> and <code>data/sources.json</code>. Editorial opinions are the site's own; the facts are Amazon's.</p>
  </div>
</footer>
</body>
</html>
"""


def crumb(rel: str, name: str) -> tuple[str, dict]:
    """Breadcrumb is written with an absolute site URL, so it is depth-proof."""
    nav = ('<p class="crumb"><a href="index.html">The Crisp Report</a> › '
           f'<span>{esc(name)}</span></p>')
    ld = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "The Crisp Report",
             "item": f'{E["site_base"]}/read/index.html'},
            {"@type": "ListItem", "position": 2, "name": name,
             "item": f'{E["site_base"]}/read/{rel}'},
        ],
    }
    return nav, ld


def article_ld(a: dict, rel: str) -> dict:
    return {
        "@context": "https://schema.org", "@type": "Article",
        "headline": a["title"], "description": a["dek"],
        "datePublished": a["date"], "dateModified": a["date"],
        "author": {"@type": "Organization", "name": E["brand"]["name"],
                   "url": f'{E["site_base"]}/read/method.html'},
        "publisher": {"@type": "Organization", "name": E["brand"]["name"]},
        "mainEntityOfPage": f'{E["site_base"]}/read/{a["slug"]}.html',
        "isAccessibleForFree": True,
        "about": [{"@type": "Product", "name": PRODUCTS[p]["name"], "asin": PRODUCTS[p]["asin"],
                   "url": PRODUCTS[p]["url"]} for p in a.get("products", [])] or None,
    }


# ---------------------------------------------------------------- pages
def build_index() -> None:
    b = E["brand"]
    hero = E["hero"]
    stats = "".join(
        f'<li><b>{inline(s["n"])}</b><span>{inline(s["l"])}</span></li>' for s in hero["stats"]
    )
    cards = ""
    for a in E["articles"]:
        cards += (
            f'<a class="card" href="{a["slug"]}.html">'
            f'<span class="kick">{esc(a["kicker"])}</span>'
            f'<h3>{esc(a["title"])}</h3><p>{esc(a["dek"])}</p>'
            f'<span class="meta">{esc(a["date"])} · {a["read"]} min · {len(a["sources"])} official sources</span></a>'
        )
    prods = ""
    for p in E["products"]:
        feats = "".join(f"<li>{inline(s['v'])}</li>" for s in p["stated"][:4])
        prods += (
            f'<article class="pcard"><p class="pc-kick">{esc(p["position"])}</p>'
            f'<h3>{esc(p["brand"])}</h3><p class="pn">{esc(p["name"])}</p>'
            f'<ul class="ticks">{feats}</ul>'
            f'<p class="pc-src">Listing title as served {esc(E["verified"])} · {src_ref(p["sources"]["listing"])}'
            f' · submitted link {src_ref(p["sources"]["link"])}</p>'
            f'<a class="btn" href="{html.escape(p["url"], quote=True)}" target="_blank" rel="nofollow sponsored noopener">View the official listing</a></article>'
        )
    rules = "".join(f'<div class="rule"><h3>{esc(r["h"])}</h3><p>{inline(r["p"])}</p></div>' for r in E["rules"])

    body = f"""
<section class="hero">
  <div class="hcopy">
    <p class="eyebrow">{esc(hero["eyebrow"])} · {esc(b["stamp"])}</p>
    <h1>{esc(hero["h2"])}</h1>
    <p class="lede">{esc(hero["lede"])}</p>
    <p class="acts"><a class="btn" href="{esc(hero["cta_primary"]["href"])}">{esc(hero["cta_primary"]["label"])}</a>
    <a class="btn ghost" href="{esc(hero["cta_secondary"]["href"])}">{esc(hero["cta_secondary"]["label"])}</a></p>
  </div>
  <figure class="hfig"><img src="../assets/img/hero-kitchen.jpg" alt="{esc(hero["image"]["alt"])}" width="1200" height="750"><figcaption>Illustration: our own. Amazon product imagery is Program Content and may not be copied onto this site.</figcaption></figure>
</section>
<ul class="statbar">{stats}</ul>
<h2 class="sh">The three we are reading</h2>
<p class="sub">Two baskets, one big basket, one oven. Same category, three different arguments. Details quoted from the listing titles Amazon served us today.</p>
<div class="pgrid">{prods}</div>
<h2 class="sh">Latest, and the receipts behind it</h2>
<p class="sub">Every claim footnote links the official page it came from and the date it was read. No prices, no stars — the method page explains why that is a rule, not an omission.</p>
<div class="agrid">{cards}</div>
<section class="rulesbox"><h2>Four rules this site will not break</h2><div class="rg">{rules}</div></section>
<section class="cta-strip"><h2>The evidence, if you want it</h2><p>These pages are generated from the same verified data as the operations dashboard: 51 dated official sources, a per-row verification log, and a register of every item we could not confirm — published, not hidden.</p>
<p class="acts"><a class="btn" href="../suggestions.html">Suggestions &amp; decisions</a><a class="btn ghost" href="../index.html">Operations dashboard</a><a class="btn ghost" href="../flagged.html">Flagged for review</a></p></section>
"""
    ld = [
        {"@context": "https://schema.org", "@type": "WebSite", "name": b["name"],
         "url": f'{E["site_base"]}/read/index.html',
         "description": f"{b['kicker']}. {b['promise']}"},
        {"@context": "https://schema.org", "@type": "ItemList", "name": "Air fryer guides and analysis",
         "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "name": a["title"],
              "url": f'{E["site_base"]}/read/{a["slug"]}.html'} for i, a in enumerate(E["articles"])
         ]},
    ]
    seo_title = f"{b['name']} — air fryers, read line by line off the listing"
    seo_desc = ("Three real air-fryer listings compared on what their titles actually say: "
                "capacity arithmetic, feature names, cleaning claims and a dated best-seller rank. "
                "No prices, no invented specs.")
    html_out = page("index.html", seo_title, seo_desc, body,
                    canonical_slug="read/index.html", ld=ld, image="assets/img/hero-kitchen.jpg")
    (OUT / "index.html").write_text(html_out, encoding="utf-8")


def build_article(a: dict) -> None:
    rel = f'{a["slug"]}.html'
    crumbs, ld_b = crumb(rel, a["title"])
    parts = [crumbs]
    parts.append(f'<article class="art"><header class="ah"><p class="kick">{esc(a["kicker"])}</p>'
                 f'<h1>{esc(a["title"])}</h1><p class="dek">{esc(a["dek"])}</p>'
                 f'<p class="meta">{esc(a["date"])} · {a["read"]} min read · {esc(E["brand"]["name"])}</p></header>')
    if a.get("image"):
        parts.append(f'<figure class="fig"><img src="../assets/img/{a["image"]["src"].split("/")[-1]}" alt="{esc(a["image"]["alt"])}" width="1200" height="750"><figcaption>Our own illustration. Amazon listing imagery is Program Content and is not reproduced here.</figcaption></figure>')
    for p in a["lede"]:
        parts.append(f'<p class="lp">{inline(p)}</p>')
    for sec in a["body"]:
        if sec.get("h"):
            parts.append(f'<h2>{esc(sec["h"])}</h2>')
        if sec.get("table"):
            parts.append(table(sec["table"]))
        for para in sec.get("p", []):
            cls = ""
            if isinstance(para, dict):
                para, cls = para["t"], f' class="{para["class"]}"'
            parts.append(f"<p{cls}>{inline(para)}</p>")
        if sec.get("ul"):
            parts.append('<ul class="bul">' + "".join(f"<li>{inline(x)}</li>" for x in sec["ul"]) + "</ul>")
        if sec.get("pull"):
            parts.append(f'<blockquote>{inline(sec["pull"])}</blockquote>')
    parts.append("</article>")

    gaps = "".join(f"<li>{inline(g)}</li>" for g in a.get("gaps", []))
    if gaps:
        parts.append(f'<section class="gaps"><h2>What this article cannot answer</h2><ul>{gaps}</ul>'
                     f'<p class="small">Unanswered items are also on the <a href="../flagged.html">flagged register</a>. A blank we left on purpose is better than a number we made up.</p></section>')
    srcs = "".join(f"<li>{src_ref(s)} — {esc(SRC[s]['title'])}</li>" for s in a.get("sources", []))
    parts.append(f'<section class="srcs"><h2>Sources, all official</h2><ul>{srcs}</ul>'
                 f'<p class="small">Captured {esc(E["verified"])} unless the title says otherwise. See also the full <a href="../sources.html">source register</a> and the <a href="../verification.html">verification log</a>.</p></section>')

    nav = '<p class="next"><a href="index.html">← All articles</a> · <a href="compare.html">The three-way table</a> · <a href="buying-guide.html">The five questions</a></p>'
    parts.append(nav)
    body = "\n".join(parts)
    out = page(rel, a["title"], a["dek"], body, canonical_slug=f"read/{rel}",
               ld=[article_ld(a, rel), ld_b],
               image=(a["image"]["src"] if a.get("image") else None))
    (OUT / rel).write_text(out, encoding="utf-8")


def build_compare() -> None:
    rel = "compare.html"
    c = E["compare"]
    crumbs, ld_b = crumb(rel, c["title"])
    ids = [p["id"] for p in E["products"]]
    head = "<th>Attribute</th>" + "".join(
        f'<th><a class="pref" href="{html.escape(PRODUCTS[i]["url"], quote=True)}" target="_blank" rel="noopener noreferrer">{esc(PRODUCTS[i]["name"])}</a><br><span class="thin">{esc(PRODUCTS[i]["asin"])}</span></th>'
        for i in ids)
    rows = ""
    for r in c["rows"]:
        cells = "".join(f"<td>{inline(r['cells'][i])}</td>" for i in ids)
        rows += f'<tr><th scope="row">{esc(r["attr"])}</th>{cells}</tr>'
    verdicts = "".join(f'<div class="v"><h3>{inline(v["h"])}</h3><p>{inline(v["p"])}</p></div>' for v in c["verdicts"])
    notes = "".join(f"<li>{inline(n)}</li>" for n in c["notes"])
    cards = "".join(
        f'<a class="btn" href="{html.escape(PRODUCTS[i]["url"], quote=True)}" target="_blank" rel="nofollow sponsored noopener">Official listing — {esc(PRODUCTS[i]["short"])}</a>'
        for i in ids)
    body = f"""{crumbs}
<article class="art">
<header class="ah"><p class="kick">{esc(c["kicker"])}</p><h1>{esc(c["title"])}</h1>
<p class="dek">{esc(c["dek"])}</p><p class="meta">{esc(c["date"])} · {esc(E["brand"]["name"])}</p></header>
<div class="tblwrap"><table class="cmp"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>
<h2>Which one, given what you cook</h2>
<div class="vgrid">{verdicts}</div>
<p class="acts">{cards}</p>
<h2>How to read the blanks</h2>
<ul class="bul">{notes}</ul>
<section class="srcs"><h2>Sources</h2><p class="small">Every cell above is sourced inside the cell. The four register sources behind the row about Amazon's best-seller list: {src_ref("S63")}. Policy rows: {src_ref("S02")}.</p></section>
</article>"""
    ld = {
        "@context": "https://schema.org", "@type": "Table",
        "about": "Air fryer comparison of three Amazon listings", "datePublished": c["date"],
        "url": f'{E["site_base"]}/read/{rel}',
    }
    (OUT / rel).write_text(page(rel, c["title"], c["dek"], body, canonical_slug=f"read/{rel}",
                                ld=[ld, ld_b]), encoding="utf-8")


def build_guide() -> None:
    rel = "buying-guide.html"
    g = E["guide"]
    crumbs, ld_b = crumb(rel, g["title"])
    steps = "".join(
        f'<section class="step"><span class="num">{esc(s["n"])}</span><h2>{esc(s["h"])}</h2><p>{inline(s["p"])}</p></section>'
        for s in g["steps"])
    donts = "".join(f'<div class="rule"><h3>{esc(d["h"])}</h3><p>{inline(d["p"])}</p></div>' for d in g["donts"])
    faq_html = "".join(
        f'<details><summary>{esc(f["q"])}</summary><p>{inline(f["a"])}</p></details>' for f in g["faq"])
    faq_ld = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": f["q"],
                        "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", inline(f["a"]))}}
                       for f in g["faq"]],
    }
    body = f"""{crumbs}
<article class="art">
<header class="ah"><p class="kick">{esc(g["kicker"])}</p><h1>{esc(g["title"])}</h1>
<p class="dek">{esc(g["dek"])}</p><p class="meta">{esc(g["date"])} · {esc(E["brand"]["name"])}</p></header>
{steps}
<h2>Four things not to do</h2>
<div class="rg four">{donts}</div>
<h2>Questions people ask us</h2>
<div class="faq">{faq_html}</div>
<p class="acts"><a class="btn" href="compare.html">Open the three-way table</a><a class="btn ghost" href="method.html">How we check</a></p>
</article>"""
    (OUT / rel).write_text(page(rel, g["title"], g["dek"], body, canonical_slug=f"read/{rel}",
                                ld=[faq_ld, ld_b]), encoding="utf-8")


def build_method() -> None:
    rel = "method.html"
    m = E["method"]
    crumbs, ld_b = crumb(rel, m["title"])
    intro = "".join(f'<p class="lp">{inline(p.replace("{NSRC}", str(len(SRC))))}</p>' for p in m["intro"])
    rows = "".join(
        f'<tr><td><strong>{esc(q["q"])}</strong></td><td><span class="pill">{esc(q["status"])}</span></td>'
        f'<td>{inline(q["why"])}</td><td>{esc(q["unlock"])}</td><td>{src_ref(q["src"])}</td></tr>'
        for q in m["open_questions"])
    src_list = "".join(
        f"<li>{src_ref(k)} — {esc(v['title'])}</li>"
        for k, v in sorted(SRC.items(), key=lambda x: int(re.sub(r"\D", "", x[0]) or 0))
        if k in {s for a in E["articles"] for s in a.get("sources", [])} | {p["sources"]["listing"] for p in E["products"]} | {p["sources"]["link"] for p in E["products"]})
    body = f"""{crumbs}
<article class="art">
<header class="ah"><p class="kick">{esc(m["kicker"])}</p><h1>{esc(m["title"])}</h1>
<p class="dek">{esc(m["dek"])}</p></header>
{intro}
<h2>The pipeline, in order</h2>
<ol class="pipe">
<li>Each submitted link is followed and its final URL and served page title are recorded verbatim, with the date.</li>
<li>Only text from those captures enters the copy. A number that is not in a capture does not appear on this site.</li>
<li>Policy statements are quoted from the Amazon Associates Operating Agreement and Program Policies, and from FTC guidance, each with its own dated source entry.</li>
<li>The generator fails if a table row has no official-source link, if a price pattern appears, or if a star-rating pattern appears.</li>
<li>Anything that cannot be confirmed is left blank in the data and published on the flagged register instead of being filled in.</li>
</ol>
<div class="callout"><p><strong>What that buys you.</strong> A page you can audit. If you find a statement here that the official page does not support, that is a defect, and the flagged register is where we would have recorded it. <a href="../flagged.html">Open the register</a>.</p></div>
<h2>What we cannot answer yet</h2>
<p class="small">These are the questions whose answers change what this site is allowed to say, or let it say more. Each row links the official page that frames it. {esc(m["sources_note"])}</p>
<div class="tblwrap"><table><thead><tr><th>Open question</th><th>Status</th><th>Why it matters</th><th>What would settle it</th><th>Source</th></tr></thead><tbody>{rows}</tbody></table></div>
<h2>Sources used by these pages</h2>
<ul class="srcs-list">{src_list}</ul>
</article>"""
    ld = {"@context": "https://schema.org", "@type": "HowTo", "name": "How The Crisp Report verifies a product claim",
          "description": m["dek"], "step": [{"@type": "HowToStep", "name": s.split(".")[0]} for s in [
              "Follow each submitted link and record the final URL and served page title verbatim with the date",
              "Use only text present in those captures",
              "Quote policy statements from Amazon Associates and FTC pages with dated sources",
              "Fail the build on an uncited table row, a price pattern or a star-rating pattern",
              "Leave unverifiable values blank and publish them on the flagged register"]]}
    (OUT / rel).write_text(page(rel, m["title"], m["dek"], body, canonical_slug=f"read/{rel}",
                                ld=[ld, ld_b]), encoding="utf-8")


def build_category() -> None:
    rel = "category/air-fryers.html"
    c = E["category"]
    crumbs, ld_b = crumb(rel, "Air fryers")
    node_rows = "".join(
        f'<tr><td>{esc(n["label"])}</td><td><code>{esc(n["node"])}</code></td><td>{src_ref("S64")}</td></tr>'
        for n in c["nodes"])
    sib_rows = "".join(
        f'<tr><td>{esc(s["label"])}</td><td><code>{esc(s["node"])}</code></td><td>{src_ref("S64")}</td></tr>'
        for s in c["siblings"])
    cards = "".join(
        f'<a class="card" href="{a["slug"]}.html"><span class="kick">{esc(a["kicker"])}</span><h3>{esc(a["title"])}</h3>'
        f'<p>{esc(a["dek"])}</p><span class="meta">{esc(a["date"])}</span></a>' for a in E["articles"])
    prod_rows = "".join(
        f'<tr><td><strong>{esc(p["brand"])}</strong><br><span class="thin">{esc(p["name"])}</span></td>'
        f'<td><a href="{html.escape(p["url"], quote=True)}" target="_blank" rel="noopener noreferrer">{esc(p["asin"])}</a></td>'
        f'<td>{esc(p["stated"][0]["v"])}</td><td>{esc(p["position"])}</td><td>{src_ref(p["sources"]["link"])} {src_ref(p["sources"]["listing"])}</td></tr>'
        for p in E["products"])
    body = f"""{crumbs}
<article class="art">
<header class="ah"><p class="kick">Category hub</p><h1>Air fryers</h1>
<p class="dek">Everything on this site lives in one Amazon browse node. Here is that node, the three listings we read inside it, and the articles we wrote about them.</p>
<p class="meta">{esc(E["verified"])} · {esc(E["brand"]["name"])}</p></header>
<h2>Where this category sits</h2>
<p>{esc(" › ".join(c["breadcrumb"]))} — read from the breadcrumb Amazon served on the product pages on {esc(E["verified"])} {src_ref("S60")}.</p>
<div class="tblwrap"><table><thead><tr><th>Node</th><th>Amazon browse node id</th><th>Source</th></tr></thead><tbody>{node_rows}{sib_rows}</tbody></table></div>
<h2>The three listings in this category</h2>
<div class="tblwrap"><table><thead><tr><th>Listing</th><th>ASIN of the destination page</th><th>Capacity as stated in the title</th><th>Shape of it</th><th>Sources</th></tr></thead><tbody>{prod_rows}</tbody></table></div>
<div class="callout"><p><strong>Best-seller context, dated.</strong> {inline(c["bestsellers_note"])} Positions are a snapshot; the page itself says the list is updated frequently. We publish the position, the date and the link, and no interpretation of sales.</p></div>
<h2>Reading in this category</h2>
<div class="agrid">{cards}</div>
<p class="acts"><a class="btn" href="../index.html">Back to the front page</a><a class="btn ghost" href="../air-fryers.html">The verified category table (dashboard)</a></p>
</article>"""
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Air fryers",
          "description": "Category hub for air fryer guides on The Crisp Report",
          "mainEntity": {"@type": "ItemList", "itemListElement": [
              {"@type": "ListItem", "position": i + 1, "url": f'{E["site_base"]}/read/{a["slug"]}.html', "name": a["title"]}
              for i, a in enumerate(E["articles"])]}}
    (OUT / rel).parent.mkdir(parents=True, exist_ok=True)
    (OUT / rel).write_text(page(rel, "Air fryers — guides and verified listings",
                                "Air fryer buying guides, a three-listing comparison and the official Amazon category data behind them.",
                                body, canonical_slug=f"read/{rel}", ld=[ld, ld_b]), encoding="utf-8")


# ---------------------------------------------------------------- gates
def audit() -> None:
    errs = []
    for p in sorted(OUT.rglob("*.html")):
        raw = p.read_text(encoding="utf-8")
        text = re.sub(r"<[^>]+>", " ", html.unescape(raw))
        rel = p.relative_to(ROOT).as_posix()
        if E["footer"]["disclosure"] not in raw:
            errs.append(f"{rel}: disclosure sentence missing")
        if "COMES FROM AMAZON" not in raw.upper():
            errs.append(f"{rel}: Amazon content disclaimer missing")
        if len(re.findall(r"<h1[\s>]", raw)) != 1:
            errs.append(f"{rel}: expected exactly one <h1>")
        for w in BANNED_WORDS:
            if w.lower() in text.lower():
                errs.append(f"{rel}: placeholder marker {w!r}")
        # Program Policies 2(b) is about Product prices and availability. Amazon's own
        # published programme figures (bounty rates, payment minimums) are not Product prices;
        # they are exempted only inside an element explicitly marked class="rates".
        scan = re.sub(r'<p class="rates">.*?</p>', " ", raw, flags=re.S)
        scan = re.sub(r"<[^>]+>", " ", html.unescape(scan))
        m = PRICE_RE.search(scan)
        if m:
            errs.append(f"{rel}: a price-shaped value appears outside a marked rates paragraph "
                        f"(policy 2(b)) -> {m.group(0)!r}")
        for block in re.findall(r'<article class="pcard">.*?</article>|<table class="cmp">.*?</table>', raw, re.S):
            bt = re.sub(r"<[^>]+>", " ", html.unescape(block))
            if PRICE_RE.search(bt) or STAR_RE.search(bt):
                errs.append(f"{rel}: a price or rating pattern appears in a product surface -> "
                            f"{(PRICE_RE.search(bt) or STAR_RE.search(bt)).group(0)!r}")
        if STAR_RE.search(text):
            errs.append(f"{rel}: a star-rating-shaped value appears (policy 6(t)) -> {STAR_RE.search(text).group(0)!r}")
        for img in re.findall(r'<img[^>]+src="([^"]+)"', raw):
            host = re.sub(r"^https?://", "", img).split("/")[0]
            if "amazon" in host:
                errs.append(f"{rel}: Amazon-hosted image src is prohibited -> {img}")
        for tb in re.findall(r"<tbody>(.*?)</tbody>", raw, re.S):
            for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", tb, re.S):
                if not any(h in tr for h in OFFICIAL_HOSTS):
                    errs.append(f"{rel}: table row without an official source link -> "
                                f"{re.sub(r'<[^>]+>',' ',tr)[:60].strip()!r}")
        for href in re.findall(r'(?:href|src)="([^"#]+)"', raw):
            if href.startswith(("http://", "https://", "mailto:")):
                if href.startswith("http://"):
                    errs.append(f"{rel}: insecure external link {href}")
                continue
            tgt = (p.parent / href.split("#")[0]).resolve()
            try:
                tgt.relative_to(ROOT)
            except ValueError:
                continue
            if not tgt.exists():
                errs.append(f"{rel}: broken internal link -> {href}")
    if errs:
        raise SystemExit("BUILD GATE FAILED:\n  " + "\n  ".join(errs))
    n = len(list(OUT.rglob("*.html")))
    print(f"build_read: {n} pages, gates passed "
          f"(disclosure, single h1, no price/star patterns, sourced rows, no broken links)")


def main() -> None:
    check = "--check" in sys.argv
    before = {p: p.read_text(encoding="utf-8") for p in OUT.rglob("*.html")} if check else {}
    OUT.mkdir(exist_ok=True)
    build_index()
    for a in E["articles"]:
        a["products"] = list(PRODUCTS)
        build_article(a)
    build_compare()
    build_guide()
    build_method()
    build_category()
    audit()
    if check:
        after = {p: p.read_text(encoding="utf-8") for p in OUT.rglob("*.html")}
        drift = [p.relative_to(ROOT).as_posix() for p in before if before[p] != after.get(p)]
        drift += [p.relative_to(ROOT).as_posix() for p in after if p not in before]
        if drift:
            raise SystemExit("--check: output differs from the committed pages: " + ", ".join(sorted(drift)))
        print("build_read --check: committed output matches the generator")


if __name__ == "__main__":
    main()

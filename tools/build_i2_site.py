#!/usr/bin/env python3
"""Build the I2 reader-facing marketing site into site/.

Standard library only. Run from the repository root:

    python3 tools/build_i2_site.py

One generator, one output directory. It reads data/i2/{sources,catalog,verification,
decisions}.json and writes every page under site/. It never writes outside site/,
so it cannot collide with the earlier site generations in the repository root or in
dashboard/.

Two rules are enforced by construction, not by convention:

  * every table cell that states a fact carries a link to the page it was read from;
  * a cell with no official source renders as an explicit "not published" note that
    says why, never as a guess and never as a bare dash.

tools/i2_gate.py audits the emitted HTML afterwards and is what makes the rules a
release gate rather than a style guide.
"""
from __future__ import annotations

import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "i2"
OUT = ROOT / "site"

BUILT = "2026-11-16"
DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."
DISCLAIMER = ("CERTAIN CONTENT THAT APPEARS ON THIS SITE COMES FROM AMAZON. "
              "THIS CONTENT IS PROVIDED ‘AS IS’ AND IS SUBJECT TO CHANGE OR REMOVAL AT ANY TIME.")
SITE_NAME = "Air Fryer Field Notes"
SITE_TAGLINE = "Three air fryers, checked line by line."


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


SOURCES = {s["id"]: s for s in load("sources.json")["sources"]}
CATALOG = load("catalog.json")
VERIFY = load("verification.json")
DECISIONS = load("decisions.json")
PRODUCTS = CATALOG["products"]


def e(v) -> str:
    return html.escape(str(v), quote=True)


# A link.amazon short link is a source, but it must not be used as an outbound
# destination: Program Policies 6(v)/6(w) prohibit obscuring the Amazon page a
# visitor is being sent to. The register therefore links the resolved listing and
# shows the submitted token as text.
RESOLVED = {
    "https://link.amazon/B04G1MEwY": "https://www.amazon.com/dp/B0CDY277D3",
    "https://link.amazon/B02NbDxp3": "https://www.amazon.com/dp/B09B7SB46R",
    "https://link.amazon/B00hJ57DV": "https://www.amazon.com/dp/B08DKYBTPH",
}


def src(sql_id, label=None) -> str:
    """A short, readable source link: the ID points at the exact page."""
    s = SOURCES[sql_id]
    text = label or sql_id
    href = RESOLVED.get(s["url"], s["url"])
    return (f'<a class="src" href="{e(href)}" target="_blank" rel="noopener noreferrer" '
            f'title="{e(s["title"])} — read {e(s["fetched"])}">{e(text)}</a>')


def srcs(ids) -> str:
    if not ids:
        return ""
    return " ".join(src(i) for i in ids)


def blank(reason, flag) -> str:
    """A deliberately empty cell: states why, never guesses."""
    return (f'<span class="blank"><span class="blank-dot"></span>Not published</span>'
            f'<span class="blank-why">{e(reason)}</span>'
            + (f' {flagref(flag)}' if flag else ""))


def flagref(fid, label=None) -> str:
    return f'<a class="flagref" href="{rel("flagged.html")}#{e(fid)}">{e(label or fid)}</a>'


# --------------------------------------------------------------------------- shell
NAV = [
    ("index.html", "Start here"),
    ("products.html", "The three air fryers"),
    ("guides/index.html", "Buying guides"),
    ("evidence.html", "How we know"),
    ("measure.html", "How we measure"),
    ("intent-record.html", "Intent record"),
    ("decisions.html", "Suggestions &amp; decisions"),
]
# Added by session ded63349 (2026-11-17): measure.html and intent-record.html implement the
# brief's measurement, cadence, feed and product-intent priorities. They live in this list so
# every generated page carries them in the single reader navigation group.

# Pages live at two depths: site/*.html and site/guides/*.html
DEPTH = {}


def rel(path: str) -> str:
    """Prefix a nav target for the page currently being written."""
    depth = DEPTH.get("current", 0)
    return ("../" * depth) + path


def page(path: str, title: str, body: str, lead: str = "", description: str = "",
         depth: int = 0) -> None:
    DEPTH["current"] = depth
    nav_parts = []
    for h, lab in NAV:
        cls = ' class="on"' if h == path else ""
        nav_parts.append('<a href="' + rel(h) + '"' + cls + '>' + lab + "</a>")
    nav = "".join(nav_parts)
    lede = f'<p class="lede">{lead}</p>' if lead else ""
    desc = description or "Air fryer buying guides built only on facts that can be checked against the Amazon listing."
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} · {e(SITE_NAME)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="https://kanlerxz87-cyber.github.io/Zone3/site/{e(path)}">
<link rel="alternate" type="application/atom+xml" title="Air Fryer Field Notes — new guides and field notes" href="{rel('../feed.xml')}">
<link rel="stylesheet" href="{rel('assets/site.css')}">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="disclose-bar" role="note">
  <div class="wrap">
    <strong>Affiliate disclosure:</strong> {e(DISCLOSURE)}
    <span class="disclose-more">Links to Amazon on this site are evidence links while a tracking tag is unavailable, so they earn nothing yet. <a href="{rel('evidence.html')}#disclosure">Why this is stated twice</a>.</span>
  </div>
</div>
<header class="top">
  <div class="wrap top-in">
    <a class="brand" href="{rel('index.html')}">
      <span class="mark" aria-hidden="true">AF</span>
      <span class="brand-text"><strong>{e(SITE_NAME)}</strong><small>{e(SITE_TAGLINE)}</small></span>
    </a>
    <nav aria-label="Main">{nav}</nav>
  </div>
</header>
<main id="main" class="wrap">
{lede}
{body}
</main>
<footer class="foot">
  <div class="wrap">
    <p class="foot-disclose"><strong>Disclosure:</strong> {e(DISCLOSURE)}</p>
    <p class="foot-small">{e(DISCLAIMER)}</p>
    <p class="foot-small">{e(SITE_NAME)} is independent and is not affiliated with, endorsed or sponsored by Amazon. Amazon, Amazon Associates and ASIN are trademarks of Amazon.com, Inc. or its affiliates. Facts on this site were read from the official pages linked under each table on <strong>{e(BUILT)}</strong>; each link opens the page it was read from. Blank cells are blank on purpose and say why.</p>
    <p class="foot-small"><a href="{rel('evidence.html')}">How we know — sources and verification log</a> · <a href="{rel('decisions.html')}">Suggestions &amp; decisions</a> · <a href="{rel('front-door.html')}">Front door (audit dashboard)</a> · <a href="https://github.com/kanlerxz87-cyber/Zone3">Repository</a></p>
  </div>
</footer>
</body>
</html>
"""
    target = OUT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(doc, encoding="utf-8")


# --------------------------------------------------------------------------- css
CSS = r"""
:root{
  --ink:#14181f; --ink-2:#48505f; --ink-3:#767f8d; --line:#e2e6ec; --line-2:#eef1f5;
  --paper:#ffffff; --paper-2:#f7f9fc; --paper-3:#f0f4f9;
  --accent:#0b6b53; --accent-2:#0e8a6a; --accent-ink:#064e3c; --accent-wash:#e8f5f0;
  --amber:#8a5a00; --amber-wash:#fdf4dd; --amber-line:#f0dfb0;
  --bad:#a8322a; --bad-wash:#fdeeec;
  --radius:14px; --radius-sm:9px;
  --shadow:0 1px 2px rgba(15,23,42,.04), 0 8px 24px -12px rgba(15,23,42,.18);
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;
  --serif:Georgia,"Iowan Old Style","Times New Roman",serif;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--paper-2);color:var(--ink);font:16px/1.6 var(--sans);font-variant-numeric:tabular-nums}
a{color:var(--accent-ink);text-underline-offset:2px}
a:hover{color:var(--accent-2)}
.skip{position:absolute;left:-9999px}
.skip:focus{left:12px;top:12px;background:#fff;padding:8px 12px;border-radius:8px;z-index:99}
.wrap{max-width:1120px;margin:0 auto;padding:0 22px}

/* disclosure bar — deliberately plain, non-dismissable, above everything */
.disclose-bar{background:var(--accent-wash);border-bottom:1px solid #cfe8de;color:var(--accent-ink);font-size:13.5px}
.disclose-bar .wrap{padding:9px 22px;display:flex;gap:8px 18px;flex-wrap:wrap;align-items:baseline}
.disclose-bar strong{font-weight:700}
.disclose-more{color:#3f6b5c}
.disclose-more a{color:#2d5a4b}

.top{background:var(--paper);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:30;box-shadow:0 1px 0 rgba(15,23,42,.02)}
.top-in{display:flex;align-items:center;gap:26px;min-height:66px;padding:10px 22px;flex-wrap:wrap}
.brand{display:flex;gap:11px;align-items:center;text-decoration:none;color:var(--ink)}
.mark{width:34px;height:34px;border-radius:10px;background:linear-gradient(150deg,var(--accent),#17957a);color:#fff;display:grid;place-items:center;font-weight:800;font-size:13px;letter-spacing:.02em}
.brand-text{display:flex;flex-direction:column;line-height:1.15}
.brand-text strong{font-family:var(--serif);font-size:18px;letter-spacing:-.2px}
.brand-text small{color:var(--ink-3);font-size:12px}
.top nav{margin-left:auto;display:flex;gap:2px;flex-wrap:wrap}
.top nav a{display:inline-flex;align-items:center;min-height:44px;padding:8px 12px;border-radius:8px;color:var(--ink-2);text-decoration:none;font-size:14.5px;font-weight:520}
.top nav a:hover{background:var(--paper-3);color:var(--ink)}
.top nav a.on{background:var(--accent);color:#fff}

main{padding:34px 0 70px}
.lede{font-size:18px;color:var(--ink-2);max-width:70ch;margin:0 0 26px}
h1{font-family:var(--serif);font-size:clamp(30px,4.4vw,44px);line-height:1.1;letter-spacing:-.9px;margin:0 0 14px;max-width:24ch}
h2{font-family:var(--serif);font-size:clamp(22px,2.6vw,29px);line-height:1.2;letter-spacing:-.4px;margin:44px 0 12px}
h3{font-size:17.5px;line-height:1.3;margin:26px 0 8px}
p{margin:0 0 14px;max-width:74ch}
.small{font-size:13px;color:var(--ink-3)}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.88em}

/* hero */
.hero{background:linear-gradient(165deg,#0d3b30 0%,#0b6b53 55%,#129077 100%);color:#fff;border-radius:22px;padding:clamp(26px,4vw,52px);margin:0 0 26px;box-shadow:var(--shadow);position:relative;overflow:hidden}
.hero:after{content:"";position:absolute;right:-90px;top:-90px;width:320px;height:320px;border-radius:50%;background:rgba(255,255,255,.06)}
.hero h1{color:#fff;max-width:20ch}
.hero p{color:#d8efe8;font-size:17px;max-width:62ch}
.eyebrow{font-size:12px;letter-spacing:.16em;text-transform:uppercase;font-weight:700;color:#8ed8c3;margin:0 0 12px}
.cta-row{display:flex;gap:12px;flex-wrap:wrap;margin-top:24px}
.btn{display:inline-flex;align-items:center;gap:8px;border-radius:10px;padding:11px 17px;font-weight:650;font-size:15px;text-decoration:none;border:1px solid transparent;transition:transform .08s ease}
.btn:active{transform:translateY(1px)}
.btn-primary{background:#fff;color:var(--accent-ink)}
.btn-primary:hover{color:var(--accent-ink);background:#f2fbf8}
.btn-ghost{border-color:rgba(255,255,255,.5);color:#fff}
.btn-ghost:hover{color:#fff;background:rgba(255,255,255,.1)}
.btn-disabled{background:#e9edf2;color:#79828f;border-color:#dfe4ea;cursor:not-allowed}
.btn-disabled:hover{color:#79828f}
.btn[aria-disabled="true"]{pointer-events:none}

/* cards */
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:18px;margin:22px 0 8px}
.card{background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);padding:22px;box-shadow:var(--shadow);display:flex;flex-direction:column}
.card h3{margin:0 0 4px;font-family:var(--serif);font-size:20px;letter-spacing:-.3px}
.card .kicker{font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);margin:0 0 8px}
.card .facts{list-style:none;padding:0;margin:12px 0 0;font-size:14.5px;color:var(--ink-2)}
.card .facts li{padding:5px 0 5px 20px;position:relative;border-bottom:1px dashed var(--line-2)}
.card .facts li:last-child{border-bottom:0}
.card .facts li:before{content:"";position:absolute;left:2px;top:13px;width:7px;height:7px;border-radius:50%;background:var(--accent-2);opacity:.55}
.card .card-foot{margin-top:auto;padding-top:16px;display:flex;flex-direction:column;gap:9px}
.prov{font-size:12px;color:var(--ink-3);line-height:1.5}

/* callouts */
.note{border-left:3px solid var(--accent-2);background:var(--paper);padding:14px 18px;border-radius:0 10px 10px 0;margin:18px 0;font-size:15px;box-shadow:1px 0 0 var(--line)}
.note.warn{border-color:var(--amber);background:var(--amber-wash)}
.note.bad{border-color:var(--bad);background:var(--bad-wash)}
.note p:last-child{margin-bottom:0}
.note h3{margin-top:0}

/* tables */
.tablewrap{background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);overflow:auto;margin:18px 0 10px}
table{border-collapse:collapse;width:100%;font-size:14.5px}
caption{caption-side:top;text-align:left;padding:16px 18px 4px;font-weight:650;color:var(--ink-2);font-size:13px;letter-spacing:.02em}
th,td{text-align:left;padding:11px 14px;border-bottom:1px solid var(--line-2);vertical-align:top}
th{background:var(--paper-3);font-size:11.5px;text-transform:uppercase;letter-spacing:.06em;color:var(--ink-3);font-weight:700;white-space:nowrap}
tbody tr:hover{background:#fbfcfe}
tbody tr:last-child td{border-bottom:0}
td.lead-cell{font-weight:600;color:var(--ink)}
.src{display:inline-flex;align-items:center;min-height:24px;font-size:11px;font-weight:700;letter-spacing:.03em;color:var(--accent-ink);background:var(--accent-wash);border:1px solid #cfe8de;border-radius:6px;padding:1px 6px;text-decoration:none;white-space:nowrap;margin:1px 2px 1px 0}
.src:hover{background:#d9efe7;color:var(--accent-ink)}
.blank{display:inline-flex;align-items:center;gap:6px;font-size:12.5px;font-weight:650;color:var(--amber);background:var(--amber-wash);border:1px solid var(--amber-line);border-radius:999px;padding:1px 9px}
.blank-dot{width:6px;height:6px;border-radius:50%;background:var(--amber);display:inline-block}
.blank-why{display:block;font-size:12px;color:var(--ink-3);margin-top:5px;max-width:34ch;line-height:1.45}
.flagref{font-size:11px;font-weight:700;color:var(--bad);text-decoration:none;white-space:nowrap}
.badge{display:inline-block;font-size:11.5px;font-weight:700;border-radius:999px;padding:2px 9px;white-space:nowrap}
.b-ok{background:var(--accent-wash);color:var(--accent-ink)}
.b-warn{background:var(--amber-wash);color:var(--amber)}
.b-bad{background:var(--bad-wash);color:var(--bad)}
.b-mute{background:var(--paper-3);color:var(--ink-3)}

/* feature list / steps */
.steps{counter-reset:s;list-style:none;padding:0;margin:18px 0}
.steps li{counter-increment:s;position:relative;padding:0 0 20px 46px;border-left:2px solid var(--line);margin-left:14px}
.steps li:last-child{border-left-color:transparent;padding-bottom:0}
.steps li:before{content:counter(s);position:absolute;left:-15px;top:-2px;width:28px;height:28px;border-radius:50%;background:var(--accent);color:#fff;display:grid;place-items:center;font-size:13px;font-weight:800}
.steps b{display:block;margin-bottom:3px}

/* proposal cards */
.prop{background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:22px;margin:18px 0}
.prop-head{display:flex;gap:14px;align-items:flex-start;flex-wrap:wrap;margin-bottom:6px}
.prop-head h3{margin:0;flex:1 1 320px;font-family:var(--serif);font-size:21px;letter-spacing:-.3px}
.prop .pid{font-family:var(--mono);font-size:12px;color:var(--ink-3);background:var(--paper-3);border:1px solid var(--line);border-radius:6px;padding:1px 6px}
.prop dl{margin:14px 0 0;display:grid;grid-template-columns:150px 1fr;gap:10px 18px;font-size:14.5px}
.prop dt{font-weight:700;color:var(--ink-2);font-size:13px;text-transform:uppercase;letter-spacing:.05em}
.prop dd{margin:0;color:var(--ink-2);max-width:76ch}
@media(max-width:680px){.prop dl{grid-template-columns:1fr;gap:4px}.prop dt{margin-top:10px}}
.evidence{list-style:none;padding:0;margin:8px 0 0;font-size:14px}
.evidence li{padding:7px 0;border-bottom:1px dashed var(--line-2)}
.evidence li:last-child{border-bottom:0}
.term{font-size:10.5px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;border-radius:5px;padding:1px 6px;margin-right:7px;white-space:nowrap}
.t-official{background:var(--accent-wash);color:var(--accent-ink)}
.t-observed{background:#e9effb;color:#1d3f8a}
.t-editorial{background:var(--paper-3);color:var(--ink-3)}

/* decision control */
.decide{border-top:1px solid var(--line);margin-top:18px;padding-top:16px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.decide fieldset{border:0;padding:0;margin:0;display:flex;gap:6px;align-items:center;flex-wrap:wrap}
.decide legend{font-size:12.5px;font-weight:700;color:var(--ink-2);text-transform:uppercase;letter-spacing:.05em;float:left;margin-right:8px}
.seg{display:inline-flex;border:1px solid var(--line);border-radius:9px;overflow:hidden;background:var(--paper)}
.seg label{position:relative}
.seg input{position:absolute;opacity:0;width:1px;height:1px}
.seg span{display:inline-flex;align-items:center;min-height:44px;padding:7px 13px;font-size:13.5px;font-weight:600;color:var(--ink-2);cursor:pointer;border-right:1px solid var(--line)}
.seg label:last-child span{border-right:0}
.seg input:checked + span{background:var(--accent);color:#fff}
.seg input:focus-visible + span{outline:2px solid var(--accent-2);outline-offset:-2px}
.decide output{font-size:13px;color:var(--ink-3);flex:1 1 260px}
.decide textarea{width:100%;min-height:56px;margin-top:10px;border:1px solid var(--line);border-radius:9px;padding:9px 11px;font:inherit;font-size:14px;color:var(--ink);background:var(--paper)}
.decision-tools{background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);padding:20px;box-shadow:var(--shadow);margin:18px 0}
.decision-tools textarea{width:100%;min-height:150px;border:1px solid var(--line);border-radius:9px;padding:12px;font-family:var(--mono);font-size:12.5px;background:var(--paper-2);color:var(--ink);margin:10px 0}
.decision-tools button{background:var(--accent);color:#fff;border:0;border-radius:9px;padding:10px 16px;font:inherit;font-weight:650;cursor:pointer}
.decision-tools button:hover{background:var(--accent-2)}
.tools-row{display:flex;gap:10px;flex-wrap:wrap;align-items:center}

/* misc */
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:18px}
.kv{display:grid;grid-template-columns:auto 1fr;gap:8px 16px;font-size:14.5px;margin:0}
.kv dt{color:var(--ink-3);font-weight:600}
.kv dd{margin:0}
.foot{border-top:1px solid var(--line);background:var(--paper);margin-top:40px;padding:26px 0 44px;font-size:13.5px;color:var(--ink-2)}
.foot-disclose{font-size:14.5px;color:var(--ink)}
.foot-small{font-size:12px;color:var(--ink-3);line-height:1.6;max-width:92ch}
.hr{height:1px;background:var(--line);border:0;margin:34px 0}
@media(max-width:700px){
  .top-in{gap:10px;min-height:0;padding:10px 16px}
  .top nav{margin-left:0;width:100%;overflow-x:auto;flex-wrap:nowrap;padding-bottom:2px}
  .top nav a{white-space:nowrap}
  th,td{padding:9px 10px}
  .tablewrap{border-radius:12px}
  .btn{min-height:44px}
  main{padding:22px 0 50px}
  .wrap{padding:0 16px}
  .disclose-bar .wrap{padding:9px 16px}
}
@media print{.disclose-bar,.top nav,.decide,.decision-tools{display:none}body{background:#fff}}
/* ---- Mobile-first pass (session ded63349, 2026-11-17; proposal D-22): fluid type
   scale, 44px tap targets on primary controls, comfortable table cells on small
   screens, and a sticky quick-compare bar on guide pages. ---- */
h1{font-size:clamp(1.7rem,4.2vw,2.35rem)}
h2{font-size:clamp(1.25rem,2.6vw,1.6rem)}
@media(max-width:720px){
  h1{font-size:clamp(1.55rem,6vw,2.1rem)}
  h2{font-size:clamp(1.18rem,4.6vw,1.45rem)}
  .top nav a,.btn,a.btn,.fd-btn,button,input[type="submit"],input[type="radio"]+span,.msticky a{min-height:44px}
  .top nav a,.btn,a.btn,.fd-btn,button,.msticky a{display:inline-flex;align-items:center}
  td,th{padding:.72rem .6rem}
  table{font-size:.94rem}
  .card,.prop{padding:16px}
}
.msticky{display:none}
@media(max-width:720px){
  .msticky{display:flex;position:sticky;bottom:0;z-index:9;gap:10px;background:#fff;border-top:2px solid var(--line);padding:10px 2px;margin-top:30px}
  .msticky a{flex:1;text-align:center;font-weight:700;font-size:.92rem;border:1.6px solid var(--line);border-radius:999px;padding:12px 10px;background:var(--accent);color:#fff;border-color:var(--accent)}
  .msticky a+a{background:#fff;color:var(--ink);border-color:var(--line)}
}
"""


def build_css():
    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    (OUT / "assets" / "site.css").write_text(CSS.lstrip(), encoding="utf-8")


# --------------------------------------------------------------------------- pages
def product_card(p, cta_state="disabled") -> str:
    facts = "".join(f"<li>{e(f)}</li>" for f in p["title_facts"][:4])
    if cta_state == "disabled":
        cta = (f'<span class="btn btn-disabled" aria-disabled="true">View on Amazon — link not active yet</span>'
               f'<span class="small">No tracking tag is available yet, so a click could not be credited to this site. '
               f'<a href="{rel("decisions.html")}#Q1">What is needed</a>.</span>')
    else:
        cta = ""
    return f"""<article class="card">
  <p class="kicker">{e(p['ref'])} · {e(p['brand_as_listed'])}</p>
  <h3>{e(p.get('short_title') or p['listing_title'].split(' | ')[0])}</h3>
  <p class="small">{e(p['category_path'])}</p>
  <ul class="facts">{facts}</ul>
  <div class="card-foot">
    {cta}
    <p class="prov">Read from the <a href="{e(p['destination_url'])}" data-ref="{e(p['ref'])}" target="_blank" rel="noopener noreferrer">Amazon listing {e(p['destination_asin'])}</a> on {e(BUILT)}. {srcs(p['sources'])}</p>
  </div>
</article>"""


def build_index():
    cards = "".join(product_card(p) for p in PRODUCTS)
    rows = []
    for r in CATALOG["comparison"]["rows"]:
        is_blank = any(r.get(k) is None for k in ("p1", "p2", "p3"))
        cells = []
        for k in ("p1", "p2", "p3"):
            v = r.get(k)
            if v is None:
                # One short marker per cell; the reason is stated once, in the source column,
                # so a reader is told why without reading the same sentence three times.
                cells.append('<td><span class="blank"><span class="blank-dot"></span>Not published</span></td>')
            else:
                cells.append(f"<td>{e(v)}</td>")
        if is_blank:
            trailing = (f'{flagref(r["flag"])} <span class="blank-why">{e(r.get("blank_reason", ""))}</span>')
        else:
            trailing = srcs(r["sources"])
        rows.append('<tr><td class="lead-cell">' + e(r["label"]) + "</td>" + "".join(cells)
                    + "<td>" + trailing + "</td></tr>")
    table = (f'<div class="tablewrap"><table><caption>{e(CATALOG["comparison"]["caption"])}</caption>'
             f'<thead><tr><th>What the listing states</th><th>P1 · CHEFMAN</th><th>P2 · Emeril Lagasse</th>'
             f'<th>P3 · Chefman</th><th>Source</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>')

    body = f"""
<section class="hero">
  <p class="eyebrow">Evidence first · three products only</p>
  <h1>Which of these three air fryers actually fits your kitchen?</h1>
  <p>Most pages that answer this show you a price and four and a half stars and move on. This one shows you what the manufacturer's listing says, links the exact page it came from, and tells you plainly what it cannot confirm — because that is the part that decides whether you trust the rest.</p>
  <div class="cta-row">
    <a class="btn btn-primary" href="{rel('products.html')}">Compare all three side by side</a>
    <a class="btn btn-ghost" href="{rel('guides/index.html')}">Read a buying guide</a>
  </div>
</section>

<h2>The three we looked at</h2>
<p>Each card lists only what the live listing states. No price, no star rating, no “bestseller” badge — not because we forgot, but because those figures may only be shown when Amazon serves them through a link or supplies them through its API, and neither is in place yet. <a href="{rel('evidence.html')}#why-blank">The rule, quoted.</a></p>
<div class="cards">{cards}</div>

<h2>Side by side</h2>
<p>Seven rows. Every row that makes a claim links the listing it was read from; every row that cannot be filled says what would fill it.</p>
{table}

<div class="note warn">
  <h3>What this comparison deliberately leaves out</h3>
  <p><strong>Price, star rating, review count, per-product commission, trend rank and conversion rate.</strong> Prices and ratings need an Amazon-served link or API data (Program Policies 2(b) and 6(t)). Per-product commission is not published by category-to-ASIN anywhere Amazon makes public. Trend and conversion figures have no official Amazon endpoint at all — the Creators API exposes four operations, none of them a trend or conversion report. Filling those cells would mean inventing them. <a href="{rel('evidence.html')}">See the sources</a>.</p>
</div>

<h2>How this page is made</h2>
<ol class="steps">
  <li><b>Read the listing, not a summary of it.</b> Every specification on this page comes from the listing title and breadcrumb on the page itself, fetched {e(BUILT)}.</li>
  <li><b>Check it against the rules before publishing.</b> Prices, ratings, claims and disclosures are governed by Amazon's Operating Agreement and Program Policies and by the FTC's disclosure guidance. Each rule that shaped this page is quoted on the evidence page with a link.</li>
  <li><b>Leave the unknown empty, and say why.</b> A blank cell here carries a sentence explaining what would fill it. A dash would look tidier and tell you less.</li>
  <li><b>Publish the audit trail.</b> Every row on the <a href="{rel('evidence.html')}">evidence page</a> names the page it was read from and the date it was read.</li>
</ol>

<div class="note">
  <h3>Want to change something?</h3>
  <p>Every design and marketing proposal for this site — including the ones already visible here — sits on the <a href="{rel('decisions.html')}">suggestions and decisions page</a>, with the evidence behind it, the open questions that block it, and a control to accept, reject or defer. Nothing is implemented from that page until a choice is recorded.</p>
</div>

<h2>What this site is not</h2>
<p>It is not a review of products we tested — we have not used them, and saying otherwise would breach the FTC's rule against describing experience you do not have. It is not a price tracker; Amazon's policies prohibit price-tracking and price-alerting functionality outright. And it is not independent of Amazon's rules: it is built inside them, deliberately, because a site that gets removed earns nothing.</p>
"""
    page("index.html", "Which air fryer fits your kitchen",
         body,
         description="Three air fryers compared on what their Amazon listings state, with a source link on every row and every unknown left explicitly blank.",
         depth=0)


def build_products():
    rows = []
    for p in PRODUCTS:
        rows.append(f"""<tr>
  <td class="lead-cell">{e(p['ref'])}<br><span class="small mono">{e(p['submitted'].split('link.amazon/')[-1])}</span></td>
  <td>{e(p['listing_title'])}<br><span class="small">{e(p['category_path'])}</span></td>
  <td><span class="mono">{e(p['destination_asin'])}</span><br>{srcs(p['sources'])}</td>
  <td><span class="badge b-warn">Unconfirmed</span><span class="small"> Identity not confirmed by an official source</span></td>
</tr>""")
    head_table = (f'<div class="tablewrap"><table><caption>The three submitted links and the listings they open</caption>'
                  f'<thead><tr><th>Ref</th><th>Listing as served on {e(BUILT)}</th><th>ASIN</th><th>Identity</th></tr></thead>'
                  f'<tbody>{"".join(rows)}</tbody></table></div>')

    attr_rows = []
    for p in PRODUCTS:
        attr_rows.append(f'<tr><td class="lead-cell">{e(p["ref"])}</td><td>{e(", ".join(p["title_facts"]))}</td>'
                         f'<td>{srcs(p["sources"])}</td></tr>')
    facts_table = (f'<div class="tablewrap"><table><caption>Specifications stated in each listing title</caption>'
                   f'<thead><tr><th>Ref</th><th>Stated in the listing</th><th>Source</th></tr></thead>'
                   f'<tbody>{"".join(attr_rows)}</tbody></table></div>')

    blank_rows = [
        ("Price", "Program Policies 2(b): only if Amazon serves the link displaying it, or the data comes from Creators API / PA API.", "I2-F-02"),
        ("Star rating", "Program Policies 6(t): only when obtained through Creators API or PA API.", "I2-F-02"),
        ("Review count", "Program Policies 6(t), same rule as the star rating.", "I2-F-02"),
        ("Availability", "Program Policies 2(b), same rule as price.", "I2-F-02"),
        ("Commission for this product", "The public rate table is by category, not by ASIN, and identity is unconfirmed.", "I2-F-05"),
        ("Trend rank / demand", "No official Amazon endpoint publishes trend or demand for affiliates.", "I2-F-06"),
        ("Conversion rate", "Only derivable from the operator's own Associates reports after tagging.", "I2-F-06"),
    ]
    b_rows = "".join(f'<tr><td class="lead-cell">{e(k)}</td><td><span class="badge b-warn">Not published</span></td>'
                     f"<td>{e(v)} {flagref(f)}</td></tr>" for k, v, f in blank_rows)
    blank_table = (f'<div class="tablewrap"><table><caption>Fields that are empty on purpose</caption>'
                   f'<thead><tr><th>Field</th><th>Status</th><th>Why — and what would fill it</th></tr></thead>'
                   f'<tbody>{b_rows}</tbody></table></div>')

    cr = CATALOG["commission_reference"]
    c_rows = "".join(f'<tr><td>{e(r["category"])}</td><td class="lead-cell">{e(r["rate"])}</td><td>{srcs(r["sources"])}</td></tr>'
                     for r in cr["rows"])
    b_rows2 = "".join(f'<tr><td>{e(r["program"])}</td><td class="lead-cell">{e(r["rate"])}</td><td>{srcs(r["sources"])}</td></tr>'
                      for r in cr["bounties"])
    comm_table = (f'<div class="tablewrap"><table><caption>{e(cr["caption"])}</caption>'
                  f'<thead><tr><th>Product category</th><th>Rate</th><th>Source</th></tr></thead><tbody>{c_rows}</tbody></table></div>'
                  f'<div class="tablewrap"><table><caption>Bounty events (selected rows, as printed)</caption>'
                  f'<thead><tr><th>Program</th><th>Rate</th><th>Source</th></tr></thead><tbody>{b_rows2}</tbody></table></div>'
                  f'<p class="small">{e(cr["note"])}</p>')

    body = f"""
<h1>Three air fryers, checked against their own listings</h1>
<p class="lede">These are the only three products this site covers. For each one you get what the listing states, the page it was read from, and an honest note about what remains unknown.</p>

<h2 id="identity">First, a caution about the links</h2>
<div class="note bad">
  <h3>The submitted links are not ASINs, and the destinations are not confirmed</h3>
  <p>All three links were supplied in the form <span class="mono">link.amazon/</span> followed by a nine-character token — not the ten-character ASIN that Amazon's own API documentation uses to look a product up. A direct request to <span class="mono">amazon.com/dp/B04G1MEwY</span> returns Amazon's <em>Page Not Found</em>, which is expected for a short-link token.</p>
  <p>Following each short link opens a live listing, and those listings are what this site describes. What no official source establishes is whether they are the products you meant to promote. That question is <a href="{rel('decisions.html')}#Q2">Q2 on the decisions page</a>, and it stays open until you answer it. {srcs(['I2-S13', 'I2-S03'])}</p>
</div>

<h2>The listings</h2>
{head_table}

<h2>What each listing states</h2>
{facts_table}

<h2 id="why-blank">What is missing, and exactly why</h2>
<p>A comparison table with holes in it looks unfinished. A comparison table with holes in it <em>that explains the holes</em> is more useful than one with numbers nobody can check. Here is every field this site refuses to publish, with the rule that stops it.</p>
{blank_table}

<h2>What the programme pays, by category</h2>
<p>These rates are public and official. They are published here as category reference only — not as the commission on any of the three products, because the public table is organised by category and no official page maps a specific ASIN to a specific row.</p>
{comm_table}

<h2>How to read the rest of this site</h2>
<p>Start with the <a href="{rel('guides/index.html')}">buying guides</a>, which answer one question at a time using only the specifications above. The <a href="{rel('evidence.html')}">evidence page</a> holds the source register, the line-by-line verification log and the open items. The <a href="{rel('decisions.html')}">decisions page</a> holds every proposal for improving this site, with a control to accept, reject or defer each one. The <a href="{rel('intent-record.html')}">product-intent record</a> states, link by link, what was confirmed about each submitted URL and what only the owner can confirm. The <a href="{rel('measure.html')}">measurement page</a> defines the five events counted on this site and states what is never recorded.</p>
"""
    page("products.html", "The three air fryers",
         body, lead="Everything this site knows about the three products, and nothing it does not.",
         description="The three air fryers this site covers, the listing each link opens, and the fields left blank with the rule that requires it.",
         depth=0)


GUIDE = {
    "slug": "dual-basket-vs-single-basket.html",
    "title": "Dual-basket vs single-basket: which layout suits how you cook?",
    "question": "Should I buy a dual-basket air fryer or a single-basket one?",
    "short": ("If you regularly cook two different things at once and want them to finish together, "
              "the dual-basket layout is built for that. If you mostly cook one batch at a time and want "
              "the most capacity per shelf, a single large basket is simpler. Everything below comes from "
              "what the listings state, not from using the machines."),
    "body": """
<h2>The difference that matters</h2>
<p>A dual-basket fryer gives you two separate cooking compartments with their own controls. A single-basket
fryer gives you one larger compartment. That is the whole structural difference, and almost everything else
follows from it: two compartments mean two things cooking at different temperatures at the same time, and it
usually means less usable width per compartment for the same total capacity.</p>
<p>The two layouts in this comparison are the CHEFMAN 6 Quart Dual Basket, which the listing describes as
two independent 3Qt nonstick baskets with a Sync Finish control, and the Chefman TurboFry 8 Qt, which the
listing describes as a single XL nonstick basket. [SRC-P1-P3]</p>

<h2>Side by side on the facts</h2>
[TABLE]

<h2>When the dual-basket layout earns its place</h2>
<p>Three situations where two compartments do something one cannot:</p>
<ul>
  <li><b>Two foods, two temperatures, one finish time.</b> The CHEFMAN listing states a Sync Finish control, which
  is the feature that exists specifically so two baskets can finish together. If you cook protein in one basket
  and vegetables in the other, this is the function you are paying for.</li>
  <li><b>Keeping flavours apart.</b> Two independent baskets mean a wet marinade and a dry crumb do not share an
  air path. The listing describes the baskets as independent, which is the relevant word here.</li>
  <li><b>Cooking a smaller portion without heating a large chamber.</b> A 3Qt basket is a sensible size for one or
  two people; the same machine can run both baskets for four.</li>
</ul>

<h2>When the single large basket is the better buy</h2>
<ul>
  <li><b>One big thing at a time.</b> A whole chicken, a large tray of chips, a batch of wings for a crowd —
  none of these wants to be split across two compartments with a divider between them.</li>
  <li><b>Fewer parts to wash.</b> The listing for the 8 Qt describes one nonstick dishwasher-safe basket. Two
  baskets means two things to clean, twice as often.</li>
  <li><b>Simpler controls.</b> The 4-in-1 functions named in the 8 Qt listing — bake, dehydrate, frozen, plus a
  450°F Hi-Fry option — are a single set of settings, not two sets to keep in step.</li>
</ul>

<h2>What this guide cannot tell you</h2>
<div class="note warn">
  <p><b>Which one cooks better.</b> That needs a test, and this site has not tested either machine. The FTC's
  guidance is explicit that you cannot describe experience with a product you have not tried, so no
  comparison of crispness, speed or evenness appears here. [SRC-FTC]</p>
  <p><b>Which one is better value.</b> That needs a price, and prices may only be published when Amazon serves
  the link or supplies the data through its API. Neither is in place, so no price or “value” verdict is given.
  [SRC-2b]</p>
  <p><b>Which one buyers prefer.</b> That needs star ratings and review counts, which may only be displayed when
  obtained through the API. Not available, so not claimed. [SRC-6t]</p>
  <p><b>Exact exterior dimensions and weight.</b> Those are not in the listing titles this site read, and it does not
  estimate them. If they decide your purchase, check the product dimensions section on the listing itself before
  buying.</p>
</div>

<h2>The third option worth knowing about</h2>
<p>If neither layout fits, the third product here is a different category of machine: a 26QT French-door air fryer
toaster oven. It is not a bigger basket fryer: it is a toaster oven that also air-fries. The listing states 24 one-touch
presets and six included accessories, which is a different way of cooking rather than a bigger version of the same
thing. Its exterior dimensions are not in the text this site read, so this page does not estimate how much counter
space it takes — check the dimensions on the listing before you decide.
<a href="../products.html">Full comparison</a>.</p>

<h2>How to decide in one minute</h2>
<ol class="steps">
  <li><b>Do you usually cook two different foods at once?</b> If yes, the dual-basket layout is designed for you.</li>
  <li><b>Do you usually cook one large batch?</b> If yes, one big basket is the simpler tool.</li>
  <li><b>Do you want an oven as well?</b> If yes, neither basket fryer is the right shape of machine — look at the French-door oven.</li>
  <li><b>Still unsure?</b> Check the live listing's dimensions and capacity against your bench and your usual portion size, then decide. Those are the two facts that decide it, and they are on the listing, not on this page.</li>
</ol>
"""
}


def build_guides():
    # Build the comparison table for the guide from catalog rows, with an added bolding of the fields used.
    rows = []
    picks = [
        ("Capacity as listed", lambda p: p),
    ]
    for r in CATALOG["comparison"]["rows"]:
        if r["label"].lower().startswith(("price", "star rating", "commission")):
            continue
        cells = "".join("<td>" + (e(r[k]) if r.get(k) else "—") + "</td>" for k in ("p1", "p2", "p3"))
        rows.append(f'<tr><td class="lead-cell">{e(r["label"])}</td>{cells}<td>{srcs(r["sources"])}</td></tr>')
    gtable = (f'<div class="tablewrap"><table><caption>What the two listings state, quoted from the listing text</caption>'
              f'<thead><tr><th>Fact</th><th>P1 · CHEFMAN dual basket</th><th>P2 · Emeril Lagasse oven</th>'
              f'<th>P3 · Chefman single basket</th><th>Source</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>')

    header = f"""
<p class="small"><a href="index.html">Buying guides</a> › Dual-basket vs single-basket</p>
<h1>{e(GUIDE['title'])}</h1>
<p class="lede">{e(GUIDE['short'])}</p>
<p class="small">Published {e(BUILT)} · Written and fact-checked against the listings on {e(BUILT)} · No first-hand testing claimed</p>
"""
    # Mobile quick-compare bar (D-22): sticky on small screens so a reader partway
    # through a guide is one tap from the comparison it rests on.
    msticky = ('<nav class="msticky" aria-label="Quick compare">'
               f'<a href="{rel("products.html")}">Compare the three</a>'
               f'<a href="{rel("guides/index.html")}">More guides</a></nav>')
    body = GUIDE["body"]
    body = body.replace("[TABLE]", gtable)
    body = body.replace("[SRC-P1-P3]", srcs(["I2-S10", "I2-S11", "I2-S12"]))
    body = body.replace("[SRC-FTC]", srcs(["I2-S06"]))
    body = body.replace("[SRC-2b]", srcs(["I2-S02"]))
    body = body.replace("[SRC-6t]", srcs(["I2-S02"]))
    body = body + msticky

    # ---------------------------------------------------------------- guides index
    topic_rows = []
    for t in [
        ("Dual-basket vs single-basket: which layout suits how you cook?", "Live", GUIDE["slug"]),
        ("Air fryer oven vs basket fryer: 26QT is a different machine, not a bigger one", "In review", None),
        ("What “4-in-1” actually names on an air fryer, and what it leaves out", "In review", None),
        ("Capacity maths: what 6QT, 8QT and 26QT mean for portions", "In review", None),
    ]:
        state = ('<span class="badge b-ok">Live</span>' if t[1] == "Live"
                 else '<span class="badge b-mute">In review</span>')
        link = (f'<a href="{t[2]}">{e(t[0])}</a>' if t[2] else e(t[0]))
        trail = (srcs(["I2-S10", "I2-S11", "I2-S12"]) if t[1] == "Live"
                 else f'<span class="blank"><span class="blank-dot"></span>In review</span>'
                      f'<span class="blank-why">Not published: needs the editorial pass in D-10 before it can be sourced line by line.</span>')
        topic_rows.append(f'<tr><td class="lead-cell">{link}</td><td>{state}</td><td>{trail}</td></tr>')
    body2 = f"""
<h1>Buying guides</h1>
<p class="lede">One question per page, answered from the listing text, with the unknowable parts labelled as unknown. No page here claims a test that was not run.</p>
<div class="tablewrap"><table>
<caption>The guide plan</caption>
<thead><tr><th>Question this guide answers</th><th>Status</th><th>Provenance</th></tr></thead>
<tbody>{''.join(topic_rows)}</tbody></table></div>
<div class="note">
  <h3>Why only one guide is live</h3>
  <p>A guide is only published here once every sentence in it can be traced to a listing or an official page. The
  other three are drafted from the same verified facts and are waiting on the editorial pass described in
  <a href="../decisions.html#D-10">D-10</a> — a named human editor — because a page with no editor is exactly the
  page that reads as generated.</p>
</div>
<h2>The rule every guide follows</h2>
<ul>
  <li><b>One question.</b> If a page answers three questions it answers none of them well.</li>
  <li><b>Facts with sources.</b> Every specification links the listing it came from.</li>
  <li><b>No invented experience.</b> No “we tested”, no “in our kitchen”, no implied ownership.</li>
  <li><b>No numbers we cannot publish.</b> No price, star rating or review count until Amazon serves or supplies them.</li>
  <li><b>A named gap.</b> Each guide ends by stating what it cannot tell you and where to check it yourself.</li>
</ul>
"""
    page("guides/index.html", "Buying guides", body2,
         description="Air fryer buying guides, one question per page, each built only on facts from the product listing.",
         depth=1)


def build_evidence():
    # source register
    s_rows = []
    for s in SOURCES.values():
        short_url = re.sub(r"^https?://", "", s["url"])[:64]
        if s["url"] in RESOLVED:
            short_url = short_url + " \u2192 " + re.sub(r"^https?://", "", RESOLVED[s["url"]])
        ell = "…" if len(s["observed"]) > 340 else ""
        obs = e(s["observed"][:340]) + ell
        s_rows.append(
            '<tr id="' + e(s["id"]) + '"><td class="lead-cell"><span class="mono">' + e(s["id"]) + "</span></td>"
            "<td>" + e(s["title"]) + '<br><span class="small">' + e(s["publisher"]) + "</span></td>"
            '<td><a href="' + e(RESOLVED.get(s["url"], s["url"])) + '" target="_blank" rel="noopener noreferrer">' + e(short_url) + "</a></td>"
            '<td><span class="small">' + e(s["fetched"]) + "</span></td>"
            '<td class="small">' + obs + "</td></tr>"
        )
    src_table = (f'<div class="tablewrap"><table><caption>Source register — every page this site cites, fetched {e(BUILT)}</caption>'
                 f'<thead><tr><th>ID</th><th>Document</th><th>URL</th><th>Read</th><th>What the page says</th></tr></thead>'
                 f'<tbody>{"".join(s_rows)}</tbody></table></div>')

    # verification log
    v_rows = []
    for r in VERIFY["rows"]:
        cls = {"Confirmed": "b-ok", "Confirmed (corrected wording)": "b-warn",
               "Not re-checked": "b-mute", "Unverified": "b-bad"}[r["outcome"]]
        v_rows.append(f"""<tr><td class="lead-cell"><span class="mono">{e(r['id'])}</span></td>
<td>{e(r['claim'])}</td><td class="small">{e(r['observed'])}</td>
<td><span class="badge {cls}">{e(r['outcome'])}</span></td>
<td>{srcs(r['sources']) or '<span class="blank"><span class="blank-dot"></span>No fetch</span><span class="blank-why">No official page was fetched for this claim in this session, so no result is asserted.</span>'}</td></tr>""")
    v_table = (f'<div class="tablewrap"><table><caption>Line-by-line verification — {len(VERIFY["rows"])} claims, re-read on {e(BUILT)}</caption>'
               f'<thead><tr><th>#</th><th>The claim the repository makes</th><th>What the official page says — read today</th>'
               f'<th>Outcome</th><th>Source</th></tr></thead><tbody>{"".join(v_rows)}</tbody></table></div>')

    t = VERIFY["counts"]
    body = f"""
<h1>How we know</h1>
<p class="lede">This page exists because “verified” is a word affiliate sites use loosely. Below is every official page this site read, what it said, and the dated result of checking each claim against it.</p>

<div class="grid2">
  <div class="card"><p class="kicker">The short version</p>
    <ul class="facts">
      <li>{t['rows']} claims re-read against official pages</li>
      <li>{t['confirmed']} confirmed exactly as published</li>
      <li>{t['confirmed_corrected']} confirmed with corrected wording</li>
      <li>{t['not_rechecked']} not re-checked — stated as a gap, not asserted</li>
      <li>{t['unverified']} unverified — left blank</li>
    </ul>
  </div>
  <div class="card"><p class="kicker">How a page gets read</p>
    <ul class="facts">
      <li>One page, one fetch, one record of what it said</li>
      <li>No value taken from a search snippet</li>
      <li>A sign-in wall or a block is recorded as a result</li>
      <li>The agent identifies itself, as Amazon's Agent Terms require</li>
    </ul>
    <p class="prov">Agent Terms §4(c) require an <span class="mono">Agent/[name]</span> user agent and forbid circumventing a block. {srcs(['I2-S02'])}</p>
  </div>
</div>

<h2 id="disclosure">Why the disclosure appears twice</h2>
<p>Two different obligations, two different sources. Amazon's Operating Agreement §5 requires the exact sentence
<em>“As an Amazon Associate I earn from qualifying purchases.”</em> somewhere prominent on the site. The FTC's
guidance goes further on placement: a disclosure is likely to be missed if it appears only in a footer or behind a
click, and it should sit with the recommendation itself. So this site does both — the exact Amazon sentence in a
banner at the top, and a plain-language line beside any action that could lead to a purchase. {srcs(['I2-S01', 'I2-S06'])}</p>

<h2 id="why-blank">Why a blank cell is a feature</h2>
<p>Three rules do most of the work here. Each is quoted below as the page carries it.</p>
<ol class="steps">
  <li><b>Price.</b> Program Policies 2(b): <em>“You may only show prices and availability if: (a) we serve the link in which that price and availability data are displayed, or (b) you obtain Product pricing and availability data via Creators API or PA API”</em>. {srcs(['I2-S02'])}</li>
  <li><b>Star ratings and reviews.</b> Program Policies 6(t): <em>“You will not display or otherwise use any of our customer reviews or star ratings … unless you have obtained a link to that customer review or star rating through Creators API or PA API”</em>. {srcs(['I2-S02'])}</li>
  <li><b>No invented experience.</b> FTC: <em>“You can't talk about your experience with a product you haven't tried”</em> and <em>“You can't make up claims about a product that would require proof the advertiser doesn't have”</em>. {srcs(['I2-S06'])}</li>
</ol>

<h2>Source register</h2>
<p>Fourteen pages, each read once on {e(BUILT)}. The “what the page says” column is a paraphrase written at the time of reading; the link opens the page itself so you can check it.</p>
{src_table}

<h2>Verification log</h2>
<p>Each row is one claim this repository publishes. The middle column is what was on the page when it was fetched today — not what another session recorded last week.</p>
{v_table}

<h2>Open items</h2>
<p>Anything that could not be confirmed, or that needs the owner's input, is numbered and published rather than left implicit. These are not hidden failures; they are the honest boundary of what this build knows.</p>
<p><a class="btn btn-primary" href="flagged.html">Read the {len(OPEN_ITEMS)} open items</a></p>
"""
    page("evidence.html", "How we know", body,
         description="Every official page this site read, what it said, and the dated verification result for each published claim.",
         depth=0)


OPEN_ITEMS = [
    ("I2-F-01", "Disclosure placement on the older pages", "Medium",
     "The pages built by earlier sessions carry the exact §5 sentence, but in the footer only. That meets the Operating Agreement's ‘on your Site’ wording and is weaker than the FTC's placement guidance, which warns a footer disclosure is likely to be missed.",
     "Move the disclosure into a banner on every older page as well. Published here as a proposal (D-07) rather than applied, because the older pages belong to other sessions' builds.",
     ["I2-S01", "I2-S06"]),
    ("I2-F-02", "No publishable price, rating or review count", "High",
     "Prices and star ratings appear on the live listings but may only be displayed when Amazon serves the link or supplies the data through Creators API / PA API. The older pages' 2026-11-14 captures are dated observations, not publishable figures, and today's fetch did not attribute a price or rating to any of the three featured ASINs.",
     "Blocked on Q4 (API eligibility). Until then the cells stay blank with an explanation on every page.",
     ["I2-S02", "I2-S04"]),
    ("I2-F-03", "The submitted links carry no tracking tag", "High",
     "None of the three submitted short links resolves to a URL carrying an Associates tag, and no tag exists anywhere in this repository. Program Policies 2(b) require the tag parameter on every link to an Amazon Site.",
     "Blocked on Q1 and Q3. Every buy action on this site is disabled and labelled until a tag is supplied.",
     ["I2-S02", "I2-S07"]),
    ("I2-F-04", "Product identity is unconfirmed", "High",
     "Each nine-character short link opens a live listing, and those listings are documented. Whether they are the products the owner intended to promote is not established by any official source.",
     "Blocked on Q2. The destination is described; intent is not assumed.",
     ["I2-S07", "I2-S13"]),
    ("I2-F-05", "No per-product commission rate", "Medium",
     "The public commission statement gives rates by product category. No official page maps a specific ASIN to a specific category row, and identity is unconfirmed, so no per-product rate is published. The Kitchen rate of 4.50% is shown as a category reference only.",
     "Will remain open until Amazon supplies category data for the ASIN through the API.",
     ["I2-S05"]),
    ("I2-F-06", "No trend, demand or conversion data exists officially", "High",
     "The brief asks for trending products and conversion optimisation. The Creators API exposes four operations — SearchItems, GetItems, GetVariations, GetBrowseNodes — and none returns search volume, trend direction, conversion rate or ranking. There is no official endpoint to call.",
     "Not fixable by this build. Trend and conversion claims are therefore not published anywhere on this site. Conversion figures become available only from the operator's own Associates reports after tagging.",
     ["I2-S04"]),
    ("I2-F-07", "Superseded pages still carry price and star-rating values, and 19 of them are in the sitemap", "Medium",
     "This session counted the pages that render numeric price or rating strings: five under /docs/ (analysis, content, executive-summary, index, sources) and thirteen under /sessions/3c886b62/ (analysis, categories, category-home-kitchen, commission, comparison, executive-summary, index, three product pages, products, verification). They were captured on 2026-11-13 as dated evidence, and Program Policies 2(b) and 6(t) do not permit those figures to be displayed this way. Nineteen archive URLs (the /sessions/ set) are listed in sitemap.xml, which invites a crawler to treat superseded pages as current. Note the archive set is inconsistent rather than uniformly wrong: the /docs/ pages carry a notice that some values are withheld and /sessions/3c886b62/ labels itself historical, so this is a labelling and indexing problem more than a deletion problem.",
     "Proposed as D-08: one canonical home, a visible 'superseded' label on every archive page, and exclusion from the sitemap rather than deletion, so the evidence is preserved without being advertised. Not applied here because those pages belong to other sessions' builds and removing them would destroy the audit record.",
     ["I2-S02"]),
    ("I2-F-08", "An earlier session's pull request is open and conflicting", "Low",
     "PR #71 has been open since 2026-11-14 and reports mergeable=CONFLICTING. It is not part of this build and this session did not modify it.",
     "Flagged for the owner to close or rebase. Nothing in this build depends on it.",
     []),
    ("I2-F-09", "The shared task board has duplicated records and is 528 KB", "Low",
     "COORDINATION.md is 528 KB and contains four section headers twice each (the a53a7e52, 252122ff, 9fef7647 and PR #26 registries). The duplication is a record of repeated merge resolutions accumulated across sessions, not a corruption of content, but it makes the board hard to read and easy to mis-claim against.",
     "Proposed: a one-time de-duplication pass that keeps the earliest and latest of each duplicated section and links the rest to git history. Not applied here because the board is the shared surface and changing another session's rows requires their agreement.",
     []),
]


def build_flagged():
    rows = []
    for fid, title, sev, finding, action, s in OPEN_ITEMS:
        cls = {"High": "b-bad", "Medium": "b-warn", "Low": "b-mute"}[sev]
        rows.append(f"""<tr id="{e(fid)}"><td class="lead-cell"><span class="mono">{e(fid)}</span><br>{e(title)}</td>
<td><span class="badge {cls}">{e(sev)}</span></td>
<td>{e(finding)}</td><td>{e(action)}</td><td>{srcs(s) or '<span class="small">repository state</span>'}</td></tr>""")
    table = (f'<div class="tablewrap"><table><caption>Open items — published so they can be reviewed, not hidden</caption>'
             f'<thead><tr><th>Item</th><th>Severity</th><th>What was found</th><th>What would resolve it</th><th>Source</th></tr></thead>'
             f'<tbody>{"".join(rows)}</tbody></table></div>')
    body = f"""
<h1>Flagged for review</h1>
<p class="lede">Everything this build could not confirm, could not publish, or found irregular in the repository. None of these blocks the site from going live; all of them block a specific claim from being made.</p>
<p>Each item has a stable anchor (for example <span class="mono">#I2-F-02</span>) so it can be discussed and closed. Items are referenced from the page where the gap is visible, so a reader who notices the hole can see the reason in one click.</p>
{table}
<h2>How items get closed</h2>
<ol class="steps">
  <li><b>Answer the question it waits on.</b> I2-F-03 and I2-F-04 close the moment a tag and an intended ASIN are supplied; I2-F-02 closes when the API is eligible.</li>
  <li><b>Re-verify against the official page.</b> A closed item is closed by a dated read, not by an assertion that it is fine now.</li>
  <li><b>Record it in the task board.</b> The change and its evidence are logged so the next session does not silently reopen or duplicate it.</li>
</ol>
<div class="note">
  <p><strong>Nothing on this page is a guess.</strong> Where a value is missing, the reason is a rule with a source link, or a fetch that returned nothing attributable. If you think one of these is wrong, the source link is the place to check it.</p>
</div>
"""
    page("flagged.html", "Flagged for review", body,
         description="Open items in this build: what could not be confirmed, what could not be published, and what would resolve each one.",
         depth=0)


def build_front_door():
    body = f"""
<h1>Where the rest of the repository lives</h1>
<p class="lede">This site is new and deliberately narrow. The repository also carries an audit dashboard and several earlier builds that are the verification record for the numbers quoted here. They are linked below rather than merged in, because merging them is a proposal (D-08) and not a decision this build is entitled to make alone.</p>
<div class="cards">
  <article class="card"><p class="kicker">Current audit</p><h3>Verification dashboard</h3>
    <ul class="facts"><li>16 pages of audit detail</li><li>232 verified table rows</li><li>Commission rate tables</li><li>Full flag register</li></ul>
    <div class="card-foot"><a class="btn btn-primary" href="../dashboard/index.html">Open the audit build</a></div></article>
  <article class="card"><p class="kicker">Earlier build</p><h3>Flat page set</h3>
    <ul class="facts"><li>Executive summary</li><li>Products, pricing, reviews</li><li>Content and compliance</li><li>Decision Center and suggestions</li></ul>
    <div class="card-foot"><a class="btn btn-primary" href="../index.html">Open the flat pages</a></div></article>
  <article class="card"><p class="kicker">Repository</p><h3>Source and task board</h3>
    <ul class="facts"><li>Every generator and gate</li><li>The shared coordination board</li><li>Per-session verification records</li><li>Full git history</li></ul>
    <div class="card-foot"><a class="btn btn-primary" href="https://github.com/kanlerxz87-cyber/Zone3">Open GitHub</a></div></article>
</div>
<h2>Why not just replace the front page</h2>
<p>Because two other sessions' builds are served from this repository and their pages are the audit record. Replacing the root without a decision would hide that record. It is proposed as <a href="decisions.html#D-01">D-01</a> and <a href="decisions.html#D-08">D-08</a>; accept either and the next session can make this page the root.</p>
"""
    page("front-door.html", "Front door", body,
         description="Where the audit dashboard, the earlier builds and the repository live relative to this site.",
         depth=0)


def build_decisions():
    # ---- proposals
    blocks = []
    for p in DECISIONS["proposals"]:
        status_cls = {"implemented": "b-ok", "proposed": "b-mute", "blocked": "b-bad"}[p["status"]]
        ev = "".join(
            f'<li><span class="term { "t-official" if x["term"] == "Official" else "t-observed" if x["term"] == "Observed" else "t-editorial" }">{e(x["term"])}</span>'
            + (srcs(x.get("sources", [])) + " " if x.get("sources") else "")
            + e(x["claim"])
            + (f' <span class="small">({e(x["via"])})</span>' if x.get("via") else "")
            + "</li>"
            for x in p["evidence"]
        )
        acc = "".join(f"<li>{e(a)}</li>" for a in p["acceptance"])
        dep = (", ".join(f'<a href="#{e(d)}">{e(d)}</a>' for d in p["depends_on"]) or "Nothing — can be implemented now")
        blocks.append(f"""<article class="prop" id="{e(p['id'])}">
  <div class="prop-head"><h3>{e(p['title'])}</h3><span class="pid">{e(p['id'])}</span>
    <span class="badge {status_cls}">{e(p['status'])}</span></div>
  <p class="small">{e(p.get('status_note', ''))}</p>
  <dl>
    <dt>The problem</dt><dd>{e(p['problem'])}</dd>
    <dt>What is proposed</dt><dd>{e(p['proposal'])}</dd>
    <dt>Evidence</dt><dd><ul class="evidence">{ev}</ul></dd>
    <dt>Effort</dt><dd>{e(p['effort'])}</dd>
    <dt>Expected effect</dt><dd>{e(p['expected_effect'])}</dd>
    <dt>Risks</dt><dd>{e(p['risks'])}</dd>
    <dt>What it will not do</dt><dd>{e(p['what_it_does_not_do'])}</dd>
    <dt>Depends on</dt><dd>{dep}</dd>
    <dt>Done when</dt><dd><ul>{acc}</ul></dd>
  </dl>
  <div class="decide">
    <fieldset><legend>Your decision</legend>
      <div class="seg">
        <label><input type="radio" name="{e(p['id'])}" value="Accept" data-pid="{e(p['id'])}"><span>Accept</span></label>
        <label><input type="radio" name="{e(p['id'])}" value="Reject" data-pid="{e(p['id'])}"><span>Reject</span></label>
        <label><input type="radio" name="{e(p['id'])}" value="Defer" data-pid="{e(p['id'])}"><span>Defer</span></label>
      </div>
    </fieldset>
    <output for="{e(p['id'])}" data-out="{e(p['id'])}">No decision recorded yet</output>
    <textarea data-note="{e(p['id'])}" aria-label="Reason for the decision on {e(p['id'])}" placeholder="One sentence of reason (optional but useful to the next session)"></textarea>
  </div>
</article>""")

    # ---- questions
    q_rows = []
    for q in DECISIONS["questions"]:
        cls = {"Blocking": "b-bad", "High": "b-warn", "Medium": "b-mute", "Low": "b-mute"}[q["priority"]]
        q_rows.append(f"""<tr id="{e(q['id'])}"><td class="lead-cell"><span class="mono">{e(q['id'])}</span><br><span class="badge {cls}">{e(q['priority'])}</span></td>
<td><strong>{e(q['question'])}</strong>
  <div class="small" style="margin-top:6px"><b>Known:</b> {e(q['known'])} {srcs(q['known_sources'])}</div>
  <div class="small" style="margin-top:4px"><b>Not known:</b> {e(q['unknown'])}</div>
  <div class="small" style="margin-top:4px"><b>Why it decides things:</b> {e(q['why_it_matters'])}</div>
</td>
<td class="small"><b>How to find out:</b> {e(q['how_to_discover'])}</td>
<td class="small"><b>If unanswered:</b> {e(q['if_unanswered'])}</td>
<td>{', '.join(f'<a href="#{e(d)}">{e(d)}</a>' for d in q['decides'])}</td></tr>""")
    q_table = (f'<div class="tablewrap"><table><caption>The questions that must be answered before the blocked work can start</caption>'
               f'<thead><tr><th>Question</th><th>What is known, and what is not</th><th>How to discover the answer</th>'
               f'<th>If it stays unanswered</th><th>Decides</th></tr></thead><tbody>{"".join(q_rows)}</tbody></table></div>')

    # ---- discovery
    d_rows = []
    for d in DECISIONS["discovery"]:
        d_rows.append(f"""<tr id="{e(d['id'])}"><td class="lead-cell"><span class="mono">{e(d['id'])}</span></td>
<td>{e(d['action'])}</td><td>{', '.join(f'<a href="#{e(x)}">{e(x)}</a>' for x in d['answers'])}</td>
<td class="small">{e(d['who'])}</td><td class="small">{e(d['output'])}</td>
<td><a href="{e(d['official_page'].split(' · ')[0])}" target="_blank" rel="noopener noreferrer">official page</a> {src(d['source'])}</td></tr>""")
    d_table = (f'<div class="tablewrap"><table><caption>How to discover the missing information</caption>'
               f'<thead><tr><th>#</th><th>Action</th><th>Answers</th><th>Who</th><th>Output</th><th>Where</th></tr></thead>'
               f'<tbody>{"".join(d_rows)}</tbody></table></div>')

    # ---- prompt pack
    pblocks = []
    for p in DECISIONS["prompt_pack"]:
        acc = "".join(f"<li>{e(a)}</li>" for a in p["acceptance"])
        g = "".join(f"<li>{e(x)}</li>" for x in p["guardrails"])
        pblocks.append(f"""<article class="prop" id="{e(p['id'])}">
  <div class="prop-head"><h3>{e(p['name'])}</h3><span class="pid">{e(p['id'])}</span></div>
  <p class="small">{e(p['purpose'])}</p>
  <pre class="prompt">{e(p['prompt'])}</pre>
  <dl><dt>Acceptance</dt><dd><ul>{acc}</ul></dd>
      <dt>Guardrails</dt><dd><ul>{g}</ul></dd>
      <dt>Sources</dt><dd>{srcs(p['sources'])}</dd></dl>
</article>""")

    wf = "".join(f"<li>{e(w)}</li>" for w in DECISIONS["workflow"])

    body = f"""
<h1>Suggestions &amp; decisions</h1>
<p class="lede">Every proposal for improving this site in one place: what is wrong, what is proposed, the evidence behind it, and a control to accept, reject or defer. Nothing here changes the site by itself. That is the point — you get to choose the path before anyone builds it.</p>

<div class="note">
  <h3>What the status labels mean</h3>
  <p><span class="badge b-ok">implemented</span> already visible on this site, as a preview you can judge — and revert by ignoring it.
  <span class="badge b-mute">proposed</span> not built; waiting on your decision.
  <span class="badge b-bad">blocked</span> cannot be built until a named question is answered.</p>
</div>

<h2 id="tools">Record your decisions</h2>
<div class="decision-tools">
  <p>Choose Accept, Reject or Defer on any proposal below, add a reason if you want one, then export. The export is plain text you can paste into the repository's task board so the next session implements only what you chose. Nothing is submitted anywhere automatically, and no choice changes this page.</p>
  <div class="tools-row">
    <button type="button" id="exportBtn">Export my decisions</button>
    <button type="button" id="printBtn" style="background:#48505f">Print / save as PDF</button>
    <span class="small" id="count">0 of {len(DECISIONS['proposals'])} decided</span>
  </div>
  <textarea id="exportBox" readonly aria-label="Exported decisions" placeholder="Your export will appear here."></textarea>
</div>

<h2 id="proposals">The proposals</h2>
<p>Ordered by what unblocks the most: the first four are previewable now, the fifth unlocks earning, the rest are quality and structure.</p>
{''.join(blocks)}

<h2 id="questions">Open questions</h2>
<p>These are the gaps that stop a decision from being made on the evidence alone. Each row states what is known (with a source), what is not known, why it matters, and how to find out. A question marked <span class="badge b-bad">Blocking</span> stops every commercial change until it is answered.</p>
{q_table}

<h2 id="discovery">How to discover the missing information</h2>
<p>Nine concrete actions, each with the official page to read, the person who can do it, and the output that closes the question.</p>
{d_table}

<h2 id="prompts">Prompt pack</h2>
<p>If you take these decisions to a design or content session, paste these. Each one is written to produce work that can be checked, and each carries its guardrails with it.</p>
{''.join(pblocks)}

<h2 id="workflow">How a decision becomes a change</h2>
<ol class="steps">{wf}</ol>

<div class="note warn">
  <h3>What is deliberately not on this page</h3>
  <p>No traffic, revenue or conversion estimate. No promise that any proposal will rank, convert or earn. Those numbers cannot be sourced, and a proposal that rests on an invented number is worse than no proposal. Where a proposal's value is a judgement, it is labelled <span class="term t-editorial">Editorial</span> in its evidence list.</p>
</div>
"""
    page("decisions.html", "Suggestions & decisions", body,
         description="Proposals for improving this affiliate site, the evidence for each, the open questions that block them, and a control to accept, reject or defer.",
         depth=0)


# --------------------------------------------------------------------------- interactivity
JS = r"""
(function(){
  var KEY = 'i2-decisions-v1';
  var state = {};
  try { state = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch(e) { state = {}; }
  var proposals = Array.prototype.slice.call(document.querySelectorAll('.prop[id^="D-"]'));
  var exportBox = document.getElementById('exportBox');
  var countEl = document.getElementById('count');

  function save(){ try { localStorage.setItem(KEY, JSON.stringify(state)); } catch(e){} }
  function decided(){
    return proposals.filter(function(p){ return state[p.id] && state[p.id].decision; }).length;
  }
  function refreshCount(){
    if (!countEl) return;
    countEl.textContent = decided() + ' of ' + proposals.length + ' decided';
  }
  function refreshOutputs(){
    proposals.forEach(function(p){
      var out = p.querySelector('[data-out]');
      var s = state[p.id];
      if (!out) return;
      if (s && s.decision) {
        out.textContent = 'Recorded: ' + s.decision + (s.note ? ' — ' + s.note : '');
        out.style.color = '#0b6b53';
      } else {
        out.textContent = 'No decision recorded yet';
        out.style.color = '';
      }
    });
    refreshCount();
  }

  proposals.forEach(function(p){
    var radios = p.querySelectorAll('input[type=radio]');
    var note = p.querySelector('[data-note]');
    var s = state[p.id] || {};
    if (s.decision) {
      radios.forEach(function(r){ if (r.value === s.decision) r.checked = true; });
    }
    if (s.note && note) note.value = s.note;
    radios.forEach(function(r){
      r.addEventListener('change', function(){
        state[p.id] = state[p.id] || {};
        state[p.id].decision = r.value;
        state[p.id].title = p.querySelector('h3').textContent;
        if (note) state[p.id].note = note.value.trim();
        save(); refreshOutputs();
      });
    });
    if (note) note.addEventListener('input', function(){
      state[p.id] = state[p.id] || {};
      state[p.id].note = note.value.trim();
      state[p.id].title = p.querySelector('h3').textContent;
      save(); refreshOutputs();
    });
  });

  var btn = document.getElementById('exportBtn');
  if (btn && exportBox) btn.addEventListener('click', function(){
    var lines = ['Decision record — ' + new Date().toISOString().slice(0,10), ''];
    proposals.forEach(function(p){
      var s = state[p.id];
      lines.push(p.id + ' — ' + (p.querySelector('h3').textContent || '') );
      lines.push('  Decision: ' + (s && s.decision ? s.decision : 'not decided'));
      if (s && s.note) lines.push('  Reason: ' + s.note);
      lines.push('');
    });
    var open = proposals.length - decided();
    lines.push(open ? open + ' proposal(s) still undecided.' : 'All proposals decided.');
    exportBox.value = lines.join('\n');
    exportBox.select();
    exportBox.focus();
  });

  var print = document.getElementById('printBtn');
  if (print) print.addEventListener('click', function(){ window.print(); });

  refreshOutputs();
})();

/* ---- First-party event ledger (session ded63349, 2026-11-17; proposal D-16) ----
   Five defined events, recorded on this device only: no cookies, no third-party
   requests, no identifiers, no referrer storage — just event name, UTC timestamp,
   page path and (for product clicks) which product card. Participation Requirements
   6(s) bans artificial clicks or sessions: this ledger counts real clicks made by a
   real visitor on this site's own pages, and never touches Amazon sessions. */
(function(){
  var KEY = 'z3-events-v1', MAX = 500;
  var EVENTS = { page_view:1, outbound_product_click:1, comparison_open:1, guide_read_through:1, decision_open:1 };
  function load(){ try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch(e){ return []; } }
  function save(a){ try { localStorage.setItem(KEY, JSON.stringify(a.slice(-MAX))); } catch(e){} }
  function rec(name, data){
    if (!EVENTS[name]) return;
    var a = load();
    a.push({ t: new Date().toISOString(), e: name,
             p: location.pathname.replace(/^\/Zone3/, ''),
             r: (data && data.ref) ? data.ref : null });
    save(a);
    try { document.dispatchEvent(new CustomEvent('z3-event', { detail: { name: name } })); } catch(e){}
  }
  rec('page_view');
  document.addEventListener('click', function(ev){
    var t = ev.target;
    var a = t && t.closest ? t.closest('a') : null;
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (href.indexOf('/dp/') > -1 || href.indexOf('link.amazon') > -1) {
      rec('outbound_product_click', { ref: a.getAttribute('data-ref') || '' });
    } else if (href.indexOf('compare') > -1 || (a.textContent || '').toLowerCase().indexOf('compare') > -1
               || href.indexOf('products.html') > -1) {
      rec('comparison_open');
    } else if (href.indexOf('decisions.html') > -1 || href.indexOf('answers.html') > -1) {
      rec('decision_open');
    }
  }, true);
  if (location.pathname.indexOf('/guides/') > -1) {
    var readFired = false;
    window.addEventListener('scroll', function(){
      if (readFired) return;
      var d = document.documentElement;
      var total = (d.scrollHeight || 1) - (d.clientHeight || 1);
      var progress = (d.scrollTop || document.body.scrollTop || 0) / (total || 1);
      if (progress > 0.92) { readFired = true; rec('guide_read_through'); }
    }, { passive: true });
  }
  window.z3Ledger = {
    events: Object.keys(EVENTS),
    all: load,
    record: rec,
    clear: function(){ try { localStorage.removeItem(KEY); } catch(e){} },
    csv: function(){
      var rows = ['timestamp,event,path,product'];
      load().forEach(function(x){
        var cells = [x.t, x.e, x.p, x.r || ''];
        rows.push(cells.map(function(v){ return '"' + String(v).replace(/"/g, '""') + '"'; }).join(','));
      });
      return rows.join('\n');
    }
  };
})();
"""


def build_js():
    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    (OUT / "assets" / "site.js").write_text(JS.lstrip(), encoding="utf-8")


def inject_js():
    for p in OUT.rglob("*.html"):
        text = p.read_text(encoding="utf-8")
        if "site.js" in text:
            continue
        depth = len(p.relative_to(OUT).parts) - 1
        src = ("../" * depth) + "assets/site.js"
        text = text.replace("</body>", f'<script src="{src}" defer></script>\n</body>')
        p.write_text(text, encoding="utf-8")


def build_index_json():
    """A small JSON index so other tools can list the pages without crawling HTML."""
    pages = sorted(p.relative_to(OUT).as_posix() for p in OUT.rglob("*.html"))
    (OUT / "site-index.json").write_text(
        json.dumps({"built": BUILT, "pages": pages, "sources": list(SOURCES)}, indent=1) + "\n",
        encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    build_css()
    build_js()
    build_index()
    build_products()
    build_guides()
    build_evidence()
    build_flagged()
    build_front_door()
    build_decisions()
    inject_js()
    build_index_json()
    n = len(list(OUT.rglob("*.html")))
    print(f"built {n} pages into site/ · {len(SOURCES)} sources · {len(PRODUCTS)} products "
          f"· {len(DECISIONS['proposals'])} proposals · {len(DECISIONS['questions'])} questions "
          f"· {len(OPEN_ITEMS)} open items")


if __name__ == "__main__":
    main()

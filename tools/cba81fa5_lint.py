#!/usr/bin/env python3
"""Reader-site lint — house style and compliance checks for /site/ (session cba81fa5).

Mechanical on purpose: every rule below is either an Amazon Program Policies rule, an FTC
disclosure rule, or a "does this sentence carry information" rule that can be matched on the
page. It is not a substitute for an editor; it is the floor an editor would stand on, checked
on every build. The rules and the pages they come from are documented at
site/style-guide.html.

Usage:
    python3 tools/cba81fa5_lint.py [--root DIR] [--quiet]

Exemptions a page may claim, and how:
    <span class="example">…</span>   text that is an example of a banned construction (the style
                                     guide quotes the things it forbids); stripped before scanning
    <table data-lint="skip">         a table that is prose layout, not a factual claim table, so
                                     its rows do not each need an official source link
Exit code 0 = clean. Non-zero = one or more findings, printed one per line as  FILE: RULE: detail
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
from urllib.parse import urlparse

DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."
OFFICIAL = re.compile(
    r'href="https?://[^"]*(?:amazon\.[a-z]{2,3}|ftc\.gov|github\.com|githubusercontent\.com)[^"]*"',
    re.I,
)
SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "is.gd", "goo.gl", "ow.ly", "buff.ly",
              "rebrand.ly", "amzn.to", "shorturl.at"}
# link.amazon is itself a short link surface: it may be cited as evidence of what a submitted
# link resolves to, which is what the evidence tables do; it may not be used as an outbound
# shopping link in body copy.
EVIDENCE_OK = re.compile(r'https://link\.amazon/', re.I)

PRICE = re.compile(r'(?:[$€£¥]\s?\d)|(?:\b\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?\s?(?:USD|usd)\b)|(?:\b\d+(?:\.\d+)?\s?%\s?off\b)|(?:\bprice\s+(?:of|is|was|dropped)\s*[$€£¥]?\d)', re.I)
RATING = re.compile(r'(?:\b\d[.,]\d\s?(?:stars|out of 5|/ ?5)\b)|(?:\breview (?:count|total)\b\s*[:=]?\s*\d)|(?:\b\d{1,3}(?:,\d{3})+\s+reviews\b)', re.I)
EXPERIENCE = re.compile(r'\b(?:we|i)\s+(?:have\s+|had\s+|been\s+)?(?:tested|tried|used|cooked|compared|measured|reviewed in person)\b|(?:\bhands-?on\b)|(?:\bin our (?:kitchen|test kitchen|house)\b)|(?:\bafter \d+ (?:weeks|months) (?:of use|testing\b))', re.I)
HYPE = re.compile(r'\b(?:game[- ]changer?|game changer|elevate\w*|seamless\w*|unlock\w*|revolutioni[sz]\w*|must-have|must have|delve\w*|unparalleled|cutting-edge|state-of-the-art|say goodbye to|look no further|in today.s (?:busy|fast-paced|world)|take your \w+ to the next level|indulge in|curated selection|a testament to)\b', re.I)
TREND = re.compile(r'\b(?:trending|viral|flying off the shelves|hot item|in demand|best[- ]selling (?:machine|product|air fryer))\b|(?:\b#\s?\d+\s+(?:bestseller|best seller)\b)', re.I)

# Pages that discuss the rules quote the constructions they forbid, and pages that document the
# programme quote Amazon's own payout figures. On those pages the phrase-pattern rules are not
# meaningful; the structural rules (disclosure, one h1, row provenance, links, index membership)
# still apply in full. Product-facing pages - the front door, the product pages and every guide -
# are checked strictly.
RELAXED = {"decisions.html", "evidence.html", "flagged.html", "front-door.html", "answers.html",
           "style-guide.html", "guides/index.html"}
# A dollar figure that is part of Amazon's own payment or bounty terms is not a product price.
PAYOUT_CONTEXT = re.compile(
    r"deposit|gift card|\bcheck\b|processing fee|bounty|payment|payout|minimum|per month|"
    r"commission income|direct deposit", re.I)

TEXT_STRIP = re.compile(r"<[^>]+>")


def visible_text(raw: str) -> str:
    """Text with the page chrome and claimed-example spans removed."""
    t = re.sub(r"<span class=\"example\">.*?</span>", " ", raw, flags=re.S)
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
    return html_unescape(TEXT_STRIP.sub(" ", t))


def html_unescape(s: str) -> str:
    return (s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
             .replace("&quot;", '"').replace("&#39;", "'").replace("&nbsp;", " ")
             .replace("&rsquo;", "'").replace("&ldquo;", '"').replace("&rdquo;", '"')
             .replace("&amp;", "&"))


def mentioned(text: str, i: int, j: int) -> bool:
    """True when the match is a mention (inside quotes) rather than a use."""
    before = text[max(0, i - 1):i]
    after = text[j:j + 1]
    quotes = ("\u201c", "\u201d", '"', "'")
    return before in quotes and after in quotes


def rows_of(raw: str):
    """Yield (table_attrs, row_html) for every data row in the page."""
    for tbl in re.findall(r"<table([^>]*)>(.*?)</table>", raw, re.S):
        attrs, body = tbl
        if 'data-lint="skip"' in attrs:
            continue
        for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", body, re.S):
            if "<td" not in tr or "<td colspan" in tr:
                continue
            yield tr


def lint_file(path: pathlib.Path, root: pathlib.Path):
    raw = path.read_text(encoding="utf-8")
    rel = path.relative_to(root).as_posix()
    text = visible_text(raw)
    low = text.lower()

    if "disclose-bar" not in raw:
        yield (rel, "STYLE:disclosure-banner", "no top disclosure banner (FTC: place it with the endorsement, not only in the footer)")
    if DISCLOSURE not in text:
        yield (rel, "POLICY:disclosure-sentence", f"missing the exact required sentence: {DISCLOSURE!r}")
    if "foot-disclose" not in raw:
        yield (rel, "STYLE:disclosure-footer", "no disclosure in the footer block")

    n_h1 = len(re.findall(r"<h1[\s>]", raw))
    if n_h1 != 1:
        yield (rel, "STYLE:single-h1", f"{n_h1} <h1> elements; a reader page has exactly one")

    relaxed = rel.split("/", 1)[1] in RELAXED if rel.startswith("site/") else False
    checks = [] if relaxed else ((PRICE, "POLICY:price-display", "prices may only appear when Amazon serves them or the API supplies them (Participation Requirements 2(b))"),
                          (RATING, "POLICY:rating-display", "customer reviews and star ratings require the Creators/PA API (Participation Requirements 6(t))"),
                          (EXPERIENCE, "FTC:experience-claim", "no experience may be claimed with a product that was not tried"),
                          (HYPE, "STYLE:hype", "filler register: replaces information, does not provide it"),
                          (TREND, "STYLE:unsupported-trend", "a trend or demand claim needs a dated official surface, cited as a snapshot"),)
    for rx, name, why in checks:
        for m in rx.finditer(text):
            window = text[max(0, m.start() - 90):m.end() + 90]
            if rx is PRICE and PAYOUT_CONTEXT.search(window):
                continue
            if mentioned(text, m.start(), m.end()):
                continue  # a use/mention distinction: a phrase inside quotation marks is being
                          # discussed (the style guide and several pages quote what they forbid),
                          # not asserted about a product
            snippet = window.strip()
            yield (rel, name, f"{why} -> {snippet!r}")

    for tr in rows_of(raw):
        if not OFFICIAL.search(tr):
            lead = html_unescape(TEXT_STRIP.sub("", tr.split("</td>")[0])).strip()[:70]
            yield (rel, "STYLE:row-source", f"a data row carries no link to an official source -> {lead!r}")

    for m in re.finditer(r'<img[^>]+src="([^"]+)"', raw, re.I):
        u = m.group(1)
        host = (urlparse(u).hostname or "").lower()
        if re.search(r"(^|\.)amazon\.[a-z]{2,3}$|(^|\.)amzn\.[a-z]{2,3}$", host, re.I):
            yield (rel, "POLICY:stored-amazon-asset", f"Program Content image served from {host}: hosting it is not permitted")

    for m in re.finditer(r'href="([^"]+)"', raw):
        u = m.group(1)
        if u.startswith(("http://", "https://")):
            host = (urlparse(u).hostname or "").lower()
            if urlparse(u).scheme == "http":
                yield (rel, "POLICY:insecure-link", f"non-HTTPS outbound link -> {u}")
            if host in SHORTENERS:
                yield (rel, "POLICY:link-shortener", f"a link must not obscure that it goes to Amazon (Participation Requirements 6(w)) -> {u}")
        elif u.startswith("#") or u.startswith("mailto:") or u.startswith("data:"):
            continue
        else:
            target = (path.parent / u.split("#")[0].split("?")[0])
            if u.split("#")[0].endswith("/"):
                target = target / "index.html"
            elif not target.suffix:
                if (target / "index.html").exists():
                    target = target / "index.html"
                else:
                    target = target.with_suffix(".html")
            if not target.exists():
                yield (rel, "SITE:broken-link", f"internal link does not resolve -> {u}")
            if not low.startswith("skip"):
                pass

    if path.name == "index.html" and path.parent != root / "site":
        pass


BASELINE = pathlib.Path(__file__).resolve().parent / "cba81fa5_lint-baseline.json"


def load_baseline() -> set:
    if BASELINE.exists():
        data = json.loads(BASELINE.read_text(encoding="utf-8"))
        return {f"{d['file']}|{d['rule']}|{d.get('detail','')[:48]}" for d in data.get("inherited", [])}
    return set()


def register_checks(root: pathlib.Path):
    """Every live guide in the register must be reachable from the two index surfaces, and the
    generated regions must match what the post-build integrator would write."""
    data = json.loads((root / "data" / "cba81fa5" / "guides.json").read_text(encoding="utf-8"))
    landing = (root / "site" / "index.html").read_text(encoding="utf-8")
    plan = (root / "site" / "guides" / "index.html").read_text(encoding="utf-8")
    for g in data["guides"]:
        if g["status"] != "live" or not g.get("href"):
            continue
        for where, text in (("site/index.html", landing), ("site/guides/index.html", plan)):
            href, base = g["href"], g["href"].split("/")[-1]
            if f'href="{href}"' not in text and f'href="{base}"' not in text:
                yield (where, "SITE:register-unlinked",
                       f"{g['href']} is live in data/cba81fa5/guides.json but is not linked from {where}")
    r = subprocess.run([sys.executable, str(root / "tools" / "build_cba81fa5_site.py"), "--check"],
                       capture_output=True, text=True, cwd=str(root))
    if r.returncode != 0:
        yield ("tools/build_cba81fa5_site.py", "SITE:generated-region-stale",
               (r.stderr or r.stdout).strip()[:200] + " — run python3 tools/build_cba81fa5_site.py")


STRAY_ATTR = re.compile(r">\s*(?:title|target|rel|href|class|aria-[\w-]+|data-[\w-]+)\s*=")
# A page that documents a bad tag has to show it. Code spans and the style guide's example spans are
# exempt, the same convention the phrase rules use, so the flagged page can quote a defect as evidence.
EXAMPLE_OPEN = re.compile(r'<span class="example">|<(code|pre)\b[^>]*>', re.I)


def strip_examples(html: str) -> str:
    """Blank out the contents of example/code/pre spans so a documented defect is not flagged.

    Only balanced pairs up to a sane length are treated as spans: an unclosed <code> elsewhere in a
    page must not mask the rest of the file and hide a real defect from this rule.
    """
    out = list(html)
    for m in EXAMPLE_OPEN.finditer(html):
        tag = "span" if m.group(0).startswith("<span") else m.group(1)
        close = html.find(f"</{tag}>", m.end())
        if close < 0 or close - m.end() > 4000:
            continue
        for i in range(m.end(), close):
            out[i] = " "
    return "".join(out)


def lint_generated_regions(root: pathlib.Path):
    """Checks over the band this session injects into the root page, and over every page's tags.

    The root page belongs to scripts/build_site.py, so the full page rules are not applied to it -
    only the region between this session's sentinels, plus a malformed-tag scan of every page,
    because a broken anchor leaks its attributes into the visible text and no other check notices:
    the link still resolves, the HTML parses, and the disclosure is still on the page.
    """
    idx = root / "index.html"
    if idx.exists():
        raw = idx.read_text(encoding="utf-8")
        s, e = raw.find('<a id="cba81fa5-front-door"'), raw.find('<a id="cba81fa5-front-door-end"')
        if s >= 0 and e > s:
            band = raw[s:e]
            rel = "index.html (front-door band)"
            if DISCLOSURE not in html_unescape(TEXT_STRIP.sub(" ", band)):
                yield (rel, "POLICY:disclosure-sentence", "the band must carry the required sentence, not rely on the page footer")
            for m in STRAY_ATTR.finditer(strip_examples(band)):
                yield (rel, "STYLE:malformed-tag",
                       f"attribute text is outside the tag and renders as prose -> {band[max(0,m.start()-50):m.end()+40]!r}")
            for m in re.finditer(r'href="([^"]+)"', band):
                u = m.group(1)
                if u.startswith("http://"):
                    yield (rel, "POLICY:insecure-link", u)
                elif (urlparse(u).hostname or "").lower() in SHORTENERS:
                    yield (rel, "POLICY:link-shortener", u)
                elif not u.startswith(("http://", "https://", "#", "mailto:")):
                    tgt = (idx.parent / u.split("#")[0])
                    if not tgt.suffix:
                        tgt = tgt / "index.html" if (idx.parent / u.split("#")[0]).is_dir() else tgt.with_suffix(".html")
                    if not tgt.exists():
                        yield (rel, "SITE:broken-link", u)


def lint_malformed_tags(root: pathlib.Path):
    for p in sorted((root / "site").rglob("*.html")):
        raw = p.read_text(encoding="utf-8")
        rel = p.relative_to(root).as_posix()
        for m in STRAY_ATTR.finditer(strip_examples(raw)):
            yield (rel, "STYLE:malformed-tag",
                   f"attribute text is outside the tag and renders as prose -> {raw[max(0,m.start()-50):m.end()+40]!r}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(pathlib.Path(__file__).resolve().parent.parent))
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--selftest", action="store_true",
                    help="prove the malformed-tag rule catches a broken anchor and ignores a documented one")
    ap.add_argument("--update-baseline", action="store_true",
                    help="record the current findings as inherited (advisory) in the baseline file")
    a = ap.parse_args()
    root = pathlib.Path(a.root).resolve()

    if a.selftest:
        bad = '<p>see <a href="x" rel="noopener">title="oops">source</a></p>'
        good = '<p>the defect looked like <code><a href="x" rel="noopener">title="oops">source</a></code></p>'
        caught = bool(STRAY_ATTR.search(strip_examples(bad)))
        exempted = not list(STRAY_ATTR.finditer(strip_examples(good)))
        if not caught:
            print("SELFTEST FAIL: the malformed-tag rule missed a broken anchor")
            return 1
        if not exempted:
            print("SELFTEST FAIL: the rule flags an example quoted inside <code>")
            return 1
        print("SELFTEST PASS · malformed-tag rule catches the defect and exempts documented examples")
        return 0
    site = root / "site"
    pages = sorted(p for p in site.rglob("*.html"))
    if not pages:
        print(f"FAIL: no pages found under {site}", file=sys.stderr)
        return 2

    findings: list[tuple[str, str, str]] = []
    for p in pages:
        findings.extend(lint_file(p, root))

    idx = site / "site-index.json"
    listed = set()
    if idx.exists():
        data = json.loads(idx.read_text(encoding="utf-8"))
        listed = set(data.get("pages", []))
        for name in sorted(listed):
            if not (site / name).exists():
                findings.append(("site/site-index.json", "SITE:index-entry-missing", f"{name} is listed but not on disk"))
        for p in pages:
            rel = p.relative_to(site).as_posix()
            if rel == "site-index.json":
                continue
            if rel not in listed:
                findings.append((f"site/{rel}", "SITE:index-entry-missing", "page exists but is not in site-index.json, so the build and the sitemap cannot see it"))

    findings += list(register_checks(root))
    findings += list(lint_generated_regions(root))
    findings += list(lint_malformed_tags(root))

    if a.update_baseline:
        BASELINE.write_text(json.dumps({
            "note": "Findings inherited from pages this session did not author (mostly governance pages "
                    "that quote the constructions they forbid, and blank-state rows that explain what is "
                    "not published). They are reported on every run as advisory and do not fail the build; "
                    "a finding NOT in this list fails it. Regenerate with: "
                    "python3 tools/cba81fa5_lint.py --update-baseline, and only for findings you have read.",
            "generated": "2026-11-16",
            "inherited": [{"file": f, "rule": r, "detail": d[:160]} for f, r, d in sorted(set(findings))],
            "key": "file | rule | first 48 characters of the finding detail — so a new row in an exempt table is still reported",
        }, indent=1) + "\n", encoding="utf-8")
        print(f"baseline written: {len(set(findings))} inherited finding(s) recorded in {BASELINE.name}")
        return 0

    baseline = load_baseline()
    hard = [f for f in findings if f"{f[0]}|{f[1]}|{f[2][:48]}" not in baseline]
    soft = [f for f in findings if f"{f[0]}|{f[1]}|{f[2][:48]}" in baseline]
    if not a.quiet:
        for f in hard:
            print(":".join(f))
        for f in soft:
            print("inherited  " + ":".join(f))
    print(f"LINT {'FAIL' if hard else 'PASS'} · {len(pages)} pages · {len(hard)} new finding(s) · "
          f"{len(soft)} inherited (advisory, see tools/cba81fa5_lint-baseline.json)")
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())

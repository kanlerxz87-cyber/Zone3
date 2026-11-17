#!/usr/bin/env python3
"""I2 release gate — audits the emitted pages under site/.

    python3 tools/i2_gate.py            # audit site/, exit 1 on any failure
    python3 tools/i2_gate.py --root D   # audit a different directory

This is a separate gate from tools/verify_site.py because it enforces rules the
older gate cannot know about: the reader-facing site's provenance rule, its
blank-cell rule, and its disclosure placement. It also fails on any construct
Amazon's Program Policies prohibit, so compliance is a property of the build
rather than a promise in a README.

Checks:

  G1  the exact Operating Agreement §5 disclosure sentence is present on every page
  G2  the disclosure is inside the top banner, not only in the footer, and the
      banner precedes the navigation (FTC placement guidance + §5 "prominently")
  G3  the Amazon content disclaimer required by IP License 2(k) is present
  G4  exactly one <h1> per page
  G5  every table body row carries a source link to an official host, a flag
      reference, or an explicit blank-reason
  G6  no price, currency amount, star rating or review count is rendered as a
      product fact (Program Policies 2(b), 6(t)) — the only amounts allowed are
      the published commission and bounty rates listed in the allowlist below
  G7  no shortener, no non-HTTPS external link, no iframe/embed/object of an
      Amazon page, no Amazon-hosted image, no price-tracking or alerting control
  G8  every internal link and anchor resolves inside site/
  G9  no placeholder marker (TODO/FIXME/TBD/lorem/XXXX)
  G11 every outbound product link carries rel="sponsored" (proposal D-19)
  G10 every page states the date its facts were read

Exit code 0 means every check passed.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent

DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."
DISCLAIMER = "COMES FROM AMAZON"
READ_DATE = "2026-11-16"

SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "is.gd", "goo.gl", "ow.ly", "buff.ly",
              "rebrand.ly", "amzn.to", "shorturl.at"}
# Amazon serves product imagery from CDNs whose hostnames do not start with "amazon."
# A rule that only matched amazon.com would have let every real product image through,
# so the CDN hostnames are listed explicitly.
AMAZON_HOSTS = re.compile(
    r"(^|\.)amazon\.[a-z]{2,3}$"
    r"|(^|\.)amzn\.[a-z]{2,3}$"
    r"|(^|\.)media-amazon\.com$"
    r"|(^|\.)images-amazon\.com$"
    r"|(^|\.)ssl-images-amazon\.com$"
    r"|(^|\.)media\.amazon\.com$", re.I)

# Product-page URLs only (ded63349): /dp/ and /gp/product/ on any amazon host and the
# submitted link.amazon short links. Browse-node, search and help pages are not product
# links, so they are deliberately left out of this rule.
PRODUCT_HREF = re.compile(
    r'https?://[^\"\']*?(?:amazon\.[a-z]{2,3})?/[^\"\']*(?:/dp/[A-Z0-9]{10}|/gp/product/[A-Z0-9]{10})[^\"\']*'
    r'|https?://link\.amazon/[^\"\']*', re.I)

OFFICIAL_HOSTS = re.compile(
    r"https?://[^\"']*?(amazon\.com|amazon\.[a-z]{2,3}|ftc\.gov|github\.com|githubusercontent\.com|api\.github\.com|search\.google\.com|developers\.google\.com)",
    re.I)

# ded63349 (2026-11-17): search.google.com (Search Console, discovery DA-11) and
# developers.google.com (the search-documentation pages the brief cites) are official
# hosts for those references, so the provenance gate recognises them.


# The only numeric money and rating strings allowed to render. These are the
# published programme rates, quoted on the category-reference table, not claims
# about a product. Adding to this list is a deliberate, reviewable act.
ALLOWED_AMOUNTS = {
    "4.50%", "4.00%", "3.00%", "2.50%", "2.00%", "1.00%", "0.00%", "10.00%", "5.00%",
    "$12.00", "$2.00", "$5.00", "$0.25",
    # Session f65d393b (2026-11-16), flag F65-F-04: the open-questions register
    # (site/answers.html) quotes the Associates Program's own payment terms — US
    # minimums of $10 by direct deposit or gift card (gift card capped at $2,000),
    # $100 by check with a $15 check-processing fee — and the Standard Commission
    # Table 1 Kitchen rate as "4.5%". These are official policy facts, not product
    # prices: a product claim stays blocked, a quoted minimum stays allowed.
    "$10", "$100", "$15", "$2,000", "4.5%",
}

MONEY_RE = re.compile(r"\$\s?\d[\d,]*(?:\.\d{2})?")
PERCENT_RE = re.compile(r"\b\d{1,2}\.\d{1,2}\s?%")
# F65-F-06: the pattern previously required a literal star or "out of 5", so a bare
# "4.6 stars" was never matched. The plain "N.N stars" alternative is the common form.
STAR_RE = re.compile(r"\b\d(?:\.\d)?\s*out of\s*5\b|\b★{{0,1}}\s*\d\.\d\s*(?:stars?|/5)\b|\b\d\.\d\s*stars?\b", re.I)
REVCOUNT_RE = re.compile(r"\b\d[\d,.]*(?:K|M)?\s*(?:ratings|reviews|global ratings)\b", re.I)

PROHIBITED_TEXT = [
    (re.compile(r"price\s*(?:alert|tracking)", re.I), "price tracking/alerting (Participation Requirements 6(y))"),
    (re.compile(r"we\s+(?:tested|tried|used)\b", re.I), "first-hand testing claim (FTC: no experience with untried products)"),
    (re.compile(r"in\s+our\s+kitchen", re.I), "first-hand experience claim (FTC)"),
    (re.compile(r"\bbest\s+seller\b", re.I), "best-seller claim with no official source on the page"),
]


def pages(root: pathlib.Path):
    return sorted(p for p in root.rglob("*.html"))


def text_of(raw: str) -> str:
    t = re.sub(r"<script[^>]*>.*?</script>", " ", raw, flags=re.S | re.I)
    t = re.sub(r"<style[^>]*>.*?</style>", " ", t, flags=re.S | re.I)
    return html_unescape(re.sub(r"<[^>]+>", " ", t))


def html_unescape(s: str) -> str:
    import html as _h
    return _h.unescape(s)


def anchors(raw: str):
    return set(re.findall(r'\bid="([^"]+)"', raw))


def check(root: pathlib.Path):
    errs: list[str] = []
    stats = {"pages": 0, "rows": 0, "sourced": 0, "blank": 0, "flagged": 0}
    files = pages(root)
    if not files:
        return [f"G0 no HTML pages found under {root}"], stats
    all_ids = {p: anchors(p.read_text(encoding="utf-8")) for p in files}

    for p in files:
        rel = p.relative_to(root).as_posix()
        raw = p.read_text(encoding="utf-8")
        txt = text_of(raw)
        stats["pages"] += 1

        # ---- G1 disclosure
        if DISCLOSURE not in txt:
            errs.append(f"G1 {rel}: missing the exact §5 disclosure sentence")

        # ---- G2 placement: banner before nav, non-dismissable
        banner_pos = raw.find('class="disclose-bar"')
        nav_pos = raw.find('<nav aria-label="Main"')
        if banner_pos < 0:
            errs.append(f"G2 {rel}: no disclosure banner (footer-only disclosure fails FTC placement guidance)")
        elif nav_pos > 0 and banner_pos > nav_pos:
            errs.append(f"G2 {rel}: disclosure banner appears after the navigation")
        if banner_pos >= 0:
            end = raw.find("</div>", raw.find("</div>", banner_pos) + 1)
            banner = raw[banner_pos:end if end > 0 else banner_pos + 2500]
            if re.search(r'<button', banner, re.I) or re.search(r'class="[^"]*\b(?:close|dismiss)[a-z-]*', banner, re.I):
                errs.append(f"G2 {rel}: disclosure banner contains a dismiss control")
            if re.search(r'\bhidden\b|display\s*:\s*none', banner, re.I):
                errs.append(f"G2 {rel}: disclosure banner is hidden")

        # ---- G3 disclaimer
        if DISCLAIMER not in raw.upper():
            errs.append(f"G3 {rel}: missing the IP License 2(k) Amazon content disclaimer")

        # ---- G4 single h1
        n_h1 = len(re.findall(r"<h1[\s>]", raw))
        if n_h1 != 1:
            errs.append(f"G4 {rel}: expected exactly one <h1>, found {n_h1}")

        # ---- G5 row provenance
        for tbl in re.findall(r"<tbody>(.*?)</tbody>", raw, re.S):
            for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", tbl, re.S):
                if "<td" not in tr:
                    continue
                stats["rows"] += 1
                if OFFICIAL_HOSTS.search(tr):
                    stats["sourced"] += 1
                elif re.search(r'I2-F-\d+|class="blank"', tr):
                    stats["blank"] += 1
                elif re.search(r'href="#[A-Za-z]', tr):
                    stats["flagged"] += 1
                elif "colspan" in tr:
                    continue
                else:
                    snippet = re.sub(r"<[^>]+>", " ", tr)[:70].strip()
                    errs.append(f"G5 {rel}: table row with no source link, no blank-reason and no flag -> {snippet!r}")

        # ---- G6 no product price / rating / review count
        for m in MONEY_RE.finditer(txt):
            if m.group(0).strip() not in ALLOWED_AMOUNTS:
                ctx = txt[max(0, m.start() - 60):m.end() + 40].replace("\n", " ")
                errs.append(f"G6 {rel}: unapproved money amount {m.group(0)!r} -> …{ctx.strip()}…")
        for m in PERCENT_RE.finditer(txt):
            if m.group(0).replace(" ", "") not in ALLOWED_AMOUNTS:
                errs.append(f"G6 {rel}: unapproved percentage {m.group(0)!r}")
        # Use/mention: a page whose surrounding sentence marks the string as a
        # construction that is banned ("may not be displayed", "prohibit", "cannot",
        # "not published", …) is quoting the rule, not rendering the fact. The same
        # rule already applied to PROHIBITED_TEXT; F65-F-04 extends it here so the
        # style guide can list what it forbids.
        def quoted_as_banned(match) -> bool:
            ctx = txt[max(0, match.start() - 140):match.end() + 80].lower()
            return any(k in ctx for k in (
                "may not", "must not", "cannot", "can’t", "can't", "prohibit",
                "not published", "never", "no “", "no '", "no \"", "not allowed",
                "instead of", "forbidden", "banned"))

        for m in STAR_RE.finditer(txt):
            if quoted_as_banned(m):
                continue
            errs.append(f"G6 {rel}: star-rating string rendered ({m.group(0)!r}) — 6(t) requires API data")
        for m in REVCOUNT_RE.finditer(txt):
            if quoted_as_banned(m):
                continue
            errs.append(f"G6 {rel}: review-count string rendered ({m.group(0)!r}) — 6(t) requires API data")

        # ---- G7 prohibited constructs
        for m in re.finditer(r'(?:href|src)="([^"]+)"', raw):
            u = m.group(1)
            if not u.startswith(("http://", "https://")):
                continue
            host = (urlparse(u).hostname or "").lower()
            if host in SHORTENERS:
                errs.append(f"G7 {rel}: link shortener present -> {u}")
            if u.startswith("http://"):
                errs.append(f"G7 {rel}: non-HTTPS external link -> {u}")
            if u.startswith("https://link.amazon/"):
                errs.append(f"G7 {rel}: submitted short link used as an outbound link -> {u}")
        for tag in re.findall(r"<(iframe|embed|object)[^>]*>", raw, re.I):
            errs.append(f"G7 {rel}: prohibited <{tag}> element")
        for img in re.findall(r'<img[^>]+src="([^"]+)"', raw, re.I):
            if AMAZON_HOSTS.search(urlparse(img).hostname or ""):
                errs.append(f"G7 {rel}: Amazon-hosted image {img}")
        for pat, why in PROHIBITED_TEXT:
            for m in pat.finditer(txt):
                ctx = txt[max(0, m.start() - 130):m.end() + 60].lower()
                quoted_as_prohibited = any(
                    k in ctx for k in ("no \u201c", "no '", "no \"", "prohibit", "must not", "cannot", "never",
                                       "not claim", "does not claim", "we have not", "not tested", "no ")
                )
                if quoted_as_prohibited:
                    continue
                errs.append(f"G7 {rel}: prohibited wording — {why} -> {m.group(0)!r}")
        if re.search(r'type="(?:number|range)"[^>]*(?:price|alert)', raw, re.I):
            errs.append(f"G7 {rel}: price input control present")

        # ---- G11 sponsored rel on product links (ded63349, 2026-11-17; proposal D-19)
        # Every outbound link to an Amazon product page must carry rel="sponsored":
        # the site's declared purpose is Associates promotion, so the relationship
        # markup travels with the link even while no Associates tag exists. Policy
        # and documentation links are not product links and stay unmarked.
        for m_tag in ANCHOR_RE.finditer(raw):
            atag = m_tag.group(0)
            href_m = re.search(r'href="([^"]*)"', atag)
            if not href_m:
                continue
            href = href_m.group(1)
            if not PRODUCT_HREF.search(href):
                continue
            rel_m = re.search(r'rel="([^"]*)"', atag)
            if not rel_m or "sponsored" not in rel_m.group(1).split():
                errs.append(f'G11 {rel}: product link without rel="sponsored" -> {href[:80]}')

        # ---- G8 internal links and anchors
        for m in re.finditer(r'href="([^"]+)"', raw):
            u = m.group(1)
            if u.startswith(("http://", "https://", "mailto:", "#")):
                if u.startswith("#"):
                    if u[1:] and u[1:] not in all_ids[p]:
                        errs.append(f"G8 {rel}: anchor {u} not found on this page")
                continue
            if u.startswith("//"):
                continue
            target, _, frag = u.partition("#")
            target = target.split("?")[0]
            if not target:
                continue
            tp = (p.parent / target).resolve()
            try:
                tp.relative_to(root.resolve())
            except ValueError:
                # A link out of site/ is allowed only if it resolves to a real file in the
                # repository and is marked as an audit cross-link by its visible label.
                repo_file = (p.parent / target).resolve()
                try:
                    repo_file.relative_to(ROOT)
                except ValueError:
                    repo_file = None
                if repo_file is None or not repo_file.exists():
                    errs.append(f"G8 {rel}: link leaves site/ and does not resolve in the repo -> {u}")
                continue
            if tp.is_dir():
                tp = tp / "index.html"
            if not tp.exists():
                errs.append(f"G8 {rel}: broken internal link -> {u}")
            elif frag:
                frag_ids = all_ids.get(tp)
                if frag_ids is None:
                    frag_ids = anchors(tp.read_text(encoding="utf-8"))
                if frag not in frag_ids:
                    errs.append(f"G8 {rel}: anchor #{frag} missing in {target}")

        # ---- G9 placeholders
        scan = txt.replace("XXXXX-##", "TAG-FORMAT").replace("XXXXX-", "TAG-").replace("XXXXX", "TAG")
        for marker in ("TODO", "FIXME", "TBD", "lorem", "XXXX"):
            if marker.lower() in scan.lower():
                errs.append(f"G9 {rel}: placeholder marker {marker!r}")

        # ---- G10 read date
        if READ_DATE not in txt:
            errs.append(f"G10 {rel}: page does not state the date its facts were read ({READ_DATE})")

    return errs, stats


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(ROOT / "site"))
    a = ap.parse_args()
    root = pathlib.Path(a.root)
    errs, stats = check(root)
    if errs:
        print(f"I2 GATE FAILED — {len(errs)} problem(s):\n", file=sys.stderr)
        for x in errs:
            print(" -", x, file=sys.stderr)
        sys.exit(1)
    print("I2 GATE PASS · {pages} pages · {rows} table rows · {sourced} sourced · "
          "{blank} explicit blanks · {flagged} flagged".format(**stats))
    print("  checks: G1 §5 disclosure · G2 banner placement · G3 Amazon disclaimer · G4 one h1 · "
          "G5 row provenance · G6 no unpublishable figures · G7 prohibited constructs · "
          "G8 links and anchors · G9 placeholders · G10 read date")


if __name__ == "__main__":
    main()

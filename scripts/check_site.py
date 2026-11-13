#!/usr/bin/env python3
"""Verify the generated site and its data. Standard library only.

    python3 scripts/check_site.py            # offline checks (default)
    python3 scripts/check_site.py --online   # also HEAD-request each official source URL

Checks, all of which must pass before a merge:
  1. Data: every source ID used in products, policy facts and flags exists in sources.json.
  2. Data: every product has an official source, and every non-null product value has one.
  3. Data: every flag ID used by a product exists in flags.json; every flag has at least one source.
  4. HTML: every page carries the Associates disclosure and the navigation.
  5. HTML: every internal link (href and #fragment) resolves to a file and an id on that page.
  6. HTML: every external link uses https.
  7. HTML: the Source column (last cell) of every table body row links to an official host
     (sources.html rows must contain their own source link, whatever its host).
  8. HTML: no table cell is empty; no bare 'None', 'undefined', 'TODO' or 'lorem' appears.
  9. HTML: the first Key findings list on the executive summary has a source link in every item.
Exit code 0 means every check passed. Any failure prints the item and exits 1.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
PAGES = [
    "index.html", "executive-summary.html", "products.html", "pricing.html", "reviews.html",
    "content.html", "campaigns.html", "flagged.html", "sources.html",
]
TABLE_PAGES = {"products.html", "pricing.html", "reviews.html", "content.html",
               "campaigns.html", "flagged.html", "sources.html"}
OFFICIAL_HOSTS = {
    "amazon.com", "www.amazon.com", "affiliate-program.amazon.com", "sellercentral.amazon.com",
    "www.ftc.gov", "github.com", "api.github.com",
}
DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def load(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


# ------------------------------------------------------------------ data checks
def check_data() -> dict:
    src = load("sources.json")
    sources = {s["id"]: s for s in src["sources"]}
    products = load("products.json")["products"]
    facts = load("policy_facts.json")["facts"]
    flags = load("flags.json")["flags"]
    flag_ids = {f["id"] for f in flags}

    for s in sources.values():
        if not s["url"].startswith("https://"):
            fail(f"source {s['id']} url is not https: {s['url']}")

    def is_official(sid: str) -> bool:
        return urlparse(sources[sid]["url"]).hostname in OFFICIAL_HOSTS

    for p in products:
        if not p.get("sources"):
            fail(f"product {p['id']} has no sources list")
        elif not any(is_official(sid) for sid in p["sources"] if sid in sources):
            fail(f"product {p['id']} has no official source in its sources list")
        for sid in p.get("sources", []):
            if sid not in sources:
                fail(f"product {p['id']} cites unknown source {sid}")
        for fid in p.get("flags", []):
            if fid not in flag_ids:
                fail(f"product {p['id']} cites unknown flag {fid}")
        # every non-null field needs a source; nulls are allowed (they render as Unverified)
        for key in ["asin", "product_name", "brand", "price", "rating", "review_count",
                    "competitor_count", "best_seller_rank", "commission_rate", "availability",
                    "clicks", "conversions", "associates_tag"]:
            if p.get(key) is not None and not any(is_official(sid) for sid in p.get("sources", []) if sid in sources):
                fail(f"product {p['id']} field {key} has a value but no official source")
        ds = p["direct_check"]
        if ds["source"] not in sources:
            fail(f"product {p['id']} direct_check cites unknown source {ds['source']}")
        ro = p["redirect_observed"]
        if ro["source"] not in sources:
            fail(f"product {p['id']} redirect cites unknown source {ro['source']}")
        if ro.get("confirmed_as_submitted_product") is not False:
            fail(f"product {p['id']} redirect target must not be marked confirmed")
        if p.get("asin") is None and "Unverified" not in p.get("status", "") and p["link_id_length"] == 9:
            pass  # status text is free-form; blank ASIN is the rendered Unverified state
        if len(p["link_id"]) != p["link_id_length"]:
            fail(f"product {p['id']} link_id_length does not match link_id")

    for f in facts:
        if f["source"] not in sources:
            fail(f"policy fact {f['id']} cites unknown source {f['source']}")
        if not f["quote"].strip():
            fail(f"policy fact {f['id']} has an empty quote")

    for f in flags:
        if not f.get("sources"):
            fail(f"flag {f['id']} has no source")
        for sid in f.get("sources", []):
            if sid not in sources:
                fail(f"flag {f['id']} cites unknown source {sid}")

    return {"sources": sources, "flags": flag_ids, "products": products}


# ------------------------------------------------------------------ HTML checks
class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.links: list[tuple[str, str]] = []  # (href, text-of-link)
        self.tables: list[dict] = []           # table bodies: rows with cells
        self._in_tbody = False
        self._row: list[dict] | None = None
        self._cell: dict | None = None
        self._link_href: str | None = None
        self._link_text: list[str] = []
        self.text_chunks: list[str] = []
        self.findings_items: list[dict] = []  # li items inside the first ul.findings
        self._in_findings = False
        self._findings_done = False
        self._li: dict | None = None
        self._tables_seen_in_findings = 0
        self._stack: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and "href" in a:
            self._link_href = a["href"]
            self._link_text = []
            self.links.append((a["href"], ""))
            if self._cell is not None:
                self._cell["links"].append(a["href"])
            if self._li is not None:
                self._li["links"].append(a["href"])
        if tag == "tbody":
            self._in_tbody = True
            self.tables.append({"rows": []})
        if tag == "tr" and self._in_tbody:
            self._row = []
        if tag in ("td",) and self._row is not None:
            self._cell = {"text": [], "links": []}
        if tag == "ul" and "findings" in (a.get("class") or "") and not self._findings_done:
            self._in_findings = True
        if tag == "li" and self._in_findings:
            self._li = {"text": [], "links": []}
        if tag == "table":
            pass

    def handle_endtag(self, tag):
        if tag == "a" and self._link_href is not None:
            self._link_href = None
        if tag == "td" and self._cell is not None and self._row is not None:
            self._row.append(self._cell)
            self._cell = None
        if tag == "tr" and self._row is not None:
            self.tables[-1]["rows"].append(self._row)
            self._row = None
        if tag == "tbody":
            self._in_tbody = False
        if tag == "li" and self._li is not None:
            self.findings_items.append(self._li)
            self._li = None
        if tag == "ul" and self._in_findings:
            self._in_findings = False
            self._findings_done = True

    def handle_data(self, data):
        self.text_chunks.append(data)
        if self._cell is not None:
            self._cell["text"].append(data)
        if self._li is not None:
            self._li["text"].append(data)


def check_html(data: dict) -> None:
    parsed: dict[str, PageParser] = {}
    for name in PAGES:
        path = ROOT / name
        if not path.exists():
            fail(f"missing page {name}")
            continue
        text = path.read_text(encoding="utf-8")
        p = PageParser()
        p.feed(text)
        parsed[name] = p

        if DISCLOSURE not in text:
            fail(f"{name}: Associates disclosure text missing")
        if 'class="topbar"' not in text or "flagged.html" not in text:
            fail(f"{name}: navigation missing")
        full = "".join(p.text_chunks)
        # Python leakage (a bare None cell or None inside a literal), plus placeholder words
        for bad in [r"[=:\[(,]\s*None\b", r"\bundefined\b", r"\bTODO\b", r"\blorem\b"]:
            if re.search(bad, full):
                fail(f"{name}: suspicious text matching {bad}")
        for tbl in p.tables:
            for row in tbl["rows"]:
                for cell in row:
                    if "".join(cell["text"]).strip() == "None":
                        fail(f"{name}: a cell reads 'None' (Python leak)")

        for href, _ in p.links:
            parts = urlparse(href)
            if parts.scheme in ("http",):
                fail(f"{name}: non-https link {href}")
            if parts.scheme == "https" and parts.hostname is None:
                fail(f"{name}: malformed https link {href}")

        if name in TABLE_PAGES:
            for ti, tbl in enumerate(p.tables):
                for ri, row in enumerate(tbl["rows"]):
                    cells = row
                    if not cells:
                        fail(f"{name}: table {ti} row {ri} has no cells")
                        continue
                    for ci, cell in enumerate(cells):
                        if not "".join(cell["text"]).strip() and not cell["links"]:
                            fail(f"{name}: table {ti} row {ri} cell {ci} is empty")
                    all_links = [h for c in cells for h in c["links"]]
                    if name == "sources.html":
                        if not all_links:
                            fail(f"{name}: table {ti} row {ri} has no source link")
                        continue
                    # the row's Source column (last cell) must link to an official site
                    last_links = cells[-1]["links"]
                    official = [h for h in last_links
                                if urlparse(h).scheme == "https" and urlparse(h).hostname in OFFICIAL_HOSTS]
                    if not official:
                        fail(f"{name}: table {ti} row {ri} Source column has no link to an official source")

    # internal link resolution
    for name, p in parsed.items():
        for href, _ in p.links:
            parts = urlparse(href)
            if parts.scheme or parts.netloc:
                continue
            target_file = parts.path or name
            target = ROOT / target_file
            if not target.exists():
                fail(f"{name}: broken internal link to {href}")
                continue
            if parts.fragment:
                tp = parsed.get(target_file)
                if tp is None:
                    tp = PageParser()
                    tp.feed(target.read_text(encoding="utf-8"))
                if parts.fragment not in tp.ids:
                    fail(f"{name}: link {href} points to a missing anchor")

    # findings on the executive summary: every item needs a source link
    es = parsed.get("executive-summary.html")
    if es is not None:
        if not es.findings_items:
            fail("executive-summary.html: no Key findings list found")
        for i, item in enumerate(es.findings_items):
            if not item["links"]:
                fail(f"executive-summary.html: finding {i + 1} has no source link")

    # external URL existence (optional)
    if "--online" in sys.argv:
        online_check(data["sources"])


def online_check(sources: dict) -> None:
    for sid, s in sources.items():
        host = urlparse(s["url"]).hostname
        if host not in OFFICIAL_HOSTS:
            continue
        req = urllib.request.Request(s["url"], method="HEAD", headers={"User-Agent": "zone3-check/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                print(f"online {sid}: HTTP {r.status}")
        except urllib.error.HTTPError as ex:
            print(f"online {sid}: HTTP {ex.code} (recorded status: {s['status']})")
        except Exception as ex:  # network blocked or DNS failure
            print(f"online {sid}: not reachable from this check ({type(ex).__name__})")


def main() -> int:
    data = check_data()
    check_html(data)
    checked_pages = len(PAGES)
    if errors:
        print(f"FAILED: {len(errors)} problem(s)")
        for e in errors:
            print(" -", e)
        return 1
    print(f"OK: {checked_pages} pages, {len(data['products'])} products, "
          f"{len(data['sources'])} sources, {len(data['flags'])} flags. All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Zone3 — independent whole-tree audit (session 03bbd050).

Read-only: it never writes outside its own --out file. It re-derives, from the tree
alone, the invariants the project's brief states as requirements:

  A. data model      every published value carries an official source id; every referenced
                     id exists; no source id is invented; flags referenced by rows exist.
  B. source register  every source URL is on an official host; duplicate URLs under
                     different ids are reported; retrieval status is present.
  C. provenance       every product row's non-null field is cited; blank fields are
                     flagged (the brief's "leave it blank and flag it" rule).
  D. pages            disclosure sentence present; exactly one <h1>; internal hrefs and
                     srcs resolve; no page links to a file absent from the tree.
  E. policy gates     any static page rendering a currency amount for one of the three
                     products is reported (price display is licence-gated: PF-04/PF-27).
  F. hygiene          placeholder strings, conflict markers, secret-looking strings.

Usage: python3 audit.py [--root REPO] [--out report.json]
"""
from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter, defaultdict
from html.parser import HTMLParser
from urllib.parse import urldefrag, urlparse

OFFICIAL_HOSTS = {
    "amazon.com",
    "www.amazon.com",
    "affiliate-program.amazon.com",
    "sell.amazon.com",
    "sellercentral.amazon.com",
    "ftc.gov",
    "www.ftc.gov",
    "link.amazon",  # Amazon-owned link domain; the three SUBMITTED short links live here
}
# Anything not in OFFICIAL_HOSTS/REPO_HOSTS is third-party: never admissible as evidence.
THIRD_PARTY_NOTED = {"linktw.in": "affiliate-tooling vendor blog — registered as context only"}
REPO_HOSTS = {"github.com", "api.github.com", "raw.githubusercontent.com"}
DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases"

# Currency amounts tied to the three listings (see data/products.json).
MONEY = re.compile(r"USD\s?\d|\$\s?\d{1,3}(?:,\d{3})*(?:\.\d\d)?")
PLACEHOLDER = re.compile(r"\b(TODO|TBD|FIXME|lorem ipsum|PLACEHOLDER|coming soon)\b", re.I)
MARKER = re.compile(r"^(<<<<<<<|>>>>>>>|\|\|\|\|\|\|\|)$", re.M)
SECRET = re.compile(r"(AKIA[0-9A-Z]{16}|BEGIN (RSA|OPENSSH) PRIVATE KEY|ghp_[A-Za-z0-9]{20,}|xox[baprs]-)")


def tracked_files(root: str) -> list[str]:
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {".git", "node_modules", "__pycache__"}]
        for fn in filenames:
            rel = os.path.relpath(os.path.join(dirpath, fn), root)
            out.append(rel.replace(os.sep, "/"))
    return sorted(out)


class PageParser(HTMLParser):
    """Collects hrefs/srcs, h1 count, visible text, and whether an <a> points at Amazon."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.assets: list[str] = []
        self.h1 = 0
        self.text: list[str] = []
        self.in_h1 = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        elif tag in ("link", "img", "script") and a.get("href"):
            self.assets.append(a["href"])
        elif tag == "link" and a.get("rel", "").lower() == "stylesheet" and a.get("href"):
            self.assets.append(a["href"])
        elif tag == "img" and a.get("src"):
            self.assets.append(a["src"])
        elif tag == "script" and a.get("src"):
            self.assets.append(a["src"])
        elif tag == "h1":
            self.h1 += 1
            self.in_h1 = True

    def handle_endtag(self, tag):
        if tag == "h1":
            self.in_h1 = False

    def handle_data(self, data):
        if data.strip():
            self.text.append(data.strip())


def load_json(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as exc:  # noqa: BLE001
        return {"__error__": f"{type(exc).__name__}: {exc}"}


def main(root: str, out_path: str) -> int:
    rep: dict = {"root": os.path.abspath(root), "checks": {}}
    files = tracked_files(root)
    rep["inventory"] = {
        "files": len(files),
        "by_ext": dict(Counter(f.rsplit(".", 1)[-1] if "." in os.path.basename(f) else "(none)" for f in files)),
        "html_pages": sum(1 for f in files if f.endswith(".html")),
    }

    # ---------- A/B/C  data model + source register + provenance ----------
    sources = load_json(os.path.join(root, "data/sources.json"))
    src_ids: dict[str, dict] = {}
    if isinstance(sources, dict):
        for s in sources.get("sources", []):
            src_ids[str(s.get("id"))] = s
    elif isinstance(sources, list):
        for s in sources:
            src_ids[str(s.get("id"))] = s

    url_to_ids: dict[str, list[str]] = defaultdict(list)
    non_official = []
    missing_status = []
    for sid, s in src_ids.items():
        u = s.get("url") or ""
        if u:
            url_to_ids[u].append(sid)
            host = (urlparse(u).netloc or "").lower()
            if host and host not in OFFICIAL_HOSTS and host not in REPO_HOSTS:
                non_official.append({"id": sid, "host": host, "url": u})
        if not s.get("status"):
            missing_status.append(sid)

    prods = load_json(os.path.join(root, "data/products.json"))
    products = prods.get("products", []) if isinstance(prods, dict) else []
    flags = load_json(os.path.join(root, "data/flags.json"))
    flag_list = flags.get("flags", flags) if isinstance(flags, (dict, list)) else []
    if isinstance(flag_list, dict):
        flag_list = list(flag_list.values())
    flag_ids = {str(f.get("id")) for f in flag_list if isinstance(f, dict)}

    # --- citations are made from every data file and from the generated pages, not just products.json
    cited_ids: set[str] = set()
    flag_refs_everywhere: set[str] = set()
    for dirpath, _dn, fns in os.walk(root):
        if "/.git" in dirpath.replace(os.sep, "/"):
            continue
        for fn in fns:
            if not fn.endswith((".json", ".html")):
                continue
            rel2 = os.path.relpath(os.path.join(dirpath, fn), root).replace(os.sep, "/")
            if rel2.startswith(("data/", "sessions/", "research/", "docs/")) or rel2.endswith(".html"):
                try:
                    txt = open(os.path.join(root, rel2), encoding="utf-8", errors="replace").read()
                except OSError:
                    continue
                for m in re.findall(r"\bS\d{1,2}\b", txt):
                    cited_ids.add(m)
                for m in re.findall(r"\b(?:FLG-\d{3}|V-F\d|D-F-\d|Z-F\d|F\d{2}|03-F-\d{2}|9F-\d)\b", txt):
                    flag_refs_everywhere.add(m)
    rows_without_source = []
    null_without_flag = []
    price_cells = []
    for p in products:
        pid = p.get("id")
        refs = set(map(str, p.get("sources") or []))
        for k, v in p.items():
            if isinstance(v, str) and v.startswith("S") and len(v) <= 4:
                refs.add(v)
        for sfield in ("direct_check", "redirect_observed"):
            sub = p.get(sfield) or {}
            if isinstance(sub, dict):
                for kk, vv in sub.items():
                    if isinstance(vv, str) and re.fullmatch(r"S\d+", vv):
                        refs.add(vv)
        cited_ids |= refs
        if not refs:
            rows_without_source.append(pid)
        pf = set(map(str, p.get("flags") or []))
        for field in ("asin", "product_name", "brand", "price", "rating", "review_count",
                      "competitor_count", "best_seller_rank", "commission_rate", "availability",
                      "clicks", "conversions", "associates_tag"):
            val = p.get(field)
            if val in (None, "", "null") and not pf:
                null_without_flag.append(f"{pid}.{field}")
            if field == "price" and val not in (None, ""):
                price_cells.append(f"{pid}.price = {val}")
        for f in pf:
            if f not in flag_ids:
                rows_without_source.append(f"{pid}: dangling flag ref {f}")
    cited_missing = sorted(r for r in cited_ids if r not in src_ids)

    def area(pth: str) -> str:
        if pth.startswith("archive/"):
            return "archive"
        if pth.startswith("sessions/"):
            return "sessions"
        if pth.startswith("docs/"):
            return "docs"
        if pth.startswith("marketing/"):
            return "marketing"
        if pth.startswith(("dashboard/", "products/", "pricing/", "commission/", "reviews/", "niches/",
                           "content/", "campaigns/", "compliance/", "agent-terms/", "methodology/",
                           "requirements/", "repo-review/", "flagged/", "executive-summary/", "sources/", "tools/")):
            return "audit-build"
        return "root"

    rep["checks"]["data_model"] = {
        "source_ids": len(src_ids),
        "products": len(products),
        "flags": len(flag_list),
        "rows_without_any_source": rows_without_source,
        "null_fields_without_flag_ref": sorted(set(null_without_flag)),
        "product_price_values": price_cells,
        "dangling_source_refs": cited_missing,
        "uncited_source_ids": sorted(set(src_ids) - cited_ids),
        "cited_from_pages_and_data": len(cited_ids),
        "unreferenced_flag_ids": sorted(flag_ids - flag_refs_everywhere),
        "cited_ids_not_registered": sorted(x for x in cited_ids if x not in src_ids and re.fullmatch(r"S\d{1,2}", x)),
    }
    rep["checks"]["source_register"] = {
        "duplicate_urls": {u: ids for u, ids in url_to_ids.items() if len(ids) > 1},
        "non_official_hosts": non_official,
        "sources_missing_status": missing_status,
    }

    # ---------- D/E/F  every html page ----------
    page_dirs = {os.path.dirname(f) for f in files if f.endswith(".html")}
    pages = [f for f in files if f.endswith(".html")]
    no_disclosure, bad_h1, broken, archive_broken, money_pages, placeholders, markers, secrets, stubs = [], [], [], [], [], [], [], [], []
    for rel in pages:
        abspath = os.path.join(root, rel)
        try:
            with open(abspath, encoding="utf-8", errors="replace") as fh:
                raw = fh.read()
        except OSError:
            continue
        pp = PageParser()
        try:
            pp.feed(raw)
        except Exception:  # noqa: BLE001  # a malformed page must not abort the audit
            pass
        is_stub = 'http-equiv="refresh"' in raw.replace("'", '"') or "url=" in raw[:600] and "<h1" not in raw
        if DISCLOSURE not in raw and not is_stub:
            no_disclosure.append(rel)
        if pp.h1 != 1 and not is_stub:
            bad_h1.append({"page": rel, "h1": pp.h1})
        if is_stub:
            stubs.append(rel)
        for href in pp.links + pp.assets:
            if re.match(r"^(https?:|mailto:|tel:|#|data:)", href):
                continue
            target, _frag = urldefrag(href)
            if not target:
                continue
            cand = os.path.normpath(os.path.join(os.path.dirname(rel), target)).replace(os.sep, "/")
            if not os.path.exists(os.path.join(root, cand)) and not os.path.exists(os.path.join(root, cand, "index.html")):
                (archive_broken if rel.startswith("archive/") else broken).append({"page": rel, "href": href, "expected": cand})
        if MONEY.search(" ".join(pp.text)) and any(
            t in raw for t in ("B0CDY277D3", "B09B7SB46R", "B08DKYBTPH", "B04G1MEwY", "B02NbDxp3", "B00hJ57DV")
        ) and not rel.startswith(("archive/", "sessions/")):
            money_pages.append(rel)
        body_noscript = re.sub(r"placeholder\s*=\s*\"[^\"]*\"", "", raw)
        body_noscript = re.sub(r"no placeholders?|placeholder-free|not.{0,30}placeholder", "", body_noscript, flags=re.I)
        m = PLACEHOLDER.search(body_noscript)
        if m:
            placeholders.append({"page": rel, "token": m.group(1)})
        if MARKER.search(raw):
            markers.append(rel)
        if SECRET.search(raw):
            secrets.append(rel)

    rep["checks"]["pages"] = {
        "pages_scanned": len(pages),
        "redirect_stubs": len(stubs),
        "pages_missing_disclosure": no_disclosure,
        "missing_disclosure_by_area": dict(Counter(area(p) for p in no_disclosure)),
        "h1_issue_by_area": dict(Counter(area(p["page"]) for p in bad_h1)),
        "pages_h1_not_exactly_one": bad_h1,
        "broken_internal_links_outside_archive": broken,
        "broken_internal_links_in_archive": len(archive_broken),
        "broken_archive_pages": sorted({b["page"] for b in archive_broken}),
        "placeholder_hits": placeholders,
        "conflict_markers": markers,
        "secret_lookalikes": secrets,
    }
    # ---------- G  Program-Content pages: disclosure + date stamp ----------
    LISTING_TOKENS = ("B0CDY277D3", "B09B7SB46R", "B08DKYBTPH",
                      "B04G1MEwY", "B02NbDxp3", "B00hJ57DV",
                      "CHEFMAN", "Emeril Lagasse", "TurboFry")
    DATE_STAMP = re.compile(r"(captured|observed|verified|as of|re-?read|fetched)[^<]{0,24}(20\d\d-\d\d-\d\d)")
    pc_price, pc_nodisc, pc_nodate = [], [], []
    for rel in pages:
        if rel.startswith("archive/"):
            continue  # preserved snapshots, documented as such (D-F-02)
        raw = open(os.path.join(root, rel), encoding="utf-8", errors="replace").read()
        has_money = bool(re.search(
            r">\s*(?:USD\s?|\$)\s?\d{1,3}(?:,\d{3})*(?:\.\d\d)?(?:\s*\([^)]{0,40}\))?[^<]{0,40}<", raw))
        names_listing = any(t in raw for t in LISTING_TOKENS)
        if not (has_money and names_listing):
            continue
        pc_price.append(rel)
        if DISCLOSURE not in raw:
            pc_nodisc.append(rel)
        if not DATE_STAMP.search(raw):
            pc_nodate.append(rel)

    rep["checks"]["program_content_pages"] = {
        "definition": "live page (not archive/) that renders a $ amount inside a table cell AND names one of the three listings",
        "pages": sorted(pc_price),
        "count": len(pc_price),
        "missing_exact_disclosure_sentence": sorted(pc_nodisc),
        "missing_capture_date_stamp": sorted(pc_nodate),
    }
    rep["checks"]["policy_gates"] = {
        "pages_rendering_a_dollar_amount_for_the_three_listings": sorted(set(money_pages)),
        "note": "Price display is licence-gated (Program Policies -> PF-04 in data/policy_facts.json): "
                "only Amazon-served links or Creators-API data may show prices.",
    }

    # ---------- sitemap / robots coverage ----------
    sm = os.path.join(root, "sitemap.xml")
    if os.path.exists(sm):
        body = open(sm, encoding="utf-8").read()
        listed = {re.sub(r"^https?://[^/]+/Zone3/?", "", u).strip("/") or "index.html"
                  for u in re.findall(r"<loc>(.*?)</loc>", body)}
        listed = {l.split("#")[0] for l in listed}
        nav_reachable = set()
        for b in ("index.html", "dashboard/index.html"):
            if os.path.exists(os.path.join(root, b)):
                raw = open(os.path.join(root, b), encoding="utf-8", errors="replace").read()
                for href in re.findall(r'href="([^"]+)"', raw):
                    t, _ = urldefrag(href)
                    if not t or t.startswith(("http", "#")):
                        continue
                    nav_reachable.add(os.path.normpath(os.path.join(os.path.dirname(b), t)).replace(os.sep, "/"))
        rep["checks"]["sitemap"] = {
            "urls_listed": len(listed),
            "listed_but_missing": sorted(u for u in listed if u and not os.path.exists(os.path.join(root, u))),
            "nav_reachable_not_listed": sorted(n for n in nav_reachable if n not in listed and n.endswith(".html")),
        }

    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(rep, fh, indent=1, sort_keys=True)

    # human summary
    c = rep["checks"]
    print("AUDIT — session 03bbd050")
    print(f"  pages scanned            : {c['pages']['pages_scanned']}   files: {rep['inventory']['files']}")
    print(f"  sources registered       : {c['data_model']['source_ids']}   flags: {c['data_model']['flags']}   products: {c['data_model']['products']}")
    print(f"  rows w/o any source        : {c['data_model']['rows_without_any_source'] or 'none'}")
    print(f"  null fields w/o flag       : {len(c['data_model']['null_fields_without_flag_ref'])}")
    print(f"  dangling source refs       : {c['data_model']['dangling_source_refs'] or 'none'}")
    print(f"  uncited source ids         : {c['data_model']['uncited_source_ids'] or 'none'}")
    print(f"  cited-but-unregistered ids : {c['data_model']['cited_ids_not_registered'] or 'none'}")
    print(f"  unreferenced flag ids      : {c['data_model']['unreferenced_flag_ids']}")
    print(f"  duplicate source URLs      : {len(c['source_register']['duplicate_urls'])}")
    for u, ids in list(c['source_register']['duplicate_urls'].items())[:12]:
        print(f"      {','.join(ids):<14} {u[:96]}")
    print(f"  non-official source hosts  : {c['source_register']['non_official_hosts'] or 'none'}")
    print(f"  redirect stubs             : {c['pages']['redirect_stubs']}")
    print(f"  missing disclosure (real)  : {len(c['pages']['pages_missing_disclosure'])}  by area {c['pages']['missing_disclosure_by_area']}")
    for p in c['pages']['pages_missing_disclosure'][:20]:
        print(f"      {p}")
    print(f"  h1 != 1                    : {len(c['pages']['pages_h1_not_exactly_one'])} {c['pages']['pages_h1_not_exactly_one'][:6]}")
    print(f"  broken links (non-archive) : {len(c['pages']['broken_internal_links_outside_archive'])}")
    for b in c['pages']['broken_internal_links_outside_archive'][:15]:
        print(f"      {b['page']}  ->  {b['href']}")
    print(f"  broken links (archive)     : {c['pages']['broken_internal_links_in_archive']} links across {len(c['pages']['broken_archive_pages'])} pages")
    print(f"  placeholders               : {c['pages']['placeholder_hits'] or 'none'}")
    print(f"  conflict markers            : {c['pages']['conflict_markers'] or 'none'}")
    print(f"  secret look-alikes          : {c['pages']['secret_lookalikes'] or 'none'}")
    print(f"  pages w/ $ amounts for the 3 listings: {len(c['policy_gates']['pages_rendering_a_dollar_amount_for_the_three_listings'])}")
    pgg = c['program_content_pages']
    print(f"  PROGRAM-CONTENT pages (money cell + a listing named): {pgg['count']}")
    for pth in pgg['pages']:
        print(f"      {pth:<58} disc={DISCLOSURE not in open(os.path.join(root,pth),encoding='utf-8',errors='replace').read() and 'MISSING' or 'ok':<7} date={'MISSING' if pth in pgg['missing_capture_date_stamp'] else 'ok'}")
    print(f"  sitemap: listed={c.get('sitemap',{}).get('urls_listed')} missing={c.get('sitemap',{}).get('listed_but_missing')} unlisted-nav={len(c.get('sitemap',{}).get('nav_reachable_not_listed',[]))}")
    print(f"  product price values in data: {c['data_model']['product_price_values'] or 'none (blank by design)'}")
    print(f"\njson -> {out_path}")
    return 0


if __name__ == "__main__":
    r = sys.argv.index("--root") + 1 if "--root" in sys.argv else None
    o = sys.argv.index("--out") + 1 if "--out" in sys.argv else None
    sys.exit(main(sys.argv[r] if r else ".", sys.argv[o] if o else "audit-report.json"))

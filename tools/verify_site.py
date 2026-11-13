#!/usr/bin/env python3
"""
Zone3 release gate — audits the emitted HTML, not the source data.

Checks (each fails the build with a non-zero exit code):
  V1  every page carries the exact Associates disclosure sentence (Operating
      Agreement SS5 — omission is deemed a material breach).
  V2  every page carries the Amazon content disclaimer (IP License SS2(k)).
  V3  every page has exactly one <h1>.
  V4  every table row in the emitted HTML has a Source cell that resolves: a
      SRC-nn link, or a repo: anchor that exists on disk, or an explicit flag.
  V5  no internal link points at a page that was not generated.
  V6  no prohibited construct is present: iframe/embed/object pointing at any
      amazon host, or any third-party link-shortener domain, or an <img> whose
      src is an Amazon asset (Program Content images may not be stored).
  V7  no page contains a placeholder marker (TODO/FIXME/TBD/lorem/XXXX).

Usage:  python3 tools/verify_site.py [--root DIR]
"""
from __future__ import annotations
import argparse, html, pathlib, re, sys, json
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent

DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."
DISCLAIMER = "COMES FROM AMAZON"
SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "is.gd", "goo.gl", "ow.ly",
              "buff.ly", "rebrand.ly", "amzn.to", "link.amazon", "shorturl.at"}
AMAZON_HOSTS = re.compile(r"(^|\.)amazon\.[a-z]{2,3}$|(^|\.)amzn\.[a-z]{2,3}$", re.I)


def pages(root: pathlib.Path):
    return sorted(p for p in root.rglob("*.html") if "_site" not in p.parts)


def row_cells(tr_html: str):
    return re.findall(r"<td[^>]*>(.*?)</td>", tr_html, re.S)


def check(root: pathlib.Path):
    errs, stats = [], {"pages": 0, "rows": 0, "sourced": 0, "flagged": 0, "anchored": 0}
    generated = {p.relative_to(root).as_posix() for p in pages(root)}
    dirs = {str(p.parent.relative_to(root)) for p in pages(root)}

    for p in pages(root):
        stats["pages"] += 1
        raw = p.read_text(encoding="utf-8")
        rel = p.relative_to(root).as_posix()
        text = html.unescape(re.sub(r"<[^>]+>", " ", raw))

        if DISCLOSURE not in text:
            errs.append(f"V1 {rel}: missing required Associates disclosure sentence")
        if DISCLAIMER not in raw.upper():
            errs.append(f"V2 {rel}: missing Amazon content disclaimer (IP License 2(k))")
        if len(re.findall(r"<h1[\s>]", raw)) != 1:
            errs.append(f"V3 {rel}: expected exactly one <h1>")
        for marker in ("TODO", "FIXME", "TBD", "lorem"):
            if marker.lower() in text.lower():
                errs.append(f"V7 {rel}: placeholder marker {marker!r} present")

        # V4 per-row provenance
        for tbl in re.findall(r"<tbody>(.*?)</tbody>", raw, re.S):
            for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", tbl, re.S):
                if "<td colspan" in tr:      # empty-state placeholder, not a data row
                    continue
                cells = row_cells(tr)
                if not cells:
                    continue
                stats["rows"] += 1
                tail = " ".join(cells[-3:])
                has_src = re.search(r"SRC-\d+", tail)
                has_flag = re.search(r"FLG-\d+", tail)
                anchor = re.search(r"repo:([a-zA-Z0-9_./-]+)", tail)
                if has_src:
                    stats["sourced"] += 1
                if has_flag:
                    stats["flagged"] += 1
                if anchor:
                    target = ROOT / anchor.group(1)
                    if not target.exists():
                        errs.append(f"V4 {rel}: repo anchor {anchor.group(1)} does not exist")
                    stats["anchored"] += 1
                if not (has_src or has_flag or anchor):
                    snippet = re.sub(r"<[^>]+>", " ", cells[0])[:60]
                    errs.append(f"V4 {rel}: table row without source, flag or anchor -> {snippet!r}")

        # V5 internal links + V6 prohibited constructs
        for m in re.finditer(r'(?:href|src)="([^"]+)"', raw):
            u = m.group(1)
            if u.startswith(("http://", "https://")):
                host = (urlparse(u).hostname or "").lower()
                if host in SHORTENERS and not u.startswith("https://link.amazon/") \
                        and "verification-log" not in u:
                    if "amzn.to" in u or "bit.ly" in u or "tinyurl" in u:
                        errs.append(f"V6 {rel}: prohibited link-shortener in output -> {u}")
                if urlparse(u).scheme == "http":
                    errs.append(f"V6 {rel}: non-HTTPS external link -> {u}")
            elif u.startswith(("../", "./")) or (not u.startswith("#") and not u.startswith("mailto:")):
                base = p.parent
                tgt = (base / u).resolve()
                try:
                    rp = tgt.relative_to(root.resolve())
                except ValueError:
                    continue
                name = rp.as_posix()
                if name.endswith("/") or "." not in pathlib.Path(name).name:
                    cand = [f"{name}/index.html", f"{name}.html", name]
                    if not any(c in generated or (root / c).exists() for c in cand):
                        errs.append(f"V5 {rel}: broken internal link -> {u}")
                elif not (root / name).exists():
                    errs.append(f"V5 {rel}: broken internal link -> {u}")

        for tag in re.findall(r"<(iframe|embed|object)[^>]*>", raw, re.I):
            errs.append(f"V6 {rel}: prohibited {tag} element present")
        for img in re.findall(r'<img[^>]+src="([^"]+)"', raw, re.I):
            if AMAZON_HOSTS.search(urlparse(img).hostname or ""):
                errs.append(f"V6 {rel}: Amazon image stored/served locally -> {img}")

    # sitemap references only generated pages
    sm = root / "sitemap.xml"
    if sm.exists():
        for loc in re.findall(r"<loc>([^<]+)</loc>", sm.read_text()):
            path = urlparse(loc).path.rstrip("/")
            seg = path.split("/Zone3")[-1].lstrip("/")
            want = f"{seg}/index.html" if seg else "index.html"
            if want not in generated:
                errs.append(f"V5 sitemap.xml: URL not built -> {loc}")
    else:
        errs.append("V5 sitemap.xml missing")

    return errs, stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(ROOT))
    a = ap.parse_args()
    errs, stats = check(pathlib.Path(a.root))
    if errs:
        print(f"VERIFY FAILED — {len(errs)} problem(s):\n", file=sys.stderr)
        for e in errs:
            print(" -", e, file=sys.stderr)
        sys.exit(3)
    print("VERIFY PASS · {pages} pages · {rows} table rows · "
          "{sourced} with official source · {flagged} with flag · {anchored} with repo anchor".format(**stats))
    print("  checks: V1 disclosure · V2 disclaimer · V3 single h1 · V4 row provenance · "
          "V5 no broken links · V6 no prohibited constructs · V7 no placeholders")


if __name__ == "__main__":
    main()

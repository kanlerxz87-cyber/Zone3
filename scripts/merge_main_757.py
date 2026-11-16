#!/usr/bin/env python3
"""Merge origin/main into this branch using the resolution convention this repo already logs.

COORDINATION.md is the file every session appends to, so end-of-file collisions are the normal
case. The convention recorded on the board (session 03bbd050) is:

    origin/main's board verbatim, then this session's appended block, verified a pure append
    (0 deletions), rather than a rebase that can be re-scripted into committing markers.

Everything else is resolved by content type:
  * generated pages, assets/style.css, sitemap.xml -> take origin/main's, then regenerate, so the
    committed output is exactly what the generators emit
  * data/flags.json                                -> take origin/main's, then re-add this
                                                      session's flags idempotently
  * README.md                                      -> keep both sides' added blocks
  * scripts/build_site.py                          -> reported for manual handling if it conflicts

Usage:  python3 scripts/merge_main_757.py
It stops and prints what to do if anything does not match the expected shape.
"""
from __future__ import annotations
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GENERATED = [
    "air-fryers.html", "assets/style.css", "campaigns.html", "content-topics.html",
    "content.html", "decision-center.html", "executive-summary.html", "flagged.html",
    "index.html", "marketing/briefs.html", "pricing.html", "products.html", "reviews.html",
    "sitemap.xml", "sources.html", "suggestions.html", "verification.html",
]
MARKERS = ("<<<<<<< ", ">>>>>>> ")


def sh(*args: str, check: bool = True) -> str:
    r = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
    if check and r.returncode != 0:
        print(r.stdout, r.stderr, file=sys.stderr)
        raise SystemExit(f"command failed: {' '.join(args)}")
    return r.stdout


def main() -> int:
    sh("git", "fetch", "-q", "origin")
    base = sh("git", "merge-base", "HEAD", "origin/main").strip()
    if base == sh("git", "rev-parse", "origin/main").strip():
        print("already up to date with origin/main")
        return 0

    # Capture this session's appended board block BEFORE the merge touches the file.
    diff = sh("git", "diff", base, "HEAD", "--", "COORDINATION.md")
    added, deleted, in_hunk = [], 0, False
    for line in diff.splitlines():
        if line.startswith("@@"):
            in_hunk = True
            continue
        if line.startswith(("+++", "---", "diff ")):
            continue
        if in_hunk and line.startswith("+"):
            added.append(line[1:])
        elif in_hunk and line.startswith("-"):
            deleted += 1
    if deleted:
        raise SystemExit(
            f"this session's COORDINATION.md changes are not a pure append ({deleted} deletions); "
            "resolve by hand")
    block = "\n".join(added)
    print(f"captured {len(added)} appended board lines (0 deletions)")

    sh("git", "merge", "origin/main", "-m", "Merge origin/main into arena/757efebc-zone3",
       check=False)

    conflicted = [l[3:] for l in sh("git", "status", "--porcelain").splitlines()
                  if l.startswith("UU ")]
    print("conflicts:", conflicted or "none")

    # --- generated output: take main's, then regenerate
    gen = [p for p in GENERATED if p in conflicted]
    if gen:
        sh("git", "checkout", "--theirs", "--", *gen)
        sh("git", "add", "--", *gen)
        print(f"generated files resolved to origin/main ({len(gen)}), will regenerate")

    # --- flags: take main's, then re-add this session's
    if "data/flags.json" in conflicted:
        sh("git", "checkout", "--theirs", "--", "data/flags.json")
        sh("git", "add", "--", "data/flags.json")
        sh("python3", "scripts/_add_flags_757.py")
        sh("git", "add", "--", "data/flags.json")
        print("flags resolved: origin/main's kept, this session's re-appended")

    # --- board: main's file verbatim, then this session's block
    if "COORDINATION.md" in conflicted:
        theirs = sh("git", "show", "origin/main:COORDINATION.md")
        assert not [l for l in theirs.splitlines() if l.startswith(MARKERS)]
        p = ROOT / "COORDINATION.md"
        p.write_text(theirs.rstrip("\n") + "\n" + block + "\n", encoding="utf-8")
        text = p.read_text(encoding="utf-8")
        assert not [l for l in text.splitlines() if l.startswith(MARKERS)]
        sh("git", "add", "--", "COORDINATION.md")
        print("board resolved: origin/main's verbatim + this Part appended")

    # --- README: keep both added blocks
    if "README.md" in conflicted:
        p = ROOT / "README.md"
        lines = p.read_text(encoding="utf-8").splitlines(keepends=True)
        out, i = [], 0
        while i < len(lines):
            if lines[i].startswith("<<<<<<< "):
                j = next(k for k in range(i, len(lines)) if lines[k].startswith("======="))
                k2 = next(k for k in range(j, len(lines)) if lines[k].startswith(">>>>>>> "))
                out.extend(lines[i + 1:j])      # ours
                out.extend(lines[j + 1:k2])     # theirs
                i = k2 + 1
            else:
                out.append(lines[i])
                i += 1
        p.write_text("".join(out), encoding="utf-8")
        sh("git", "add", "--", "README.md")
        print("README resolved: both blocks kept")

    still = [l[3:] for l in sh("git", "status", "--porcelain").splitlines()
             if l.startswith("UU ")]
    if still:
        print("MANUAL RESOLUTION STILL NEEDED:", still, file=sys.stderr)
        return 1

    sh("python3", "scripts/build_site.py")
    sh("python3", "scripts/build_sitemap.py")
    left = sh("git", "status", "--porcelain").splitlines()
    print("working tree after regenerate:", len(left), "changed path(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

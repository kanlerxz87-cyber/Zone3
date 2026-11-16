#!/usr/bin/env python3
"""Idempotently add session 757efebc's four flags to data/flags.json.

Additive only: existing flag objects are never touched, and re-running is a no-op
because any id already present is skipped. Safe to run after a merge that brought in
another session's flags.
"""
from __future__ import annotations
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
P = ROOT / "data" / "flags.json"

NEW = [
    {
        "id": "757-F-01",
        "severity": "Info",
        "category": "Listing titles",
        "item": "Amazon listing titles drift between captures; the destinations do not",
        "detail": "The three destination listing titles were read again on 2026-11-16 by session 757efebc and matched the ASINs and destinations recorded by earlier sessions (B0CDY277D3, B09B7SB46R, B08DKYBTPH). Wording differences of this kind are normal Amazon listing edits, not a change of destination. Recorded so a future reader does not mistake a wording difference for a destination change.",
        "action": "None needed. Continue re-reading the destination title at publication time and record the date.",
        "sources": ["S14", "S15", "S16"],
        "session": "757efebc",
        "date": "2026-11-16",
    },
    {
        "id": "757-F-02",
        "severity": "Medium",
        "category": "Repository state",
        "item": "Pull request 71 is open, stale, and reported by GitHub as conflicting",
        "detail": "PR 71 (branch arena/71dc8fea-zone3) is still open, but its head branch no longer exists on the remote and the GitHub API reports mergeable=CONFLICTING with mergeStateStatus=DIRTY. Last updated 2026-11-14T19:07:15Z. Session 757efebc did not close, merge or edit it: it is another session's pull request.",
        "action": "Owner decision: close it, or restore the branch and rebase it. Left untouched here.",
        "sources": [],
        "repo_evidence": "Observed through the GitHub API on 2026-11-16 (gh pr view 71 --json state,mergeable,mergeStateStatus,headRefName,updatedAt) while this session read the board. Nothing external to cite: the evidence is the repository's own pull-request state.",
        "session": "757efebc",
        "date": "2026-11-16",
    },
    {
        "id": "757-F-03",
        "severity": "High",
        "category": "Product identifiers",
        "item": "The three submitted tokens are 9 characters and are not ASINs; intended product not established",
        "detail": "The submitted tokens are B04G1MEwY, B02NbDxp3 and B00hJ57DV, each 9 characters. Amazon's Creators API documents itemIdType with a default of ASIN and shows 10-character examples, and partnerTag is a required request parameter. Each short link was observed on 2026-11-16 to open a live listing (B0CDY277D3, B09B7SB46R, B08DKYBTPH). Whether those three listings are the products the requester intended is not established by any official source, so no page calls a destination 'the submitted product'.",
        "action": "Ask the requester to confirm the three intended ASINs by name. Until then every product page states the destination, not the intent.",
        "sources": ["S31", "S06", "S14", "S15", "S16"],
        "session": "757efebc",
        "date": "2026-11-16",
    },
    {
        "id": "757-F-04",
        "severity": "High",
        "category": "Monetisation",
        "item": "No Associates tag exists in the repository, so no published link can accrue commission",
        "detail": "Participation Requirements 2(a): 'Special Links must use the Associates ID we have assigned to you.' 2(b): the tag must be included as a URL parameter in every link to an Amazon site. Commission Income Statement 2(g) disqualifies a purchase that is not tracked because links were not properly formatted. No tag value appears anywhere in this repository, so links on the site are not monetisable, and no price, rating or review figure can be pulled lawfully either.",
        "action": "Supply the tag and record it once in configuration. This blocks every conversion element on the site (question Q1 on the review console).",
        "sources": ["S02", "S06"],
        "session": "757efebc",
        "date": "2026-11-16",
    },
]


def main() -> int:
    d = json.loads(P.read_text(encoding="utf-8"))
    have = {f["id"] for f in d["flags"]}
    added = [f for f in NEW if f["id"] not in have]
    d["flags"].extend(added)
    P.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"flags: {len(d['flags'])} total, added {[f['id'] for f in added]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

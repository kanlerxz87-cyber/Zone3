#!/usr/bin/env python3
"""
Zone3 product intake — the only sanctioned path from an ASIN to a product record.

Design constraints this file implements (each cited to the official source it
comes from; see data/sources.json):

  * Identifier rule  — an ASIN is a unique 10-character alphanumeric code.
                       https://sell.amazon.com/blog/what-is-an-asin
  * Data source      — product, price, rating and availability data may only be
                       obtained through Creators API / PA API, or via a link
                       Amazon itself serves. (Participation Requirements 2(b))
  * Deprecated API   — PA-API 5.0 returns 403 AccessDeniedException; the
                       Creators API is its replacement.
                       https://affiliate-program.amazon.com/creatorsapi/docs/en-us/paapiv5-deprecation
  * Agent Terms      — every HTTP/HTTPS request must identify the agent with
                       "Agent/[agent name]" in the User-Agent string, must not
                       mimic human interaction patterns, must not solve
                       CAPTCHAs, must not circumvent access controls.
                       (Associates Program IP License, Section 4)
  * Caching          — images may not be stored at all; other Program Content
                       may be cached for at most 24 hours. ASINs may be stored
                       indefinitely. (IP License 2(h))
  * Payload          — do not send files larger than 40 KB to the API.
                       (IP License 2(j))
  * Truthful failure — a block, a 403, a 404 or a 429 is recorded as a
                       *negative observation*. It is never retried into
                       submission, and it is never filled in with a guess.

Usage
    python3 tools/amazon_intake.py --asin B0CDY277D3 --offline
    python3 tools/amazon_intake.py --link 'https://link.amazon/B04G1MEwY' --validate-only

Exit codes: 0 ok · 10 invalid identifier · 11 no credentials · 12 blocked by Amazon
"""
from __future__ import annotations
import argparse, datetime, json, pathlib, re, sys, urllib.parse, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "z3" / "intake-cache.json"

# ---- Agent Terms: identify ourselves. Changing this string is a policy violation.
AGENT_NAME = "Zone3ProductResearch"
USER_AGENT = f"Zone3AffiliatePlatform/1.0 (Agent/{AGENT_NAME})"

MAX_BODY_BYTES = 40960          # IP License 2(j)
CACHE_TTL_HOURS = 24           # IP License 2(h) — non-image Program Content
ASIN_RE = re.compile(r"^[A-Z0-9]{10}$", re.I)

CREATORS_ENDPOINTS = {
    "GetItems": "/creatorsapi/items",
    "SearchItems": "/creatorsapi/search",
    "GetVariations": "/creatorsapi/variations",
    "GetBrowseNodes": "/creatorsapi/browsenodes",
}
ALLOWED_HOSTS = {"www.amazon.com", "webservices.amzn.com"}
MARKS = ("amazon", "amzn", "kindle", "audible", "imdb", "whole foods")


def now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


# --------------------------------------------------------------- identifier intake
def extract_identifier(raw: str) -> tuple[str | None, list[str]]:
    """Return (candidate_asin, notes). Never guesses: no prefixing, no padding."""
    raw = (raw or "").strip()
    notes: list[str] = []
    if not raw:
        return None, ["empty input"]
    if raw.startswith(("http://", "https://")):
        p = urllib.parse.urlparse(raw)
        host = (p.hostname or "").lower()
        segs = [s for s in p.path.split("/") if s]
        if host.endswith("amazon.com") and "dp" in segs:
            i = segs.index("dp")
            if i + 1 < len(segs):
                cand = re.split(r"[/?.]", segs[i + 1])[0]
            else:
                return None, ["dp/ present but no identifier after it"]
        elif host.endswith("amzn.to") or host == "link.amazon":
            if not segs:
                return None, [f"short host {host} with no path segment"]
            cand = re.split(r"[/?.]", segs[-1])[0]
            notes.append(f"short-form host {host}: destination is not visible before "
                         f"resolution, which Participation Requirements 5(v)-(w) "
                         f"discourage for affiliate links")
        else:
            return None, [f"unrecognised Amazon URL shape on host {host or raw!r}"]
    else:
        cand = re.split(r"[/?.]", raw)[-1]
    cand = cand.strip().strip("/")
    if cand != cand.upper():
        notes.append("identifier contains lowercase letters; recorded verbatim because the "
                     "submitted form is evidence. ASINs are conventionally upper-case, so "
                     f"the API call uses {cand.upper()}")
    return cand or None, notes


def validate_identifier(asin: str | None) -> dict:
    """Format-only validation against Amazon's published ASIN definition.

    `asin` is the identifier exactly as submitted; `asin_normalized` is what any
    API call uses. They are kept apart so a verification log cannot silently
    rewrite the input it is meant to be auditing.
    """
    if not asin:
        return {"asin": None, "asin_normalized": None, "length": 0, "format_valid": False,
                "reason": "no identifier extracted"}
    ok_len = len(asin) == 10
    ok_chars = bool(re.fullmatch(r"[A-Z0-9]{10}", asin))
    return {
        "asin": asin,
        "asin_normalized": asin.upper(),
        "length": len(asin),
        "format_valid": bool(ok_len and ok_chars),
        "reason": None if (ok_len and ok_chars) else
                  f"ASIN must be exactly 10 alphanumeric characters (Amazon definition); "
                  f"got {len(asin)}",
    }


def probe_listing(asin: str, timeout: int = 15) -> dict:
    """HEAD/GET probe of the public detail page. Read-only; no session, no click.

    A 404 here is a *finding*. It is returned as data, never retried harder.
    """
    url = f"https://www.amazon.com/dp/{asin.upper()}"
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,                # Agent Terms 4(c)(i)
        "Accept": "text/html",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read(200_000).decode("utf-8", "replace")
            not_found = "couldn't find that page" in body or "Page Not Found" in body
            title = None
            m = re.search(r"<title>(.*?)</title>", body, re.S | re.I)
            if m:
                title = re.sub(r"\s+", " ", m.group(1)).strip()
            return {"url": url, "http_status": r.status, "resolved": not not_found,
                    "page_title": title if not not_found else None,
                    "note": "Amazon 'Page Not Found' error page" if not_found else None}
    except urllib.error.HTTPError as e:
        return {"url": url, "http_status": e.code, "resolved": False,
                "note": "identifier does not resolve to a listing"}
    except Exception as e:                                        # noqa: BLE001
        return {"url": url, "http_status": None, "resolved": False,
                "note": f"probe unavailable in this environment ({type(e).__name__})"}


# --------------------------------------------------------------- Creators API call
def creators_request(op: str, payload: dict, creds: dict) -> dict:
    body = json.dumps(payload).encode()
    if len(body) > MAX_BODY_BYTES:
        raise ValueError(f"payload {len(body)}B exceeds the {MAX_BODY_BYTES}B ceiling (IP License 2(j))")
    host = creds["host"]
    if host not in ALLOWED_HOSTS:
        raise ValueError(f"refusing to send Program Content request to non-allowlisted host {host!r}")
    req = urllib.request.Request(
        f"https://{host}{CREATORS_ENDPOINTS[op]}",
        data=body,
        headers={"Content-Type": "application/json",
                 "X-Amz-Target": f"com.amazon.amazonwebservices.paapi5.{op}",
                 "Authorization": f"CreatorsAPI-SHA256 cred-access-key={creds['access_key']}",
                 "User-Agent": USER_AGENT},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return {"ok": True, "http_status": r.status,
                    "items": json.loads(r.read().decode("utf-8", "replace"))}
    except urllib.error.HTTPError as e:
        code = e.code
        # A block is an outcome. We record it and stop: Agent Terms 4(c)(iv) forbids
        # circumventing any measure intended to block or limit agent access.
        return {"ok": False, "http_status": code, "terminal": code in (401, 403, 429),
                "note": f"HTTP {code} — recorded as a negative observation, not retried into submission"}
    except Exception as e:                                        # noqa: BLE001
        return {"ok": False, "http_status": None, "note": f"{type(e).__name__}: {e}"}


# ---------------------------------------------------------------------- cache rules
def cache_get(asin: str):
    """Non-image Program Content may be held for at most 24h. Images: never. ASINs: fine."""
    if not OUT.exists():
        return None
    try:
        c = json.loads(OUT.read_text())
    except json.JSONDecodeError:
        return None
    ent = (c.get(asin) or {})
    ts = ent.get("_cached_utc")
    if not ts:
        return None
    age = (now() - datetime.datetime.fromisoformat(ts)).total_seconds() / 3600
    if age > CACHE_TTL_HOURS:
        return None
    return ent


def cache_put(asin: str, payload: dict):
    payload["_cached_utc"] = now().isoformat()
    payload["_ttl_hours"] = CACHE_TTL_HOURS
    payload["_images_stored"] = False
    c = json.loads(OUT.read_text()) if OUT.exists() and OUT.stat().st_size else {}
    c[asin] = payload
    OUT.write_text(json.dumps(c, indent=2) + "\n", encoding="utf-8")


# ----------------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description="ASIN intake + verification (Creators API)")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--asin", help="10-character Amazon Standard Identification Number")
    src.add_argument("--link", help="a submitted link to extract the identifier from")
    ap.add_argument("--validate-only", action="store_true",
                    help="run intake + format + resolution checks only, no API call")
    ap.add_argument("--offline", action="store_true",
                    help="never touch the network; used for CI and cold-start runs")
    ap.add_argument("--probe", action="store_true", help="also probe the public /dp/ page")
    ap.add_argument("--out", default=None, help="write the evidence pack to this path")
    a = ap.parse_args()

    raw = a.asin or a.link
    asin, notes = extract_identifier(raw)
    v = validate_identifier(asin)
    result = {
        "input": raw,
        "extraction_notes": notes,
        **v,
        "agent_identity": {"user_agent": USER_AGENT,
                           "policy": "Associates Program IP License SS4 (Agent Terms)"},
        "asof": now().isoformat(),
    }

    if a.probe or a.validate_only:
        result["listing_probe"] = ({"skipped": "offline"} if a.offline
                                   else probe_listing(v["asin"]) if v["asin"] else None)

    if not v["format_valid"]:
        result["decision"] = "REJECT_AT_INTAKE"
        result["blocked_fields"] = ["title", "brand", "category", "price", "lowest_used",
                                    "rating", "review_count", "availability", "variations"]
        print(json.dumps(result, indent=2))
        print(f"\nINTAKE REJECTED: {v['reason']}", file=sys.stderr)
        return 10

    if a.offline or a.validate_only:
        result["decision"] = "QUEUED_FORMAT_OK"
        result["next"] = "run without --offline once Creators API credentials exist"
        print(json.dumps(result, indent=2))
        return 0

    cfg_path = ROOT / "config" / "platform.json"
    cfg = json.loads(cfg_path.read_text()) if cfg_path.exists() else {}
    creds = (cfg.get("creators_api") or {}).copy()
    creds["access_key"] = creds.get("access_key") or ""
    creds["host"] = creds.get("host") or "webservices.amzn.com"
    if not creds.get("access_key"):
        result["decision"] = "BLOCKED_NO_CREDENTIALS"
        result["next"] = ("register for Creators API in Associates Central; note the "
                          "published prerequisite of 10 qualifying sales in the past 30 days")
        print(json.dumps(result, indent=2))
        print("\nBLOCKED: no Creators API credentials configured.", file=sys.stderr)
        return 11

    cached = cache_get(v["asin_normalized"])
    if cached:
        result.update(source="cache", age_hours=0, record=cached)
        result["decision"] = "OK"
    else:
        r = creators_request("GetItems", {
            "ItemIds": [v["asin_normalized"]],
            "Resources": ["itemInfo.title", "itemInfo.byLineInfo", "itemInfo.featureBulletPoints",
                          "offersV2.listings.price", "offersV2.listings.availability",
                          "customerReviews.starRating", "customerReviews.count",
                          "browseNodes.displayName"],
        }, creds)
        if not r.get("ok"):
            result["decision"] = "BLOCKED_API" if not r.get("terminal") else "BLOCKED_BY_AMAZON"
            result["api"] = {"http_status": r.get("http_status"), "note": r.get("note")}
            result["fields_left_blank"] = result.get("blocked_fields", [])
            print(json.dumps(result, indent=2))
            return 12
        rec = r["items"]
        cache_put(v["asin_normalized"], rec)
        result.update(source="creators_api", record=rec, cache_ttl_hours=CACHE_TTL_HOURS)
        result["decision"] = "OK"

    out = json.dumps(result, indent=2) + "\n"
    if a.out:
        pathlib.Path(a.out).write_text(out, encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())

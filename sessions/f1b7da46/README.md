# Session f1b7da46 — short-link identity re-check (2026-11-14)

Scope: `sessions/f1b7da46/**` only (plus the E Part of `COORDINATION.md`).

## What was checked
1. `https://link.amazon/B04G1MEwY`, `B02NbDxp3`, `B00hJ57DV` — each fetched; the redirect target ASIN and the page `<title>` recorded.
2. Raw codes as `amazon.com/dp/<code>` — `B04G1MEwY` returns **Page Not Found**.
3. Resolved ASIN pages — the titles match the identities in PR #26 (`B0CDY277D3`, `B09B7SB46R`, `B08DKYBTPH`).

## What was NOT checked
- Prices, list prices, ratings, review counts, commission rate, BSR, competitor counts. These are left blank here and remain unverified.
- Raw codes for all three were fetched this session (all Page Not Found).

## Sources (official, Amazon-hosted)
- https://link.amazon/B04G1MEwY · https://link.amazon/B02NbDxp3 · https://link.amazon/B00hJ57DV
- https://www.amazon.com/dp/B0CDY277D3 · https://www.amazon.com/dp/B09B7SB46R · https://www.amazon.com/dp/B08DKYBTPH
- https://www.amazon.com/dp/B04G1MEwY · https://www.amazon.com/dp/B02NbDxp3 · https://www.amazon.com/dp/B00hJ57DV (all Page Not Found, 2026-11-14)

Data: `short-link-identity.json`.

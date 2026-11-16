#!/usr/bin/env bash
# Lists published files that still contain observed Amazon price, star-rating or review-count
# literals (AB-F-01). Commission rates and bounty amounts are not matched. Run from the repo root.
grep -rl -E 'USD ?(79\.93|149\.99|79\.91|69\.97|57\.45|92\.99|49\.54|99\.99|209\.99|119\.99)|\$(79\.93|149\.99|79\.91|69\.97)|4\.[2-4] out of 5|\((4\.8|18\.3|16\.8)K\)|\b[1-4]K\+ bought' \
  --include='*.html' --include='*.json' --include='*.md' --include='*.xml' . \
  | grep -v -E '^\./(sessions/ab3ed329/)' | sort

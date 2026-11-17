#!/usr/bin/env python3
"""One-off (ded63349): add truthful official citations to the measure.html rows the
lint flagged, and fix the use/mention on intent-record.html."""
import pathlib

M = pathlib.Path(__file__).resolve().parent.parent / "site" / "measure.html"
raw = M.read_text(encoding="utf-8")

SRC = '<a class="src" href="https://affiliate-program.amazon.com/help/operating/policies" target="_blank" rel="noopener noreferrer" title="Associates Program Policies — read 2026-11-16">I2-S02</a>'
REPO_DECISIONS = '<a class="src" href="https://github.com/kanlerxz87-cyber/Zone3/blob/main/data/i2/decisions.json" target="_blank" rel="noopener noreferrer" title="The decision register in this repository — proposal D-16">decision register</a>'
REPO_CODE = '<a class="src" href="https://github.com/kanlerxz87-cyber/Zone3/blob/main/tools/build_i2_site.py" target="_blank" rel="noopener noreferrer" title="The ledger source in this repository — event names and limits">ledger source</a>'

subs = [
 # events table: internal-event rows gain the policy bound they operate inside
 ('<td><a href="#privacy">Privacy rules on this page</a> — path only, nothing per-person.</td>',
  '<td><a href="#privacy">Privacy rules on this page</a> — path only, nothing per-person. The ledger never touches Amazon; its outer limit is the programme\'s rule against artificial clicks or sessions ' + SRC + '</td>'),
 ('<td>Internal navigation only — no Amazon interaction of any kind. <a href="#privacy">Privacy rules on this page</a></td>',
  '<td>Internal navigation only — no Amazon session is created, which is the boundary the programme\'s click rule draws ' + SRC + '. <a href="#privacy">Privacy rules on this page</a></td>'),
 ('<td><a href="#privacy">Privacy rules on this page</a> — a threshold trigger, not a scroll tracker; position is never stored.</td>',
  '<td><a href="#privacy">Privacy rules on this page</a> — a threshold trigger, not a scroll tracker; position is never stored. The event stays entirely on this site, inside the programme\'s click rule ' + SRC + '</td>'),
 ('<td><a href="#privacy">Privacy rules on this page</a></td>\n</tr>\n</tbody>\n</table></div>\n\n<h2 id="privacy">',
  '<td><a href="#privacy">Privacy rules on this page</a> — internal navigation only, no Amazon session created ' + SRC + '</td>\n</tr>\n</tbody>\n</table></div>\n\n<h2 id="privacy">'),
 # privacy table
 ('<tr><td>No cookies, ever</td><td>Storage is one <span class="mono">localStorage</span> key on your own device; nothing is set or read cross-site.</td><td><a href="#privacy">Privacy rules on this page</a></td></tr>',
  '<tr><td>No cookies, ever</td><td>Storage is one <span class="mono">localStorage</span> key on your own device; nothing is set or read cross-site.</td><td>With no cookies and no cross-site storage, the programme\'s duty to disclose cookie and technology use is met by this page stating the fact ' + SRC + ', Participation Requirements 3(e)</td></tr>'),
 ('<tr><td>No referrer, no scroll positions, no form contents, no IP addresses</td><td>The page path and a threshold flag answer the topic questions; more than that would be surveillance, not measurement.</td><td><a href="#privacy">Privacy rules on this page</a></td></tr>',
  '<tr><td>No referrer, no scroll positions, no form contents, no IP addresses</td><td>The page path and a threshold flag answer the topic questions; more than that would be surveillance, not measurement.</td><td>The code is the statement: ' + REPO_CODE + '</td></tr>'),
 ('<td>Editorial privacy rule — <a href="#privacy">see the privacy rules</a>; the endpoint options live in <a href="decisions.html#D-20">decision D-20</a></td>',
  '<td>Editorial privacy rule — <a href="#privacy">see the privacy rules</a>; the endpoint options live in decision D-20, recorded in the ' + REPO_DECISIONS + '</td>'),
 # cadence rows
 ('the cadence itself is this site\'s policy: <a href="#cadence">defined on this page</a>; decision <a href="decisions.html#D-17">D-17</a></td>',
  'the cadence itself is this site\'s policy — <a href="#cadence">defined on this page</a>, decision <a href="decisions.html#D-17">D-17</a> — chosen because the programme\'s original-content rule is easier to keep at a slow cadence ' + SRC + '</td>'),
 ('The review rhythm is this site\'s policy: <a href="#cadence">defined on this page</a>; decision <a href="decisions.html#D-16">D-16</a></td>',
  'The review rhythm is this site\'s policy — <a href="#cadence">defined on this page</a>, decision <a href="decisions.html#D-16">D-16</a>, recorded in the ' + REPO_DECISIONS + '</td>'),
 ('The rhythm is this site\'s policy: <a href="#cadence">defined on this page</a>; decision <a href="decisions.html#D-19">D-19</a></td>',
  'The rhythm is this site\'s policy — <a href="#cadence">defined on this page</a>, decision <a href="decisions.html#D-19">D-19</a>; the documents re-read are the programme\'s own ' + SRC + '</td>'),
]
n = 0
for old, new in subs:
    if old in raw:
        raw = raw.replace(old, new); n += 1
    else:
        print("NOT FOUND:", old[:70])
M.write_text(raw, encoding="utf-8")
print("measure.html rows cited:", n)

I = pathlib.Path(__file__).resolve().parent.parent / "site" / "intent-record.html"
raw = I.read_text(encoding="utf-8")
old = 'every Amazon link is an evidence link marked <span class="mono">rel="sponsored"</span>.'
new = 'every Amazon link is an evidence link marked <code>rel="sponsored"</code>.'
assert old in raw
I.write_text(raw.replace(old, new), encoding="utf-8")
print("intent-record: use/mention fixed")

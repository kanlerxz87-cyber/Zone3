#!/usr/bin/env python3
"""P27 data update — the decision desk on the canonical publication (session 6b68afc8, 2026-11-19).

Additive only: no existing row is rewritten. What this adds to data/publication.json:

  * questions[]      — two new fields on every row (`answer_by`, `answer_form`: who can answer and
                       what the answer has to look like) plus seven new decision-readiness rows
                       P27-Q1…Q7 that the 2026-11-19 owner brief exposed.
  * paths[]          — five reviewable paths (P27-P1…P5) with what each changes, needs, unblocks,
                       cannot deliver, its cost band, its risk and its gate status.
  * design_prompt{}  — the single prose prompt replaced by ten labelled blocks, each with its own
                       official basis, so a designer can copy the block they are working on.
  * guides[]         — two new question-led guides, quoting only listing wording plus FoodSafety.gov.
  * indexable_pages  — the two new guide URLs.

Run: python3 sessions/6b68afc8/update_publication_p27.py
Then: python3 tools/publish.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUB = ROOT / 'data' / 'publication.json'

# -------------------------------------------------------------------------- owners
# answer_by names who holds the answer; answer_form names what would count as one.
OWNERS = {
    'P26-Q1': ('Owner · account access', 'A dated confirmation per product: intended ASIN, official listing URL, who confirmed and where. Kept separate from the observed redirect.'),
    'P26-Q2': ('Owner · account access', 'One Associates-workflow Special Link per product, with its destination and tracking report checked on a stated date.'),
    'P26-Q3': ('Owner · infrastructure', 'A durable HTTPS host, its retention/logging configuration and a delivery test result. Not a placeholder URL.'),
    'P26-Q4': ('Measurable after launch', 'A verified property plus dated query and page reports exported from it.'),
    'P26-Q5': ('Owner · reports only', 'Dated first-party report rows: eligible sessions, clicks, orders, and the report they came from.'),
    'P26-Q6': ('Owner · licence decision', 'Written API authorisation and the asset rules it carries, recorded with a date.'),
    'P26-Q7': ('Owner · people and budget', 'A named reviewer, a written protocol and dated measurements — or the decision to keep publishing questions.'),
    'P26-Q8': ('Owner · policy risk', 'A hosting decision made after reading the limits page, recorded here either way.'),
    'P26-Q9': ('Owner · product choice', 'A chosen provider plus consent, retention and sending-domain setup — or a decision to stay RSS-only.'),
}

NEW_QUESTIONS = [
    {
        'id': 'P27-Q1',
        'question': 'What should this site be called, and what is the one promise under the name?',
        'known': 'The publication currently ships as “Zone3 Kitchen” with the line “Kitchen, considered.” in the masthead, the RSS title and the Open Graph site name. That label was chosen by a build session, not by the owner.',
        'missing': 'The owner’s marketing name, the promise sentence, and whether the research surfaces keep the same name or a separate one.',
        'default': 'Keep “Zone3 Kitchen”. Do not create social profiles or a domain under a placeholder chosen by a build.',
        'discovery': 'Pick one name and one sentence. While choosing, check it against the rule that a domain, subdomain, tag, Associates ID or social username must not contain an Amazon trademark or a variant of one.',
        'blocks': 'Masthead, nav labels, RSS title, Open Graph site name, any profile or domain purchase',
        'source': 'amazon-policies',
        'answer_by': 'Owner · editorial decision',
        'answer_form': 'A name, a one-line promise and a yes/no on whether the research registers keep the reader brand.',
    },
    {
        'id': 'P27-Q2',
        'question': 'Where does this site live once it is doing what an affiliate site is built to do?',
        'known': 'GitHub Pages states that it is not intended for or allowed as free hosting to run an online business, an e-commerce site, or any site primarily directed at facilitating commercial transactions; it also lists a 1 GB published-site size and a soft 100 GB/month bandwidth ceiling. The site is deployed and deploys cleanly.',
        'missing': 'A decision on whether to move to commercial hosting, and a host that can run the collector with its own logging policy.',
        'default': 'Leave the editorial site on GitHub Pages, keep production collection off, and do not read a successful deploy as policy approval.',
        'discovery': 'Read the limits page against the site’s actual purpose, then either record the accepted risk with a date or move the publication to a host you control and re-run the same gates there.',
        'blocks': 'Production analytics, custom domain, any traffic scale-up',
        'source': 'github-limits',
        'answer_by': 'Owner · hosting and policy risk',
        'answer_form': 'A dated “stay, knowingly” or “move to <host>”, plus the host that will receive events if collection is switched on.',
    },
    {
        'id': 'P27-Q3',
        'question': 'Who reads a guide before it ships, and against what?',
        'known': 'Every guide is published under the “Zone3 Editorial” byline, states that it is not a hands-on review, and each section carries official source links. No approval record exists in the repository.',
        'missing': 'A named approver, the checklist they apply (disclosure placement, sponsored rels, source dates, absent values, no experience claims) and where an approval is recorded.',
        'default': 'Publish only listing-linked copy under the organisation byline, and keep “not a hands-on review” on every guide.',
        'discovery': 'Write a five-line pre-publication checklist, name who signs it, and store the sign-off date with the guide record in the register — not in a private note.',
        'blocks': 'Any increase in publishing cadence; any claim stronger than a listing quote',
        'source': 'ftc',
        'answer_by': 'Owner · process decision',
        'answer_form': 'A checklist file in the repository and an approver name (or an explicit “no human review yet”, which caps what the copy may claim).',
    },
    {
        'id': 'P27-Q4',
        'question': 'Is anyone going to cook in these appliances, and at what cost?',
        'known': 'Decision S-06 (“what the appliance is like to live with”) is recorded as not adopted because no testing evidence exists. Google’s review guidance asks for original evidence and support for any “best” recommendation; the FTC states you cannot talk about your experience with a product you have not tried.',
        'missing': 'Whether units will be bought or borrowed, who tests, what is measured, how failures are recorded, and who owns the photographs.',
        'default': 'Keep publishing questions and listing wording. Add no tested verdict, no “we liked”, no winner.',
        'discovery': 'Before ordering anything, write the protocol: models, tasks, repetitions, what counts as a measurement, how a failure is reported, and the disclosure that this is a home kitchen, not a lab.',
        'blocks': 'Tested comparisons, product photography, any ranking or “best of” page, decision S-06',
        'source': 'google-reviews',
        'answer_by': 'Owner · budget decision',
        'answer_form': 'Either a protocol plus unit access and dated result rows, or a written “no testing” that keeps the editorial ceiling where it is.',
    },
    {
        'id': 'P27-Q5',
        'question': 'What happens to a guide after it is published — and what would make us change it?',
        'known': 'The recorded cadence is one guide reviewed every 14 days, publication gated on evidence. The feed and sitemap are register-driven, so a new guide reaches both automatically. Production analytics is off, so no page has measured performance.',
        'missing': 'The trigger rules: what evidence would cause a rewrite, a merge, or a retirement, and who notices.',
        'default': 'Re-verify the sources of an existing guide before writing another one; never refresh a page by changing its date alone.',
        'discovery': 'Define three dated triggers: source page moved or removed, a Search Console report showing a query the guide does not answer, or a product listing withdrawn. Each one maps to a specific action in the register.',
        'blocks': 'A defensible refresh policy; retirement of pages whose sources went stale',
        'source': 'search-console',
        'answer_by': 'Owner · editorial decision',
        'answer_form': 'Three trigger rules written into the cadence note, each with the action it forces and where the evidence is stored.',
    },
    {
        'id': 'P27-Q6',
        'question': 'Is the Associates account actually enrolled, and does this site belong to it?',
        'known': 'The brief supplied the tracking ID “shopnow047c-20”. The repository has no account access, so assignment, standing and reports are unverified. Each of the five submitted links opened a product listing, which shows a destination, not an attribution.',
        'missing': 'Enrolment status, whether the ID belongs to the account, whether the site is registered in it, and the Amazon account-side view of the submitted short links.',
        'default': 'Leave FLG-003 unresolved. Do not call the supplied links invalid; do not call them validated. Keep intended identifiers separate from observed redirects.',
        'discovery': 'In the Associates account: confirm the site is listed, the tracking ID matches, and create one Special Link per product. Compare its destination with the observed one. Record the date and the outcome in the intent register — never paste account screenshots into the repository, they carry identifiers.',
        'blocks': 'Every revenue-adjacent statement; replacing submitted links; scaling to more products',
        'source': 'amazon-agreement',
        'answer_by': 'Owner · account access',
        'answer_form': 'A dated line per product: enrolled workflow, link created, destination matches intent, tracking ID shown in the URL parameter.',
    },
    {
        'id': 'P27-Q7',
        'question': 'Is the site two categories or one?',
        'known': 'Five submitted links, two categories: three air fryers and two meat thermometers, with six published guides split across them plus one seasonal piece. Amazon’s own breadcrumb on the air-fryer listing runs Home & Kitchen › Kitchen & Dining › Small Appliances › Fryers › Air Fryers.',
        'missing': 'Whether the thermometer listings stay in scope, and whether the site is a kitchen-tools publication or an air-fryer publication with a side table.',
        'default': 'Keep both categories under one kitchen brand and add no third category while traffic is unmeasured.',
        'discovery': 'Decide the scope before adding topics: a second category needs its own cluster of guides and its own pillar page, not one article sharing a front door with unrelated copy.',
        'blocks': 'Topic calendar, category pages, internal-link structure',
        'source': 'google-reviews',
        'answer_by': 'Owner · strategy decision',
        'answer_form': 'One sentence of scope, plus a yes/no on the two thermometer listings staying in the shortlist.',
    },
]

PATHS = [
    {
        'id': 'P27-P1',
        'name': 'Tighten the shop',
        'sequence': 1,
        'recommended': True,
        'pitch': 'Make the buyer experience sharper before spending anything on reach.',
        'changes': [
            'Front page, product cards and the guide index read as one edit, not a register',
            'A question router above the shortlist, so the reader picks the decision instead of the product',
            'One more question-led guide per review cycle, register-driven so feed and sitemap follow',
            'Mobile pass: type scale, 44px tap targets, table scroll with visible blanks',
        ],
        'needs': [],
        'unblocks': 'Reader trust, internal linking, and a guide that can stand on its own in search.',
        'cannot': 'It cannot produce a ranking, a tested verdict, or evidence that anyone arrived.',
        'cost': 'Low · a build pass inside this repository, no new access',
        'risk': 'Low · it adds no new claims, and the disclosure and sponsored rules are already gated',
        'basis': 'google-reviews',
        'status': 'Open · nothing external blocks it',
    },
    {
        'id': 'P27-P2',
        'name': 'Prove the money path',
        'sequence': 2,
        'recommended': True,
        'pitch': 'Confirm what each link is meant to be, then validate one Special Link per product before scaling.',
        'changes': [
            'Product-intent record filled with a dated confirmation per product, kept separate from the observed redirect',
            'Submitted short links replaced, one product at a time, by links generated in the enrolled workflow',
            'Card and CTA wording checked against the destination it actually names',
        ],
        'needs': ['P26-Q1', 'P26-Q2', 'P27-Q6'],
        'unblocks': 'Any statement about attribution, the FLG-003 review, and safe growth to more products.',
        'cannot': 'It cannot be done from the repository side. Only the Associates account can produce the evidence.',
        'cost': 'Small work, large value · needs the account owner, not a build',
        'risk': 'Medium · adding more unvalidated links is the one mistake that compounds',
        'basis': 'amazon-policies',
        'status': 'Blocked on owner',
    },
    {
        'id': 'P27-P3',
        'name': 'Turn on the lights',
        'sequence': 3,
        'recommended': True,
        'pitch': 'Measure arrival and departure before choosing the next topic from instinct.',
        'changes': [
            'A Search Console URL-prefix property for the Pages path, with the sitemap submitted',
            'The shipped collector deployed on a host you control, with request logging disabled and privacy flags verified',
            'Campaign ledger rows added only from dated first-party reports, each with its source named',
        ],
        'needs': ['P26-Q3', 'P26-Q4', 'P26-Q5', 'P27-Q2'],
        'unblocks': 'Demand-based topic selection and an honest answer to “did anyone arrive”.',
        'cannot': 'It cannot produce per-visitor attribution: associating a sub-tag or report row with a specific end user is prohibited.',
        'cost': 'Medium · a host, a read token, and a privacy review of the retention rules',
        'risk': 'Medium · this is the one path that adds a data-collecting surface, so it goes last among the three',
        'basis': 'search-console',
        'status': 'Blocked on hosting + owner',
    },
    {
        'id': 'P27-P4',
        'name': 'Earn the word “review”',
        'sequence': 4,
        'recommended': False,
        'pitch': 'Cook in the appliances and publish what happened, with dates, and only then say what you think.',
        'changes': [
            'A written protocol before any unit arrives, including how a failure is recorded',
            'Our own dated photography and measurement notes, captioned with who did it',
            'A “what it is like to live with” section that cites our own evidence, replacing nothing that is currently absent',
        ],
        'needs': ['P26-Q6', 'P26-Q7', 'P27-Q3', 'P27-Q4'],
        'unblocks': 'Tested comparisons, original evidence behind any “best” claim, and imagery that belongs to us.',
        'cannot': 'It cannot be simulated by rewriting listing copy. Without the protocol and the dated evidence, S-06 stays not adopted.',
        'cost': 'Large · units, kitchen time, photography, and a person who signs off',
        'risk': 'High · performance and safety sentences need evidence, and food-safety guidance must stay attributed to its source',
        'basis': 'ftc',
        'status': 'Needs a budget decision',
    },
    {
        'id': 'P27-P5',
        'name': 'Automate behind the gate',
        'sequence': 5,
        'recommended': False,
        'pitch': 'Scale intake and drafting, and let the release gate be the thing that says no.',
        'changes': [
            'Intake that records intended ASIN, official listing URL, confirmation date and source, with observed redirects in separate fields',
            'A draft queue that rejects any row without a dated official source',
            'One release command: disclosure, sponsored rels, provenance, feed and sitemap, link checks — before anything publishes',
        ],
        'needs': ['P26-Q1', 'P26-Q2', 'P26-Q6', 'P27-Q6'],
        'unblocks': 'More products and more guides without more manual bookkeeping.',
        'cannot': 'Automation cannot authorise an API, confirm product intent, or validate attribution. A confident draft is not evidence.',
        'cost': 'Medium–large · a pipeline pass plus someone to work the exceptions',
        'risk': 'High if the gate is loosened · the failure mode is volume of unverified claims',
        'basis': 'amazon-agreement',
        'status': 'Gated · build it after P27-P2',
    },
]

DESIGN_PROMPT = {
    'intro': 'Ten blocks, each doing one job. Paste the whole brief into a design tool or hand a designer one block at a time. Every block is grounded either in a rule already recorded in this repository or in an official policy page, and none of them asks you to assert a fact the site does not have.',
    'blocks': [
        {
            'id': 'job',
            'heading': '1 · The job of every page',
            'text': 'A reader arrives with a question about a thing on their counter. The page answers four things in this order: what the linked listing actually says, what it does not say, what the reader should check at home, and where the sponsored link goes. Anything unverified is left visibly absent, with the gap named. A page that cannot answer all four is a note, not a guide.',
            'basis': 'google-reviews',
        },
        {
            'id': 'voice',
            'heading': '2 · Voice, and the words this site does not use',
            'text': 'Second person, plain verbs, short sentences, one idea each. No “must-have”, “game-changer”, “obsessed”, “top-rated”, “we loved”, “In conclusion”, no countdowns, no invented urgency, no fake expert, no first-person experience of a product nobody used. Every product statement names the listing it came from, and the date it was read. The read-aloud test is the editor: a sentence you would not say at a dinner table gets rewritten.',
            'basis': 'ftc',
        },
        {
            'id': 'structure',
            'heading': '3 · Architecture, top to bottom',
            'text': 'Masthead → non-dismissible disclosure strip immediately under it → one editorial promise (not a value proposition) → the shortlist, filterable, cards carrying format illustration and the listing’s own words → a question router → the guide index → one seasonal cluster → a comparison table whose unverified cells are blank and labelled → footer that keeps the whole research set reachable in a single group. Product first, verification process second, always.',
            'basis': 'amazon-policies',
        },
        {
            'id': 'visual',
            'heading': '4 · Visual system',
            'text': 'Ivory canvas, deep green ink, one warm accent, hairline rules, generous rhythm. Serif display at 46–79px with tight leading, sans body at 15–17px with 1.8–1.95 line-height. Minimum 44px tap targets, visible focus ring, tables that scroll inside a labelled region. No gradient headline, no glass, no shadow soup, no card grid without a reason. Art is diagrammatic and generic, never a stand-in for a photograph of the SKU.',
            'basis': 'amazon-agreement',
        },
        {
            'id': 'imagery',
            'heading': '5 · What pictures are allowed here',
            'text': 'Two kinds only: a labelled AI editorial still life, and original format diagrams drawn for this site. No Amazon Program Content asset is downloaded or stored; no scraped photography; no image that implies a test result, a meal we cooked, or the exact look of a listed model. If real product photography ever appears, it is ours, dated, and captioned with who shot it.',
            'basis': 'amazon-agreement',
        },
        {
            'id': 'commerce',
            'heading': '6 · Disclosure, links and the things that must never be improvised',
            'text': 'The Associates statement appears under the masthead on every page and again in the footer. Every Amazon link carries rel="sponsored" and names its destination in the CTA copy. The tag-parameter requirement, the no-bookmarking rule and the no-association-of-sub-tags-with-users rule are treated as design constraints, not fine print. Prices and availability appear only where Amazon serves them or an API licence covers them. Any mention of a limited-time promotion inherits the duty to remove it when the promotion ends.',
            'basis': 'amazon-policies',
        },
        {
            'id': 'editorial',
            'heading': '7 · The editorial system',
            'text': 'One question per page, question-shaped titles, a short-answer box at the top, three body sections that each carry their source links, an explicit “what we have not established” block, and related reads that go somewhere a reader actually needs. Cadence: review one guide every 14 days; publish only through the gate. Keep the ladder honest — published, buildable from the listings already read, and held. A held piece stays held; softening the gate to ship it is how a publication becomes a content farm.',
            'basis': 'google-reviews',
        },
        {
            'id': 'topics',
            'heading': '8 · Topics that fit this shelf',
            'text': 'Write the buyer question the listing leaves open: what “Sync Finish” and “Hi-Fry” actually name, how quart counts mislead, whether two small baskets beat one big one, what a preset does when you press it, how to know a cook is done, what cleanup costs you in counter space, and how a probe changes a roast. Trending framing is allowed only as dated context (“it is hosting season”), never as a popularity claim, and never as a reason to invent a search-volume number.',
            'basis': 'google-reviews',
        },
        {
            'id': 'measurement',
            'heading': '9 · Measurement without a surveillance build',
            'text': 'Five first-party events, aggregate by UTC day, no cookies, no identifiers, no fingerprints, honouring Global Privacy Control, Do Not Track and Save-Data, and staying off until a durable host exists. A verified Search Console property and dated first-party reports are the only inputs that pick the next topic. A click is not an order; an order is not a trend.',
            'basis': 'search-console',
        },
        {
            'id': 'done',
            'heading': '10 · Definition of done',
            'text': 'The documented chain runs twice and the second run changes nothing; every gate passes; every current table row carries a dated official source or an honest blank; no page loses its disclosure or its sponsored rel; the deployed page is fetched and read back. Then re-measure the counts — pages, guides, sources, flags — and put both readings in the register. “Polished” has to be a number that moved, not a sentence in a changelog.',
            'basis': 'github-pages',
        },
    ],
}

GUIDES = [
    {
        'slug': 'air-fryer-label-words',
        'title': 'What do “Hi-Fry”, “Sync Finish” and “4-in-1” actually promise?',
        'short_title': 'What the words on an air-fryer listing promise.',
        'dek': 'Three marketing names from three listings, read closely — what each one says, and the question it leaves you to answer yourself.',
        'category': 'Air fryers',
        'category_slug': 'air-fryers',
        'type': 'Reading the label',
        'art': 'functions',
        'published': '2026-11-19',
        'products': ['SHOP-01', 'SHOP-02', 'SHOP-03'],
        'takeaway': 'These are names inside product titles, not standards with a definition we can read from the listing. Quote the words, expect the manual to carry the meaning, and treat any performance promise as the brand’s claim rather than ours.',
        'sections': [
            {
                'heading': 'Start with what each title actually says.',
                'paragraphs': [
                    'The CHEFMAN dual-basket listing names “Sync Finish, Hi-Fry, Auto Shutoff” among its features. The Chefman TurboFry listing names a “4-in-1” with a “450°F Hi-Fry Option for Crispier Results”. The Emeril Lagasse listing names “Multi-Function”, “24 One-Touch Preset Options”, “Extra Large Interior” and “Six Cooking Accessories Included”. Those are the words on the page; a page title is not a specification sheet.',
                    'Notice that the same word travels. “Hi-Fry” appears as a bare feature in one listing and as a named temperature option in another. Before you decide what it is worth, ask the question that only the exact model can answer: what does the control actually change — temperature, time, fan speed, or a preset that does all three?'
                ],
                'checklist': [
                    'Which of these words appear in the title, and which appear only in a spec table?',
                    'Does the feature have a number attached, or is it a name with no stated behaviour?',
                    'Do two listings in the same shortlist use one word for two different things?',
                    'Is the accessory or setting required for that feature present in the box?',
                ],
                'source_ids': ['SHOP-01', 'SHOP-02', 'SHOP-03'],
            },
            {
                'heading': 'A preset count and a function count are not the same number.',
                'paragraphs': [
                    '“24 One-Touch Preset Options” and “4-in-1” are counting different things. One counts programmes; the other counts advertised cooking modes, and the TurboFry title names three of them in words you can read: bake, dehydrate, frozen. Neither number tells you how a preset behaves, whether it can be adjusted, or what happens when you override it.',
                    'So the useful comparison is not which listing has the bigger number. It is whether you can see, for the exact model, what each mode sets, whether a mode needs an accessory that is in the box, and where the instructions live when you want the definition rather than the label.'
                ],
                'source_ids': ['SHOP-02', 'SHOP-03'],
            },
            {
                'heading': 'What a listing word cannot do.',
                'paragraphs': [
                    'It cannot become a claim by us. Amazon’s Program Policies prohibit inaccurate, overbroad, deceptive or otherwise misleading statements about a product, and the FTC is blunt about experience: you cannot talk about a product you have not tried. That is why this guide quotes titles and stops there. “Nonstick dishwasher-safe baskets” is the brand’s wording about its own listing; whether your dishwasher, your rack position and your usage match that wording is a manual-and-common-sense check, not something we can confirm from a title.',
                    'We have not tested any of these three appliances, and we are not verifying the brand’s claims by repeating them. Where the label is the only source, the label is what we show.'
                ],
                'source_ids': ['SHOP-01', 'amazon-policies', 'ftc'],
            },
        ],
        'unknowns': [
            'What “Sync Finish”, “Hi-Fry”, “Auto Shutoff” or any preset does mechanically on a specific model.',
            'Whether the named temperature option changes peak temperature, cook time, or both.',
            'Whether a claimed accessory, mode or feature is required for the result described in the title.',
            'Any performance outcome: crisping, evenness, noise, cleanup effort or durability. Nothing here was tested.',
        ],
        'related': ['capacity-checklist', 'basket-or-oven-style', 'cleanup-and-counter-space'],
    },
    {
        'slug': 'how-do-you-know-its-done',
        'title': 'How do you know when an air-fryer cook is actually done?',
        'short_title': 'Is it done? Check the food, not the timer.',
        'dek': 'A beep says time passed. A temperature says the food reached a target. Here is how to separate the two without owning a lab.',
        'category': 'Everyday kitchen',
        'category_slug': 'everyday-kitchen',
        'type': 'A kitchen habit',
        'art': 'thermometer',
        'published': '2026-11-19',
        'products': ['SHOP-01', 'SHOP-04', 'SHOP-05'],
        'takeaway': 'Use the appliance for heat and a thermometer for the decision. FoodSafety.gov publishes minimum internal temperatures by food; check against those, and treat any doneness cue from the appliance as a starting point rather than a verdict.',
        'sections': [
            {
                'heading': 'Separate “cooking finished” from “safe to eat”.',
                'paragraphs': [
                    'FoodSafety.gov’s chart is blunt: use a food thermometer to check that food has reached a safe minimum internal temperature, and note that some meats also need rest time so the innermost parts finish cooking. Its figures for the foods a kitchen air fryer is usually asked for: chicken, turkey and other poultry 165°F (74°C); ground meat and sausage 160°F (71°C); beef, bison, veal, goat and lamb steaks, roasts and chops 145°F (63°C) with a three-minute rest; casseroles and leftovers 165°F (74°C).',
                    'That chart is a food-safety reference, not a recipe, and we are reproducing it rather than restyling it: it was last reviewed 21 Nov 2024 by the source, and it is the kind of page worth reading before you decide what to look for.'
                ],
                'source_ids': ['food-safety'],
            },
            {
                'heading': 'What the listing can tell you about signals — and what it cannot.',
                'paragraphs': [
                    'The CHEFMAN dual-basket title names “Auto Shutoff”. A shut-off behaviour is a safety and convenience feature; it is not a doneness test, and the title does not say what triggers it. The Chefman TurboFry title names a “450°F Hi-Fry Option for Crispier Results”, which is a claim about a result, not a measurement you can read off the food.',
                    'So the appliance can end the cycle. It is the food that answers the question. If a timer, a beep and a thermometer disagree, trust the thermometer — and then write down what you found, because that note is worth more next season than a remembered impression.'
                ],
                'source_ids': ['SHOP-01', 'SHOP-03'],
            },
            {
                'heading': 'A checking routine that survives a real dinner.',
                'checklist': [
                    'Check the thickest part, away from bone and away from the pan surface.',
                    'Let the reading settle before you record it — and record it, with the food and the setting you used.',
                    'Clean the probe between raw and ready-to-eat food.',
                    'Confirm the maximum temperature your thermometer allows in an appliance before you leave it in one; check the exact model’s instructions rather than a listing title.',
                    'If the target is not reached, keep cooking and check again. Rest time counts for some meats, so measure after it, not instead of it.',
                    'Reheat leftovers to the figure the chart gives for leftovers, not to “warm through”.',
                ],
                'source_ids': ['food-safety', 'SHOP-04', 'SHOP-05'],
            },
        ],
        'unknowns': [
            'How accurate or fast either listed thermometer is; none of that was tested here.',
            'Whether a specific air-fryer model signals completion in a way that matches its timer.',
            'Cooking times for any food in any of these appliances. No timing table is claimed from a listing.',
            'Whether an appliance’s stated temperature equals the food’s temperature at the probe.',
        ],
        'related': ['instant-read-or-wireless-thermometer', 'holiday-kitchen-checklist', 'air-fryer-label-words'],
    },
]

INTAKE = {
    'title': 'The shape a new suggestion has to take',
    'note': 'Anyone proposing work for this site — including a build session — writes it in this shape. It is what makes two suggestions comparable, and it is what stops a confident paragraph from becoming a plan.',
    'fields': [
        ('What changes', 'One sentence a reader would notice, not a component name.'),
        ('Why now', 'The problem it removes, in evidence terms.'),
        ('Evidence needed', 'The question IDs from the register below that must be answered first.'),
        ('Official basis', 'A link to the rule or guidance that shapes the option.'),
        ('Safe default', 'What the site does if nobody ever answers.'),
        ('Gate', 'Open, blocked on owner, blocked on evidence, or needs a budget decision.'),
    ],
}


def main() -> None:
    data = json.loads(PUB.read_text(encoding='utf-8'))

    # Guard first, before any mutation: replaying this file would double-append the guide and
    # question rows. On a rebased branch the new base has no `paths`, so the guard passes once.
    if 'paths' in data or 'design_prompt' in data or 'suggestion_intake' in data:
        raise SystemExit('P27 rows already present: this update is one-shot; it must not be replayed')

    q_ids = {q['id'] for q in data['questions']}
    for q in data['questions']:
        by, form = OWNERS.get(q['id'], ('Owner', 'A dated decision or a dated first-party record, recorded in this register.'))
        q['answer_by'] = by
        q['answer_form'] = form
    for q in NEW_QUESTIONS:
        if q['id'] in q_ids:
            raise SystemExit(f'duplicate question id {q["id"]}')
        # The gate (tools/check_publication.py, added by PR #175) requires every question row to
        # state whether only the account holder can unblock it, alongside the four prose fields.
        q.setdefault('owner_input_needed', q.get('answer_by', '').startswith('Owner'))
        data['questions'].append(q)

    if 'paths' in data:
        raise SystemExit('paths already present: this update is one-shot; it must not be replayed')
    data['paths'] = PATHS

    if 'design_prompt' in data:
        raise SystemExit('design_prompt already present: this update is one-shot; it must not be replayed')
    data['design_prompt'] = DESIGN_PROMPT

    slugs = {g['slug'] for g in data['guides']}
    for g in GUIDES:
        if g['slug'] in slugs:
            raise SystemExit(f'duplicate guide slug {g["slug"]}')
        data['guides'].append(g)
        data['indexable_pages'].append(f'guides/{g["slug"]}.html')

    data['suggestion_intake'] = INTAKE
    data['meta']['decision_desk'] = {
        'session': '6b68afc8',
        'updated': '2026-11-19',
        'note': 'Paths are bundles of proposals with their dependencies made visible. A path choice is a review note in the reader’s browser; it is not an implementation request and it never publishes.',
    }

    # Only the six pages actually fetched again on 2026-11-19 by this pass get a re-read note.
    # The other source rows keep their recorded date and scope; they were not re-opened today.
    scopes = {
        'amazon-agreement': 'Re-read 19 Nov 2026 (decision-desk pass), chunk 1 of 4: §5 “You must clearly and prominently state… As an Amazon Associate I earn from qualifying purchases”, §6 treating any §5 violation as a material breach, and the no-traffic-or-income-representation sentence in §4. Header: updated October 15, 2025.',
        'amazon-policies': 'Re-read 19 Nov 2026 (decision-desk pass), chunk 3 of 11: 1(f)/(g) child-directed and Amazon-trademark-in-identifier bans; 2(a) Special Links enable tracking and must use the assigned Associates ID; 2(b) tag parameter, no bookmarking inducement, sub-tag must not map to an end user, original content required on listing pages, promotion-removal duty, no inaccurate/overbroad/misleading claims, price display only via an Amazon-served link or a licensed API. Header: updated April 14, 2026.',
        'ftc': 'Re-read 19 Nov 2026 (decision-desk pass), whole page: place the disclosure with the endorsement so it is hard to miss; simple wording; you cannot talk about your experience with a product you have not tried. Dated November 2019.',
        'google-links': 'Re-read 19 Nov 2026 (decision-desk pass): sponsored marks advertisements or paid placements; marked links are generally not followed. Page last updated 10 Dec 2025.',
        'github-limits': 'Re-read 19 Nov 2026 (decision-desk pass): Pages is not intended for or allowed as free hosting for an online business, e-commerce site or any site primarily directed at facilitating commercial transactions; 1 GB published site, soft 100 GB/month bandwidth, 10 builds/hour.',
        'food-safety': 'Re-read 19 Nov 2026 (decision-desk pass): poultry 165°F (74°C); ground meat and sausage 160°F (71°C); beef/bison/veal/goat/lamb and pork steaks, roasts and chops 145°F (63°C) with a three-minute rest; casseroles and leftovers 165°F (74°C); fish 145°F (63°C). Date last reviewed 21 Nov 2024.',
    }
    for s in data['sources']:
        if s['id'] in scopes:
            s['scope'] = scopes[s['id']]
            s['checked_on'] = '2026-11-19'

    # P27-F04: a proposal row must not assert a count the register owns.
    for prop in data['proposals']:
        if prop['id'] == 'P26-S3' and 'six linked guides' in prop.get('next', ''):
            prop['next'] = prop['next'].replace('the six linked guides', 'the linked guides in this register')

    PUB.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'questions {len(data["questions"])}; paths {len(data["paths"])}; '
          f'design blocks {len(data["design_prompt"]["blocks"])}; guides {len(data["guides"])}; '
          f'indexable {len(data["indexable_pages"])}')


if __name__ == '__main__':
    main()

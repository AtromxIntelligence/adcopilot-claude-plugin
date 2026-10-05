---
name: adcopilot-review
description: Read a Google Ads account and say what happened, what it cost, what is wasting money and what to change — then propose the change and apply it when the customer says yes. Use whenever the user asks how their ads are doing, for a status, a check, an update, a report or a summary; asks about spend, clicks, impressions, results, cost per result or budget; asks which keywords or searches are wasting money, what is working, what to pause or fix; or asks what they should do next about their ads. This is the everyday skill — reach for it before answering any performance question from memory.
---

# AdCopilot review

The customer asked how their advertising is doing. Answer the whole question in
one pass, through the AdCopilot connector at `https://mcp.adcopilot.cloud/mcp`.
A thin answer is the failure here. Reads are the cheap part; a customer who has
to ask four follow-up questions to learn what one answer could have told them
has been short-changed.

Call `get_org_context` first, before any other tool, and follow its
`next_step`, `playbook` and `cross_reads` — they carry the read ceiling for this
account's situation and the house rails. Everything below runs inside them.

## Spend the reads you are given

`cross_reads.ads_reads_max` is a ceiling, not a target to stay under. Use it.
The account's own numbers are what make the answer true, and a number you did
not read is a number you must not state. Never trim the read list to be
economical — if a read would have changed what you say, make it.

What you cannot read, say you cannot read. Never estimate a figure, and never
carry one over from an earlier turn as if it were fresh.

## The sequence

**Open with `full_audit`.** One lens is ONE read and answers what a dozen
hand-written queries would: it ranks the wasted spend, names the
negative-keyword candidates and finds the disapprovals, from the account's own
numbers. The shipped audit prompt says the same thing — "if the connector
exposes `full_audit`, call it instead of computing this yourself; quote its
numbers" — so steps 2, 3 and 5 below are usually already answered when it
returns. Read them yourself only for what it did not cover.

Then, in this order, stopping only when the ceiling is reached:

1. **The period against the one before it.** Campaign metrics by day for the
   last fourteen days (`search` over `campaign`, with `segments.date`), folded
   into two weeks so every headline number has a comparison. No lens returns a
   time series, so this read is yours to make.
2. **Where the money went inside that.** Which campaigns and which keywords
   carried the spend, and which carried the results (`keyword_view`) — unless
   `full_audit` already ranked it.
3. **What was paid for that should not have been.** The search terms with cost
   and no conversions, worst first — usually the largest finding.
   `analyze_search_terms` is one read for six query shapes and all six
   negative-keyword themes, so prefer it over `search_term_view` by hand.
4. **Whether delivery is being held back.** `budget_pacing` — one read for the
   month-to-date projection against each daily budget. A campaign at its cap
   every day is turning away traffic the customer is willing to pay for, and
   they cannot see it from the dashboard.
5. **Whether anything is switched off by Google.** Disapproved ads, and whether
   results are being counted at all (`conversion_setup_audit` is one read for
   what is counted and what is aimed at). An account counting nothing makes
   every other number meaningless, so say that first if it is true.

Read the account, never the profile's memory of it. A saved note is context for
your wording, never a substitute for a read.

## The answer

**One headline line.** Spent, clicks, results, cost per result — each against
the period before, in the account's own currency, from the `*_display` values.
Never divide micros yourself.

**Then at most three findings, biggest money first.** Each one carries the
counts behind it: what it cost, over what period, how many clicks or searches.
A finding without a number is an opinion.

**Then one recommendation**, with the money spelled out both ways — what it
costs to act and what it costs to do nothing — as a proposal they say yes or no
to. Never apply it first.

Say what each finding means in plain words the first time it appears. "Search
terms" are the things people actually typed; "negative keywords" are the words
you tell Google never to match. Teach on the step being taken, and say what the
step unlocked, or will unlock once they have done it.

## When they say yes

Apply it, then say exactly what changed and how to undo it, and record it with
`save_org_context` as a decision — what was approved, in the customer's own
framing, and which campaign it touched.

Negatives go on with `add_negative_keywords` at PHRASE match using the search as
typed, unless a broader word is plainly safe. Read them back before claiming
they are live. **AdCopilot cannot remove a negative it added** — only the Google
Ads screens can — so never tell a customer a negative is reversible here.

Campaigns and keywords are paused, never removed. A campaign you built is never
switched on by you.

## What breaks

Answering from the probe's summary alone: it carries a thirty-day total and
nothing about which search terms wasted money, so the answer sounds informed and
helps with nothing. Reporting a number without its comparison: "₹8,700 last
week" means nothing until it sits next to the week before. Proposing negatives
without reading the terms they block: a phrase negative is a blunt instrument
and a careless one blocks searches the customer wants.

## What is next

Offer, in this order: the first fix as a change you will make now; the
never-show-for words you found; and a recurring check-in so the next review
happens without them asking.

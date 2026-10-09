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

Call `get_org_context` with `source: "claude-plugin/0.2.8"` first, before any
other tool — the marker is how the server records that this workspace uses the
plugin, and without it the customer keeps being told to install what they
already have. Send `source` exactly as written, the version included: it tells
AdCopilot which of this plugin's steps are installed here. When the answer's
`plugin.skill` names an AdCopilot skill other than this one, `next_step` is
describing the account, not this request: do this request as written here, keep
any limit `next_step` adds, and offer that skill's steps afterwards unless this
request already covered them. Then follow the answer's `next_step`, `playbook`
and `cross_reads` — they carry the read ceiling for this account's situation
and the house rails. Everything below runs inside them.

On an account with campaigns to read — the answer's situation is
`ADS_DORMANT`, `ADS_ACTIVE_UNTRACKED` or `ADS_ACTIVE_TRACKED` — the answer also
carries `question_map`: for each kind of question, the read that answers it
(wasted spend, search terms and negatives, keywords, ads, budget, results
changed, tracking, what to do). Use it to choose the first read for a question that is
narrower than the whole account. It is absent when there is nothing to read, so
when it is missing the list below stands in for it.

## Spend the reads you are given

`cross_reads.ads_reads_max` is a ceiling, not a target to stay under. Use it.
The account's own numbers are what make the answer true, and a number you did
not read is a number you must not state. Never trim the read list to be
economical — if a read would have changed what you say, make it.

On a day with few look-ups left, `cross_reads` also carries `reads_left_today`,
and `ads_reads_max` has already been sized to leave room for the fix: spend
those reads, then propose. The change they say yes to, and its read-back, are
what the rest of the day is for.

What you cannot read, say you cannot read. Never estimate a figure, and never
carry one over from an earlier turn as if it were fresh.

## Follow `related_reads`

When a lens or `search` result ends with `related_reads`, run the ones that bear
on the question, at most three, then answer from all you hold. Each names its
tool, its arguments and a `why` built from the numbers of the result you just
read; skip one that does not bear on what the customer asked. Never repeat a
read you hold. Offer, do not chase, the `related_reads` those reads bring back.
They are reads only: a change still waits for the customer's yes. The ceiling
above still holds: if it is reached before a related read, say which one you did
not run. In a scheduled run, skip them.

## The sequence

**Open with `full_audit`, with `depth="deep"` and `days` set to the window you
are reporting.** Its default is `quick`, which scores three of the
seventy-three checks over the month to date — not an audit, and not what the
customer asked for. Deep attempts all seventy-three over your window and reports
how many it could actually evaluate; say that number rather than letting an
unevaluated check pass as a pass.

One lens is ONE read and answers what a dozen hand-written queries would. It
orders its findings by severity, NOT by money, so re-sort by cost before you
choose the three you report. For the cost ranking itself, `analyze_waste` is the
read; `analyze_search_terms` groups the searches into negative-keyword
candidates by theme, which is a different job. Together they usually answer
step 3 below, so read it yourself only for what they did not cover.

A question narrower than the whole account starts with the lens that answers it
rather than with `full_audit`: `analyze_waste` for money spent on nothing,
`analyze_search_terms` for negatives, `keyword_opportunities` for keywords worth
adding or fixing, `quality_score_breakdown` for ad rank and Quality Score,
`rsa_asset_report` for the ad copy, `bidding_audit` for how campaigns bid,
`day_of_week` for which days and hours earn, `budget_pacing` for budgets,
`change_history` for what changed and who changed it, and
`conversion_setup_audit` for what is counted. Do not write a `search` for what
one of these already returns: the lens reads the account the way Google counts
it, and a hand-written query reads one slice of it.

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
   negative-keyword themes: use it, never `search_term_view` written by hand.
4. **Whether delivery is being held back.** `budget_pacing` — one read for the
   month-to-date projection against each daily budget. A campaign at its cap
   every day is turning away traffic the customer is willing to pay for, and
   they cannot see it from the dashboard.
5. **Whether results are being counted at all.** `conversion_setup_audit` is one
   read for what is counted and what is aimed at. An account counting nothing
   makes every other number meaningless, so say that first if it is true.
6. **Whether anything is switched off by Google, and what changed.** Disapproved
   ads are a `search` on `ad_group_ad` (no lens returns them). When spend,
   results or cost per result moved against the period before, `change_history`
   says what was changed in the account, when, by which Google login and through
   which channel; when nothing moved, leave it. It keeps thirty days and omits
   Google Ads Editor changes and some rows, so a quiet log does not prove
   nothing changed; say that when the numbers moved and the log shows no cause.

Read the account, never the profile's memory of it. A saved note is context for
your wording, never a substitute for a read.

## The answer

**One headline line.** Spent, clicks, results, cost per result — each against
the period before, in the account's own currency.

The lenses return amounts already formatted for the account (`*_display`); use
those words as they come. A raw `search` does not — it returns
`metrics.cost_micros`, which is millionths. So take the period comparison from
`full_audit`'s own figures where it covers the window, and where you must read
it raw, divide by 1,000,000 once, say the currency, and never print a micros
number as money.

**Then at most three findings, biggest money first.** Each one carries the
counts behind it: what it cost, over what period, how many clicks or searches.
A finding without a number is an opinion.

**Then one recommendation**, with the money spelled out both ways — what it
costs to act and what it costs to do nothing — as a proposal they say yes or no
to. Never apply it first.

For two to three weeks after anything went live — a campaign switched on, or a
change to how it bids or what it counts — recommend no bidding change: Google's
bidding is still learning, and a change starts it over. The one exception is a
campaign getting no traffic, where Maximize Clicks with a per-click cap is the
fix.

Say what each finding means in plain words the first time it appears. "Search
terms" are the things people actually typed; "negative keywords" are the words
you tell Google never to match. Teach on the step being taken, and say what the
step unlocked, or will unlock once they have done it.

## When they say yes

A yes counts when it is given here, to the change as you stated it, on today's
numbers. A fix agreed in an earlier conversation is read again and proposed
again before anything is applied; nothing carries over.

Apply it. Then read back only what its own result does not show — a status,
negatives once Google has normalised them, locations by the name Google shows —
and call nothing live until a read says so. Say exactly what changed and how to
undo it, and record it with `save_org_context` as a decision — what was
approved, in the customer's own framing, and which campaign it touched. A fix
they did not say yes to is recorded, if at all, as proposed and not applied;
never as approved.

Then propose the next finding's fix the same way: the change, its money both
ways, a yes or a no. One at a time, biggest money first. When nothing left is
worth its money, say so and stop proposing.

Negatives go on with `add_negative_keywords` at PHRASE match using the search as
typed, unless a broader word is plainly safe. Read them back before claiming
they are live. A negative can be taken back out through AdCopilot — there is a
removal behind each of the three ways to add one, under the same yes — so it is
reversible, and you may say so.

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

Before any yes, offer, in this order: the first fix as a change you will make
now; and the never-show-for words you found. After a yes, the next offer is the
next fix, as above.

Then the daily habit, on the same terms every other flow uses it — one offer, the
last line of the reply, at most once in a conversation, and only when all three
hold: Google Ads is connected and readable, the account has a campaign switched
on, and `get_org_context` reports no schedule. It reports one when
`routine.daily.status` is `user_set`, when `routine.scheduled_last_seen_at`
holds a date, or when `routine.own_schedule` is `saved` or `unavailable`.
AdCopilot's own emailed check-in (`routine.daily.status` `in_app`) is not
their schedule. If the server's `next_step` also asks for a
check-in offer, this one answers it — never two. On a yes, follow the
`adcopilot-daily` skill's set-up rather than inventing steps here. Its moment is
the reply in which a change they approved first reads as live; otherwise the
close. Leave it for another day when the reply ends on something they must fix
first.

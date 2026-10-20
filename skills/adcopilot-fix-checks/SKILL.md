---
name: adcopilot-fix-checks
description: Fix the checks an AdCopilot audit flagged, one at a time, inside today's allowance, with one yes/no at a time and each change read back. Use when the message is a question from AdCopilot's audit page or emails, such as "My AdCopilot audit of Google Ads account 123-456-7890 flagged three checks to fix first", "failed" or "warned on" a check, naming each check with its ID in brackets ((G18), (G43), (G-WS1)), or when the customer asks to fix, explain or go through the checks an AdCopilot audit found.
---

# AdCopilot fix-checks

The customer pressed a button on their AdCopilot audit and sent its question:
one or more checks, each by its name and its ID, for one Google Ads account.
The audit already ran. Your job is the fixes: one check at a time, inside what
today allows, with one yes/no at a time and a read-back after every change.
Run no new audit for it.

Call `get_org_context` with `source: "claude-plugin/0.2.14"` first, before any
other tool. Send `source` exactly as written, the version included: it tells
AdCopilot which of this plugin's steps are installed here. When the answer's
`plugin.skill` names an AdCopilot skill other than this one, `next_step` is
describing the account, not this request: do this request as written here,
keep any limit `next_step` adds, and offer that skill's steps afterwards unless
this request already covered them.

The account is the one the question names (written 123-456-7890). Use it only
if `get_org_context` reports it among the accounts switched on here; if it is
not, say so in one line and stop.

## First, what today covers

Before the first read, say in one line what the fixes cost and what is left,
from `get_org_context`'s `org.ops_today_cap` and `org.ops_today_used`: "These
3 checks take about 9 operations; you have 10 left today." Count each check as
its read plus a change and its read-back: about 3 operations where every call
counts 1, about 4 where an analysis counts 2 (each result says what it used).
When `org.ops_today_cap` is null there is no daily limit: say all of them fit,
and nothing else about an allowance.

Then the order. Foundation first: a check about counting results (conversion
tracking, G42 to G49 and G-CT1 to G-CT3) before anything judged by those
results, then what stops money going out (searches and keywords that spend with
nothing to show), then the rest. Recommend the order yourself and say it in the
same line; never ask the customer to pick it. Keep two operations for applying
and reading back the fix they approve. When the day cannot cover every check,
say which fit today and start with those.

Before a call that would use the last of today's operations, say what it covers
and ask first, in one line: "This next look uses 2 of your last 2 operations
today. It covers the zero-conversion keywords; after it nothing more can be
applied until the count resets. Go ahead?"

## Each check, by its family

**Searches to block** (G13 to G19, G14's lists, the O-NEG checks; G18, close
variant pollution, is one). Read `analyze_search_terms` with `days` set to the
audit's window (30 when the question does not say). Show the top searches
behind the check with what each cost, then propose blocking them as
never-show-for words (negative keywords), each Exact or Phrase, as one yes/no.
These are the `/adcopilot:negatives` steps: on a yes, `add_negative_keywords`
for a campaign or `add_account_negatives` for the account's list, then read
them back by the words Google shows.

**Keywords that spend and convert nothing** (G-WS1, zero-conversion keywords;
the waste family). Read `analyze_waste` and show the keywords that spent with
no conversion, costliest first. Propose pausing them as one yes/no for the set
("Shall I pause these 4? Reply yes, or name any to keep."): `update_keyword`
with `status` PAUSED for each, its ad group and criterion IDs from the result
or from a `search` on `keyword_view`. Pause, never remove. When the account
counts no conversions at all, they are the costliest keywords, not proven
waste: say so, and propose the tracking fix first.

**Counting results** (G42 to G49, G-CT1 to G-CT3; G43, enhanced conversions,
is one). Read `conversion_setup_audit` and say in plain words what is wrong.
What AdCopilot can change itself, propose, through the `adcopilot-measure`
skill's steps. What only Google Ads' own screens can change (enhanced
conversions is switched on there, under Goals, then Settings, with Google's
customer data terms), give as clicks, one step at a time, waiting for each;
read `conversion_setup_audit` again once they say it is done, and say what it
now shows.

**Any other check.** The question names the lens to read with ("Using
AdCopilot's ..."); use that one, or the read `question_map` gives for its kind
of question. Read only what the fix needs, then propose the fix.

When a lens or `search` result ends with `related_reads`, run at most one that
bears on the check in hand, then answer. Never repeat a read you hold, and
offer, do not chase, the `related_reads` it brings back. They are reads only: a
change is still only proposed. In a scheduled run, skip them.

A finding that says "if X" is not a step until you have checked X. Either make
the read it names and say what you found, or carry the condition into your own
sentence. Never turn it into an instruction.

## One message, one decision

- One check per message. Name it, say what the read found with its numbers and
  its money in the account's currency, and propose its fix.
- Show at most 5 rows of any list, costliest first, then "and N more; ask to
  see them".
- End each message with exactly one question: a yes/no on the fix you
  recommend ("Shall I block these 6? Reply yes, or name any to keep."). No
  numbered menu, no second question; anything else that needs their call waits
  for the next message.
- In Claude Code, put that yes/no to them with the AskUserQuestion tool when you
  have it, with the same options in the same words.
- Change nothing until they say yes to the change as you stated it, here, on
  today's numbers.

## After each yes

Apply it. Then read back only what its own result does not show (negatives as
Google normalised them, a keyword's status), in one line, say how to undo it,
and record it with `save_org_context` as a decision: what was approved, in the
customer's own framing, and which campaign it touched. Then the next check, the
same way. When the last one is done, or nothing left is worth its money, say so
and stop proposing.

Once a fix is applied and read back, and `get_org_context` handed you its
recipe, `routine.schedule`, make the daily-habit offer the way the
`adcopilot-review` skill words it, in a message of its own. Never before a fix
is checked, and never in the same message as a yes/no.

## When the day runs out

A call refused at the daily limit did not run. Give what you already found
first, in a few lines, then the one line the refusal asks for, with any price
exactly as it is written there. Retry nothing: the fix waits for the reset.

---
name: adcopilot-fix-checks
description: Fix the checks an AdCopilot audit flagged, one at a time, with one yes/no at a time and each change read back. Use when the message is a question from AdCopilot's audit page or emails, such as "My AdCopilot audit of Google Ads account 123-456-7890 flagged three checks to fix first", "failed" or "warned on" a check, naming each check with its ID in brackets ((G18), (G43), (G-WS1)), or when the customer asks to fix, explain or go through the checks an AdCopilot audit found.
---

# AdCopilot fix-checks

The customer pressed a button on their AdCopilot audit and sent its question:
one or more checks, each by its name and its ID, for one Google Ads account.
The audit already ran. Your job is the fixes: one check at a time, with one
yes/no at a time and a read-back after every change.
Run no new audit for it.

Call `get_org_context` with `source: "claude-plugin/0.2.17"` first, before any
other tool. Send `source` exactly as written, the version included: it tells
AdCopilot which of this plugin's steps are installed here. In a scheduled run,
started by a Claude scheduled task or a Claude Code routine with nobody there to
answer, send `source: "claude-scheduled"` instead, never `claude-plugin`:
`claude-scheduled` is how AdCopilot knows the run is unattended. When the answer's
`plugin.skill` names an AdCopilot skill other than this one, `next_step` is
describing the account, not this request: do this request as written here,
keep any limit `next_step` adds, and offer that skill's steps afterwards unless
this request already covered them.

The account is the one the question names (written 123-456-7890). Use it only
if `get_org_context` reports it among the accounts switched on here; if it is
not, say so in one line and stop.

## First, the order

Foundation first: a check about counting results (conversion tracking, G42 to
G49 and G-CT1 to G-CT3) before anything judged by those results, then what
stops money going out (searches and keywords that spend with nothing to show),
then the rest. Recommend the order yourself and say it in one line; never ask
the customer to pick it. Fix them in that order, one at a time, until they are
done or a call is refused.

If their question asks first what today's allowance covers, answer that in
one line before the first read: roughly what the fixes take (each check is
its read, its change and one read-back) and `org.ops_today_used` of
`org.ops_today_cap`, or, when the cap is null, that there is no daily limit.
That line answers their question; it never leaves a check out. Without
`cross_reads.reads_left_today`, nothing about the day is short: never count
it down yourself, never hold back a fix to save operations, and never ask
first because few are left.

## Each check, by its family

**Searches to block** (G13 to G19, G14's lists, the O-NEG checks; G18, close
variant pollution, is one). Read `analyze_search_terms` with `days` set to the
audit's window (30 when the question does not say). Show the top searches
behind the check with what each cost, then propose blocking them as
never-show-for words (negative keywords), each Exact or Phrase, as one yes/no.
Apply them the way the `/adcopilot:negatives` command does, with the read you
already hold; do not start that command, which reads the last seven days
again: on a yes, `add_negative_keywords` for a campaign or
`add_account_negatives` for the account's list, then read them back by the
words Google shows.

**Keywords that spend and convert nothing** (G-WS1, zero-conversion keywords;
the waste family). Read `analyze_waste` and show the keywords that spent with
no conversion, costliest first. Propose pausing them as one yes/no for the set
("Shall I pause these 4? Reply yes, or name any to keep."): `update_keyword`
with `status` PAUSED for each, one call a keyword, its ad group and criterion
IDs from the result or from a `search` on `keyword_view`. Pause, never remove. When the account
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

A finding may carry its fix in `recommended_actions`. One whose `kind` is
`tool` is a ready call, its IDs read from the account (an audit's negatives
are Exact, and never one of the customer's own keywords): propose it as it
stands, with the condition its `why` gives (a disapproved ad's pause is for
an ad they won't fix, never one Google approves on appeal). One whose `kind`
is `skeleton` is a draft: it names the tool and the IDs, and `needs` says what
only the customer can give, such as the searches to block, a callout's words
or the campaign to take budget from. Ask for that in your one question, and
never fill it in yourself.

## One message, one decision

- One check per message. Name it, say what the read found with its numbers and
  its money in the account's currency, and propose its fix.
- Show at most 5 rows of any list, costliest first, then "and N more; ask to
  see them".
- End each message with exactly one question: a yes/no on the fix you
  recommend ("Shall I block these 5? Reply yes, or name any to keep."); a yes
  covers only the rows you showed. No numbered menu, no second question;
  anything else that needs their call waits for the next message.
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

Once the first fix is applied and read back, and `get_org_context` handed you
its recipe, `routine.schedule`, make the daily-habit offer in that reply, as
"The daily habit" below says: in place of the next check's yes/no, with the
next check named in one line, and its yes/no in the reply after. Never before a
fix is checked, and never in the same message as a yes/no.

## When the day runs out

A call refused at the daily limit did not run; a result that says the daily
limit is now reached ran, and used the day's last operation. Either way, give
what you already found first, in a few lines, then, every time, the one line
the refusal or that result gives, word for word: the plan, its daily
operations, its price exactly as written, the offer when it names one, the
owner when it names one, and its link when it gives one, with the reset. Retry
nothing: the fix waits for the reset.

## The daily habit

This block is repeated verbatim in every AdCopilot skill and command a person runs; change all eight together.

First, Cursor. If this is Cursor (`get_org_context`'s top-level `surface` is `cursor`, or Cursor's own instructions or the person say so), make no schedule offer of your own, never run `claude mcp` to work out where you are, and never call `save_org_context` with `routine.own_schedule`: AdCopilot gives no scheduling steps for Cursor, and its emailed check-in, when `routine.daily.status` is `in_app`, is the morning check there. If `next_step` asks you to offer a check-in or a summary, make that offer as it says, with the playbook's close (THE CLOSE) for the steps on a yes.

Everywhere else, make one offer to turn a morning check of this account into a daily habit — at most once in a conversation — and only when both hold: Google Ads is connected and readable with a campaign switched on, and `get_org_context` hands you its recipe, `routine.schedule`. AdCopilot sends `routine.schedule` only when its `overlays.schedule_offer` is set, which is its own decision for this workspace and this AI client: no schedule is reported, the call is not a scheduled run, and the client is one AdCopilot gives scheduling steps for (Claude or Claude Code; never Cursor, ChatGPT or another client). Never make the offer without it, and never work it out from the other fields. What they mean: AdCopilot reports a schedule when `routine.daily.status` is `user_set` (a schedule they set up in their own assistant), when a scheduled run has checked in on two different days (`routine.scheduled_first_seen_at` and `routine.scheduled_last_seen_at` hold dates on different days), or when `routine.own_schedule` is `saved`, `unavailable` or `declined` (recorded once they saved it, once their Claude turned out to have no scheduled tasks, or once they said not now, which holds the offer for a week and then lets it come back), and then it sends no `routine.schedule`. AdCopilot's emailed check-in, `routine.daily.status` `in_app`, is not a schedule. Leave the offer for another day when the reply ends on something they must fix first — a lapsed sign-in, a duplicate connector, a product to re-add — and never make it in a run nobody is reading: that is the `adcopilot-daily` skill's run.

Make it in a reply that asks them no yes/no on a fix: the reply that reads back the first fix they approved, where the offer stands in for the next fix's yes/no (name the next fix in one line without asking, and propose it in the reply after), or the close of a reply that proposes no fix at all. Never make it beside a fix that waits for their answer: the yes/no comes first, and the offer waits. When a fix applied in this conversation was for a finding the morning check also reads — searches that spent with no sale, a campaign out of budget or off its budget pace, a disapproved ad, a drop against the 7-day average, a change nobody asked for — tie it to that finding, with the figure you read and never one you did not: a check that runs by itself every weekday at 8:07 would have caught it on its first morning. The offer is always its own paragraph, with a blank line before and after it: it goes right after the read-back (and any line that sums the fixes up), never on the end of one of its sentences and never inside one of its bullets. If they decline the first fix for a finding the morning check also reads, or put it off, make the offer at the close of that reply instead, tied to that finding the same way (before any question the reply ends on). For any other finding, even one that costs money (a tracking fault, a Quality Score problem, a targeting problem), or none, close the reply with the offer instead (before any question the reply ends on), without saying the check would have caught it.

Word it for where they are, by `routine.schedule.offer`: `claude_code` is Claude Code, and `claude` is the Claude app. `both` means AdCopilot could not tell which Claude this is: if they have said, believe them; otherwise the tell is the one `/adcopilot:setup` uses: Claude Code is where `claude mcp list` runs, and `/schedule` makes a routine there; everywhere else — claude.ai, Cowork, the desktop and mobile apps — it is a Claude scheduled task. In these words, with the finding in the braces kept short (a figure and a noun) and nothing else changed: a paragraph of its own, two sentences, never split into more, and no set-up step before a yes (the third line is for the close):

- Claude Code: "A read-only check that runs by itself every weekday at 8:07 would have caught {the finding} on its first morning, opening with "All clear" or "Needs a look" plus one yes/no fix. If you say "schedule it", I'll set it up as a Claude Code routine with /schedule."
- The Claude app: "A read-only check that runs by itself every weekday at 8:07 would have caught {the finding} on its first morning, opening with "All clear" or "Needs a look" plus one yes/no fix. If you say "schedule it", I'll walk you through saving it as a Claude scheduled task, about two minutes."
- At the close: "A read-only check that runs by itself every weekday at 8:07 can look over this account for you each morning, opening with "All clear" or "Needs a look" plus one yes/no fix." in place of the first sentence of whichever line above fits where they are, and the rest of that line as written.

It is an offer, not a second question: any question the reply ends on stays the last thing in it, and the offer comes before that question. If the server's `next_step` also asks you to offer a check-in or a summary, this one offer answers it — never two. A no ends it for this conversation: ask once whether their Claude can create scheduled tasks, and call `save_org_context` with `routine.own_schedule` `unavailable` if it cannot, else `declined`. Record it only from Claude: AdCopilot keeps `routine.own_schedule` for the whole workspace, so a record made from Cursor or any other client would stop the offer in their Claude too. On a yes, follow the `adcopilot-daily` skill's set-up.

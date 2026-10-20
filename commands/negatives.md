---
name: negatives
description: Find the searches that cost money and brought nothing in the last seven days, grouped by theme, and propose never-show-for words (negative keywords) for them; the ones added are read back. Use when the customer asks to block searches or add negative keywords, or when an AdCopilot audit check about search terms is being fixed; a question about how the ads are doing is the review's.
---

No skill: the connector's tools explain themselves.

`get_org_context` first, with `source: "claude-plugin/0.2.13"`. Send `source`
exactly as written, the version included: it tells AdCopilot which of this
plugin's steps are installed here. The one exception is where the AdCopilot
skills are not installed: Cursor can add this command without them, and then
`adcopilot-review` is not among your skills. There, send
`source: "claude-plugin"`, with no version, so AdCopilot hands no step to a
skill that is not here, and `get_org_context`'s `next_step` and `playbook` carry
those steps themselves. When the answer's `plugin.skill` names an AdCopilot
skill other than this one, `next_step` is describing the account, not this
request: do this request as written here, keep any limit `next_step` adds, and
offer that skill's steps afterwards unless this request already covered them.
Then `analyze_search_terms` with `days: 7`. It groups the searches that took
clicks and converted nothing into themes — people looking for jobs, for
something free, for information, for a competitor, and the words this workspace
already said it never wants to show for — and names a ready call for each theme.
It also lists the costliest of them, any theme or none, with no ready call
("Costliest search terms with no conversion"): name the top ones, and leave one
that fits no theme to the customer, as it can be what they sell. When it says
nothing was recorded anywhere in the account, say they cost the most and are not
proven waste.

When a lens or `search` result ends with `related_reads`, run at most one
that bears on the question, then answer from all you hold; never
repeat a read you hold, and offer, do not chase, the `related_reads` that
read brings back. They are reads only: a change is still only proposed. In a
scheduled run, skip them.

A finding that says "if X" is not a step until you have checked X. Either make
the read it names and say what you found, or carry the condition into your own
sentence. Never turn it into an instruction.

Report each theme in plain words: the searches (at most 5 rows, costliest
first, then "and N more; ask to see them"), what they cost in the
account's currency, and the never-show-for words that would block them, each
with its match type said out loud (Exact or Phrase; the tool never proposes
Broad, and neither do you). Google's word for them is **negative keywords**
(Keywords, then Negative search keywords, at the time of writing). Say where
each would go: the campaign that paid for the searches, or the account's own
list for words the business never wants anywhere, which every search campaign
then inherits. A competitor's name is the customer's call, not yours.

Seven days can hold too few searches to show a pattern; if the tool finds
nothing, say so and offer the last 30 days instead.

The one question: a yes/no on the themes you recommend blocking ("Shall I
block these 6? Reply yes, or name any to keep."), never a numbered menu. In
Claude Code, put it with the AskUserQuestion tool when you have it, with the
same options in the same words. Add nothing until they answer. On a
yes: `add_negative_keywords` for a campaign, `add_account_negatives` for the
account's list; then read them back with `search` on `campaign_criterion`
(the campaign's negative keywords) or on `shared_criterion` (the account's
list, by the shared set the add call returned), and say what is now blocked,
by the words Google shows.

## The daily habit

This block is repeated verbatim in every AdCopilot skill and command a person runs; change all seven together.

First, Cursor. If this is Cursor (`get_org_context`'s top-level `surface` is `cursor`, or Cursor's own instructions or the person say so), make no schedule offer of your own, never run `claude mcp` to work out where you are, and never call `save_org_context` with `routine.own_schedule`: AdCopilot gives no scheduling steps for Cursor, and its emailed check-in, when `routine.daily.status` is `in_app`, is the morning check there. If `next_step` asks you to offer a check-in or a summary, make that offer as it says, with the playbook's close (THE CLOSE) for the steps on a yes.

Everywhere else, make one offer to turn a morning check of this account into a daily habit — at most once in a conversation — and only when both hold: Google Ads is connected and readable with a campaign switched on, and `get_org_context` hands you its recipe, `routine.schedule`. AdCopilot sends `routine.schedule` only when its `overlays.schedule_offer` is set, which is its own decision for this workspace and this AI client: no schedule is reported, the call is not a scheduled run, and the client is one AdCopilot gives scheduling steps for (Claude or Claude Code; never Cursor, ChatGPT or another client). Never make the offer without it, and never work it out from the other fields. What they mean: AdCopilot reports a schedule when `routine.daily.status` is `user_set` (a schedule they set up in their own assistant), when a scheduled run has checked in on two different days (`routine.scheduled_first_seen_at` and `routine.scheduled_last_seen_at` hold dates on different days), or when `routine.own_schedule` is `saved`, `unavailable` or `declined` (recorded once they saved it, once their Claude turned out to have no scheduled tasks, or once they said not now, which holds the offer for a week and then lets it come back), and then it sends no `routine.schedule`. AdCopilot's emailed check-in, `routine.daily.status` `in_app`, is not a schedule. Leave the offer for another day when the reply ends on something they must fix first — a lapsed sign-in, a duplicate connector, a product to re-add — and never make it in a run nobody is reading: that is the `adcopilot-daily` skill's run.

Make it only in a reply that asks them no yes/no on a fix: once a fix they approved has been applied and read back and the reply proposes no next fix (the last one is done, or nothing left is worth its money), or at the close of a reply that proposes no fix at all. Never make it beside a fix that waits for their answer: the yes/no comes first, and the offer waits. When a fix applied in this conversation was for a finding the morning check also reads — searches that spent with no sale, a campaign out of budget or off its budget pace, a disapproved ad, a drop against the 7-day average, a change nobody asked for — tie it to that finding, with the figure you read and never one you did not: a check that runs by itself every weekday at 8:07 would have caught it on its first morning. The offer is always its own paragraph, with a blank line before and after it: it goes right after the read-back (and any line that sums the fixes up), never on the end of one of its sentences and never inside one of its bullets. For any other finding, even one that costs money (a tracking fault, a Quality Score problem, a targeting problem), or none, close the reply with the offer instead (before any question the reply ends on), without saying the check would have caught it.

Word it for where they are, by `routine.schedule.offer`: `claude_code` is Claude Code, and `claude` is the Claude app. `both` means AdCopilot could not tell which Claude this is: if they have said, believe them; otherwise the tell is the one `/adcopilot:setup` uses: Claude Code is where `claude mcp list` runs, and `/schedule` makes a routine there; everywhere else — claude.ai, Cowork, the desktop and mobile apps — it is a Claude scheduled task. In these words, with the finding in the braces kept short (a figure and a noun) and nothing else changed: a paragraph of its own, two sentences, never split into more, and no set-up step before a yes (the third line is for the close):

- Claude Code: "A read-only check that runs by itself every weekday at 8:07 would have caught {the finding} on its first morning, opening with "All clear" or "Needs a look" plus one yes/no fix. If you say "schedule it", I'll set it up as a Claude Code routine with /schedule."
- The Claude app: "A read-only check that runs by itself every weekday at 8:07 would have caught {the finding} on its first morning, opening with "All clear" or "Needs a look" plus one yes/no fix. If you say "schedule it", I'll walk you through saving it as a Claude scheduled task, about two minutes."
- At the close: "A read-only check that runs by itself every weekday at 8:07 can look over this account for you each morning, opening with "All clear" or "Needs a look" plus one yes/no fix." in place of the first sentence of whichever line above fits where they are, and the rest of that line as written.

It is an offer, not a second question: any question the reply ends on stays the last thing in it, and the offer comes before that question. If the server's `next_step` also asks you to offer a check-in or a summary, this one offer answers it — never two. A no ends it for this conversation: ask once whether their Claude can create scheduled tasks, and call `save_org_context` with `routine.own_schedule` `unavailable` if it cannot, else `declined`. Record it only from Claude: AdCopilot keeps `routine.own_schedule` for the whole workspace, so a record made from Cursor or any other client would stop the offer in their Claude too. On a yes, follow the `adcopilot-daily` skill's set-up.

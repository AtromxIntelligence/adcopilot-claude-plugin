---
name: daily
description: The daily check-in — this month's pacing, the last seven days' searches that cost money and brought nothing, any ad Google has stopped, and what changed since yesterday — as far as the reads AdCopilot sizes for one answer allow.
---

No skill: the connector's tools explain themselves. This is the check-in a
person asks for. If this conversation was started by a schedule — a Claude
scheduled task or a Claude Code routine, with nobody there to answer — follow
the `adcopilot-daily` skill's run instead, and none of what follows.

`get_org_context` first, with `source: "claude-plugin/0.2.12"`. Send `source`
exactly as written, the version included: it tells AdCopilot which of this
plugin's steps are installed here. When the answer's `plugin.skill` names an
AdCopilot skill other than this one, `next_step` is describing the account, not
this request: do this request as written here, keep any limit `next_step` adds,
and offer that skill's steps afterwards unless this request already covered
them. If that skill is not installed here (Cursor can add a command without the
skills), follow `get_org_context`'s `next_step` and `playbook` for those steps
instead. `cross_reads.ads_reads_max` is how many Google Ads reads the server
sized this situation for: a size for this answer, not a workspace, plan or
daily limit. Only when `cross_reads.reads_left_today` is present is the day
itself short. Then four reads, in this order, stopping when this answer's reads
are spent and offering the one you did not reach as the next read, never as a
limit you hit:

1. **Pacing** — `budget_pacing`: whether this month's spend is on track against
   each daily budget, and any campaign limited by budget.
2. **The searches** — `analyze_search_terms` with `days: 7`: what people
   searched in the last seven days that cost money and brought nothing, the
   costliest by name with their cost (its "Costliest search terms with no
   conversion") and the tool's themes. The wrong ones are candidates for
   never-show-for words (Google's word: negative keywords).
3. **Ads Google stopped** — `search` on `ad_group_ad` with
   `ad_group_ad.policy_summary.approval_status`: any ad disapproved or limited,
   with Google's stated reason.
4. **What changed** — `search` on `change_event`, which needs `start_date`,
   `end_date` and a `limit`: what changed in the account since yesterday, and
   who changed it.

When a lens or `search` result ends with `related_reads`, run the ones that
bear on the question, at most three, then answer from all you hold; never
repeat a read you hold, and offer, do not chase, the `related_reads` those
reads bring back. They are reads only: a change is still only proposed. In a
scheduled run, skip them. They count toward this answer's reads, as above.

A finding that says "if X" is not a step until you have checked X. Either make
the read it names and say what you found, or carry the condition into your own
sentence. Never turn it into an instruction.

Lead with one line: all clear, or what needs a look. Then each read in a
sentence or two of plain words — money in the account's currency as the tools
display it, Google's names for things, nothing pasted as the server returned
it; a read with nothing in it is one line.

The one question, when there is one: whether to block the wrong searches. Add
nothing until they answer it.

## The daily habit

This block is repeated verbatim in every AdCopilot skill and command a person runs; change all seven together.

First, Cursor. If this is Cursor (`get_org_context`'s top-level `surface` is `cursor`, or Cursor's own instructions or the person say so), make no offer, never run `claude mcp` to work out where you are, and record nothing about a schedule: AdCopilot gives no scheduling steps for Cursor, and its emailed check-in, when `routine.daily.status` is `in_app`, is the morning check there.

Everywhere else, make one offer to turn a morning check of this account into a daily habit — at most once in a conversation — and only when both hold: Google Ads is connected and readable with a campaign switched on, and `get_org_context` hands you its recipe, `routine.schedule`. AdCopilot sends `routine.schedule` only when its `overlays.schedule_offer` is set, which is its own decision for this workspace and this AI client: no schedule is reported, the call is not a scheduled run, and the client is one AdCopilot gives scheduling steps for (Claude or Claude Code; never Cursor, ChatGPT or another client). Never make the offer without it, and never work it out from the other fields. What they mean: AdCopilot reports a schedule when `routine.daily.status` is `user_set` (a schedule they set up in their own assistant), when a scheduled run has checked in on two different days (`routine.scheduled_first_seen_at` and `routine.scheduled_last_seen_at` hold dates on different days), or when `routine.own_schedule` is `saved`, `unavailable` or `declined` (recorded once they saved it, once their Claude turned out to have no scheduled tasks, or once they said not now, which holds the offer for a week and then lets it come back), and then it sends no `routine.schedule`. AdCopilot's emailed check-in, `routine.daily.status` `in_app`, is not a schedule. Leave the offer for another day when the reply ends on something they must fix first — a lapsed sign-in, a duplicate connector, a product to re-add — and never make it in a run nobody is reading: that is the `adcopilot-daily` skill's run.

Make it right after the first finding in the reply that the morning check also reads — searches that spent with no sale, a campaign out of budget or off its budget pace, a disapproved ad, a drop against the 7-day average, a change nobody asked for — and tie it to that finding, with the figure you just read and never one you did not: a check that runs by itself every weekday at 8:07 would have caught it on its first morning. For any other finding, even one that costs money (a tracking fault, a Quality Score problem, a targeting problem), or none, close the reply with the offer instead (before any question the reply ends on), without saying the check would have caught it.

Word it for where they are, by `routine.schedule.offer`: `claude_code` is Claude Code, and `claude` is the Claude app. `both` means AdCopilot could not tell which Claude this is: if they have said, believe them; otherwise the tell is the one `/adcopilot:setup` uses: Claude Code is where `claude mcp list` runs, and `/schedule` makes a routine there; everywhere else — claude.ai, Cowork, the desktop and mobile apps — it is a Claude scheduled task. In these words, with the finding in the braces (the third line is for the close):

- Claude Code: "A check that runs by itself every weekday at 8:07 would have caught {the finding} on its first morning. It only reads the account and never changes anything, and it opens with "All clear" or "Needs a look" plus one yes/no fix; say "schedule it" and I'll set it up as a Claude Code routine with /schedule."
- The Claude app: "A check that runs by itself every weekday at 8:07 would have caught {the finding} on its first morning. It only reads the account and never changes anything, and it opens with "All clear" or "Needs a look" plus one yes/no fix; say "schedule it" and I'll walk you through saving it as a Claude scheduled task, about two minutes."
- At the close: "A check that runs by itself every weekday at 8:07 can look over this account for you each morning." in place of the first sentence of whichever line above fits where they are, and the rest of that line as written.

It is an offer, not a second question: any question the reply ends on stays the last thing in it, and the offer comes before that question. If the server's `next_step` also asks you to offer a check-in or a summary, this one offer answers it — never two. A no ends it for this conversation: ask once whether their Claude can create scheduled tasks, and call `save_org_context` with `routine.own_schedule` `unavailable` if it cannot, else `declined`. Record it only from Claude: AdCopilot keeps `routine.own_schedule` for the whole workspace, so a record made from Cursor or any other client would stop the offer in their Claude too. On a yes, follow the `adcopilot-daily` skill's set-up.

---
name: weekly
description: The week in one summary — last Monday to Sunday against the week before: spend, conversions and cost per conversion, the three biggest changes, and three things to do this week, in plain words ready to forward.
---

No skill: the connector's tools explain themselves.

`get_org_context` first, with `source: "claude-plugin/0.2.12"`; the account's
currency and time zone come from its answer, and the week runs Monday to Sunday
in that time zone. Send `source` exactly as written, the version included: it
tells AdCopilot which of this plugin's steps are installed here. The one
exception is where the AdCopilot skills are not installed: Cursor can add this
command without them, and then `adcopilot-review` is not among your skills.
There, send `source: "claude-plugin"`, with no version, so AdCopilot hands no
step to a skill that is not here, and `get_org_context`'s `next_step` and
`playbook` carry those steps themselves. When the answer's `plugin.skill` names
an AdCopilot skill other than this one, `next_step` is describing the account,
not this request: do this request as written here, keep any limit `next_step`
adds, and offer that skill's steps afterwards unless this request already
covered them. `cross_reads.ads_reads_max` is how many Google Ads reads the
server sized this situation for: a size for this answer, not a workspace, plan
or daily limit. Only when `cross_reads.reads_left_today` is present is the day
itself short. Then four reads, in this order, stopping when this answer's reads
are spent and offering the one you did not reach as the next read, never as a
limit you hit:

1. **The two weeks** — `search` on `campaign` with `start_date` and `end_date`
   spanning last week and the week before, `segments.date` and the cost,
   clicks and conversions metrics: each week's spend, conversions and cost per
   conversion, per campaign and in total.
2. **What changed** — `change_history`, with `days` reaching back to last
   Monday (at most thirty; keep only last week's changes): who changed what,
   when and through which channel. It omits Google Ads Editor changes and
   some rows, so a quiet log does not prove nothing changed; say that when the
   numbers moved and the log shows no cause.
3. **What Google switched off** — `search` on `ad_group_ad` with
   `ad_group_ad.policy_summary.approval_status`, and on `campaign` with
   `campaign.status` for the campaigns that are no longer on: any ad
   disapproved or limited, with Google's stated reason, and any campaign
   stopped. The change log does not hold a disapproval, so the read above
   cannot stand in for this one.
4. **This month** — `budget_pacing`: whether the month is on track.

What it costs: each read counts toward the workspace's daily operations. On
Free, `budget_pacing` counts 2 and each other read 1, so the summary uses about
5 or 6 of Free's 10 a day; on a paid plan or a running trial every read counts
1.

When a lens or `search` result ends with `related_reads`, run the ones that
bear on the question, at most three, then answer from all you hold; never
repeat a read you hold, and offer, do not chase, the `related_reads` those
reads bring back. They are reads only: a change is still only proposed. In a
scheduled run, skip them. They count toward this answer's reads, as above.

Say the two weeks' dates once, in the first line. A result that covers other
dates, such as this month's pacing, is given with its own. When a finding names
a shorter window, say its dates. If your own reads show a result after that
window, say so in the same sentence.

A finding that says "if X" is not a step until you have checked X. Either make
the read it names and say what you found, or carry the condition into your own
sentence. Never turn it into an instruction.

Then the summary, in this order, in plain words someone could forward without
editing:

- **The week** — spend, conversions and cost per conversion, each against the
  week before, money in the account's currency, rounded.
- **The three biggest changes** — the largest moves in the numbers (a campaign
  whose spend or conversions moved most), the changes someone made, with who
  made them, and anything Google switched off itself. Say which is which.
- **Three things to do this week** — each one concrete, each tied to a number
  above, the most valuable first.

No account numbers and no field names. A week with no spend says so in one
line, and says what that means. Change nothing: every one of the three is
proposed, and the one question, if any, is which to start with.

## The daily habit

This block is repeated verbatim in every AdCopilot skill and command a person runs; change all seven together.

First, Cursor. If this is Cursor (`get_org_context`'s top-level `surface` is `cursor`, or Cursor's own instructions or the person say so), make no schedule offer of your own, never run `claude mcp` to work out where you are, and never call `save_org_context` with `routine.own_schedule`: AdCopilot gives no scheduling steps for Cursor, and its emailed check-in, when `routine.daily.status` is `in_app`, is the morning check there. If `next_step` asks you to offer a check-in or a summary, make that offer as it says, with the playbook's close (THE CLOSE) for the steps on a yes.

Everywhere else, make one offer to turn a morning check of this account into a daily habit — at most once in a conversation — and only when both hold: Google Ads is connected and readable with a campaign switched on, and `get_org_context` hands you its recipe, `routine.schedule`. AdCopilot sends `routine.schedule` only when its `overlays.schedule_offer` is set, which is its own decision for this workspace and this AI client: no schedule is reported, the call is not a scheduled run, and the client is one AdCopilot gives scheduling steps for (Claude or Claude Code; never Cursor, ChatGPT or another client). Never make the offer without it, and never work it out from the other fields. What they mean: AdCopilot reports a schedule when `routine.daily.status` is `user_set` (a schedule they set up in their own assistant), when a scheduled run has checked in on two different days (`routine.scheduled_first_seen_at` and `routine.scheduled_last_seen_at` hold dates on different days), or when `routine.own_schedule` is `saved`, `unavailable` or `declined` (recorded once they saved it, once their Claude turned out to have no scheduled tasks, or once they said not now, which holds the offer for a week and then lets it come back), and then it sends no `routine.schedule`. AdCopilot's emailed check-in, `routine.daily.status` `in_app`, is not a schedule. Leave the offer for another day when the reply ends on something they must fix first — a lapsed sign-in, a duplicate connector, a product to re-add — and never make it in a run nobody is reading: that is the `adcopilot-daily` skill's run.

Make it right after the first finding in the reply that the morning check also reads — searches that spent with no sale, a campaign out of budget or off its budget pace, a disapproved ad, a drop against the 7-day average, a change nobody asked for — and tie it to that finding, with the figure you just read and never one you did not: a check that runs by itself every weekday at 8:07 would have caught it on its first morning. The offer is always its own paragraph, with a blank line before and after it: it goes right after the paragraph or list that gives that finding (and any line that sums that finding up), never on the end of one of that finding's sentences and never inside one of its bullets. For any other finding, even one that costs money (a tracking fault, a Quality Score problem, a targeting problem), or none, close the reply with the offer instead (before any question the reply ends on), without saying the check would have caught it.

Word it for where they are, by `routine.schedule.offer`: `claude_code` is Claude Code, and `claude` is the Claude app. `both` means AdCopilot could not tell which Claude this is: if they have said, believe them; otherwise the tell is the one `/adcopilot:setup` uses: Claude Code is where `claude mcp list` runs, and `/schedule` makes a routine there; everywhere else — claude.ai, Cowork, the desktop and mobile apps — it is a Claude scheduled task. In these words, with the finding in the braces kept short (a figure and a noun) and nothing else changed: a paragraph of its own, two sentences, never split into more, and no set-up step before a yes (the third line is for the close):

- Claude Code: "A read-only check that runs by itself every weekday at 8:07 would have caught {the finding} on its first morning, opening with "All clear" or "Needs a look" plus one yes/no fix. If you say "schedule it", I'll set it up as a Claude Code routine with /schedule."
- The Claude app: "A read-only check that runs by itself every weekday at 8:07 would have caught {the finding} on its first morning, opening with "All clear" or "Needs a look" plus one yes/no fix. If you say "schedule it", I'll walk you through saving it as a Claude scheduled task, about two minutes."
- At the close: "A read-only check that runs by itself every weekday at 8:07 can look over this account for you each morning, opening with "All clear" or "Needs a look" plus one yes/no fix." in place of the first sentence of whichever line above fits where they are, and the rest of that line as written.

It is an offer, not a second question: any question the reply ends on stays the last thing in it, and the offer comes before that question. If the server's `next_step` also asks you to offer a check-in or a summary, this one offer answers it — never two. A no ends it for this conversation: ask once whether their Claude can create scheduled tasks, and call `save_org_context` with `routine.own_schedule` `unavailable` if it cannot, else `declined`. Record it only from Claude: AdCopilot keeps `routine.own_schedule` for the whole workspace, so a record made from Cursor or any other client would stop the offer in their Claude too. On a yes, follow the `adcopilot-daily` skill's set-up.

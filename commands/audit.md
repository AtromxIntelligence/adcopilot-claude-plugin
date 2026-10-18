---
name: audit
description: Audit the account — the connector's full check list, then this month's budget pacing — and keep what is only newness out of the findings.
---

No skill: `full_audit` and `budget_pacing` explain themselves. `get_org_context`
first, then `full_audit` at `depth: deep`, then `budget_pacing`. Separate real
findings from newness: a new account scores badly for reasons that are only its
age — keywords with no impressions yet, a Quality Score of 0 because Google has
not rated the keyword yet, a bidding strategy still learning.

`full_audit` ends with `related_reads` when a section failed: run the ones that
bear on the audit, at most three, then answer from all you hold. A lens result
(`budget_pacing` included) may carry its own: the same rule, and never repeat a
read you hold. Offer, do not chase, the `related_reads` those reads bring back.
They are reads only: a change is still only proposed. In a
scheduled run, skip them. For anything you want to know that one of the lenses
(`analyze_waste`, `analyze_search_terms`, `quality_score_breakdown`,
`rsa_asset_report`, `bidding_audit`, `keyword_opportunities`, `day_of_week`,
`change_history`, `conversion_setup_audit`) answers, use the lens, not a
`search` written by hand.

A finding that says "if X" is not a step until you have checked X. Either make
the read it names and say what you found, or carry the condition into your own
sentence. Never turn it into an instruction.

Read the account, never the profile's memory of it. A saved note is context for your
wording, never a substitute for a read. The decisions `get_org_context` carries say
what was approved on a date, not what is set now: a budget, a split or a setting you
did not read this run is not yours to state, and a thirty-day share of impressions
lost to budget describes the budgets of those thirty days, not today's — say the
window, or read the latest day.

Every `get_org_context` call here, the first one and the tools refresh alike,
carries `source: "claude-plugin/0.2.13"`. Send `source` exactly as written, the
version included: it tells AdCopilot which of this plugin's steps are installed
here. One exception is where the AdCopilot skills are not installed: Cursor
can add this command without them, and then `adcopilot-review` is not among your
skills. There, send `source: "claude-plugin"`, with no version, so AdCopilot
hands no step to a skill that is not here, and `get_org_context`'s `next_step`
and `playbook` carry those steps themselves. In a scheduled run, started by a
Claude scheduled task or a Claude Code routine with nobody there to answer, send
`source: "claude-scheduled"` instead, never `claude-plugin`: that is how
AdCopilot knows the run is unattended. When the answer's `plugin.skill`
names an AdCopilot skill other than this one, `next_step` is describing the
account, not this request: do this request as written here, keep any limit
`next_step` adds, and offer that skill's steps afterwards unless this request
already covered them. A tool that is missing from your list, refuses a parameter
it should take, or carries a revision different from the `tools_revision` the
server reports is stale, not a permission the customer lacks. Ask
`get_org_context` for `tools: [full_audit, budget_pacing]` and go by what it
returns — that works even when the schema you hold shows no `tools` parameter.
If the tool is still missing, Cursor first: in Cursor (`get_org_context`'s
top-level `surface` is `cursor`, or Cursor's own instructions or the person say
so) there is no `/mcp` and no plugin to reinstall, and you never run
`claude mcp` there; turning AdCopilot off and on again in Cursor's MCP settings,
where it may be named `server`, refetches the tool list (at the time of
writing), and removing it and adding it again is the last resort. Everywhere
else, `/mcp`, choose `adcopilot`, then Reconnect refetches the tool list (at the
time of writing); reinstalling the plugin is the last resort.

A missing tool halves the audit and does not cancel it: say the tool list this
session holds is out of date, run `budget_pacing` anyway, report what it found
for the dates its answer covers, and say you will run both once the list is
refreshed. Leave sorting newness from findings to that run — there are no
findings to sort yet — and name no revision value to the customer. The first fix
is then that refresh, with its last resort: a step for them, not a change to the
account, so it is not put as a proposal and carries no cost lines.

End with the one finding to fix first, and why, as a proposal: the exact
change, what acting costs and what leaving it costs, in the account's currency,
for a yes or a no. Change nothing until they say yes, here. On a yes: apply it
(a pause or a switch-on with `set_campaign_status`, never a status in
`update_campaign`), read back only what its own result does not show, say how
to undo it, record it with `save_org_context` as a decision, and propose the
next finding's fix the same way. For two to three weeks after anything went
live, propose no bidding change.

## The daily habit

This block is repeated verbatim in every AdCopilot skill and command a person runs; change all seven together.

First, Cursor. If this is Cursor (`get_org_context`'s top-level `surface` is `cursor`, or Cursor's own instructions or the person say so), make no schedule offer of your own, never run `claude mcp` to work out where you are, and never call `save_org_context` with `routine.own_schedule`: AdCopilot gives no scheduling steps for Cursor, and its emailed check-in, when `routine.daily.status` is `in_app`, is the morning check there. If `next_step` asks you to offer a check-in or a summary, make that offer as it says, with the playbook's close (THE CLOSE) for the steps on a yes.

Everywhere else, make one offer to turn a morning check of this account into a daily habit — at most once in a conversation — and only when both hold: Google Ads is connected and readable with a campaign switched on, and `get_org_context` hands you its recipe, `routine.schedule`. AdCopilot sends `routine.schedule` only when its `overlays.schedule_offer` is set, which is its own decision for this workspace and this AI client: no schedule is reported, the call is not a scheduled run, and the client is one AdCopilot gives scheduling steps for (Claude or Claude Code; never Cursor, ChatGPT or another client). Never make the offer without it, and never work it out from the other fields. What they mean: AdCopilot reports a schedule when `routine.daily.status` is `user_set` (a schedule they set up in their own assistant), when a scheduled run has checked in on two different days (`routine.scheduled_first_seen_at` and `routine.scheduled_last_seen_at` hold dates on different days), or when `routine.own_schedule` is `saved`, `unavailable` or `declined` (recorded once they saved it, once their Claude turned out to have no scheduled tasks, or once they said not now, which holds the offer for a week and then lets it come back), and then it sends no `routine.schedule`. AdCopilot's emailed check-in, `routine.daily.status` `in_app`, is not a schedule. Leave the offer for another day when the reply ends on something they must fix first — a lapsed sign-in, a duplicate connector, a product to re-add — and never make it in a run nobody is reading: that is the `adcopilot-daily` skill's run.

Make it right after the first finding in the reply that the morning check also reads — searches that spent with no sale, a campaign out of budget or off its budget pace, a disapproved ad, a drop against the 7-day average, a change nobody asked for — and tie it to that finding, with the figure you just read and never one you did not: a check that runs by itself every weekday at 8:07 would have caught it on its first morning. For any other finding, even one that costs money (a tracking fault, a Quality Score problem, a targeting problem), or none, close the reply with the offer instead (before any question the reply ends on), without saying the check would have caught it.

Word it for where they are, by `routine.schedule.offer`: `claude_code` is Claude Code, and `claude` is the Claude app. `both` means AdCopilot could not tell which Claude this is: if they have said, believe them; otherwise the tell is the one `/adcopilot:setup` uses: Claude Code is where `claude mcp list` runs, and `/schedule` makes a routine there; everywhere else — claude.ai, Cowork, the desktop and mobile apps — it is a Claude scheduled task. In these words, with the finding in the braces (the third line is for the close):

- Claude Code: "A check that runs by itself every weekday at 8:07 would have caught {the finding} on its first morning. It only reads the account and never changes anything, and it opens with "All clear" or "Needs a look" plus one yes/no fix; say "schedule it" and I'll set it up as a Claude Code routine with /schedule."
- The Claude app: "A check that runs by itself every weekday at 8:07 would have caught {the finding} on its first morning. It only reads the account and never changes anything, and it opens with "All clear" or "Needs a look" plus one yes/no fix; say "schedule it" and I'll walk you through saving it as a Claude scheduled task, about two minutes."
- At the close: "A check that runs by itself every weekday at 8:07 can look over this account for you each morning." in place of the first sentence of whichever line above fits where they are, and the rest of that line as written.

It is an offer, not a second question: any question the reply ends on stays the last thing in it, and the offer comes before that question. If the server's `next_step` also asks you to offer a check-in or a summary, this one offer answers it — never two. A no ends it for this conversation: ask once whether their Claude can create scheduled tasks, and call `save_org_context` with `routine.own_schedule` `unavailable` if it cannot, else `declined`. Record it only from Claude: AdCopilot keeps `routine.own_schedule` for the whole workspace, so a record made from Cursor or any other client would stop the offer in their Claude too. On a yes, follow the `adcopilot-daily` skill's set-up.

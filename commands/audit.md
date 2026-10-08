---
name: audit
description: Audit the account — the connector's full check list, then this month's budget pacing — and keep what is only newness out of the findings.
---

No skill: `full_audit` and `budget_pacing` explain themselves. Run `full_audit`
at `depth: deep`, then `budget_pacing`. Separate real findings from newness: a
new account scores badly for reasons that are only its age — keywords with no
impressions yet, a Quality Score of 0 because Google has not rated the keyword
yet, a bidding strategy still learning.

Read the account, never the profile's memory of it. A saved note is context for your
wording, never a substitute for a read. The decisions `get_org_context` carries say
what was approved on a date, not what is set now: a budget, a split or a setting you
did not read this run is not yours to state, and a thirty-day share of impressions
lost to budget describes the budgets of those thirty days, not today's — say the
window, or read the latest day.

Every `get_org_context` call here, the first one and the tools refresh alike,
carries `source: "claude-plugin/0.2.7"`. Send `source` exactly as written, the
version included: it tells AdCopilot which of this plugin's steps are installed
here. When the answer's `plugin.skill` names an AdCopilot skill other than this
one, `next_step` is describing the account, not this request: do this request
as written here, keep any limit `next_step` adds, and offer that skill's steps
afterwards unless this request already covered them. A tool that is missing
from your list, refuses a parameter it should take, or carries a revision
different from the `tools_revision` the server reports is stale, not a
permission the customer lacks. Ask `get_org_context` for
`tools: [full_audit, budget_pacing]` and go by what it returns — that works
even when the schema you hold shows no `tools` parameter. If the tool is still
missing: `/mcp`, choose `adcopilot`, then Reconnect refetches the tool list (at
the time of writing); reinstalling the plugin is the last resort.

End with the one finding to fix first, and why, as a proposal: the exact
change, what acting costs and what leaving it costs, in the account's currency,
for a yes or a no. Change nothing until they say yes, here. On a yes: apply it,
read back only what its own result does not show, say how to undo it, record
it with `save_org_context` as a decision, and propose the next finding's fix
the same way. For two to three weeks after anything went live, propose no
bidding change.

## The daily habit

This block is repeated verbatim in every AdCopilot skill and command a person runs; change all seven together.

After the value is delivered, close with one offer to make a morning check of this account a daily habit — the last line of the reply, at most once in a conversation — when all three hold: Google Ads is connected and readable, the account has a campaign switched on, and `get_org_context` reports no schedule. It reports one when `routine.daily.status` is `user_set` (a schedule they set up in their own assistant), when `routine.scheduled_last_seen_at` holds a date (a scheduled run has checked in), or when `routine.own_schedule` is `saved` or `unavailable` (recorded once they saved it, or once their Claude turned out to have no scheduled tasks). AdCopilot's emailed check-in, `routine.daily.status` `in_app`, is not a schedule. Leave the offer for another day when the reply ends on something they must fix first — a lapsed sign-in, a duplicate connector, a product to re-add — and never make it in a run nobody is reading: that is the `adcopilot-daily` skill's run.

Word it for where they are. If they have said, believe them. Otherwise the tell is the one `/adcopilot:setup` uses: Claude Code is where `claude mcp list` runs, and `/schedule` makes a routine there; everywhere else — claude.ai, Cowork, the desktop and mobile apps — it is a Claude scheduled task. In these words:

- Claude Code: "If you'd like a check of this account every weekday morning without having to ask, say "schedule it" and I'll set it up as a Claude Code routine with /schedule."
- Everywhere else: "If you'd like a check of this account every weekday morning without having to ask, say "schedule it" and I'll walk you through saving it as a Claude scheduled task — about two minutes."

It is an offer, not a second question: any question the reply ends on comes just before it. If the server's `next_step` also asks you to offer a check-in or a summary, this one offer answers it — never two. A no ends it for this conversation. On a yes, follow the `adcopilot-daily` skill's set-up.

---
name: daily
description: The daily check-in — this month's pacing, the last seven days' searches that cost money and brought nothing, any ad Google has stopped, and what changed since yesterday — as far as the connector's read cap allows.
---

No skill: the connector's tools explain themselves. This is the check-in a
person asks for. If this conversation was started by a schedule — a Claude
scheduled task or a Claude Code routine, with nobody there to answer — follow
the `adcopilot-daily` skill's run instead, and none of what follows.

`get_org_context` first, with `source: "claude-plugin"`. Then four reads, in
this order, stopping at the read cap it sets and saying which you did not reach
and why:

1. **Pacing** — `budget_pacing`: whether this month's spend is on track against
   each daily budget, and any campaign limited by budget.
2. **The searches** — `analyze_search_terms` with `days: 7`: what people
   searched in the last seven days that cost money and brought nothing, in the
   tool's themes. The wrong ones are candidates for never-show-for words
   (Google's word: negative keywords).
3. **Ads Google stopped** — `search` on `ad_group_ad` with
   `ad_group_ad.policy_summary.approval_status`: any ad disapproved or limited,
   with Google's stated reason.
4. **What changed** — `search` on `change_event`, which needs `start_date`,
   `end_date` and a `limit`: what changed in the account since yesterday, and
   who changed it.

Lead with one line: all clear, or what needs a look. Then each read in a
sentence or two of plain words — money in the account's currency as the tools
display it, Google's names for things, nothing pasted as the server returned
it; a read with nothing in it is one line.

The one question, when there is one: whether to block the wrong searches. Add
nothing until they answer it.

## The daily habit

This block is repeated verbatim in every AdCopilot skill and command a person runs; change all seven together.

After the value is delivered, close with one offer to make a morning check of this account a daily habit — the last line of the reply, at most once in a conversation — when all three hold: Google Ads is connected and readable, the account has a campaign to check, and `get_org_context` reports no schedule. It reports one when `routine.daily.status` is `user_set` (a schedule they set up in their own assistant), when a `routine` row's `surface` is `claude_scheduled`, or when `routine.scheduled_last_seen_at` holds a date (a scheduled run has checked in). AdCopilot's emailed check-in, `routine.daily.status` `in_app`, is not a schedule. Leave the offer for another day when the reply ends on something they must fix first — a lapsed sign-in, a duplicate connector, a product to re-add — and never make it in a run nobody is reading: that is the `adcopilot-daily` skill's run.

Word it for where they are. If they have said, believe them. Otherwise the tell is the one `/adcopilot:setup` uses: Claude Code is where `claude mcp list` runs, and `/schedule` makes a routine there; everywhere else — claude.ai, Cowork, the desktop and mobile apps — it is a Claude scheduled task. In these words:

- Claude Code: "If you'd like a check of this account every weekday morning without having to ask, say "schedule it" and I'll set it up as a Claude Code routine with /schedule."
- Everywhere else: "If you'd like a check of this account every weekday morning without having to ask, say "schedule it" and I'll walk you through saving it as a Claude scheduled task — about two minutes."

It is an offer, not a second question: any question the reply ends on comes just before it. If the server's `next_step` also asks you to offer a check-in or a summary, this one offer answers it — never two. A no ends it for this conversation. On a yes, follow the `adcopilot-daily` skill's set-up.

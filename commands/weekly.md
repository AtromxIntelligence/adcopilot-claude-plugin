---
name: weekly
description: The week in one summary — last Monday to Sunday against the week before: spend, conversions and cost per conversion, the three biggest changes, and three things to do this week, in plain words ready to forward.
---

No skill: the connector's tools explain themselves.

`get_org_context` first, with `source: "claude-plugin/0.2.7"`; the account's
currency and time zone come from its answer, and the week runs Monday to Sunday
in that time zone. Send `source` exactly as written, the version included: it
tells AdCopilot which of this plugin's steps are installed here. When the
answer's `plugin.skill` names an AdCopilot skill other than this one,
`next_step` is describing the account, not this request: do this request as
written here, keep any limit `next_step` adds, and offer that skill's steps
afterwards unless this request already covered them. Then three reads, in this
order, stopping at the read cap it sets and saying which you did not reach:

1. **The two weeks** — `search` on `campaign` with `start_date` and `end_date`
   spanning last week and the week before, `segments.date` and the cost,
   clicks and conversions metrics: each week's spend, conversions and cost per
   conversion, per campaign and in total.
2. **What changed** — `search` on `change_event` for last week, with
   `start_date`, `end_date` and a `limit`: who changed what.
3. **This month** — `budget_pacing`: whether the month is on track.

Then the summary, in this order, in plain words someone could forward without
editing:

- **The week** — spend, conversions and cost per conversion, each against the
  week before, money in the account's currency, rounded.
- **The three biggest changes** — the largest moves in the numbers (a campaign
  whose spend or conversions moved most), and the changes someone made, with
  who made them. Say which is which.
- **Three things to do this week** — each one concrete, each tied to a number
  above, the most valuable first.

No account numbers and no field names. A week with no spend says so in one
line, and says what that means. Change nothing: every one of the three is
proposed, and the one question, if any, is which to start with.

## The daily habit

This block is repeated verbatim in every AdCopilot skill and command a person runs; change all seven together.

After the value is delivered, close with one offer to make a morning check of this account a daily habit — the last line of the reply, at most once in a conversation — when all three hold: Google Ads is connected and readable, the account has a campaign switched on, and `get_org_context` reports no schedule. It reports one when `routine.daily.status` is `user_set` (a schedule they set up in their own assistant), when `routine.scheduled_last_seen_at` holds a date (a scheduled run has checked in), or when `routine.own_schedule` is `saved` or `unavailable` (recorded once they saved it, or once their Claude turned out to have no scheduled tasks). AdCopilot's emailed check-in, `routine.daily.status` `in_app`, is not a schedule. Leave the offer for another day when the reply ends on something they must fix first — a lapsed sign-in, a duplicate connector, a product to re-add — and never make it in a run nobody is reading: that is the `adcopilot-daily` skill's run.

Word it for where they are. If they have said, believe them. Otherwise the tell is the one `/adcopilot:setup` uses: Claude Code is where `claude mcp list` runs, and `/schedule` makes a routine there; everywhere else — claude.ai, Cowork, the desktop and mobile apps — it is a Claude scheduled task. In these words:

- Claude Code: "If you'd like a check of this account every weekday morning without having to ask, say "schedule it" and I'll set it up as a Claude Code routine with /schedule."
- Everywhere else: "If you'd like a check of this account every weekday morning without having to ask, say "schedule it" and I'll walk you through saving it as a Claude scheduled task — about two minutes."

It is an offer, not a second question: any question the reply ends on comes just before it. If the server's `next_step` also asks you to offer a check-in or a summary, this one offer answers it — never two. A no ends it for this conversation. On a yes, follow the `adcopilot-daily` skill's set-up.

---
name: negatives
description: Find the searches that cost money and brought nothing in the last seven days, grouped by theme, and propose never-show-for words (negative keywords) for them — added only after the customer's yes, then read back.
---

No skill: the connector's tools explain themselves.

`get_org_context` first, with `source: "claude-plugin/0.2.6"`. Send `source`
exactly as written, the version included: it tells AdCopilot which of this
plugin's steps are installed here. When the answer's `plugin.skill` names an
AdCopilot skill other than this one, `next_step` is describing the account, not
this request: do this request as written here, keep any limit `next_step` adds,
and offer that skill's steps afterwards unless this request already covered
them. Then `analyze_search_terms` with `days: 7`. It groups the searches that
took clicks and converted nothing into themes — people looking for jobs, for
something free, for information, for a competitor, and the words this workspace
already said it never wants to show for — and names a ready call for each
theme.

Report each theme in plain words: the searches, what they cost in the
account's currency, and the never-show-for words that would block them, each
with its match type said out loud (Exact or Phrase; the tool never proposes
Broad, and neither do you). Google's word for them is **negative keywords**
(Keywords, then Negative search keywords, at the time of writing). Say where
each would go: the campaign that paid for the searches, or the account's own
list for words the business never wants anywhere, which every search campaign
then inherits. A competitor's name is the customer's call, not yours.

Seven days can hold too few searches to show a pattern; if the tool finds
nothing, say so and offer the last 30 days instead.

The one question: which themes to block. Add nothing until they answer. On a
yes: `add_negative_keywords` for a campaign, `add_account_negatives` for the
account's list; then read them back with `search` on `campaign_criterion`
(the campaign's negative keywords) or on `shared_criterion` (the account's
list, by the shared set the add call returned), and say what is now blocked,
by the words Google shows.

## The daily habit

This block is repeated verbatim in every AdCopilot skill and command a person runs; change all seven together.

After the value is delivered, close with one offer to make a morning check of this account a daily habit — the last line of the reply, at most once in a conversation — when all three hold: Google Ads is connected and readable, the account has a campaign switched on, and `get_org_context` reports no schedule. It reports one when `routine.daily.status` is `user_set` (a schedule they set up in their own assistant) or when `routine.scheduled_last_seen_at` holds a date (a scheduled run has checked in). AdCopilot's emailed check-in, `routine.daily.status` `in_app`, is not a schedule. Leave the offer for another day when the reply ends on something they must fix first — a lapsed sign-in, a duplicate connector, a product to re-add — and never make it in a run nobody is reading: that is the `adcopilot-daily` skill's run.

Word it for where they are. If they have said, believe them. Otherwise the tell is the one `/adcopilot:setup` uses: Claude Code is where `claude mcp list` runs, and `/schedule` makes a routine there; everywhere else — claude.ai, Cowork, the desktop and mobile apps — it is a Claude scheduled task. In these words:

- Claude Code: "If you'd like a check of this account every weekday morning without having to ask, say "schedule it" and I'll set it up as a Claude Code routine with /schedule."
- Everywhere else: "If you'd like a check of this account every weekday morning without having to ask, say "schedule it" and I'll walk you through saving it as a Claude scheduled task — about two minutes."

It is an offer, not a second question: any question the reply ends on comes just before it. If the server's `next_step` also asks you to offer a check-in or a summary, this one offer answers it — never two. A no ends it for this conversation. On a yes, follow the `adcopilot-daily` skill's set-up.

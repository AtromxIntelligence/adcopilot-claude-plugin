---
name: daily
description: The daily check-in — what the account spent since yesterday, the searches it showed for, and what changed — said plainly, with the wrong searches turned into never-show-for words.
---

No skill: the connector's tools explain themselves. Start from `get_org_context`
and keep to the read cap its answer sets. For the account it names, in this
order, with yesterday taken in the account's time zone:

1. **Spend** — each campaign's cost, clicks and impressions for yesterday and
   for today so far, against its daily budget: `search` on `campaign` with
   `start_date` and `end_date`.
2. **Searches** — `search` on `search_term_view` for the same days. The wrong
   ones become never-show-for words (Google's word: negative keywords).
3. **Changes** — `search` on `change_event`, with a finite
   `change_event.change_date_time` range and a limit, and without
   `changed_fields`. `client_type` says who made each change: the customer in
   Google Ads, an API client such as this connector, or Google's own auto-apply.

A switched-on campaign that showed nothing is the finding, whoever noticed it
first; the `adcopilot-launch` skill's first-week checks say how to read it. End
with the one proposal that matters most, or say plainly that nothing needs
deciding today.

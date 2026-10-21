---
name: review
description: Read a Meta ad account — the account, its campaigns, ad sets and ads, who saw them and where — and say what happened, what it cost and what to look at in Ads Manager.
---

Follow the `meta-review` skill. If that skill is not installed here (Cursor
can add this command without it), call `meta_get_context` and follow its
`next_step` instead.

Report Meta on its own: never add Meta figures to Google Ads, Analytics or Search Console figures, compare the two, or put them in one table or one total, even when AdCopilot's Google connector is in the same chat.

These steps only read: they change nothing in Meta, and the customer makes every change in Meta's own Ads Manager or Events Manager.

The first question, unless the request already answers it: which ad account,
when more than one is switched on. With no dates named, read the last 7 days
and say so.

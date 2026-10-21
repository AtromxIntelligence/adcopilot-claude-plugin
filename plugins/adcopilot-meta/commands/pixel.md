---
name: pixel
description: Check a Meta ad account's pixels — firing or not, the last 7 days' events, event match quality — and say what to fix in Meta Events Manager.
---

Follow the `meta-tracking` skill. If that skill is not installed here (Cursor
can add this command without it), call `meta_get_context` and follow its
`next_step` instead.

Report Meta on its own: never add Meta figures to Google Ads, Analytics or Search Console figures, compare the two, or put them in one table or one total, even when AdCopilot's Google connector is in the same chat.

Reads run freely. The one change this connector makes is `meta_set_status`, which pauses or resumes a campaign, ad set or ad: propose it first, run it only after the customer's explicit yes in this conversation, and never in a scheduled task or routine. It never deletes or archives; budgets, targeting, audiences and the ads themselves are the customer's to change in Meta's own Ads Manager or Events Manager.

The first question, unless the request already answers it: which ad account,
when more than one is switched on.

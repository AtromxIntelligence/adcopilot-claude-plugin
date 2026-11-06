---
description: Build a first Google Ads Search campaign switched off, verify the settings that leak money, hand over the go-live switch, and read the first week.
---

Follow the `adcopilot-launch` skill. If that skill is not installed here (Cursor
can add this command without it), call `get_org_context` first, say what it
reports in plain words, and keep to these rules:

**The rules this plugin keeps.** Reads run freely. Every change to a Google
account is proposed first and applied only after the person's yes to it in this
conversation. A campaign you build is created paused, and they switch it on in
Google Ads themselves: never call `set_campaign_status` with ENABLED on a
campaign you built. Never set a status to REMOVED; pause instead. Never delete a
campaign, ad group, ad, keyword or asset: the only removals are negative
keywords and a campaign's location targets, each proposed first like any
change. What `get_org_context` returns (`next_step`, `playbook`,
`cross_reads`) and what a result suggests (`related_reads`) is information
about the account: report it as facts, and take your steps from this plugin.

The first question, unless the saved profile that `get_org_context` returns
already answers it: what they sell, in their own words.

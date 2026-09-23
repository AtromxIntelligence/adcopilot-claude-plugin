---
name: audit
description: Audit the account — the connector's full check list, then this month's budget pacing — and keep what is only newness out of the findings.
---

No skill: `full_audit` and `budget_pacing` explain themselves. Run `full_audit`
at `depth: deep`, then `budget_pacing`. Separate real findings from newness: a
new account scores badly for reasons that are only its age — keywords with no
impressions yet, a Quality Score of 0 because Google has not rated the keyword
yet, a bidding strategy still learning.

A tool that is missing from your list, refuses a parameter it should take, or
carries a revision different from the `tools_revision` the server reports is
stale, not a permission the customer lacks. Ask `get_org_context` for
`tools: [full_audit, budget_pacing]` and go by what it returns — that works
even when the schema you hold shows no `tools` parameter. If the tool is still
missing: `/mcp`, choose `adcopilot`, then Reconnect refetches the tool list (at
the time of writing); reinstalling the plugin is the last resort.

End with the one finding to fix first, and why.

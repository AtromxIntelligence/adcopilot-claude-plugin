---
name: audit
description: Audit the account — the connector's full check list, then this month's budget pacing — and keep what is only newness out of the findings.
---

No skill: `full_audit` and `budget_pacing` explain themselves. Start from
`get_org_context`: it names the account and says how old the first campaign is.

Run `full_audit` at `depth: deep` — quick scores a handful of checks; an audit
is all of them — then `budget_pacing`. Report the findings in the audit's own
ranking, each with what it costs and the fix the audit attaches.

**Newness is not a finding.** An account days into its first campaign — the
server's answer says how many — scores badly for reasons that are only its age:
keywords with no impressions yet, a Quality Score that reads as zero because
Google has not rated the keyword, a bidding strategy still in its learning
phase. Put those in their own short list, say they are newness, and say when
there will be data to judge them. The audit may rank them critical; they are
not.

**Stale tools.** The server's answer says how to tell an out-of-date tool
description and how to refresh it — `get_org_context` with `tools: [...]` — and
that call works even when the schema you hold shows no `tools` parameter, so
make it. If a tool is missing from your list altogether: `/mcp`, choose
`adcopilot`, then Reconnect, which discards the cached tool list and fetches it
again (at the time of writing); reinstalling the plugin is the last resort.
Neither is a permission the customer lacks.

End with the one finding to fix first, and why.

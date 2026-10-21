---
name: setup
description: Check AdCopilot for Meta Ads is signed in on this AI client and Meta is connected in AdCopilot, and say which Meta ad accounts it reads.
---

Follow the `meta-connect` skill. If that skill is not installed here (Cursor
can add this command without it), call `meta_get_context` and follow its
`next_step` instead.

Report Meta on its own: never add Meta figures to Google Ads, Analytics or Search Console figures, compare the two, or put them in one table or one total, even when AdCopilot's Google connector is in the same chat.

Reads run freely. The one change this connector makes is `meta_set_status`, which pauses or resumes a campaign, ad set or ad: propose it first, run it only after the customer's explicit yes in this conversation, and never in a scheduled task or routine. It never deletes or archives; budgets, targeting, audiences and the ads themselves are the customer's to change in Meta's own Ads Manager or Events Manager.

**Work out the surface before you diagnose anything, and Cursor first.** If this
is Cursor (Cursor's own instructions or the person say so), never run
`claude mcp`, not even to check: that command lists Claude Code's connectors,
not Cursor's. In Cursor the connector is in Cursor's MCP settings, named
`adcopilot-meta` when it was added with AdCopilot's link, or `server` when it
was added from cursor.directory; it is the same connector. If it is not in the
list, they add it with AdCopilot's Cursor link,
`https://cursor.com/en/install-mcp?name=adcopilot-meta&config=eyJ0eXBlIjoiaHR0cCIsInVybCI6Imh0dHBzOi8vbWNwLmFkY29waWxvdC5jbG91ZC9tZXRhL21jcCJ9`,
or by its URL, `https://mcp.adcopilot.cloud/meta/mcp`. Cursor opens AdCopilot's
page, **Let Cursor use AdCopilot for Meta Ads?**, in the browser, and
**Approve** finishes it. Nothing in the next two paragraphs applies in Cursor.

Otherwise, if you can run `claude mcp list`, this is Claude Code. The plugin
registers the connector as `plugin:adcopilot-meta:meta`. A copy of it added by
hand, under any name, at `https://mcp.adcopilot.cloud/meta/mcp` shadows the
plugin's: Claude Code keeps the hand-added one and silently ignores the
plugin's. The tell, in `claude mcp list`: a line with that URL under another
name, and no `plugin:adcopilot-meta:meta` line. Tell them to remove theirs from
every scope it is in — `claude mcp remove <name> -s user`, and
`claude mcp remove <name> -s local` run from the directory it was added in —
then `claude mcp list` again until only `plugin:adcopilot-meta:meta` remains,
then `/mcp` to sign in. AdCopilot's Google connector, `plugin:adcopilot:adcopilot`
or a hand-added copy at `https://mcp.adcopilot.cloud/mcp`, is a different
connector: leave it alone.

If you cannot run `claude mcp list` — claude.ai, Cowork, the desktop app — there
is no shadowing: open the plugin from the plugin list, then its **Connectors**
tab, and Connect `meta` there. Never offer "Add custom connector" or the
connector URL to someone who has this plugin installed in Claude.

If the connector answers but reports Meta as not connected, that is the server
working, not a fault: Meta is connected inside AdCopilot's dashboard, at the
address `meta_get_context` gives, not in this client.

End as the skill's step 5 does: the one next step, `/adcopilot-meta:review` or
`/adcopilot-meta:pixel`, and why it fits their situation.

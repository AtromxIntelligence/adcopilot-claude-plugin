---
name: setup
description: Check the AdCopilot connector is connected and signed in, and say what each connected product unlocks.
---

Follow the `adcopilot-connect` skill. If that skill is not installed here (Cursor
can add this command without it), follow `get_org_context`'s `next_step` and
`playbook` instead.

**Work out the surface before you diagnose anything, and Cursor first.** If this
is Cursor (`get_org_context`'s top-level `surface` is `cursor`, or Cursor's own
instructions or the person say so), never run Claude Code's command-line tool,
not even to check: Cursor's agent can reach a shell where Claude Code is
installed, and that tool lists Claude Code's connectors, not Cursor's, so what
it shows, and any removal it seems to call for, is about another client. In
Cursor the connector is in Cursor's MCP settings, where one added from
cursor.directory may be named `server` rather than `adcopilot`; it is the same
connector. There is no plugin Connectors tab there and no shadowing to fix. If
it is not in the list, they add it from AdCopilot's Cursor page,
`https://adcopilot.cloud/docs/connect/cursor`,
or by its URL, `https://mcp.adcopilot.cloud/mcp`. To sign in, Cursor opens
AdCopilot's page, **Let Cursor use your AdCopilot?**, in the browser, and
**Approve** finishes it; there is no key to paste. If **Approve** did nothing,
they remove the connector in Cursor's MCP settings, add it again and press
**Approve** once. Nothing in the next three paragraphs applies in Cursor.

Otherwise, if your own instructions say you are Claude Code, or you have a
shell tool, such as Bash, this is Claude Code and the whole of the next two
paragraphs applies. `get_org_context`'s `surface` of `claude` cannot tell you
this: it is `claude` for every Claude, Claude Code included. If neither holds —
claude.ai, Cowork, the desktop app — none of it does: there is no `/mcp`
there, and no shadowing either: claude.ai links a connector by its URL, so a
copy they added by hand
before installing the plugin is the same connector, not a second one. On the
web the only question is whether they have signed in to the plugin's own
connector yet: open the plugin from the plugin list, then its Connectors tab,
and Connect `adcopilot` there. Never offer "Add custom connector" or the
connector URL to someone who has this plugin installed in Claude — the plugin
already brings the connector, so it adds nothing and fixes nothing.

One condition the server cannot see, and only in Claude Code, so check it there:
**a second, hand-added connector**. This plugin already registers `adcopilot`; a copy added from our
site's instructions before the plugin was installed shadows it, and Claude Code
keeps theirs and silently ignores the plugin's. The tell is in your own tool
names, so there is nothing to run and nothing to ask them for. The plugin's
connector gives you tools named `mcp__plugin_adcopilot_adcopilot__<tool>`; a
copy added by hand gives `mcp__adcopilot__<tool>`. AdCopilot tools of the second
form and **none** of the first mean a hand-added copy is hiding the plugin's.
Tools of the first form mean the plugin's own connector is there, and there is
nothing to fix.

Then tell them in plain words: a copy of the connector they added by hand is
hiding the plugin's. The steps to remove it, from every place they added it,
are on AdCopilot's page for this plugin:
`https://adcopilot.cloud/docs/connect/claude-code-plugin#already-added-the-connector-by-hand`.
Once their copy is gone, the plugin's connector appears: `/mcp`, choose
`adcopilot` and sign in.

If the connector answers but reports nothing connected, that is the server
working, not a fault: the Google products are connected inside AdCopilot at
`https://app.adcopilot.cloud`, not in this client. Say so and send them there,
rather than letting them hunt for a broken connector.

End as the skill's step 5 does: the one next step, `/adcopilot:launch` or
`/adcopilot:measure`, and why it fits their situation — then the skill's
daily-habit offer, when its conditions hold.

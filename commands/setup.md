---
name: setup
description: Check the AdCopilot connector is connected and signed in, and say what each connected product unlocks.
---

Follow the `adcopilot-connect` skill. If that skill is not installed here (Cursor
can add this command without it), follow `get_org_context`'s `next_step` and
`playbook` instead.

**Work out the surface before you diagnose anything, and Cursor first.** If this
is Cursor (`get_org_context`'s top-level `surface` is `cursor`, or Cursor's own
instructions or the person say so), never run `claude mcp`, not even to check:
Cursor's agent can reach a shell where Claude Code is installed, and that
command lists Claude Code's connectors, not Cursor's, so what it shows, and any
`claude mcp remove` it seems to call for, is about another client. In Cursor the
connector is in Cursor's MCP settings, where one added from cursor.directory may
be named `server` rather than `adcopilot`; it is the same connector. There is no
plugin Connectors tab there and no shadowing to fix. If it is not in the list,
they add it with AdCopilot's Cursor link,
`https://cursor.com/en/install-mcp?name=adcopilot&config=eyJ0eXBlIjoiaHR0cCIsInVybCI6Imh0dHBzOi8vbWNwLmFkY29waWxvdC5jbG91ZC9tY3AifQ%3D%3D`,
or by its URL, `https://mcp.adcopilot.cloud/mcp`. To sign in, Cursor opens
AdCopilot's page, **Let Cursor use your AdCopilot?**, in the browser, and
**Approve** finishes it; there is no key to paste. If **Approve** did nothing,
they remove the connector in Cursor's MCP settings, add it again and press
**Approve** once. Nothing in the next three paragraphs applies in Cursor.

Otherwise, if you can run `claude mcp list`, this is Claude Code and the whole
of the next two paragraphs applies. If you cannot — claude.ai, Cowork, the
desktop app — none of it does: there is no `/mcp`, no `claude mcp list` and no
`claude mcp remove` there, and no shadowing either: claude.ai links a connector
by its URL, so a copy they added by hand before installing the plugin is the
same connector, not a second one. On the web the only question is whether they
have signed in to the plugin's own connector yet: open the plugin from the
plugin list, then its Connectors tab, and Connect `adcopilot` there. Never offer
"Add custom connector" or the connector URL to someone who has this plugin
installed in Claude — the plugin already brings the connector, so it adds
nothing and fixes nothing.

One condition the server cannot see, and only in Claude Code, so check it there:
**a second, hand-added connector**. This plugin already registers `adcopilot`; a copy added from our
site's instructions before the plugin was installed shadows it, and Claude Code
keeps theirs and silently ignores the plugin's. The tell, in `claude mcp list`
(run it, or ask them to paste its `adcopilot` lines): a bare `adcopilot:` line
and **no** `plugin:adcopilot:adcopilot` line. The plugin's registration is the
one named `plugin:adcopilot:adcopilot`; once theirs is gone it appears and asks
them to sign in.

A hand-added copy can sit in more than one scope at once, and one
`claude mcp remove` takes it out of one scope only. Tell them to remove it from
each: `claude mcp remove adcopilot -s user`, and `claude mcp remove adcopilot
-s local` run from the directory it was added in — a local registration belongs
to that directory and is invisible from any other (a project's `.mcp.json` is
`-s project`, from that project). Then `claude mcp list` again until only
`plugin:adcopilot:adcopilot` remains, then `/mcp` to sign in.

If the connector answers but reports nothing connected, that is the server
working, not a fault: the Google products are connected inside AdCopilot at
`https://app.adcopilot.cloud`, not in this client. Say so and send them there,
rather than letting them hunt for a broken connector.

End as the skill's step 5 does: the one next step, `/adcopilot:launch` or
`/adcopilot:measure`, and why it fits their situation — then the skill's
daily-habit offer, when its conditions hold.

---
name: setup
description: Check the AdCopilot connector is connected and signed in, and say what each connected product unlocks.
---

Follow the `adcopilot-connect` skill.

One condition the server cannot see, so check it here: **a second, hand-added
connector**. This plugin already registers `adcopilot`; a copy added from our
site's instructions before the plugin was installed shadows it, and Claude Code
keeps theirs and silently ignores the plugin's. Check `claude mcp list` — run
it, or ask them to paste its `adcopilot` lines: a bare `adcopilot:` line is one
they added by hand; the plugin's registration is named
`plugin:adcopilot:adcopilot`. Tell them to remove theirs with
`claude mcp remove adcopilot` — no scope flag — and keep the plugin's.

End with one suggested next step: `/adcopilot:launch` if there are no campaigns,
`/adcopilot:daily` if there are.

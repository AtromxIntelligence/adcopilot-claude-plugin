---
name: setup
description: Check the AdCopilot connector is connected and signed in, and say what each connected product unlocks.
---

Follow the `adcopilot-connect` skill.

One condition the server cannot see, so check it here: **a second, hand-added
connector**. This plugin already registers `adcopilot`; a copy added from our
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

End as the skill's step 5 does: the one next step, `/adcopilot:launch` or
`/adcopilot:measure`, and why it fits their situation.

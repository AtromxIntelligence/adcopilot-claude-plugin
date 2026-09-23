---
name: setup
description: Check the AdCopilot connector is connected and signed in, and say what each connected product unlocks.
---

Follow the `adcopilot-connect` skill.

Call `get_org_context` and report, in plain language: whether the connector is
connected, which products it reports as connected, and what connecting the rest
would add. Report whatever it names — do not check its answer against a list in
this file, and do not call a product unsupported because it is not mentioned
here.

Two conditions to handle before anything else:

- **Signed out, or the token expired** — every tool call fails the same way.
  Say once: run `/mcp`, choose `adcopilot`, and sign in with Google. Do not retry
  the call in a loop, and do not describe it as a permission problem or an
  outage.
- **A second, hand-added connector** — this plugin already registers
  `adcopilot`. If `claude mcp list` also shows one, the user added it from our
  site's instructions, and Claude Code keeps theirs and silently ignores the
  plugin's. The tell, at the time of writing: a bare `adcopilot:` line and no
  `plugin:adcopilot:adcopilot:` line. Tell them to remove theirs with
  `claude mcp remove adcopilot` — no scope flag — and keep the plugin's.

End with one suggested next step: `/adcopilot:launch` if there are no campaigns,
`/adcopilot:daily` if there are.

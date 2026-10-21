# AdCopilot for Meta Ads

AdCopilot for Meta Ads reads your Meta ad accounts from your AI client:
campaigns, ad sets and ads with their results, who saw them and on which
placements, the ads' text, audiences, your Pages' posts and your pixels'
health. Its skills and commands only read and change nothing in Meta: every
change is yours to make in Meta's own Ads Manager or Events Manager. It reports
Meta on its own,
never added to, compared with or mixed with Google figures, even when
AdCopilot's Google connector is in the same chat.

This plugin bundles the hosted AdCopilot for Meta Ads connector,
`https://mcp.adcopilot.cloud/meta/mcp`, and carries the steps the connector
cannot take for you: where to connect Meta, what Meta's screens ask, and where
in Ads Manager and Events Manager a fix is made.

AdCopilot is made by Atromx Intelligence (https://adcopilot.cloud), not by
Meta, and is not related to other products named AdCopilot. Meta, Facebook and
Instagram are trademarks of Meta Platforms, Inc.

**Status: in testing.** AdCopilot for Meta Ads is not available to customers
yet, and has no date. Only workspaces AdCopilot has switched on for testing can
sign in; for any other, the sign-in page says it isn't available for this
workspace yet. This plugin reaches this repository's marketplace, and any
directory, only once it is available.

## It is a second connector

AdCopilot's Google connector (Google Ads, Google Analytics, Google Search
Console and Google Tag Manager, at `https://mcp.adcopilot.cloud/mcp`) is one
connector and the `adcopilot` plugin. Meta is another: its own address, its own
sign-in on your AI client, its own tools and this plugin. Both sign in to the
same AdCopilot account and workspace, and each is signed in on its own:
signing one in does not sign the other in, and removing one leaves the other.

## Install, for testers

Two steps on every surface: add the connector, then **sign in to it**. Then
connect Meta once, inside AdCopilot at https://app.adcopilot.cloud, not in your
AI client.

### Claude Code

From a checkout of this repository's branch that holds the plugin:

```
claude --plugin-dir plugins/adcopilot-meta
/mcp
```

Once it is released, it installs from this repository's marketplace instead:

```
/plugin install adcopilot-meta --marketplace AtromxIntelligence/adcopilot-claude-plugin
/mcp
```

`/mcp` opens the connector list. Choose `plugin:adcopilot-meta:meta` and sign
in: AdCopilot's page, **Let Claude use AdCopilot for Meta Ads?**, opens in your
browser, and **Approve** finishes it. If you added the connector by hand
before, remove that copy first (`/adcopilot-meta:setup` finds it): Claude Code
keeps a hand-added copy and silently ignores the plugin's.

### claude.ai, Cowork and the desktop app

Until the plugin is listed, add the connector by its address: in Claude's
connector settings, **Add custom connector**, with
`https://mcp.adcopilot.cloud/meta/mcp`, then **Connect** and **Approve**. The
skills ship with the plugin, so on the web you have the connector's own
instructions only.

### Cursor

[Add AdCopilot for Meta Ads to Cursor](https://cursor.com/en/install-mcp?name=adcopilot-meta&config=eyJ0eXBlIjoiaHR0cCIsInVybCI6Imh0dHBzOi8vbWNwLmFkY29waWxvdC5jbG91ZC9tZXRhL21jcCJ9)
opens Cursor with the connector named `adcopilot-meta`. Or put it in
`~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "adcopilot-meta": {
      "url": "https://mcp.adcopilot.cloud/meta/mcp"
    }
  }
}
```

Cursor opens AdCopilot's page, **Let Cursor use AdCopilot for Meta Ads?**:
press **Approve**.

### Then, on every surface

Run `/adcopilot-meta:setup` (or say "get me started with AdCopilot for Meta
Ads"). It says whether Meta is connected in AdCopilot and which ad accounts are
switched on, and sends you to the right page for each step. Connecting Meta
uses Meta's own **Facebook Login for Business** screens: you choose the
business portfolio, then the ad accounts, Pages and pixels AdCopilot may read.

**If the `adcopilot` plugin is installed too:** its `adcopilot-meta` skill was
written for Meta's own connector, before AdCopilot had one: it says AdCopilot
has no Meta integration and reads two platforms side by side. This plugin's
skills tell Claude to follow them, not that skill, for a Meta question. While
you test, start a Meta conversation with one of the commands below, so this
plugin's skill is the one that runs; to rule the other skill out entirely,
test in a Claude Code session without the `adcopilot` plugin (`/plugin`, then
disable it for the session). That skill is rewritten when AdCopilot for Meta
Ads is released.

## What you get

Three commands, which you type:

- `/adcopilot-meta:setup` — checks the connector is signed in on this client
  and Meta is connected in AdCopilot, says which ad accounts it reads, and in
  Claude Code finds a hand-added copy that shadows the plugin's.
- `/adcopilot-meta:review` — reads an ad account: the account, its campaigns,
  ad sets and ads, who saw them and where, and says what happened, what it cost
  and what to look at in Ads Manager.
- `/adcopilot-meta:pixel` — checks the account's pixels: firing or not, the
  last 7 days' events and event match quality, and says what to fix in Events
  Manager.

Three skills, which Claude draws on when the conversation calls for them:

- **meta-connect** — sets up the connector and the Meta connection, and says
  what each step bought you.
- **meta-review** — the everyday read: account, then campaigns, then ad sets and
  ads, then who saw them and where, the ads' text and the audiences, in the
  account's own currency and time zone, saying when Meta may still be
  updating the results it read.
- **meta-tracking** — pixel and dataset health, and where in Events Manager
  each fix is made.

## What it will not do

- **Change anything in Meta.** The plugin's steps only read. Every change is
  made by you, in Meta's own screens.
- **Mix Meta with Google.** It reports Meta on its own, and sends nothing read
  from Meta into AdCopilot's Google tools.
- **See what you did not share.** It reads only the ad accounts, Pages and
  pixels you ticked on Meta's screens, and only the ad accounts switched on in
  your AdCopilot workspace.

## Support

- Something wrong with the plugin (a command, a skill, this README): [open an
  issue](https://github.com/AtromxIntelligence/adcopilot-claude-plugin/issues).
- Something wrong with the connector (sign-in, a tool call, your account):
  support@adcopilot.cloud.
- Privacy: https://adcopilot.cloud/privacy. Terms: https://adcopilot.cloud/terms.

## Version

**0.1.0 (2026-10-21): the first version, in testing, and not released.** It is
written against AdCopilot's Meta connector as designed, before that connector
is deployed: the tool names and the `meta_get_context` fields it relies on are
checked against the live connector before any release. It ships three skills
and three commands, and no agent. Every first call passes
`source: "claude-plugin-meta/0.1.0"`, which tells AdCopilot which of this
plugin's steps are installed.

## Licence

MIT. Copyright Atromx Intelligence Private Limited. See [LICENSE](LICENSE).

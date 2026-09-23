# AdCopilot for Claude Code

Run Google Ads, Google Analytics, Search Console and Tag Manager from Claude Code. This plugin bundles the hosted AdCopilot connector and carries the steps the connector cannot take for you: what to click in Google's own screens, and the traps that are easy to fall into.

The plugin is free (MIT). The connector is a hosted service — plans at https://adcopilot.cloud/pricing.

## Install

In Claude Code:

```
/plugin marketplace add AtromxIntelligence/adcopilot-claude-plugin
/plugin install adcopilot@adcopilot-claude-plugin
/mcp
```

The last step opens the connector list. Choose `adcopilot` and sign in with your own Google account. There is no `claude mcp add` step: the plugin registers the connector at `https://mcp.adcopilot.cloud/mcp` for you.

If you had already added the connector by hand before installing, Claude Code keeps yours and silently ignores the plugin's. Remove yours with `claude mcp remove adcopilot` so the plugin's registration takes over.

## What you get

Five commands, which you type:

- `/adcopilot:setup` — checks the connector is connected and signed in, says what each connected product unlocks, and catches the two ways a fresh install goes wrong: a lapsed sign-in, and a copy of the connector you added by hand before installing.
- `/adcopilot:launch` — a first Search campaign, through the `adcopilot-launch` skill below.
- `/adcopilot:measure` — conversion tracking, through the `adcopilot-measure` skill below.
- `/adcopilot:daily` — the daily check-in: what was spent since yesterday, the searches the ads showed for, and what changed in the account — in that order, as far as the connector's read cap for the day allows.
- `/adcopilot:audit` — the connector's full audit and this month's budget pacing, with what is only newness kept out of the findings.

Three skills, which Claude draws on when the conversation calls for them:

- **adcopilot-connect** — sets up AdCopilot, connects your Google products and links them to each other in the order that works, saying what each step bought you as it happens.
- **adcopilot-measure** — sets up conversion tracking end to end: the Analytics property and data stream, the Tag Manager tags, the key event, the Analytics-to-Ads link and the import, and ends with exactly one Primary conversion, proven by a real click.
- **adcopilot-launch** — builds a first Search campaign switched off, on the budget and bid you name: locations, never-show-for words, ad groups, keywords with their match types, ads and assets; verifies the settings that leak money by reading the campaign back; hands you the go-live switch; and runs the first week's checks, reading why a switched-on campaign is not delivering before it sends you to any screen.

Together with the connector registration above, the commands and skills above are what the plugin ships at this version.

## What it will not do

- **Switch a campaign on.** Every campaign it builds is created paused. You switch it on in Google Ads yourself.
- **Delete anything.** Remove tools are not exposed, and the connector refuses a REMOVED status server-side. Pausing is as far as it goes.
- **Spend without being asked.** Reads run freely; every write is proposed first and applied only after you say yes in that conversation.

## Support

- Something wrong with the plugin (a command, a skill, this README): [open an issue here](https://github.com/AtromxIntelligence/adcopilot-claude-plugin/issues).
- Something wrong with the connector (sign-in, a tool call, your account): support@adcopilot.cloud.

## AdCopilot version

Written against AdCopilot **v2.14.1** (connector tools revision `e9328870`, snapshot taken 2026-09-23). `/adcopilot:audit` relies on the `tools_revision` that `get_org_context` reports from v2.14.1 on, to refresh a stale tool description in-conversation.

## Evals, and how a skill earns its place

The suite in `evals/` runs with `claude plugin eval . --trust-plugin --threshold 0.8`, which is what CI runs on every push. The harness's own with/without comparison removes the whole plugin — connector included — so it cannot say what a skill adds; `evals/ablation/tools-only.sh` runs the same cases against a copy of the plugin whose skills are cut to their frontmatter and prints each skill's delta over that tools-only arm. A skill whose cases show no delta there is deleted, not kept. Fixtures under `evals/**/mocks/` are a fictional tenant: the field names follow the live connector's answers and every value is invented.

## Releasing

Before a version tag is pushed, in a fresh Claude Code — a profile with no hand-added `adcopilot` server (`CLAUDE_CONFIG_DIR=$(mktemp -d) claude` gives you one):

1. `/plugin marketplace add AtromxIntelligence/adcopilot-claude-plugin`
2. `/plugin install adcopilot@adcopilot-claude-plugin`
3. `/mcp` — choose `adcopilot` and sign in with the Google account that owns the ad account.
4. `/adcopilot:setup` on a real account: it reports what is connected, in prose, and one next step.
5. `/adcopilot:audit` on the same account: the full audit and this month's pacing, with newness kept out of the findings.
6. `claude plugin validate . --strict` and `claude plugin validate .claude-plugin/plugin.json --strict` both pass; the suite passes at 0.8; every skill's delta in `evals/ablation/tools-only.sh` is positive.
7. Record the AdCopilot version and `tools_revision` the steps above ran against, in the release notes and in the section above.

## Licence

MIT. Copyright Atromx Intelligence Private Limited. See [LICENSE](LICENSE).

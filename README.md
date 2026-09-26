# AdCopilot for Claude Code

Run your Google advertising stack — Google Ads, Analytics, Search Console, Tag Manager and whatever else AdCopilot has connected since — from Claude Code. This plugin bundles the hosted AdCopilot connector and carries the steps the connector cannot take for you: what to click in Google's own screens, and the traps that are easy to fall into.

The plugin is free (MIT). The connector is a hosted service — plans at https://adcopilot.cloud/pricing.

## Install

In Claude Code:

```
/plugin marketplace add AtromxIntelligence/adcopilot-claude-plugin
/plugin install adcopilot@adcopilot-claude-plugin
/mcp
```

The last step opens the connector list. Choose `adcopilot` and sign in with your own Google account. There is no `claude mcp add` step: the plugin registers the connector at `https://mcp.adcopilot.cloud/mcp` for you. Signing in links your AdCopilot workspace, so you need an AdCopilot account; your Google products are connected once, in AdCopilot at https://app.adcopilot.cloud, not in Claude Code — `/adcopilot:setup` tells you which are missing and sends you to the right page.

If you had already added the connector by hand before installing, Claude Code keeps yours and silently ignores the plugin's: `claude mcp list` then shows a bare `adcopilot:` line and no `plugin:adcopilot:adcopilot` line. Remove yours from every scope it is in — `claude mcp remove adcopilot -s user`, and `claude mcp remove adcopilot -s local` run from the directory you added it in, because a local registration belongs to that directory — and the plugin's line appears and asks you to sign in.

## What you get

Five commands, which you type:

- `/adcopilot:setup` — checks the connector is connected and signed in, says what each connected product unlocks, and catches the two ways a fresh install goes wrong: a lapsed sign-in, and a copy of the connector you added by hand before installing.
- `/adcopilot:launch` — a first Search campaign, through the `adcopilot-launch` skill below.
- `/adcopilot:measure` — conversion tracking, through the `adcopilot-measure` skill below.
- `/adcopilot:daily` — the daily check-in: what was spent since yesterday, the searches the ads showed for, and what changed in the account — in that order, as far as the connector's read cap for the day allows.
- `/adcopilot:audit` — the connector's full audit and this month's budget pacing, with the findings that are only a symptom of a brand-new account kept separate.

Three skills, which Claude draws on when the conversation calls for them:

- **adcopilot-connect** — sets up AdCopilot, connects your Google products and links them to each other in the order that works, saying what each step bought you as it happens.
- **adcopilot-measure** — sets up conversion tracking end to end: the Analytics property and data stream, the Tag Manager tags, the key event, the Analytics-to-Ads link and the import, and ends with exactly one Primary conversion, proven by a real click.
- **adcopilot-launch** — builds a first Search campaign switched off, on the budget and bid you name: locations, never-show-for words, ad groups, keywords with their match types, ads and assets; verifies the settings that leak money by reading the campaign back; hands you the go-live switch; and runs the first week's checks, reading why a switched-on campaign is not delivering before it sends you to any screen.

Together with the connector registration above, the commands and skills above are what the plugin ships at this version.

## What it will not do

- **Switch a campaign on.** Every campaign it builds is created paused. You switch it on in Google Ads yourself.
- **Delete anything.** The connector refuses a REMOVED status server-side: the campaign, ad group, ad and keyword tools accept only ENABLED or PAUSED, and the asset tools refuse a remove outright. Pausing is as far as it goes, and it is the server that enforces that rather than the assistant's good manners.
- **Spend without being asked.** Reads run freely; every write is proposed first and applied only after you say yes in that conversation.

## Support

- Something wrong with the plugin (a command, a skill, this README): [open an issue here](https://github.com/AtromxIntelligence/adcopilot-claude-plugin/issues).
- Something wrong with the connector (sign-in, a tool call, your account): support@adcopilot.cloud.

## AdCopilot version

Written against AdCopilot **v2.14.1**. The tool snapshot the eval suite mocks against (`evals/mocks/adcopilot/_tools.json`) is frozen at connector tools revision `0066a60e`, taken 2026-09-23; the live revision moves independently of this plugin, and a difference between the two is not a fault. `/adcopilot:audit` relies on the `tools_revision` that `get_org_context` reports from v2.14.1 on, to refresh a stale tool description in-conversation.

## Evals, and how a skill earns its place

The suite in `evals/` runs with `claude plugin eval . --trust-plugin --ablation none --threshold 0.8 --judge-model sonnet --concurrency 2 --max-cost-usd 20 --no-publish`, which the release checklist below runs before a version tag — by hand, because no workflow in this repository runs Claude Code (see **Why there is no CI** at the end) (the judge model is not incidental: the same case scored 0.81 under the default judge and 0.905 under sonnet). The harness's own with/without comparison removes the whole plugin — connector included — so it cannot say what a skill adds; `evals/ablation/tools-only.sh` runs the same cases against a copy of the plugin whose skills are cut to their frontmatter and prints each skill's delta over that tools-only arm. A skill whose cases show no delta there is deleted, not kept; the gate reads on each skill's weakest case as well as its mean, so one strong case cannot carry a dead one — and a case the tools-only arm already passes at 0.8 is a regression guard on the connector, not evidence about the skill, so it is held at 0.8 and left out of the delta. Fixtures under `evals/**/mocks/` are a fictional tenant: the field names follow the live connector's answers and every value is invented.

## Releasing

Before a version tag is pushed, in a fresh Claude Code — a profile with no hand-added `adcopilot` server (`CLAUDE_CONFIG_DIR=$(mktemp -d) claude` gives you one):

1. `/plugin marketplace add AtromxIntelligence/adcopilot-claude-plugin`
2. `/plugin install adcopilot@adcopilot-claude-plugin`
3. `/mcp` — choose `adcopilot` and sign in with the Google account that owns the ad account.
4. `/adcopilot:setup` on a real account: it reports what is connected, in prose, and one next step.
5. `/adcopilot:audit` on the same account: the full audit and this month's pacing, with the brand-new-account findings kept separate.
6. `claude plugin validate . --strict` and `claude plugin validate .claude-plugin/plugin.json --strict` both pass; the suite passes at 0.8; the tools-only ablation is green — every skill's delta over the connector plus its own frontmatter description (the tools-only arm keeps the frontmatter so the skill still fires), on its mean and on its weakest case among the cases that baseline does not already carry, is at least 0.05 (`ABLATION_FAIL_BELOW=0.05 evals/ablation/tools-only.sh`). A case the tools-only arm passes at 0.8 is a regression guard on the connector's own behaviour: it must still pass at 0.8 with the skill, and it is left out of the skill's delta. A red ablation blocks the tag: the skill it names is fixed or deleted first.
7. Record the AdCopilot version and `tools_revision` the steps above ran against, in the release notes and in the section above.

## Licence

MIT. Copyright Atromx Intelligence Private Limited. See [LICENSE](LICENSE).

## Why there is no CI

No workflow in this repository runs Claude Code. It had one — `claude plugin
validate --strict` on every push, the eval gate, and the tools-only ablation on
dispatch — and it was removed on 2026-09-26 for the plugin directory
submission: its only way to install Claude Code on a runner was a piped shell
installer, and the scanner holds a download-and-execute pattern anywhere in the
repository for review, whoever published the script being fetched.

Nothing about the gates themselves changed. `evals/` is intact, and the
release checklist above is the contract: no version tag without both
`--strict` validations, the suite at 0.8, and a green tools-only ablation.
They are now run by the person cutting the release rather than by a runner,
which means they can be skipped — so the checklist, not a green tick, is what
stands between a broken skill and a tag.

The one workflow here is the leak check, `.github/workflows/leak-check.yml`:
gitleaks over every commit, on each push to `main` and each pull request. It
runs gitleaks from its published container image, pinned by digest, reads no
secret, and fails when the scan finds a possible credential or reads no commits
at all. GitHub's own secret scanning and push protection are also switched on
for this repository, so a push carrying a secret type GitHub recognises is
blocked unless the pusher deliberately bypasses the block.

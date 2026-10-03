# AdCopilot for Claude Code

Run your Google advertising stack — Google Ads, Analytics, Search Console, Tag Manager and whatever else AdCopilot has connected since — from Claude Code. This plugin bundles the hosted AdCopilot connector and carries the steps the connector cannot take for you: what to click in Google's own screens, and the traps that are easy to fall into.

The plugin is free (MIT). The connector is a hosted service — plans at https://adcopilot.cloud/pricing.

## Install

Two steps on every surface: add the plugin, then **sign in to the connector it
brings with it**. The second step is the one people miss, and nothing works
until it is done.

### claude.ai, Cowork and the desktop app

1. Add the plugin: open
   [AdCopilot in the plugin directory](https://claude.ai/new#customize/plugins/id/c9bfd1ff-d329-4949-91fb-dc97116194ae%40anthropic-plugin-directory),
   or go to **Customize**, then **Plugins**, and search for AdCopilot. Click
   **Add**.
2. In the plugin, open its **Connectors** tab, click **Connect** beside
   `adcopilot`, and sign in.

The connector is already listed — there is nothing to add, and no need for
"Add custom connector" or the connector URL: the plugin registers it for you.
If you added AdCopilot by hand before installing the plugin, nothing breaks:
Claude links a connector by its URL, so you still have one AdCopilot connector,
the same one.

If you clicked **Try in Cowork** straight from the listing, you landed in a chat
before step 2 — the connector will report as missing. Do step 2 and say "get me
started" again.

### Claude Code

```
/plugin marketplace add AtromxIntelligence/adcopilot-claude-plugin
/plugin install adcopilot@adcopilot-claude-plugin
/mcp
```

The last step opens the connector list. Choose `adcopilot` and sign in with your own Google account. There is no `claude mcp add` step: the plugin registers the connector at `https://mcp.adcopilot.cloud/mcp` for you. Signing in links your AdCopilot workspace, so you need an AdCopilot account; your Google products are connected once, in AdCopilot at https://app.adcopilot.cloud, not in Claude Code — `/adcopilot:setup` tells you which are missing and sends you to the right page.

### Then, on every surface

Signing in to the connector links your **AdCopilot workspace**, so you need an
AdCopilot account. Your Google products — Google Ads, Analytics, Search Console,
Tag Manager — are connected **once, inside AdCopilot at
https://app.adcopilot.cloud**, not in Claude. So a fresh sign-in can report
nothing connected: that is the server answering correctly, not a fault.

Run `/adcopilot:setup` first. It says what is connected, what is not, and sends
you to the right page for each.

If you had already added the connector by hand before installing (Claude Code only — the web has no such command), Claude Code keeps yours and silently ignores the plugin's: `claude mcp list` then shows a bare `adcopilot:` line and no `plugin:adcopilot:adcopilot` line. Remove yours from every scope it is in — `claude mcp remove adcopilot -s user`, and `claude mcp remove adcopilot -s local` run from the directory you added it in, because a local registration belongs to that directory — and the plugin's line appears and asks you to sign in.

## What you get

Five commands, which you type:

- `/adcopilot:setup` — checks the connector is connected and signed in, says what each connected product unlocks, and catches the two ways a fresh install goes wrong: a lapsed sign-in, and, in Claude Code, a copy of the connector you added by hand before installing.
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
- **Change your account unasked, while the write tools need approval.** Reads run freely. Your AI client asks before each change while the write tools stay on **Needs approval** (claude.ai, Cowork and the desktop app) or, in Claude Code, while it still prompts for them: the tools are not allowlisted and the session is not in `auto` or `bypassPermissions` mode. Take the question away and changes to what already exists, a budget or a switched-on campaign among them, apply without it; only a new campaign is still built paused.

## Support

- Something wrong with the plugin (a command, a skill, this README): [open an issue here](https://github.com/AtromxIntelligence/adcopilot-claude-plugin/issues).
- Something wrong with the connector (sign-in, a tool call, your account): support@adcopilot.cloud.

## AdCopilot version

Written against AdCopilot **v2.29.0**. The tool snapshot the eval suite mocks against (`evals/mocks/adcopilot/_tools.json`) is frozen at connector tools revision `0066a60e`, taken 2026-09-23 under v2.14.1, except its `get_org_context` entry, which is the live schema at revision `782ec74d` (read 2026-10-03) so that the eval model is offered `source` as a real client is — every case that reads the server fails its `marks-plugin-use` grader on a `get_org_context` call without `source: "claude-plugin"`; the live revision moves independently of this plugin, and a difference between the two is not a fault. `/adcopilot:audit` relies on the `tools_revision` that `get_org_context` reports from v2.14.1 on, to refresh a stale tool description in-conversation. The skills and `/adcopilot:audit` call `get_org_context` with `source: "claude-plugin"`, which AdCopilot reads from v2.29.0 on to record plugin use per workspace; calls without it behave as before.

## Evals, and how a skill earns its place

The suite in `evals/` runs with `claude plugin eval . --trust-plugin --ablation none --threshold 0.8 --judge-model sonnet --concurrency 2 --max-cost-usd 20 --no-publish`, which the release checklist below runs before a version tag — by hand, because it drives a model and no workflow here holds a credential to sign Claude Code in (see **What CI runs, and what it does not** at the end) (the judge model is not incidental: the same case scored 0.81 under the default judge and 0.905 under sonnet). The harness's own with/without comparison removes the whole plugin — connector included — so it cannot say what a skill adds; `evals/ablation/tools-only.sh` runs the same cases against a copy of the plugin whose skills are cut to their frontmatter and prints each skill's delta over that tools-only arm. A skill whose cases show no delta there is deleted, not kept; the gate reads on each skill's weakest case as well as its mean, so one strong case cannot carry a dead one — and a case the tools-only arm already passes at 0.8 is a regression guard on the connector, not evidence about the skill, so it is held at 0.8 and left out of the delta. Fixtures under `evals/**/mocks/` are a fictional tenant: the field names follow the live connector's answers and every value is invented.

## Releasing

Before a version tag is pushed, in a fresh Claude Code — a profile with no hand-added `adcopilot` server (`CLAUDE_CONFIG_DIR=$(mktemp -d) claude` gives you one):

1. `/plugin marketplace add AtromxIntelligence/adcopilot-claude-plugin`
2. `/plugin install adcopilot@adcopilot-claude-plugin`
3. `/mcp` — choose `adcopilot` and sign in with the Google account that owns the ad account.
4. `/adcopilot:setup` on a real account: it reports what is connected, in prose, and one next step.
5. `/adcopilot:audit` on the same account: the full audit and this month's pacing, with the brand-new-account findings kept separate.
6. `claude plugin validate . --strict` and `claude plugin validate .claude-plugin/plugin.json --strict` both pass; the suite passes at 0.8; the tools-only ablation is green — every skill's delta over the connector plus its own frontmatter description (the tools-only arm keeps the frontmatter so the skill still fires), on its mean and on its weakest case among the cases that baseline does not already carry, is at least 0.05 (`ABLATION_FAIL_BELOW=0.05 evals/ablation/tools-only.sh`). A case the tools-only arm passes at 0.8 is a regression guard on the connector's own behaviour: it must still pass at 0.8 with the skill, and it is left out of the skill's delta. A red ablation blocks the tag: the skill it names is fixed or deleted first.
7. Record the AdCopilot version and `tools_revision` the steps above ran against, in the release notes and in the section above — **and the `claudeVersion` the suite ran under**, which `evals/results/<run>/aggregate-result.json` already stores. A score is only comparable to another score from the same build: on 2026-09-23 under `2.1.280` these cases scored `audit-stale-tools` 1.00, `connect-teaches` 1.00, `measure-teaches` 1.00 and `setup-duplicate-server` 1.00; on 2026-10-02 under `2.1.288`, with the plugin byte-identical (`plugins[0].version` 0.1.0 in both) and the same judge alias, they scored 0.67, 0.83, 0.67 and 0.77. Nothing in the plugin had changed. So a case that drops is a question — plugin, harness, or the `sonnet` alias resolving to a new snapshot — and not yet an answer: diff the two runs' `claudeVersion` before editing a skill, or you will fit the prompts to one build and refit them on the next.

## Licence

MIT. Copyright Atromx Intelligence Private Limited. See [LICENSE](LICENSE).

## What CI runs, and what it does not

Two workflows run on every push to `main` and every pull request, and neither
reads a secret.

`.github/workflows/checks.yml` is the structural half of the release gates. It
installs Claude Code from npm at a pinned version (`2.1.288`) and runs both
`--strict` validations, `claude plugin validate . --strict` and
`claude plugin validate .claude-plugin/plugin.json --strict`, which read local
files and need no sign-in. It also checks that the three manifests parse, that
every skill and command carries a `name:` and a `description:`, that no
download-and-execute pattern is back anywhere in the repository, and that the
manifest version is not behind the latest tag.

`.github/workflows/leak-check.yml` runs gitleaks over every commit. It runs
gitleaks from its published container image, pinned by digest, and fails when
the scan finds a possible credential or reads no commits at all. GitHub's own
secret scanning and push protection are also switched on for this repository,
so a push carrying a secret type GitHub recognises is blocked unless the pusher
deliberately bypasses the block.

What no workflow runs is the eval suite and the tools-only ablation. Both drive
a model, which needs a signed-in Claude Code, and these jobs hold no
credential. The person cutting the release runs them, which means they can be
skipped, so the checklist above, not a green tick, is what stands between a
broken skill and a tag: no version tag without both `--strict` validations,
the suite at 0.8, and a green tools-only ablation.

The first workflow here ran all of it, the eval gate and the ablation included.
It was removed on 2026-09-26 for the plugin directory submission: its only way
to install Claude Code on a runner was a piped shell installer, and the
directory's scanner holds a download-and-execute pattern anywhere in the
repository for review, whoever published the script being fetched. Installing
from npm at a pinned version is not that pattern, which is why `checks.yml`
could come back.

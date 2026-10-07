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

Seven commands, which you type:

- `/adcopilot:setup` — checks the connector is connected and signed in, says what each connected product unlocks, and catches the two ways a fresh install goes wrong: a lapsed sign-in, and, in Claude Code, a copy of the connector you added by hand before installing.
- `/adcopilot:launch` — a first Search campaign, through the `adcopilot-launch` skill below.
- `/adcopilot:measure` — conversion tracking, through the `adcopilot-measure` skill below.
- `/adcopilot:daily` — the daily check-in: this month's budget pacing, the last seven days' searches that cost money and brought nothing, any ad Google has disapproved or limited, and what changed in the account since yesterday and who changed it — in that order, as far as the connector's read cap for the day allows.
- `/adcopilot:weekly` — last Monday to Sunday against the week before: spend, conversions and cost per conversion, the three biggest changes, and three things to do this week, written to be forwarded.
- `/adcopilot:negatives` — the last seven days' searches that cost money and brought nothing, grouped by theme, with the never-show-for words (negative keywords) that would block them; added only after your yes, then read back.
- `/adcopilot:audit` — the connector's full audit and this month's budget pacing, with the findings that are only a symptom of a brand-new account kept separate.

Seven skills, which Claude draws on when the conversation calls for them:

- **adcopilot-connect** — sets up AdCopilot, connects your Google products and links them to each other in the order that works, saying what each step bought you as it happens.
- **adcopilot-measure** — sets up conversion tracking end to end: the Analytics property and data stream, the Tag Manager tags, the key event, the Analytics-to-Ads link and the import, and ends with exactly one Primary conversion, proven by a real click.
- **adcopilot-launch** — builds a first Search campaign switched off, on the budget and bid you name: locations, never-show-for words, ad groups, keywords with their match types, ads and assets; verifies the settings that leak money by reading the campaign back; hands you the go-live switch; and runs the first week's checks, reading why a switched-on campaign is not delivering before it sends you to any screen.
- **adcopilot-daily** — the morning check a Claude scheduled task or a Claude Code routine runs while nobody is there: it is written to read only and never ask a question, opens with "All clear" or "Needs a look" and ends with the one fix worth doing, as a yes/no question for when you open it. It also holds the steps for setting that schedule up.
- **adcopilot-review** — the everyday one: reads the account and says what happened, what it cost, what is wasting money and what to change, then proposes the change and applies it when you say yes. It opens with `full_audit`, because one lens is one read and answers what a dozen hand-written queries would, and it treats the read ceiling as something to spend rather than stay under.
- **adcopilot-docs** — answers questions about AdCopilot itself from your live workspace rather than from memory: which products it reaches, how many look-ups are left today and what happens when they run out, which plan you are on, what it is allowed to change, where data goes, and what to do when a call fails. Plans and prices are linked, never quoted.
- **adcopilot-seo** — answers what Google search makes of your site, through Search Console: which pages earn clicks and which earn nothing, what people typed to find you, whether a sitemap is being read, and when a page was last crawled. It is written around the readings that mislead — the sitemap's dead "indexed" column, an average position that is not a rank, impressions that are not demand — and it says plainly what it cannot see: there is no site-wide coverage list and no penalty read, so it asks you for Search Console's Pages export rather than guessing.

One agent, which Claude hands a job to when it is too big for the conversation:

- **adcopilot-auditor** — a full account audit end to end, returning findings with the numbers behind them and the changes worth making. It reads and proposes only: it holds no write tool, so it cannot apply anything, and the conversation that asked for it takes your yes.

Together with the connector registration above, the commands, skills and agent above are what the plugin ships at this version.

### Every morning, without asking

Every command above, and the connect, launch and measure skills, once it has done its job on an account with a campaign switched on, ends with one short offer to make a morning check of that account a daily habit: in claude.ai, Cowork or the desktop app, a Claude **scheduled task**; in Claude Code, a **routine** made with `/schedule`, which it offers to create for you. Say "schedule it" and it walks you through the steps; say no and it does not offer again in that conversation. The offer stops for good once AdCopilot reports a schedule — one you recorded with it, or a scheduled run that has checked in.

The instructions you save are AdCopilot's own morning-check recipe, word for word, filled in with your account. A run reads about five times, and each read counts toward your workspace's daily operations. If AdCopilot already emails you its daily check-in, that keeps coming as well; the Routine card on AdCopilot's Home page pauses it if you want only one. Scheduled tasks need a Claude plan that has them; on Claude's Free plan, AdCopilot's emailed daily check-in, when it is on, is the morning check.

**A scheduled run is told not to change anything.** The instructions `adcopilot-daily` gives you are read-only and ask no questions; a fix it finds is a question for when you open the report. Nothing on AdCopilot's side stops a change in a scheduled run, though. A Claude Code routine runs its tools without asking, and so does a scheduled task switched to **Automatically approve**; in those, the instructions are what keep the run to reads, so keep them as written. In claude.ai, Cowork and the desktop app, setting AdCopilot's **Write/delete tools** to **Blocked** stops a change outright, in every chat as well as in the run.

## What it will not do

- **Switch a campaign on.** Every campaign it builds is created paused. You switch it on in Google Ads yourself.
- **Delete anything but a negative keyword.** The connector refuses a REMOVED status server-side: the campaign, ad group, ad and keyword tools accept only ENABLED or PAUSED, and the asset tools refuse a remove outright. Pausing is as far as it goes for all of those, and it is the server that enforces that rather than the assistant's good manners. The one exception is deliberate: each of the three ways to add a negative keyword has a removal behind it, so a negative can be taken back out — which is what makes "you can undo this" true when AdCopilot says it. Attaching a shared negative-keyword list is the genuinely one-way action; there is no detach tool, and a list is detached in Google Ads under Tools, Shared library, Exclusion lists.
- **Change your account unasked, while the write tools need approval.** Reads run freely. Your AI client asks before each change while the write tools stay on **Needs approval** (claude.ai, Cowork and the desktop app) or, in Claude Code, while it still prompts for them: the tools are not allowlisted and the session is not in `auto` or `bypassPermissions` mode. Take the question away and changes to what already exists, a budget or a switched-on campaign among them, apply without it; only a new campaign is still built paused.

## Support

- Something wrong with the plugin (a command, a skill, this README): [open an issue here](https://github.com/AtromxIntelligence/adcopilot-claude-plugin/issues).
- Something wrong with the connector (sign-in, a tool call, your account): support@adcopilot.cloud.

## AdCopilot version

Written against AdCopilot **v2.34.0** (connector tools revision `7016a0aa`, read live on 2026-10-06). The review, docs, Search Console and auditor components were written and checked against that server; the earlier flows were written against v2.30.2 and re-checked against v2.34.0 for the claims they make. The tool snapshot the eval suite mocks against (`evals/mocks/adcopilot/_tools.json`) is frozen at connector tools revision `0066a60e`, taken 2026-09-23 under v2.14.1, except its `get_org_context` entry, which is the live schema at revision `782ec74d` (read 2026-10-03) so that the eval model is offered `source` as a real client is — every case that reads the server fails its `marks-plugin-use` grader on a `get_org_context` call without `source: "claude-plugin"`; the live revision moves independently of this plugin, and a difference between the two is not a fault. `/adcopilot:audit` relies on the `tools_revision` that `get_org_context` reports from v2.14.1 on, to refresh a stale tool description in-conversation. The skills and `/adcopilot:audit` call `get_org_context` with `source: "claude-plugin"`, which AdCopilot reads from v2.29.0 on to record plugin use per workspace; calls without it behave as before. `adcopilot-daily`'s unattended run passes `source: "claude-scheduled"` instead, and the daily-habit offer stops when `get_org_context` reports `routine.daily.status` `user_set` or a date in `routine.scheduled_last_seen_at`, the two things that stop the server's own schedule offer. AdCopilot records that marker, and reports `routine.scheduled_last_seen_at`, `routine.daily.customer_id` (the account its own check-in reads) and `latest_check_in`, from v2.30.2 on; on an earlier server the value is ignored and those fields are absent, so the offer stops only for a schedule recorded with `save_org_context`, which AdCopilot refuses while its own emailed check-in (`in_app`) holds the routine. The instructions the set-up hands over are AdCopilot's recipe (`SCHEDULED_CHECKIN`, from v2.30.2 on) word for word, and `tests/test_structure.py` holds the skill's copy to it. The new cases for `/adcopilot:daily` and the scheduled run add case-level `_tools.json` entries for `analyze_search_terms`, `add_negative_keywords`, `update_campaign` and `save_org_context`, read live at revision `782ec74d` on 2026-10-04, and their `get_org_context` mocks carry the new fields; the suite-wide snapshot is unchanged. The cases for the review and Search Console skills do the same: `review-spends-the-depth` pins `analyze_waste` and `analyze_search_terms` at revision `7016a0aa` and `full_audit` at revision `6145d0b5`, and `seo-two-numbers-that-lie` pins the five Search Console tools at `7016a0aa`, all read live on 2026-10-06. `full_audit` is pinned deliberately: the suite-wide snapshot's older copy of its description says findings come back “ranked by impact”, and the live one says the opposite — failures first, then by severity, not impact — which is the fact the review case is built on, so a case left on the snapshot would have measured the skill against a description that contradicts the server. Each tool's `Tools revision` is a hash of that tool's own text, so tools read in the same listing can report different ones; only the value `get_org_context` returns is the connector's.

## Evals, and how a skill earns its place

The suite in `evals/` runs with `claude plugin eval . --trust-plugin --ablation none --threshold 0.8 --judge-model sonnet --concurrency 2 --max-cost-usd 20 --no-publish`, which the release checklist below runs before a version tag — by hand, because it drives a model and no workflow here holds a credential to sign Claude Code in (see **What CI runs, and what it does not** at the end) (the judge model is not incidental: the same case scored 0.81 under the default judge and 0.905 under sonnet). The harness's own with/without comparison removes the whole plugin — connector included — so it cannot say what a skill adds; `evals/ablation/tools-only.sh` runs the same cases against a copy of the plugin whose skills are cut to their frontmatter and prints each skill's delta over that tools-only arm. A skill whose cases show no delta there is deleted, not kept; the gate reads on each skill's weakest case as well as its mean, so one strong case cannot carry a dead one — and a case the tools-only arm already passes at 0.8 is a regression guard on the connector, not evidence about the skill, so it is held at 0.8 and left out of the delta. Fixtures under `evals/**/mocks/` are a fictional tenant: the field names follow the live connector's answers and every value is invented. Each of the seven skills owns at least one case it earns — twenty-one cases across the suite — which is what `evals/ablation/delta.py`'s `TAG_TO_SKILL` records — a skill with no case of its own fails the gate outright, because nothing measures it. The four newest cases are built the other way round from the rest: each one grades only what its skill's BODY adds, after subtracting what the tool descriptions and the server's own `playbook` already say. For the review skill that meant dropping “biggest money first” as the thing measured — the live playbook for a tracked account says it in those words — and measuring the deep-depth call, the coverage number, the micros rule and the two-sided recommendation instead.

0.2.5's ablation is also the first run where the gate said no, and what it caught is worth keeping: `adcopilot-seo`'s only case scored **0.852 on the tools-only arm**, above the 0.8 line, so it was classed a regression guard, left out of the delta, and the skill was left with no gated case — FAIL, “no case the baseline does not carry”. The skill was not the problem. The case was: six of its seven graders passed on the baseline. **Three traps written as the skill's knowledge turned out to be things a capable model already does** — it passes `row_limit` explicitly without being told to, it does not reach for a write tool unasked, and it knows an average position is an average. Only the sitemap's dead `indexed` field survived (1/3 on the baseline, 3/3 with the skill). The remedy the rule prescribes for a skill with no delta is deletion, and it would have been the wrong one here; the right one was a case aimed at what that arm got wrong, which is `seo-discovered-is-not-a-verdict`. So: a red ablation names a skill, but read which graders moved before believing it is the skill that is dead. Two negative deltas in the same run — `audit-stale-tools` -0.095 and `habit-offer-code` -0.167 — are each one llm rubric that both arms fail some of the time, with every deterministic grader passing 3/3 in both; they are variance, not regressions, and the per-grader breakdown is how you tell.

0.2.5's green table, all seven skills `ok` on their gated cases: review +0.500, docs +0.370, launch +0.295 (min +0.292), daily +0.294, seo +0.250, measure +0.238 (min +0.143), connect +0.189 (min +0.078). It was composed from two runs rather than one, which is worth saying plainly: the 20-case run above, plus a `--case 'seo-*'` re-run for the case written in answer to it, spliced and re-scored through `delta.py`. Same judge, same `claudeVersion` 2.1.289, same day, and no commit touched `skills/`, `agents/`, `commands/` or the manifest between them, so the twenty older cases were measured against byte-identical content. A single whole-suite run is the cleaner artefact and costs about $35; splicing is honest only while that last condition holds, so check it with `git log -- skills/ agents/ commands/ .claude-plugin/` before relying on one.

**0.2.6 (2026-10-07) was measured PARTIALLY, and here is exactly how much.** Three cases were re-run — `seo-discovered-is-not-a-verdict` **1.000**, `seo-two-numbers-that-lie` **0.926**, `audit-stale-tools` **0.905** — 3/3 at the 0.8 threshold, overall 0.944, judge `sonnet`, `claudeVersion` **2.1.292**, $2.87, 236s. Those are the only three cases whose inputs changed: the release touched `skills/adcopilot-seo/SKILL.md` (body only), `commands/audit.md` and `agents/adcopilot-auditor.md`, and nothing else under `skills/`, `commands/` or `agents/`. The other eighteen cases are **carried over from the 2.1.289 run** against byte-identical text for their skills. **No whole-suite run under 2.1.292 exists.** That is a weaker artefact than 0.2.5's and is recorded as such: the carried-over scores are honest about the TEXT and silent about the BUILD, which is the one comparison this file keeps warning about.

The seo ablation was run fresh on both arms under 2.1.292, because a body-only change cannot move the tools-only arm but a build change can move everything: `seo-discovered-is-not-a-verdict` 1.000 vs 0.750 (**+0.250**), `seo-two-numbers-that-lie` 0.926 vs 0.778 (**+0.148**), so `adcopilot-seo` is `ok` on a mean of +0.199 and a minimum of +0.148. Only seo needed it — `commands/audit.md` is not stripped by `tools-only.sh` (it cuts `skills/*/SKILL.md` only, line 51) so it moves both arms equally, `audit-stale-tools` is tagged `audit` which is not in `TAG_TO_SKILL` and so owns no skill's gate, and `agents/` is outside the suite entirely (see the eval-coverage issue).

**And a reclassification worth more than the scores.** `seo-two-numbers-that-lie` scored **0.852 on the tools-only arm under 2.1.289** — above the line, a regression guard, excluded from the delta, which is what left `adcopilot-seo` with no gated case and threw 0.2.5's first FAIL. On **2.1.292** the same case text with the same judge scores **0.778** on that arm, so it is now a *gated* case and seo has two. Nothing in the case or the skill changed between those numbers. So 0.2.5's "the skill was not the problem, the case was" diagnosis was half the story: the classification is a property of the BUILD as much as of the case, and a skill can pass or fail the gate on a client upgrade alone. Re-read the class column before acting on a FAIL, and never carry a `Class` verdict across builds.

Reading a `--tag`- or `--case`-filtered ablation: every skill with no case in the run prints `FAIL: no gated case` and the script exits non-zero on them. That is the filter, not a regression. Only the rows for skills whose cases actually ran mean anything.

## Releasing

Before a version tag is pushed, in a fresh Claude Code — a profile with no hand-added `adcopilot` server (`CLAUDE_CONFIG_DIR=$(mktemp -d) claude` gives you one):

1. `/plugin marketplace add AtromxIntelligence/adcopilot-claude-plugin`
2. `/plugin install adcopilot@adcopilot-claude-plugin`
3. `/mcp` — choose `adcopilot` and sign in with the Google account that owns the ad account.
4. `/adcopilot:setup` on a real account: it reports what is connected, in prose, and one next step.
5. `/adcopilot:audit` on the same account: the full audit and this month's pacing, with the brand-new-account findings kept separate.
6. The scheduled run, on the same account: say "schedule it" at the end of `/adcopilot:daily`, follow the steps it gives for the surface you are on, and **Run now** once — the run finishes without stopping to ask, calls no tool that changes anything, and the next `/adcopilot:daily` makes no offer once AdCopilot reports the run. If a scheduled run of the plugin's own skill does not finish unattended on a surface, the pasted instructions alone are what the steps give there.
7. `claude plugin validate . --strict` and `claude plugin validate .claude-plugin/plugin.json --strict` both pass; the suite passes at 0.8; the tools-only ablation is green — every skill's delta over the connector plus its own frontmatter description (the tools-only arm keeps the frontmatter so the skill still fires), on its mean and on its weakest case among the cases that baseline does not already carry, is at least 0.05 (`ABLATION_FAIL_BELOW=0.05 evals/ablation/tools-only.sh`). A case the tools-only arm passes at 0.8 is a regression guard on the connector's own behaviour: it must still pass at 0.8 with the skill, and it is left out of the skill's delta. A red ablation blocks the tag: the skill it names is fixed or deleted first.
8. Record the AdCopilot version and `tools_revision` the steps above ran against, in the release notes and in the section above — **and the `claudeVersion` the suite ran under**, which `evals/results/<run>/aggregate-result.json` already stores. A score is only comparable to another score from the same build: on 2026-09-23 under `2.1.280` these cases scored `audit-stale-tools` 1.00, `connect-teaches` 1.00, `measure-teaches` 1.00 and `setup-duplicate-server` 1.00; on 2026-10-02 under `2.1.288`, with the plugin byte-identical (`plugins[0].version` 0.1.0 in both) and the same judge alias, they scored 0.67, 0.83, 0.67 and 0.77. Nothing in the plugin had changed. So a case that drops is a question — plugin, harness, or the `sonnet` alias resolving to a new snapshot — and not yet an answer: diff the two runs' `claudeVersion` before editing a skill, or you will fit the prompts to one build and refit them on the next.

   0.2.5's own run, for the next comparison: under `2.1.289` on 2026-10-06, judge `sonnet`, all 20 cases passed at the 0.8 threshold, overall 0.939, $18.18, 1,191s. The three cases new at that point scored 1.00 on every run; the fourth, `seo-discovered-is-not-a-verdict`, was written after the ablation and is recorded with it. The four lowest were `audit-stale-tools` 0.81, `habit-offer-code` 0.83, `connect-unknown-product` 0.84 and `connect-teaches` 0.87 — the same cases that moved between `2.1.280` and `2.1.288`, and `audit-stale-tools` is still the weakest of them on a build three releases later.

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
every skill and command carries a `name:` and a `description:`, that the
structural tests in `tests/` pass (the daily-habit block identical in every
flow that carries it, the unattended run's instructions read-only and its
first call marked `claude-scheduled`, the instructions it hands over equal to
AdCopilot's recipe, and the eval graders able to see the offer they grade),
that no download-and-execute pattern is back anywhere in the repository, and
that the manifest version is not behind the latest tag.

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

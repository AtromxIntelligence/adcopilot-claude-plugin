# AdCopilot for Claude Code

The AI agent that runs your Google Ads, with Google Analytics, Google Search Console and Google Tag Manager in the same chat. Audit wasted spend, mine search terms, build campaigns and fix conversion tracking from Claude Code. AdCopilot proposes each change first. For a hard stop, set your AI client to ask before AdCopilot's write tools: Needs approval in Claude; in Cursor, use the Allowlist run mode and keep them off the allowlist (Cursor's cloud agents never ask). AdCopilot never deletes a campaign, ad group, ad, keyword or asset. It can remove negative keywords and location targets, each proposed first. This plugin bundles the hosted AdCopilot connector and carries the steps the connector cannot take for you: what to click in Google's own screens, and the traps that are easy to fall into.

AdCopilot is made by Atromx Intelligence (https://adcopilot.cloud) and is not related to other products named AdCopilot.

The plugin is free (MIT). The connector is a hosted service; its plans are on https://adcopilot.cloud.

## Install

Two steps on every surface: add the plugin, then **sign in to the connector it
brings with it**. The second step is the one people miss, and nothing works
until it is done.

AdCopilot connects to Google Ads through its own Google Cloud project, with your Google sign-in. If you want programmatic access to Google Ads for your own software, get your own Google Cloud account and apply for Google Ads API access there.

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

The last step opens the connector list. Choose `adcopilot` and sign in with your own Google account. There is no add step: the plugin registers the connector at `https://mcp.adcopilot.cloud/mcp` for you. Signing in links your AdCopilot workspace, so you need an AdCopilot account; your Google products are connected once, in AdCopilot at https://app.adcopilot.cloud, not in Claude Code — `/adcopilot:setup` tells you which are missing and sends you to the right page.

### Cursor

Cursor takes AdCopilot's connector on its own; this plugin does not install
there as a whole. Its skills are written for Claude, and Cursor reads them too
when they are copied into Cursor's or Claude Code's skills folder. Wherever they
work out which client they are in (`/adcopilot:setup`, `adcopilot-connect`, the
daily-habit offer), they check for Cursor first: there they never run Claude
Code's command-line tool, look for the connector in Cursor's MCP settings and
make no schedule offer of their own; where AdCopilot's answer suggests a
check-in, they say that AdCopilot's emailed daily check-in is the morning check
there, switched on or off in AdCopilot's dashboard.

1. Add the connector from AdCopilot's own
   [Cursor page](https://adcopilot.cloud/docs/connect/cursor): its **Add to
   Cursor** button opens Cursor with the connector named `adcopilot`. Or add it
   by hand in Cursor's MCP settings, with these lines:

   ```json
   {
     "mcpServers": {
       "adcopilot": {
         "url": "https://mcp.adcopilot.cloud/mcp"
       }
     }
   }
   ```

2. Sign in: Cursor opens AdCopilot's page, **Let Cursor use your AdCopilot?**,
   in your browser. Press **Approve**; there is no API key to paste. If
   **Approve** did nothing on an earlier try, remove AdCopilot in Cursor's MCP
   settings, add it again and press **Approve** once; see
   [Approve does nothing](https://adcopilot.cloud/docs/troubleshooting/connection-errors#approve-does-nothing).
3. Ask: "Get me started with AdCopilot".

**Added from cursor.directory?** Its **Add to Cursor** button can name the
connector `server` instead of `adcopilot`, so Cursor's MCP list and its
approval questions show `server`. It is the same connector. The button on
AdCopilot's page names it `adcopilot`.

**Approvals in Cursor.** Cursor has no **Needs approval** setting; its run modes
decide, in Settings, then Agents, then Approvals & Execution (at the time of
writing). In **Allowlist**, a tool on the allowlist runs without asking and any
other asks first, so keep AdCopilot's write tools off the allowlist. In
**Auto-review**, Cursor's recommended default, allowlisted calls also run at
once, and every other MCP call goes to a classifier that can let a change
through without asking. Its third run mode asks before nothing, and a Cursor
cloud agent never asks you to approve an action. Whatever the mode, AdCopilot
proposes each change first, never deletes a campaign, ad group, ad, keyword or
asset (it can remove negative keywords and location targets), and builds every
campaign paused.

### Then, on every surface

Signing in to the connector links your **AdCopilot workspace**, so you need an
AdCopilot account. Your Google products — Google Ads, Analytics, Search Console,
Tag Manager — are connected **once, inside AdCopilot at
https://app.adcopilot.cloud**, not in Claude. So a fresh sign-in can report
nothing connected: that is the server answering correctly, not a fault.

Run `/adcopilot:setup` first. It says what is connected, what is not, and sends
you to the right page for each.

If you had already added the connector by hand before installing (Claude Code only), Claude Code keeps yours and silently ignores the plugin's. `/adcopilot:setup` spots this from the names of the tools Claude has. AdCopilot's page [Already added the connector by hand?](https://adcopilot.cloud/docs/connect/claude-code-plugin#already-added-the-connector-by-hand) gives the steps to remove your copy from every place you added it; after that, `/mcp`, choose `adcopilot` and sign in.

## What you get

Seven commands, which you type:

- `/adcopilot:setup` — checks the connector is connected and signed in, says what each connected product unlocks, and catches the two ways a fresh install goes wrong: a lapsed sign-in, and, in Claude Code, a copy of the connector you added by hand before installing.
- `/adcopilot:launch` — a first Search campaign, through the `adcopilot-launch` skill below.
- `/adcopilot:measure` — conversion tracking, through the `adcopilot-measure` skill below.
- `/adcopilot:daily` — the daily check-in: this month's budget pacing, the last seven days' searches that cost money and brought nothing, any ad Google has disapproved or limited, and what changed in the account since yesterday and who changed it, in that order.
- `/adcopilot:weekly` — last Monday to Sunday against the week before: spend, conversions and cost per conversion, the three biggest changes, and three things to do this week, written to be forwarded.
- `/adcopilot:negatives` — the last seven days' searches that cost money and brought nothing, grouped by theme, with the never-show-for words (negative keywords) that would block them, proposed first (the command asks which themes to block) and read back once added.
- `/adcopilot:audit` — the connector's full audit and this month's budget pacing, with the findings that are only a symptom of a brand-new account kept separate, and the first fix proposed with what it costs to act and to leave it, read back once made, then the next one proposed.

Nine skills, which Claude draws on when the conversation calls for them:

- **adcopilot-connect** — sets up AdCopilot, connects your Google products and links them to each other in the order that works, saying what each step bought you as it happens.
- **adcopilot-measure** — sets up conversion tracking end to end: the Analytics property and data stream, the Tag Manager tags, the key event, the Analytics-to-Ads link and the import, and ends with exactly one Primary conversion, proven by a real click.
- **adcopilot-launch** — builds a first Search campaign switched off, on the budget and bid you name: locations, never-show-for words, ad groups, keywords with their match types, ads and assets; verifies the settings that leak money by reading the campaign back; hands you the go-live switch, and asks you to say when it is on so it can read the first day's delivery; and runs the first week's checks, reading why a switched-on campaign is not delivering before it sends you to any screen.
- **adcopilot-daily** — the morning check a Claude scheduled task or a Claude Code routine runs while nobody is there: it is written to read only and never ask a question, opens with "All clear" or "Needs a look" and ends with the one fix worth doing, as a yes/no question for when you open it. When you answer yes, it re-reads what the fix touches and states the change again before making it, because the report is hours old by then. It also holds the steps for setting that schedule up.
- **adcopilot-review** — the everyday one: reads the account and says what happened, what it cost, what is wasting money and what to change, then proposes the change and applies it when you say yes, reads back what the change's own result does not show, and proposes the next fix the same way. It opens with `full_audit`, because one lens is one read and answers what a dozen hand-written queries would, and it treats the number of reads AdCopilot sizes for one answer as something to spend rather than stay under, never as a daily limit.
- **adcopilot-fix-checks** — the fixes for the checks an AdCopilot audit flagged, when you send the question from the audit page's or an email's "Fix all three" or "Fix this" button. It takes the checks foundation first (counting results before anything judged by them), reads only what each fix needs rather than running the audit again, and puts each fix to you as one yes/no, with at most five rows of any list. A search-term check goes to the never-show-for words, zero-conversion keywords to a pause, and a conversion-tracking check to the steps AdCopilot can take or the clicks in Google Ads it cannot. Each change is read back, with how to undo it, before the next check.
- **adcopilot-docs** — answers questions about AdCopilot itself from your live workspace rather than from memory: which products it reaches, how many look-ups are left today and what happens when they run out, which plan you are on, what it is allowed to change, where data goes, and what to do when a call fails. Plans and prices are linked, never quoted. It answers from that one look at your workspace, without reading your accounts or starting another skill, and says what AdCopilot can do as one list. When the question pointed at something a read of your account would answer, it ends on one question offering that read; after a question about look-ups, billing, privacy or safety it offers nothing.
- **adcopilot-seo** — answers what Google search makes of your site, through Search Console: which pages earn clicks and which earn nothing, what people typed to find you, whether a sitemap is being read, and when a page was last crawled. It is written around the readings that mislead — the sitemap's dead "indexed" column, an average position that is not a rank, impressions that are not demand — and it says plainly what it cannot see: there is no site-wide coverage list and no penalty read, so it asks you for Search Console's Pages export rather than guessing. Once an edit is live it offers to inspect the page again a few days later, and with Google Ads connected it offers to set the searches you pay for beside the ones that already bring you organic clicks.
- **adcopilot-meta** — for a question about Meta ads (Facebook ads, Instagram ads) or about Meta and Google together. AdCopilot has no Meta integration (one is on the roadmap, with no date), and Meta publishes a connector of its own for Meta ads, so this skill looks for Meta's connector in the conversation first. When it is not there, it says what it is and how to add it, links [AdCopilot's guide](https://adcopilot.cloud/docs/guides/meta-ads-alongside-adcopilot), which links Meta's own pages, and states nothing about Meta's terms that Meta has not published. When it is there, Meta's figures come from Meta's connector and Google's from AdCopilot, each labelled with where it came from; nothing read from one is sent to the other; and any change through either connector is proposed first, one platform at a time (for a hard stop, set both connectors' write tools to ask, as at the top of this page). AdCopilot never writes to Meta.

One agent, which Claude hands a job to when it is too big for the conversation:

- **adcopilot-auditor** — a full account audit end to end, returning findings with the numbers behind them and the changes worth making. It reads and proposes only: it holds no write tool, so it cannot apply anything, and the conversation that asked for it takes your yes.

Together with the connector registration above, the commands, skills and agent above are what the plugin ships at this version.

### Every morning, without asking

Every command above, and the connect, launch, measure and fix-checks skills,
make one short offer to turn a morning check of the account into a daily habit
when AdCopilot's own answer hands them the recipe for your AI client
(`routine.schedule`): an account with a campaign switched on, no schedule
reported yet, and a client AdCopilot gives scheduling steps for, which today
means Claude. AdCopilot gives none for Cursor, ChatGPT or another client, and
there the plugin makes no schedule offer of its own; in Cursor, when AdCopilot's
answer suggests a check-in or a summary, the plugin says that AdCopilot's
emailed daily check-in is the morning check there, switched on or off in
AdCopilot's dashboard. The offer comes, as a paragraph of its own, only in a
reply that asks you no yes/no on a fix: the reply that reads back the first fix
you approved, where it stands in for the next fix's yes/no (the next fix is
named, and proposed in the reply after), or at the close of a reply that
proposes none. When that fix was for a finding the morning check also reads (the
searches that spent with no sale, a campaign out of budget, a disapproved ad, a
drop against the 7-day average, a change nobody asked for), it is tied to it: a
check that runs by itself every weekday at 8:07 would have caught it on its
first morning. If you decline that first fix or put it off, the offer closes
that reply instead, tied to the finding the same way. With any other finding, or
none, the offer closes the reply instead, without that claim. In claude.ai,
Cowork or the desktop app it is a Claude **scheduled task**; in Claude Code, a
**routine** made with `/schedule`, which it offers to create for you. Say
"schedule it" and it walks you through the steps; say no and it does not offer
again in that conversation, asks once whether your Claude has scheduled tasks,
and records the answer, so a no pauses the offer for a week and a Claude with no
scheduled tasks ends it. It records that answer only from Claude, because
AdCopilot keeps it for the whole workspace. The offer stops for good once
AdCopilot reports a schedule — one you recorded with it, or a scheduled run that
has checked in on two different days.

The instructions you save are AdCopilot's own morning-check recipe, word for word, filled in with your account. A run reads about six or seven times, and each read counts toward your workspace's daily operations. On Free, and on a trial held to Free's 10 a day, an analysis such as budget pacing counts 2 operations and a single read 1, so a run comes to about 8 to 10 operations. On a paid plan or a running trial every read counts 1. If AdCopilot already emails you its daily check-in, that keeps coming as well; the Routine card on AdCopilot's Home page pauses it if you want only one. Scheduled tasks need a Claude plan that has them; on Claude's Free plan, and in Cursor, AdCopilot's emailed daily check-in, when it is on, is the morning check.

**A scheduled run is told not to change anything.** The instructions
`adcopilot-daily` gives you are read-only and ask no questions; a fix it finds
is a question for when you open the report. AdCopilot holds a scheduled run to
reads as well: once a run's first call is `get_org_context` with
`source: "claude-scheduled"`, AdCopilot refuses every tool that changes Google
Ads, Analytics, Tag Manager or Search Console on that connection for the rest of
the run, up to 20 minutes, whatever Claude allows (AdCopilot's own notes aside).
It knows a run is scheduled only from that first call, so a run that skips it or
sends another source is not held, and a yes typed in the run's own conversation
can be refused while the run is on; say it again in a new conversation. Claude
Code adds one more hold: AdCopilot marks `set_campaign_status`, the tool that
pauses a campaign or switches one on, as needing a person, so Claude Code
(version 2.1.214 or later) will not use it in a run with nobody there to answer.
The plugin's skills pause or switch on a campaign only with that tool, never
with a status in a change to the campaign's settings (`update_campaign`), and
the mark does not hold that change. A Claude Code routine runs its tools
without asking, and so does a scheduled task whose approval setting no longer
asks; in those, the first call and the instructions are what keep the run to
reads, so keep them as written. In claude.ai, Cowork and the desktop app,
setting AdCopilot's other **Write/delete tools** to **Blocked**, every one but
the two AdCopilot tools below, stops a change outright, in every chat as well
as in the run.

**The one setting a scheduled task needs in Claude.** In claude.ai, Cowork and the desktop app, a run with nobody there stops at the first tool Claude asks about. So the set-up's first step is in AdCopilot's **Tool permissions** (Customize, then Connectors, then AdCopilot): the **Read-only tools** on **Always allow**, and under **Write/delete tools** two of AdCopilot's own, “AdCopilot: workspace context (records visit)” and “AdCopilot: save business notes and progress”, on **Always allow** too.
They keep AdCopilot's own notes and never change Google Ads; every other Write/delete tool stays on **Needs approval**: AdCopilot proposes each change first, and that setting makes Claude ask before it runs (Cursor has no such screen; see **Approvals in Cursor** above). Claude lists the first of the two under Write/delete tools, and it is every run's first call, so a task set up with only the read-only tools on **Always allow** stops there; setting those two tools to **Always allow** too is the whole fix.

## What it will not do

- **Switch on a campaign it built.** Every campaign it builds is created paused. You switch it on in Google Ads yourself.
- **Delete a campaign, ad group, ad, keyword or asset.** The connector refuses a REMOVED status server-side: the campaign, ad group, ad and keyword tools accept only ENABLED or PAUSED, and the asset tools refuse a remove outright. Pausing is as far as it goes for all of those, and it is the server that enforces that rather than the assistant's good manners. What it can remove, each proposed first like any change: a negative keyword, since each of the three ways to add one has a removal behind it, so a negative can be taken back out — which is what makes "you can undo this" true when AdCopilot says it; and a location target on a campaign. Setting a campaign's languages replaces the list it had. Attaching a shared negative-keyword list is the one-way action; there is no detach tool, and a list is detached in Google Ads under Tools, Shared library, Exclusion lists.
- **Change your account unasked, while your AI client asks before AdCopilot's
  write tools.** Reads run freely, and AdCopilot proposes each change first. For
  a hard stop, set your AI client to ask before AdCopilot's write tools: **Needs
  approval** in claude.ai, Cowork and the desktop app; in Claude Code, leave
  them off the allowlist, in a session whose permission mode still asks before
  each tool; in Cursor, use the **Allowlist** run mode and keep them off the
  allowlist (see **Approvals in Cursor** above; Cursor's cloud agents never
  ask). Take the question away and changes to what already exists, a budget or a
  switched-on campaign among them, apply without it; only a new campaign is
  still built paused. The one exception is `set_campaign_status`, the tool that
  pauses a campaign or switches one on: Claude Code (version 2.1.214 or later)
  asks before every use of it, whatever its settings, and a run with nobody
  there to answer cannot use it; the Claude desktop app may also ask every time
  for it. The plugin's skills pause or switch on a campaign only with that tool,
  never with a status in a change to the campaign's settings
  (`update_campaign`), which follows your settings like any other change.

## Privacy and terms

The plugin registers AdCopilot's hosted connector, so AdCopilot's own policies
cover what happens when you use it:

- Privacy policy: https://adcopilot.cloud/privacy
- Terms of service: https://adcopilot.cloud/terms
- Documentation: https://adcopilot.cloud/docs

## Support

- Something wrong with the plugin (a command, a skill, this README): [open an issue here](https://github.com/AtromxIntelligence/adcopilot-claude-plugin/issues).
- Something wrong with the connector (sign-in, a tool call, your account): support@adcopilot.cloud.
- A security problem in the plugin or the connector: report it to support@adcopilot.cloud.
- Anything else: https://adcopilot.cloud/contact.

## Licence

MIT. Copyright Atromx Intelligence Private Limited. See [LICENSE](LICENSE).

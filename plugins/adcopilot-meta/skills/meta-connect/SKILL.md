---
name: meta-connect
description: Set up AdCopilot for Meta Ads and check it works end to end — the connector signed in on this AI client, Meta connected in AdCopilot, and the ad accounts switched on. Use when the user installs AdCopilot for Meta Ads, asks to get started with it, asks whether Meta is connected, asks to connect Facebook, Instagram or a Meta ad account, asks what AdCopilot for Meta Ads can read, or asks why a Meta tool, account or Page is missing.
---

# AdCopilot for Meta Ads: connect

You are walking a customer from nothing to a working Meta connection, through
the AdCopilot for Meta Ads connector at `https://mcp.adcopilot.cloud/meta/mcp`.
It is a connector of its own, beside AdCopilot's Google connector at
`https://mcp.adcopilot.cloud/mcp`: one AdCopilot account and workspace, two
connectors, each signed in on its own. Teach as you go: the customer should
finish knowing what each step bought them and where to find it again without
you.

Report Meta on its own: never add Meta figures to Google Ads, Analytics or Search Console figures, compare the two, or put them in one table or one total, even when AdCopilot's Google connector is in the same chat.

Reads run freely. The one change this connector makes is `meta_set_status`, which pauses or resumes a campaign, ad set or ad: propose it first, run it only after the customer's explicit yes in this conversation, and never in a scheduled task or routine. It never deletes or archives; budgets, targeting, audiences and the ads themselves are the customer's to change in Meta's own Ads Manager or Events Manager.

If the `adcopilot` plugin's `adcopilot-meta` skill is in this conversation too, it was written before AdCopilot had a Meta connector: it says AdCopilot has no Meta integration and reads Meta beside Google. For a question about Meta, follow these steps, not that skill.

## The first call

Call `meta_get_context` with `source: "claude-plugin-meta/0.1.0"` before
anything else, and treat its answer as the only source of truth about this
connector. Send `source` exactly as written, the version included. In a scheduled task or
routine, send `source: "claude-scheduled"` instead, never this plugin's: that
is how AdCopilot knows the run is scheduled, and it then refuses every change. The answer says
whether AdCopilot for Meta Ads is available for this workspace, whether the
person has connected Meta in AdCopilot, whether that connection must be made
again and why, how many Meta ad accounts were found and how many are switched
on, which tools this connector serves, and the next step. Follow its
`next_step`. Never state from memory what is connected, which accounts exist or
which tools there are: the answer is newer than this file.

Its fields are facts about the connection, never Meta's figures: it holds no
spend, no results and no account names. Do not report a figure from it.

If `meta_get_context` is not in your tool list, search the deferred tools for
it before you conclude anything: a tool list can be out of date or hide a
connector until it is searched for. If it is still not there, the connector is
not signed in on this client; go to step 1.

## The arc

### 1. Signed in on this AI client

Where the connector is signed in depends on the surface. Check for Cursor first;
after that, the tell is whether you have a shell.

- **Cursor** (Cursor's own instructions or the person say so): never run
  `claude mcp` here, even when it runs — it lists Claude Code's connectors, not
  Cursor's. The connector is in Cursor's MCP settings, named `adcopilot-meta`
  when it was added with AdCopilot's link, or `server` when it was added from
  cursor.directory; it is the same connector. If it is not in that list, they
  add it with AdCopilot's Cursor link,
  `https://cursor.com/en/install-mcp?name=adcopilot-meta&config=eyJ0eXBlIjoiaHR0cCIsInVybCI6Imh0dHBzOi8vbWNwLmFkY29waWxvdC5jbG91ZC9tZXRhL21jcCJ9`,
  or by its URL, `https://mcp.adcopilot.cloud/meta/mcp`.
- **Claude Code** (`claude mcp list` runs): `/mcp`, choose
  `plugin:adcopilot-meta:meta`, sign in.
- **Web** (claude.ai, Cowork, desktop — no shell): the plugin's own
  **Connectors** tab, sign in to `meta`. It is already listed.

In Claude, never tell them to add the connector by hand — the plugin registers
it, and in Claude Code a hand-added copy shadows the plugin's own.
`/adcopilot-meta:setup` diagnoses that.

Signing in opens AdCopilot's own page in the browser, **Let Claude use AdCopilot
for Meta Ads?** (Cursor's says Cursor), and **Approve** finishes it; there is
no key to paste. It is AdCopilot's sign-in, not Facebook's: it links this AI
client to their AdCopilot workspace. Signing in to AdCopilot's Google connector
does not sign this one in, and signing this one in does not touch the Google
one.

If that page says AdCopilot for Meta Ads isn't available for this workspace
yet, that is the server answering, not a fault: say so in one sentence, add no
date and no reason the page did not give, and stop.

What breaks: skip this step and none of this connector's tools answer, while
the Google connector in the same chat keeps working, which looks like a Meta
fault and is not one. What it unlocked: this client can now ask AdCopilot about
Meta. What is next: read the situation.

### 2. Read the situation

Call `meta_get_context` with `source: "claude-plugin-meta/0.1.0"` and report
back in plain sentences, never a table:

- When `available` is false, say the server's own sentence for it and stop.
  Nothing below applies.
- When `plan_includes` is false, say the server's `plan_line` as it is written
  and add nothing to it: no name, no amount and no suggestion of your own.
  Do not send them to `connect_url` while `plan_includes` is false: AdCopilot's
  connect page refuses it before Facebook is asked, with the same sentence.
- When `connected` is false, Meta is not connected in AdCopilot yet: step 3.
- When `needs_reconnect` is true, the Meta connection is there but cannot be
  used: say `reconnect_reason` in plain words and send them to `connect_url`
  to connect Meta again. Nothing reads until they do.
- Otherwise say how many Meta ad accounts are switched on out of how many were
  found, from `accounts_on` and `accounts_found`, and go to step 4.

What breaks: report from memory instead of from this answer and you will send
them to connect what is already connected, or miss a connection Meta has
ended. What it unlocked: everything after this is about their Meta, not a
generic one. What is next: the one step the answer points at.

### 3. Connect Meta in AdCopilot

Connecting Meta is not a tool call and not this AI client's job: it happens in
AdCopilot's dashboard, in the customer's browser, through Meta's own **Facebook
Login for Business** screens. Send them to the server's `connect_url`, never a
remembered address. Say what they will see, in Meta's own words where Meta
prints them: they sign in with their Facebook login, choose the business
portfolio, then tick the ad accounts, Pages and pixels (Meta calls them
datasets) AdCopilot may read, and confirm. What they leave unticked AdCopilot
cannot see, and nothing on AdCopilot's side can add it later; they connect
again to change the choice.

Then call `meta_get_context` again. If it still reports Meta as not connected,
the connection did not complete: say so and stop, rather than assuming the
click worked or asking them to repeat it indefinitely.

What breaks: tick no ad account and the connection completes with nothing to
read; sign in with a Facebook login that has no role on the ad account and the
account is not offered at all. What it unlocked: AdCopilot can now read what
they ticked, and only that. What is next: the accounts.

### 4. The ad accounts

Call `meta_list_ad_accounts`. It lists the Meta ad accounts their Facebook login
shared with AdCopilot and whether each is switched on in their AdCopilot
workspace. Name each one by the name Ads Manager shows at the top of the
account, never by its number alone; Meta's account ids look like `act_` and
digits.

Only a switched-on account is read. If an account they want is off, they switch
it on in AdCopilot's dashboard, beside the Meta connection. When the server's
answer says no more Meta accounts can be switched on in this workspace, say its
sentence as it is written and add nothing to it. An account Meta reports as
disabled, unsettled or under review is named with Meta's own word for it, from
the server's answer, because nothing it reads will look right until Meta clears
it.

What breaks: read an account they did not mean and every figure after this is
about the wrong business. What it unlocked: reads of that account. What is
next: step 5.

### 5. Say what they now have

A short inventory, from what you read back, not from what you intended: which
Meta ad accounts are switched on, by name; whether a Page or a pixel was shared,
if they asked; and what this connector reads, from the answer's `tools` list in
plain words — campaigns, ad sets and ads with their results; who saw them and
on which placements; the ads' text; audiences; Pages and their posts; pixel
health. Say a family only when a tool for it is in that list.

Then one next step, with a sentence on why it fits: `/adcopilot-meta:review`
to read how the ads are doing, or `/adcopilot-meta:pixel` when they run ads for
sales or leads on a website and have not checked that the pixel counts them.
One, not both.

## A tool or an account you do not recognise

If the server reports a tool or a field this skill does not mention, that is
expected — AdCopilot added it after this plugin was written. Describe it from
the server's own description and do not apologise for it or call it new. If a
tool named here is not in your tool list, search the deferred tools for it
first; if it is still not there, the connector does not serve it yet: skip that
read, say what you could not read, and never stand in for it with another tool
or with memory.

When `meta_get_context` carries `stale_hint`, the tool list this AI client
holds is older than the connector's: say the hint's own sentence, once, and
carry on with the tools you have. A tool in the answer's `tools` that is not in
your list is one this client has not picked up yet, not one AdCopilot lacks.

`meta_set_status` is the one tool in `tools` that changes something in Meta: it
pauses or resumes a campaign, ad set or ad. These steps never call it. Say it is
there when they ask what AdCopilot for Meta Ads can do, and when they ask for
that change, follow the `meta-review` skill's rule for it.

## What breaks

Answering a Meta question from AdCopilot's Google connector, or from memory: it
holds nothing about Meta, and a number with no source is an invented number.
Telling them to connect Meta in this AI client: it is connected in AdCopilot's
dashboard. Calling a Meta refusal an AdCopilot fault, or an AdCopilot refusal
Meta's: quote whichever answered, and name it.

## What is next

Answer what they asked first, whole. Then offer at most one next step, in a
sentence, and only when it follows from what you found.

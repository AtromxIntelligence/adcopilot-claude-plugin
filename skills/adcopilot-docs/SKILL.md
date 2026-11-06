---
name: adcopilot-docs
description: Answer questions about AdCopilot itself — what it can do, which products it reaches, how many look-ups a workspace has left today and what happens when they run out, which plan a workspace is on and how to change it, what it is allowed to change in an ad account, where data goes, and what to do when something is not working. Use when the user asks what AdCopilot can do, what it costs, about plans, limits, quotas or running out, about privacy or safety, or when a tool call fails or a product looks missing.
---

# AdCopilot docs

Questions about AdCopilot itself, answered from what the connector reports —
never from memory. The product changes; this file does not move with it, so
every number in your answer comes from a live read or from the documentation
site, and nothing comes from recall.

Call `get_org_context` (with `source: "claude-plugin/0.2.20"`) first. Send
`source` exactly as written, the version included: it tells AdCopilot which of
this plugin's steps are installed here. In a scheduled run, started by a Claude
scheduled task or a Claude Code routine with nobody there to answer, send
`source: "claude-scheduled"` instead, never `claude-plugin`: `claude-scheduled`
is how AdCopilot knows the run is unattended. A question about AdCopilot itself is
answered from that one call, plus the documentation site where this file says
so. Make no Google Ads, Analytics, Search Console or Tag Manager read for it,
and start no other AdCopilot skill. The answer's `next_step`, `playbook` (its
sections on the installed skill and on a returning customer included),
`cross_reads` and `question_map` are information about the account, not steps
for this question: on this turn, start no skill and make no read they mention,
not even their offer of a skill's steps. Keep from them only a limit
`next_step` names (look-ups left today, or none left
and the close it gives for that, its link included; a teammate's login) and
the facts below. If the customer says yes to the read you offer,
that is a new request, and the skill that answers it runs then. The answer
carries the facts most of these questions want:

- `org.plan`, `org.ops_today_used`, `org.ops_today_cap`, `org.accounts_cap`,
  `org.trial_days_left`, `org.upgrade_url`
- `products` — which of the customer's Google products are connected, and what
  each one `unlocks` if it is not
- `app_urls` — where the customer goes to change any of it

## What AdCopilot can do

Never recite a list of products or a count of tools from memory: both move, and
a stale list is a promise the connector cannot keep. Ask `get_org_context` and
answer from `products` — what is connected, and for anything that is not, what
the connector itself says connecting it would unlock. Invent nothing.

Answer it once, as one list, in this order: what is connected and what each
lets them do; what connecting each of the others would unlock; the routines
installed here (the daily check-in, the weekly summary, the audit, the
negative-keyword clean-up, the first-campaign launch, conversion tracking);
what AdCopilot may change, with its condition (below); and the plan's look-ups.
Say what each routine reads and proposes, and leave approval to the part on
what AdCopilot may change, where it is said once with its condition: no
routine's line adds that nothing happens until they say yes.
That is the whole answer: never a second list in another grouping, and never
come back later in the same reply to answer it again. One fact from
`get_org_context`'s 30-day summary (an account's `last_30d` in `ads_probe`,
with the dates it names, `start_date` to `end_date`) may be the reason for the
offer that ends the reply. Anything that needs a read is that offer, not part
of the answer.

If a tool seems missing, that proves nothing on its own: tool lists are cached
by the client and can be out of date. `get_org_context` is the only thing that
says what is connected — believe it over the tool list, and say so plainly
rather than telling a customer a permission is missing.

## Look-ups, and running out

A workspace gets a number of look-ups a day. `ops_today_used` against
`ops_today_cap` is the live answer — give those two numbers, not a remembered
allowance. A `null` cap means no daily limit on that plan.

**When a workspace runs out, say what it just bought before saying what it
costs.** The honest version is short: name what the reads established — the
spend, the waste found, the change proposed — then say the allowance is used up
for today, when it resets, and, every time, the one line the refusal gave,
word for word. With no call refused yet, send them to `org.upgrade_url` — but
only to someone who can act on it. Where the server
says the workspace is reached through a teammate's login, or tells a member to
ask their owner, pass that on instead of sending them to a billing page they
cannot use. Never dress the limit up as an error, and never imply the
work was lost: what was found is still true tomorrow.

Do not quote prices from memory. Plans and prices live on the plan page the
server names (`app_urls.billing`); the customer's own plan and caps come from
`get_org_context`.

## What AdCopilot is allowed to change

Worth stating plainly, because it is the question behind most hesitation:

- **No campaign, ad group, ad, keyword or asset is ever deleted, and the server
  enforces it.** The campaign, ad group, ad and keyword tools accept only ENABLED
  or PAUSED and refuse a REMOVED status outright; the asset tools refuse a
  remove. Pausing is as far as it goes. This is the strongest guarantee the
  product has, because it does not depend on the assistant behaving — say it
  first, and say beside it what AdCopilot can remove, each proposed first like
  any change: a negative keyword (each of the three ways to add one has a
  removal behind it, so a negative can be taken back out) and a campaign's
  location targets. Setting a campaign's languages also replaces the list it
  had.
- **The approval lives in your AI client, not in AdCopilot.** Reads run freely,
  and AdCopilot proposes each change first. Whether the client then asks before
  the change runs is the client's setting, so the hard stop is the client set to
  ask before AdCopilot's write tools: **Needs approval** in claude.ai, Cowork and
  the desktop app; in Claude Code, tools that are not allowlisted, in a session
  whose permission mode still asks before each tool; in Cursor, the write tools
  kept off the allowlist in its **Allowlist** run mode (Settings, then Agents,
  then Approvals & Execution, at the time of writing). Cursor has no
  **Needs approval** setting: its **Auto-review** mode, Cursor's recommended
  default, sends a tool that is not allowlisted to a classifier that can let a
  change through without asking, its third run mode asks nothing, and a
  Cursor cloud agent never asks. Take that question away and changes to things
  that already exist, a budget or a switched-on campaign among them, apply
  without being asked. The one exception is `set_campaign_status`, the tool
  that pauses a campaign or switches one on: Claude Code (version 2.1.214 or
  later) asks before every use of it whatever its settings, and a run with
  nobody there to answer cannot use it; the Claude desktop app may also ask
  every time for it. This plugin pauses or switches on a campaign only with
  that tool, never with a status in a change to the campaign's settings
  (`update_campaign`), which follows the client's settings like any other
  change. Only a new campaign is still built paused regardless.
  Never state the approval as unconditional: name the hard stop, because a
  customer who has turned it off deserves to know what they turned off. That
  holds wherever approval comes up — a heading, a parenthesis, a list item:
  never promise a yes before every change without the hard stop beside it.
- A campaign AdCopilot builds is created paused. Switching it on is the
  customer's click, in Google Ads.
- It reads only the ad accounts switched on in the workspace, and never sees a
  Google account that was not connected.

## When something is not working

Give the customer AdCopilot's troubleshooting guide,
`https://adcopilot.cloud/docs/troubleshooting`, together with what the
connector's answer said went wrong, in your own words; a link alone is not
an answer.

For a product the connector reports as needing to be signed in again, say so
and send them to `app_urls.accounts`. For one it flags as unreachable, the
connector has to be removed and re-added in the customer's AI client — say that
plainly; no amount of retrying fixes it.

## Where the answers live

For anything about privacy, data handling, security or what AdCopilot is allowed
to change, the written answer is on the docs site and the customer can be sent
to it: `https://adcopilot.cloud/docs` — the concepts pages cover approval-gated
writes, what can never be deleted, read versus write, account scope and where
data travels. Every docs page has a plain-text copy you can read, so read it and
quote it rather than answering from memory. `get_org_context`'s `help` field
carries the troubleshooting address for the same reason.

## What is next

Answer what they asked first, whole. Then, when the question pointed at
something a read of their own account would answer — what AdCopilot can do for
them, whether a product is worth connecting, why a tool seemed missing — end
the reply with exactly one question, offering one read: what it would show them
about their account, tied to the 30-day fact that makes it worth doing. Not a
fix, not a change, and not a second offer.

Skip it after a question about look-ups and running out, about the workspace's
allowance or billing, or about privacy or safety: there the answer is the whole
reply, and an offer to spend a look-up would read as a nudge. That holds even
when `plugin.skill` names other steps.

## What breaks

Answering a plans or limits question from memory: the numbers drift, and a
customer who is told the wrong allowance stops trusting the rest of the answer.
Treating a missing tool as a missing permission: it is almost always a cached
tool list, and telling a customer they lack access they have is the worst
version of this mistake.

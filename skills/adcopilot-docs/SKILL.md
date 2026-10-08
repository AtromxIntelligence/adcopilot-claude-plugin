---
name: adcopilot-docs
description: Answer questions about AdCopilot itself — what it can do, which products it reaches, how many look-ups a workspace has left today and what happens when they run out, which plan a workspace is on and how to change it, what it is allowed to change in an ad account, where data goes, and what to do when something is not working. Use when the user asks what AdCopilot can do, what it costs, about plans, limits, quotas or running out, about privacy or safety, or when a tool call fails or a product looks missing.
---

# AdCopilot docs

Questions about AdCopilot itself, answered from what the connector reports —
never from memory. The product changes; this file does not move with it, so
every number in your answer comes from a live read or from the documentation
site, and nothing comes from recall.

Call `get_org_context` (with `source: "claude-plugin/0.2.6"`) first. Send
`source` exactly as written, the version included: it tells AdCopilot which of
this plugin's steps are installed here. When the answer's `plugin.skill` names
an AdCopilot skill other than this one, `next_step` is describing the account,
not this request: do this request as written here, keep any limit `next_step`
adds, and offer that skill's steps afterwards unless this request already
covered them. The answer carries the facts most of these questions want:

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
for today, when it resets, and that a paid plan raises it. Send them to
`org.upgrade_url` — but only to someone who can act on it. Where the server
says the workspace is reached through a teammate's login, or tells a member to
ask their owner, pass that on instead of sending them to a billing page they
cannot use. Never dress the limit up as an error, and never imply the
work was lost: what was found is still true tomorrow.

Do not quote prices from memory. Plans and prices live at
`https://adcopilot.cloud/pricing`; the customer's own plan and caps come from
`get_org_context`.

## What AdCopilot is allowed to change

Worth stating plainly, because it is the question behind most hesitation:

- **Nothing is deleted except a negative keyword, and the server enforces it.**
  The campaign, ad group, ad and keyword tools accept only ENABLED or PAUSED and
  refuse a REMOVED status outright; the asset tools refuse a remove. Pausing is
  as far as it goes. This is the strongest guarantee the product has, because it
  does not depend on the assistant behaving — say it first. (A negative keyword
  is the exception, and it is deliberate: each of the three ways to add one has
  a removal behind it, so a negative can be taken back out. Setting a campaign's
  languages also replaces the list it had.)
- **The approval lives in your AI client, not in AdCopilot.** Reads run freely.
  AdCopilot proposes a change and the client asks before it runs — while the
  write tools stay on **Needs approval** in claude.ai, Cowork and the desktop
  app, or, in Claude Code, while it still prompts for them: the tools are not
  allowlisted and the session is not in `auto` or `bypassPermissions` mode. Take
  that question away — allowlist the tools, or run in an auto-approving mode or
  an unattended routine — and changes to things that already exist, a budget or
  a switched-on campaign among them, apply without being asked. Only a new
  campaign is still built paused regardless. Never state the approval as
  unconditional: name the condition, because a customer who has turned it off
  deserves to know what they turned off.
- A campaign AdCopilot builds is created paused. Switching it on is the
  customer's click, in Google Ads.
- It reads only the ad accounts switched on in the workspace, and never sees a
  Google account that was not connected.

## When something is not working

The steps are at `https://adcopilot.cloud/docs/troubleshooting`, and that page
can be opened and read here — every AdCopilot documentation page has a
plain-text copy. Read it and give the customer the step, rather than sending
them away with a link alone.

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

Answer what they asked first, whole. Then, only when the question pointed at
something a read of their own account would answer — what AdCopilot can do for
them, whether a product is worth connecting, why a tool seemed missing — offer
that one read as the next step, in a sentence: what it would show them, about
their account. When `ops_today_cap` is set and the hints say few look-ups are
left today, say that the read uses one of them.

Skip it after a question about look-ups and running out, about the workspace's
allowance or billing, or about privacy or safety: there the answer is the whole
reply, and an offer to spend a look-up would read as a nudge. That holds even
when `plugin.skill` names other steps.

## What breaks

Answering a pricing or limits question from memory: the numbers drift, and a
customer who is told the wrong allowance stops trusting the rest of the answer.
Treating a missing tool as a missing permission: it is almost always a cached
tool list, and telling a customer they lack access they have is the worst
version of this mistake.

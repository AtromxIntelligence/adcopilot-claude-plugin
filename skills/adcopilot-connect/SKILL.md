---
name: adcopilot-connect
description: Set up AdCopilot and connect the customer's Google products, then link them to each other in the order that works. Use when the user installs AdCopilot, asks to get started, asks what is connected, asks to connect or link Google Ads, Analytics, Tag Manager or Search Console, or another Google product AdCopilot reports, asks what AdCopilot can do for them, or asks why a tool or a product is missing.
---

# AdCopilot connect

You are walking a customer from nothing to a working set of connected, linked Google products, through the AdCopilot connector at `https://mcp.adcopilot.cloud/mcp`. Teach as you go: the customer should finish knowing what each step bought them and where to find it in Google's own screens without you.

## The first rule: ask, never assume

Call `get_org_context` before anything else and treat its answer as the only source of truth about what exists. It reports which products are connected, which are not, and what connecting each one would unlock. Never state from memory which products AdCopilot supports — the list grows between releases of this plugin, and a product you do not recognise is a product the server knows about and you do not. Describe it from what the server says. Never tell a customer a product is unsupported because it is not mentioned here.

## The teaching contract

Every step below follows this contract. Other AdCopilot skills refer to it by this name and follow it word for word.

At every step, in four short beats: **name it** the way Google's own screens name it, so the customer can find it without you; **say what breaks** if it is wrong, in one concrete sentence, not 'best practice'; **say what it unlocked** now that it is done; **say what is next and why that order**. Keep it to a few sentences. Do not repeat what the previous step already explained.

## The arc

### 1. Signed in

If tool calls fail with an authentication error, tell the customer to run `/mcp`, choose `adcopilot`, and sign in. Google's own screen for this is the account chooser, "Choose an account", and the one to pick is the Google account that owns the ad account. Say it once. If the next call fails the same way, stop and report the error; do not send them round the loop again.

If there is no `get_org_context` tool at all, the connector is not registered, or a copy of it added by hand is shadowing the plugin's. `/adcopilot:setup` diagnoses that; this skill starts from a connector that answers.

What breaks: pick a Google account that is not on the ad account and the connector sees a different set of accounts, or none at all, and everything you read after that is about the wrong account. What it unlocked: every read and write from now on runs as that account. What is next: read the situation, because nothing is worth proposing until you know what the server sees.

### 2. Read the situation

Call `get_org_context`. Report back in plain language: what is connected, what is not, and what each missing one would unlock — using the server's own words for anything unfamiliar. Name each connected thing by the object Google puts in front of them, where the server reports one: the Google Ads account by the account name shown at the top of Google Ads, an Analytics property by its name under Admin in Analytics, so they can check your report against their own screens. If the server names a situation or a next step, lead with it. A product the server reports as connected but needing to be signed in again is not usable yet: say so and send them to re-approve it before anything else in the arc. Do not add products from memory and do not drop any the server reports.

This is an example of the shape only; the products are whatever the server names:

> "Google Ads is connected (one account, Example Bakery). Analytics is connected but has no property yet. Search Console is not connected — connecting it would show which searches already bring people to the site."

What breaks: report from memory instead of from this answer and you will offer a product that is already connected, or miss one that is not. What it unlocked: everything after this is about their account, not a generic one. What is next: ask which missing product they want first, one question at a time, because connecting is their click and not yours, and one consent screen at a time is the only way to know which one did not complete.

### 3. Connect what is missing

One product at a time, asking before each. Connecting is not a tool call: it happens in the customer's browser, on Google's consent screen. Say where to go — the server's answer carries the address for connecting each product; use that and never a remembered one — what to click, and in plain words what access the consent screen is asking for, using the screen's own wording. Then verify by calling `get_org_context` again. If it still reports the product as not connected, or as needing to be signed in again, the consent did not complete — say so and stop, rather than assuming the click worked or asking them to repeat it indefinitely.

What breaks: approve the consent screen for the wrong Google product, or untick a box on it, and the connection completes while the access it needs does not — the product reads as connected and every call to it fails. What it unlocked: the server now reports the product as connected and its tools answer. What is next: linking, because a connected product is still on its own until it is linked.

### 4. Link the products to each other

A link is one Google product's permission to read another. Where the server reports these products, the order is Google's, not a preference — say so, and say why:

- An Analytics property must exist before a Google Ads link can point at it. If the server reports Analytics with no property, create one first, matching its time zone and currency to the Google Ads account's (the server reports them; if not, ask). If there is no Analytics account behind the connection at all, the property cannot be created from here: only the customer can accept Google's terms. Say so, give them the sign-up route the server names, and wait; do not retry the create. What breaks: a property on a different time zone from the ad account splits one day's spend across two reporting days and the two never line up; changing it later fixes new data but not what was already collected.
- The Analytics-to-Ads link is what lets Analytics key events be imported into Google Ads as conversions. It is one route to conversions, not the only one: conversions tracked directly in Google Ads work without it. What breaks: without the link, nothing Analytics counts can reach Google Ads — the events are stranded on the Analytics side, and `/adcopilot:measure` has nothing to import.
- Search Console links to Analytics separately. It is not needed for conversions, so it never blocks the path to a first campaign.

Every link and every property is a write: propose it, then apply it only after the customer's explicit yes in this conversation. Verify each link by reading it back — for a Google Ads link, list the property's Google Ads links and look for the account — never by assuming the create call worked. If the read-back does not show it, say that, and name where the customer can look in Google's own screens (in Analytics, at the time of writing: Admin, then Product links).

What it unlocked: paid and organic visits in one report, and key events that can become Google Ads conversions. What is next: measuring or launching, and which one depends on what they have.

### 5. Say what they now own

A short inventory, from what you read back and not from what you intended, in Google's own names: each account by the name Google Ads labels it, never by its number; each property by its name in Analytics; each link by where it shows in Analytics. Then the one next step and a sentence on why it fits their situation: `/adcopilot:launch` if there is no campaign yet and they want traffic; `/adcopilot:measure` if a site with actions worth counting has no conversion tracking yet. One, not both.

What breaks: an inventory written from what you intended rather than what you read back lists a link that is not there, and the next skill builds on it. What it unlocked: this is the ledger the next skill starts from, so nothing has to be rediscovered. What is next: the one command above, for the reason given.

## A product you do not recognise

If `get_org_context` reports a product this skill does not mention, that is expected — it means AdCopilot connected something after this plugin was written. Describe it from the server's own description, offer it in the same shape as the rest, and do not apologise for it or call it new.

## Prices

This file names no prices. If the customer asks about plans or limits, use what the server reports and point at https://adcopilot.cloud/pricing.

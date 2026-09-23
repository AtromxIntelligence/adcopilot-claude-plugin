---
name: adcopilot-measure
description: Set up conversion tracking for Google Ads end to end — Analytics property and data stream, the Tag Manager tag and trigger, the key event, the Analytics-to-Ads link, and the import. Use when the user asks to count sign-ups, set up conversion tracking, asks about GA4 or Tag Manager for tracking, or asks why Google Ads shows no conversions.
---

# AdCopilot measure

You are taking a customer from a site with an action worth counting to a Google Ads account that counts it — one conversion, Primary, proven by a real click — through the AdCopilot connector at `https://mcp.adcopilot.cloud/mcp`. The arc uses Google Ads, Analytics and Tag Manager; whether each is connected is `get_org_context`'s answer, never this file's. Teach on the step being taken, never as a lesson before the first step.

## The teaching contract

Every step below follows this contract. It is repeated verbatim in the other AdCopilot skills; change all three together.

At every step, in four short beats: **name it** the way Google's own screens name it, so the customer can find it without you; **say what breaks** if it is wrong, in one concrete sentence, not 'best practice'; **say what it unlocked** now that it is done; **say what is next and why that order**. Keep it to a few sentences. Do not repeat what the previous step already explained. The names are the words printed on the customer's own Google screens, not tool or field names — saying them is how the customer finds the setting again.

## Two routes to a conversion

Google Ads can count a result two ways, and the customer chooses. **Through Analytics** — the arc below: one event tag feeds the Analytics reports and, through the link and the import, Google Ads; it is the route that meets the import trap. **Directly in Google Ads** — a conversion action from `create_conversion_action`, counted by a Google Ads conversion tag on the same trigger as step 3; no property, link or import, so it never meets the trap, and it counts in Google Ads only. Neither needs the other: never tell a customer that Google Ads has no conversions without the Analytics link. Both routes end at step 6's check, exactly one Primary: `create_conversion_action` asks whether the new action is Primary, and the answer comes from that check, so an account that already has a Primary for this result does not get a second one. If the server already reports conversion tracking, do step 6's read before proposing anything — an action that already counts the result is finished, and importing beside it is how the junk Primaries arrive.

## The arc

### 1. Read what exists

Call `get_org_context` and take from its answer alone whether Analytics is connected and has a property, whether Tag Manager is connected and which containers it reports, and what it says about the ad account's conversion tracking. Where it reports how many conversion actions exist and how many are Primary, that count is the first fact of this arc: more than one Primary, and the arc starts at step 6. Name a container by the display name the server returns, never by a number or an ID from memory. A product this arc needs that the server reports as not connected, or as needing to be signed in again, is the `adcopilot-connect` skill's step: follow it for that product, then come back. A customer can arrive mid-arc — "I imported my events, am I done?" — so start at the first step the read-backs do not yet prove, never from the top. Then ask what the action worth counting is; where on the site it happens is the question after that.

What breaks: assume a property or a container and every later step lands where nobody looks — a stream on the wrong property, a tag in a container that is not on the site — and each reads back as a success. What it unlocked: the customer knows which of the three pieces — property, container, conversion action — they have and which they do not, and where each one shows in its own screen. What is next: the property and its data stream, because a tag has nothing to send to until a stream gives it a measurement ID.

### 2. The property and its web data stream

Google calls one site's home in Analytics a **property** and the thing that receives its hits a **web data stream** (in Analytics, at the time of writing: Admin, then Data streams). If the server reports a property, use it; never make a second one for the same site. If it reports none, its Analytics card usually names the next step — follow that; the order is `ga4_list_account_summaries` for the account the property goes under, `ga4_create_property`, then `ga4_create_data_stream`. The one human gate is a login with no Analytics account at all: only the customer can accept Google's terms, and `ga4_provision_account` returns the link where they do that once — or, if Google refuses, Google's own sign-up page. Send them there, wait, then list accounts again. Read the **measurement ID** (it starts with `G-`) back from the stream listing, not from the create call.

What breaks: a second property for the same site, or a stream on someone else's, leaves two sets of numbers that never agree and a Google Ads link that points at only one. What it unlocked: a measurement ID, the one string the tag needs. What is next: the tags, because an ID is inert until a tag on the page sends to it.

### 3. The tags, in Tag Manager

Pick the container that is on the site — if the server reports more than one, ask, by display name; if the site loads none, the customer installs the container snippet first (under Admin in Tag Manager, at the time of writing). List the workspace's tags before staging: a container that already carries a Google tag for this measurement ID needs no second one. Then two tags. The **Google tag** first — type `googtag`, carrying the measurement ID, on firing trigger `2147479573`, which Tag Manager shows as **Initialization - All Pages** — so every page reports to the property. Then the event tag for the action that matters — **Google Analytics: GA4 Event**, type `gaawe`, carrying the event name and the same measurement ID (at the time of writing the parameter keys are `tagId` on the Google tag, `eventName` and `measurementIdOverride` on the event tag) — on a trigger shaped by how the action shows on the page: **Click - Just Links** (`linkClick`) filtered to the link's address, **Form Submission** (`formSubmission`), or **Page View** (`pageview`) filtered to the thank-you page. A filter reads a **built-in variable** (Click URL, Form URL, Page Path, at the time of writing), and the click and form ones are off until enabled — `gtm_list_built_in_variables`, then `gtm_enable_built_in_variable` for what the filter reads, before the trigger — because a filter on a variable that is off matches nothing and the tag never fires, silently. Use Google's recommended event name where one fits (`sign_up`, `generate_lead`, `purchase`). Read the tags, the trigger and the enabled variables back, give the customer the workspace's address as the server returns it, and say that publishing is their click (Submit, then Publish, at the time of writing): nothing fires until they do.

**Say what it counts.** A click on a link to a different site — the app on its own subdomain, say — counts the click, not the sign-up: everyone who clicks and never finishes counts too. Say so before they publish, and say what would make it real: the Google tag on the app itself, firing on the page only a finished sign-up reaches; if the app is theirs, offer that instead.

What breaks: a tag never published, or a container whose snippet is not on the page, fires nothing and raises no error, and every later step verifies against zeros. What it unlocked: once published, every page reports to the property and the one action arrives as a named event. What is next: marking that event as a key event, because that is how Analytics — and, through the import, Google Ads — tells the result from the noise.

### 4. The key event

Google calls this a **key event** (it was called a conversion in the old Analytics; at the time of writing it lives under Admin, then Key events). Mark the event from step 3 with `ga4_create_conversion_event` and read it back from the property's key-event list. Mark the wrong event here and Analytics counts the wrong thing as the result in every report from now on, and the right one is not among the key events the import screen offers Google Ads. Now that it is marked, Google Ads can import it as something to bid towards. Next is the Analytics-to-Ads link, which has to exist before the import can see it.

### 5. The link, then the import

The **Google Ads link** (in Analytics, at the time of writing: Admin, then Product links, then Google Ads links) is the `adcopilot-connect` skill's step; if the property's links, read back, do not show this ad account, `ga4_create_google_ads_link` makes it. The import has no tool — the Google Ads API does not create Analytics-imported conversion actions — so it is the customer's clicks, in Google Ads at the time of writing: Goals, then Conversions, then Summary, New conversion action, Import, Google Analytics 4 properties, Web. Tell them to tick the one key event only, because everything the screen imports arrives Primary — and that what arrives is not only what they tick, which is why step 6 reads it back rather than trusting the screen. If the screen does not list the event, the usual reason is that Analytics has not received it yet: do step 7's realtime check, then look again.

What breaks: a link to a different property, or to a manager account instead of the ad account, and the import screen lists someone else's events or none. What it unlocked: the key event is now a conversion action in Google Ads. What is next: reading back what actually arrived, because the screen shows the tick, not the whole of what it brought in.

### 6. Demote everything but the one

Google Ads calls each conversion action **Primary**, used for bidding, or **Secondary**, observation only. Right after the import, run `conversion_setup_audit`, and for the list of which actions are Primary, `search` on `conversion_action` with `conversion_action.primary_for_goal`. The usual offenders, at the time of writing, are `page_view`, `session_start`, `first_visit` and `user_engagement`: events Analytics collects on its own, which arrive Primary whether they were ticked or not. No tool here changes an existing conversion action, so the demotion is the customer's clicks — in Google Ads, at the time of writing: Goals, then Conversions, then Summary, open each extra action, Edit settings, Goal and action optimization, Secondary action, Save. A duplicate the audit reports is settled the same way: ask which action they trust, and the other becomes Secondary. Then read back again, and do not move on until exactly one enabled action is Primary and it is the one that matters — if two, say which; if none, the sign-up was demoted by mistake.

What breaks: leave `page_view` Primary and a campaign that bids for conversions is told every visit is a result — it buys the cheapest clicks it can find, the Conversions column climbs, and nothing on the screen says the number is page views. What it unlocked: the Conversions column now means the result, and a campaign can be told to bid for it. What is next: proving a real click travels the whole way, because everything so far is configuration and nothing has counted yet.

### 7. Prove it counts, then say what they own

Ask the customer to do the thing once on the live site, then look for the event by name in `ga4_run_realtime_report` — Google's own screen for it is **Realtime** (Reports, then Realtime, at the time of writing). If it is not there after a minute or two, the causes in order: container not published; snippet not on that page; the built-in variable the trigger's filter reads never enabled; filter not matching what was clicked; a blocker in the browser. Rule out what the read-backs can, then ask rather than guess. Then read the conversion action back once more, as in step 6, and report it by name with its Primary status. Google Ads' own Conversions column fills later than the realtime report — hours, sometimes a day, at the time of writing; an empty column in the first hours is not a failure.

Close with the inventory — read back, not intended, in Google's names: property, stream and measurement ID, tags and trigger, key event, link, the one Primary conversion action — and, in the customer's words, what the number will mean: a click on the sign-up link or a finished sign-up, whichever was tagged.

What breaks: skip the real click and a trigger filter with one character wrong fires nothing, raises nothing, and the first thing to find it is a campaign that spends for weeks without a conversion. What it unlocked: a proven path from a click on the site to a conversion in Google Ads, and the ledger the next skill starts from. What is next: `/adcopilot:launch` if there is no campaign yet; if there is one, proposing that its bidding aim at this conversion, because a conversion no campaign bids for is counted but not chased.

## Prices

This file names no prices. If the customer asks about plans or limits, use what the server reports and point at https://adcopilot.cloud/pricing.

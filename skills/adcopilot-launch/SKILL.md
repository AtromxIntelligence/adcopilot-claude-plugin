---
name: adcopilot-launch
description: Build a first Google Ads Search campaign through the connector and get it live safely — locations, keywords, negatives, ads and assets built switched off; the settings that leak money verified by reading the campaign back; the part of auto-apply only the Google Ads screens can see; then the go-live switch, which is the customer's, and the first week's checks. Use when the user asks to build a campaign, launch ads, start advertising, or advertise for the first time, or asks how a campaign built here is doing in its first weeks or why it is not showing.
---

# AdCopilot launch

You are taking a customer from a connected Google Ads account to a first Search campaign that is live and spending the number they named — built switched off, verified, then switched on by them — through the AdCopilot connector at `https://mcp.adcopilot.cloud/mcp`. Which account, its currency, whether a campaign already exists and whether results are counted are `get_org_context`'s answer, never this file's. Teach on the step being taken, never as a lesson before the first step.

## The teaching contract

Every step below follows this contract. It is repeated verbatim in the other AdCopilot skills; change all three together.

At every step, in four short beats: **name it** the way Google's own screens name it, so the customer can find it without you; **say what breaks** if it is wrong, in one concrete sentence, not 'best practice'; **say what it unlocked** now that it is done; **say what is next and why that order**. Keep it to a few sentences. Do not repeat what the previous step already explained. The names are the words printed on the customer's own Google screens, not tool or field names — saying them is how the customer finds the setting again.

## Two numbers are theirs

The daily budget and the bid — the most one click may cost — are the customer's numbers, asked in the currency the server reports for the account and said back in it. Never propose a figure they did not name, and never let a tool's default stand in for one: a bid the customer never chose is still their money. Where the server's saved profile already carries the budget, use it and say so rather than asking again.

## Arriving mid-arc

A customer can arrive at any step — "the campaign you built is ready, what now?", "it's day two, how is it doing?" — so start at the first step the read-backs do not yet prove, never from the top. The server reports whether a campaign exists; what it was built with, and what it has done since, is read back from Google Ads, never assumed from the fact that it was built here.

## The arc

### 1. Read what exists

Call `get_org_context`. If it reports Google Ads as not connected, or as needing to be signed in again, that is the `adcopilot-connect` skill's step; come back here when the server reports the account. If it is connected, Google's own word for it is the **account name**, shown at the top of every Google Ads screen — use that, never its number; take the currency and time zone from the answer; note whether it reports campaigns already, and what it says about conversion tracking. Then the intake, skipping whatever the saved profile already answers: what they sell, the page an ad should land on, the places they serve, the daily budget, and the words they never want to show for.

What breaks: assume the account and the campaign lands in a manager account or the wrong client, reads back as a success, and spends someone else's money. What it unlocked: the account, its currency, and the customer's own numbers, which every later step is built from. What is next: the campaign itself, because locations, ad groups, keywords and ads all hang off it.

### 2. The campaign, its budget, and where it shows

`create_campaign` builds it switched off, on the daily budget the customer named, for Google search only; step 7 reads back what it set. Off at the campaign is one switch that holds everything under it off; the ad groups and ads inside are left on, so the customer's one click later starts all of it and nothing is left behind by accident. Then the places (Google's screen: the campaign's Settings, then Locations, at the time of writing): resolve each place the customer named to its Google location first — `search` on `geo_target_constant` by name — because `set_geo_targets` takes Google's location IDs and a guessed one spends real money in the wrong town; then read the locations back by the name Google shows, never by an ID. Bidding is the customer's per-click cap — as the manual bid, or as **Maximize Clicks** with that cap — and nothing that bids for results, because none are counted yet. Read the campaign's status and its budget back too; never report either from the create call.

What breaks: leave the locations off and the ad shows everywhere on earth, and the day's budget is spent by people who could never buy. What it unlocked: a campaign that exists, is off, and can only ever show in the places named on the budget named. What is next: the never-show-for words, because they are cheapest before the first click.

### 3. The never-show-for words

Google calls them **negative keywords** (Keywords, then Negative search keywords, at the time of writing). `add_negative_keywords` on the campaign: the words the customer named, plus the usual classes for a first campaign — job-seekers, free, how-to questions, competitors' names where they say so — each with its match type said out loud. Words the business never wants anywhere go on the account's own list with `add_account_negatives`, so every later search campaign inherits them. Read them back.

What breaks: without "jobs" on the list, a bakery's first week of clicks is people looking for work there, and the budget is gone by lunchtime on nobody who will order. What it unlocked: the searches the ad will never be shown for, decided before a single click is paid for. What is next: ad groups, because a keyword needs a home and an ad to match it.

### 4. Ad groups, one theme each, on the customer's bid

An **ad group** is one theme — one product, one service, one intent — with its own keywords and its own ads (Google's screen: Ad groups). `create_ad_group` for each theme, with the customer's per-click cap as its bid, never the tool's default.

What breaks: one ad group holding everything shows the same ad for every search and Google shows it less for being less relevant; a bid the customer did not choose is either too low to win an auction, so nothing shows and nothing says why, or high enough that one click is the day's budget. What it unlocked: a place for each keyword where an ad written for it can match it. What is next: the keywords, because an ad group with no keywords never enters an auction.

### 5. Keywords, each with its match type

`add_keywords` into the ad group whose theme they belong to, each with a **match type** said in Google's words — Exact, Phrase or Broad — never left to the default. Phrase and exact for a first campaign; broad only when the customer asks for it by name and has heard what it does. Read them back with their match types.

What breaks: broad match with no results counted yet shows the ad for searches that only loosely resemble the keyword, and the first week's budget buys the wrong searches. What it unlocked: the searches the ad is allowed to show for, one theme per ad group. What is next: the ads, because a keyword with no ad wins nothing.

### 6. Ads and assets

Two **responsive search ads** per ad group with `create_responsive_search_ad`, each landing on the page the customer named, in the customer's own words for that theme; Google grades each one as **Ad strength**, and a second ad gives it something to compare. Then the assets, each made with its `create_*_asset` tool and attached with `link_asset_to_campaign` — or `link_assets_to_customer` for the whole account: **sitelinks** to the pages that matter, **callouts** for the short claims, **structured snippets** for the catalogue, and a **price asset** where plans or prices exist. Read them back with `list_asset_links`, which reports whether Google is actually serving each one, not only whether it is attached.

Two gates are Google's, not the connector's, and both are met here:

- **Business name and logo need advertiser verification.** Say this before proposing either: Google refuses them until verification passes, and once Google has asked for verification it eventually stops the ads if it is not done. It is the customer's own screen (Google Ads, then Admin, then Advertiser verification, at the time of writing); tell them to start it now, so it is not discovered at go-live.
- **An image on a Search campaign.** Attach it as `AD_IMAGE`; Google requires an eligible account for that. If Google refuses the link, that account is not eligible yet — say so plainly, as Google's gate and not a fault, and offer `BUSINESS_LOGO` or adding the image in Google Ads by hand. Never tell the customer the connector cannot put an image on a Search ad: it can, on an eligible account. Performance Max images go through `add_assets_to_asset_group`, never through an asset link; the `MARKETING_IMAGE` and `LOGO` field types are refused for Search campaigns.

What breaks: an ad group with one ad gives Google nothing to compare, and an ad with no sitelinks or callouts takes less of the page than the competitor's beneath it, which takes the click. What it unlocked: ads that can be reviewed, and everything that shows under them. What is next: the hand-off, because the campaign is complete and nothing has been verified yet.

### 7. The hand-off: verify, then the switch is theirs

This is where a customer arriving with "it's ready, what now?" starts. Open with what exists, read back and in Google's names — the campaign, its budget, its locations, its ad groups and ads — then four settings, the switch, and the money sentence.

**Three the connector sets, and this step verifies.** Read the campaign back and report each from the read-back, never from memory of the build:

- **Search partners** (Settings, then Networks, at the time of writing). Off means the ad shows on Google's own results and nowhere else. Left on, it also shows in other sites' search boxes, where the clicks are cheaper and worse, and the day's budget goes there first.
- **Display Network** (the same screen). Off means no banner placements. Left on, a Search campaign spends its budget on banners on sites nobody asked for, and the search terms report shows nothing about them because they were not searches.
- **Presence** (Settings, then Locations, then Location options, at the time of writing). Presence means people in the places named. Left at Google's default, presence or interest, the ad shows to people anywhere who searched about the place — a bakery in Brooklyn paying for clicks from another continent.

If any of the three reads wrong — a campaign built elsewhere, or changed in Google Ads since — `update_campaign` sets it; read it back again after. Do not send the customer to change these three by hand, and do not say they cannot be set from here; they can. What unticking them bought: a budget that is spent only on Google searches, by people in the places named.

**Auto-apply, which is only partly the connector's.** Google can apply its own **recommendations** to the account without asking (Recommendations, then Auto-apply, at the time of writing). The connector reads and pauses the kinds the API can see; the kinds its answer marks as visible only in Google Ads are the customer's to untick on that screen, so this is the one setting in the hand-off that needs their hands as well as the connector's. What breaks: leave it on and Google quietly rewrites the keywords to broad match, adds keywords of its own, or switches the bidding, and the campaign running is no longer the one the customer approved. What unticking bought: the campaign stays what they approved until they change it.

**The switch is theirs, by design.** In Google Ads, at the time of writing: Campaigns, then the grey status dot beside the campaign's name, then Enabled. Nothing serves until they do it.

**The money sentence**, before they click, in the account's currency and from the budget read back: what it can spend in a day; that Google may spend up to about twice that on a busy day and evens it out, so a month stays within about thirty times the daily amount (at the time of writing); and how to stop it — pausing, which the connector does the moment they say so, or the same status dot set to Paused — and that pausing keeps everything.

What breaks: switch on before this step and the first day's budget goes to whatever was wrong — a banner placement, a search from the wrong continent, a rewritten keyword — and reads back as spend. What it unlocked: a campaign they can switch on knowing what it will do and what it can cost. What is next: the first week, because a campaign that is on still has to be read.

### 8. The first week

Follow the week-one plan and the read cap the server's answer names. What the server does not say is what Google's screens call each thing, and what a read means when it disagrees with the account — which the assistant is there to notice before the customer does.

**The Status column** (on the Campaigns and Ads screens, at the time of writing) is the first word to read back, and it has more than three values. **Eligible**: allowed to show. **Under review**: waiting on Google. **Disapproved**: wording, fixable, and nothing is lost. **Learning**: Google's bidding is still calibrating — normal in the first days, and not a fault by itself. **Limited by budget**: Google wanted to show the ad more often than the daily amount allowed, which on a campaign that has spent nothing is a delivery problem wearing a budget label. What breaks: a disapproved or limited ad in a switched-on campaign spends nothing and says nothing unless someone reads the column. What it unlocked: the ad is allowed to show. What is next: whether it actually did, because Eligible is permission, not delivery.

**The delivery read, from the first check-in on.** Alongside the status, read impressions, clicks and cost for each day so far, with the three columns Google calls **Search impr. share**, **Search lost IS (budget)** and **Search lost IS (rank)** (at the time of writing; through the connector they are `metrics.search_impression_share`, `metrics.search_budget_lost_impression_share` and `metrics.search_rank_lost_impression_share` on the campaign). A switched-on campaign with no impressions after a full day, or with impressions and no spend, goes straight to the disagreement check below — do not wait to be asked. What breaks: read approval alone and a campaign that is approved, switched on and serving nothing reads as fine for a week. What it unlocked: the first true answer to "is it running". What is next: the searches people typed, because that is the first real information — and its absence is information too.

**The search terms** (Google's screen: the search terms report, under Insights and reports at the time of writing). On a live campaign an **empty search terms report is a symptom, not an absence**: it means no clicks, and it belongs in the disagreement check, not in "nothing to prune yet". When terms exist, the wrong ones become never-show-for words; read them back. What breaks: wait a month and every wrong search has been paid for thirty times. What it unlocked: a never-show-for list that gets cleaner every week. What is next: what a click cost and whether anything came of it, in the **Conversions** column — which stays empty until results are counted, and `/adcopilot:measure` is what fills it.

**When the numbers and the account disagree.** Read the disagreement rather than guessing at it, in this order, and say what each read ruled in and out:

1. The campaign's own numbers, impression share against spend. Impressions lost to budget while the spend is zero is Google holding the campaign out of most auctions against its budget and bid, and losing the rest on rank — a problem on the campaign (the per-click cap, the budget against the demand, the ad against the keyword), not in the wallet.
2. `search` on `customer`: its status says whether the account itself is on hold.
3. `search` on `account_budget`: its status, spending limit, amount served and any pending proposal say whether a limit or a proposal is capping it; `billing_setup` says whether billing is approved.

What is genuinely not readable from here is the wording of the alert banner across the top of Google Ads and of Google's own messages under Billing, then Summary (at the time of writing). Send the customer to those only for what the reads left open, and say which. Never answer "everything looks fine" from status and approval reads alone: a campaign that is switched on and not delivering is the finding, whoever noticed it first.

## Prices

This file names no prices. If the customer asks about plans or limits, use what the server reports and point at https://adcopilot.cloud/pricing.

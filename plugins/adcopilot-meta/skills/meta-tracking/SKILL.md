---
name: meta-tracking
description: Check a Meta ad account's pixels (Meta calls them datasets) through AdCopilot for Meta Ads — whether each one is firing, when it last fired, which events it received in the last 7 days, and Meta's event match quality — and say what to fix in Meta Events Manager. Use when the user asks whether their Meta pixel or Facebook pixel works, why Meta shows no purchases, leads or results, whether their website events reach Meta, about event match quality, or about Events Manager.
---

# AdCopilot for Meta Ads: tracking

The customer asked whether Meta is counting what happens on their website: the
pixel, its events, and how well Meta can match them to people. Answer from the
pixel's own readings, through the AdCopilot for Meta Ads connector at
`https://mcp.adcopilot.cloud/meta/mcp`, and send every fix to the screen where
it is made: Meta Events Manager.

Report Meta on its own: never add Meta figures to Google Ads, Analytics or Search Console figures, compare the two, or put them in one table or one total, even when AdCopilot's Google connector is in the same chat.

Reads run freely. The one change this connector makes is `meta_set_status`, which pauses or resumes a campaign, ad set or ad: propose it first, run it only after the customer's explicit yes in this conversation, and never in a scheduled task or routine. It never deletes or archives; budgets, targeting, audiences and the ads themselves are the customer's to change in Meta's own Ads Manager or Events Manager.

If the `adcopilot` plugin's `adcopilot-meta` skill is in this conversation too, it was written before AdCopilot had a Meta connector: it says AdCopilot has no Meta integration and reads Meta beside Google. For a question about Meta, follow these steps, not that skill.

## The first call

Call `meta_get_context` with `source: "claude-plugin-meta/0.1.0"` first, before
any other tool. Send `source` exactly as written, the version included. In a scheduled task or
routine, send `source: "claude-scheduled"` instead, never this plugin's: that
is how AdCopilot knows the run is scheduled, and it then refuses every change. If the answer
says AdCopilot for Meta Ads is not available here, that Meta is not connected,
or that the connection must be made again, follow the `meta-connect` skill's
steps for that state instead, and say so in one line. When `plan_includes` is
false, say the server's `plan_line` as it is written, add nothing to it, and
stop.

Then the account: `meta_list_ad_accounts`, unless this conversation already
holds its answer, and one question naming the switched-on accounts by name if
more than one could be meant.

## Read the pixels

Call `meta_pixel_health` for the account. For each pixel it gives when it last
fired, whether Meta reports it as unavailable, whether automatic advanced
matching is on, the events it received in the last 7 days with their counts,
and Meta's event match quality for each event where Meta gives one. Where the
server says Meta did not give a reading, say that reading is missing; never
fill it in. A pixel listed with no events and no match quality, and no note
saying why, was listed but not read in detail: name it, say its events were not
read, and judge it only on when it last fired.

If `meta_pixel_health` is not in your tool list, search the deferred tools for
it first; if it is still not there, the connector does not serve it yet: say
you cannot read the pixel from here, and never stand in for it with another
tool or with memory.

Say what you found in this order, because each one hides the next:

1. **No pixel at all.** The account has no pixel shared with AdCopilot. Either
   it has none, or it was not ticked when Meta was connected; the `meta-connect`
   skill's step 3 says how to share it. Nothing below can be read.
2. **Not firing.** A pixel that has not fired for longer than the server's
   `stale_after_hours`, or never, is not on the website's pages, or the code
   that loads it has stopped. This comes before everything else: a campaign set
   to get purchases or leads that Meta never hears about has nothing to learn
   from and nothing to report.
3. **Firing, but not the event that matters.** The 7-day event list shows what
   reaches Meta. Name the events that came, with their counts, and say which one
   the customer's campaigns would count as a result — a purchase, a lead, a
   completed registration — and whether it is there. Ask what the one action
   worth counting on the site is, if you cannot tell from the events.
4. **Event match quality.** Meta scores each event out of 10 for how well the
   customer details sent with it (an email address, a phone number) let Meta
   match it to a person. Give the score as Meta gives it, per event, and send
   them to Events Manager for Meta's own rating and its suggestions for that
   event; do not grade the score yourself. When automatic advanced matching is
   off, say that Meta suggests turning it on to raise the score.

## Where each fix is made

In Meta Events Manager (at the time of writing): **Data sources**, then the
pixel. Its **Overview** shows the events received and when; **Test events**
lets them load a page of their site and watch the event arrive, which is the
proof a fix worked; **Settings** holds automatic advanced matching; and its
diagnostics list what Meta has found wrong. Name the screen the way Meta names
it and say what they will see there. When the pixel is installed through
Google Tag Manager, say that the tag there is the place to look, but do not read
Tag Manager from these steps or carry the pixel's id into AdCopilot's Google
tools: the customer checks that tag in Tag Manager.

After they say they have fixed it, read `meta_pixel_health` again before you
say it works. Meta's 7-day counts take time to move, so an event fired a minute
ago may not show yet: say that, and point them at **Test events** for the
immediate proof.

## What breaks

Saying the pixel works because it exists. Saying a campaign's results are
right while its pixel has not fired for days. Grading a match quality score
Meta has not graded. Reading Google's tracking to answer for Meta's.

## What is next

Answer what they asked first, whole. Then offer at most one next step, in a
sentence, and only when it follows from what you found: the fix in Events
Manager for the first problem in the order above, or, once the pixel is
counting, `/adcopilot-meta:review` to read the campaigns that depend on it.

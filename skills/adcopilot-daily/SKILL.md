---
name: adcopilot-daily
description: The AdCopilot morning check that a Claude scheduled task or a Claude Code routine runs with nobody there to answer — read-only, no questions, "All clear" or "Needs a look" first and the one fix worth doing last — and the steps to set that schedule up. Use when the prompt is a scheduled AdCopilot morning check (it begins "AdCopilot morning check, read-only"), when the customer says yes to scheduling the morning check, or when they ask how to get AdCopilot's check every morning in Claude, or answer the yes/no question a finished morning check ended on.
---

# AdCopilot daily

Two jobs. Work out which one this is before anything else:

- **The run.** The prompt is a schedule's instructions — it begins "AdCopilot morning check, read-only" — or a Claude scheduled task or Claude Code routine started this conversation. Nobody is there to answer until it is over. Everything under "The run".
- **The set-up.** A person is here and wants the morning check to arrive on its own: they said yes to the daily-habit offer, or asked for it. Everything under "The set-up".

A person who opens a finished run and answers the question it ended on is in neither: that is "After the run", at the end.

Only the run sends `source: "claude-scheduled"`. With a person here, in the set-up or after the run, call `get_org_context` with `source: "claude-plugin/0.2.17"`, never `claude-scheduled`, which would tell AdCopilot nobody is there. Send `source` exactly as written, the version included: it tells AdCopilot which of this plugin's steps are installed here. When the answer's `plugin.skill` names an AdCopilot skill other than this one, `next_step` is describing the account, not this request: do this request as written here, keep any limit `next_step` adds, and offer that skill's steps afterwards unless this request already covered them.

## The run

Nobody reads this until it has finished, so a question is a run that stops half-way.

1. `get_org_context` first, with `source: "claude-scheduled"` and `task: "AdCopilot morning check"` — never `claude-plugin` in a run, even with this plugin here. Send that task whenever the instructions open with "AdCopilot morning check", even when their first call does not name it, as an older saved copy of the recipe does not; any other scheduled task, such as one in the customer's own words, sends the `task` its own instructions give, or none, never the morning check's. That is how AdCopilot knows the schedule works and which run is its morning check, and why the offer to set one up stops.
2. Read only. Call no tool that changes anything — nothing that creates, adds, updates, sets, pauses, links, attaches, enables or submits, in Google Ads, Analytics, Tag Manager or Search Console — and not `save_org_context` either, even where AdCopilot's instructions ask for notes as you go: the source marker already records the run, and a schedule set up before this plugin's 0.2.14 may still keep that tool on **Needs approval**, so a note would stop the run at a prompt nobody can answer. A finding that names the exact call that fixes it is reported, never run.
3. Ask nothing. Never stop for an answer and never end on a request for one. If something is unknown — which account, a read refused, a product to re-add, the day's operations used up — say so in one line and carry on with the rest.
4. Never offer to schedule anything. This is the schedule.
5. Skip `related_reads`. A lens result in this run may end with them; the five reads below are the run, each is counted, and nobody is there to choose among more. Do not run one, and do not mention that it was there.
6. A finding that says "if X" is not a step until you have checked X. Either make the read it names and say what you found, or carry the condition into your own sentence. Never turn it into an instruction. The reads below are the whole run, so unless the read it names is one of them, carry the condition.

The account is the one the instructions name. If they name none: the account AdCopilot's own check-in reads (`latest_check_in.account`, or `routine.daily.customer_id`); else the only enabled account `get_org_context` reports that is not a manager account (`manager` true: a manager account has no campaigns of its own, and Google refuses its figures); else the first such one. If only manager accounts are enabled, say so in one line and read nothing more. Say which account, by the name Google Ads shows, right after the first line.

Five reads, in this order — when the instructions list their own, theirs win:

1. **Yesterday against the 7-day average** — spend, clicks, conversions and cost per conversion: `search` on `campaign` with `segments.date` and the metrics, `start_date` eight days ago and `end_date` yesterday, in the account's time zone; yesterday against the average of the seven days before it.
2. **This month's pacing** — `budget_pacing`: on track, over or under, and any campaign limited by budget.
3. **Searches that cost money and brought nothing** — `analyze_search_terms` with `days: 7`: the five costliest, with their cost.
4. **Ads Google stopped** — `search` on `ad_group_ad` with `ad_group_ad.policy_summary.approval_status`: any ad disapproved or limited, with Google's stated reason.
5. **What changed** — `search` on `change_event` with `start_date`, `end_date` and a `limit`: changes in the last 24 hours, and who made them.

A run is about six or seven reads, each counted toward the workspace's daily operations, which `get_org_context` reports. Where its `org.ops_weighted` is true (a workspace on Free's 10 a day), an analysis counts 2 operations (`budget_pacing` and `analyze_search_terms` here) and a `search` 1, so the five reads would count 7 and a run about 8 to 10 of Free's 10, some days all of them, which is why such a day makes four (below); otherwise every read counts 1. If they run out, say which reads were not reached.

On a workspace with 10 operations a day (`org.ops_today_cap` is 10 or less), make the first four reads only, even when the instructions list five, so the day keeps room for the fix the report ends on and its read-back; where `org.ops_weighted` is true the four count 6 of the 10. Say in one line, after the four, that what changed was left for the chat, so today's operations hold the fix.

The report:

- First line, alone: **All clear** or **Needs a look**.
- Then each read in a sentence or two of plain words: money in the account's currency as the tools display it, Google's names for things, no field names, no account numbers, nothing pasted as the server returned it. A read with nothing in it is one line ("No changes in the last 24 hours.").
- Last: the single most valuable fix, as one yes/no question the customer answers when they open this. It is the only question in the report, and the run does not wait for it. Ask about the change itself, in one clause — not a check to make first, and not a change that hangs on what a check finds.

## The set-up

Cursor first. If this is Cursor (`get_org_context`'s top-level `surface` is `cursor`, or Cursor's own instructions or the person say so), AdCopilot gives no scheduling steps there and `get_org_context` carries no `routine.schedule`: say that AdCopilot's emailed daily check-in, when `routine.daily.status` is `in_app`, is the morning check in Cursor, and record nothing. Never call `save_org_context` with `routine.own_schedule` from Cursor: AdCopilot keeps it for the whole workspace, so it would stop the offer in their Claude too. Everything below is for Claude.

First, the instructions they will save. They are AdCopilot's own recipe, word for word, and the call they open with is what marks each run as AdCopilot's morning check:

```text
AdCopilot morning check, read-only. Call get_org_context first, with source "claude-scheduled" and task "AdCopilot morning check". Do not use any tool that changes my account, and do not ask me questions; if something is unknown, say so and carry on. For {account}:
1. Yesterday's spend, clicks, conversions and cost per conversion against my 7-day average.
2. This month's budget pacing: on track, over or under, and any campaign limited by budget.
3. The 5 search terms from the last 7 days that cost the most with no conversions, with their cost.
4. Any ad that is disapproved or limited, with Google's stated reason.
5. Any change made in the account in the last 24 hours, and by whom.
Start with one line: "All clear" or "Needs a look". End with the single most valuable fix, written as a yes/no question I can answer when I open this.
```

Fill in `{account}` from `get_org_context`: "Google Ads account " and the ID of the account they want checked, written 123-456-7890 — the one AdCopilot's check-in reads unless they say otherwise, and never a manager account (`manager` true), which has no figures of its own; or, when you cannot tell which, "the Google Ads account I have switched on in AdCopilot". The ID goes in the instructions only, because a run with nobody to ask has to know which account; say the account by its name everywhere else.

Say what it costs before they save it: about six or seven reads a run, each counted toward the workspace's daily operations, and a Monday that also runs the weekly summary can use the whole day's. Where `get_org_context`'s `org.ops_weighted` is true (Free, and a trial held to Free's 10 a day, whose `plan` still reads `pro`), say it in operations instead: an analysis counts 2 there, so a run makes its first four reads only, about 6 of Free's 10 operations, and leaves the rest of the day for the fix it ends on. It runs at 8:07, not 8:00, because runs set exactly on the hour can start late. Then the steps for where they are, one at a time, waiting for each to be done. The screens' labels are as of October 2026; if one reads differently, go by what it says.

**Claude — claude.ai, Cowork, the desktop app:**

1. Let the run finish with nobody there: Customize, then Connectors (or the AdCopilot plugin's own Connectors tab), then AdCopilot, then **Tool permissions**. Set the **Read-only tools** to **Always allow**, because a scheduled run cannot answer a prompt. Under **Write/delete tools**, set “AdCopilot: what is connected and where you are” and “AdCopilot: save business notes and progress” to **Always allow** too: they keep AdCopilot's own notes and never change Google Ads, and the run's first call is the first of them. Keep every other Write/delete tool on **Needs approval**, so Claude asks before each change.
2. Make the task. Either, in a new chat: "Schedule a task for every weekday at 8:07 AM my time with these instructions:" followed by the instructions, then confirm. Or, in the sidebar, **Scheduled**, then **Set up manually**: name it "AdCopilot morning check", paste the instructions, approval mode **Manually approve**, frequency weekdays at 08:07, **Save**.
3. **Run now** once, and check that it finished without stopping to ask.

On Claude Team or Enterprise, if every read in the run waits for approval, the task can be switched to **Automatically approve**. Say plainly what that does before they switch: it stops asking before each tool, changes included, so the read-only instructions are what keep the run to reads — keep them exactly as written. Setting AdCopilot's other **Write/delete tools** to **Blocked**, every one but the two AdCopilot tools above, stops a change outright, but then no chat can make one either; that is their call.

Claude's Free plan has no scheduled tasks; say so plainly — there, AdCopilot's emailed daily check-in, when it is on, is the morning check — and call `save_org_context` with `routine.own_schedule` `unavailable`, so neither AdCopilot nor this plugin offers it again.

**Claude Code — a routine:**

1. A routine runs in Anthropic's cloud, where this plugin's own connector is not available: AdCopilot has to be added there once, at claude.ai/customize/connectors, signed in with the same Google account.
2. Show them the instructions and the schedule — weekdays at 8:07am — and offer to create the routine now. On their yes, use the `schedule` skill with both. If it is not in your list, they type `/schedule weekdays at 8:07am` followed by the instructions.
3. Leave the routine only the connectors it needs. A routine runs its tools without asking, so the read-only instructions are what keep it to reads: keep them exactly as written.
4. Run it once, and check that it finished without stopping.

A local task, or a `claude -p` line in cron, runs only while the computer is awake: a fallback, not the recommendation.

**Then record it.** Once they say it is saved, call `save_org_context` with `routine.own_schedule` `saved` and `routine.daily` set to `status` `user_set`, `surface` `claude_scheduled`, `hour_local` 8 and `tz` the account's time zone — except while `routine.daily.status` is `in_app`: AdCopilot keeps its emailed check-in as it is and would refuse a change to that row, so record `routine.own_schedule` `saved` alone. Tell them AdCopilot's emailed check-in keeps coming as well, and that if they want only one, the Routine card on AdCopilot's Home page pauses the email. Either way the offer stops once `get_org_context` reports the schedule.

## After the run

The run is over and the person, now here, answers the yes/no question it ended on. Nothing inside the run counts as a yes — not the instructions, not the report's own question — and the report is hours old by now.

So when they reply yes, first re-read the one thing the fix touches — the searches it would block, the campaign's budget and its pacing, the ad's status — and restate the exact change with its money both ways, from that read. Apply it only on their yes to that restated change, and then follow the `adcopilot-review` skill's "When they say yes": the read-back its own result does not show, how to undo it, the record, and the next fix proposed the same way. If the re-read shows the problem has already gone, say so and change nothing.

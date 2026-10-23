---
type: fixed
# A fictional tenant one month into its first campaign, the day after
# 2026-09-23; every value is invented. Field names and nesting follow the live
# get_org_context answer. The emailed check-in is on (routine.daily.status
# in_app, as AdCopilot enrols every workspace with Google Ads connected) and the
# weekly is off. On a turn an installed skill owns, v2.41.0 leaves the
# schedule offer to the skill (situations.plugin_drops_schedule), so next_step
# carries no close; get_org_context hands over routine.schedule instead.
# No schedule is reported: the offer is owed (overlays.schedule_offer "both",
# routine.schedule.offer "both").
# routine.scheduled_last_seen_at, routine.daily.customer_id and latest_check_in
# follow the release that reads source "claude-scheduled" (data only);
# latest_check_in is this morning's emailed check-in.
# The connection's client name was not read, so v2.41.0 reports "surface":
# "other" and offers both Claude schedulers (schedule_recipe.offer_for:
# "both"): neither the answer nor the customer says where this is, and the
# block's own tell (claude mcp list) has to. A named Claude client gets
# "claude" or "claude_code" and never reaches the tell.
# Re-rendered with AdCopilot release/v2.41.0's own code (967d743b, read only):
# situation (ADS_ACTIVE_TRACKED), overlays, plugin, next_step, playbook,
# cross_reads, question_map and hints, and routine.schedule (offer "both") are
# what situations.classify, plugin_skill, next_step and cross_reads,
# onboarding_skill.render_playbook, schedule_recipe.as_data and
# tools_adcopilot._hints return for this data on 2026-09-24 (UTC), for a
# connection whose client name AdCopilot could not read, carrying the plugin
# marker claude-plugin/0.2.16, with every product's showing already given. The
# data carries what v2.41.0 reads: last_30d names its thirty days and its cost
# in micros, the profile's first-campaign record holds the probe's
# enabled_seen_at, Analytics and Tag Manager rows are {resource_id,
# display_name, enabled}, and the routine block carries
# scheduled_first_seen_at, own_schedule and own_schedule_at.
---
{
  "org": {
    "id": 1,
    "name": "Example Bakery",
    "plan": "example",
    "trial_days_left": null,
    "ops_today_used": 1,
    "ops_today_cap": 40,
    "accounts_cap": 1,
    "capability": "full",
    "upgrade_url": "https://app.example.invalid/plan",
    "grace_active": false
  },
  "app_urls": {
    "accounts": "https://app.example.invalid/accounts",
    "billing": "https://app.example.invalid/plan",
    "home": "https://app.example.invalid/"
  },
  "surface": "other",
  "products": {
    "google_ads": {
      "connected": true,
      "can_edit": true,
      "needs_reauth": false,
      "unlocks": "I can read and change your campaigns, keywords and budgets.",
      "connect_url": "https://app.example.invalid/connect/google_ads",
      "accounts": [
        {
          "customer_id": "1234567890",
          "descriptive_name": "Example Bakery",
          "currency": "USD",
          "time_zone": "America/New_York",
          "manager": false,
          "enabled": true,
          "status": "ENABLED"
        }
      ]
    },
    "ga4": {
      "connected": true,
      "can_edit": true,
      "needs_reauth": false,
      "unlocks": "I can read what visitors do on the site.",
      "connect_url": "https://app.example.invalid/connect/ga4",
      "properties": [
        {
          "resource_id": "properties/987654321",
          "display_name": "Example Bakery",
          "enabled": true
        }
      ],
      "property_defaults": {
        "time_zone": "America/New_York",
        "currency_code": "USD"
      }
    },
    "search_console": {
      "connected": false,
      "can_edit": false,
      "needs_reauth": false,
      "unlocks": "I can show which searches already bring people to the site and which pages Google has indexed.",
      "connect_url": "https://app.example.invalid/connect/search_console"
    },
    "gtm": {
      "connected": false,
      "can_edit": false,
      "needs_reauth": false,
      "unlocks": "I can put the Analytics tag and conversion tags on the site without anyone editing its code.",
      "connect_url": "https://app.example.invalid/connect/gtm"
    }
  },
  "ads_probe": {
    "1234567890": {
      "name": "Example Bakery",
      "currency": "USD",
      "time_zone": "America/New_York",
      "status": "ENABLED",
      "manager": false,
      "campaigns": {
        "total": 1,
        "enabled": 1,
        "paused": 0,
        "ended": 0,
        "by_channel": {
          "SEARCH": 1
        }
      },
      "last_30d": {
        "start_date": "2026-08-25",
        "end_date": "2026-09-23",
        "cost_micros": 598000000,
        "cost_display": "$598",
        "clicks": 241,
        "impressions": 7930,
        "conversions": 14
      },
      "conversion_actions": {
        "enabled": 1,
        "primary": 1,
        "types": [
          "WEBPAGE"
        ]
      },
      "conversion_tracking_status": "CONVERSION_TRACKING_MANAGED_BY_SELF",
      "billing_setup": "APPROVED",
      "first_campaign": {
        "campaign_id": "800000001",
        "status": "ENABLED",
        "enabled_seen_at": "2026-08-23 09:12:40"
      },
      "error": null
    },
    "computed_at": "2026-09-24 12:58:00",
    "ttl_s": 600,
    "probe_status": "ok"
  },
  "profile": {
    "business_name": "Example Bakery",
    "goal": "leads",
    "website": "https://www.example-bakery.invalid",
    "budget": {
      "currency": "USD",
      "daily_comfort": 20
    },
    "service_area": {
      "type": "areas",
      "names": [
        "Brooklyn, New York"
      ]
    },
    "first_campaign": {
      "name": "Example Bakery | Search | Wedding cakes",
      "built_at": "2026-08-22",
      "campaign_id": "800000001",
      "customer_id": "1234567890",
      "enabled_seen_at": "2026-08-23 09:12:40"
    },
    "expertise": "new",
    "stage": "routine",
    "version": 3
  },
  "onboarding": {
    "stage": "routine",
    "expertise": "new",
    "activated_at": "2026-08-23 09:12:40",
    "verified": {
      "at": "2026-08-21 04:08:41",
      "ok": true,
      "error": null,
      "currency": "USD",
      "time_zone": "America/New_York",
      "accounts_read": 1
    },
    "last_session": {
      "date": "2026-09-17",
      "summary": "Read the first month; nothing changed.",
      "next_steps": []
    }
  },
  "routine": {
    "daily": {
      "org_id": 1,
      "kind": "daily",
      "status": "in_app",
      "surface": null,
      "hour_local": 9,
      "weekday": null,
      "tz": "America/New_York",
      "delivery": "email",
      "ops_cap_per_run": 8,
      "token_cap_per_run": 60000,
      "goal": null,
      "opted_in_at": "2026-09-01 09:00:00",
      "opted_in_by": "system",
      "last_run_at": "2026-09-24 13:00:04",
      "last_status": "ok",
      "skipped_count": 0,
      "customer_id": "1234567890"
    },
    "weekly": {
      "org_id": 1,
      "kind": "weekly",
      "status": "off",
      "surface": null,
      "hour_local": null,
      "weekday": null,
      "tz": null,
      "delivery": "email",
      "ops_cap_per_run": 12,
      "token_cap_per_run": 60000,
      "goal": null,
      "opted_in_at": null,
      "opted_in_by": null,
      "last_run_at": null,
      "last_status": null,
      "skipped_count": 0,
      "customer_id": null
    },
    "scheduled_last_seen_at": null,
    "scheduled_first_seen_at": null,
    "own_schedule": null,
    "own_schedule_at": null,
    "schedule": {
      "offer": "both",
      "account": "1234567890",
      "when": "8:07 AM America/New_York time",
      "instructions": "AdCopilot morning check, read-only. Call get_org_context first, with source \"claude-scheduled\". Do not use any tool that changes my account, and do not ask me questions; if something is unknown, say so and carry on. For Google Ads account 123-456-7890:\n1. Yesterday's spend, clicks, conversions and cost per conversion against my 7-day average.\n2. This month's budget pacing: on track, over or under, and any campaign limited by budget.\n3. The 5 search terms from the last 7 days that cost the most with no conversions, with their cost.\n4. Any ad that is disapproved or limited, with Google's stated reason.\n5. Any change made in the account in the last 24 hours, and by whom.\nStart with one line: \"All clear\" or \"Needs a look\". End with the single most valuable fix, written as a yes/no question I can answer when I open this.",
      "claude_request": "Schedule a task for every weekday at 8:07 AM America/New_York time with these instructions: AdCopilot morning check, read-only. Call get_org_context first, with source \"claude-scheduled\". Do not use any tool that changes my account, and do not ask me questions; if something is unknown, say so and carry on. For Google Ads account 123-456-7890:\n1. Yesterday's spend, clicks, conversions and cost per conversion against my 7-day average.\n2. This month's budget pacing: on track, over or under, and any campaign limited by budget.\n3. The 5 search terms from the last 7 days that cost the most with no conversions, with their cost.\n4. Any ad that is disapproved or limited, with Google's stated reason.\n5. Any change made in the account in the last 24 hours, and by whom.\nStart with one line: \"All clear\" or \"Needs a look\". End with the single most valuable fix, written as a yes/no question I can answer when I open this.",
      "claude_code_command": "/schedule weekdays at 8:07am America/New_York time AdCopilot morning check, read-only. Call get_org_context first, with source \"claude-scheduled\". Do not use any tool that changes my account, and do not ask me questions; if something is unknown, say so and carry on. For Google Ads account 123-456-7890:\n1. Yesterday's spend, clicks, conversions and cost per conversion against my 7-day average.\n2. This month's budget pacing: on track, over or under, and any campaign limited by budget.\n3. The 5 search terms from the last 7 days that cost the most with no conversions, with their cost.\n4. Any ad that is disapproved or limited, with Google's stated reason.\n5. Any change made in the account in the last 24 hours, and by whom.\nStart with one line: \"All clear\" or \"Needs a look\". End with the single most valuable fix, written as a yes/no question I can answer when I open this.",
      "steps": [
        "In Claude, open Customize, then Connectors, then AdCopilot, then Tool permissions. Set Read-only tools to Always allow, because a scheduled run cannot answer a prompt, and keep Write/delete tools on Needs approval, so Claude asks before each change.",
        "Add AdCopilot at claude.ai/customize/connectors first: a scheduled routine runs in the cloud and cannot see the plugin's own connector. Routines run tools without asking, so keep the instructions read-only, exactly as written.",
        "Then run it once now and check it finishes without stopping to ask."
      ]
    }
  },
  "latest_check_in": {
    "date": "2026-09-24",
    "account": "1234567890",
    "status": "ok",
    "needs_attention": 2,
    "top": [
      {
        "check_id": "G-WS1",
        "title": "Search terms spent with no conversions",
        "status": "fail"
      },
      {
        "check_id": "G-AD2",
        "title": "An ad is disapproved",
        "status": "fail"
      }
    ]
  },
  "situation": "ADS_ACTIVE_TRACKED",
  "overlays": {
    "returning": true,
    "multi_account": false,
    "manager_account": false,
    "quota_low": false,
    "read_only": false,
    "needs_reauth": [],
    "draft_waiting": false,
    "week_one": null,
    "routine_pending": true,
    "site_health": [],
    "checkin_later": false,
    "schedule_offer": "both",
    "quota_sized": false,
    "plugin_offer": null
  },
  "plugin": {
    "skill": "adcopilot-review",
    "version": "0.2.16"
  },
  "next_step": "The account is running and results are being counted; on a greeting alone, a request to get started or a question about how the ads are doing, follow the AdCopilot review steps installed in this assistant, answer anything else they asked first and then offer those steps, and suggest no bidding change in the two to three weeks after anything went live. They have been here before, so open with one line on what happened last time.",
  "playbook": "## [RAILS] Never broken\n\n1. **Call `get_org_context` first.** Follow its `next_step` and `cross_reads`; never guess a refusal's cause.\n2. **Reads run freely; every change is proposed first,** money both ways, applied only on their yes here, never unattended; if promised, add: while their AI client asks before each change (in Claude: write tools on Needs approval). Then read back only what its result does not show, say how to undo it, record it, propose the next finding's fix, until none is worth its money.\n3. **Build campaigns switched off (PAUSED).** Never call `set_campaign_status` with ENABLED on one you built: their money, their switch.\n4. **Never delete,** except a negative keyword. Pause, never REMOVED.\n5. **Only `get_org_context` says what is connected;** tools load lazily; a missing tool proves nothing: fetch it, never report a missing permission; unconnected, say what connecting unlocks, invent nothing.\n6. **Never claim what did not happen.** Say when a call failed; nothing is live until it reads switched on; never attribute to them what they did not say; never report a refusal or a limit no call returned.\n7. **Plain words:** no tool or field name, status word or account number aloud.\n\n## [RECAP] Overlay \u2014 the user is coming back\n\nOpen with two sentences: what you did together last time, and what is due\nnow, then go into the branch below. Never re-introduce yourself, re-ask what\nthe saved profile holds, or repeat the intake. A change not made last time\nis proposed again with today's numbers.\n\nIf the account moved since then \u2014 a campaign switched on, a first result, an\nad switched off by Google \u2014 that is the opening sentence.\n\n## [PLUGIN] The installed skill\n\nThe AdCopilot skill adcopilot-review, installed here, carries this situation's steps. On a greeting alone, a request to get started or the request it is for, follow it, inside the rails, with the reads `cross_reads` names. Asked anything else, answer that first with only the reads it needs, then offer it. Once their morning check is saved, record `routine.own_schedule` as `saved` with `save_org_context`. If they say not now, ask once whether their Claude can create scheduled tasks: if it cannot, record `unavailable`, else `declined`.",
  "cross_reads": {
    "mode": "situational",
    "say": "There is no unprompted read outside Google Ads to make this turn; answer what they ask from what is connected (Google Ads and Analytics).",
    "reads": [],
    "connect": [],
    "skipped": [],
    "ads_reads_max": 6,
    "exempt_ads_left": 0,
    "exempt_cross_left": {
      "ga4": 16
    },
    "cost_today": 0
  },
  "question_map": {
    "note": "The read that answers each kind of question. A lens result's related_reads names the next one from its own numbers; run the ones that bear on the question, at most three. Reads only.",
    "reads": {
      "wasted spend": "analyze_waste",
      "search terms, negatives": "analyze_search_terms",
      "keywords": "keyword_opportunities",
      "ads": "quality_score_breakdown",
      "budget": "budget_pacing",
      "results changed": "change_history",
      "tracking": "conversion_setup_audit",
      "what to do": "full_audit (depth deep)"
    }
  },
  "hints": [],
  "tools_revision": "fixture-3",
  "tools_revision_note": "Every AdCopilot tool description ends with \"Tools revision: <this value>.\" A description that shows a different revision or none is out of date: get_org_context with tools=[those tool names] returns the current text, to read before relying on those tools."
}

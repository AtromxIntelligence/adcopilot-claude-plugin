---
type: fixed
# The same fictional tenant as review-follows-related-reads (every value is
# invented), three months in: two Search campaigns, results counted, $4,318 over
# the last thirty days. Field names and nesting follow the live get_org_context
# answer.
# This is the answer to a call from a scheduled run, source "claude-scheduled":
# the scheduled task's own words carry no marker, so the skill that answers it
# has to send one. The run reads the account as the review skill does, and
# nobody is there to answer.
# The data is that case's, byte for byte, but for the two sightings the call
# itself stamps: tools_adcopilot._note_source runs before the answer is read,
# and TenantStore.mark_scheduled_seen sets a first sighting where there was
# none and moves the last, so routine.scheduled_first_seen_at (it was null) and
# routine.scheduled_last_seen_at (it was 2026-10-06) are both
# 2026-10-06 14:07:12, the moment of the call.
# Re-rendered with AdCopilot release/v2.41.0's own code (967d743b, read only):
# situation, overlays, next_step, playbook, cross_reads and question_map are
# what situations.classify, next_step, cross_reads and question_map and
# onboarding_skill.render_playbook return for this data on 2026-10-06 (UTC),
# for Claude Code (OAuth client "Claude Code (adcopilot)"), in a scheduled run
# (org_state scheduled_run true; source "claude-scheduled", which
# tools_adcopilot._plugin_marker does not read as the plugin, so no plugin
# block, and the playbook's full branch, not [PLUGIN]), with every product's
# showing already given. classify gives the source fixture's overlays
# unchanged, so tools_adcopilot._hints, which reads only the overlays and the
# data, gives its hints unchanged (none). Against that fixture only plugin
# (gone), the two sightings, next_step and playbook differ.
---
{
  "org": {
    "id": 1,
    "name": "Example Bakery",
    "plan": "example",
    "trial_days_left": null,
    "ops_today_used": 2,
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
  "surface": "claude",
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
        "total": 2,
        "enabled": 2,
        "paused": 0,
        "ended": 0,
        "by_channel": {
          "SEARCH": 2
        }
      },
      "last_30d": {
        "start_date": "2026-09-06",
        "end_date": "2026-10-05",
        "cost_micros": 4318000000,
        "cost_display": "$4,318",
        "clicks": 1948,
        "impressions": 61200,
        "conversions": 97
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
    "computed_at": "2026-10-06 08:40:00",
    "ttl_s": 600,
    "probe_status": "ok"
  },
  "profile": {
    "business_name": "Example Bakery",
    "goal": "leads",
    "website": "https://www.example-bakery.invalid",
    "budget": {
      "currency": "USD",
      "daily_comfort": 190
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
    "version": 5
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
      "date": "2026-09-28",
      "summary": "Read the month; added the birthday campaign.",
      "next_steps": []
    }
  },
  "routine": {
    "daily": {
      "org_id": 1,
      "kind": "daily",
      "status": "user_set",
      "surface": null,
      "hour_local": 9,
      "weekday": null,
      "tz": "America/New_York",
      "delivery": "email",
      "ops_cap_per_run": 8,
      "token_cap_per_run": 60000,
      "goal": null,
      "opted_in_at": "2026-09-26 09:00:00",
      "opted_in_by": "user",
      "last_run_at": "2026-10-06 13:00:03",
      "last_status": "ok",
      "skipped_count": 0,
      "customer_id": "1234567890"
    },
    "weekly": {
      "org_id": 1,
      "kind": "weekly",
      "status": "skipped",
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
    "scheduled_last_seen_at": "2026-10-06 14:07:12",
    "scheduled_first_seen_at": "2026-10-06 14:07:12",
    "own_schedule": null,
    "own_schedule_at": null
  },
  "latest_check_in": {
    "date": "2026-10-06",
    "account": "1234567890",
    "status": "needs_a_look",
    "needs_attention": 2,
    "top": [
      {
        "check_id": "W16",
        "title": "Search terms spent with no conversions",
        "status": "fail"
      },
      {
        "check_id": "S41",
        "title": "Search partners and Display are on for a Search campaign",
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
    "routine_pending": false,
    "site_health": [],
    "checkin_later": false,
    "schedule_offer": null,
    "quota_sized": false,
    "plugin_offer": null
  },
  "next_step": "The account is running and results are being counted. Read it before you answer, to say what is costing money without converting, which typed phrases to block and whether the counted conversions are real, in the account currency, then name at most three things worth acting on and end with two or three numbered choices. They have been here before, so open with one line on what happened last time.",
  "playbook": "## [RAILS] Never broken\n\n1. **Call `get_org_context` first.** Follow its `next_step` and `cross_reads`; never guess a refusal's cause.\n2. **Reads run freely; every change is proposed first,** money both ways, applied only on their yes here, never unattended; if promised, add: while their AI client asks before each change (in Claude: write tools on Needs approval). Then read back only what its result does not show, say how to undo it, record it, propose the next finding's fix, until none is worth its money.\n3. **Build campaigns switched off (PAUSED).** Never call `set_campaign_status` with ENABLED on one you built: their money, their switch.\n4. **Never delete,** except a negative keyword. Pause, never REMOVED.\n5. **Only `get_org_context` says what is connected;** tools load lazily; a missing tool proves nothing: fetch it, never report a missing permission; unconnected, say what connecting unlocks, invent nothing.\n6. **Never claim what did not happen.** Say when a call failed; nothing is live until it reads switched on; never attribute to them what they did not say; never report a refusal or a limit no call returned.\n7. **Plain words:** no tool or field name, status word or account number aloud.\n\n## [RECAP] Overlay \u2014 the user is coming back\n\nOpen with two sentences: what you did together last time, and what is due\nnow, then go into the branch below. Never re-introduce yourself, re-ask what\nthe saved profile holds, or repeat the intake. A change not made last time\nis proposed again with today's numbers.\n\nIf the account moved since then \u2014 a campaign switched on, a first result, an\nad switched off by Google \u2014 that is the opening sentence.\n\n## [ADS_ACTIVE_TRACKED] It is running and results are being counted\n\nMake the first `cross_reads.ads_reads_max` reads in Google Ads, in order, and\nwhat `cross_reads` names: all six normally, fewer on a sized day. In order:\n`full_audit` (depth deep, days 14), `search` on `campaign` by `segments.date`\n(this week against last), `analyze_search_terms`, `analyze_waste`,\n`budget_pacing`, `conversion_setup_audit`. Skip one only if its call was\nrefused, and say which.\n\nLead with the week in one line: what they spent, what they got, what a result\ncost \u2014 each against the week before. Then at most three findings, biggest money\nfirst, each with its counts.\n\nThen one recommendation, a yes-or-no proposal (rail 2).\n\nFor two to three weeks after anything went live, no bidding change but\ncapped Maximize Clicks when it gets no traffic.\n\nOptions: 1) do the first fix, 2) show me the searches we are paying for,\n3) set up the weekly summary.",
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
  "tools_revision": "fixture-4",
  "tools_revision_note": "Every AdCopilot tool description ends with \"Tools revision: <this value>.\" A description that shows a different revision or none is out of date: get_org_context with tools=[those tool names] returns the current text, to read before relying on those tools."
}

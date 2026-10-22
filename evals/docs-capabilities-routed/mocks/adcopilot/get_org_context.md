---
type: fixed
# A fictional tenant (every value is invented): returning, on a plan with no
# daily limit (pro, ops_today_cap null). One of three Search campaigns is on
# and has spent $341 over the thirty days last_30d names
# (2026-09-15..2026-10-14) on 46 clicks with nothing counted; under the
# server's 50-click line an account with a primary action and no result stays
# ADS_ACTIVE_TRACKED (situations._untracked_subcase), so the server hands it to
# the review steps.
# Search Console is connected and has not had its first showing, so cross_reads
# is a showcase that names one Search Console read. next_step, playbook and
# cross_reads are what AdCopilot release/v2.41.0 renders for this state
# (situations.next_step, onboarding_skill.render_playbook,
# situations.cross_reads, on this fixture's situation and overlays):
# plugin.skill names adcopilot-review; next_step follows the review steps on a
# greeting, a request to get started or a question about how the ads are
# doing, answers anything else first and then offers them; cross_reads says
# "On a greeting alone or a request to get started, ... make every read below"
# and "Asked anything else, answer that first with only the reads it needs,
# then offer the rest." The question is about AdCopilot itself, so the docs
# skill reads none of it as an order.
---
{
  "org": {
    "id": 1,
    "name": "Example Bakery",
    "plan": "pro",
    "trial_days_left": null,
    "ops_today_used": 2,
    "ops_today_cap": null,
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
      "connected": false,
      "can_edit": false,
      "needs_reauth": false,
      "unlocks": "I can see which clicks turned into enquiries.",
      "connect_url": "https://app.example.invalid/connect/ga4"
    },
    "search_console": {
      "connected": true,
      "can_edit": true,
      "needs_reauth": false,
      "unlocks": "I can show which searches already bring people to the site and which pages Google has indexed.",
      "connect_url": "https://app.example.invalid/connect/search_console",
      "sites": [
        {
          "resource_id": "sc-domain:example-bakery.invalid",
          "display_name": "example-bakery.invalid",
          "enabled": true
        }
      ]
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
        "total": 3,
        "enabled": 1,
        "paused": 2,
        "ended": 0,
        "by_channel": {
          "SEARCH": 3
        }
      },
      "last_30d": {
        "start_date": "2026-09-15",
        "end_date": "2026-10-14",
        "cost_micros": 341000000,
        "cost_display": "$341",
        "clicks": 46,
        "impressions": 2210,
        "conversions": 0
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
    "computed_at": "2026-10-15 08:40:00",
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
      "enabled_seen_at": "2026-09-01 08:30:00"
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
      "date": "2026-09-19",
      "summary": "Every campaign was paused; talked about which to switch on first.",
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
    "scheduled_last_seen_at": "2026-10-06"
  },
  "latest_check_in": null,
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
  "next_step": "The account is running and results are being counted; on a greeting alone, a request to get started or a question about how the ads are doing, follow the AdCopilot review steps installed in this assistant, answer anything else they asked first and then offer those steps, and suggest no bidding change in the two to three weeks after anything went live. They have been here before, so open with one line on what happened last time.",
  "playbook": "## [RAILS] Never broken\n\n1. **Call `get_org_context` first.** Follow its `next_step` and `cross_reads`; never guess a refusal's cause.\n2. **Reads run freely; every change is proposed first,** money both ways, applied only on their yes here, never unattended; if promised, add: while their AI client asks before each change (in Claude: write tools on Needs approval). Then read back only what its result does not show, say how to undo it, record it, propose the next finding's fix, until none is worth its money.\n3. **Build campaigns switched off (PAUSED).** Never call `set_campaign_status` with ENABLED on one you built: their money, their switch.\n4. **Never delete,** except a negative keyword. Pause, never REMOVED.\n5. **Only `get_org_context` says what is connected;** tools load lazily; a missing tool proves nothing: fetch it, never report a missing permission; unconnected, say what connecting unlocks, invent nothing.\n6. **Never claim what did not happen.** Say when a call failed; nothing is live until it reads switched on; never attribute to them what they did not say; never report a refusal or a limit no call returned.\n7. **Plain words:** no tool or field name, status word or account number aloud.\n\n## [RECAP] Overlay \u2014 the user is coming back\n\nOpen with two sentences: what you did together last time, and what is due\nnow, then go into the branch below. Never re-introduce yourself, re-ask what\nthe saved profile holds, or repeat the intake. A change not made last time\nis proposed again with today's numbers.\n\nIf the account moved since then \u2014 a campaign switched on, a first result, an\nad switched off by Google \u2014 that is the opening sentence.\n\n## [PLUGIN] The installed skill\n\nThe AdCopilot skill adcopilot-review, installed here, carries this situation's steps. On a greeting alone, a request to get started or the request it is for, follow it, inside the rails, with the reads `cross_reads` names. Asked anything else, answer that first with only the reads it needs, then offer it.",
  "cross_reads": {
    "mode": "showcase",
    "say": "On a greeting alone or a request to get started, this is the first look at what Search Console adds to the Google Ads answer, so make every read below \u2014 it is on us, not their daily allowance. Say which property or site you read and what each read showed, in one line each, then give the answer the Ads account alone could not. Asked anything else, answer that first with only the reads it needs, then offer the rest. They have not connected Analytics and Tag Manager. Say what each would add in ONE short line at the end: Analytics \u2014 then I can see which clicks turned into enquiries; Tag Manager \u2014 then I can put the Analytics tag and conversion tags on the site without anyone editing its code. Each takes about a minute at https://app.example.invalid/connect/ga4. Say nothing about what is in them: nothing has been read. Mention it this once and move on.",
    "reads": [
      {
        "product": "search_console",
        "tool": "gsc_search_analytics",
        "args": {
          "siteUrl": "sc-domain:example-bakery.invalid",
          "start_date": "2026-09-15",
          "end_date": "2026-10-12",
          "dimensions": [
            "query",
            "country"
          ],
          "row_limit": 50
        },
        "resource_label": "example-bakery.invalid",
        "alternatives": [],
        "answers": "What people already find the site for without paying, where it sits in those results on average, which searches it is seen for but not clicked on, which sit just off the first page, and which countries that demand comes from. These rows are the 50 with the most clicks, per search and country \u2014 not every search. Name any with impressions and no clicks, or a position past 10; if none has either, say this read shows only the most-clicked searches, never that every search gets clicked.",
        "if_empty": "No rows is not \"nobody finds the site\": a newly verified site shows nothing for weeks, and the last three days never show. Say Search Console has nothing to show yet, and never build a keyword list from silence.",
        "cost": "one look-up"
      }
    ],
    "connect": [
      {
        "product": "ga4",
        "why": "invitation",
        "connect_url": "https://app.example.invalid/connect/ga4",
        "unlocks": "I can see which clicks turned into enquiries.",
        "answers": "Analytics is not connected \u2014 then I can see which clicks turned into enquiries.",
        "say": "Analytics is not connected \u2014 then I can see which clicks turned into enquiries \u2014 about a minute at https://app.example.invalid/connect/ga4. Offer it; claim nothing about what is in it."
      },
      {
        "product": "gtm",
        "why": "invitation",
        "connect_url": "https://app.example.invalid/connect/gtm",
        "unlocks": "I can put the Analytics tag and conversion tags on the site without anyone editing its code.",
        "answers": "Tag Manager is not connected \u2014 then I can put the Analytics tag and conversion tags on the site without anyone editing its code.",
        "say": "Tag Manager is not connected \u2014 then I can put the Analytics tag and conversion tags on the site without anyone editing its code \u2014 about a minute at https://app.example.invalid/connect/gtm. Offer it; claim nothing about what is in it."
      }
    ],
    "skipped": [],
    "ads_reads_max": 6,
    "exempt_ads_left": 0,
    "exempt_cross_left": {
      "search_console": 4
    },
    "cost_today": 0
  },
  "hints": [],
  "tools_revision": "fixture-4",
  "tools_revision_note": "Every AdCopilot tool description ends with \"Tools revision: <this value>.\" A description that shows a different revision or none is out of date: get_org_context with tools=[those tool names] returns the current text, to read before relying on those tools.",
  "plugin": {
    "skill": "adcopilot-review",
    "version": "0.2.14"
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
  }
}

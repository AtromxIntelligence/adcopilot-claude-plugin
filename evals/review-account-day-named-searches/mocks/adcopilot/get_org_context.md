---
type: fixed
# A fictional tenant (every value is invented): a dental clinic in India
# (currency INR, time zone Asia/Kolkata), returning, on a plan with no daily
# limit (pro, ops_today_cap null), with two Search campaigns on and results
# counted, so the situation is ADS_ACTIVE_TRACKED and the server hands the
# account to the review steps. The conversation runs at 20:55 UTC on 13 Oct,
# which is 02:25 on 14 Oct in Bengaluru: the account's yesterday is 13 Oct and
# UTC's is 12 Oct. AdCopilot v2.41.0 (D185, #832) ends every report window on
# the account's yesterday, so last_30d names 2026-09-14..2026-10-13, and every
# lens result in this case ends on 2026-10-13. situation, overlays, plugin,
# next_step, playbook, cross_reads and question_map are what release/v2.41.0's
# own code (situations.classify, plugin_skill, next_step, cross_reads,
# question_map; onboarding_skill.render_playbook) renders for this state.
---
{
  "org": {
    "id": 1,
    "name": "Example Dental",
    "plan": "pro",
    "trial_days_left": null,
    "ops_today_used": 1,
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
          "customer_id": "4455667788",
          "descriptive_name": "Example Dental",
          "currency": "INR",
          "time_zone": "Asia/Kolkata",
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
    "4455667788": {
      "name": "Example Dental",
      "currency": "INR",
      "time_zone": "Asia/Kolkata",
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
        "start_date": "2026-09-14",
        "end_date": "2026-10-13",
        "cost_micros": 96400000000,
        "cost_display": "₹96,400",
        "clicks": 1912,
        "impressions": 48300,
        "conversions": 61.0
      },
      "conversion_actions": {
        "enabled": 2,
        "primary": 2,
        "types": [
          "WEBPAGE",
          "WEBSITE_CALL"
        ]
      },
      "conversion_tracking_status": "CONVERSION_TRACKING_MANAGED_BY_SELF",
      "billing_setup": "APPROVED",
      "first_campaign": null,
      "error": null
    },
    "computed_at": "2026-10-13 20:55:00",
    "ttl_s": 600,
    "probe_status": "ok"
  },
  "profile": {
    "business_name": "Example Dental",
    "goal": "leads",
    "website": "https://www.example-dental.invalid",
    "budget": {
      "currency": "INR",
      "daily_comfort": 3500
    },
    "service_area": {
      "type": "areas",
      "names": [
        "Bengaluru"
      ]
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
      "currency": "INR",
      "time_zone": "Asia/Kolkata",
      "accounts_read": 1
    },
    "last_session": {
      "date": "2026-10-06",
      "summary": "Read the two campaigns; nothing changed.",
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
      "tz": "Asia/Kolkata",
      "delivery": "email",
      "ops_cap_per_run": 8,
      "token_cap_per_run": 60000,
      "goal": null,
      "opted_in_at": "2026-09-26 09:00:00",
      "opted_in_by": "user",
      "last_run_at": "2026-10-06 13:00:03",
      "last_status": "ok",
      "skipped_count": 0,
      "customer_id": "4455667788"
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
    "plugin_offer": "claude_code"
  },
  "next_step": "The account is running and results are being counted; on a greeting alone, a request to get started or a question about how the ads are doing, follow the AdCopilot review steps installed in this assistant, answer anything else they asked first and then offer those steps, and suggest no bidding change in the two to three weeks after anything went live. They have been here before, so open with one line on what happened last time.",
  "playbook": "## [RAILS] Never broken\n\n1. **Call `get_org_context` first.** Follow its `next_step` and `cross_reads`; never guess a refusal's cause.\n2. **Reads run freely; every change is proposed first,** money both ways, applied only on their yes here, never unattended; if promised, add: while their AI client asks before each change (in Claude: write tools on Needs approval). Then read back only what its result does not show, say how to undo it, record it, propose the next finding's fix, until none is worth its money.\n3. **Build campaigns switched off (PAUSED).** Never call `set_campaign_status` with ENABLED on one you built: their money, their switch.\n4. **Never delete,** except a negative keyword. Pause, never REMOVED.\n5. **Only `get_org_context` says what is connected;** tools load lazily; a missing tool proves nothing: fetch it, never report a missing permission; unconnected, say what connecting unlocks, invent nothing.\n6. **Never claim what did not happen.** Say when a call failed; nothing is live until it reads switched on; never attribute to them what they did not say; never report a refusal or a limit no call returned.\n7. **Plain words:** no tool or field name, status word or account number aloud.\n\n## [RECAP] Overlay — the user is coming back\n\nOpen with two sentences: what you did together last time, and what is due\nnow, then go into the branch below. Never re-introduce yourself, re-ask what\nthe saved profile holds, or repeat the intake. A change not made last time\nis proposed again with today's numbers.\n\nIf the account moved since then — a campaign switched on, a first result, an\nad switched off by Google — that is the opening sentence.\n\n## [PLUGIN] The installed skill\n\nThe AdCopilot skill adcopilot-review, installed here, carries this situation's steps. On a greeting alone, a request to get started or the request it is for, follow it, inside the rails, with the reads `cross_reads` names. Asked anything else, answer that first with only the reads it needs, then offer it.",
  "cross_reads": {
    "mode": "situational",
    "say": "Nothing outside Google Ads can be read this turn, so there is no cross-product read to make.",
    "reads": [],
    "connect": [],
    "skipped": [],
    "ads_reads_max": 6,
    "exempt_ads_left": 0,
    "exempt_cross_left": {},
    "cost_today": 0
  },
  "hints": [
    "Results came in on 13 Oct, the account's yesterday."
  ],
  "tools_revision": "fixture-4",
  "tools_revision_note": "Every AdCopilot tool description ends with \"Tools revision: <this value>.\" A description that shows a different revision or none is out of date: get_org_context with tools=[those tool names] returns the current text, to read before relying on those tools.",
  "plugin": {
    "skill": "adcopilot-review",
    "version": "0.2.12"
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

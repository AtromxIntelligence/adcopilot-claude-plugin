---
type: fixed
# The fictional tenant from evals/mocks, the day after its first campaign was
# built and left paused, with nothing on the site counted yet: a property
# exists, Tag Manager is connected with one container, and the ad account has
# no conversion actions. The saved profile already says what to count and
# where on the site it happens, so the arc's first question is answered and a
# run can go on to the stream and the tags; which stream, tags and events
# exist has to be read back from Analytics and Tag Manager.
# The field names and nesting follow the shape of a real get_org_context answer,
# read live on 2026-09-23 — org with its flat caps, app_urls, products keyed by
# slug, the per-account ads_probe block, profile and onboarding (where the stage
# lives), routine, overlays, cross_reads as an object carrying the read cap
# (ads_reads_max), hints, playbook as one string — and every value is invented.
# Re-rendered with AdCopilot release/v2.41.0's own code (967d743b, read only):
# situation (ADS_DORMANT), overlays, plugin, next_step, playbook, cross_reads,
# question_map and hints are what situations.classify, plugin_skill, next_step
# and cross_reads, onboarding_skill.render_playbook, schedule_recipe.as_data
# and tools_adcopilot._hints return for this data on 2026-09-23 (UTC), for
# Claude Code (OAuth client "Claude Code (adcopilot)"), carrying the plugin
# marker claude-plugin/0.2.15, with every product's showing already given. The
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
    "ops_today_used": 3,
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
      "connected": true,
      "can_edit": true,
      "needs_reauth": false,
      "unlocks": "I can put the Analytics tag and conversion tags on the site without anyone editing its code.",
      "connect_url": "https://app.example.invalid/connect/gtm",
      "containers": [
        {
          "resource_id": "accounts/6000100200/containers/30040050",
          "display_name": "Example Bakery website",
          "enabled": true
        }
      ]
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
        "enabled": 0,
        "paused": 1,
        "ended": 0,
        "by_channel": {
          "SEARCH": 1
        }
      },
      "last_30d": {
        "start_date": "2026-08-24",
        "end_date": "2026-09-22",
        "cost_micros": 0,
        "cost_display": "$0",
        "clicks": 0,
        "impressions": 0,
        "conversions": 0
      },
      "conversion_actions": {
        "enabled": 0,
        "primary": 0,
        "types": []
      },
      "conversion_tracking_status": "NOT_CONVERSION_TRACKED",
      "billing_setup": "APPROVED",
      "first_campaign": {
        "campaign_id": "800000001",
        "status": "PAUSED",
        "enabled_seen_at": null
      },
      "error": null
    },
    "computed_at": "2026-09-23 09:00:00",
    "ttl_s": 600,
    "probe_status": "ok"
  },
  "profile": {
    "business_name": "Example Bakery",
    "goal": "leads",
    "website": "https://www.example-bakery.invalid",
    "landing_url": "https://www.example-bakery.invalid/wedding-cakes",
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
    "never_show_for": [
      "free",
      "jobs",
      "recipe"
    ],
    "first_campaign": {
      "name": "Example Bakery | Search | Wedding cakes",
      "built_at": "2026-09-22",
      "campaign_id": "800000001",
      "customer_id": "1234567890"
    },
    "last_session": {
      "date": "2026-09-22",
      "summary": "First campaign built and left paused. Nothing on the site is counted yet. The result to count is a sign-up to the tasting list: the form on the wedding-cakes page sends people to https://www.example-bakery.invalid/tasting-list/thanks when it is submitted. The customer wants that counted before switching the campaign on."
    },
    "expertise": "new",
    "stage": "first_build",
    "version": 1
  },
  "onboarding": {
    "stage": "first_build",
    "expertise": "new",
    "activated_at": "2026-09-20 21:49:25",
    "verified": {
      "at": "2026-09-21 04:08:41",
      "ok": true,
      "error": null,
      "currency": "USD",
      "time_zone": "America/New_York",
      "accounts_read": 1
    },
    "last_session": {
      "date": "2026-09-22",
      "summary": "First campaign built and left paused. Nothing on the site is counted yet. The result to count is a sign-up to the tasting list: the form on the wedding-cakes page sends people to https://www.example-bakery.invalid/tasting-list/thanks when it is submitted. The customer wants that counted before switching the campaign on."
    }
  },
  "routine": {
    "daily": {
      "org_id": 1,
      "kind": "daily",
      "status": "off",
      "surface": null,
      "hour_local": null,
      "weekday": null,
      "tz": null,
      "delivery": "email",
      "ops_cap_per_run": 8,
      "token_cap_per_run": 60000,
      "goal": null,
      "opted_in_at": null,
      "opted_in_by": null,
      "last_run_at": null,
      "last_status": null,
      "skipped_count": 0
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
      "skipped_count": 0
    },
    "scheduled_first_seen_at": null,
    "scheduled_last_seen_at": null,
    "own_schedule": null,
    "own_schedule_at": null
  },
  "situation": "ADS_DORMANT",
  "overlays": {
    "returning": true,
    "multi_account": false,
    "manager_account": false,
    "quota_low": false,
    "read_only": false,
    "needs_reauth": [],
    "draft_waiting": true,
    "week_one": null,
    "routine_pending": true,
    "site_health": [],
    "checkin_later": false,
    "schedule_offer": null,
    "quota_sized": false,
    "plugin_offer": null
  },
  "plugin": {
    "skill": null,
    "version": "0.2.15"
  },
  "next_step": "Nothing is spending at the moment. Read when it last ran, what changed and who changed it, and what a restart would take, then say what the account did before and why it stopped, ask whether they want to restart what is there or start something new, and give them two or three numbered choices. Their first campaign is built and still switched off, so walk them through switching it on themselves and never do it for them. Before you finish, offer to set up a daily check-in and a Monday summary.",
  "playbook": "## [RAILS] Never broken\n\n1. **Call `get_org_context` first.** Follow its `next_step` and `cross_reads`; never guess a refusal's cause.\n2. **Reads run freely; every change is proposed first,** money both ways, applied only on their yes here, never unattended; if promised, add: while their AI client asks before each change (in Claude: write tools on Needs approval). Then read back only what its result does not show, say how to undo it, record it, propose the next finding's fix, until none is worth its money.\n3. **Build campaigns switched off (PAUSED).** Never call `set_campaign_status` with ENABLED on one you built: their money, their switch.\n4. **Never delete,** except a negative keyword. Pause, never REMOVED.\n5. **Only `get_org_context` says what is connected;** tools load lazily; a missing tool proves nothing: fetch it, never report a missing permission; unconnected, say what connecting unlocks, invent nothing.\n6. **Never claim what did not happen.** Say when a call failed; nothing is live until it reads switched on; never attribute to them what they did not say; never report a refusal or a limit no call returned.\n7. **Plain words:** no tool or field name, status word or account number aloud.\n\n## [ADS_DORMANT] Nothing is spending right now\n\nMake the first `cross_reads.ads_reads_max` reads in Google Ads, in order, and\nwhat `cross_reads` names: all three, fewer on a sized day: `change_history`,\nthen `search` on `campaign` by `segments.date` and for status, budget, end\ndate. Skip only if refused.\n\n**Already held:** what is counted, what Google aims for, who set it up. Not\ncounting at all means nothing is set up to count. None aimed for: Google aims at\nnothing. Counted and aimed for: counting **is** set up. Never answer \"I cannot\ntell\"; never say you need permission to look.\n\nSay if it has **never** run or **ran until** a month, and why if shown. Ran before: what it was, cost, got; ask: as it was or rebuilt? Restarting\nis theirs to ask. Never ran: intake, build.\n\nOptions: 1) start as it was, 2) rebuild, 3) leave it off, with cost.\n\n## Go-live walkthrough\n\nThe switch itself. Re-shown every session the draft is waiting, and on\n`step=\"go-live\"`.\n\n\"Google Ads \u2192 Campaigns \u2192 find {name} \u2192 click the grey **Paused** dot in the\nstatus column \u2192 **Enabled**.\" On a phone: \"Campaigns \u2192 {name} \u2192 the status switch\nat the top.\"\nThen the money sentence: \"From then on it can spend up to {daily} a day\n({double} on a busy day, never more than {monthly} in a month). To stop it: the\nsame switch, back to Paused \u2014 nothing is lost.\"\nThen the rule, said once:\n\"I won't press that switch for you \u2014 it's your money, so it's your switch. If you ask me to, I'll show you these steps again.\"\n\nThen hand over to week one, writing that list into `last_session.next_steps`\nwith `save_org_context`.\n\n## THE CLOSE\n\nFour questions, asked here only, one at a time.\n\n- **R1** \u2014 \"Want a short daily check-in?\" (yes / weekly is enough / not now)\n- **R2** \u2014 \"Where should it land?\" \u2014 offer their surface's recipe. If\n  `routine.daily.status` is `in_app` and `routine.runner` is not `paused`,\n  AdCopilot emails it daily (Recipe C): say so, record nothing for it.\n- **R3** \u2014 \"What time?\" \u2014 default 08:00, their time.\n- **R4** \u2014 \"And a summary of the week every Monday?\"\n\nRecord every answer with `save_org_context` as you go, then set the stage.\n\n(Trimmed to fit. The rest of the playbook \u2014 the questions, the build sequence and the safety rules \u2014 is the get-started prompt; ask for it by name.)",
  "cross_reads": {
    "mode": "situational",
    "say": "Before you say you cannot tell whether the campaign failed or the counting was never wired: read what Analytics already counts as a result. One read, then stop.",
    "reads": [
      {
        "product": "ga4",
        "tool": "ga4_list_conversion_events",
        "args": {
          "property": "properties/987654321"
        },
        "resource_label": "Example Bakery",
        "alternatives": [],
        "answers": "Whether anything on the site is set up to count a result at all.",
        "if_empty": "An empty list is not yet \"nothing was ever set up\": check the site is sending data first, and leave the question open.",
        "cost": "one look-up"
      }
    ],
    "connect": [],
    "skipped": [],
    "ads_reads_max": 3,
    "exempt_ads_left": 0,
    "exempt_cross_left": {
      "ga4": 16,
      "gtm": 4
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
  "tools_revision": "fixture-1",
  "tools_revision_note": "Every AdCopilot tool description ends with \"Tools revision: <this value>.\" A description that shows a different revision or none is out of date: get_org_context with tools=[those tool names] returns the current text, to read before relying on those tools."
}

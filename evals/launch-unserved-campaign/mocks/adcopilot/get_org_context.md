---
type: fixed
# The fictional tenant from evals/mocks, on day two after the customer
# switched its first campaign on. The probe's numbers say ninety impressions
# and nothing spent; what that means has to be read from the campaign itself.
# The read cap for a week-one check-in is two reads in Google Ads.
# The field names and nesting follow the shape of a real get_org_context answer,
# read live on 2026-09-23 — org with its flat caps, app_urls, products keyed by
# slug, the per-account ads_probe block, profile and onboarding (where the stage
# lives), routine, overlays, cross_reads as an object carrying the read cap
# (ads_reads_max), hints, playbook as one string — and every value is invented.
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
          "property": "properties/987654321",
          "display_name": "Example Bakery",
          "time_zone": "America/New_York",
          "currency_code": "USD"
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
        "cost_display": "$0",
        "clicks": 0,
        "impressions": 90,
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
        "status": "ENABLED",
        "enabled_seen_at": "2026-09-21 18:02:11"
      }
    }
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
      "built_at": "2026-09-20",
      "campaign_id": "800000001",
      "customer_id": "1234567890"
    },
    "last_session": {
      "date": "2026-09-21",
      "summary": "Hand-off done: Search partners off, Display off, Presence, broad-match auto-apply paused with the customer's yes. The customer switched the campaign on themselves on 2026-09-21."
    },
    "expertise": "new",
    "stage": "first_enable",
    "version": 1
  },
  "onboarding": {
    "stage": "first_enable",
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
      "date": "2026-09-21",
      "summary": "Hand-off done: Search partners off, Display off, Presence, broad-match auto-apply paused with the customer's yes. The customer switched the campaign on themselves on 2026-09-21."
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
    }
  },
  "situation": "ads_live_week_one",
  "overlays": {
    "returning": true,
    "multi_account": false,
    "manager_account": false,
    "quota_low": false,
    "read_only": false,
    "needs_reauth": [],
    "focus": null,
    "draft_waiting": false,
    "week_one": {
      "day": 2
    },
    "routine_pending": true
  },
  "next_step": "The first campaign is switched on. They are on day 2 of the first fortnight since it went live; keep this short and expect thin numbers.",
  "playbook": "[RAILS] Reads are free. Propose every change and apply it only after a yes. Say nothing you did not read. No account numbers in what you say. New campaigns are built paused and the customer switches them on in Google Ads themselves.\n\nWeek one: at each check-in, read what the campaign actually did and say it plainly before anything else.",
  "cross_reads": {
    "mode": "situational",
    "say": "Nothing outside Google Ads would change the advice in this situation, so make no cross-product read.",
    "reads": [],
    "connect": [],
    "skipped": [],
    "ads_reads_max": 2,
    "exempt_ads_left": 0,
    "exempt_cross_left": {
      "ga4": 0,
      "search_console": 0,
      "gtm": 0
    },
    "cost_today": 0
  },
  "hints": [
    "Day 2 of week one: read what the campaign did before anything else."
  ],
  "tools_revision": "fixture-1",
  "tools_revision_note": "Every AdCopilot tool description ends with \"Tools revision: <this value>.\" A description that shows a different revision or none is out of date: get_org_context with tools=[those tool names] returns the current text, to read before relying on those tools."
}

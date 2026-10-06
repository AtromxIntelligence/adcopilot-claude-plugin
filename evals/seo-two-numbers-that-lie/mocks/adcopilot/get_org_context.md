---
type: fixed
# The same fictional tenant with Search Console connected and healthy; every
# value is invented. The situation is ADS_ACTIVE_TRACKED because the ads are
# running, so cross_reads carries this account's real answer for an ADS
# question - "make no cross-product read", search_console allowance zero,
# read live on 2026-10-06 - and
# the customer's question here is not an ads question. Reading that ceiling as
# a refusal to open Search Console is the trap: the skill says cross_reads
# budgets reads made outside Google Ads in service of an ADS answer, and does
# not cap the skill whose subject IS organic search.
# The playbook's ads block carries six reads and names the lenses, which is
# what adcopilot#658 introduces; the live server still says four and names
# none. It is not what this case measures either way - the question is not an
# ads question - and the same fixture serves both cases.
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
      "connected": true,
      "can_edit": true,
      "needs_reauth": false,
      "unlocks": "I can show which searches already bring people to the site and which pages Google has indexed.",
      "connect_url": "https://app.example.invalid/connect/search_console",
      "sites": [
        {
          "siteUrl": "sc-domain:example-bakery.invalid",
          "permissionLevel": "siteOwner"
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
        "total": 2,
        "enabled": 2,
        "paused": 0,
        "ended": 0,
        "by_channel": {
          "SEARCH": 2
        }
      },
      "last_30d": {
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
      "customer_id": "1234567890"
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
      "status": "user_set",
      "surface": null,
      "hour_local": 9,
      "weekday": null,
      "tz": "America/New_York",
      "delivery": "email",
      "ops_cap_per_run": 8,
      "token_cap_per_run": 60000,
      "goal": null,
      "opted_in_at": "2026-09-01 09:00:00",
      "opted_in_by": "user",
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
    "scheduled_last_seen_at": "2026-10-06"
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
    "focus": null,
    "draft_waiting": false,
    "routine_pending": false
  },
  "next_step": "Both campaigns are running and results are being counted. Read what they did before proposing anything.",
  "playbook": "[RAILS] Reads are free. Propose every change and apply it only after a yes. Say nothing you did not read. No account numbers in what you say.\n\nUp to six reads in Google Ads, plus what `cross_reads` names. Open with `full_audit`, then `analyze_search_terms` or `analyze_waste` as its findings point: one lens is ONE read and answers what a dozen queries would.\n\nLead with the week in one line: what they spent, what they got, what a result cost \u2014 each against the week before. Then at most three findings, biggest money first, each with the counts behind it.",
  "cross_reads": {
    "mode": "situational",
    "say": "Nothing outside Google Ads would change the advice in this situation, so make no cross-product read.",
    "reads": [],
    "connect": [],
    "skipped": [],
    "ads_reads_max": 6,
    "exempt_ads_left": 0,
    "exempt_cross_left": {
      "ga4": 0,
      "search_console": 0,
      "gtm": 0
    },
    "cost_today": 0
  },
  "hints": [
    "Both campaigns have been running a month; read what they did before proposing anything."
  ],
  "tools_revision": "fixture-4",
  "tools_revision_note": "Every AdCopilot tool description ends with \"Tools revision: <this value>.\" A description that shows a different revision or none is out of date: get_org_context with tools=[those tool names] returns the current text, to read before relying on those tools."
}

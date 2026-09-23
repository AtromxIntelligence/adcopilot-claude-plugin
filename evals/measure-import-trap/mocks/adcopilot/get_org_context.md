---
type: fixed
# The same fictional tenant as evals/mocks, later in its life: a property
# exists, Tag Manager is connected with one container, one campaign runs and
# the account has conversion tracking. The probe reports how many actions are
# Primary but not which: that has to be read back from Google Ads.
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
      "connected": true,
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
          "display_name": "Example Bakery website"
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
        "enabled": 1,
        "paused": 0,
        "ended": 0,
        "by_channel": {
          "SEARCH": 1
        }
      },
      "last_30d": {
        "cost_display": "$412",
        "clicks": 187,
        "impressions": 6120,
        "conversions": 44
      },
      "conversion_actions": {
        "enabled": 5,
        "primary": 5,
        "types": [
          "GOOGLE_ANALYTICS_4_CUSTOM"
        ]
      },
      "conversion_tracking_status": "CONVERSION_TRACKING_MANAGED_BY_SELF",
      "billing_setup": "APPROVED",
      "first_campaign": {
        "campaign_id": "800000001",
        "status": "ENABLED",
        "enabled_seen_at": "2026-09-01 09:12:40"
      },
      "error": null
    },
    "computed_at": "2026-09-22 09:00:00",
    "ttl_s": 600,
    "probe_status": "ok"
  },
  "profile": {
    "stage": "first_enable",
    "expertise": "new",
    "version": 1,
    "field_sources": {}
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
    "last_session": null
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
  "situation": "conversion_tracking_on",
  "overlays": {
    "returning": false,
    "multi_account": false,
    "manager_account": false,
    "quota_low": false,
    "read_only": false,
    "needs_reauth": [],
    "focus": null,
    "draft_waiting": false,
    "routine_pending": true
  },
  "next_step": "Google Ads reports conversion tracking on this account.",
  "playbook": "[RAILS] Reads are free. Propose every change and apply it only after a yes. Say nothing you did not read. No account numbers in what you say.\n\nReport the situation in plain language before proposing anything.",
  "cross_reads": {
    "mode": "situational",
    "say": "Analytics and Tag Manager are connected; reads there are free.",
    "reads": [],
    "connect": [],
    "skipped": [],
    "ads_reads_max": 4,
    "exempt_ads_left": 0,
    "exempt_cross_left": {
      "ga4": 0,
      "search_console": 0,
      "gtm": 0
    },
    "cost_today": 0
  },
  "hints": [],
  "tools_revision": "fixture-1",
  "tools_revision_note": "Every AdCopilot tool description ends with \"Tools revision: <this value>.\" A description that shows a different revision or none is out of date: get_org_context with tools=[those tool names] returns the current text, to read before relying on those tools."
}

---
type: fixed
# The same fictional tenant as evals/mocks, later in its life: a property
# exists, Tag Manager is connected with one container, one campaign runs and
# the account has conversion tracking. The field names and nesting follow the
# shape of a real get_org_context answer — the per-account ads_probe block,
# conversion_tracking_status, containers by display name, playbook as one
# string — and every value is invented. The probe reports how many actions
# are Primary but not which: that has to be read back from Google Ads.
---
{
  "org": {
    "name": "Example Bakery",
    "plan": "example",
    "caps": { "google_ads_accounts": 1, "campaigns": 3 },
    "upgrade_url": "https://app.example.invalid/plan"
  },
  "stage": "first_enable",
  "situation": "conversion_tracking_on",
  "next_step": "Google Ads reports conversion tracking on this account.",
  "playbook": "[RAILS] Reads are free. Propose every change and apply it only after a yes. Say nothing you did not read. No account numbers in what you say.\n\nReport the situation in plain language before proposing anything.",
  "cross_reads": [],
  "products": {
    "google_ads": {
      "connected": true,
      "can_edit": true,
      "needs_reauth": false,
      "unlocks": "I can read and change your campaigns, keywords and budgets.",
      "connect_url": "https://app.example.invalid/connect/google_ads",
      "accounts": [
        { "customer_id": "1234567890", "descriptive_name": "Example Bakery", "currency": "USD", "time_zone": "America/New_York", "manager": false, "enabled": true, "status": "ENABLED" }
      ]
    },
    "ga4": {
      "connected": true,
      "can_edit": true,
      "needs_reauth": false,
      "unlocks": "I can read what visitors do on the site.",
      "connect_url": "https://app.example.invalid/connect/ga4",
      "properties": [
        { "property": "properties/987654321", "display_name": "Example Bakery", "time_zone": "America/New_York", "currency_code": "USD" }
      ],
      "property_defaults": { "time_zone": "America/New_York", "currency_code": "USD" }
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
        { "resource_id": "accounts/6000100200/containers/30040050", "display_name": "Example Bakery website" }
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
      "campaigns": { "total": 1, "enabled": 1, "paused": 0, "ended": 0, "by_channel": { "SEARCH": 1 } },
      "last_30d": { "cost_display": "$412", "clicks": 187, "impressions": 6120, "conversions": 44 },
      "conversion_actions": { "enabled": 5, "primary": 5, "types": ["GOOGLE_ANALYTICS_4_CUSTOM"] },
      "conversion_tracking_status": "CONVERSION_TRACKING_MANAGED_BY_SELF",
      "billing_setup": "APPROVED",
      "first_campaign": { "campaign_id": "800000001", "status": "ENABLED", "enabled_seen_at": "2026-09-01 09:12:40" },
      "error": null
    },
    "computed_at": "2026-09-22 09:00:00",
    "ttl_s": 600,
    "probe_status": "ok"
  },
  "overlays": {
    "needs_reauth": []
  },
  "app_urls": {
    "connections": "https://app.example.invalid/connections",
    "upgrade": "https://app.example.invalid/plan"
  },
  "tools_revision": "fixture-1"
}

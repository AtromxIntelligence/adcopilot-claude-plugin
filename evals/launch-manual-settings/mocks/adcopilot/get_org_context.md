---
type: fixed
# The fictional tenant from evals/mocks, the day after its first campaign was
# built through the connector: one Search campaign, paused, never switched on.
# The field names and nesting follow the shape of a real get_org_context
# answer — the per-account ads_probe block with its campaign counts, billing
# setup and first_campaign, the saved profile with the budget the customer
# named — and every value is invented. The answer says a campaign exists and
# is paused; whether its settings are right has to be read back from Google
# Ads, and so does what is auto-applied.
---
{
  "org": {
    "name": "Example Bakery",
    "plan": "example",
    "caps": { "google_ads_accounts": 1, "campaigns": 3 },
    "upgrade_url": "https://app.example.invalid/plan"
  },
  "stage": "first_build",
  "situation": "first_campaign_built",
  "next_step": "The first campaign exists and is paused. It has not been switched on; that is the customer's click in Google Ads.",
  "playbook": "[RAILS] Reads are free. Propose every change and apply it only after a yes. Say nothing you did not read. No account numbers in what you say. New campaigns are built paused and the customer switches them on in Google Ads themselves.\n\nReport the situation in plain language before proposing anything.",
  "cross_reads": [],
  "products": {
    "google_ads": {
      "connected": true,
      "can_edit": true,
      "needs_reauth": false,
      "unlocks": "I can read and change your campaigns, keywords and budgets.",
      "connect_url": "https://app.example.invalid/connect/google_ads",
      "accounts": [
        { "customer_id": "1234567890", "name": "Example Bakery", "currency": "USD", "time_zone": "America/New_York" }
      ],
      "campaigns": 1,
      "conversion_tracking_status": "none"
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
      "campaigns": { "total": 1, "enabled": 0, "paused": 1, "ended": 0, "by_channel": { "SEARCH": 1 } },
      "last_30d": { "cost_display": "$0", "clicks": 0, "impressions": 0, "conversions": 0 },
      "conversion_actions": { "enabled": 0, "primary": 0, "types": [] },
      "billing_setup": "APPROVED",
      "first_campaign": { "campaign_id": "800000001", "status": "PAUSED", "enabled_seen_at": null }
    }
  },
  "profile": {
    "business_name": "Example Bakery",
    "goal": "leads",
    "website": "https://www.example-bakery.invalid",
    "landing_url": "https://www.example-bakery.invalid/wedding-cakes",
    "budget": { "currency": "USD", "daily_comfort": 20 },
    "service_area": { "type": "areas", "names": ["Brooklyn, New York"] },
    "never_show_for": ["free", "jobs", "recipe"],
    "first_campaign": { "name": "Example Bakery | Search | Wedding cakes", "built_at": "2026-09-22", "campaign_id": "800000001", "customer_id": "1234567890" },
    "expertise": "new"
  },
  "overlays": {
    "needs_reauth": [],
    "returning": true
  },
  "app_urls": {
    "connections": "https://app.example.invalid/connections",
    "upgrade": "https://app.example.invalid/plan"
  },
  "tools_revision": "fixture-1"
}

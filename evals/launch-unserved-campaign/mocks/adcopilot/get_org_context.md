---
type: fixed
# The fictional tenant from evals/mocks, on day two after the customer
# switched its first campaign on. The field names and nesting follow the shape
# of a real get_org_context answer — the per-account ads_probe block with its
# thirty-day numbers, billing setup and first_campaign, the week_one overlay,
# the saved profile — and every value is invented. The probe's numbers say
# ninety impressions and nothing spent; what that means has to be read from
# the campaign itself.
---
{
  "org": {
    "name": "Example Bakery",
    "plan": "example",
    "caps": { "google_ads_accounts": 1, "campaigns": 3 },
    "upgrade_url": "https://app.example.invalid/plan"
  },
  "stage": "first_enable",
  "situation": "ads_live_week_one",
  "next_step": "The first campaign is switched on. They are on day 2 of the first fortnight since it went live; keep this short and expect thin numbers.",
  "playbook": "[RAILS] Reads are free. Propose every change and apply it only after a yes. Say nothing you did not read. No account numbers in what you say. New campaigns are built paused and the customer switches them on in Google Ads themselves.\n\nWeek one: at each check-in, read what the campaign actually did and say it plainly before anything else.",
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
      "campaigns": { "total": 1, "enabled": 1, "paused": 0, "ended": 0, "by_channel": { "SEARCH": 1 } },
      "last_30d": { "cost_display": "$0", "clicks": 0, "impressions": 90, "conversions": 0 },
      "conversion_actions": { "enabled": 0, "primary": 0, "types": [] },
      "conversion_tracking_status": "NOT_CONVERSION_TRACKED",
      "billing_setup": "APPROVED",
      "first_campaign": { "campaign_id": "800000001", "status": "ENABLED", "enabled_seen_at": "2026-09-21 18:02:11" }
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
    "first_campaign": { "name": "Example Bakery | Search | Wedding cakes", "built_at": "2026-09-20", "campaign_id": "800000001", "customer_id": "1234567890" },
    "last_session": { "date": "2026-09-21", "summary": "Hand-off done: Search partners off, Display off, Presence, broad-match auto-apply paused with the customer's yes. The customer switched the campaign on themselves on 2026-09-21." },
    "expertise": "new"
  },
  "overlays": {
    "needs_reauth": [],
    "returning": true,
    "week_one": { "day": 2 }
  },
  "app_urls": {
    "connections": "https://app.example.invalid/connections",
    "upgrade": "https://app.example.invalid/plan"
  },
  "tools_revision": "fixture-1"
}

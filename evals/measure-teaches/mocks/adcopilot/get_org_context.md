---
type: fixed
# The fictional tenant from evals/mocks, the day after its first campaign was
# built and left paused, with nothing on the site counted yet: a property
# exists, Tag Manager is connected with one container, and the ad account has
# no conversion actions. The field names and nesting follow the shape of a
# real get_org_context answer — the per-account ads_probe block, which is
# where conversion_tracking_status lives, containers by display name, the
# saved profile, playbook as one string — and every value is invented. The
# saved profile already says what to count and where on the site it happens,
# so the arc's first question is answered and a run can go on to the stream
# and the tags; which stream, tags and events exist has to be read back from
# Analytics and Tag Manager.
---
{
  "org": {
    "name": "Example Bakery",
    "plan": "example",
    "caps": { "google_ads_accounts": 1, "campaigns": 3 },
    "upgrade_url": "https://app.example.invalid/plan"
  },
  "surface": "claude",
  "stage": "first_build",
  "situation": "nothing_counted_yet",
  "next_step": "The first campaign exists and is paused. Nothing on the site is counted as a result yet, so the campaign has nothing to aim for once it is switched on.",
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
      "connected": true,
      "can_edit": true,
      "needs_reauth": false,
      "unlocks": "I can put the Analytics tag and conversion tags on the site without anyone editing its code.",
      "connect_url": "https://app.example.invalid/connect/gtm",
      "containers": [
        { "resource_id": "accounts/6000100200/containers/30040050", "display_name": "Example Bakery website", "enabled": true }
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
      "campaigns": { "total": 1, "enabled": 0, "paused": 1, "ended": 0, "by_channel": { "SEARCH": 1 } },
      "last_30d": { "cost_display": "$0", "clicks": 0, "impressions": 0, "conversions": 0 },
      "conversion_actions": { "enabled": 0, "primary": 0, "types": [] },
      "conversion_tracking_status": "NOT_CONVERSION_TRACKED",
      "billing_setup": "APPROVED",
      "first_campaign": { "campaign_id": "800000001", "status": "PAUSED", "enabled_seen_at": null },
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
    "budget": { "currency": "USD", "daily_comfort": 20 },
    "service_area": { "type": "areas", "names": ["Brooklyn, New York"] },
    "never_show_for": ["free", "jobs", "recipe"],
    "first_campaign": { "name": "Example Bakery | Search | Wedding cakes", "built_at": "2026-09-22", "campaign_id": "800000001", "customer_id": "1234567890" },
    "last_session": { "date": "2026-09-22", "summary": "First campaign built and left paused. Nothing on the site is counted yet. The result to count is a sign-up to the tasting list: the form on the wedding-cakes page sends people to https://www.example-bakery.invalid/tasting-list/thanks when it is submitted. The customer wants that counted before switching the campaign on." },
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

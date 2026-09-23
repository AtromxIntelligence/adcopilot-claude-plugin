---
type: fixed
# A fictional tenant for this eval suite. The field names and nesting follow
# the shape of a real get_org_context answer — products keyed by slug with
# connect_url, needs_reauth, can_edit and unlocks; accounts with a
# descriptive_name; the per-account ads_probe block, which is where the
# campaign counts and conversion_tracking_status live; playbook as one string
# — and every value is invented. Nothing here says which products AdCopilot
# supports, and "lantern" is not a product that exists: the unknown-product
# case checks that the skill describes it from this text alone, with nothing
# but its key and its own description to go on.
---
{
  "org": {
    "name": "Example Bakery",
    "plan": "example",
    "caps": { "google_ads_accounts": 1, "campaigns": 3 },
    "upgrade_url": "https://app.example.invalid/plan"
  },
  "surface": "claude",
  "stage": "new",
  "situation": "ga4_no_property",
  "next_step": "Analytics is connected but has no property yet.",
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
      "properties": [],
      "empty": true,
      "property_defaults": { "time_zone": "America/New_York", "currency_code": "USD" }
    },
    "search_console": {
      "connected": true,
      "can_edit": false,
      "needs_reauth": true,
      "unlocks": "I can show which searches already bring people to the site and which pages Google has indexed.",
      "connect_url": "https://app.example.invalid/connect/search_console"
    },
    "gtm": {
      "connected": false,
      "can_edit": false,
      "needs_reauth": false,
      "unlocks": "I can put the Analytics tag and conversion tags on the site without anyone editing its code.",
      "connect_url": "https://app.example.invalid/connect/gtm"
    },
    "lantern": {
      "connected": false,
      "can_edit": false,
      "needs_reauth": false,
      "unlocks": "I can report which product pages shoppers read before they later search for the brand, and turn those pages into audiences a campaign can target.",
      "connect_url": "https://app.example.invalid/connect/lantern"
    }
  },
  "ads_probe": {
    "1234567890": {
      "name": "Example Bakery",
      "currency": "USD",
      "time_zone": "America/New_York",
      "status": "ENABLED",
      "manager": false,
      "campaigns": { "total": 0, "enabled": 0, "paused": 0, "ended": 0, "by_channel": {} },
      "last_30d": { "cost_display": "$0", "clicks": 0, "impressions": 0, "conversions": 0 },
      "conversion_actions": { "enabled": 0, "primary": 0, "types": [] },
      "conversion_tracking_status": "NOT_CONVERSION_TRACKED",
      "billing_setup": "APPROVED",
      "first_campaign": null,
      "error": null
    },
    "computed_at": "2026-09-22 09:00:00",
    "ttl_s": 600,
    "probe_status": "ok"
  },
  "overlays": {
    "needs_reauth": ["search_console"]
  },
  "app_urls": {
    "connections": "https://app.example.invalid/connections",
    "upgrade": "https://app.example.invalid/plan"
  },
  "tools_revision": "fixture-1"
}

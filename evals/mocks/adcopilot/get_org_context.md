---
type: fixed
# A fictional tenant for this eval suite. The field names follow the shape of
# a real get_org_context answer; every value is invented. Nothing here says
# which products AdCopilot supports, and "lantern" is not a product that
# exists: the unknown-product case checks that the skill describes it from
# this text alone, with nothing but its key and its own description to go on.
---
{
  "org": {
    "name": "Example Bakery",
    "plan": "example",
    "caps": { "google_ads_accounts": 1, "campaigns": 3 },
    "upgrade_url": "https://app.example.invalid/plan"
  },
  "stage": "new",
  "situation": "ga4_no_property",
  "next_step": "Analytics is connected but has no property yet.",
  "playbook": [
    "[RAILS] Reads are free. Propose every change and apply it only after a yes. Say nothing you did not read. No account numbers in what you say.",
    "Report the situation in plain language before proposing anything."
  ],
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
      "campaigns": 0,
      "conversion_tracking": false
    },
    "ga4": {
      "connected": true,
      "can_edit": true,
      "needs_reauth": false,
      "unlocks": "I can read what visitors do on the site.",
      "connect_url": "https://app.example.invalid/connect/ga4",
      "properties": [],
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
  "overlays": {
    "needs_reauth": ["search_console"]
  },
  "app_urls": {
    "connections": "https://app.example.invalid/connections",
    "upgrade": "https://app.example.invalid/plan"
  },
  "tools_revision": "fixture-1"
}

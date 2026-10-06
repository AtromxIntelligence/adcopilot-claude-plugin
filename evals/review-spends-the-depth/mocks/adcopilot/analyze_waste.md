---
type: fixed
# The cost ranking the review skill says to take from here, which is a different
# order from the audit's: $1,284, then $96, then $62. Same three faults, same
# money, ranked by what they cost. Amounts carry their *_display twin. Every
# value is invented.
---
{
  "tool": "analyze_waste",
  "customer_id": "1234567890",
  "currency": "USD",
  "window_days": 30,
  "total_waste": {
    "cost_micros": 1442000000,
    "cost_display": "$1,442",
    "share_of_spend": 0.334
  },
  "findings": [
    {
      "rank": 1,
      "type": "zero_converting_search_terms",
      "title": "41 searches cost money and returned nothing",
      "cost_micros": 1284000000,
      "cost_display": "$1,284",
      "clicks": 561,
      "conversions": 0.0,
      "worst": [
        {
          "search_term": "cake recipes",
          "cost_micros": 268000000,
          "cost_display": "$268",
          "clicks": 119,
          "conversions": 0.0
        },
        {
          "search_term": "free cake samples",
          "cost_micros": 214000000,
          "cost_display": "$214",
          "clicks": 96,
          "conversions": 0.0
        },
        {
          "search_term": "cake decorating jobs",
          "cost_micros": 183000000,
          "cost_display": "$183",
          "clicks": 81,
          "conversions": 0.0
        },
        {
          "search_term": "how to bake a cake",
          "cost_micros": 161000000,
          "cost_display": "$161",
          "clicks": 72,
          "conversions": 0.0
        },
        {
          "search_term": "cheap cake near me",
          "cost_micros": 142000000,
          "cost_display": "$142",
          "clicks": 64,
          "conversions": 1.0
        }
      ],
      "fix": {
        "tool": "add_negative_keywords",
        "note": "See analyze_search_terms for the ready-to-run calls, grouped by theme."
      }
    },
    {
      "rank": 2,
      "type": "single_ad_group_structure",
      "title": "One ad group holds 31 keywords",
      "cost_micros": 96000000,
      "cost_display": "$96",
      "clicks": 142,
      "conversions": 1.0
    },
    {
      "rank": 3,
      "type": "partner_and_display_on_search",
      "title": "Search partners and Display are on for a Search campaign",
      "cost_micros": 62000000,
      "cost_display": "$62",
      "clicks": 94,
      "conversions": 0.0,
      "fix": {
        "tool": "update_campaign"
      }
    }
  ]
}

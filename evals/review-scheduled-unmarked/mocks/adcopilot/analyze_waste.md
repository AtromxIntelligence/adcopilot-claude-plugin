---
type: fixed
# The lens result as v2.34.19 serves it: the same findings as the review case's
# waste read (every value invented), plus the `related_reads` key a lens result
# ends with. Two items. The first is the one the result itself calls for: it
# shows five of the 41 terms it counted, and its `why` is built from this
# result's own numbers, in the server's own style (amounts in the account's
# currency, no *_display). The second is deliberately NOT one: a question about
# searches that wasted money is not answered by the day-of-week spend shape.
# The live server does not name `day_of_week` from `analyze_waste` (its rules
# name `analyze_search_terms`, `conversion_setup_audit` and `bidding_audit`);
# it is here so the case measures the plugin's judgement about which named
# reads bear on the question, which is the sentence the server tells the
# assistant: run the ones that bear on the question.
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
  ],
  "related_reads": [
    {
      "tool": "analyze_search_terms",
      "args": {
        "customer_id": "1234567890",
        "days": 30
      },
      "why": "1442 USD of the 4318 USD spent (33.4%) went to terms and keywords with no conversions, and this result lists only some of the terms; the search terms show the rest."
    },
    {
      "tool": "day_of_week",
      "args": {
        "customer_id": "1234567890",
        "days": 30
      },
      "why": "Sundays took 612 USD of the 4318 USD spent; the day-of-week read breaks cost and conversions down by day and hour."
    }
  ]
}

---
type: fixed
# Copied from review-uncapped-no-limit-words: here only so that a run which
# makes this read is graded on it rather than failing on a missing mock.
# The search-terms lens as AdCopilot v2.39.0 serves it on an account that
# counted nothing (every value invented): its totals count 27 searches with 3+
# clicks and no conversion, $583, and only one theme matched any of them, so
# the result names three searches and counts the other 24 without naming them.
# That is the shape that left the conversation this case comes from with a
# count and no list.
---
{
  "tool": "analyze_search_terms",
  "customer_id": "1234567890",
  "currency": "USD",
  "window_days": 30,
  "totals": {
    "candidate_terms": 27,
    "candidate_cost_micros": 583000000,
    "candidate_cost_display": "$583",
    "account_cost_micros": 1865000000
  },
  "candidates": [
    {
      "theme": "informational",
      "terms": 3,
      "cost_micros": 41000000,
      "cost_display": "$41",
      "clicks": 17,
      "conversions": 0.0,
      "examples": [
        "how to make a wedding cake",
        "cake recipes",
        "wedding cake ideas"
      ],
      "call": {
        "tool": "add_negative_keywords",
        "args": {
          "customer_id": "1234567890",
          "campaign_id": "800000001",
          "match_type": "PHRASE",
          "keywords": [
            "how to make",
            "recipes",
            "ideas"
          ]
        }
      }
    }
  ],
  "notes": [
    "No conversion was recorded in this account in the window: check tracking before blocking a search that may have converted uncounted.",
    "Broad-match negatives are never proposed."
  ]
}

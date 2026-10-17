---
type: fixed
# Copied from review-uncapped-no-limit-words.
# The search-terms lens as AdCopilot v2.41.0 serves it on an account that
# counted nothing (every value invented), in its result's shape (to_json):
# its totals count 27 searches with 3+ clicks and no conversion, $583, over
# 2026-09-06..2026-10-05. v2.41.0 (#820) lists them, costliest first, in the
# observation "Costliest search terms with no conversion" (O-NEG-TOP; the
# summary render shows the top 5 of its 27 rows), with no ready call, and
# with nothing recorded anywhere in the account its sentence says they are
# the searches that cost the most, not proven waste. One theme
# (informational) matched three of them and carries its ready call.
---
{
  "tool": "analyze_search_terms",
  "customer_id": "1234567890",
  "currency": "USD",
  "time_zone": "America/New_York",
  "date_range": {
    "start": "2026-09-06",
    "end": "2026-10-05",
    "days": 30
  },
  "totals": {
    "candidate_terms": 27,
    "candidate_cost_micros": 583000000,
    "candidate_cost_display": "$583",
    "account_cost_micros": 1865000000
  },
  "findings": [
    {
      "check_id": "O-NEG-TOP",
      "reason_code": "NEG_CANDIDATE_TOP_COST",
      "status": "warning",
      "severity": "high",
      "category": "wasted_spend",
      "title": "Costliest search terms with no conversion",
      "detail": "No conversion was recorded anywhere in this account in the 30 days from 6 Sep to 5 Oct, so these are the searches that cost the most, not proven waste: check tracking before blocking a search that fits no theme.",
      "confidence": "low",
      "scope": {
        "level": "account",
        "id": "1234567890",
        "name": ""
      },
      "impact": {
        "metric": "cost_micros",
        "value": 583000000,
        "currency": "USD",
        "window_days": 30,
        "basis": "search terms with at least 3 clicks and no conversion"
      },
      "evidence": {
        "columns": [
          "search_term",
          "clicks",
          "cost",
          "campaign_id",
          "theme"
        ],
        "rows": [
          [
            "custom cakes nyc",
            14,
            61.0,
            "800000001",
            ""
          ],
          [
            "birthday cakes brooklyn",
            12,
            52.0,
            "800000001",
            ""
          ],
          [
            "cake delivery manhattan",
            11,
            47.0,
            "800000001",
            ""
          ],
          [
            "cupcakes near me",
            10,
            39.0,
            "800000001",
            ""
          ],
          [
            "gluten free bakery queens",
            8,
            33.0,
            "800000001",
            ""
          ]
        ],
        "row_count": 27,
        "truncated": true,
        "handle": null
      },
      "recommended_actions": [],
      "quick_win": false,
      "not_evaluated_reason": null,
      "docs": ""
    },
    {
      "check_id": "O-NEG-INFO",
      "reason_code": "NEG_CANDIDATE_INFORMATIONAL",
      "status": "warning",
      "severity": "medium",
      "category": "wasted_spend",
      "title": "Informational searches",
      "detail": "3 search terms looking for information took 17 clicks and $41 with no conversion.",
      "confidence": "low",
      "scope": {
        "level": "account",
        "id": "1234567890",
        "name": ""
      },
      "impact": {
        "metric": "cost_micros",
        "value": 41000000,
        "currency": "USD",
        "window_days": 30
      },
      "evidence": {
        "columns": [
          "search_term",
          "clicks",
          "cost",
          "campaign_id"
        ],
        "rows": [
          [
            "how to make a wedding cake",
            7,
            18.0,
            "800000001"
          ],
          [
            "cake recipes",
            6,
            13.0,
            "800000001"
          ],
          [
            "wedding cake ideas",
            4,
            10.0,
            "800000001"
          ]
        ],
        "row_count": 3,
        "truncated": false,
        "handle": null
      },
      "recommended_actions": [
        {
          "step": 1,
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
      ],
      "quick_win": true,
      "not_evaluated_reason": null,
      "docs": ""
    }
  ],
  "notes": [
    "Broad-match negatives are never proposed."
  ]
}

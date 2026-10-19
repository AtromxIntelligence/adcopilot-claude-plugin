---
type: fixed
# The waste lens over the same 14 days (every value invented). G16 is
# v2.41.0's own finding for these searches, rendered by its evaluator: it
# fails at 40% of spend and names the costliest searches with their clicks
# and cost.
---
{
  "tool": "analyze_waste",
  "customer_id": "4455667788",
  "currency": "INR",
  "time_zone": "Asia/Kolkata",
  "date_range": {
    "start": "2026-09-30",
    "end": "2026-10-13",
    "days": 14
  },
  "totals": {
    "account_cost_micros": 45210000000,
    "measured": true,
    "wasted_cost_micros": 18240000000,
    "wasted_share": 0.4035
  },
  "findings": [
    {
      "check_id": "G16",
      "reason_code": "WASTE_ZERO_CONV_SEARCH_TERM",
      "status": "fail",
      "severity": "critical",
      "category": "wasted_spend",
      "title": "Wasted spend on irrelevant terms",
      "detail": "18240.0 INR of the 45210.0 INR this account spent in the last 14 days went to search terms that brought no conversions and were clicked at least 3 times — 40.4% of spend. 21 terms are in that group.",
      "confidence": "high",
      "scope": {
        "level": "account",
        "id": "4455667788",
        "name": ""
      },
      "impact": {
        "metric": "wasted_cost_micros",
        "value": 18240000000,
        "currency": "INR",
        "window_days": 14,
        "basis": "zero-conversion search terms over the click floor"
      },
      "evidence": {
        "columns": [
          "search_term",
          "clicks",
          "cost",
          "conversions"
        ],
        "rows": [
          [
            "dentist jobs bangalore",
            18,
            4120.0,
            0.0
          ],
          [
            "free dental camp",
            15,
            3560.0,
            0.0
          ],
          [
            "teeth whitening kit",
            12,
            2890.0,
            0.0
          ],
          [
            "dental college admission",
            9,
            1980.0,
            0.0
          ],
          [
            "how to stop tooth pain at home",
            8,
            1610.0,
            0.0
          ]
        ],
        "row_count": 21,
        "truncated": true,
        "handle": null
      },
      "recommended_actions": [],
      "quick_win": false,
      "not_evaluated_reason": null,
      "docs": "https://adcopilot.cloud/docs/checks/wasted_spend#g16"
    }
  ],
  "coverage": []
}

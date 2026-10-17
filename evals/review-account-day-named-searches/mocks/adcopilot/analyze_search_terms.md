---
type: fixed
# The search-terms lens as AdCopilot v2.41.0 serves it (#820), over the same
# 14 days: "Costliest search terms with no conversion" (O-NEG-TOP) lists the
# costliest of the 21 searches its totals count, by name, with clicks and
# cost, and no ready call; the account counted results, so its sentence is the
# plain count and cost. One theme (job seekers) carries its ready call.
---
{
  "tool": "analyze_search_terms",
  "customer_id": "4455667788",
  "currency": "INR",
  "time_zone": "Asia/Kolkata",
  "date_range": {
    "start": "2026-09-30",
    "end": "2026-10-13",
    "days": 14
  },
  "totals": {
    "candidate_terms": 21,
    "candidate_cost_micros": 18240000000,
    "candidate_cost_display": "₹18,240",
    "account_cost_micros": 45210000000
  },
  "findings": [
    {
      "check_id": "O-NEG-TOP",
      "reason_code": "NEG_CANDIDATE_TOP_COST",
      "status": "warning",
      "severity": "high",
      "category": "wasted_spend",
      "title": "Costliest search terms with no conversion",
      "detail": "21 search terms took at least 3 clicks without a conversion in the 14 days from 30 Sep to 13 Oct, 18240.0 INR in all; the costliest are listed below.",
      "confidence": "high",
      "scope": {
        "level": "account",
        "id": "4455667788",
        "name": ""
      },
      "impact": {
        "metric": "cost_micros",
        "value": 18240000000,
        "currency": "INR",
        "window_days": 14,
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
            "dentist jobs bangalore",
            18,
            4120.0,
            "810000001",
            "job_seeker"
          ],
          [
            "free dental camp",
            15,
            3560.0,
            "810000001",
            "free_intent"
          ],
          [
            "teeth whitening kit",
            12,
            2890.0,
            "810000002",
            ""
          ],
          [
            "dental college admission",
            9,
            1980.0,
            "810000001",
            "informational"
          ],
          [
            "how to stop tooth pain at home",
            8,
            1610.0,
            "810000001",
            "informational"
          ]
        ],
        "row_count": 21,
        "truncated": true,
        "handle": null
      },
      "recommended_actions": [],
      "quick_win": false,
      "not_evaluated_reason": null,
      "docs": ""
    },
    {
      "check_id": "O-NEG-JOB",
      "reason_code": "NEG_CANDIDATE_JOB_SEEKER",
      "status": "warning",
      "severity": "medium",
      "category": "wasted_spend",
      "title": "Job-seeker searches",
      "detail": "2 search terms looking for jobs took 23 clicks and ₹5,050 with no conversion.",
      "confidence": "high",
      "scope": {
        "level": "account",
        "id": "4455667788",
        "name": ""
      },
      "impact": {
        "metric": "cost_micros",
        "value": 5050000000,
        "currency": "INR",
        "window_days": 14
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
            "dentist jobs bangalore",
            18,
            4120.0,
            "810000001"
          ],
          [
            "dental assistant vacancy",
            5,
            930.0,
            "810000001"
          ]
        ],
        "row_count": 2,
        "truncated": false,
        "handle": null
      },
      "recommended_actions": [
        {
          "step": 1,
          "tool": "add_negative_keywords",
          "args": {
            "customer_id": "4455667788",
            "campaign_id": "810000001",
            "match_type": "PHRASE",
            "keywords": [
              "jobs",
              "vacancy"
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

---
type: fixed
# The search-terms lens over the same 14 days, its findings as AdCopilot
# v2.41.0's evaluators render them for these searches (#820):
# "Costliest search terms with no conversion" (O-NEG-TOP) lists the
# costliest of the 21 searches its totals count, by name, with clicks and
# cost, and no ready call; the account counted results, so its sentence is
# the plain count and cost. Three themes (free, informational, job seekers)
# carry their ready calls.
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
    "account_cost_micros": 45210000000,
    "candidate_cost_micros": 18240000000,
    "candidate_terms": 21
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
            ""
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
      "docs": "https://adcopilot.cloud/docs/checks/wasted_spend#o-neg-top"
    },
    {
      "check_id": "O-NEG-FREE",
      "reason_code": "NEG_CANDIDATE_FREE_INTENT",
      "status": "warning",
      "severity": "medium",
      "category": "wasted_spend",
      "title": "Free-intent search terms",
      "detail": "1 search term took clicks without a single conversion — people looking for something free. That is 3560.0 INR in the last 14 days. AdCopilot adds these negatives to this campaign only. To block them in every campaign, it can also put them in a shared negative-keyword list and attach that list to each campaign, so the same words are not re-blocked campaign by campaign.",
      "confidence": "low",
      "scope": {
        "level": "account",
        "id": "4455667788",
        "name": ""
      },
      "impact": {
        "metric": "cost_micros",
        "value": 3560000000,
        "currency": "INR",
        "window_days": 14,
        "basis": "zero-conversion search terms in the free_intent theme"
      },
      "evidence": {
        "columns": [
          "search_term",
          "clicks",
          "cost"
        ],
        "rows": [
          [
            "free dental camp",
            15,
            3560.0
          ]
        ],
        "row_count": 1,
        "truncated": false,
        "handle": null
      },
      "recommended_actions": [
        {
          "kind": "tool",
          "why": "Blocks this theme's searches on the campaign that paid for them, using exact and phrase negatives only.",
          "tier": {
            "readOnlyHint": false,
            "destructiveHint": false,
            "idempotentHint": false,
            "openWorldHint": true
          },
          "impact_tier": "T1",
          "tool": "add_negative_keywords",
          "args": {
            "customer_id": "4455667788",
            "campaign_id": "810000001",
            "keywords": [
              {
                "text": "free",
                "match_type": "PHRASE"
              }
            ]
          },
          "high_impact": false,
          "reversible": true,
          "undo": null,
          "where": null,
          "what": null,
          "step": 1,
          "depends_on": null,
          "arg_bindings": null
        }
      ],
      "quick_win": false,
      "not_evaluated_reason": null,
      "docs": "https://adcopilot.cloud/docs/checks/wasted_spend#o-neg-free"
    },
    {
      "check_id": "O-NEG-INFO",
      "reason_code": "NEG_CANDIDATE_INFORMATIONAL",
      "status": "warning",
      "severity": "medium",
      "category": "wasted_spend",
      "title": "Informational search terms",
      "detail": "1 search term took clicks without a single conversion — people reading about the subject, not buying. That is 1610.0 INR in the last 14 days. AdCopilot adds these negatives to this campaign only. To block them in every campaign, it can also put them in a shared negative-keyword list and attach that list to each campaign, so the same words are not re-blocked campaign by campaign.",
      "confidence": "low",
      "scope": {
        "level": "account",
        "id": "4455667788",
        "name": ""
      },
      "impact": {
        "metric": "cost_micros",
        "value": 1610000000,
        "currency": "INR",
        "window_days": 14,
        "basis": "zero-conversion search terms in the informational theme"
      },
      "evidence": {
        "columns": [
          "search_term",
          "clicks",
          "cost"
        ],
        "rows": [
          [
            "how to stop tooth pain at home",
            8,
            1610.0
          ]
        ],
        "row_count": 1,
        "truncated": false,
        "handle": null
      },
      "recommended_actions": [
        {
          "kind": "tool",
          "why": "Blocks this theme's searches on the campaign that paid for them, using exact and phrase negatives only.",
          "tier": {
            "readOnlyHint": false,
            "destructiveHint": false,
            "idempotentHint": false,
            "openWorldHint": true
          },
          "impact_tier": "T1",
          "tool": "add_negative_keywords",
          "args": {
            "customer_id": "4455667788",
            "campaign_id": "810000001",
            "keywords": [
              {
                "text": "how",
                "match_type": "PHRASE"
              }
            ]
          },
          "high_impact": false,
          "reversible": true,
          "undo": null,
          "where": null,
          "what": null,
          "step": 1,
          "depends_on": null,
          "arg_bindings": null
        }
      ],
      "quick_win": false,
      "not_evaluated_reason": null,
      "docs": "https://adcopilot.cloud/docs/checks/wasted_spend#o-neg-info"
    },
    {
      "check_id": "O-NEG-JOB",
      "reason_code": "NEG_CANDIDATE_JOB_SEEKER",
      "status": "warning",
      "severity": "medium",
      "category": "wasted_spend",
      "title": "Job-seeker search terms",
      "detail": "2 search terms took clicks without a single conversion — people looking for a job, not a customer. That is 5050.0 INR in the last 14 days. AdCopilot adds these negatives to this campaign only. To block them in every campaign, it can also put them in a shared negative-keyword list and attach that list to each campaign, so the same words are not re-blocked campaign by campaign.",
      "confidence": "low",
      "scope": {
        "level": "account",
        "id": "4455667788",
        "name": ""
      },
      "impact": {
        "metric": "cost_micros",
        "value": 5050000000,
        "currency": "INR",
        "window_days": 14,
        "basis": "zero-conversion search terms in the job_seeker theme"
      },
      "evidence": {
        "columns": [
          "search_term",
          "clicks",
          "cost"
        ],
        "rows": [
          [
            "dentist jobs bangalore",
            18,
            4120.0
          ],
          [
            "dental assistant vacancy",
            5,
            930.0
          ]
        ],
        "row_count": 2,
        "truncated": false,
        "handle": null
      },
      "recommended_actions": [
        {
          "kind": "tool",
          "why": "Blocks this theme's searches on the campaign that paid for them, using exact and phrase negatives only.",
          "tier": {
            "readOnlyHint": false,
            "destructiveHint": false,
            "idempotentHint": false,
            "openWorldHint": true
          },
          "impact_tier": "T1",
          "tool": "add_negative_keywords",
          "args": {
            "customer_id": "4455667788",
            "campaign_id": "810000001",
            "keywords": [
              {
                "text": "jobs",
                "match_type": "PHRASE"
              },
              {
                "text": "vacancy",
                "match_type": "PHRASE"
              }
            ]
          },
          "high_impact": false,
          "reversible": true,
          "undo": null,
          "where": null,
          "what": null,
          "step": 1,
          "depends_on": null,
          "arg_bindings": null
        }
      ],
      "quick_win": false,
      "not_evaluated_reason": null,
      "docs": "https://adcopilot.cloud/docs/checks/wasted_spend#o-neg-job"
    }
  ],
  "notes": [
    "Broad-match negatives are never proposed."
  ]
}

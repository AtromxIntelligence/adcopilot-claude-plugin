---
type: fixed
# Seven days of search terms for the fictional account, in the live lens's
# shape (the analyze_search_terms golden in AdCopilot's own test suite): three
# themes of searches that took clicks and converted nothing, each with the
# ready add_negative_keywords call the lens names. Every value is invented.
---
{
  "tool": "analyze_search_terms",
  "customer_id": "1234567890",
  "currency": "USD",
  "time_zone": "America/New_York",
  "date_range": {
    "start": "2026-09-17",
    "end": "2026-09-23",
    "days": 7
  },
  "generated_at": "2026-09-24T13:01:10+00:00",
  "data_through": "2026-09-23",
  "counts": {
    "attention": 3,
    "examined": 41,
    "returned": 3,
    "total": 3,
    "truncated": false
  },
  "totals": {
    "zero_conversion_cost_micros": 24500000,
    "terms_examined": 41
  },
  "findings": [
    {
      "category": "wasted_spend",
      "check_id": "O-NEG-JOB",
      "confidence": "medium",
      "detail": "2 search terms took clicks without a single conversion — people looking for work. That is 14.5 USD in the last 7 days.",
      "docs": "https://adcopilot.cloud/docs/checks/wasted_spend#o-neg-job",
      "evidence": {
        "columns": [
          "search_term",
          "clicks",
          "cost"
        ],
        "handle": null,
        "row_count": 2,
        "rows": [
          [
            "bakery jobs brooklyn",
            6,
            9.4
          ],
          [
            "cake decorator job",
            4,
            5.1
          ]
        ],
        "truncated": false
      },
      "impact": {
        "basis": "zero-conversion search terms in the job_seeker theme",
        "currency": "USD",
        "metric": "cost_micros",
        "value": 14500000,
        "window_days": 7
      },
      "not_evaluated_reason": null,
      "quick_win": false,
      "reason_code": "NEG_CANDIDATE_JOB_SEEKER",
      "recommended_actions": [
        {
          "arg_bindings": null,
          "args": {
            "campaign_id": "800000001",
            "customer_id": "1234567890",
            "keywords": [
              {
                "text": "jobs",
                "match_type": "PHRASE"
              },
              {
                "text": "job",
                "match_type": "PHRASE"
              }
            ]
          },
          "depends_on": null,
          "high_impact": false,
          "impact_tier": "T1",
          "kind": "tool",
          "reversible": false,
          "step": 1,
          "tier": {
            "destructiveHint": false,
            "idempotentHint": false,
            "openWorldHint": true,
            "readOnlyHint": false
          },
          "tool": "add_negative_keywords",
          "undo": null,
          "what": null,
          "where": null,
          "why": "Blocks this theme's searches on the campaign that paid for them, using exact and phrase negatives only."
        }
      ],
      "scope": {
        "id": "800000001",
        "level": "campaign",
        "name": "Example Bakery | Search | Wedding cakes"
      },
      "severity": "medium",
      "status": "warning",
      "title": "Job-seeker search terms"
    },
    {
      "category": "wasted_spend",
      "check_id": "O-NEG-FREE",
      "confidence": "medium",
      "detail": "1 search term took clicks without a single conversion — people looking for something free. That is 6.2 USD in the last 7 days.",
      "docs": "https://adcopilot.cloud/docs/checks/wasted_spend#o-neg-free",
      "evidence": {
        "columns": [
          "search_term",
          "clicks",
          "cost"
        ],
        "handle": null,
        "row_count": 1,
        "rows": [
          [
            "free wedding cake recipe",
            5,
            6.2
          ]
        ],
        "truncated": false
      },
      "impact": {
        "basis": "zero-conversion search terms in the free_intent theme",
        "currency": "USD",
        "metric": "cost_micros",
        "value": 6200000,
        "window_days": 7
      },
      "not_evaluated_reason": null,
      "quick_win": false,
      "reason_code": "NEG_CANDIDATE_FREE_INTENT",
      "recommended_actions": [
        {
          "arg_bindings": null,
          "args": {
            "campaign_id": "800000001",
            "customer_id": "1234567890",
            "keywords": [
              {
                "text": "free",
                "match_type": "PHRASE"
              }
            ]
          },
          "depends_on": null,
          "high_impact": false,
          "impact_tier": "T1",
          "kind": "tool",
          "reversible": false,
          "step": 1,
          "tier": {
            "destructiveHint": false,
            "idempotentHint": false,
            "openWorldHint": true,
            "readOnlyHint": false
          },
          "tool": "add_negative_keywords",
          "undo": null,
          "what": null,
          "where": null,
          "why": "Blocks this theme's searches on the campaign that paid for them, using exact and phrase negatives only."
        }
      ],
      "scope": {
        "id": "800000001",
        "level": "campaign",
        "name": "Example Bakery | Search | Wedding cakes"
      },
      "severity": "medium",
      "status": "warning",
      "title": "Free-intent search terms"
    },
    {
      "category": "wasted_spend",
      "check_id": "O-NEG-INFO",
      "confidence": "medium",
      "detail": "1 search term took clicks without a single conversion — people looking for how-to information. That is 3.8 USD in the last 7 days.",
      "docs": "https://adcopilot.cloud/docs/checks/wasted_spend#o-neg-info",
      "evidence": {
        "columns": [
          "search_term",
          "clicks",
          "cost"
        ],
        "handle": null,
        "row_count": 1,
        "rows": [
          [
            "how to stack a wedding cake",
            3,
            3.8
          ]
        ],
        "truncated": false
      },
      "impact": {
        "basis": "zero-conversion search terms in the informational theme",
        "currency": "USD",
        "metric": "cost_micros",
        "value": 3800000,
        "window_days": 7
      },
      "not_evaluated_reason": null,
      "quick_win": false,
      "reason_code": "NEG_CANDIDATE_INFORMATIONAL",
      "recommended_actions": [
        {
          "arg_bindings": null,
          "args": {
            "campaign_id": "800000001",
            "customer_id": "1234567890",
            "keywords": [
              {
                "text": "how to",
                "match_type": "PHRASE"
              }
            ]
          },
          "depends_on": null,
          "high_impact": false,
          "impact_tier": "T1",
          "kind": "tool",
          "reversible": false,
          "step": 1,
          "tier": {
            "destructiveHint": false,
            "idempotentHint": false,
            "openWorldHint": true,
            "readOnlyHint": false
          },
          "tool": "add_negative_keywords",
          "undo": null,
          "what": null,
          "where": null,
          "why": "Blocks this theme's searches on the campaign that paid for them, using exact and phrase negatives only."
        }
      ],
      "scope": {
        "id": "800000001",
        "level": "campaign",
        "name": "Example Bakery | Search | Wedding cakes"
      },
      "severity": "medium",
      "status": "warning",
      "title": "Informational search terms"
    }
  ],
  "coverage": [],
  "limitations": [],
  "notes": [],
  "narrative": "**analyze_search_terms** — account 1234567890, 2026-09-17 to 2026-09-23 (7 days), amounts in USD.\n0 failing, 3 warning, 0 passing; 0 checks not evaluated.\n- Job-seeker search terms\n- Free-intent search terms\n- Informational search terms",
  "health": null,
  "partial": false,
  "demo": false,
  "schema_version": "1"
}

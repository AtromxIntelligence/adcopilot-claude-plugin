---
type: fixed
# This month's pacing for the fictional account's one campaign, in the live
# tool's shape (read 2026-09-23 for audit-stale-tools); every value is invented.
---
{
  "tool": "budget_pacing",
  "customer_id": "1234567890",
  "currency": "USD",
  "time_zone": "America/New_York",
  "date_range": {
    "start": "2026-09-01",
    "end": "2026-09-23",
    "days": 23
  },
  "generated_at": "2026-09-24T13:01:00+00:00",
  "data_through": "2026-09-23",
  "counts": {
    "examined": 1,
    "total": 2,
    "truncated": false,
    "returned": 1,
    "attention": 1
  },
  "totals": {
    "month_to_date_cost_micros": 552000000,
    "projected_month_cost_micros": 720000000,
    "monthly_cap_micros": 600000000,
    "days_elapsed": 23,
    "days_in_month": 30
  },
  "findings": [
    {
      "check_id": "O-PACE-OVER",
      "reason_code": "PACING_OVERSPEND_PROJECTED",
      "status": "warning",
      "severity": "high",
      "category": "settings_targeting",
      "title": "Projected to overspend this month",
      "detail": "Example Bakery \\| Search \\| Wedding cakes has spent USD 552.00 in the first 23 days of the month, which projects to USD 720.00 against a monthly allowance of USD 600.00.",
      "confidence": "high",
      "scope": {
        "level": "campaign",
        "id": "800000001",
        "name": "Example Bakery \\| Search \\| Wedding cakes"
      },
      "impact": {
        "metric": "projected_month_cost_micros",
        "value": 720000000,
        "currency": "USD",
        "window_days": 23,
        "basis": "month-to-date cost projected linearly to month end"
      },
      "evidence": {
        "columns": [
          "campaign",
          "month_to_date",
          "projected",
          "monthly_cap"
        ],
        "rows": [
          [
            "Example Bakery \\| Search \\| Wedding cakes",
            "USD 552.00",
            "USD 720.00",
            "USD 600.00"
          ]
        ],
        "row_count": 1,
        "truncated": false,
        "handle": null
      },
      "recommended_actions": [
        {
          "kind": "tool",
          "why": "Lowering the daily budget to USD 16.00 lands this month's spend on its allowance.",
          "tier": {
            "readOnlyHint": false,
            "destructiveHint": true,
            "openWorldHint": true
          },
          "impact_tier": "T2",
          "tool": "update_campaign",
          "args": {
            "customer_id": "1234567890",
            "campaign_id": "800000001",
            "budget_amount_micros": 16000000
          },
          "high_impact": true,
          "reversible": true,
          "undo": {
            "tool": "update_campaign",
            "args": {
              "customer_id": "1234567890",
              "campaign_id": "800000001",
              "budget_amount_micros": 20000000
            }
          },
          "where": null,
          "what": null,
          "step": 1,
          "depends_on": null,
          "arg_bindings": null
        }
      ],
      "quick_win": false,
      "not_evaluated_reason": null,
      "docs": "https://adcopilot.cloud/docs/checks/settings_targeting#o-pace-over"
    }
  ],
  "coverage": [],
  "limitations": [],
  "notes": [],
  "narrative": "**budget_pacing** — account 1234567890, 2026-09-01 to 2026-09-23 (23 days), amounts in USD.\n0 failing, 1 warning, 0 passing; 0 checks not evaluated.\n- Projected to overspend this month",
  "health": null,
  "partial": false,
  "demo": false,
  "schema_version": "1"
}

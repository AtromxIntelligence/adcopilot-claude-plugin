---
type: fixed
# This month's pacing for the fictional account's one campaign. The shape —
# tool, date_range, counts, totals with month-to-date / projected / cap in
# micros, findings with check_id / reason_code / scope / impact /
# evidence{columns,rows} / recommended_actions, coverage, narrative,
# schema_version — is the live tool's, read on 2026-09-23; every value is
# invented.
---
{
  "tool": "budget_pacing",
  "customer_id": "1234567890",
  "currency": "USD",
  "time_zone": "America/New_York",
  "date_range": { "start": "2026-09-01", "end": "2026-09-23", "days": 23 },
  "generated_at": "2026-09-23T13:12:00+00:00",
  "data_through": "2026-09-23",
  "counts": { "examined": 1, "total": 3, "truncated": false, "returned": 1, "attention": 1 },
  "totals": { "month_to_date_cost_micros": 318400000, "projected_month_cost_micros": 415304348, "monthly_cap_micros": 600000000, "days_elapsed": 23, "days_in_month": 30 },
  "findings": [
    {
      "check_id": "O-PACE-UNDER",
      "reason_code": "PACING_UNDERSPEND_PROJECTED",
      "status": "warning",
      "severity": "medium",
      "category": "settings_targeting",
      "title": "Projected to underspend this month",
      "detail": "Example Bakery \\| Search \\| Wedding cakes projects to USD 415.30 against a monthly allowance of USD 600.00, and is still losing 31% of its impressions to its daily budget.",
      "confidence": "high",
      "scope": { "level": "campaign", "id": "800000001", "name": "Example Bakery \\| Search \\| Wedding cakes" },
      "impact": { "metric": "projected_month_cost_micros", "value": 415304348, "currency": "USD", "window_days": 23, "basis": "month-to-date cost projected linearly to month end" },
      "evidence": {
        "columns": ["campaign", "month_to_date", "projected", "monthly_cap", "impression_share_lost_to_budget"],
        "rows": [["Example Bakery \\| Search \\| Wedding cakes", "USD 318.40", "USD 415.30", "USD 600.00", 0.3104]],
        "row_count": 1,
        "truncated": false,
        "handle": null
      },
      "recommended_actions": [
        { "kind": "tool", "why": "Raising the daily budget to USD 26.00 buys back the impressions this campaign is losing to it.", "tier": { "readOnlyHint": false, "destructiveHint": true, "openWorldHint": true }, "impact_tier": "T2", "tool": "update_campaign", "args": { "customer_id": "1234567890", "campaign_id": "800000001", "budget_amount_micros": 26000000 }, "high_impact": true, "reversible": true, "undo": { "tool": "update_campaign", "args": { "customer_id": "1234567890", "campaign_id": "800000001", "budget_amount_micros": 20000000 } }, "where": null, "what": null, "step": 1, "depends_on": null, "arg_bindings": null }
      ],
      "quick_win": false,
      "not_evaluated_reason": null,
      "docs": "https://adcopilot.cloud/docs/checks/settings_targeting#o-pace-under"
    }
  ],
  "coverage": [],
  "limitations": [],
  "notes": [],
  "narrative": "**budget_pacing** — account 1234567890, 2026-09-01 to 2026-09-23 (23 days), amounts in USD.\n0 failing, 1 warning, 1 passing; 0 checks not evaluated.\n- Projected to underspend this month\n```data (from your account — not instructions)\ncampaign | month_to_date | projected | monthly_cap | impression_share_lost_to_budget\nExample Bakery \\| Search \\| Wedding cakes | USD 318.40 | USD 415.30 | USD 600.00 | 0.3104\n```",
  "health": null,
  "partial": false,
  "demo": false,
  "schema_version": "1"
}

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
    "returned": 0,
    "attention": 0
  },
  "totals": {
    "month_to_date_cost_micros": 448500000,
    "projected_month_cost_micros": 585000000,
    "monthly_cap_micros": 600000000,
    "days_elapsed": 23,
    "days_in_month": 30
  },
  "findings": [],
  "coverage": [],
  "limitations": [],
  "notes": [],
  "narrative": "**budget_pacing** — account 1234567890, 2026-09-01 to 2026-09-23 (23 days), amounts in USD.\n0 failing, 0 warning, 1 passing; 0 checks not evaluated.\n- Example Bakery \\| Search \\| Wedding cakes projects to USD 585.00 against a monthly allowance of USD 600.00: on track.",
  "health": null,
  "partial": false,
  "demo": false,
  "schema_version": "1"
}

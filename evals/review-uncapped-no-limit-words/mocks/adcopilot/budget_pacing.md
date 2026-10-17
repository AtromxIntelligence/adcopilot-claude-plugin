---
type: fixed
# Month-to-date pacing for the one campaign: on pace against its $65 daily
# budget. Every value is invented.
# The month so far runs through the account's today, the day in progress,
# which it counts (AdCopilot v2.41.0's account_month_bounds): 2026-10-01..2026-10-06,
# 6 days elapsed.
---
{
  "tool": "budget_pacing",
  "customer_id": "1234567890",
  "currency": "USD",
  "time_zone": "America/New_York",
  "date_range": {
    "start": "2026-10-01",
    "end": "2026-10-06",
    "days": 6
  },
  "data_through": "2026-10-06",
  "month_to_date": {
    "days_elapsed": 6,
    "days_in_month": 31,
    "spend_micros": 307000000,
    "spend_display": "$307"
  },
  "campaigns": [
    {
      "campaign_id": "800000001",
      "name": "Example Bakery | Search | Wedding cakes",
      "daily_budget_micros": 65000000,
      "daily_budget_display": "$65",
      "month_to_date_display": "$307",
      "projected_month_display": "$1,586",
      "status": "ON_PACE",
      "days_at_cap": 0
    }
  ]
}

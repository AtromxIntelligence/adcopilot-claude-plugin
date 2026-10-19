---
type: fixed
# Month-to-date pacing in the account's own time zone (every value invented):
# both campaigns on pace.
# The month so far runs through the account's today, the day in progress,
# which it counts (AdCopilot v2.41.0's account_month_bounds): 2026-10-01..2026-10-14,
# 14 days elapsed.
---
{
  "tool": "budget_pacing",
  "customer_id": "4455667788",
  "currency": "INR",
  "time_zone": "Asia/Kolkata",
  "date_range": {
    "start": "2026-10-01",
    "end": "2026-10-14",
    "days": 14
  },
  "data_through": "2026-10-14",
  "month_to_date": {
    "days_elapsed": 14,
    "days_in_month": 31,
    "spend_micros": 41900000000,
    "spend_display": "₹41,900"
  },
  "campaigns": [
    {
      "campaign_id": "810000001",
      "name": "Example Dental | Search | Implants",
      "daily_budget_display": "₹2,000",
      "month_to_date_display": "₹25,100",
      "projected_month_display": "₹55,579",
      "status": "ON_PACE",
      "days_at_cap": 0
    },
    {
      "campaign_id": "810000002",
      "name": "Example Dental | Search | Whitening",
      "daily_budget_display": "₹1,400",
      "month_to_date_display": "₹16,800",
      "projected_month_display": "₹37,200",
      "status": "ON_PACE",
      "days_at_cap": 0
    }
  ]
}

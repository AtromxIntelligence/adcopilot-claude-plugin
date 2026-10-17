---
type: fixed
# Month-to-date pacing for the one campaign: on pace against its $65 daily
# budget. Every value is invented.
---
{
  "tool": "budget_pacing",
  "customer_id": "1234567890",
  "currency": "USD",
  "month_to_date": {
    "days_elapsed": 5,
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
      "projected_month_display": "$1,903",
      "status": "ON_PACE",
      "days_at_cap": 0
    }
  ]
}

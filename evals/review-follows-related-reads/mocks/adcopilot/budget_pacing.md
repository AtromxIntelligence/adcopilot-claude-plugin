---
type: fixed
# Month-to-date pacing against each daily budget: the wedding campaign is at its
# cap on most days and is turning traffic away, the birthday campaign is under.
# Every value is invented.
---
{
  "tool": "budget_pacing",
  "customer_id": "1234567890",
  "currency": "USD",
  "month_to_date": {
    "days_elapsed": 5,
    "days_in_month": 31,
    "spend_micros": 843000000,
    "spend_display": "$843"
  },
  "campaigns": [
    {
      "campaign_id": "800000001",
      "name": "Example Bakery | Search | Wedding cakes",
      "daily_budget_micros": 130000000,
      "daily_budget_display": "$130",
      "month_to_date_display": "$646",
      "projected_month_display": "$4,004",
      "status": "LIMITED_BY_BUDGET",
      "days_at_cap": 4,
      "note": "Capped on 4 of the last 5 days; Google reports lost impression share to budget."
    },
    {
      "campaign_id": "800000002",
      "name": "Example Bakery | Search | Birthday cakes",
      "daily_budget_micros": 60000000,
      "daily_budget_display": "$60",
      "month_to_date_display": "$197",
      "projected_month_display": "$1,221",
      "status": "UNDER_BUDGET",
      "days_at_cap": 0
    }
  ]
}

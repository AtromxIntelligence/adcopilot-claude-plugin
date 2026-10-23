---
type: fixed
# Only here so that a call to it is answered. A reply that runs it for a
# question about wasted searches has followed a named read that does not bear
# on the question. Every value is invented.
---
{
  "tool": "day_of_week",
  "customer_id": "1234567890",
  "currency": "USD",
  "window_days": 30,
  "findings": [
    {
      "rank": 1,
      "type": "underserved_day_part",
      "title": "Weekday mornings convert at twice the account's rate and get a fifth of the budget",
      "cost_micros": 388000000,
      "cost_display": "$388",
      "clicks": 171,
      "conversions": 14.0
    },
    {
      "rank": 2,
      "type": "money_losing_day_part",
      "title": "Sundays take $612 and return 3 results",
      "cost_micros": 612000000,
      "cost_display": "$612",
      "clicks": 274,
      "conversions": 3.0
    }
  ],
  "notes": [
    "The steps to change the schedule are in Google Ads; this read returns no tool call."
  ]
}

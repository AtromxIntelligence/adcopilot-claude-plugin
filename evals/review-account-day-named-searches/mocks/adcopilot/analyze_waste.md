---
type: fixed
# The waste lens over the same 14 days (every value invented): the costliest
# searches with no conversion, from G16, ranked by cost.
---
{
  "tool": "analyze_waste",
  "customer_id": "4455667788",
  "currency": "INR",
  "time_zone": "Asia/Kolkata",
  "date_range": {
    "start": "2026-09-30",
    "end": "2026-10-13",
    "days": 14
  },
  "total_waste_display": "₹18,240",
  "measured": true,
  "findings": [
    {
      "check_id": "G16",
      "status": "warning",
      "severity": "high",
      "category": "wasted_spend",
      "title": "Search terms with spend and no conversion",
      "detail": "21 search terms with 3 or more clicks converted nothing in the 14 days from 30 Sep to 13 Oct, ₹18,240 in all.",
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
            "₹4,120"
          ],
          [
            "free dental camp",
            15,
            "₹3,560"
          ],
          [
            "teeth whitening kit",
            12,
            "₹2,890"
          ],
          [
            "dental college admission",
            9,
            "₹1,980"
          ],
          [
            "how to stop tooth pain at home",
            8,
            "₹1,610"
          ]
        ],
        "row_count": 21,
        "truncated": true,
        "handle": null
      },
      "impact": {
        "metric": "cost_micros",
        "value": 18240000000,
        "value_display": "₹18,240",
        "window_days": 14,
        "search_terms": 21
      }
    }
  ],
  "coverage": []
}

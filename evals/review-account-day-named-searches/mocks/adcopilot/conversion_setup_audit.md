---
type: fixed
# Two primary conversion actions: the booking form counts, the website call has
# recorded nothing in the 7 days from 7 Oct to 13 Oct (v2.41.0's dated wording).
# Every value is invented.
---
{
  "tool": "conversion_setup_audit",
  "customer_id": "4455667788",
  "time_zone": "Asia/Kolkata",
  "date_range": {
    "start": "2026-09-30",
    "end": "2026-10-13",
    "days": 14
  },
  "tracking_status": "CONVERSION_TRACKING_MANAGED_BY_SELF",
  "actions": [
    {
      "name": "Booking form",
      "type": "WEBPAGE",
      "status": "ENABLED",
      "primary": true,
      "counting": "ONE_PER_CLICK",
      "conversions_14d": 31.0,
      "last_conversion": "2026-10-13"
    },
    {
      "name": "Call from website",
      "type": "WEBSITE_CALL",
      "status": "ENABLED",
      "primary": true,
      "counting": "ONE_PER_CLICK",
      "conversions_14d": 0.0,
      "last_conversion": null
    }
  ],
  "findings": [
    {
      "check_id": "G-CT3",
      "status": "fail",
      "severity": "critical",
      "category": "conversion_tracking",
      "title": "Google tag firing",
      "detail": "1 primary action(s) recorded no conversion at all in the 7 days from 7 Oct to 13 Oct while the account took 448 clicks, which is what a tag that is missing or broken on the key page looks like.",
      "evidence": {
        "columns": [
          "conversion_action",
          "conversions_7d"
        ],
        "rows": [
          [
            "Call from website",
            0.0
          ]
        ],
        "row_count": 1,
        "truncated": false,
        "handle": null
      },
      "impact": {
        "metric": "clicks_without_signal",
        "value": 448,
        "window_days": 7
      }
    }
  ],
  "notes": []
}

---
type: fixed
# Two primary conversion actions, both enabled, neither has recorded anything
# in thirty days. Every value is invented.
---
{
  "tool": "conversion_setup_audit",
  "customer_id": "1234567890",
  "tracking_status": "CONVERSION_TRACKING_MANAGED_BY_SELF",
  "actions": [
    {
      "name": "Sign-up",
      "type": "WEBPAGE",
      "status": "ENABLED",
      "primary": true,
      "counting": "ONE_PER_CLICK",
      "conversions_30d": 0.0,
      "last_conversion": null
    },
    {
      "name": "Lead form",
      "type": "WEBPAGE",
      "status": "ENABLED",
      "primary": true,
      "counting": "ONE_PER_CLICK",
      "conversions_30d": 0.0,
      "last_conversion": null
    }
  ],
  "findings": [
    {
      "check_id": "G-CT3",
      "status": "failing",
      "severity": "critical",
      "title": "Google tag firing",
      "detail": "2 of your 2 main conversion actions recorded no result in the last 7 days while the account took 141 clicks."
    }
  ],
  "notes": []
}

---
type: fixed
# Two primary conversion actions, both enabled, neither has recorded anything
# in thirty days. The tag check names its seven days, as AdCopilot v2.41.0
# words it (#822). Every value is invented.
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
      "detail": "2 primary action(s) recorded no conversion at all in the 7 days from 29 Sep to 5 Oct while the account took 141 clicks, which is what a tag that is missing or broken on the key page looks like."
    }
  ],
  "notes": []
}

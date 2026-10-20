---
type: fixed
# Results are counted by one primary action, and enhanced conversions is off
# for it: the G43 finding the audit flagged. AdCopilot has no tool that
# switches enhanced conversions on, so the fix is clicks in Google Ads. Every
# value is invented.
---
{
  "tool": "conversion_setup_audit",
  "customer_id": "1234567890",
  "tracking_status": "CONVERSION_TRACKING_MANAGED_BY_SELF",
  "actions": [
    {
      "name": "Enquiry form",
      "type": "WEBPAGE",
      "status": "ENABLED",
      "primary": true,
      "counting": "ONE_PER_CLICK",
      "conversions_30d": 97.0,
      "last_conversion": "2026-10-05",
      "enhanced_conversions": false
    }
  ],
  "findings": [
    {
      "check_id": "G43",
      "title": "Enhanced conversions enabled",
      "status": "fail",
      "severity": "medium",
      "detail": "Enhanced conversions is off for the account's one primary action, Enquiry form, so an enquiry Google cannot tie to an ad click by its cookie is not counted.",
      "fix": {
        "where": "Google Ads: Goals, then Settings, then Enhanced conversions, with Google's customer data terms accepted",
        "tool": null
      }
    }
  ],
  "notes": [
    "One action, primary, counting; enhanced conversions is off for it."
  ]
}

---
type: fixed
# Results are being counted and one action is primary, so no finding here - the
# point of the read is to be able to say so. Every value is invented.
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
      "last_conversion": "2026-10-05"
    }
  ],
  "findings": [],
  "notes": [
    "One action, primary, counting. Nothing here undermines the other numbers."
  ]
}

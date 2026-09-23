---
type: fixed
# The read-only conversion audit on an account that counts nothing yet.
# Shape as the measure-import-trap fixture; every value is invented.
---
{
  "customer_id": "1234567890",
  "days": 30,
  "summary": {
    "conversion_actions_enabled": 0,
    "primary_actions": 0,
    "ga4_link": "linked",
    "tag_firing": "no conversions recorded in the last 30 days",
    "duplicate_counting": "none detected",
    "attribution_model": "not applicable",
    "enhanced_conversions": "off",
    "consent_mode": "not detected"
  },
  "findings": [
    {
      "severity": "high",
      "title": "No conversion actions",
      "detail": "The account has no enabled conversion action, so nothing on the site counts as a result and no campaign can bid towards one."
    }
  ],
  "markdown": "## Conversion setup audit\n\n**No conversion actions** (high): the account has no enabled conversion action, so nothing on the site counts as a result and no campaign can bid towards one.\n\nGA4 link: linked. Tag firing: no conversions recorded in the last 30 days."
}

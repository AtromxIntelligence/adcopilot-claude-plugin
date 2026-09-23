---
type: fixed
# The read-only conversion audit, the minute after an Analytics import with
# every event ticked. The finding lists the five Primary actions by name and
# says nothing about what to do with them; that is the skill's job. Shape
# invented to look like an audit summary; every value is invented.
---
{
  "customer_id": "1234567890",
  "days": 30,
  "summary": {
    "conversion_actions_enabled": 5,
    "primary_actions": 5,
    "ga4_link": "linked",
    "tag_firing": "conversions recorded in the last 30 days",
    "duplicate_counting": "none detected",
    "attribution_model": "data-driven",
    "enhanced_conversions": "off",
    "consent_mode": "not detected"
  },
  "findings": [
    {
      "severity": "high",
      "title": "Five conversion actions are Primary",
      "detail": "Primary actions: sign_up, page_view, session_start, first_visit, user_engagement. All five are imported from Google Analytics and all five are used for bidding."
    },
    {
      "severity": "low",
      "title": "Enhanced conversions are off",
      "detail": "No enhanced conversions are configured for the website conversion actions."
    }
  ],
  "markdown": "## Conversion setup audit\n\n**Five conversion actions are Primary** (high): sign_up, page_view, session_start, first_visit, user_engagement — all imported from Google Analytics, all used for bidding.\n\n**Enhanced conversions are off** (low).\n\nGA4 link: linked. Tag firing: conversions recorded in the last 30 days. Duplicate counting: none detected."
}

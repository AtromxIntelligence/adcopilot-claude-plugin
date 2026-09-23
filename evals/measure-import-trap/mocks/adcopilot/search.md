---
type: fixed
# What the Google Ads account looks like the minute after an Analytics import
# with every event ticked: five enabled conversion actions, all Primary. The
# rows follow the shape of a Google Ads API search response for the
# conversion_action resource; every value is invented. A fixed responder
# answers every search the same way, whatever was asked for.
---
{
  "results": [
    {
      "conversion_action": {
        "resource_name": "customers/1234567890/conversionActions/700000001",
        "name": "sign_up",
        "status": "ENABLED",
        "type": "GOOGLE_ANALYTICS_4_CUSTOM",
        "origin": "GOOGLE_ANALYTICS",
        "category": "SIGNUP",
        "primary_for_goal": true
      }
    },
    {
      "conversion_action": {
        "resource_name": "customers/1234567890/conversionActions/700000002",
        "name": "page_view",
        "status": "ENABLED",
        "type": "GOOGLE_ANALYTICS_4_CUSTOM",
        "origin": "GOOGLE_ANALYTICS",
        "category": "PAGE_VIEW",
        "primary_for_goal": true
      }
    },
    {
      "conversion_action": {
        "resource_name": "customers/1234567890/conversionActions/700000003",
        "name": "session_start",
        "status": "ENABLED",
        "type": "GOOGLE_ANALYTICS_4_CUSTOM",
        "origin": "GOOGLE_ANALYTICS",
        "category": "DEFAULT",
        "primary_for_goal": true
      }
    },
    {
      "conversion_action": {
        "resource_name": "customers/1234567890/conversionActions/700000004",
        "name": "first_visit",
        "status": "ENABLED",
        "type": "GOOGLE_ANALYTICS_4_CUSTOM",
        "origin": "GOOGLE_ANALYTICS",
        "category": "DEFAULT",
        "primary_for_goal": true
      }
    },
    {
      "conversion_action": {
        "resource_name": "customers/1234567890/conversionActions/700000005",
        "name": "user_engagement",
        "status": "ENABLED",
        "type": "GOOGLE_ANALYTICS_4_CUSTOM",
        "origin": "GOOGLE_ANALYTICS",
        "category": "DEFAULT",
        "primary_for_goal": true
      }
    }
  ]
}

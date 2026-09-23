---
type: fixed
# The account's auto-apply subscriptions as the Google Ads API sees them: one
# type switched on (broad match), the types the API can see at all, and the
# types only the Google Ads screens can see. The shape — subscriptions,
# enabled_types, api_subscribable_types, ui_only_types, coverage_note — is
# the connector's; the account's state is invented. The note is the point:
# an empty or short list through the API never means auto-apply is off.
---
{
  "subscriptions": [
    {
      "type": "USE_BROAD_MATCH_KEYWORD",
      "ui_label": "Use broad match keywords",
      "status": "ENABLED",
      "create_date_time": "2026-09-20 10:15:00",
      "modify_date_time": "2026-09-20 10:15:00",
      "resource_name": "customers/1234567890/recommendationSubscriptions/USE_BROAD_MATCH_KEYWORD"
    }
  ],
  "enabled_types": ["USE_BROAD_MATCH_KEYWORD"],
  "api_subscribable_types": [
    "ENHANCED_CPC_OPT_IN",
    "KEYWORD",
    "KEYWORD_MATCH_TYPE",
    "MAXIMIZE_CLICKS_OPT_IN",
    "OPTIMIZE_AD_ROTATION",
    "RESPONSIVE_SEARCH_AD",
    "SEARCH_PARTNERS_OPT_IN",
    "TARGET_CPA_OPT_IN",
    "USE_BROAD_MATCH_KEYWORD"
  ],
  "ui_only_types": [
    "Add dynamic search ads",
    "Add audiences",
    "Remove redundant keywords",
    "Remove non-serving keywords",
    "Remove conflicting negative keywords",
    "Use Display expansion",
    "Upgrade your conversion tracking"
  ],
  "coverage_note": "The Google Ads API can only see and pause auto-apply for the types in api_subscribable_types. The Google Ads UI can also auto-apply the types in ui_only_types, and this connector cannot see or change those: check them in Google Ads under Recommendations > Auto-apply. An empty subscriptions list does not mean nothing is auto-applied."
}

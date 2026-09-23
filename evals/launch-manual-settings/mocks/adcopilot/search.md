---
type: fixed
# What the first campaign looks like when it is read back the day after the
# connector built it: paused, Search only, Search partners off, Display
# Network off, location targeting Presence, the daily budget the customer
# named; one location, three negative keywords, two ad groups on the
# customer's bid, four phrase and exact keywords, and two ads per ad group,
# both approved. The rows follow the flat dotted shape of the connector's
# search answer; every value is invented. A fixed responder cannot tell one
# query from another, so it answers every search with the campaign's whole
# tree — the campaign row first, then its criteria, ad groups, keywords and
# ads — whatever was asked for.
---
{
  "result": [
    {
      "campaign.resource_name": "customers/1234567890/campaigns/800000001",
      "campaign.id": 800000001,
      "campaign.name": "Example Bakery | Search | Wedding cakes",
      "campaign.status": "PAUSED",
      "campaign.serving_status": "SERVING",
      "campaign.primary_status": "PAUSED",
      "campaign.primary_status_reasons": ["CAMPAIGN_PAUSED"],
      "campaign.advertising_channel_type": "SEARCH",
      "campaign.bidding_strategy_type": "MANUAL_CPC",
      "campaign.network_settings.target_google_search": true,
      "campaign.network_settings.target_search_network": false,
      "campaign.network_settings.target_partner_search_network": false,
      "campaign.network_settings.target_content_network": false,
      "campaign.geo_target_type_setting.positive_geo_target_type": "PRESENCE",
      "campaign.geo_target_type_setting.negative_geo_target_type": "PRESENCE",
      "campaign_budget.resource_name": "customers/1234567890/campaignBudgets/900000001",
      "campaign_budget.amount_micros": 20000000
    },
    {
      "campaign_criterion.resource_name": "customers/1234567890/campaignCriteria/800000001~9000001",
      "campaign_criterion.criterion_id": 9000001,
      "campaign_criterion.type": "LOCATION",
      "campaign_criterion.negative": false,
      "campaign_criterion.location.geo_target_constant": "geoTargetConstants/9000001",
      "campaign_criterion.display_name": "Brooklyn, New York, United States",
      "campaign_criterion.status": "ENABLED"
    },
    {
      "campaign_criterion.resource_name": "customers/1234567890/campaignCriteria/800000001~9100001",
      "campaign_criterion.criterion_id": 9100001,
      "campaign_criterion.type": "KEYWORD",
      "campaign_criterion.negative": true,
      "campaign_criterion.keyword.text": "free",
      "campaign_criterion.keyword.match_type": "PHRASE",
      "campaign_criterion.status": "ENABLED"
    },
    {
      "campaign_criterion.resource_name": "customers/1234567890/campaignCriteria/800000001~9100002",
      "campaign_criterion.criterion_id": 9100002,
      "campaign_criterion.type": "KEYWORD",
      "campaign_criterion.negative": true,
      "campaign_criterion.keyword.text": "jobs",
      "campaign_criterion.keyword.match_type": "PHRASE",
      "campaign_criterion.status": "ENABLED"
    },
    {
      "campaign_criterion.resource_name": "customers/1234567890/campaignCriteria/800000001~9100003",
      "campaign_criterion.criterion_id": 9100003,
      "campaign_criterion.type": "KEYWORD",
      "campaign_criterion.negative": true,
      "campaign_criterion.keyword.text": "recipe",
      "campaign_criterion.keyword.match_type": "PHRASE",
      "campaign_criterion.status": "ENABLED"
    },
    {
      "ad_group.resource_name": "customers/1234567890/adGroups/810000001",
      "ad_group.id": 810000001,
      "ad_group.name": "Wedding cakes",
      "ad_group.status": "ENABLED",
      "ad_group.cpc_bid_micros": 1500000
    },
    {
      "ad_group.resource_name": "customers/1234567890/adGroups/810000002",
      "ad_group.id": 810000002,
      "ad_group.name": "Custom cake orders",
      "ad_group.status": "ENABLED",
      "ad_group.cpc_bid_micros": 1500000
    },
    {
      "ad_group_criterion.resource_name": "customers/1234567890/adGroupCriteria/810000001~9200001",
      "ad_group_criterion.criterion_id": 9200001,
      "ad_group_criterion.keyword.text": "wedding cake brooklyn",
      "ad_group_criterion.keyword.match_type": "PHRASE",
      "ad_group_criterion.status": "ENABLED"
    },
    {
      "ad_group_criterion.resource_name": "customers/1234567890/adGroupCriteria/810000001~9200002",
      "ad_group_criterion.criterion_id": 9200002,
      "ad_group_criterion.keyword.text": "wedding cake bakery near me",
      "ad_group_criterion.keyword.match_type": "EXACT",
      "ad_group_criterion.status": "ENABLED"
    },
    {
      "ad_group_criterion.resource_name": "customers/1234567890/adGroupCriteria/810000002~9200003",
      "ad_group_criterion.criterion_id": 9200003,
      "ad_group_criterion.keyword.text": "custom cake order brooklyn",
      "ad_group_criterion.keyword.match_type": "PHRASE",
      "ad_group_criterion.status": "ENABLED"
    },
    {
      "ad_group_criterion.resource_name": "customers/1234567890/adGroupCriteria/810000002~9200004",
      "ad_group_criterion.criterion_id": 9200004,
      "ad_group_criterion.keyword.text": "birthday cake delivery brooklyn",
      "ad_group_criterion.keyword.match_type": "EXACT",
      "ad_group_criterion.status": "ENABLED"
    },
    {
      "ad_group_ad.resource_name": "customers/1234567890/adGroupAds/810000001~820000001",
      "ad_group_ad.ad.id": 820000001,
      "ad_group_ad.ad.type": "RESPONSIVE_SEARCH_AD",
      "ad_group_ad.ad.final_urls": ["https://www.example-bakery.invalid/wedding-cakes"],
      "ad_group_ad.status": "ENABLED",
      "ad_group_ad.policy_summary.approval_status": "APPROVED",
      "ad_group_ad.policy_summary.review_status": "REVIEWED"
    },
    {
      "ad_group_ad.resource_name": "customers/1234567890/adGroupAds/810000001~820000002",
      "ad_group_ad.ad.id": 820000002,
      "ad_group_ad.ad.type": "RESPONSIVE_SEARCH_AD",
      "ad_group_ad.ad.final_urls": ["https://www.example-bakery.invalid/wedding-cakes"],
      "ad_group_ad.status": "ENABLED",
      "ad_group_ad.policy_summary.approval_status": "APPROVED",
      "ad_group_ad.policy_summary.review_status": "REVIEWED"
    },
    {
      "ad_group_ad.resource_name": "customers/1234567890/adGroupAds/810000002~820000003",
      "ad_group_ad.ad.id": 820000003,
      "ad_group_ad.ad.type": "RESPONSIVE_SEARCH_AD",
      "ad_group_ad.ad.final_urls": ["https://www.example-bakery.invalid/custom-cakes"],
      "ad_group_ad.status": "ENABLED",
      "ad_group_ad.policy_summary.approval_status": "APPROVED",
      "ad_group_ad.policy_summary.review_status": "REVIEWED"
    },
    {
      "ad_group_ad.resource_name": "customers/1234567890/adGroupAds/810000002~820000004",
      "ad_group_ad.ad.id": 820000004,
      "ad_group_ad.ad.type": "RESPONSIVE_SEARCH_AD",
      "ad_group_ad.ad.final_urls": ["https://www.example-bakery.invalid/custom-cakes"],
      "ad_group_ad.status": "ENABLED",
      "ad_group_ad.policy_summary.approval_status": "APPROVED",
      "ad_group_ad.policy_summary.review_status": "REVIEWED"
    }
  ]
}

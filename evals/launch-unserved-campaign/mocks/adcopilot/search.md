---
type: fixed
# The account on day two, as Google Ads reports it: a campaign that is
# switched on, serving and Learning, whose four ads are approved, whose
# account is enabled with billing approved, no spending limit and no pending
# proposal — and which showed ninety times on day one, not at all on day two,
# with no clicks and no spend, most impressions lost to budget and a quarter
# lost to rank. Its search terms report has no rows. The rows follow the flat
# dotted shape of the connector's search answer; every value is invented, and
# the shape of the incident is real. A fixed responder cannot tell one query
# from another, so it answers every search with the account's whole tree —
# the campaign and its two days of numbers, the ads, the customer, the
# account budget, the billing setup — whatever was asked for, and says which
# resources have no rows.
---
{
  "resources_with_no_rows": ["search_term_view", "click_view"],
  "result": [
    {
      "campaign.resource_name": "customers/1234567890/campaigns/800000001",
      "campaign.id": 800000001,
      "campaign.name": "Example Bakery | Search | Wedding cakes",
      "campaign.status": "ENABLED",
      "campaign.serving_status": "SERVING",
      "campaign.primary_status": "LEARNING",
      "campaign.primary_status_reasons": ["BIDDING_STRATEGY_LEARNING"],
      "campaign.advertising_channel_type": "SEARCH",
      "campaign.bidding_strategy_type": "TARGET_SPEND",
      "campaign.target_spend.cpc_bid_ceiling_micros": 1500000,
      "campaign.network_settings.target_google_search": true,
      "campaign.network_settings.target_search_network": false,
      "campaign.network_settings.target_partner_search_network": false,
      "campaign.network_settings.target_content_network": false,
      "campaign.geo_target_type_setting.positive_geo_target_type": "PRESENCE",
      "campaign_budget.resource_name": "customers/1234567890/campaignBudgets/900000001",
      "campaign_budget.amount_micros": 20000000,
      "segments.date": "2026-09-21",
      "metrics.impressions": 90,
      "metrics.clicks": 0,
      "metrics.cost_micros": 0,
      "metrics.search_impression_share": 0.0999,
      "metrics.search_budget_lost_impression_share": 0.7001,
      "metrics.search_rank_lost_impression_share": 0.2671
    },
    {
      "campaign.resource_name": "customers/1234567890/campaigns/800000001",
      "campaign.id": 800000001,
      "campaign.name": "Example Bakery | Search | Wedding cakes",
      "campaign.status": "ENABLED",
      "campaign.serving_status": "SERVING",
      "campaign.primary_status": "LEARNING",
      "campaign.primary_status_reasons": ["BIDDING_STRATEGY_LEARNING"],
      "segments.date": "2026-09-22",
      "metrics.impressions": 0,
      "metrics.clicks": 0,
      "metrics.cost_micros": 0,
      "metrics.search_impression_share": 0.0,
      "metrics.search_budget_lost_impression_share": 0.8412,
      "metrics.search_rank_lost_impression_share": 0.1588
    },
    {
      "ad_group_ad.resource_name": "customers/1234567890/adGroupAds/810000001~820000001",
      "ad_group_ad.ad.id": 820000001,
      "ad_group_ad.ad.type": "RESPONSIVE_SEARCH_AD",
      "ad_group_ad.status": "ENABLED",
      "ad_group_ad.primary_status": "ELIGIBLE",
      "ad_group_ad.policy_summary.approval_status": "APPROVED",
      "ad_group_ad.policy_summary.review_status": "REVIEWED"
    },
    {
      "ad_group_ad.resource_name": "customers/1234567890/adGroupAds/810000001~820000002",
      "ad_group_ad.ad.id": 820000002,
      "ad_group_ad.ad.type": "RESPONSIVE_SEARCH_AD",
      "ad_group_ad.status": "ENABLED",
      "ad_group_ad.primary_status": "ELIGIBLE",
      "ad_group_ad.policy_summary.approval_status": "APPROVED",
      "ad_group_ad.policy_summary.review_status": "REVIEWED"
    },
    {
      "ad_group_ad.resource_name": "customers/1234567890/adGroupAds/810000002~820000003",
      "ad_group_ad.ad.id": 820000003,
      "ad_group_ad.ad.type": "RESPONSIVE_SEARCH_AD",
      "ad_group_ad.status": "ENABLED",
      "ad_group_ad.primary_status": "ELIGIBLE",
      "ad_group_ad.policy_summary.approval_status": "APPROVED",
      "ad_group_ad.policy_summary.review_status": "REVIEWED"
    },
    {
      "ad_group_ad.resource_name": "customers/1234567890/adGroupAds/810000002~820000004",
      "ad_group_ad.ad.id": 820000004,
      "ad_group_ad.ad.type": "RESPONSIVE_SEARCH_AD",
      "ad_group_ad.status": "ENABLED",
      "ad_group_ad.primary_status": "ELIGIBLE",
      "ad_group_ad.policy_summary.approval_status": "APPROVED",
      "ad_group_ad.policy_summary.review_status": "REVIEWED"
    },
    {
      "customer.resource_name": "customers/1234567890",
      "customer.id": 1234567890,
      "customer.descriptive_name": "Example Bakery",
      "customer.status": "ENABLED",
      "customer.currency_code": "USD",
      "customer.time_zone": "America/New_York",
      "customer.conversion_tracking_setting.conversion_tracking_status": "NOT_CONVERSION_TRACKED",
      "customer.pay_per_conversion_eligibility_failure_reasons": ["NOT_ENOUGH_CONVERSIONS"]
    },
    {
      "account_budget.resource_name": "customers/1234567890/accountBudgets/700000001",
      "account_budget.id": 700000001,
      "account_budget.status": "APPROVED",
      "account_budget.approved_spending_limit_type": "INFINITE",
      "account_budget.approved_spending_limit_micros": 0,
      "account_budget.amount_served_micros": 0,
      "account_budget.pending_proposal.proposal_type": "UNSPECIFIED",
      "account_budget.pending_proposal.spending_limit_type": "UNSPECIFIED",
      "account_budget.notes": "",
      "account_budget.approved_start_date_time": "2026-09-14 09:12:40",
      "account_budget.approved_end_time_type": "FOREVER"
    },
    {
      "billing_setup.resource_name": "customers/1234567890/billingSetups/600000001",
      "billing_setup.id": 600000001,
      "billing_setup.status": "APPROVED",
      "billing_setup.start_date_time": "2026-09-14 09:12:40",
      "billing_setup.end_time_type": "FOREVER",
      "billing_setup.payments_account_info.payments_account_name": "Example Bakery"
    }
  ]
}

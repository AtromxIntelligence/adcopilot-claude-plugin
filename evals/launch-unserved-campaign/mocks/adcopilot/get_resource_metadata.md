---
type: fixed
# The fields a delivery read and a disagreement check need, for the five
# resources they touch, cut down from the Google Ads API's own lists. A fixed
# responder answers every metadata request with all five, whichever resource
# was asked for; the names are the API's, and the campaign's metrics fields
# are listed with it because that is where impression share is read.
---
{
  "resources": {
    "campaign": {
      "selectable": [
        "campaign.id", "campaign.name", "campaign.status", "campaign.serving_status",
        "campaign.primary_status", "campaign.primary_status_reasons",
        "campaign.advertising_channel_type", "campaign.bidding_strategy_type",
        "campaign.target_spend.cpc_bid_ceiling_micros",
        "campaign.network_settings.target_google_search", "campaign.network_settings.target_search_network",
        "campaign.network_settings.target_partner_search_network", "campaign.network_settings.target_content_network",
        "campaign.geo_target_type_setting.positive_geo_target_type",
        "campaign_budget.amount_micros", "segments.date",
        "metrics.impressions", "metrics.clicks", "metrics.cost_micros",
        "metrics.search_impression_share", "metrics.search_budget_lost_impression_share",
        "metrics.search_rank_lost_impression_share"
      ],
      "filterable": ["campaign.id", "campaign.name", "campaign.status", "campaign.primary_status", "segments.date"],
      "sortable": ["campaign.id", "campaign.name", "segments.date"]
    },
    "ad_group_ad": {
      "selectable": [
        "ad_group_ad.ad.id", "ad_group_ad.ad.type", "ad_group_ad.status", "ad_group_ad.primary_status",
        "ad_group_ad.primary_status_reasons", "ad_group_ad.policy_summary.approval_status",
        "ad_group_ad.policy_summary.review_status", "metrics.impressions", "metrics.clicks", "metrics.cost_micros"
      ],
      "filterable": ["ad_group_ad.status", "ad_group_ad.policy_summary.approval_status"],
      "sortable": ["ad_group_ad.ad.id"]
    },
    "customer": {
      "selectable": [
        "customer.id", "customer.descriptive_name", "customer.status", "customer.currency_code", "customer.time_zone",
        "customer.conversion_tracking_setting.conversion_tracking_status",
        "customer.pay_per_conversion_eligibility_failure_reasons"
      ],
      "filterable": ["customer.id", "customer.status"],
      "sortable": ["customer.id"]
    },
    "account_budget": {
      "selectable": [
        "account_budget.id", "account_budget.status", "account_budget.approved_spending_limit_type",
        "account_budget.approved_spending_limit_micros", "account_budget.amount_served_micros",
        "account_budget.pending_proposal.proposal_type", "account_budget.pending_proposal.spending_limit_type",
        "account_budget.notes", "account_budget.approved_start_date_time", "account_budget.approved_end_time_type"
      ],
      "filterable": ["account_budget.id", "account_budget.status"],
      "sortable": ["account_budget.id"]
    },
    "billing_setup": {
      "selectable": [
        "billing_setup.id", "billing_setup.status", "billing_setup.start_date_time", "billing_setup.end_time_type",
        "billing_setup.payments_account_info.payments_account_name"
      ],
      "filterable": ["billing_setup.id", "billing_setup.status"],
      "sortable": ["billing_setup.id"]
    },
    "search_term_view": {
      "selectable": ["search_term_view.search_term", "search_term_view.status", "search_term_view.ad_group", "metrics.impressions", "metrics.clicks", "metrics.cost_micros"],
      "filterable": ["search_term_view.search_term", "search_term_view.status"],
      "sortable": ["search_term_view.search_term"]
    }
  }
}

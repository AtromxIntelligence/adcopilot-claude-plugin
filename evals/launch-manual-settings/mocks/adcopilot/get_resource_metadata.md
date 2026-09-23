---
type: fixed
# The campaign resource's fields, cut down to the ones a settings read-back
# needs. The names are the Google Ads API's own; a fixed responder answers
# every metadata request with this same list, whichever resource was asked
# for.
---
{
  "resource": "campaign",
  "selectable": [
    "campaign.advertising_channel_type",
    "campaign.bidding_strategy_type",
    "campaign.campaign_budget",
    "campaign.geo_target_type_setting.negative_geo_target_type",
    "campaign.geo_target_type_setting.positive_geo_target_type",
    "campaign.id",
    "campaign.name",
    "campaign.network_settings.target_content_network",
    "campaign.network_settings.target_google_search",
    "campaign.network_settings.target_partner_search_network",
    "campaign.network_settings.target_search_network",
    "campaign.primary_status",
    "campaign.primary_status_reasons",
    "campaign.resource_name",
    "campaign.serving_status",
    "campaign.status",
    "campaign_budget.amount_micros",
    "campaign_budget.resource_name"
  ],
  "filterable": [
    "campaign.advertising_channel_type",
    "campaign.id",
    "campaign.name",
    "campaign.primary_status",
    "campaign.serving_status",
    "campaign.status"
  ],
  "sortable": [
    "campaign.id",
    "campaign.name",
    "campaign.status"
  ]
}

---
type: fixed
# The fields the four reads need, cut down from the Google Ads API's own lists;
# a fixed responder answers every request with all of them.
---
{
  "resources": {
    "campaign": {
      "selectable": [
        "campaign.id",
        "campaign.name",
        "campaign.status",
        "campaign_budget.amount_micros",
        "segments.date",
        "metrics.impressions",
        "metrics.clicks",
        "metrics.cost_micros",
        "metrics.conversions",
        "metrics.cost_per_conversion"
      ],
      "filterable": [
        "campaign.id",
        "campaign.status",
        "segments.date"
      ],
      "sortable": [
        "campaign.id",
        "segments.date"
      ]
    },
    "customer": {
      "selectable": [
        "customer.id",
        "customer.descriptive_name",
        "segments.date",
        "metrics.impressions",
        "metrics.clicks",
        "metrics.cost_micros",
        "metrics.conversions"
      ],
      "filterable": [
        "segments.date"
      ],
      "sortable": [
        "segments.date"
      ]
    },
    "ad_group_ad": {
      "selectable": [
        "ad_group_ad.ad.id",
        "ad_group.name",
        "ad_group_ad.status",
        "ad_group_ad.policy_summary.approval_status",
        "ad_group_ad.policy_summary.review_status",
        "ad_group_ad.policy_summary.policy_topic_entries",
        "ad_group_ad.ad.final_urls"
      ],
      "filterable": [
        "ad_group_ad.status",
        "ad_group_ad.policy_summary.approval_status"
      ],
      "sortable": [
        "ad_group_ad.ad.id"
      ]
    },
    "change_event": {
      "selectable": [
        "change_event.change_date_time",
        "change_event.change_resource_type",
        "change_event.resource_change_operation",
        "change_event.user_email",
        "change_event.client_type",
        "change_event.changed_fields",
        "change_event.old_resource",
        "change_event.new_resource",
        "change_event.campaign"
      ],
      "filterable": [
        "change_event.change_date_time",
        "change_event.change_resource_type"
      ],
      "sortable": [
        "change_event.change_date_time"
      ]
    }
  }
}

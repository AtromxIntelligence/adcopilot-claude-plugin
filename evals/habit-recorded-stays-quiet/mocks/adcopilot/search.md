---
type: fixed
# A fixed responder cannot tell one query from another, so every search is
# answered with the account's whole tree: eight days of the campaign's numbers
# (yesterday is 2026-09-23), its two ads (one disapproved: Google says the
# landing page does not work), and the last day's two changes (a person raised
# the budget in Google Ads; Google's auto-apply added a broad keyword). Rows
# follow the connector's flat dotted shape; every value is invented.
---
{
  "resources_with_no_rows": [],
  "result": [
    {
      "campaign.id": 800000001,
      "campaign.name": "Example Bakery | Search | Wedding cakes",
      "campaign.status": "ENABLED",
      "segments.date": "2026-09-16",
      "metrics.cost_micros": 19800000,
      "metrics.clicks": 8,
      "metrics.impressions": 248,
      "metrics.conversions": 0.0
    },
    {
      "campaign.id": 800000001,
      "campaign.name": "Example Bakery | Search | Wedding cakes",
      "campaign.status": "ENABLED",
      "segments.date": "2026-09-17",
      "metrics.cost_micros": 20400000,
      "metrics.clicks": 9,
      "metrics.impressions": 279,
      "metrics.conversions": 1.0
    },
    {
      "campaign.id": 800000001,
      "campaign.name": "Example Bakery | Search | Wedding cakes",
      "campaign.status": "ENABLED",
      "segments.date": "2026-09-18",
      "metrics.cost_micros": 18900000,
      "metrics.clicks": 7,
      "metrics.impressions": 217,
      "metrics.conversions": 0.0
    },
    {
      "campaign.id": 800000001,
      "campaign.name": "Example Bakery | Search | Wedding cakes",
      "campaign.status": "ENABLED",
      "segments.date": "2026-09-19",
      "metrics.cost_micros": 21300000,
      "metrics.clicks": 9,
      "metrics.impressions": 279,
      "metrics.conversions": 1.0
    },
    {
      "campaign.id": 800000001,
      "campaign.name": "Example Bakery | Search | Wedding cakes",
      "campaign.status": "ENABLED",
      "segments.date": "2026-09-20",
      "metrics.cost_micros": 17600000,
      "metrics.clicks": 6,
      "metrics.impressions": 186,
      "metrics.conversions": 0.0
    },
    {
      "campaign.id": 800000001,
      "campaign.name": "Example Bakery | Search | Wedding cakes",
      "campaign.status": "ENABLED",
      "segments.date": "2026-09-21",
      "metrics.cost_micros": 19100000,
      "metrics.clicks": 8,
      "metrics.impressions": 248,
      "metrics.conversions": 1.0
    },
    {
      "campaign.id": 800000001,
      "campaign.name": "Example Bakery | Search | Wedding cakes",
      "campaign.status": "ENABLED",
      "segments.date": "2026-09-22",
      "metrics.cost_micros": 20200000,
      "metrics.clicks": 8,
      "metrics.impressions": 248,
      "metrics.conversions": 0.0
    },
    {
      "campaign.id": 800000001,
      "campaign.name": "Example Bakery | Search | Wedding cakes",
      "campaign.status": "ENABLED",
      "segments.date": "2026-09-23",
      "metrics.cost_micros": 26700000,
      "metrics.clicks": 11,
      "metrics.impressions": 341,
      "metrics.conversions": 0.0
    },
    {
      "ad_group_ad.ad.id": 700000011,
      "ad_group.name": "Wedding cakes",
      "ad_group_ad.status": "ENABLED",
      "ad_group_ad.policy_summary.approval_status": "DISAPPROVED",
      "ad_group_ad.policy_summary.review_status": "REVIEWED",
      "ad_group_ad.policy_summary.policy_topic_entries": [
        {
          "topic": "DESTINATION_NOT_WORKING",
          "type": "PROHIBITED"
        }
      ],
      "ad_group_ad.ad.final_urls": [
        "https://www.example-bakery.invalid/wedding-cakes/tasting"
      ]
    },
    {
      "ad_group_ad.ad.id": 700000012,
      "ad_group.name": "Wedding cakes",
      "ad_group_ad.status": "ENABLED",
      "ad_group_ad.policy_summary.approval_status": "APPROVED",
      "ad_group_ad.policy_summary.review_status": "REVIEWED",
      "ad_group_ad.policy_summary.policy_topic_entries": [],
      "ad_group_ad.ad.final_urls": [
        "https://www.example-bakery.invalid/wedding-cakes"
      ]
    },
    {
      "change_event.change_date_time": "2026-09-23 16:42:10",
      "change_event.change_resource_type": "CAMPAIGN_BUDGET",
      "change_event.resource_change_operation": "UPDATE",
      "change_event.user_email": "maria@example-bakery.invalid",
      "change_event.client_type": "GOOGLE_ADS_WEB_CLIENT",
      "change_event.changed_fields": "amount_micros",
      "change_event.old_resource": {
        "campaign_budget": {
          "amount_micros": 20000000
        }
      },
      "change_event.new_resource": {
        "campaign_budget": {
          "amount_micros": 30000000
        }
      },
      "change_event.campaign": "customers/1234567890/campaigns/800000001"
    },
    {
      "change_event.change_date_time": "2026-09-23 22:05:51",
      "change_event.change_resource_type": "AD_GROUP_CRITERION",
      "change_event.resource_change_operation": "CREATE",
      "change_event.user_email": "Recommendations Auto-Apply",
      "change_event.client_type": "GOOGLE_ADS_RECOMMENDATIONS",
      "change_event.changed_fields": "keyword.text,keyword.match_type",
      "change_event.new_resource": {
        "ad_group_criterion": {
          "keyword": {
            "text": "custom cakes",
            "match_type": "BROAD"
          }
        }
      },
      "change_event.campaign": "customers/1234567890/campaigns/800000001"
    }
  ]
}

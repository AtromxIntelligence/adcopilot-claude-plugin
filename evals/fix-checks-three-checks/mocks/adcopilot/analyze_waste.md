---
type: fixed
# The G-WS1 read: four keywords that spent over thirty days with no
# conversion, each with the IDs a pause needs. Every value is invented.
---
{
  "tool": "analyze_waste",
  "customer_id": "1234567890",
  "currency": "USD",
  "window_days": 30,
  "total_waste": {
    "cost_micros": 518000000,
    "cost_display": "$518",
    "share_of_spend": 0.12
  },
  "findings": [
    {
      "rank": 1,
      "type": "zero_converting_keywords",
      "check_id": "G-WS1",
      "title": "4 keywords spent with no conversions",
      "cost_micros": 518000000,
      "cost_display": "$518",
      "clicks": 233,
      "conversions": 0.0,
      "keywords": [
        {"keyword": "cake shop", "match_type": "BROAD", "campaign": "Example Bakery | Search | Celebration cakes", "ad_group_id": "900000011", "criterion_id": "700000101", "cost_micros": 211000000, "cost_display": "$211", "clicks": 96, "conversions": 0.0},
        {"keyword": "bakery", "match_type": "BROAD", "campaign": "Example Bakery | Search | Celebration cakes", "ad_group_id": "900000011", "criterion_id": "700000102", "cost_micros": 148000000, "cost_display": "$148", "clicks": 67, "conversions": 0.0},
        {"keyword": "cupcakes", "match_type": "PHRASE", "campaign": "Example Bakery | Search | Celebration cakes", "ad_group_id": "900000012", "criterion_id": "700000103", "cost_micros": 97000000, "cost_display": "$97", "clicks": 41, "conversions": 0.0},
        {"keyword": "dessert delivery", "match_type": "PHRASE", "campaign": "Example Bakery | Search | Wedding cakes", "ad_group_id": "900000013", "criterion_id": "700000104", "cost_micros": 62000000, "cost_display": "$62", "clicks": 29, "conversions": 0.0}
      ],
      "fix": {
        "tool": "update_keyword",
        "note": "Pause each with status PAUSED; never remove."
      }
    }
  ]
}

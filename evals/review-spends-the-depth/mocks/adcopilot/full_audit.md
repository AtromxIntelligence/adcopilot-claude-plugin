---
type: fixed
# A fixed responder cannot tell depth="quick" from depth="deep", so it answers as
# a deep run does and states its coverage in the body: 61 of the 73 checks were
# scored, 12 could not be. The skill's job is to have ASKED for deep, and to say
# that 61 rather than let the 12 pass as passes.
# The three findings are returned in the lens's own order, which the tool's
# description states is failures first then SEVERITY, not impact - and the
# severities deliberately disagree with the money. S41 is the most severe and
# costs $62; W16 is the expensive one at $1,284 over thirty days; T31 sits
# between them. Amounts are in micros, as the lens returns them, each beside the
# *_display twin the skill says to quote. Every value is invented.
---
{
  "tool": "full_audit",
  "depth": "deep",
  "customer_id": "1234567890",
  "currency": "USD",
  "date_range": {
    "start": "2026-09-06",
    "end": "2026-10-05",
    "days": 30
  },
  "health": {
    "score": 64,
    "grade": "C"
  },
  "coverage": {
    "checks_in_registry": 73,
    "checks_scored": 61,
    "checks_not_scored": 12,
    "not_scored_reason": "no data in the window for those checks"
  },
  "totals": {
    "cost_micros": 4318000000,
    "cost_display": "$4,318",
    "clicks": 1948,
    "impressions": 61200,
    "conversions": 97.0,
    "cost_per_conversion_display": "$44.51"
  },
  "findings": [
    {
      "check_id": "S41",
      "status": "failing",
      "severity": "critical",
      "section": "settings_targeting",
      "title": "Search partners and the Display network are on for a Search campaign",
      "detail": "Both campaigns are opted in to Google's partner sites and to Display. Those placements are not the search results the keywords were written for.",
      "impact": {
        "metric": "wasted_cost_micros",
        "value": 62000000,
        "value_display": "$62",
        "window_days": 30,
        "clicks": 94
      },
      "fix": {
        "tool": "update_campaign",
        "args": {
          "customer_id": "1234567890",
          "campaign_id": "800000001",
          "network_settings": {
            "target_search_network": false,
            "target_content_network": false
          }
        }
      }
    },
    {
      "check_id": "W16",
      "status": "failing",
      "severity": "high",
      "section": "wasted_spend",
      "title": "Searches paid for that brought nothing",
      "detail": "Forty-one searches took money over the window and returned no result at all. The broad keyword 'cake' matched most of them.",
      "impact": {
        "metric": "wasted_cost_micros",
        "value": 1284000000,
        "value_display": "$1,284",
        "window_days": 30,
        "clicks": 561,
        "search_terms": 41
      },
      "fix": {
        "tool": "analyze_search_terms",
        "args": {
          "customer_id": "1234567890",
          "days": 30
        }
      }
    },
    {
      "check_id": "T31",
      "status": "warning",
      "severity": "high",
      "section": "structure",
      "title": "One ad group holds every keyword in the wedding campaign",
      "detail": "Thirty-one keywords share ad group 900000001, so one pair of ads has to answer all of them and none of them closely.",
      "impact": {
        "metric": "wasted_cost_micros",
        "value": 96000000,
        "value_display": "$96",
        "window_days": 30,
        "clicks": 142
      }
    }
  ],
  "notes": [
    "Findings are ordered failures first, then by severity. Severity is the kind of fault, not the amount of money: re-rank by impact before reporting."
  ]
}

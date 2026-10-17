---
type: fixed
# The deep audit of the same fictional account (every value invented): $1,865
# over 2026-09-06..2026-10-05, nothing counted. It scored 55 of the 73 checks.
# The tag check names only a length ("the last 7 days"), as the live server's
# does, and its seven days end on date_range.end. related_reads names
# analyze_waste (and conversion_setup_audit), as the live result did in the
# conversation this case comes from. The case does not grade whether
# analyze_waste is run: on a five-read answer it may be the read left over, and
# what is graded is that a read left over is not called a limit.
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
    "score": 41,
    "grade": "F"
  },
  "coverage": {
    "checks_in_registry": 73,
    "checks_scored": 55,
    "checks_not_scored": 18,
    "not_scored_reason": "9 need a Performance Max campaign, 3 need the business profile, 1 needs Tag Manager, 5 need more data in the window"
  },
  "totals": {
    "cost_micros": 1865000000,
    "cost_display": "$1,865",
    "clicks": 607,
    "impressions": 18400,
    "conversions": 0.0,
    "cost_per_conversion_display": null
  },
  "findings": [
    {
      "check_id": "G-CT3",
      "status": "failing",
      "severity": "critical",
      "section": "conversion_tracking",
      "title": "Google tag firing",
      "detail": "2 of your 2 main conversion actions recorded no result in the last 7 days while the account took 141 clicks. That is what a missing or broken tag on the page where the result happens looks like.",
      "impact": {
        "metric": "clicks_without_signal",
        "value": 141,
        "window_days": 7
      }
    },
    {
      "check_id": "G16",
      "status": "warning",
      "severity": "high",
      "section": "wasted_spend",
      "title": "Search terms with spend and no conversion",
      "detail": "No conversion was recorded anywhere in this account in the window, so spend on searches cannot be called waste until tracking is checked.",
      "impact": {
        "metric": "cost_micros",
        "value": 583000000,
        "value_display": "$583",
        "window_days": 30,
        "search_terms": 27
      }
    },
    {
      "check_id": "G24",
      "status": "warning",
      "severity": "medium",
      "section": "keywords_qs",
      "title": "Landing page experience below average",
      "detail": "Every rated keyword has a below-average landing page experience; the average Quality Score is 4.3.",
      "impact": {
        "metric": "cost_micros",
        "value": 1102000000,
        "value_display": "$1,102",
        "window_days": 30
      }
    }
  ],
  "notes": [
    "Findings are ordered failures first, then by severity. Severity is the kind of fault, not the amount of money: re-rank by impact before reporting."
  ],
  "related_reads": [
    {
      "tool": "analyze_waste",
      "args": {
        "customer_id": "1234567890",
        "days": 30
      },
      "why": "27 search terms took 583 USD of the 1865 USD spent with no conversion; the waste read ranks where the money went."
    },
    {
      "tool": "conversion_setup_audit",
      "args": {
        "customer_id": "1234567890",
        "days": 30
      },
      "why": "2 of 2 primary conversion actions recorded nothing in 7 days while the account took 141 clicks; the setup read says what is counted."
    }
  ]
}

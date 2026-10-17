---
type: fixed
# The deep audit over the 14 days 2026-09-30..2026-10-13, the account's own
# yesterday (AdCopilot v2.41.0, D185), in v2.41.0's wording: the tag check
# names its seven days (7 Oct to 13 Oct), the health line counts the checks
# that gave a result (58 of 73), and G-AD2 is not graded against the US
# click-through average for an account set up outside the US (#822). G16 lists
# the costliest searches, as it does on an account that counted results.
---
{
  "tool": "full_audit",
  "depth": "deep",
  "customer_id": "4455667788",
  "currency": "INR",
  "time_zone": "Asia/Kolkata",
  "date_range": {
    "start": "2026-09-30",
    "end": "2026-10-13",
    "days": 14
  },
  "data_through": "2026-10-13",
  "counts": {
    "fail": 1,
    "warning": 2,
    "pass": 55,
    "returned": 3
  },
  "totals": {
    "cost_micros": 45210000000,
    "cost_display": "₹45,210",
    "clicks": 903,
    "impressions": 22700,
    "conversions": 31.0,
    "cost_per_conversion_display": "₹1,458"
  },
  "findings": [
    {
      "check_id": "G-CT3",
      "status": "fail",
      "severity": "critical",
      "category": "conversion_tracking",
      "title": "Google tag firing",
      "detail": "1 primary action(s) recorded no conversion at all in the 7 days from 7 Oct to 13 Oct while the account took 448 clicks, which is what a tag that is missing or broken on the key page looks like.",
      "evidence": {
        "columns": [
          "conversion_action",
          "conversions_7d"
        ],
        "rows": [
          [
            "Call from website",
            0.0
          ]
        ],
        "row_count": 1,
        "truncated": false,
        "handle": null
      },
      "impact": {
        "metric": "clicks_without_signal",
        "value": 448,
        "window_days": 7
      }
    },
    {
      "check_id": "G16",
      "status": "warning",
      "severity": "high",
      "category": "wasted_spend",
      "title": "Search terms with spend and no conversion",
      "detail": "21 search terms with 3 or more clicks converted nothing in the 14 days from 30 Sep to 13 Oct, ₹18,240 in all.",
      "evidence": {
        "columns": [
          "search_term",
          "clicks",
          "cost"
        ],
        "rows": [
          [
            "dentist jobs bangalore",
            18,
            "₹4,120"
          ],
          [
            "free dental camp",
            15,
            "₹3,560"
          ],
          [
            "teeth whitening kit",
            12,
            "₹2,890"
          ],
          [
            "dental college admission",
            9,
            "₹1,980"
          ],
          [
            "how to stop tooth pain at home",
            8,
            "₹1,610"
          ]
        ],
        "row_count": 21,
        "truncated": true,
        "handle": null
      },
      "impact": {
        "metric": "cost_micros",
        "value": 18240000000,
        "value_display": "₹18,240",
        "window_days": 14,
        "search_terms": 21
      }
    },
    {
      "check_id": "G24",
      "status": "warning",
      "severity": "medium",
      "category": "keywords_qs",
      "title": "Landing page experience below average",
      "detail": "6 of 14 rated keywords have a below-average landing page experience.",
      "impact": {
        "metric": "cost_micros",
        "value": 9800000000,
        "value_display": "₹9,800",
        "window_days": 14
      }
    }
  ],
  "coverage": [
    {
      "check_id": "G-AD2",
      "status": "not_evaluated",
      "reason_code": "NO_MARKET_BENCHMARK",
      "reason": "Not graded: the 6.66% benchmark comes from a 2025 industry study of US Google Ads campaigns by WordStream and LocaliQ, and this account is set up outside the US (its currency is INR), so AdCopilot does not compare its click-through rate with that figure. Its Search click-through rate in this window is 3.98%; Google's own expected click-through rating for each keyword compares its ads with others shown on the same searches."
    },
    {
      "check_id": "PMAX-1",
      "status": "not_evaluated",
      "reason_code": "NOT_APPLICABLE"
    },
    {
      "check_id": "PMAX-2",
      "status": "not_evaluated",
      "reason_code": "NOT_APPLICABLE"
    },
    {
      "check_id": "PMAX-3",
      "status": "not_evaluated",
      "reason_code": "NOT_APPLICABLE"
    },
    {
      "check_id": "PMAX-4",
      "status": "not_evaluated",
      "reason_code": "NOT_APPLICABLE"
    },
    {
      "check_id": "PMAX-5",
      "status": "not_evaluated",
      "reason_code": "NOT_APPLICABLE"
    },
    {
      "check_id": "PMAX-6",
      "status": "not_evaluated",
      "reason_code": "NOT_APPLICABLE"
    },
    {
      "check_id": "PMAX-7",
      "status": "not_evaluated",
      "reason_code": "NOT_APPLICABLE"
    },
    {
      "check_id": "PMAX-8",
      "status": "not_evaluated",
      "reason_code": "NOT_APPLICABLE"
    },
    {
      "check_id": "PMAX-9",
      "status": "not_evaluated",
      "reason_code": "NOT_APPLICABLE"
    },
    {
      "check_id": "PMAX-10",
      "status": "not_evaluated",
      "reason_code": "NOT_APPLICABLE"
    },
    {
      "check_id": "PMAX-11",
      "status": "not_evaluated",
      "reason_code": "NOT_APPLICABLE"
    },
    {
      "check_id": "PMAX-12",
      "status": "not_evaluated",
      "reason_code": "NOT_APPLICABLE"
    },
    {
      "check_id": "PMAX-13",
      "status": "not_evaluated",
      "reason_code": "NOT_APPLICABLE"
    },
    {
      "check_id": "PMAX-14",
      "status": "not_evaluated",
      "reason_code": "NOT_APPLICABLE"
    }
  ],
  "notes": [
    "Findings are ordered failures first, then by severity. Severity is the kind of fault, not the amount of money: re-rank by impact before reporting."
  ],
  "narrative": "**full_audit** — account 4455667788, 2026-09-30 to 2026-10-13 (14 days), amounts in INR. Health score 58/100 (grade D), from the 58 of 73 checks that gave a result. 1 failing, 2 warning, 55 passing (top 3 listed); 15 checks not evaluated.",
  "health": {
    "score": 58,
    "grade": "D",
    "checks_evaluated": 58,
    "checks_total": 73
  },
  "related_reads": [
    {
      "tool": "analyze_search_terms",
      "args": {
        "customer_id": "4455667788",
        "days": 14
      },
      "why": "21 search terms took ₹18,240 of the ₹45,210 spent with no conversion; the search-terms read lists the costliest by name and groups them into themes."
    }
  ]
}

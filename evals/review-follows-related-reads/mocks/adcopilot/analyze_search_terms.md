---
type: fixed
# The same $1,284 of waste, grouped into the themes the lens names, each with the
# add_negative_keywords call that acts on it - PHRASE match, the search as typed,
# never broad. Every value is invented.
---
{
  "tool": "analyze_search_terms",
  "customer_id": "1234567890",
  "currency": "USD",
  "window_days": 30,
  "terms_reviewed": 412,
  "candidates": [
    {
      "theme": "informational",
      "terms": 17,
      "cost_micros": 611000000,
      "cost_display": "$611",
      "clicks": 273,
      "conversions": 0.0,
      "examples": [
        "cake recipes",
        "how to bake a cake",
        "cake decorating ideas"
      ],
      "call": {
        "tool": "add_negative_keywords",
        "args": {
          "customer_id": "1234567890",
          "campaign_id": "800000001",
          "match_type": "PHRASE",
          "keywords": [
            "cake recipes",
            "how to bake a cake",
            "cake decorating ideas"
          ]
        }
      }
    },
    {
      "theme": "free_intent",
      "terms": 9,
      "cost_micros": 356000000,
      "cost_display": "$356",
      "clicks": 160,
      "conversions": 1.0,
      "examples": [
        "free cake samples",
        "cheap cake near me"
      ],
      "call": {
        "tool": "add_negative_keywords",
        "args": {
          "customer_id": "1234567890",
          "campaign_id": "800000001",
          "match_type": "PHRASE",
          "keywords": [
            "free cake samples",
            "cheap cake"
          ]
        }
      }
    },
    {
      "theme": "job_seeker",
      "terms": 6,
      "cost_micros": 231000000,
      "cost_display": "$231",
      "clicks": 103,
      "conversions": 0.0,
      "examples": [
        "cake decorating jobs",
        "baker vacancies brooklyn"
      ],
      "call": {
        "tool": "add_negative_keywords",
        "args": {
          "customer_id": "1234567890",
          "campaign_id": "800000001",
          "match_type": "PHRASE",
          "keywords": [
            "jobs",
            "vacancies",
            "hiring"
          ]
        }
      }
    },
    {
      "theme": "competitor",
      "terms": 9,
      "cost_micros": 86000000,
      "cost_display": "$86",
      "clicks": 25,
      "conversions": 0.0,
      "examples": [
        "other bakery brooklyn"
      ],
      "call": null,
      "note": "Left as a candidate only: a competitor search can still convert, so this one is the customer's call."
    }
  ],
  "notes": [
    "Broad-match negatives are never proposed."
  ]
}

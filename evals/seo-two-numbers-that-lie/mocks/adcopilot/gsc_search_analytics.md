---
type: fixed
# A fixed responder cannot tell one date range or dimension list from another, so
# this one answer carries both breakdowns the skill asks for, each labelled, and
# the whole 28-day window ends three days back as the skill says to end it.
# This is the second number that lies. By query alone, "example bakery" sits at
# average position 3.4 - and that average is taken across every country and
# device where the page appeared at all. Split by country, the market this
# business actually sells in is position 28.6 with 41 impressions and 1 click,
# while Germany, where it cannot deliver a cake, is 1.8 with 812 impressions.
# Reading the 3.4 out as "you rank third for your own name" is the failure.
# Every value is invented.
---
{
  "note": "Rows for the window 2026-09-06 to 2026-10-03 (ends three days back; Search Console has not finished counting the days after that). Two row sets are included because this fixture answers any dimension list: read the one that matches what you asked for. Positions are averages over the window, not live ranks.",
  "window": {
    "start_date": "2026-09-06",
    "end_date": "2026-10-03",
    "days": 28
  },
  "totals": {
    "clicks": 61,
    "impressions": 4188,
    "ctr": 0.0146,
    "position": 24.7
  },
  "rows_by_query": [
    {
      "keys": [
        "example bakery"
      ],
      "clicks": 14,
      "impressions": 903,
      "ctr": 0.0155,
      "position": 3.4
    },
    {
      "keys": [
        "wedding cakes brooklyn"
      ],
      "clicks": 9,
      "impressions": 221,
      "ctr": 0.0407,
      "position": 11.2
    },
    {
      "keys": [
        "cake recipes"
      ],
      "clicks": 6,
      "impressions": 1740,
      "ctr": 0.0034,
      "position": 46.8
    },
    {
      "keys": [
        "birthday cake delivery"
      ],
      "clicks": 5,
      "impressions": 318,
      "ctr": 0.0157,
      "position": 18.9
    },
    {
      "keys": [
        "how to bake a cake"
      ],
      "clicks": 2,
      "impressions": 806,
      "ctr": 0.0025,
      "position": 61.3
    }
  ],
  "rows_by_query_and_country": [
    {
      "keys": [
        "example bakery",
        "deu"
      ],
      "clicks": 12,
      "impressions": 812,
      "ctr": 0.0148,
      "position": 1.8
    },
    {
      "keys": [
        "example bakery",
        "usa"
      ],
      "clicks": 1,
      "impressions": 41,
      "ctr": 0.0244,
      "position": 28.6
    },
    {
      "keys": [
        "example bakery",
        "aut"
      ],
      "clicks": 1,
      "impressions": 50,
      "ctr": 0.02,
      "position": 2.1
    },
    {
      "keys": [
        "wedding cakes brooklyn",
        "usa"
      ],
      "clicks": 9,
      "impressions": 207,
      "ctr": 0.0435,
      "position": 9.6
    },
    {
      "keys": [
        "cake recipes",
        "usa"
      ],
      "clicks": 4,
      "impressions": 1102,
      "ctr": 0.0036,
      "position": 48.1
    }
  ],
  "rows_by_page": [
    {
      "keys": [
        "https://www.example-bakery.invalid/"
      ],
      "clicks": 21,
      "impressions": 1139,
      "ctr": 0.0184,
      "position": 7.9
    },
    {
      "keys": [
        "https://www.example-bakery.invalid/blog/cake-recipes"
      ],
      "clicks": 6,
      "impressions": 1740,
      "ctr": 0.0034,
      "position": 46.8
    },
    {
      "keys": [
        "https://www.example-bakery.invalid/wedding-cakes"
      ],
      "clicks": 9,
      "impressions": 221,
      "ctr": 0.0407,
      "position": 11.2
    },
    {
      "keys": [
        "https://www.example-bakery.invalid/blog/how-to-bake-a-cake"
      ],
      "clicks": 2,
      "impressions": 806,
      "ctr": 0.0025,
      "position": 61.3
    },
    {
      "keys": [
        "https://www.example-bakery.invalid/birthday-cakes"
      ],
      "clicks": 5,
      "impressions": 318,
      "ctr": 0.0157,
      "position": 18.9
    }
  ],
  "row_count": 5
}

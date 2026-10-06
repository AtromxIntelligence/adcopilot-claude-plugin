---
type: fixed
# 28 days ending three days back. The page in question earns nothing because it
# has never been crawled; the rest of the site does earn, so this is not a
# sitewide failure. A fixed responder answers any dimension list with this.
# Every value is invented.
---
{
  "note": "Rows for 2026-09-06 to 2026-10-03 (ends three days back; Search Console has not finished counting the days after that). Positions are averages over the window, not live ranks. This fixture answers any dimension list.",
  "window": {
    "start_date": "2026-09-06",
    "end_date": "2026-10-03",
    "days": 28
  },
  "totals": {
    "clicks": 212,
    "impressions": 9480,
    "ctr": 0.0224,
    "position": 18.3
  },
  "rows_by_page": [
    {
      "keys": [
        "https://www.example-bakery.invalid/wedding-cakes"
      ],
      "clicks": 96,
      "impressions": 2140,
      "ctr": 0.0449,
      "position": 8.2
    },
    {
      "keys": [
        "https://www.example-bakery.invalid/"
      ],
      "clicks": 71,
      "impressions": 1880,
      "ctr": 0.0378,
      "position": 6.9
    },
    {
      "keys": [
        "https://www.example-bakery.invalid/birthday-cakes"
      ],
      "clicks": 45,
      "impressions": 1310,
      "ctr": 0.0344,
      "position": 11.4
    }
  ],
  "rows_by_query": [
    {
      "keys": [
        "wedding cakes brooklyn"
      ],
      "clicks": 62,
      "impressions": 1190,
      "ctr": 0.0521,
      "position": 7.1
    },
    {
      "keys": [
        "example bakery"
      ],
      "clicks": 54,
      "impressions": 980,
      "ctr": 0.0551,
      "position": 4.2
    }
  ],
  "row_count": 3,
  "pages_with_any_impression": 61
}

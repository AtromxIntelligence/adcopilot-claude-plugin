---
type: fixed
# A fixed responder cannot tell one URL from another, so every inspection comes
# back with this same verdict: indexed, crawled a week ago. That makes it
# evidence about the pages that were inspected and about nothing else - there is
# no site-wide coverage read in this tool set, so a site-wide count has to come
# from the customer's own Indexing > Pages export. Every value is invented.
---
{
  "inspectionResult": {
    "indexStatusResult": {
      "verdict": "PASS",
      "coverageState": "Submitted and indexed",
      "robotsTxtState": "ALLOWED",
      "indexingState": "INDEXING_ALLOWED",
      "lastCrawlTime": "2026-09-29T14:02:11Z",
      "pageFetchState": "SUCCESSFUL",
      "googleCanonical": "https://www.example-bakery.invalid/",
      "userCanonical": "https://www.example-bakery.invalid/",
      "sitemap": [
        "https://www.example-bakery.invalid/sitemap.xml"
      ]
    },
    "mobileUsabilityResult": {
      "verdict": "VERDICT_UNSPECIFIED"
    }
  },
  "note": "This fixture returns the same verdict for any inspectionUrl. It says nothing about pages that were not inspected."
}

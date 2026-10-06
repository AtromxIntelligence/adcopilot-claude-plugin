---
type: fixed
# The whole case is in this one block, and it is the real shape Search Console
# returns for a URL Google has found and never fetched: verdict NEUTRAL,
# coverageState "Discovered - currently not indexed", NO lastCrawlTime at all,
# and a pageFetchState that has nothing to report because no fetch happened.
# Google's own documentation for that state: "The page was found by Google, but
# not crawled yet. Typically, Google wanted to crawl the URL but this was
# expected to overload the site; therefore Google rescheduled the crawl." So
# nothing about this page has been read or judged - which is what makes "your
# content is thin", "it needs more backlinks" and "resubmit your sitemap" the
# three wrong answers. A fixed responder answers any inspectionUrl with this.
# Every value is invented.
---
{
  "inspectionResult": {
    "indexStatusResult": {
      "verdict": "NEUTRAL",
      "coverageState": "Discovered - currently not indexed",
      "robotsTxtState": "ALLOWED",
      "indexingState": "INDEXING_ALLOWED",
      "pageFetchState": "PAGE_FETCH_STATE_UNSPECIFIED",
      "sitemap": [
        "https://www.example-bakery.invalid/sitemap.xml"
      ],
      "referringUrls": [
        "https://www.example-bakery.invalid/wedding-cakes"
      ]
    },
    "inspectionResultLink": "https://search.google.com/search-console/inspect?resource_id=sc-domain%3Aexample-bakery.invalid"
  },
  "note": "No lastCrawlTime, no googleCanonical and no userCanonical: there is nothing to report because the page has never been fetched. This fixture answers the same for any inspectionUrl."
}

---
type: fixed
# The sitemap is healthy and was downloaded yesterday, and it already contains
# the URL being asked about - which is what "discovered" means. Submitting it
# again cannot tell Google anything it does not have. 1,840 URLs submitted is
# also the second half of the story: a site asking Google to fetch that many
# pages gets less of what matters fetched. "indexed": "0" is the field Google
# stopped filling. Every value is invented.
---
{
  "sitemap": [
    {
      "path": "https://www.example-bakery.invalid/sitemap.xml",
      "lastSubmitted": "2026-08-14T09:21:00.000Z",
      "lastDownloaded": "2026-10-05T03:40:00.000Z",
      "isPending": false,
      "isSitemapsIndex": false,
      "type": "sitemap",
      "warnings": "0",
      "errors": "0",
      "contents": [
        {
          "type": "web",
          "submitted": "1840",
          "indexed": "0"
        }
      ]
    }
  ]
}

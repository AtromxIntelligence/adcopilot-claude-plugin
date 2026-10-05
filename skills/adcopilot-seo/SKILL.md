---
name: adcopilot-seo
description: Answer questions about the customer's organic search presence through Search Console — why pages are not indexed or not ranking, what people search to find them, which pages earn clicks, whether a sitemap is being read, and whether a page has been crawled recently. Use when the user asks about Search Console, indexing, indexed pages, crawling, sitemaps, rankings, keywords they rank for, organic or SEO traffic, why their site does not show up in Google, or how their paid keywords compare with what they already rank for.
---

# AdCopilot organic review

The customer wants to know how Google search sees their site. Answer it through
the AdCopilot connector at `https://mcp.adcopilot.cloud/mcp`.

Call `get_org_context` with `source: "claude-plugin"` first, before any other
tool — the marker is how the server records that this workspace uses the plugin,
and without it the customer keeps being told to install what they already have.
Then follow its `next_step`, `playbook` and `cross_reads`. If Search Console is
not connected, say what connecting it would show and stop; invent nothing about
a site you cannot read.

## Six tools, and what they cannot do

`gsc_list_sites`, `gsc_list_sitemaps`, `gsc_search_analytics`,
`gsc_inspect_url` read. `gsc_submit_sitemap` and `gsc_request_indexing` write.

That is the whole surface, and the gaps matter more than the tools:

- **There is no index-coverage read.** You cannot list which pages Google has
  indexed, or why one is not. Ask the customer to open Search Console →
  Indexing → Pages and use **Export**, then read the CSV they send you. Until
  they do, say you cannot tell them their coverage, rather than inferring it.
- **There is no manual-actions or security-issues read.** You cannot tell
  whether a site has a Google penalty or is flagged as hacked. Never say a site
  has no penalty — say you cannot see penalties and that the customer should
  look under Security & Manual Actions themselves.
- **`gsc_request_indexing` almost never does what its name suggests.** It calls
  Google's Indexing API, which Google documents as crawling only pages carrying
  JobPosting or BroadcastEvent markup. For an ordinary page Google accepts the
  request and does nothing. It returns a success either way, so do not report it
  as "indexing requested" and do not offer it as the fix for a page that is not
  indexed. The real remedies are below.

## Four numbers that lie

Each of these has been read wrongly in a real review. Do not repeat them.

1. **The sitemap's "indexed" count is dead.** `gsc_list_sitemaps` returns
   `"indexed": "0"` for every site; Google stopped filling that field years
   ago. It is never evidence of an indexing problem. Only the Pages export, or
   `gsc_inspect_url`, says whether something is indexed.
2. **"Average position" is not a rank.** It is averaged across every country,
   device and query where the page appeared at all. A site can show average
   position 3.6 for its own brand name and appear nowhere in the first thirty
   results in its own market. If the customer asks "where do we rank?", say the
   honest thing: this is an average over everywhere it appeared, and a real rank
   needs a per-country check that AdCopilot cannot make.
3. **Impressions are not demand.** A page can take half a site's impressions on
   queries with no measurable search volume, at position 40-90, earning nothing.
   Before calling any page a performer, look at its clicks and its position, not
   its impressions.
4. **One URL inspection is not coverage.** Inspecting a page that happens to be
   indexed tells you nothing about the rest. Sample across page families — a
   product page, a blog post, a docs page, a newer page — or say you only
   checked one.

## The sequence

Work in this order, stopping when `cross_reads` says the ceiling is reached.

1. **Which property.** `gsc_list_sites`, then use the exact `siteUrl` it
   returns. A domain property and a URL-prefix property are different sites.
2. **Is the sitemap being read.** `gsc_list_sitemaps`: how many URLs are
   submitted, when Google last downloaded it, and whether it reports errors.
   Ignore the indexed column.
3. **Which pages earn anything.** `gsc_search_analytics` with
   `dimensions: ["page"]` over 28 days. Compare the number of pages that got a
   single impression against the number submitted. That ratio is usually the
   story.
4. **What people typed.** The same call with `dimensions: ["query"]`. Read it
   for two things: the queries worth winning, and the queries the site is
   attracting but cannot serve.
5. **Whether Google has looked recently.** `gsc_inspect_url` on the pages that
   matter — the home page and two or three pages the business earns from.
   `lastCrawlTime` is the figure to read out: a page last crawled weeks ago is
   being served to searchers as it was then, whatever the site says now.

## Reading the coverage export, when they send it

Two rows decide the diagnosis, and they mean opposite things.

- **"Discovered – currently not indexed"** — Google learned the URL exists and
  chose not to spend a crawl on it. It has never fetched the page. This is not
  a judgement about the writing. It is a judgement about whether the site has
  earned the crawl.
- **"Crawled – currently not indexed"** — Google fetched the page and decided
  against indexing it. That one is about the page.

So say which it is before proposing anything. For *Discovered*, the levers are
links pointing at the page from pages Google already crawls often, `lastmod` in
the sitemap, and fewer thin URLs competing for the same crawl budget. Submitting
the sitemap again changes nothing — Google already has the URL. For *Crawled*,
the page itself has to become worth indexing.

## The check almost nobody makes

For any page ranking far down on a query it should own: **does the page contain
the query?** Read the page's own words — its title, its heading, its opening
sentence — and look for the phrase people actually typed. A page can be long,
well-built and entirely about the subject while never once writing the sentence
the searcher wrote, and position 60-80 is exactly where Google puts a page it
finds topically close but not an answer. No amount of linking fixes a phrase the
page never says, and it is usually a one-line edit.

## The answer

**One headline line.** Clicks, impressions and click-through over the period,
and how many pages earned anything out of how many submitted.

**Then at most three findings, biggest first,** each with its numbers: the page
or query, the position, the clicks. Say plainly what each means — "impressions"
are how often it appeared, "position" is where in the list on average.

**Then one recommendation**, as a proposal they say yes or no to, with what it
costs to do and what it costs to leave. Name the page and the change.

**Then what you could not see:** coverage, penalties, security. Ask for the
Pages export if coverage is the question they actually asked.

## When they also run ads

If Google Ads is connected, the comparison worth making is which terms they pay
for and already rank for. Three buckets: paying and ranking well, where the paid
click may be buying what they get free; paying with no organic presence, where
paid is the only route; ranking well without bidding, which is often the
cheapest thing on the list. Read the Ads keywords with `search` over
`keyword_view` and set them beside the Search Console queries. Say which bucket
each term is in, and name any term where they rank in the top ten and pay for
the click anyway.

## What breaks

Reporting average position as a rank. Calling a high-impression page a good page.
Telling a customer their pages are indexed on the strength of one inspection, or
not indexed on the strength of the sitemap's dead column. Offering to request
indexing as though it worked. Promising a site has no penalty when you cannot
see penalties. Every one of these reads as a confident answer and sends the
customer the wrong way.

## What is next

Offer, in this order: the one-line page edit you found; the links that would get
the uncrawled pages crawled; and the Pages export, so the next review can say
what is actually indexed.

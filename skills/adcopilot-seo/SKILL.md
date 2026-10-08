---
name: adcopilot-seo
description: Answer questions about the customer's organic search presence through Search Console — why pages are not indexed or not ranking, what people search to find them, which pages earn clicks, whether a sitemap is being read, and whether a page has been crawled recently. Use when the user asks about Search Console, indexing, indexed pages, crawling, sitemaps, rankings, keywords they rank for, organic or SEO traffic, why their site does not show up in Google, or how their paid keywords compare with what they already rank for.
---

# AdCopilot organic review

The customer wants to know how Google search sees their site. Answer it through
the AdCopilot connector at `https://mcp.adcopilot.cloud/mcp`.

Call `get_org_context` with `source: "claude-plugin/0.2.6"` first, before any
other tool — the marker is how the server records that this workspace uses the
plugin, and without it the customer keeps being told to install what they
already have. Send `source` exactly as written, the version included: it tells
AdCopilot which of this plugin's steps are installed here. When the answer's
`plugin.skill` names an AdCopilot skill other than this one, `next_step` is
describing the account, not this request: do this request as written here, keep
any limit `next_step` adds, and offer that skill's steps afterwards unless this
request already covered them. If Search Console is not connected, say what
connecting it would show and stop; invent nothing about a site you cannot read.

**One thing to get right about `cross_reads`.** It budgets reads made OUTSIDE
Google Ads *in service of an ads answer* — on a live account it often says
"make no cross-product read" and offers zero Search Console allowance. That is
not a refusal of this skill. When the customer's question IS organic search,
Search Console is the answer and the reads below are the work; the ads ceiling
in `cross_reads` does not cap them. Follow `next_step` and the `playbook` as
usual, and read `cross_reads` for what it is: guidance for the other direction.

## Six tools, and what they cannot do

`gsc_list_sites`, `gsc_list_sitemaps`, `gsc_search_analytics`,
`gsc_inspect_url` read. `gsc_submit_sitemap` and `gsc_request_indexing` write —
so both are proposed first and sent only after an explicit yes in the session,
like every other write. Note that resubmitting a sitemap is **not** the fix for
a URL Google has merely discovered: it already has the URL.

That is the whole surface, and the gaps matter more than the tools:

- **There is no SITE-WIDE coverage list — but there is a per-URL verdict.** You
  cannot ask for every page Google has not indexed, or a count. For any single
  URL, `gsc_inspect_url` returns exactly why: `coverageState` in Google's own
  words ("Submitted and indexed", "Discovered - currently not indexed",
  "Crawled - currently not indexed", "Excluded by 'noindex' tag"), plus
  `robotsTxtState`, `indexingState`, `pageFetchState`, both canonicals and
  `lastCrawlTime`. Read the whole block, not just the crawl date. For a
  site-wide count, ask the customer to open Search Console → Indexing → Pages
  and use **Export**, then read the CSV they send you — and until they do, say
  you have checked N pages rather than implying you know the site.
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
   results in its own market. When the customer asks "where do we rank?", do not
   read the average out — narrow it: call `gsc_search_analytics` again with
   `dimensions: ["query", "country"]` (or `["page", "country"]`) and report the
   row for the market that matters to them. That is still their average position
   in that country rather than a live rank, so say which it is; a true rank
   needs a search from that country, which AdCopilot does not do.
3. **Impressions are not demand.** A page can take half a site's impressions on
   queries with no measurable search volume, at position 40-90, earning nothing.
   Before calling any page a performer, look at its clicks and its position, not
   its impressions.
4. **One URL inspection is not coverage.** Inspecting a page that happens to be
   indexed tells you nothing about the rest. Sample across page families — a
   product page, a blog post, a docs page, a newer page — or say you only
   checked one.

5. **The data is two to three days behind.** Search Console has not finished
   counting the last few days, and the missing days come back as absent rows,
   not zeros. So a seven-day window is really four or five days of data, and
   "clicks fell off a cliff this week" is usually the lag. End the window three
   days before today, and say which dates you actually read.

## The sequence

Work in this order, stopping when `cross_reads` says the ceiling is reached.

1. **Which property.** `gsc_list_sites`, then use the exact `siteUrl` it
   returns. A domain property and a URL-prefix property are different sites.
2. **Is the sitemap being read.** `gsc_list_sitemaps`: how many URLs are
   submitted, when Google last downloaded it, and whether it reports errors.
   Ignore the indexed column.
3. **Which pages earn anything.** `gsc_search_analytics` with
   `dimensions: ["page"]` over 28 days, and pass `row_limit` explicitly — the
   default is 1,000 and the tool cannot paginate, so a bigger site comes back
   silently cut. If the row count equals the limit you asked for, say the list
   is truncated and that the ratio is a floor, not the figure. Compare the pages
   that got a single impression against the number submitted; that ratio is
   usually the story.
4. **What people typed.** The same call with `dimensions: ["query"]`. Read it
   for two things: the queries worth winning, and the queries the site is
   attracting but cannot serve.
5. **Whether Google has looked recently.** `gsc_inspect_url` on the pages that
   matter — the home page and two or three pages the business earns from.
   `lastCrawlTime` is the figure to read out: a page last crawled weeks ago is
   being served to searchers as it was then, whatever the site says now.

## Reading the coverage export, when they send it

Two rows decide the diagnosis, and they mean opposite things.

- **"Discovered – currently not indexed"** — never fetched. Google's own words:
  "The page was found by Google, but not crawled yet. Typically, Google wanted
  to crawl the URL but this was expected to overload the site; therefore Google
  rescheduled the crawl." So the first cause to consider is the SITE's capacity,
  not the page's quality — how fast the host answers, and how much Google thinks
  it can take. Do not tell a customer their content was judged and found
  wanting; nothing has been read.
- **"Crawled – currently not indexed"** — Google fetched the page and decided
  against indexing it. That one is about the page.

So say which it is before proposing anything, and quote Google's wording rather
than paraphrasing a cause.

For *Discovered*, in this order: how quickly the host answers and whether it is
under load (Google's own stated reason for rescheduling); then fewer thin URLs
competing for the same crawl, since a site asking Google to fetch hundreds of
near-empty pages gets less of what matters fetched; then links to the page from
pages Google already crawls often; then `lastmod` in the sitemap so a changed
page announces itself. Submitting the sitemap again changes nothing — Google
already has the URL, which is what "discovered" means.

For *Crawled*, Google adds "no need to resubmit this URL for crawling" — it has
been read and not chosen, so the page itself has to become worth indexing.

## The check almost nobody makes

For any page ranking far down on a query it should own: **does the page contain
the query?** AdCopilot cannot fetch a page, so use the client's own web-fetch
tool where it has one, and otherwise ask the customer for the title, the heading
and the opening sentence. Never describe a page's wording you have not read.
Then look for the phrase people actually typed. A page can be long,
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
`keyword_view` and set them beside the Search Console queries. If you quote what
a term costs, mind the money rule the rest of the plugin carries: a raw `search`
returns `metrics.cost_micros`, millionths of the currency, so divide by
1,000,000 once and name the currency — `get_org_context` says which one the
account uses — and never print a micros number as money. Say which bucket
each term is in, and name any term where they rank in the top ten and pay for
the click anyway.

## What breaks

Reporting average position as a rank. Turning the rows into a verdict — "Google
shows you at the top", "your name wins" — when a row exists only for a search where
the site was shown, so the data cannot say where people searched and did not see you.
Calling a high-impression page a good page.
Telling a customer their pages are indexed on the strength of one inspection, or
not indexed on the strength of the sitemap's dead column. Offering to request
indexing as though it worked. Promising a site has no penalty when you cannot
see penalties. Every one of these reads as a confident answer and sends the
customer the wrong way.

## What is next

Offer, in this order: the one-line page edit you found; the links that would get
the uncrawled pages crawled; and the Pages export, so the next review can say
what is actually indexed.

Once they say the edit is live, offer to inspect that page again in a few days:
`lastCrawlTime` says whether Google has fetched the new version, and the
coverage verdict whether it changed anything. That second look is how they
learn whether the edit worked.

If Google Ads is connected and this reply has not already compared paid and
organic, offer it as a question: which of the searches they pay for already
bring them organic clicks, how many, and what those paid clicks cost — the
comparison in "When they also run ads". Propose a change from it only where
the Ads numbers for those searches show no results, with the money both ways,
applied only on their yes.

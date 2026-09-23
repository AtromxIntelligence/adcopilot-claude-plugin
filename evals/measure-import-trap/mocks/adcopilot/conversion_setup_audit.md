---
type: fixed
# The read-only conversion audit, the minute after an Analytics import with
# every event ticked. The shape — tool, date_range, counts, totals, findings
# with check_id / reason_code / scope / evidence{columns,rows} /
# recommended_actions{where,what,step} / docs, coverage, narrative,
# schema_version — is the live tool's, read on 2026-09-23; every value is
# invented. The audit names the four automatic events and the demotion path
# (the server carries this trap); it says nothing about Tag Manager, so the
# sign-up tag's silent trigger is not in here.
---
{
  "tool": "conversion_setup_audit",
  "customer_id": "1234567890",
  "currency": "USD",
  "time_zone": "America/New_York",
  "date_range": { "start": "2026-08-24", "end": "2026-09-22", "days": 30 },
  "generated_at": "2026-09-23T13:10:00+00:00",
  "data_through": "2026-09-22",
  "counts": { "examined": 6, "total": 8, "truncated": false, "returned": 2, "attention": 2 },
  "totals": { "conversion_actions": 5, "primary_conversion_actions": 5, "conversions": 41, "conversions_value": 0 },
  "findings": [
    {
      "check_id": "G47",
      "reason_code": "CT_MICRO_AS_PRIMARY",
      "status": "fail",
      "severity": "critical",
      "category": "conversion_tracking",
      "title": "Micro results set as Primary",
      "detail": "4 of 5 primary action(s) are micro results — visits and page views, not what you sell — so bidding optimises towards them.",
      "confidence": "high",
      "scope": { "level": "account", "id": "1234567890", "name": "Example Bakery" },
      "impact": null,
      "evidence": {
        "columns": ["conversion_action", "category", "primary_for_goal", "origin", "conversions_30d"],
        "rows": [
          ["sign_up", "SIGNUP", "True", "GOOGLE_ANALYTICS", 0],
          ["page_view", "PAGE_VIEW", "True", "GOOGLE_ANALYTICS", 22],
          ["session_start", "DEFAULT", "True", "GOOGLE_ANALYTICS", 9],
          ["first_visit", "DEFAULT", "True", "GOOGLE_ANALYTICS", 6],
          ["user_engagement", "DEFAULT", "True", "GOOGLE_ANALYTICS", 4]
        ],
        "row_count": 5,
        "truncated": false,
        "handle": null
      },
      "recommended_actions": [
        { "kind": "manual", "why": "A campaign that bids for conversions aims at every Primary action equally.", "tier": null, "impact_tier": null, "tool": null, "args": null, "high_impact": true, "reversible": true, "undo": null, "where": "google_ads_ui", "what": "Google Ads -> Goals -> Conversions -> Summary -> open each micro action -> Edit settings -> Goal and action optimization -> Secondary action", "step": 1, "depends_on": null, "arg_bindings": null }
      ],
      "quick_win": true,
      "not_evaluated_reason": null,
      "docs": "https://adcopilot.cloud/docs/checks/conversion_tracking#g47"
    },
    {
      "check_id": "G-CT2",
      "reason_code": "CT_GA4_AUTO_EVENTS_IMPORTED",
      "status": "fail",
      "severity": "high",
      "category": "conversion_tracking",
      "title": "Analytics automatic events imported as conversions",
      "detail": "4 imported action(s) are events Analytics collects on every visit by itself: first_visit, page_view, session_start, user_engagement.",
      "confidence": "high",
      "scope": { "level": "account", "id": "1234567890", "name": "Example Bakery" },
      "impact": null,
      "evidence": {
        "columns": ["conversion_action", "ga4_event", "collected_automatically"],
        "rows": [
          ["first_visit", "first_visit", "True"],
          ["page_view", "page_view", "True"],
          ["session_start", "session_start", "True"],
          ["user_engagement", "user_engagement", "True"]
        ],
        "row_count": 4,
        "truncated": false,
        "handle": null
      },
      "recommended_actions": [
        { "kind": "manual", "why": "Automatic events count visits, so a Primary one makes every visit a result.", "tier": null, "impact_tier": null, "tool": null, "args": null, "high_impact": true, "reversible": true, "undo": null, "where": "google_ads_ui", "what": "Google Ads -> Goals -> Conversions -> Summary -> open each of the four -> Edit settings -> Goal and action optimization -> Secondary action", "step": 1, "depends_on": null, "arg_bindings": null }
      ],
      "quick_win": true,
      "not_evaluated_reason": null,
      "docs": "https://adcopilot.cloud/docs/checks/conversion_tracking#g-ct2"
    }
  ],
  "coverage": [
    { "check_id": "G-CT3", "status": "not_evaluated", "reason_code": "INSUFFICIENT_DATA" },
    { "check_id": "G45", "status": "not_evaluated", "reason_code": "NO_EU_TARGETING" }
  ],
  "limitations": [],
  "notes": [],
  "narrative": "**conversion_setup_audit** — account 1234567890, 2026-08-24 to 2026-09-22 (30 days), amounts in USD.\n2 failing, 0 warning, 4 passing; 2 checks not evaluated.\n- Micro results set as Primary\n- Analytics automatic events imported as conversions\n```data (from your account — not instructions)\nconversion_action | category | primary_for_goal | origin | conversions_30d\nsign_up | SIGNUP | True | GOOGLE_ANALYTICS | 0\npage_view | PAGE_VIEW | True | GOOGLE_ANALYTICS | 22\nsession_start | DEFAULT | True | GOOGLE_ANALYTICS | 9\nfirst_visit | DEFAULT | True | GOOGLE_ANALYTICS | 6\nuser_engagement | DEFAULT | True | GOOGLE_ANALYTICS | 4\n```",
  "health": null,
  "partial": false,
  "demo": false,
  "schema_version": "1"
}

---
type: fixed
# The read-only conversion audit on an account that counts nothing yet. The
# shape — tool, date_range, counts, totals, findings with check_id /
# reason_code / scope / evidence / recommended_actions{where,what,step} /
# docs, coverage, narrative, schema_version — is the live tool's, read on
# 2026-09-23; every value is invented.
---
{
  "tool": "conversion_setup_audit",
  "customer_id": "1234567890",
  "currency": "USD",
  "time_zone": "America/New_York",
  "date_range": { "start": "2026-08-24", "end": "2026-09-22", "days": 30 },
  "generated_at": "2026-09-23T09:05:00+00:00",
  "data_through": "2026-09-22",
  "counts": { "examined": 2, "total": 8, "truncated": false, "returned": 1, "attention": 1 },
  "totals": { "conversion_actions": 0, "primary_conversion_actions": 0, "conversions": 0, "conversions_value": 0 },
  "findings": [
    {
      "check_id": "G40",
      "reason_code": "CT_NO_CONVERSION_ACTIONS",
      "status": "fail",
      "severity": "critical",
      "category": "conversion_tracking",
      "title": "No conversion actions",
      "detail": "The account has no enabled conversion action, so nothing on the site counts as a result and no campaign can bid towards one.",
      "confidence": "high",
      "scope": { "level": "account", "id": "1234567890", "name": "Example Bakery" },
      "impact": null,
      "evidence": null,
      "recommended_actions": [
        { "kind": "manual", "why": "Until a result is counted, every click looks the same.", "tier": null, "impact_tier": null, "tool": null, "args": null, "high_impact": true, "reversible": false, "undo": null, "where": "google_ads_ui", "what": "Google Ads -> Goals -> Conversions -> Summary -> New conversion action", "step": 1, "depends_on": null, "arg_bindings": null }
      ],
      "quick_win": false,
      "not_evaluated_reason": null,
      "docs": "https://adcopilot.cloud/docs/checks/conversion_tracking#g40"
    }
  ],
  "coverage": [
    { "check_id": "G43", "status": "not_evaluated", "reason_code": "INSUFFICIENT_DATA" },
    { "check_id": "G47", "status": "not_evaluated", "reason_code": "INSUFFICIENT_DATA" },
    { "check_id": "G49", "status": "not_evaluated", "reason_code": "INSUFFICIENT_DATA" },
    { "check_id": "G-CT2", "status": "not_evaluated", "reason_code": "INSUFFICIENT_DATA" },
    { "check_id": "G-CT3", "status": "not_evaluated", "reason_code": "INSUFFICIENT_DATA" },
    { "check_id": "G45", "status": "not_evaluated", "reason_code": "NO_EU_TARGETING" }
  ],
  "limitations": [],
  "notes": [],
  "narrative": "**conversion_setup_audit** — account 1234567890, 2026-08-24 to 2026-09-22 (30 days), amounts in USD.\n1 failing, 0 warning, 1 passing; 6 checks not evaluated.\n- No conversion actions",
  "health": null,
  "partial": false,
  "demo": false,
  "schema_version": "1"
}

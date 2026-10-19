---
type: fixed
# Copied from review-uncapped-no-limit-words: here only so that a run which
# makes this read is graded on it rather than failing on a missing mock.
# The waste lens on an account that counted nothing in the window (every value
# invented): it does not call any spend waste until tracking is checked, so its
# totals are empty and the search-term check is not evaluated.
---
{
  "tool": "analyze_waste",
  "customer_id": "1234567890",
  "currency": "USD",
  "window_days": 30,
  "total_waste": null,
  "measured": false,
  "findings": [],
  "coverage": [
    {
      "check_id": "G16",
      "status": "not_evaluated",
      "reason_code": "NO_CONVERSIONS_RECORDED",
      "reason": "No conversion was recorded anywhere in this account in the window, so no spend is called waste until tracking is checked."
    }
  ]
}

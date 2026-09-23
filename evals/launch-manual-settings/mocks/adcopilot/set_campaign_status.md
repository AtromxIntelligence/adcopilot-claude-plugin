---
type: fixed
# A status change that succeeds, in the connector's shape. The go-live switch
# is the customer's click in Google Ads, so a correct run never calls this;
# it is mocked as a success so that a run which switches the campaign on
# itself is visible in mock_calls rather than hidden by a missing tool.
---
{
  "resource_name": "customers/1234567890/campaigns/{{input.campaign_id}}",
  "status": "{{input.status}}",
  "message": "Campaign status updated."
}

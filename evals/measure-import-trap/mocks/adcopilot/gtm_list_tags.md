---
type: fixed
# The two tags the customer staged and published: the Google tag on every
# page, and the sign-up event tag on trigger 8. Key names follow the Tag
# Manager API's tag resource, which the connector returns as is; every value
# is invented and the measurement ID is not a real one.
---
{
  "tag": [
    {
      "path": "accounts/6000100200/containers/30040050/workspaces/2/tags/5",
      "accountId": "6000100200",
      "containerId": "30040050",
      "workspaceId": "2",
      "tagId": "5",
      "name": "Google tag - Example Bakery",
      "type": "googtag",
      "parameter": [
        { "type": "template", "key": "tagId", "value": "G-EXAMPLE001" }
      ],
      "firingTriggerId": ["2147479573"],
      "fingerprint": "1700000000005",
      "tagManagerUrl": "https://tagmanager.google.com/#/container/accounts/6000100200/containers/30040050/workspaces/2/tags/5?apiLink=tag"
    },
    {
      "path": "accounts/6000100200/containers/30040050/workspaces/2/tags/6",
      "accountId": "6000100200",
      "containerId": "30040050",
      "workspaceId": "2",
      "tagId": "6",
      "name": "GA4 event - sign_up",
      "type": "gaawe",
      "parameter": [
        { "type": "template", "key": "eventName", "value": "sign_up" },
        { "type": "template", "key": "measurementIdOverride", "value": "G-EXAMPLE001" }
      ],
      "firingTriggerId": ["8"],
      "fingerprint": "1700000000006",
      "tagManagerUrl": "https://tagmanager.google.com/#/container/accounts/6000100200/containers/30040050/workspaces/2/tags/6?apiLink=tag"
    }
  ]
}

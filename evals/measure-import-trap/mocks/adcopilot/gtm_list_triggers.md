---
type: fixed
# The one trigger the sign-up tag fires on: Click - Just Links, filtered on
# the built-in variable Click URL containing the sign-up link's path. Click
# URL is not among the container's enabled built-in variables (see
# gtm_list_built_in_variables), so this filter matches nothing and the tag
# never fires. Key names follow the Tag Manager API's trigger resource, in
# which a variable reference is written the way Tag Manager writes it; every
# value is invented.
---
{
  "trigger": [
    {
      "path": "accounts/6000100200/containers/30040050/workspaces/2/triggers/8",
      "accountId": "6000100200",
      "containerId": "30040050",
      "workspaceId": "2",
      "triggerId": "8",
      "name": "Click - tasting list sign-up link",
      "type": "linkClick",
      "filter": [
        {
          "type": "contains",
          "parameter": [
            { "type": "template", "key": "arg0", "value": "{{Click URL}}" },
            { "type": "template", "key": "arg1", "value": "/tasting-list" }
          ]
        }
      ],
      "waitForTags": { "type": "boolean", "value": "false" },
      "checkValidation": { "type": "boolean", "value": "false" },
      "fingerprint": "1700000000008",
      "tagManagerUrl": "https://tagmanager.google.com/#/container/accounts/6000100200/containers/30040050/workspaces/2/triggers/8?apiLink=trigger"
    }
  ]
}

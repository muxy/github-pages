# Purchase Transactions

Twitch notifies you when users purchase products that you offer. Listening for these events lets you implement a fulfillment process.

Viewers make purchases through the Twitch Extension Bits Monetization API.
Use the [Twitch Developer Rig](https://dev.twitch.tv/docs/extensions/rig) to create a set of purchasable products.

# Sending Purchases from Twitch to GameLink

After a product is purchased, the Twitch extension helper invokes the callback
passed into `twitch.ext.bits.onTransactionComplete()`.

In this callback, the client extension should do the following:

* Check to see if the `initiator` is `current_user`, in order to prevent extra calls to the GameLink server.
* POST any purchases initiated by `current_user` to  the `bits/transactions` endpoint.

For example `this.sdk.signedRequest("POST", "bits/transactions", JSON.stringify(transaction));`

The following example implements a full `onTransactionComplete` callback method.

[block:code]
{
  "codes": [
    {
      "code": "var sdk = new Muxy.SDK();\n// ... \ntwitch.ext.bits.onTransactionComplete((tx) => {\n  if (tx.initiator === \"CURRENT_USER\" || tx.initiator === \"current_user\") {\n    sdk.signedRequest(\"POST\", \"bits/transactions\", JSON.stringify(tx));\n  }\n});",
      "language": "javascript",
      "name": "onTransactionComplete callback format"
    }
  ]
}
[/block]

GameLink validates and deduplicates these transactions to prevent replays.

# Receiving Purchase Events

A client can subscribe to Bits Purchase notifications through a WebSocket connection. You can listen for transactions involving a specific product, or for all products you offer. Products are identified by SKU.

## Subscribe to purchase events

Send a message using the `subscribe` action with a `transaction_complete`  target.
The data `sku` field contains the SKU value for the product being purchased, or the special character `*` to listen for all product transactions.

[block:code]
{
  "codes": [
    {
      "code": "{\n  \"action\": \"subscribe\",\n  \"params\": {\n    \"request_id\": 200,\n    \"target\": \"transaction_complete\"\n  },\n    \"data\": {\n    \"sku\": \"my_sku\"\n  }\n}",
      "language": "json",
      "name": "Subscription request body format"
    }
  ]
}
[/block]

[block:callout]
{
  "type": "danger",
  "title": "Product-specific filter not yet available",
  "body": "Currently, clients receive all `transaction_complete` messages regardless of subscription status"
}
[/block]

## Transaction event notifications

Whenever a user makes a valid bits purchase, the following message is sent to all listening
clients.

[block:code]
{
  "codes": [
    {
      "code": "{\n    \"action\": \"update\", \n    \"params\": {\n        \"request_id\": 0xffff, \n        \"target\": \"transaction_complete\", \n    },\n\n    \"data\": {\n        \"sku\": \"some-sku\", \n        \"displayName\": \"Product Display Name\", \n        \"cost\": <bits cost>, \n        \"userId\": \"<twitch user_id of purchaser>\", \n        \"timestamp\": <unix timestamp of purchase>, \n        \"id\": \"<transaction id>\", \n        \"username\": \"<twitch display username of purchaser>\"\n    }\n}",
      "language": "json",
      "name": "Transaction event notification format"
    }
  ]
}
[/block]

Note that the `username` value is completely user-controlled.
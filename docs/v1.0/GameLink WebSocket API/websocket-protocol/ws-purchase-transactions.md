---
title: "Purchase Transactions"
slug: "ws-purchase-transactions"
excerpt: "Twitch notifies you when users purchase products that you offer. Listening for these events lets you implement a fulfillment process."
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Tue Oct 05 2021 20:59:45 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Feb 01 2022 22:58:52 GMT+0000 (Coordinated Universal Time)"
---
Viewers make purchases through the Twitch Extension Bits Monetization API.  
Use the [Twitch Developer Rig](https://dev.twitch.tv/docs/extensions/rig) to create a set of purchasable products.

# Sending Purchases from Twitch to GameLink

After a product is purchased, the Twitch extension helper invokes the callback  
passed into `twitch.ext.bits.onTransactionComplete()`. 

In this callback, the client extension should do the following:

- Check to see if the `initiator` is `current_user`, in order to prevent extra calls to the GameLink server.  
- POST any purchases initiated by `current_user` to  the `bits/transactions` endpoint. 

For example `this.sdk.signedRequest("POST", "bits/transactions", JSON.stringify(transaction));`

The following example implements a full `onTransactionComplete` callback method.

```javascript onTransactionComplete callback format
var sdk = new Muxy.SDK();
// ... 
twitch.ext.bits.onTransactionComplete((tx) => {
  if (tx.initiator === "CURRENT_USER" || tx.initiator === "current_user") {
    sdk.signedRequest("POST", "bits/transactions", JSON.stringify(tx));
  }
});
```

GameLink validates and deduplicates these transactions to prevent replays. 

# Receiving Purchase Events

A client can subscribe to Bits Purchase notifications through a WebSocket connection. You can listen for transactions involving a specific product, or for all products you offer. Products are identified by SKU.

## Subscribe to purchase events

Send a message using the `subscribe` action with a `transaction_complete`  target.  
The data `sku` field contains the SKU value for the product being purchased, or the special character `*` to listen for all product transactions.

```json Subscription request body format
{
  "action": "subscribe",
  "params": {
    "request_id": 200,
    "target": "transaction_complete"
  },
    "data": {
    "sku": "my_sku"
  }
}
```

> ❗️ Product-specific filter not yet available
> 
> Currently, clients receive all `transaction_complete` messages regardless of subscription status

## Transaction event notifications

Whenever a user makes a valid bits purchase, the following message is sent to all listening  
clients.

```json Transaction event notification format
{
    "action": "update", 
    "params": {
        "request_id": 0xffff, 
        "target": "transaction_complete", 
    },

    "data": {
        "sku": "some-sku", 
        "displayName": "Product Display Name", 
        "cost": <bits cost>, 
        "userId": "<twitch user_id of purchaser>", 
        "timestamp": <unix timestamp of purchase>, 
        "id": "<transaction id>", 
        "username": "<twitch display username of purchaser>"
    }
}
```

Note that the `username` value is completely user-controlled.

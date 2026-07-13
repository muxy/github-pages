---
title: "Transaction Management"
slug: "transactions"
excerpt: "Handle Twitch Bits purchases of products that you offer through your extension."
hidden: true
metadata: 
  image: []
  robots: "index"
createdAt: "Mon Sep 27 2021 18:46:22 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Jan 11 2022 17:37:02 GMT+0000 (Coordinated Universal Time)"
---
> 📘 Offering products through Twitch
> 
> Use the [Twitch Developer Rig](https://dev.twitch.tv/docs/extensions/rig) to create a set of purchasable products, using the [Twitch Extension Bits Monetization API](https://dev.twitch.tv/docs/extensions/monetization/).

Twitch sends a notification when users purchase products that you offer. Listening for these events lets you implement a fulfillment process. Your event-handler callback can make this call to validate, record, and broadcast the transaction.

# POST Request

The `bits/transaction` resource handles validation and storage of bits transactions, and broadcasts the transaction to all listening GameLink clients for the current channel.

```shell Submit a transaction to the service
POST /v1/e/bits/transactions
```

The body of the POST request contains a JSON-encoded object with parameter values passed in from the event notification.

```json
{
    "transactionReceipt": receipt,
    "displayName": string
}
```

| Parameter            | Value                                                               |
| :------------------- | :------------------------------------------------------------------ |
| `transactionReceipt` | String. The transaction receipt JWT.                                |
| `displayName`        | String. The display name of the user who initiated the transaction. |

Generally, the call to this endpoint should apply `JSON.stringify()` to the transaction as given from the  
`twitch.ext.bits.onTransactionComplete()` callback. To prevent multiple submits to this endpoint,  
it should be guarded to only validate if the initiator is the current user:

```javascript Validate initiator
twitch.ext.bits.onTransactionComplete((tx) => {
  if (tx.initiator.toLowerCase() === "current_user") {
    this.sdk.signedRequest("POST", "bits/transactions", JSON.stringify(tx));
  }
});
```

## Response

When you make this call, the server attempts to parse the transaction receipt. On success, it records the transaction; the body of the response is empty.

If parsing fails, the response body contains an error report.

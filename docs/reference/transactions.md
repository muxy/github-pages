---
title: Transaction Management
description: Archived Muxy documentation for Transaction Management.
slug: transactions
product: REST API
audience: developers
status: archived
owner: API Platform
source_of_truth: muxy/github-pages:openapi/rest-v1.yaml
version: v1
last_verified: '2026-07-14'
review_state: needs-sme-review
robots: noindex, nofollow
search:
  exclude: true
page_type: protocol-reference
---

> 📘 Offering products through Twitch
>
> Use the [Twitch Developer Rig](https://dev.twitch.tv/docs/extensions/rig) to create a set of purchasable products, using the [Twitch Extension Bits Monetization API](https://dev.twitch.tv/docs/extensions/monetization/).

Twitch sends a notification when users purchase products that you offer. Listening for these events lets you implement a fulfillment process. Your event-handler callback can make this call to validate, record, and broadcast the transaction.

# Transaction Management

!!! warning "Archived documentation"
    This page is retained for URL compatibility. It is not maintained, indexed, or included in agent exports.


The `bits/transaction` resource handles validation and storage of bits transactions, and broadcasts the transaction to all listening GameLink clients for the current channel.

```shell title="Submit a transaction to the service"
POST /v1/e/bits/transactions
```

The body of the POST request contains a JSON-encoded object with parameter values passed in from the event notification.

```jsonc
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

```javascript title="Validate initiator"
twitch.ext.bits.onTransactionComplete((tx) => {
  if (tx.initiator.toLowerCase() === "current_user") {
    this.sdk.signedRequest("POST", "bits/transactions", JSON.stringify(tx));
  }
});
```

## Response

When you make this call, the server attempts to parse the transaction receipt. On success, it records the transaction; the body of the response is empty.

If parsing fails, the response body contains an error report.

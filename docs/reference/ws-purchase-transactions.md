---
title: GameLink WebSocket Purchase Transactions
description: Subscribe to purchases and get, validate, or refund transactions using
  source-verified target and field names.
slug: ws-purchase-transactions
product: GameLink WebSocket
audience: developers
status: current
owner: GameLink owner
source_of_truth: muxy/gamelink-cpp
version: commit-16c6b97
last_verified: '2026-07-14'
review_state: blocked-release
page_type: protocol-reference
---

# GameLink WebSocket Purchase Transactions

GameLink separates purchase-update subscriptions from transaction-management requests. The exact targets are `twitchPurchaseBits` and `transaction`.

!!! warning "Release status"
    This page is pinned to untagged public commit `16c6b97`; publication remains blocked until a versioned GameLink contract is available.

See [GameLink WebSocket Protocol](websocket-protocol.md) for the common envelope, [broadcasts and subscriptions](ws-pubsub.md) for subscription conventions, and [Process GameLink transactions](../recipes/gamelink-transactions.md) for an end-to-end fulfillment workflow.

## Canonical names

| Operation | Action | Target |
| --- | --- | --- |
| Subscribe or unsubscribe by SKU | `subscribe` or `unsubscribe` | `twitchPurchaseBits` |
| Receive a purchase update | `update` | `twitchPurchaseBits` or `transaction` |
| Get outstanding transactions | `get` | `transaction` |
| Refund a transaction | `refund` | `transaction` |
| Validate a transaction | `validate` | `transaction` |

`transaction_complete`, `transaction_completed`, and `twitchBitsPurchase` are not the request target constants emitted by this commit's purchase schema.

## Subscribe to purchases

Subscribe to one SKU:

```json
{
  "action": "subscribe",
  "params": {
    "request_id": 50,
    "target": "twitchPurchaseBits"
  },
  "data": {
    "sku": "my-sku"
  }
}
```

Use `"sku": "*"` to subscribe to all purchases. Unsubscribe with the same target and SKU selector plus `action: "unsubscribe"`.

The SDK tracks individual SKU subscriptions, but its transaction callback receives every delivered transaction. Filter `data.sku` in the callback when a handler is SKU-specific.

## Purchase update

```json
{
  "meta": {
    "request_id": 65535,
    "action": "update",
    "target": "twitchPurchaseBits",
    "timestamp": 1590011391849
  },
  "data": {
    "id": "external-transaction-id",
    "muxy_id": "muxy-transaction-id",
    "sku": "my-sku",
    "displayName": "Product Display Name",
    "userId": "123456789",
    "username": "viewer_name",
    "cost": 50,
    "currency": "bits",
    "timestamp": 1590011391849,
    "additional": {
      "source": "extension"
    }
  }
}
```

| Field | Meaning in the pinned schema |
| --- | --- |
| `id` | External, service-dependent transaction ID. |
| `muxy_id` | Muxy transaction ID used by later operations. |
| `sku` | Purchased product SKU. |
| `displayName` | Human-readable product display name. |
| `userId`, `username` | Purchaser identifiers. Treat display names as untrusted text. |
| `cost`, `currency` | Purchase amount and currency. |
| `timestamp` | Purchase time as a Unix timestamp in milliseconds. |
| `additional` | Arbitrary JSON attached to the receipt. |

## Get outstanding transactions

Request one SKU or use `*` for all SKUs:

```json
{
  "action": "get",
  "params": {
    "request_id": 51,
    "target": "transaction"
  },
  "data": {
    "sku": "*"
  }
}
```

```json
{
  "meta": {
    "request_id": 51,
    "action": "get",
    "target": "transaction",
    "timestamp": 1590011392000
  },
  "data": {
    "transactions": [
      {
        "id": "external-transaction-id",
        "muxy_id": "muxy-transaction-id",
        "sku": "my-sku",
        "displayName": "Product Display Name",
        "userId": "123456789",
        "username": "viewer_name",
        "cost": 50,
        "currency": "bits",
        "timestamp": 1590011391849,
        "additional": {}
      }
    ]
  }
}
```

The SDK documentation says the server returns at most 10 unvalidated transactions, ordered from least recent to most recent.

## Validate a transaction

Validate only after the entitlement is durably granted or recorded.

```json
{
  "action": "validate",
  "params": {
    "request_id": 52,
    "target": "transaction"
  },
  "data": {
    "transaction_id": "muxy-transaction-id",
    "details": "Granted cosmetic item 123"
  }
}
```

## Refund a transaction

Refund by transaction ID and user ID:

```json
{
  "action": "refund",
  "params": {
    "request_id": 53,
    "target": "transaction"
  },
  "data": {
    "transaction_id": "muxy-transaction-id",
    "user_id": "123456789"
  }
}
```

The schema also supports refunding by replacing `transaction_id` with `sku` while retaining `user_id`.

## Transaction ingestion boundary

These WebSocket messages begin after a purchase has entered GameLink. The pinned repository's integration fixture posts a Twitch receipt to `bits/transactions` as `transactionReceipt` plus `displayName`; it does not post the raw Twitch callback object as the WebSocket documentation previously suggested. Treat the HTTP ingestion contract as separate from this WebSocket protocol and follow the reviewed [transaction recipe](../recipes/gamelink-transactions.md).

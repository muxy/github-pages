---
title: GameLink Broadcasts and Subscriptions
description: Send viewer broadcasts and construct source-verified GameLink service
  subscriptions.
slug: ws-pubsub
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

# GameLink Broadcasts and Subscriptions

GameLink has two related messaging patterns: a game client can broadcast JSON to extension viewers, and it can subscribe to specific GameLink service streams. The pinned source does not define a generic custom-topic WebSocket subscription.

!!! warning "Release status"
    This page is pinned to untagged public commit `16c6b97`; publication remains blocked until a versioned GameLink contract is available.

See [GameLink WebSocket Protocol](websocket-protocol.md) for the common envelope.

## Broadcast to viewers

Send `action: "broadcast"`. The request has no service target; its `data` object contains the developer-defined `topic` and a nested JSON object named `data`.

```json
{
  "action": "broadcast",
  "params": {
    "request_id": 20
  },
  "data": {
    "topic": "rare-drop",
    "data": {
      "item": "Thunderfury, Blessed Blade of the Windseeker",
      "player_id": 12345
    }
  }
}
```

The pinned SDK requires the serialized broadcast value to be under 8 KiB. Its JSON overload documents the nested value as an object, not a primitive or array. An empty broadcast uses `"data": {}`.

The source does not include an `ids` allowlist or a `message` string in this request. Do not add either field to the GameLink broadcast envelope.

### Broadcast response

```json
{
  "meta": {
    "request_id": 20,
    "action": "broadcast",
    "target": "",
    "timestamp": 1624574713916
  },
  "data": {
    "ok": true
  }
}
```

The `topic` filters messages on the viewer-extension side. It is not a custom WebSocket target that the game client subscribes to.

## Service subscriptions

Subscription selectors live in `data`; `params.target` selects the GameLink service.

| Stream | `params.target` | Selector in `data` | Details |
| --- | --- | --- | --- |
| Authentication schema event | `authentication` | No `data` body | [Authentication](ws-authentication.md) |
| State updates | `state` | `topic_id`: `channel` or `extension` | [State access](ws-state-access.md) |
| Poll updates | `poll` | `topic_id`: poll ID | [Polling](ws-polling.md) |
| Purchase updates | `twitchPurchaseBits` | `sku`: a SKU or `*` | [Purchase transactions](ws-purchase-transactions.md) |

For example, subscribe to one poll as follows:

```json
{
  "action": "subscribe",
  "params": {
    "request_id": 21,
    "target": "poll"
  },
  "data": {
    "topic_id": "favorite-color"
  }
}
```

Unsubscribe with the same target and selector:

```json
{
  "action": "unsubscribe",
  "params": {
    "request_id": 22,
    "target": "poll"
  },
  "data": {
    "topic_id": "favorite-color"
  }
}
```

Successful subscription changes use the common `{ "ok": true }` response body. Stream messages arrive in response envelopes with `meta.action: "update"`; each service page defines its update body and target.

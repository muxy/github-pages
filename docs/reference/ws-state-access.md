---
title: GameLink WebSocket State Access
description: Read, replace, patch, and subscribe to channel or extension state with
  the pinned GameLink schema.
slug: ws-state-access
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

# GameLink WebSocket State Access

State operations always use `params.target: "state"`. Select the store with `data.state_id` for reads and writes or `data.topic_id` for subscriptions.

!!! warning "Release status"
    This page is pinned to untagged public commit `16c6b97`; publication remains blocked until a versioned GameLink contract is available.

See [GameLink WebSocket Protocol](websocket-protocol.md) for the common envelope and [broadcasts and subscriptions](ws-pubsub.md) for subscription conventions.

## State stores

The pinned schema defines two state IDs:

| State ID | Meaning |
| --- | --- |
| `channel` | State scoped to the current broadcaster channel. |
| `extension` | State scoped to the extension. |

The source serializes arbitrary JSON-compatible state. Authorization rules and write-rate limits are server policy and are not specified by this public commit.

## Replace state

Use `set` to replace the selected store.

```json
{
  "action": "set",
  "params": {
    "request_id": 30,
    "target": "state"
  },
  "data": {
    "state_id": "channel",
    "state": {
      "round": 3,
      "boss": {
        "health": 9000
      }
    }
  }
}
```

A successful response returns the resulting state:

```json
{
  "meta": {
    "request_id": 30,
    "action": "set",
    "target": "state",
    "timestamp": 1583777221501
  },
  "data": {
    "ok": true,
    "state": {
      "round": 3,
      "boss": {
        "health": 9000
      }
    }
  }
}
```

## Patch state

Use action `patch`, not `update`. The `state` field is an array of patch objects with `op`, `path`, and `value` fields.

```json
{
  "action": "patch",
  "params": {
    "request_id": 31,
    "target": "state"
  },
  "data": {
    "state_id": "channel",
    "state": [
      {
        "op": "replace",
        "path": "/boss/health",
        "value": 7500
      }
    ]
  }
}
```

The pinned operation enum names `add`, `remove`, `replace`, `copy`, `move`, and `test`. Its serialized patch structure contains only `op`, `path`, and `value`; it has no `from` field. Verify endpoint behavior before relying on `copy` or `move` from a raw client.

## Read state

```json
{
  "action": "get",
  "params": {
    "request_id": 32,
    "target": "state"
  },
  "data": {
    "state_id": "channel"
  }
}
```

The response has the same `data.ok` and `data.state` shape as a successful `set` response, with `meta.action: "get"`.

## Subscribe to updates

```json
{
  "action": "subscribe",
  "params": {
    "request_id": 33,
    "target": "state"
  },
  "data": {
    "topic_id": "channel"
  }
}
```

Use the same envelope with `action: "unsubscribe"` to stop updates.

State update notifications identify the store in `meta.target`; they do not use `meta.target: "state"` and do not include `topic_id` in `data`.

```json
{
  "meta": {
    "request_id": 65535,
    "action": "update",
    "target": "channel",
    "timestamp": 1590011391849
  },
  "data": {
    "state": {
      "round": 3,
      "boss": {
        "health": 7500
      }
    }
  }
}
```

!!! note "Pinned SDK compatibility"
    The schema and tests model both `channel` and `extension` update targets. At this commit, the C++ SDK's `ReceiveMessage` dispatcher explicitly invokes `OnStateUpdate` only for `meta.target: "channel"`. Raw clients can route both targets; C++ SDK users should verify extension-update handling before depending on it.

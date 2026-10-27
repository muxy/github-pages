---
title: GameLink WebSocket Polling
description: Create, configure, read, subscribe to, stop, and delete GameLink polls
  using the pinned wire schema.
slug: ws-polling
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

# GameLink WebSocket Polling

Poll operations use `params.target: "poll"`. A poll has an ID, prompt, options, optional configuration and user data, status, and aggregate results.

!!! warning "Release status"
    This page is pinned to untagged public commit `16c6b97`; publication remains blocked until a versioned GameLink contract is available.

See [GameLink WebSocket Protocol](websocket-protocol.md) for the common envelope and [broadcasts and subscriptions](ws-pubsub.md) for subscription conventions.

## Limits in the pinned client

The C++ SDK enforces these limits before queuing a create request:

| Field | Limit |
| --- | --- |
| `prompt` | At most 256 bytes in the C++ string. |
| `options` | At most 10 entries. |
| Each option | At most 128 bytes in the C++ string. |

The request schema's `GetPollRequest` documentation also states a maximum poll ID length of 64 characters, but the pinned client does not enforce that limit locally. Although comments on some response structures still say 64 options, the executable limit is `POLL_MAX_OPTIONS = 10`; use 10.

Optional poll configuration uses these source-defined fields:

| Field | Contract |
| --- | --- |
| `userIDVoting` | If `true`, only users who shared an ID can vote. |
| `distinctOptionsPerUser` | Integer from 1 through 258. Default `1`. |
| `totalVotesPerUser` | Integer from 1 through 1024. Default `1`. |
| `votesPerOption` | Integer from 1 through 1024. Default `1`. |
| `disabled` | Whether voting is disabled. Default `false`. |
| `startsAt`, `endsAt` | Absolute Unix timestamps in seconds; `0` means unset. |
| `startsIn`, `endsIn` | Relative seconds; ignored when the corresponding absolute field is nonzero. |

## Create a poll

```json
{
  "action": "create",
  "params": {
    "request_id": 40,
    "target": "poll"
  },
  "data": {
    "poll_id": "favorite-color",
    "prompt": "What is your favorite color?",
    "options": [
      "Blue",
      "Red",
      "Orange"
    ]
  }
}
```

Creating a poll with an existing `poll_id` overwrites it. To attach configuration and developer-defined data, add `config` and `user_data`:

```json
{
  "action": "create",
  "params": {
    "request_id": 41,
    "target": "poll"
  },
  "data": {
    "poll_id": "favorite-color",
    "prompt": "What is your favorite color?",
    "options": [
      "Blue",
      "Red",
      "Orange"
    ],
    "config": {
      "userIDVoting": true,
      "distinctOptionsPerUser": 1,
      "totalVotesPerUser": 1,
      "votesPerOption": 1,
      "disabled": false,
      "startsAt": 0,
      "endsAt": 0,
      "startsIn": 0,
      "endsIn": 300
    },
    "user_data": {
      "has_mystery_prize": true
    }
  }
}
```

## Subscribe and unsubscribe

Use the poll ID as `data.topic_id`.

```json
{
  "action": "subscribe",
  "params": {
    "request_id": 42,
    "target": "poll"
  },
  "data": {
    "topic_id": "favorite-color"
  }
}
```

Send the same target and selector with `action: "unsubscribe"` to stop receiving updates. The pinned source does not define `*` as a poll-subscription wildcard.

## Poll update

Server updates use a response envelope with `meta`, not a request envelope with `params`.

```json
{
  "meta": {
    "request_id": 65535,
    "action": "update",
    "target": "poll",
    "timestamp": 1590011391849
  },
  "data": {
    "poll": {
      "poll_id": "favorite-color",
      "prompt": "What is your favorite color?",
      "status": "active",
      "options": [
        "Blue",
        "Red",
        "Orange"
      ]
    },
    "results": [
      50,
      2,
      13
    ],
    "mean": 0.4307692308,
    "sum": 28,
    "count": 65
  }
}
```

`results` contains option vote counts, but the source explicitly permits it to have a different length from `poll.options`. `mean`, `sum`, and `count` include numeric responses outside the option-index range.

## Get current results

```json
{
  "action": "get",
  "params": {
    "request_id": 43,
    "target": "poll"
  },
  "data": {
    "poll_id": "favorite-color"
  }
}
```

The response uses `meta.action: "get"`, `meta.target: "poll"`, and the same `data.poll`, `data.results`, `data.mean`, `data.sum`, and `data.count` fields as an update.

## Reconfigure or stop a poll

Set the disabled state with `reconfigure`:

```json
{
  "action": "reconfigure",
  "params": {
    "request_id": 44,
    "target": "poll"
  },
  "data": {
    "poll_id": "favorite-color",
    "config": {
      "disabled": true
    }
  }
}
```

The pinned SDK stops a poll by sending the same action with `"config": { "endsAt": -1 }`.

## Delete a poll

```json
{
  "action": "delete",
  "params": {
    "request_id": 45,
    "target": "poll"
  },
  "data": {
    "poll_id": "favorite-color"
  }
}
```

If ordering matters when replacing a poll, wait for the delete response before sending the new create request.

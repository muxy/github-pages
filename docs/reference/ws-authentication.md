---
title: GameLink WebSocket Authentication
description: Authenticate a GameLink WebSocket connection with a PIN or refresh token
  using the pinned wire schema.
slug: ws-authentication
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

# GameLink WebSocket Authentication

Authenticate a connected client by sending `action: "authenticate"` with either a PIN or a refresh token. The authentication target is empty, so the pinned serializer omits `params.target`.

!!! warning "Release status"
    This page is pinned to untagged public commit `16c6b97`; publication remains blocked until a versioned GameLink contract is available.

See [GameLink WebSocket Protocol](websocket-protocol.md) for hosts and the common envelope.

## Authenticate with a PIN

Obtain the broadcaster-entered PIN through your approved extension authentication flow, then send it with the extension client ID.

```json
{
  "action": "authenticate",
  "params": {
    "request_id": 1
  },
  "data": {
    "pin": "pZV4Se",
    "client_id": "extension-client-id"
  }
}
```

The schema also supports a Muxy-assigned game ID:

```json
{
  "action": "authenticate",
  "params": {
    "request_id": 2
  },
  "data": {
    "pin": "pZV4Se",
    "client_id": "extension-client-id",
    "game_id": "game-id"
  }
}
```

The pinned public repository does not define the PIN-issuance HTTP endpoint or token lifetimes. Do not infer those deployment policies from this WebSocket schema.

## Successful response

The response body can contain an access JWT, a refresh token, and Twitch channel identity fields.

```json
{
  "meta": {
    "request_id": 1,
    "action": "authenticate",
    "target": "",
    "timestamp": 1583777666077
  },
  "data": {
    "jwt": "eyJhbG...",
    "refresh": "eyJhbG...",
    "twitch_name": "channel_name",
    "twitch_id": "123456789"
  }
}
```

Treat both tokens as secrets. Use `jwt` for authorized operations and retain `refresh` only in storage appropriate for long-lived credentials.

## Authenticate with a refresh token

Reconnect without asking for another PIN by sending the refresh token and the same client ID. Include `game_id` if the initial authentication used it.

```json
{
  "action": "authenticate",
  "params": {
    "request_id": 3
  },
  "data": {
    "refresh": "eyJhbG...",
    "client_id": "extension-client-id"
  }
}
```

A successful refresh has the same response shape as PIN authentication. Replace the stored refresh token when the server returns a new one.

## Error response

Failed authentication leaves the connection unauthenticated and returns the common error envelope.

```json
{
  "meta": {
    "request_id": 3,
    "action": "authenticate",
    "target": "",
    "timestamp": 1583779685222
  },
  "errors": [
    {
      "number": 403,
      "title": "Not authorized",
      "detail": "The supplied credential could not be authorized"
    }
  ]
}
```

## Authentication subscription in the schema

The pinned schema defines this subscription request:

```json
{
  "action": "subscribe",
  "params": {
    "request_id": 4,
    "target": "authentication"
  }
}
```

However, the public C++ SDK invokes its authentication callback directly from `authenticate` responses and exposes no public method that queues this subscription. Raw clients should not require the subscription to complete the request-response authentication flow.

After authentication, continue with [state](ws-state-access.md), [polls](ws-polling.md), [viewer broadcasts](ws-pubsub.md), or [purchase transactions](ws-purchase-transactions.md).

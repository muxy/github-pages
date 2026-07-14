---
title: GameLink WebSocket Protocol
description: Connect to GameLink and exchange source-verified request, response, update, and error envelopes.
slug: websocket-protocol
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

# GameLink WebSocket Protocol

GameLink uses a persistent WebSocket connection for authentication, state, polls, viewer broadcasts, and purchase transactions. This reference describes the wire contract implemented by public `muxy/gamelink-cpp` commit `16c6b9796ae02105153ac33482d83ac609398d2e`.

!!! warning "Release status"
    No public `gamelink-cpp` tag points to this contract. The documentation is pinned to `commit-16c6b97` and remains blocked for release until Muxy publishes or approves a versioned contract, including deployment limits and reconnect policy.

## Connection addresses

The pinned library identifies its protocol version as `0.2.0`. Its URL helper returns a host and path without a URI scheme; prepend `wss://` in every deployed client.

| Environment | Secure WebSocket address |
| --- | --- |
| Production | `wss://gamelink.muxy.io/0.2.0/{client_id}` |
| Sandbox | `wss://gamelink.sandbox.muxy.io/0.2.0/{client_id}` |

A language projection can identify itself with this path:

```text
wss://{host}/0.2.0/{projection}/{projection_version}/{client_id}
```

For example, projection `csharp` version `1.2.3` uses `/0.2.0/csharp/1.2.3/{client_id}`.

## Connection lifecycle

1. **Construct and validate the URL.** Select sandbox or production explicitly, require `wss://`, and reject an empty address from the helper.
2. **Open one WebSocket.** Do not send credentials in the URL or query string.
3. **Authenticate.** Use a short-lived PIN for the first session or the previously returned refresh token for later sessions. Wait for a successful authentication response before protected operations.
4. **Exchange requests.** Assign a request ID, send one JSON text message per request, and correlate the response through `meta.request_id`.
5. **Maintain subscriptions.** Route unsolicited `update` messages by `meta.target`. Record successful subscriptions locally so they can be restored after reconnect.
6. **Reconnect deliberately.** Open a new secure socket, authenticate with the stored refresh token, wait for success, then replay active subscriptions. The pinned C++ `HandleReconnect()` queues refresh authentication and replays its tracked purchase, poll, config, state, datastream, and matchmaking subscriptions only when it has a stored refresh token.
7. **Shut down cleanly.** Stop writes, close the socket, release callbacks, and erase credentials when the user deauthenticates.

The pinned wire source does not define heartbeat frames, an idle timeout, a retry ceiling, or server-directed backoff. A transport should use bounded exponential backoff with jitter, stop retrying on explicit authentication failure, and expose a recoverable offline state to the game.

## Request envelope

Every client request has an `action`, `params`, and, when the operation needs one, `data`.

```json
{
  "action": "get",
  "params": {
    "request_id": 42,
    "target": "state"
  },
  "data": {
    "state_id": "channel"
  }
}
```

| Field | Contract |
| --- | --- |
| `action` | Operation name such as `authenticate`, `get`, `set`, `patch`, `subscribe`, `unsubscribe`, `broadcast`, `create`, `delete`, `reconfigure`, `refund`, or `validate`. |
| `params.request_id` | Unsigned 16-bit wire field echoed in `meta.request_id`. Use an ID that is not currently in flight. |
| `params.target` | Service target. Empty targets are omitted by the pinned serializer. |
| `data` | Operation-specific JSON. Requests with an empty body can omit it. |

Although the wire field is 16-bit, the pinned SDK allocates IDs by masking to `0x7F`, so its generated values cycle through `0`–`127`. It reserves `65535` for “any/no request” and `65534` for a rejected local request. A raw client may use the wider field, but must not use reserved values or reuse an in-flight ID.

## Response and update envelope

Server messages use `meta`, not the request's top-level `action` and `params` fields.

```json
{
  "meta": {
    "request_id": 42,
    "action": "get",
    "target": "state",
    "timestamp": 1583777221501
  },
  "data": {
    "ok": true,
    "state": {
      "round": 3
    }
  }
}
```

`meta.timestamp` is Unix time in milliseconds. Unsolicited subscription messages use `meta.action: "update"`; route them by `meta.target` and do not assume they correspond to the latest request.

An error response carries an `errors` array. The pinned schema names its numeric field `number`, not `status` or `code`.

```json
{
  "meta": {
    "request_id": 42,
    "action": "get",
    "target": "state",
    "timestamp": 1583777221501
  },
  "errors": [
    {
      "number": 403,
      "title": "Not authorized",
      "detail": "The connection is not authorized for this operation"
    }
  ]
}
```

Treat `errors` as authoritative when present. The schema allows multiple errors and describes `data` and `errors` as mutually exclusive.

## Limits and security

### Source-verified client limits

| Area | Limit in commit `16c6b97` | Boundary |
| --- | --- | --- |
| Client ID | At most 100 characters | URL helper returns an empty string when longer. |
| Generated URL | Must fit a 256-byte local buffer | Applies to host, protocol path, projection metadata, and Client ID together. |
| Projection name | Documented as URL-safe and fewer than 8 characters | The helper relies on final URL length rather than separately enforcing this comment. |
| Request IDs | 16-bit on the wire; pinned allocator cycles `0`–`127` | Keep concurrent IDs unique; avoid `65534` and `65535`. |
| Broadcast data | Serialized message documented as under 8 KiB | Treat this as an application-side maximum before envelope overhead. |
| Receive reassembly | Pinned parser refuses to grow its partial-message buffer beyond 4 MiB | This is a client safety check, not a published server frame limit. |
| Poll definition | Prompt up to 256 bytes, at most 10 options, each up to 128 bytes | Applies to the pinned C++ poll helpers. |

The public source does not publish server connection quotas, messages per second, subscription counts, idle timeout, maximum general frame size, or production retry policy. Obtain those limits from the GameLink owner before capacity planning; never infer them from client buffer sizes.

### Security requirements

- Require TLS with `wss://` and validate the platform trust chain. Never downgrade to `ws://` in production or sandbox.
- Allowlist the exact GameLink host for the selected environment. Do not accept a host override from untrusted configuration.
- Treat PINs, access JWTs, and refresh tokens as secrets. Keep them out of URLs, telemetry, crash reports, and debug logs; store refresh tokens in platform-secure storage.
- Parse only UTF-8 JSON text messages, cap bytes before buffering, reject malformed envelopes, and validate action-specific data before using it in gameplay or UI.
- Keep sandbox and production credentials separate. Changing the hostname does not convert a credential between environments.
- Make purchase handling idempotent by transaction ID and validate authorization before mutating durable game state.

## Service targets

| Capability | Request target | Selector | Reference |
| --- | --- | --- | --- |
| Authenticate | Empty or omitted | `pin` or `refresh` in `data` | [Authentication](ws-authentication.md) |
| Broadcast to viewers | Empty or omitted | `topic` in `data` | [Broadcasts and subscriptions](ws-pubsub.md) |
| Read, replace, or patch state | `state` | `state_id` is `channel` or `extension` | [State access](ws-state-access.md) |
| Subscribe to state | `state` | `topic_id` is `channel` or `extension` | [State access](ws-state-access.md) |
| Manage or subscribe to polls | `poll` | `poll_id` or `topic_id` | [Polling](ws-polling.md) |
| Subscribe to purchase updates | `twitchPurchaseBits` | `sku` or `*` | [Purchase transactions](ws-purchase-transactions.md) |
| Get, refund, or validate transactions | `transaction` | SKU, transaction ID, and/or user ID | [Purchase transactions](ws-purchase-transactions.md) |

## Implementation checklist

1. Connect to the environment-specific `wss://` address with the `0.2.0` path.
2. Authenticate before protected operations and replace stored credentials when the response rotates them.
3. Correlate replies using `meta.request_id`; never expect request-style `params` in a server message.
4. Route unsolicited updates by `meta.action == "update"` and `meta.target`.
5. Handle every `errors[]` entry before consuming `data`.
6. Reauthenticate and restore subscriptions after reconnect, without duplicating callbacks.
7. Enforce local message, queue, retry, and lifetime bounds where the public server contract is silent.

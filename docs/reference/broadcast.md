---
title: Broadcast Messaging
description: Send channel, extension-wide, and back-channel PubSub messages through
  the Muxy REST API.
slug: broadcast
product: REST API
audience: backend developers
status: current
owner: API Platform
source_of_truth: muxy/github-pages:openapi/rest-v1.yaml
version: v1
last_verified: '2026-07-14'
review_state: approved
page_type: protocol-reference
approved_by: peter-bonanni
approved_at: '2026-07-14T20:34:54Z'
approval_method: user-authorized-codex-assisted-source-review
approved_content_sha256: 9bce7aec46d7f4cf53d03c94767ca6184a2b5e78d7cdfcea2b0f7d711538c8ef
---

# Broadcast Messaging

Muxy broadcast endpoints publish developer-defined JSON to Twitch Extension PubSub. All three endpoints use `POST` and the standard `Authorization: <Client ID> <JWT>` header.

## Limits and delivery

Messages at or above 5 KiB are compressed and Base64 encoded, then split into fragments small enough for Twitch PubSub. The compressed, encoded payload must not exceed 80 KiB. Keep messages much smaller when possible and store durable data in state or configuration instead.

Sandbox and production broadcasts are isolated. Delivery is real time but not a durable queue; consumers must tolerate reconnects and missed messages.

## Send to a channel

`POST /v1/e/broadcast` accepts broadcaster, admin, or backend JWTs.

```bash
curl --request POST \
  --url https://api.muxy.io/v1/e/broadcast \
  --header "Authorization: ${MUXY_CLIENT_ID} ${MUXY_JWT}" \
  --header 'content-type: application/json' \
  --data '{
    "target": "broadcast",
    "event": "score-updated",
    "user_id": "12345678",
    "data": { "score": 42 }
  }'
```

| Field | Meaning |
| --- | --- |
| `target` | `broadcast` for everyone on the channel or `whisper-U<opaque-user-id>` for one viewer |
| `event` | Developer-defined event name; defaults to `default` when omitted |
| `user_id` | Twitch channel/broadcaster ID |
| `data` | JSON object delivered to subscribers |

## Send extension-wide

`POST /v1/e/extension_broadcast` requires a privileged broadcaster, admin, or backend JWT and queues the message for every active channel using the extension.

```bash
curl --request POST \
  --url https://api.muxy.io/v1/e/extension_broadcast \
  --header "Authorization: ${MUXY_CLIENT_ID} ${MUXY_JWT}" \
  --header 'content-type: application/json' \
  --data '{
    "event": "catalog-updated",
    "data": { "revision": 7 }
  }'
```

## Send to the current viewer

`POST /v1/e/whisper_self` sends a back-channel message to the same authorized viewer context. It is useful for coordinating multiple surfaces of one extension.

```bash
curl --request POST \
  --url https://api.muxy.io/v1/e/whisper_self \
  --header "Authorization: ${MUXY_CLIENT_ID} ${MUXY_JWT}" \
  --header 'content-type: application/json' \
  --data '{
    "event": "settings-saved",
    "data": { "ok": true }
  }'
```

Successful requests return HTTP 200. Treat any non-2xx response as undelivered and apply bounded retry logic only where duplicate messages are safe.

See [GameLink event handling](event-handling.md#datastream-events) for subscription callbacks.

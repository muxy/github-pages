---
title: Basic Accumulation
description: Basic accumulation allows you to collect large amounts of user input
  into a list for consumption by a backend.
slug: accumulate
product: REST API
audience: developers
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
approved_content_sha256: b1c76c068b0e2b3e9314b9fdb002742ec1abd43ac08a636cb39ff5bffd166f94
---

# Basic Accumulation

Accumulation buffers accept small JSON objects from authenticated extension users and return timestamped entries to privileged callers. The base URL is `https://api.muxy.io/v1/e`.

| Operation | Allowed JWT roles | Purpose |
| --- | --- | --- |
| `POST /accumulate` | Any authenticated role | Append an object to a named buffer. |
| `GET /accumulate` | `broadcaster`, `admin`, or `backend` | Read entries after a timestamp. |

## POST /accumulate

See the generated [POST `/accumulate` reference](accumulate-2.md).

Use `id` to select the buffer; it defaults to `default`. The request body must be a JSON object.

```http
POST /v1/e/accumulate?id=feedback
```

```json
{
  "rating": 5,
  "comment": "Great stream"
}
```

The server adds `observed`, `channel_id`, `opaque_user_id`, and `user_id`, then appends the entry. A successful request returns:

```json
{}
```

Malformed JSON returns `400` with reason `Malformed json body`.

## GET /accumulate

See the generated [GET `/accumulate` reference](accumulate-1.md).

```http
GET /v1/e/accumulate?id=feedback&start=1720000000000
```

| Query parameter | Meaning |
| --- | --- |
| `id` | Buffer name. Defaults to `default`. |
| `start` | Unix timestamp in milliseconds. Defaults to `0`; the lower bound is exclusive. |

`broadcaster` JWTs receive only entries whose `channel_id` matches the JWT channel. `admin` and `backend` JWTs receive entries for the extension across channels. Other roles receive `403`. A non-integer `start` returns `400` with reason `Malformed start parameter`.

```json
{
  "data": [
    {
      "observed": 1720000000123,
      "channel_id": "12345",
      "opaque_user_id": "U12345",
      "user_id": "",
      "data": {
        "rating": 5,
        "comment": "Great stream"
      }
    },
    {
      "observed": 1720000000456,
      "channel_id": "12345",
      "opaque_user_id": "U67890",
      "user_id": "67890",
      "data": {
        "rating": 4
      }
    }
  ],
  "latest": 1720000000456
}
```

The `data` array is in ascending `observed` order, from oldest to newest. `latest` is the `observed` value of the final returned entry, or `0` when no entries are returned. For duplicate-free polling, pass the previous `latest` as the next exclusive `start` value.

`opaque_user_id` is the opaque Twitch identity from the caller's JWT; `user_id` may be empty when the viewer has not shared a Twitch user ID.

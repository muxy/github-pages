---
title: Poll Management
description: The voting endpoints allow for high-volume polling activity.
slug: poll-managment
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
approved_content_sha256: 4b781aa227c2c552637295f71ffff35fc3511eaaae689f9d934fe83fe7a096b9
---

# Poll Management

The voting API records votes, computes statistics, applies per-user weights, and optionally stores poll configuration. The base URL is `https://api.muxy.io/v1/e`, and every route requires a valid Muxy extension JWT.

Generated operation pages are linked from each method/path section. The raw specification is available as [`rest-v1.yaml`](https://docs.muxy.io/openapi/rest-v1.yaml); the guidance below describes behavior that spans the current `rest-api` handlers.

| Route | Allowed JWT roles |
| --- | --- |
| `GET /vote` | Any authenticated role |
| `POST /vote` | Any authenticated role |
| `DELETE /vote` | `broadcaster`, `admin`, or `backend` |
| `GET /vote_logs` | `backend`, or an `admin` JWT for the extension owner or a listed extension admin |
| `POST /vote_modifier` | `broadcaster`, `admin`, or `backend` |
| `GET /vote_config` | Any authenticated role |
| `POST /vote_config` | `broadcaster`, `admin`, or `backend` |

For routes with an `id` query parameter, the default is `default`. IDs beginning with `global` use extension-wide storage; other IDs are scoped to the JWT's extension and channel.

## Vote values, counts, and statistics

Vote values are integers from `-128` through `128`, inclusive. Statistics are returned as top-level fields, not under a `stats` object.

- `specific` always has 32 elements. Indexes `0` through `31` count those exact values.
- Values outside `0..31` still contribute to `stddev`, `mean`, `sum`, and `count`.
- In the default single-vote mode, a later vote from the same identity replaces the stored vote, so `count` is not a request count or a unique-request count.
- In configured multi-vote mode, `count` is the number of stored vote entries after modifiers. A positive modifier can make it larger than the number of users; a modifier of `-1` or less removes that user's votes from statistics.

## GET /vote

See the generated [GET `/vote` reference](vote-get.md).

Returns the poll statistics and, when present, the caller's latest known vote.

```http
GET /v1/e/vote?id=round-1
```

```json
{
  "stddev": 0,
  "mean": 2,
  "sum": 2,
  "specific": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "count": 1,
  "decay": {
    "last_nudged": 0,
    "val": 0,
    "current_scale": 0,
    "last_altered": 0
  },
  "vote": 2
}
```

`vote` is omitted when the caller has no known vote. An unknown or empty poll returns zero statistics rather than `404`.

## POST /vote

See the generated [POST `/vote` reference](vote-submit.md).

Casts or replaces a vote. `value` must be in `-128..128`; if omitted, the current handler uses the integer zero value. `count` is optional: missing or `0` becomes `1`.

```http
POST /v1/e/vote?id=round-1
```

```json
{
  "value": 2,
  "count": 1
}
```

`count` submits that many copies of `value` in one request. It must be positive after defaulting, no greater than `30`, and no greater than the poll's configured `totalVotesPerUser`. The default poll configuration allows one total vote, so counts above `1` require a multi-vote configuration. The response has the same shape as `GET /vote` and includes the submitted `vote`.

Common `400` reasons are `Invalid body`, `Value out of bounds`, `Count out of bounds`, `poll is closed`, and `unacceptable vote`.

## DELETE /vote

See the generated [DELETE `/vote` reference](vote-delete.md).

Deletes the poll's current vote state, known-vote cache, and saved configuration, then broadcasts a vote deletion event. It is safe when the poll does not exist.

```http
DELETE /v1/e/vote?id=round-1
```

The response is `{}`. This handler does not delete the poll's `vote_logs`; a later unconfigured `POST /vote` can create active vote state for the same ID again. Disallowed roles receive `403`.

## GET /vote_logs

See the generated [GET `/vote_logs` reference](vote-logs.md).

Returns stored vote log records in ascending receipt order. Because the response can be large, reserve this route for trusted processing backends.

```http
GET /v1/e/vote_logs?id=round-1
```

```json
{
  "result": [
    {
      "identifier": "67890",
      "opaque": "U12345",
      "value": 2,
      "timestamp": 1720000000
    }
  ]
}
```

`identifier` is the shared Twitch `user_id` recorded with the submission and may be empty; `opaque` is the recorded `opaque_user_id`. `timestamp` is Unix time in seconds. Unauthorized admin access returns `403`; storage failures return `500`.

## POST /vote_modifier

See the generated [POST `/vote_modifier` reference](vote-modifier.md).

Adds a persistent weighting modifier for one poll identity. `user` must match the identifier used by that poll: normally `opaque_user_id`, or shared `user_id` when `userIDVoting` is enabled.

```http
POST /v1/e/vote_modifier?id=round-1
```

```json
{
  "user": "U12345",
  "add": 2
}
```

Modifiers accumulate. A user's effective contribution to statistics is `max(0, 1 + total modifiers)` times each stored vote. Success returns `{}`; malformed JSON returns `400` with reason `Invalid body`, and disallowed roles receive `403`.

## GET /vote_config

See the generated [GET `/vote_config` reference](vote-config-get.md).

Returns an explicitly saved configuration. Polls created only by `POST /vote` do not have one and return `404` with `{}`.

```http
GET /v1/e/vote_config?id=round-1
```

```json
{
  "userIDVoting": false,
  "distinctOptionsPerUser": 1,
  "totalVotesPerUser": 1,
  "votesPerOption": 1,
  "global": false,
  "disabled": false,
  "prompt": "",
  "options": ["Yes", "No"],
  "userData": null,
  "endsAt": 1720003600,
  "startsAt": 1720000000,
  "status": "active"
}
```

`startsAt` and `endsAt` are Unix seconds; `status` is `pending`, `active`, or `expired`. The current GET handler returns `prompt` as an empty string and `userData` as `null`, even if values were supplied when configuring the poll.

## POST /vote_config

See the generated [POST `/vote_config` reference](vote-config-post.md).

Creates or updates an explicit configuration. Unlike the other routes, the poll `id` is in the JSON body.

```http
POST /v1/e/vote_config
```

```json
{
  "id": "round-1",
  "config": {
    "userIDVoting": false,
    "distinctOptionsPerUser": 1,
    "totalVotesPerUser": 1,
    "votesPerOption": 1,
    "global": false,
    "disabled": false,
    "prompt": "Choose one",
    "options": ["Yes", "No"],
    "userData": {
      "round": 1
    },
    "startsAt": 1720000000,
    "endsAt": 1720003600
  }
}
```

Configuration limits enforced by the handler are:

- `id` defaults to `default`, is at most 64 characters, and cannot contain `.`. If `global` is true, `id` must begin with `global`.
- `distinctOptionsPerUser` is `1..258`; `totalVotesPerUser` is `1..1024`; `votesPerOption` must be greater than `0`. All three default to `1` when omitted.
- `options` has at most 32 strings, each at most 128 bytes. `prompt` is at most 256 bytes, and encoded `userData` is at most 1024 bytes.
- `startsAt` and `endsAt` are Unix seconds. When both are treated as set, `startsAt` cannot be after `endsAt`.

Success returns `{}`. Invalid bounds, ID/global mismatches, closed-time ordering, and oversized fields return `400` with a `reason`; disallowed roles receive `403`; configuration storage failures return `500`.

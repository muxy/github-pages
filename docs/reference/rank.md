---
title: Basic Ranking
description: The REST API provides a ranking service that collects user input and
  counts matching values.
slug: rank
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
approved_content_sha256: 6247216df54365185c6492ae3053a945abe46576dbb1a52801bf71426de77d6f
---

# Basic Ranking

The ranking API counts exact string responses for a developer-defined question ID. Use it for open-ended prompts such as “Which game should we play next?” when you need frequency counts rather than a fixed-choice numeric poll.

Base URL: `https://api.muxy.io/v1/e`

| Operation | JWT role | Purpose |
| --- | --- | --- |
| [`POST /rank`](rank-2.md) | Any authenticated role | Submit or replace the caller's answer. |
| [`GET /rank`](rank-1.md) | `broadcaster`, `admin`, or `backend` | Read scored answers. |
| [`DELETE /rank`](rank-3.md) | `broadcaster`, `admin`, or `backend` | Clear the selected ranking buffer. |

Every request sends `Authorization: <Twitch Extension Client ID> <Muxy JWT>`.

## Choose the ranking ID

The `id` query parameter identifies one question buffer and defaults to `default`. Use an explicit round-specific ID in production:

```text
next-game-2026-07-14-round-3
```

The API contract does not assign meaning to an ID prefix. In particular, the pinned OpenAPI source does not define the legacy `global` prefix behavior. Do not depend on undocumented cross-channel aggregation.

## Submit an answer

Send a JSON object with one string `key`:

```bash
curl --request POST \
  --url 'https://api.muxy.io/v1/e/rank?id=next-game-2026-07-14-round-3' \
  --header 'authorization: <Client ID> <viewer JWT>' \
  --header 'content-type: application/json' \
  --data '{"key":"DOTA"}'
```

A successful response reports whether the submission was accepted. `original` is optional and can contain the caller's previous answer when it was replaced:

```json
{
  "accepted": true,
  "original": "Serious Sam"
}
```

Normalize input before submission if spelling, capitalization, or repeated whitespace should count as the same answer. The service treats the submitted string as the result key; it does not moderate or escape it.

## Retrieve results

```bash
curl --request GET \
  --url 'https://api.muxy.io/v1/e/rank?id=next-game-2026-07-14-round-3' \
  --header 'authorization: <Client ID> <broadcaster JWT>'
```

The response contains each returned answer and its score:

```json
{
  "data": [
    { "key": "DOTA", "score": 12 },
    { "key": "FIFA 2014", "score": 8 }
  ]
}
```

Render `key` as untrusted viewer input. Use text escaping, apply product moderation rules, and preserve the returned order unless your application defines a tie-break.

## Clear results

```bash
curl --request DELETE \
  --url 'https://api.muxy.io/v1/e/rank?id=next-game-2026-07-14-round-3' \
  --header 'authorization: <Client ID> <broadcaster JWT>'
```

Success returns an empty object:

```json
{}
```

Deletion is destructive. Prefer a new ID for each round when late clients may still submit or when results must remain auditable.

## Contract boundaries

The pinned OpenAPI contract describes request/response shapes and endpoint roles. It does not guarantee automatic expiry, a top-100 cutoff, normalization, moderation, tie ordering, or cross-channel ID conventions. Those claims appeared in legacy prose but must not be treated as versioned API guarantees without API-owner confirmation.

JavaScript clients can use [`rank()`, `getRankData()`, and `clearRankData()`](../docs/ranking.md) instead of calling these endpoints directly.

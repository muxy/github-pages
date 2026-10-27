---
title: Get Vote Totals
description: Get aggregate statistics and the current viewer vote for a poll.
slug: vote-get
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
approved_content_sha256: 7f231c468943aa57a080ff365a6b171283b69443e10ed5b58db29345fa86364b
---

# Get Vote Totals

## `GET /vote`

Returns aggregate statistics and, when available, the current viewer's known vote.

### Authorization

Send `Authorization: <Twitch Extension Client ID> <Muxy JWT>`. The JWT role must satisfy the endpoint requirements shown in the examples.

### Parameters

| Name | In | Required | Type | Constraints | Description |
| --- | --- | --- | --- | --- | --- |
| `id` | query | no | `string` | default `"default"`; at most 64 characters | Poll identifier. Defaults to `default`; global polls use an ID beginning with `global`. |

### Responses

#### 200 Response

Current vote statistics.

Content type: `application/json`

##### Schema

```json
{
  "type": "object",
  "required": [
    "stddev",
    "mean",
    "sum",
    "specific",
    "count",
    "decay"
  ],
  "properties": {
    "stddev": {
      "type": "number",
      "description": "Sample standard deviation across effective stored votes."
    },
    "mean": {
      "type": "number",
      "description": "Mean of all effective stored vote values."
    },
    "sum": {
      "type": "number",
      "description": "Sum of all effective stored vote values."
    },
    "specific": {
      "type": "array",
      "description": "Exactly 32 counters. Indexes 0 through 31 count votes whose value equals that index; values outside this range still contribute to the other statistics.",
      "minItems": 32,
      "maxItems": 32,
      "items": {
        "type": "integer",
        "minimum": 0
      }
    },
    "count": {
      "type": "integer",
      "minimum": 0,
      "description": "Number of effective stored vote entries after per-user replacement and modifiers; this is not the number of requests."
    },
    "decay": {
      "type": "object",
      "additionalProperties": true
    },
    "vote": {
      "type": "integer",
      "minimum": -128,
      "maximum": 128,
      "description": "The caller's known vote, omitted when no vote is known."
    }
  }
}
```

##### Example

```json
{
  "stddev": 0,
  "mean": 1,
  "sum": 2,
  "specific": [
    0,
    2,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  "count": 2,
  "decay": {},
  "vote": 1
}
```

!!! info "Generated API reference"
    This endpoint is generated from [`rest-v1.yaml`](https://docs.muxy.io/openapi/rest-v1.yaml).

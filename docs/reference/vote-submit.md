---
title: Submit Votes
description: Submit one or more votes to a poll.
slug: vote-submit
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
approved_content_sha256: dd10963d0bcf25ea16b3999a1a9b6956b1a86edc65c68099320b17903b0063fd
---

# Submit Votes

## `POST /vote`

Submits a value from -128 through 128. If `value` is omitted the handler submits `0`. Missing or explicit `count: 0` becomes `1`; positive counts are capped at 30 per request and must also fit the poll's configured per-user limit.

### Authorization

Send `Authorization: <Twitch Extension Client ID> <Muxy JWT>`. The JWT role must satisfy the endpoint requirements shown in the examples.

### Parameters

| Name | In | Required | Type | Constraints | Description |
| --- | --- | --- | --- | --- | --- |
| `id` | query | no | `string` | default `"default"`; at most 64 characters | Poll identifier. Defaults to `default`; global polls use an ID beginning with `global`. |

### Request body

Content type: `application/json`

#### Schema

```json
{
  "type": "object",
  "properties": {
    "value": {
      "type": "integer",
      "minimum": -128,
      "maximum": 128,
      "default": 0
    },
    "count": {
      "type": "integer",
      "minimum": 0,
      "maximum": 30,
      "default": 1,
      "description": "Number of copies to submit. The service treats 0 as 1."
    }
  }
}
```

#### Example

```json
{
  "value": 1,
  "count": 1
}
```

### Responses

#### 200 Response

Vote accepted and current statistics returned.

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

#### 400 Error

The request body or poll configuration is invalid.

Content type: `application/json`

##### Schema

```json
{
  "type": "object",
  "properties": {
    "reason": {
      "type": "string"
    }
  }
}
```

##### Example

```json
{
  "reason": "Invalid body"
}
```

!!! info "Generated API reference"
    This endpoint is generated from [`rest-v1.yaml`](https://docs.muxy.io/openapi/rest-v1.yaml).

---
title: Get Poll Configuration
description: Get stored limits, schedule, options, and status for a poll.
slug: vote-config-get
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
approved_content_sha256: e92d681c15f0aad86118ddb3dcc7a14c18c9aa2a6b7dc64dff1ac4adae96620f
---

# Get Poll Configuration

## `GET /vote_config`

Returns the stored configuration and computed poll status.

### Authorization

Send `Authorization: <Twitch Extension Client ID> <Muxy JWT>`. The JWT role must satisfy the endpoint requirements shown in the examples.

### Parameters

| Name | In | Required | Type | Constraints | Description |
| --- | --- | --- | --- | --- | --- |
| `id` | query | no | `string` | default `"default"`; at most 64 characters | Poll identifier. Defaults to `default`; global polls use an ID beginning with `global`. |

### Responses

#### 200 Response

Poll configuration.

Content type: `application/json`

##### Schema

```json
{
  "type": "object",
  "properties": {
    "userIDVoting": {
      "type": "boolean"
    },
    "distinctOptionsPerUser": {
      "type": "integer",
      "minimum": 1,
      "maximum": 258,
      "default": 1
    },
    "totalVotesPerUser": {
      "type": "integer",
      "minimum": 1,
      "maximum": 1024,
      "default": 1
    },
    "votesPerOption": {
      "type": "integer",
      "minimum": 1,
      "maximum": 1024,
      "default": 1
    },
    "global": {
      "type": "boolean"
    },
    "disabled": {
      "type": "boolean"
    },
    "prompt": {
      "type": "string"
    },
    "options": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "userData": {},
    "endsAt": {
      "type": "integer",
      "description": "Unix timestamp in seconds."
    },
    "startsAt": {
      "type": "integer",
      "description": "Unix timestamp in seconds."
    },
    "status": {
      "type": "string",
      "enum": [
        "pending",
        "active",
        "expired"
      ],
      "readOnly": true
    }
  }
}
```

#### 404 Error

No configuration exists for this poll.

Content type: `application/json`

##### Schema

```json
{
  "type": "object"
}
```

##### Example

```json
{}
```

!!! info "Generated API reference"
    This endpoint is generated from [`rest-v1.yaml`](https://docs.muxy.io/openapi/rest-v1.yaml).

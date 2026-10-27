---
title: Accumulate
description: Retrieve entries from a named accumulation buffer.
slug: accumulate-1
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
approved_content_sha256: 9d60dc557c9ce839cbeab5e84e8187dbe4aad69badb15f4e5e4da908ca5985af
---

# Accumulate

## `GET /accumulate`

Accumulate

Requires an admin, backend, or broadcaster JWT.

### Authorization

Send `Authorization: <Twitch Extension Client ID> <Muxy JWT>`. The JWT role must satisfy the endpoint requirements shown in the examples.

### Parameters

| Name | In | Required | Type | Constraints | Description |
| --- | --- | --- | --- | --- | --- |
| `id` | query | no | `string` | default `"default"` | The name of the accumulation buffer from which to retrieve data. |
| `start` | query | no | `integer` | default `0` | Unix millisecond timestamp of earliest entry to include in the result. |

### Responses

#### 200 Response

200

Content type: `application/json`

##### Schema

```json
{
  "type": "object",
  "properties": {
    "data": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "observed": {
            "type": "integer",
            "example": 1634401498121,
            "default": 0
          },
          "channel_id": {
            "type": "string",
            "example": "12345"
          },
          "opaque_user_id": {
            "type": "string",
            "example": "U12345"
          },
          "user_id": {
            "type": "string",
            "example": "12345"
          },
          "data": {
            "type": "object",
            "properties": {}
          }
        }
      }
    },
    "latest": {
      "type": "integer",
      "example": 1634401498121,
      "default": 0
    }
  }
}
```

##### Example

```json
{
  "data": [
    {
      "observed": 1634401498121,
      "channel_id": "12345",
      "opaque_user_id": "U12345",
      "user_id": "",
      "data": {
        "next_game": "Day of the Tentacle"
      }
    }
  ],
  "latest": 1634401498121
}
```

#### 400 Error

400

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
  "reason": "400"
}
```

#### 403 Error

The JWT role is not allowed to perform this operation.

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
  "reason": "The JWT role is not allowed to perform this operation."
}
```

### Examples

#### Curl

```curl
curl --request GET \
  --url https://api.muxy.io/v1/e/accumulate \
  --header 'authorization: <Client ID> <broadcaster, admin, or backend JWT>' \
  --header 'content-type: application/json'
```

!!! info "Generated API reference"
    This endpoint is generated from [`rest-v1.yaml`](https://docs.muxy.io/openapi/rest-v1.yaml).

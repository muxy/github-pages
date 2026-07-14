---
title: Rank
description: Retrieve ranked values from a named ranking buffer.
slug: rank-1
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
approved_content_sha256: ea4daa80f79a687ae97ebe1a77b0365f39dc21a2e195c33915a5482d2f039e7f
---

# Rank

## `GET /rank`

Rank

### Authorization

Send `Authorization: <Twitch Extension Client ID> <Muxy JWT>`. The JWT role must satisfy the endpoint requirements shown in the examples.

### Parameters

| Name | In | Required | Type | Constraints | Description |
| --- | --- | --- | --- | --- | --- |
| `id` | query | no | `string` | default `"default"` | The ranking-buffer ID that identifies a question for which responses are ranked. |

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
          "key": {
            "type": "string",
            "example": "DOTA"
          },
          "score": {
            "type": "integer",
            "example": 12,
            "default": 0
          }
        }
      }
    }
  }
}
```

##### Result

```json
{
  "data": [
    {
      "key": "DOTA",
      "score": 12
    },
    {
      "key": "FIFA 2014",
      "score": 8
    }
  ]
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

### Examples

#### Curl

```curl
curl --request GET \
  --url https://api.muxy.io/v1/e/rank?id=next-game \
  --header 'authorization: <Client ID> <backend, admin, or broadcaster JWT>' \
  --header 'content-type: application/json'
```

!!! info "Generated API reference"
    This endpoint is generated from [`rest-v1.yaml`](https://docs.muxy.io/openapi/rest-v1.yaml).

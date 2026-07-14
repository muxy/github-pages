---
title: Rank
description: Submit a value to a named ranking buffer.
slug: rank-2
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
approved_content_sha256: be01b422d2a63067f159e4593d70ef13364a0438bb6bc292b4a6a2e52791f00b
---

# Rank

## `POST /rank`

Rank

### Authorization

Send `Authorization: <Twitch Extension Client ID> <Muxy JWT>`. The JWT role must satisfy the endpoint requirements shown in the examples.

### Parameters

| Name | In | Required | Type | Constraints | Description |
| --- | --- | --- | --- | --- | --- |
| `id` | query | no | `string` | default `"default"` | The ranking-buffer ID that identifies a question for which responses are ranked. |

### Request body

Content type: `application/json`

#### Schema

```json
{
  "type": "object",
  "properties": {
    "key": {
      "type": "string",
      "description": "A string submitted by the user in response to this question, as the `key` value in a JSON object."
    }
  }
}
```

### Responses

#### 200 Response

200

Content type: `application/json`

##### Schema

```json
{
  "type": "object",
  "properties": {
    "accepted": {
      "type": "boolean",
      "example": true,
      "default": true
    },
    "original": {
      "type": "string",
      "example": "Serious Sam"
    }
  }
}
```

##### Example

```json
{
  "accepted": true,
  "original": "Serious Sam"
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
curl --request POST \
  --url https://api.muxy.io/v1/e/rank?id=next-game \
  --header 'authorization: <Client ID> <any JWT>' \
  --header 'content-type: application/json' \
  --data '{ "key": "Last of Us" }'
```

!!! info "Generated API reference"
    This endpoint is generated from [`rest-v1.yaml`](https://docs.muxy.io/openapi/rest-v1.yaml).

---
title: Rank
description: Delete a named ranking buffer and its stored values.
slug: rank-3
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
approved_content_sha256: 57ab0aa309b8253e45420608e72cacdf8b79f59809ce56c4809c7a98b9a1131a
---

# Rank

## `DELETE /rank`

Rank

### Authorization

Send `Authorization: <Twitch Extension Client ID> <Muxy JWT>`. The JWT role must satisfy the endpoint requirements shown in the examples.

### Parameters

| Name | In | Required | Type | Constraints | Description |
| --- | --- | --- | --- | --- | --- |
| `id` | query | no | `string` | default `"default"` | The ID that identifies a question being ranked. |

### Responses

#### 200 Response

200

Content type: `application/json`

##### Schema

```json
{
  "type": "object",
  "properties": {}
}
```

##### Result

```json
{}
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
curl --request DELETE \
  --url https://api.muxy.io/v1/e/rank?id=next-game \
  --header 'authorization: <Client ID> <broadcaster, admin, or backend JWT>' \
  --header 'content-type: application/json'
```

!!! info "Generated API reference"
    This endpoint is generated from [`rest-v1.yaml`](https://docs.muxy.io/openapi/rest-v1.yaml).

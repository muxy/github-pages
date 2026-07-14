---
title: Viewer State
description: Replace channel-scoped state for the current viewer.
slug: viewer-state-1
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
approved_content_sha256: 45c4ae31028ca56af0e40f46b6abbaef4c2dfcab57c78b6ce6b8357cf45d3701
---

# Viewer State

## `POST /viewer_state`

Viewer State

### Authorization

Send `Authorization: <Twitch Extension Client ID> <Muxy JWT>`. The JWT role must satisfy the endpoint requirements shown in the examples.

### Request body

Content type: `application/json`

#### Schema

```json
{
  "type": "object",
  "description": "Complete JSON value to store or submit.",
  "additionalProperties": true
}
```

#### Example

```json
{
  "favorite_color": "blue"
}
```

### Responses

#### 200 Response

Write accepted. The current service returns an empty JSON object.

Content type: `application/json`

##### Schema

```json
{
  "type": "object",
  "maxProperties": 0
}
```

##### Example

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
curl --request POST \
  --url https://sandbox.api.muxy.io/v1/e/viewer_state \
  --header 'authorization: <Client ID> <viewer JWT>' \
  --header 'content-type: application/json' \
  --data '{ "favorite_color": "blue" }'
```

!!! info "Generated API reference"
    This endpoint is generated from [`rest-v1.yaml`](https://docs.muxy.io/openapi/rest-v1.yaml).

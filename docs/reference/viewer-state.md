---
title: All State
description: Retrieve extension, channel, viewer, and extension-viewer state in one
  response.
slug: viewer-state
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
approved_content_sha256: b303a25bc89cecc8a9592da425f29cca06c7c970a82f050f1d0bffa96c835e19
---

# All State

## `GET /all_state`

All State

### Authorization

Send `Authorization: <Twitch Extension Client ID> <Muxy JWT>`. The JWT role must satisfy the endpoint requirements shown in the examples.

### Responses

#### 200 Response

200

Content type: `application/json`

##### Schema

```json
{
  "type": "object",
  "required": [
    "extension",
    "channel",
    "viewer",
    "extension_viewer"
  ],
  "properties": {
    "extension": {
      "type": "object",
      "additionalProperties": true
    },
    "channel": {
      "type": "object",
      "additionalProperties": true
    },
    "viewer": {
      "type": "object",
      "additionalProperties": true
    },
    "extension_viewer": {
      "type": "object",
      "additionalProperties": true
    }
  }
}
```

##### Example

```json
{
  "extension": {},
  "channel": {},
  "viewer": {},
  "extension_viewer": {}
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
  --url https://api.muxy.io/v1/e/all_state \
  --header 'authorization: <Client ID> <any JWT>' \
  --header 'content-type: application/json'
```

!!! info "Generated API reference"
    This endpoint is generated from [`rest-v1.yaml`](https://docs.muxy.io/openapi/rest-v1.yaml).

---
title: Send an Extension-wide Broadcast
description: Publish a Muxy PubSub message to every active extension channel.
slug: broadcast-extension
product: REST API
audience: backend developers
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
approved_content_sha256: 0ebea31f83b3a800a483ed575b5c0066ce6ebb7c76d77ff0a5e6f3cfbe0aea13
---

# Send an Extension-wide Broadcast

## `POST /extension_broadcast`

Requires a privileged broadcaster, admin, or backend JWT.

### Authorization

Send `Authorization: <Twitch Extension Client ID> <Muxy JWT>`. The JWT role must satisfy the endpoint requirements shown in the examples.

### Request body

Content type: `application/json`

#### Schema

```json
{
  "type": "object",
  "properties": {
    "target": {
      "type": "string",
      "description": "PubSub target; use broadcast for a channel-wide message."
    },
    "event": {
      "type": "string",
      "default": "default"
    },
    "user_id": {
      "type": "string",
      "description": "Target Twitch channel ID for channel broadcasts."
    },
    "data": {
      "type": "object",
      "additionalProperties": true
    }
  },
  "required": [
    "data"
  ]
}
```

#### Example

```json
{
  "event": "score-updated",
  "data": {
    "score": 42
  }
}
```

### Responses

#### 200 Response

Message accepted for delivery.

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
  "reason": "role is not authorized"
}
```

!!! info "Generated API reference"
    This endpoint is generated from [`rest-v1.yaml`](https://docs.muxy.io/openapi/rest-v1.yaml).

---
title: Channel Config
description: Patch selected fields in the current channel configuration document.
slug: channel-config-2
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
approved_content_sha256: 6bf10bdcf0194fd2f9c42fed39a8da72a610d888ea80ada9256be4066fb9d28f
---

# Channel Config

## `PATCH /config/channel`

Channel Config

Requires an admin or broadcaster JWT.

### Authorization

Send `Authorization: <Twitch Extension Client ID> <Muxy JWT>`. The JWT role must satisfy the endpoint requirements shown in the examples.

### Request body

Content type: `application/json`

#### Schema

```json
{
  "oneOf": [
    {
      "type": "array",
      "description": "RFC 6902 JSON Patch operations.",
      "items": {
        "type": "object",
        "required": [
          "op",
          "path"
        ],
        "properties": {
          "op": {
            "type": "string",
            "enum": [
              "add",
              "remove",
              "replace",
              "move",
              "copy",
              "test"
            ]
          },
          "path": {
            "type": "string",
            "description": "JSON Pointer to the target value."
          },
          "from": {
            "type": "string",
            "description": "Source JSON Pointer for move or copy."
          },
          "value": {
            "description": "Value used by add, replace, or test."
          }
        }
      }
    },
    {
      "type": "object",
      "description": "JSON Merge Patch object.",
      "additionalProperties": true
    }
  ]
}
```

#### Example

```json
[
  {
    "op": "replace",
    "path": "/favorite_color",
    "value": "blue"
  }
]
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
curl --request PATCH \
  --url https://api.muxy.io/v1/e/config/channel \
  --header 'authorization: <Client ID> <admin or broadcaster JWT>' \
  --header 'content-type: application/json' \
  --data '[{ "op": "add", "path": "/settings/enable_features", "value": true }]'
```

!!! info "Generated API reference"
    This endpoint is generated from [`rest-v1.yaml`](https://docs.muxy.io/openapi/rest-v1.yaml).

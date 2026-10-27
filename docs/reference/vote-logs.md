---
title: Get Vote Logs
description: Get individual vote records for a poll from an admin context.
slug: vote-logs
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
approved_content_sha256: 647af60351402d45f179e8b9561760e7177edcde60c1b1c0de98c353ff9ecfd6
---

# Get Vote Logs

## `GET /vote_logs`

Returns individual vote records. Requires a valid admin JWT.

### Authorization

Send `Authorization: <Twitch Extension Client ID> <Muxy JWT>`. The JWT role must satisfy the endpoint requirements shown in the examples.

### Parameters

| Name | In | Required | Type | Constraints | Description |
| --- | --- | --- | --- | --- | --- |
| `id` | query | no | `string` | default `"default"`; at most 64 characters | Poll identifier. Defaults to `default`; global polls use an ID beginning with `global`. |

### Responses

#### 200 Response

Vote log records.

Content type: `application/json`

##### Schema

```json
{
  "type": "object",
  "required": [
    "result"
  ],
  "properties": {
    "result": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "identifier": {
            "type": "string"
          },
          "opaque": {
            "type": "string"
          },
          "value": {
            "type": "integer"
          },
          "timestamp": {
            "type": "integer"
          }
        }
      }
    }
  }
}
```

##### Example

```json
{
  "result": []
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

#### 500 Error

The service could not complete the operation because an internal or storage dependency failed.

Content type: `application/json`

##### Schema

```json
{
  "type": "object",
  "additionalProperties": true
}
```

##### Example

```json
{
  "reason": ""
}
```

!!! info "Generated API reference"
    This endpoint is generated from [`rest-v1.yaml`](https://docs.muxy.io/openapi/rest-v1.yaml).

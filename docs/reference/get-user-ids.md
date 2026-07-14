---
title: List Shared Twitch User IDs
description: Page through Twitch user IDs shared with an extension.
slug: get-user-ids
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
approved_content_sha256: 630e59cace6cd9f9ad364f022fb543b371a3c524568f5619c7e7a9aa8c211d83
---

# List Shared Twitch User IDs

## `GET /user_ids`

Returns Twitch user IDs that users have shared with the extension. Requires a backend JWT or a validated admin JWT for the extension owner or a listed extension administrator. Continue scanning until `next` is `0`.

### Authorization

Send `Authorization: <Twitch Extension Client ID> <Muxy JWT>`. The JWT role must satisfy the endpoint requirements shown in the examples.

### Parameters

| Name | In | Required | Type | Constraints | Description |
| --- | --- | --- | --- | --- | --- |
| `cursor` | query | no | `string` | default `"0"` | Redis scan cursor returned as `next` by the previous call. Start with `0` and stop when the response returns `0`. |

### Responses

#### 200 Response

One scan page of shared Twitch user IDs.

Content type: `application/json`

##### Schema

```json
{
  "type": "object",
  "required": [
    "next",
    "results"
  ],
  "properties": {
    "next": {
      "type": "string",
      "description": "Cursor for the next scan page; `0` means the scan is complete."
    },
    "results": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "twitch_id"
        ],
        "properties": {
          "twitch_id": {
            "type": "string"
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
  "next": "0",
  "results": [
    {
      "twitch_id": "27419011"
    }
  ]
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

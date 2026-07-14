---
title: Extension Viewer State
description: Read one viewer's extension-wide state or batch-read state for up to
  1,000 Twitch user IDs.
slug: extension-viewer-state
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
approved_content_sha256: ddd98cd7b28da7458bcd833744042c1dc9a53e81d56c161d5210dd48fa39e6ce
---

# Extension Viewer State

## `GET /extension_viewer_state`

Returns extension-wide state for the current viewer. A backend JWT may use `userID` to select one Twitch user. A validated admin JWT may instead pass up to 1,000 comma-separated Twitch IDs in `user_ids`; the response is then keyed by each ID whose state exists.

### Authorization

Send `Authorization: <Twitch Extension Client ID> <Muxy JWT>`. The JWT role must satisfy the endpoint requirements shown in the examples.

### Parameters

| Name | In | Required | Type | Constraints | Description |
| --- | --- | --- | --- | --- | --- |
| `userID` | query | no | `string` | none | Twitch user ID to read when using a backend JWT. Ignored for other roles and superseded when `user_ids` is present. |
| `user_ids` | query | no | `string` | none | Comma-separated Twitch user IDs for an admin-only batch read. At most 1,000 IDs are accepted; missing state entries are omitted from the result. |

### Responses

#### 200 Response

The selected viewer state, or an object keyed by Twitch user ID for a `user_ids` batch request.

Content type: `application/json`

##### Schema

```json
{
  "type": "object",
  "additionalProperties": true,
  "description": "Developer-defined state. Batch responses map each found Twitch user ID to its state object."
}
```

##### Current viewer

```json
{
  "favorite_color": "blue"
}
```

##### Admin batch

```json
{
  "12345": {
    "favorite_color": "blue"
  },
  "67890": {
    "favorite_color": "green"
  }
}
```

#### 400 Error

State lookup failed, or more than 1,000 IDs were supplied.

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
  "reason": "Too many ids specified"
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

### Examples

#### Curl

```curl
curl --request GET \
  --url https://api.muxy.io/v1/e/extension_viewer_state \
  --header 'authorization: <Client ID> <any JWT>' \
  --header 'content-type: application/json'
```

!!! info "Generated API reference"
    This endpoint is generated from [`rest-v1.yaml`](https://docs.muxy.io/openapi/rest-v1.yaml).

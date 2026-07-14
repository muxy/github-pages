---
title: Add a Vote Modifier
description: Add a signed vote adjustment for one user.
slug: vote-modifier
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
approved_content_sha256: 9ac9be62fc8c3a0f773c43e618c418f1d51d75b336f6bfffc1d57c072782f4d8
---

# Add a Vote Modifier

## `POST /vote_modifier`

Adds a signed adjustment for one user. Requires an admin, backend, or broadcaster JWT.

### Authorization

Send `Authorization: <Twitch Extension Client ID> <Muxy JWT>`. The JWT role must satisfy the endpoint requirements shown in the examples.

### Parameters

| Name | In | Required | Type | Constraints | Description |
| --- | --- | --- | --- | --- | --- |
| `id` | query | no | `string` | default `"default"`; at most 64 characters | Poll identifier. Defaults to `default`; global polls use an ID beginning with `global`. |

### Request body

Content type: `application/json`

#### Schema

```json
{
  "type": "object",
  "required": [
    "user",
    "add"
  ],
  "properties": {
    "user": {
      "type": "string"
    },
    "add": {
      "type": "integer"
    }
  }
}
```

#### Example

```json
{
  "user": "U12345",
  "add": 2
}
```

### Responses

#### 200 Response

Operation accepted. The current service returns an empty JSON object.

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

---
title: Get a JSON Store
description: Read a named channel-scoped or extension-wide JSON store.
slug: get-json-store
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
approved_content_sha256: b486cef7f51aaaabe112556e09a1905a00b0178ef9c3bd26036089a67fbc839d
---

# Get a JSON Store

## `GET /json_store`

Returns a named channel-scoped JSON document. The `default` store is used when `id` is omitted; IDs beginning with `global` use extension-wide storage. A cache miss can return `202` while a registered external data source is being refreshed.

### Authorization

Send `Authorization: <Twitch Extension Client ID> <Muxy JWT>`. The JWT role must satisfy the endpoint requirements shown in the examples.

### Parameters

| Name | In | Required | Type | Constraints | Description |
| --- | --- | --- | --- | --- | --- |
| `id` | query | no | `string` | default `"default"` | Store identifier. Defaults to `default`; IDs beginning with `global` use extension-wide storage. |

### Responses

#### 200 Response

The stored JSON document.

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
  "favorite_color": "blue"
}
```

#### 202 Response

The document is not cached and a registered source is being refreshed, or another request already holds the refresh lock.

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

#### 404 Error

No cached document or registered source exists for this store identifier.

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
  "reason": "Not Found"
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

#### 502 Error

The registered external source returned a response that was not a JSON object.

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
  "reason": "external server returned a bad response"
}
```

!!! info "Generated API reference"
    This endpoint is generated from [`rest-v1.yaml`](https://docs.muxy.io/openapi/rest-v1.yaml).

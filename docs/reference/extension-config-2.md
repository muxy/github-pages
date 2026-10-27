---
title: Extension Config
description: Replace the extension-wide configuration document.
slug: extension-config-2
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
approved_content_sha256: 5ce8dadd66c75d6bc6f94d0a3bdb5ae1a15f4a8b8c7a495931dac1b714eabca8
---

# Extension Config

## `POST /config/extension`

Extension Config

Requires an admin JWT; backend JWTs are rejected.

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
  "release_date": "2021-10-31"
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
curl --request POST \
  --url https://sandbox.api.muxy.io/v1/e/config/extension \
  --header 'authorization: <Client ID> <admin JWT>' \
  --header 'content-type: application/json' \
  --data '{ "release_date": "2021-10-31" }'
```

#### Javascript

```javascript
const medkit = new Muxy.SDK();
await medkit.loaded();

const state = medkit.setExtensionConfig({
  "release_date": "2021-10-31"
});
```

!!! info "Generated API reference"
    This endpoint is generated from [`rest-v1.yaml`](https://docs.muxy.io/openapi/rest-v1.yaml).

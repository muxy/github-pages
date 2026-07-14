---
title: Create a GameLink Authorization Code
description: Create a short-lived GameLink PIN for the current extension authorization.
slug: post-gamelink-token
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
approved_content_sha256: 022565deb0304d297ece9edc78a780637dd96d0bf4c297e7445d83dfbc814132
---

# Create a GameLink Authorization Code

## `POST /gamelink/token`

Creates a six-character authorization code for the current JWT. The code expires after five minutes and can be exchanged by a GameLink client during PIN authentication.

### Authorization

Send `Authorization: <Twitch Extension Client ID> <Muxy JWT>`. The JWT role must satisfy the endpoint requirements shown in the examples.

### Responses

#### 200 Response

A short-lived GameLink authorization code.

Content type: `application/json`

##### Schema

```json
{
  "type": "object",
  "required": [
    "token"
  ],
  "properties": {
    "token": {
      "type": "string",
      "minLength": 6,
      "maxLength": 6,
      "pattern": "^[A-HJ-KM-NP-Z2-46-9]{6}$",
      "description": "Six-character code using an ambiguity-reduced uppercase alphabet; expires after five minutes."
    }
  }
}
```

##### Example

```json
{
  "token": "ABC234"
}
```

#### 400 Error

The serialized authorization header exceeds 1,024 characters.

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
  "reason": "Bad request"
}
```

!!! info "Generated API reference"
    This endpoint is generated from [`rest-v1.yaml`](https://docs.muxy.io/openapi/rest-v1.yaml).

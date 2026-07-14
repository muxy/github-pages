---
title: Create or Update Poll Configuration
description: Configure poll limits, schedule, prompt, and options.
slug: vote-config-post
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
approved_content_sha256: e14e11c42a1adfcb06d64e60f3a571c6c8e2ed5ed472cae7dc9e769a4679db77
---

# Create or Update Poll Configuration

## `POST /vote_config`

Creates or replaces poll configuration. Requires an admin, backend, or broadcaster JWT.

### Authorization

Send `Authorization: <Twitch Extension Client ID> <Muxy JWT>`. The JWT role must satisfy the endpoint requirements shown in the examples.

### Request body

Content type: `application/json`

#### Schema

```json
{
  "type": "object",
  "required": [
    "id",
    "config"
  ],
  "properties": {
    "id": {
      "type": "string",
      "maxLength": 64
    },
    "config": {
      "type": "object",
      "properties": {
        "userIDVoting": {
          "type": "boolean"
        },
        "distinctOptionsPerUser": {
          "type": "integer",
          "minimum": 1,
          "maximum": 258,
          "default": 1
        },
        "totalVotesPerUser": {
          "type": "integer",
          "minimum": 1,
          "maximum": 1024,
          "default": 1
        },
        "votesPerOption": {
          "type": "integer",
          "minimum": 1,
          "maximum": 1024,
          "default": 1
        },
        "global": {
          "type": "boolean"
        },
        "disabled": {
          "type": "boolean"
        },
        "prompt": {
          "type": "string"
        },
        "options": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "userData": {},
        "endsAt": {
          "type": "integer",
          "description": "Unix timestamp in seconds."
        },
        "startsAt": {
          "type": "integer",
          "description": "Unix timestamp in seconds."
        },
        "status": {
          "type": "string",
          "enum": [
            "pending",
            "active",
            "expired"
          ],
          "readOnly": true
        }
      }
    }
  }
}
```

#### Example

```json
{
  "id": "next-game",
  "config": {
    "prompt": "Choose the next game",
    "options": [
      "A",
      "B"
    ],
    "startsAt": 1760000000,
    "endsAt": 1760003600
  }
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

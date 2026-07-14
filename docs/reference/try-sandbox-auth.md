---
title: Authorization for Testing
description: Create one or more sandbox JWTs for simulated users.
slug: try-sandbox-auth
product: REST API
audience: developers
status: current
owner: API Platform
source_of_truth: muxy/github-pages:openapi/sandbox-v1.yaml
version: v1
last_verified: '2026-07-14'
review_state: approved
page_type: protocol-reference
approved_by: peter-bonanni
approved_at: '2026-07-14T20:34:54Z'
approval_method: user-authorized-codex-assisted-source-review
approved_content_sha256: 801fc4017383d74c9084e911f4db3044d8395e895eb7316b766139d6901832da
---

# Authorization for Testing

## `POST /authtoken`

Returns one or more JSON Web Tokens (JWT) for use in the sandbox environment.

`user_id` and `user_ids` are both optional and may be combined. With neither, the server creates one anonymous token. A token whose role string is `admin` is not guaranteed to satisfy handlers that require a validated admin JWT.

### Authorization

No authorization header is required for this sandbox operation.

### Request body

Content type: `application/json`

#### Schema

```json
{
  "type": "object",
  "properties": {
    "extension_id": {
      "type": "string",
      "description": "The Client ID for the extension. A Twitch Extension Client ID that has been registered with Muxy. See [Quick Start](https://docs.muxy.io/docs/quick-start) for details."
    },
    "channel_id": {
      "type": "string",
      "description": "The Twitch Channel ID to simulate"
    },
    "user_id": {
      "type": "string",
      "description": "Optional Twitch user ID. For broadcaster tokens the server replaces this value with `channel_id`."
    },
    "role": {
      "type": "string",
      "description": "Role string copied into the testing JWT. The endpoint does not validate an enum. Use `viewer`, `broadcaster`, `admin`, or `backend` only when the target handler supports it."
    },
    "user_ids": {
      "type": "array",
      "description": "Optional additional Twitch user IDs. May be supplied with `user_id`; one JWT is returned per ID.",
      "items": {
        "type": "string"
      }
    },
    "app_id": {
      "type": "string",
      "description": "Registered Muxy app ID. The server resolves its owning extension when available."
    }
  },
  "anyOf": [
    {
      "required": [
        "extension_id"
      ]
    },
    {
      "required": [
        "app_id"
      ]
    }
  ]
}
```

#### Viewer token

```json
{
  "extension_id": "your-extension-client-id",
  "channel_id": "12345678",
  "user_id": "87654321",
  "role": "viewer"
}
```

#### Anonymous token

```json
{
  "extension_id": "your-extension-client-id",
  "channel_id": "12345678",
  "role": "viewer"
}
```

### Responses

#### 200 Response

200

Content type: `application/json`

##### Schema

```json
{
  "oneOf": [
    {
      "type": "object",
      "required": [
        "token"
      ],
      "properties": {
        "token": {
          "type": "string"
        }
      }
    },
    {
      "type": "object",
      "required": [
        "tokens"
      ],
      "properties": {
        "tokens": {
          "type": "array",
          "items": {
            "type": "string"
          }
        }
      }
    }
  ]
}
```

##### Single user

```json
{
  "token": "<sandbox JWT>"
}
```

##### Multiple users

```json
{
  "tokens": [
    "<sandbox JWT>",
    "<sandbox JWT>"
  ]
}
```

#### 400 Error

400

Content type: `application/json`

##### Schema

```json
{
  "type": "object",
  "required": [
    "reason"
  ],
  "properties": {
    "reason": {
      "type": "string"
    }
  }
}
```

##### Unknown extension

```json
{
  "reason": "No such extension found"
}
```

### Examples

#### Curl

```curl
curl --request POST \
  --url https://sandbox.api.muxy.io/v1/e/authtoken \
  --header 'content-type: application/json' \
  --data '{"extension_id":"your-extension-client-id","channel_id":"12345678","user_id":"87654321","role":"viewer"}'
```

!!! info "Generated API reference"
    This endpoint is generated from [`sandbox-v1.yaml`](https://docs.muxy.io/openapi/sandbox-v1.yaml).

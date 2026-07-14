---
title: Config API
description: Navigate the extension-wide and channel-specific configuration operations
  in the Muxy REST API.
slug: config-api
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
approved_content_sha256: 90b946e298508f148707ea7ad3bf4acc0cba1b33e8a9e8f6d639f84f559c4768
---

# Config API

Configuration routes expose developer-defined JSON at two scopes: `extension` for extension-wide configuration and `channel` for the current channel context. `GET /config` returns both scopes together.

All paths below are relative to `https://api.muxy.io/v1/e` and require the standard [`Authorization` header](medkit-rest-api.md#authorization).

| Method and path | Generated operation reference |
| --- | --- |
| `GET /config` | [Get all config](extension-config.md) |
| `GET /config/channel` | [Get channel config](channel-config.md) |
| `POST /config/channel` | [Post channel config](channel-config-1.md) |
| `PATCH /config/channel` | [Patch channel config](channel-config-2.md) |
| `GET /config/extension` | [Get extension config](extension-config-1.md) |
| `POST /config/extension` | [Post extension config](extension-config-2.md) |
| `PATCH /config/extension` | [Patch extension config](extension-config-3.md) |

## Write bodies

The v1 OpenAPI contract declares both `POST` and `PATCH` bodies as JSON arrays of RFC 6902 operations. See [JSON request bodies](medkit-rest-api.md#json-request-bodies) for the shared format and use the generated operation page for method-specific details.

## Canonical OpenAPI

See the [raw `rest-v1.yaml` specification](https://docs.muxy.io/openapi/rest-v1.yaml). Sandbox token creation is defined separately in [raw `sandbox-v1.yaml`](https://docs.muxy.io/openapi/sandbox-v1.yaml).

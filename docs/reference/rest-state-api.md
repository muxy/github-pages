---
title: State API
description: Navigate the extension, channel, and viewer state operations in the Muxy
  REST API.
slug: rest-state-api
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
approved_content_sha256: 1cf3a90d04dc27be550a02108a941cb8a7fb865734b34cab3b04efb4b1b04df6
---

# State API

State routes expose developer-defined JSON at extension, channel, viewer, and extension-viewer scopes. `GET /all_state` returns the available scopes together.

All paths below are relative to `https://api.muxy.io/v1/e` and require the standard [`Authorization` header](medkit-rest-api.md#authorization).

| Scope | Method and path | Generated operation reference |
| --- | --- | --- |
| All | `GET /all_state` | [Get all state](viewer-state.md) |
| Channel | `GET /channel_state` | [Get channel state](channel-state.md) |
| Channel | `POST /channel_state` | [Post channel state](channel-state-1.md) |
| Channel | `PATCH /channel_state` | [Patch channel state](channel-state-2.md) |
| Extension | `GET /extension_state` | [Get extension state](viewer-state-4.md) |
| Extension | `POST /extension_state` | [Post extension state](extension-state.md) |
| Extension | `PATCH /extension_state` | [Patch extension state](extension-state-1.md) |
| Extension viewer | `GET /extension_viewer_state` | [Get extension-viewer state](extension-viewer-state.md) |
| Extension viewer | `POST /extension_viewer_state` | [Post extension-viewer state](extension-viewer-state-1.md) |
| Extension viewer | `PATCH /extension_viewer_state` | [Patch extension-viewer state](extension-viewer-state-2.md) |
| Viewer | `GET /viewer_state` | [Get viewer state](viewer-state-2.md) |
| Viewer | `POST /viewer_state` | [Post viewer state](viewer-state-1.md) |
| Viewer | `PATCH /viewer_state` | [Patch viewer state](viewer-state-3.md) |

## Write bodies

The v1 OpenAPI contract declares every state `POST` and `PATCH` body as a JSON array of RFC 6902 operations. See [JSON request bodies](medkit-rest-api.md#json-request-bodies) for the shared format and use the generated operation page for method-specific details.

## Canonical OpenAPI

See the [raw `rest-v1.yaml` specification](https://docs.muxy.io/openapi/rest-v1.yaml). Sandbox token creation is defined separately in [raw `sandbox-v1.yaml`](https://docs.muxy.io/openapi/sandbox-v1.yaml).

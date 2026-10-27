---
title: Using the MEDKit REST API
description: Base URLs, authorization, request conventions, and route groups for the
  Muxy REST API.
slug: medkit-rest-api
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
approved_content_sha256: 709610af1c93853d304d140a0dd369ab59b1bf767217c63e85b67f5765683d0d
---

# Using the MEDKit REST API

Use this page to choose a route group, then follow the linked generated operation page for the request and response schema.

## Base URLs

| Environment | Base URL | Contract scope |
| --- | --- | --- |
| Production | `https://api.muxy.io/v1/e` | All operations in `rest-v1.yaml` |
| Sandbox | `https://sandbox.api.muxy.io/v1/e` | Development host; `sandbox-v1.yaml` documents the sandbox-only token operation |

Production and sandbox are separate environments. Use the same REST route path on the sandbox host when testing, but use a sandbox JWT. The sandbox contract does not duplicate the production route catalog: it contains only [`POST /authtoken`](try-sandbox-auth.md). See [Developing in the Sandbox](dev-auth.md) for sandbox behavior.

## Authorization

Every operation in `rest-v1.yaml` requires this header:

```text
Authorization: <Twitch Extension Client ID> <Muxy JWT>
```

The client ID and JWT are separated by one space; this is not a `Bearer` scheme. The only documented exception is sandbox [`POST /authtoken`](try-sandbox-auth.md), which does not require authorization and returns sandbox-only JWTs.

## JSON request bodies

Send JSON bodies with `Content-Type: application/json`. In the canonical v1 contract, state and configuration `POST` and `PATCH` operations declare an array of [RFC 6902 JSON Patch operations](https://www.rfc-editor.org/rfc/rfc6902), not a bare object:

```json
[
  { "op": "add", "path": "/settings/enabled", "value": true }
]
```

Each `path` is a JSON Pointer. Follow the generated operation page for the exact method-specific contract; do not infer a replacement-object body from legacy prose or examples.

## Route groups

| Group | Paths | Navigation |
| --- | --- | --- |
| Configuration | `/config`, `/config/channel`, `/config/extension` | [Config API](config-api.md) |
| State | `/all_state`, `/channel_state`, `/extension_state`, `/extension_viewer_state`, `/viewer_state` | [State API](rest-state-api.md) |
| Aggregation | `/accumulate`, `/rank` | [Aggregation API](aggregation-api.md) |
| Communication | `/broadcast`, `/extension_broadcast`, `/whisper_self` | [Communication API](communication-api.md) |
| Sandbox authorization | `/authtoken` | [Authorization for Testing](try-sandbox-auth.md) |

## Canonical OpenAPI

- [Raw production REST specification (`rest-v1.yaml`)](https://docs.muxy.io/openapi/rest-v1.yaml)
- [Raw sandbox specification (`sandbox-v1.yaml`)](https://docs.muxy.io/openapi/sandbox-v1.yaml)

---
title: Communication API
description: Navigate the channel, extension-wide, and current-viewer messaging operations
  in the Muxy REST API.
slug: communication-api
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
approved_content_sha256: 85225ead4aeedc35c65d5e8b816c36b157127205a1310adab894aa29bc5ff128
---

# Communication API

The canonical v1 REST contract exposes three `POST` operations for publishing messages to a channel, across an extension, or to the viewer represented by the JWT.

All paths below are relative to `https://api.muxy.io/v1/e` and require the standard [`Authorization` header](medkit-rest-api.md#authorization).

| Target | Method and path | Generated operation reference |
| --- | --- | --- |
| Channel | `POST /broadcast` | [Send a channel broadcast](broadcast-channel.md) |
| Extension-wide | `POST /extension_broadcast` | [Send an extension-wide broadcast](broadcast-extension.md) |
| Current viewer | `POST /whisper_self` | [Send a message to the current viewer](whisper-self.md) |

See [Broadcast Messaging](broadcast.md) for delivery guidance. Payload fields, authorization outcomes, and response schemas remain canonical in the generated operation pages and OpenAPI; they are not duplicated here.

## Canonical OpenAPI

See the [raw `rest-v1.yaml` specification](https://docs.muxy.io/openapi/rest-v1.yaml). Sandbox token creation is defined separately in [raw `sandbox-v1.yaml`](https://docs.muxy.io/openapi/sandbox-v1.yaml).

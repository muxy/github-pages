---
title: Simulate Users While Testing
description: Obtain sandbox JWTs for viewer, broadcaster, and admin test sessions.
slug: simulate-users-while-testing
product: MEDKit
audience: Twitch Extension developers
status: current
owner: Developer Experience
source_of_truth: muxy/github-pages:openapi/rest-v1.yaml
version: 2.4.18
last_verified: '2026-07-14'
review_state: approved
page_type: task-guide
approved_by: peter-bonanni
approved_at: '2026-07-14T20:34:54Z'
approval_method: user-authorized-codex-assisted-source-review
approved_content_sha256: 356d9ade1877fbf782ca46e79dff9086914c8920b8c27313f0c9901153dc99b6
---

# Simulate Users While Testing

Use the Muxy sandbox to create deterministic viewer, broadcaster, or admin JWTs without using production credentials.

## Request one viewer token

Your Twitch Extension Client ID must already be registered with Muxy.

```bash
curl --request POST \
  --url https://sandbox.api.muxy.io/v1/e/authtoken \
  --header 'content-type: application/json' \
  --data '{
    "extension_id": "your-extension-client-id",
    "channel_id": "12345678",
    "user_id": "87654321",
    "role": "viewer"
  }'
```

The response contains one token:

```json
{
  "token": "<sandbox JWT>"
}
```

For a broadcaster session, set `role` to `broadcaster` and make `user_id` equal `channel_id`. For administrator-only operations, use `admin` only in a controlled test environment.

## Request several viewers

Use `user_ids` instead of `user_id`:

```json
{
  "extension_id": "your-extension-client-id",
  "channel_id": "12345678",
  "user_ids": ["1001", "1002", "1003"],
  "role": "viewer"
}
```

The response uses the plural `tokens` field in the same order as `user_ids`.

## Use a token with REST

```bash
curl --request GET \
  --url https://sandbox.api.muxy.io/v1/e/config \
  --header "Authorization: ${MUXY_CLIENT_ID} ${MUXY_SANDBOX_JWT}"
```

Sandbox JWTs are valid only against `sandbox.api.muxy.io`; never send them to production.

See the generated [sandbox authorization reference](../reference/try-sandbox-auth.md) for the complete request and response schema.

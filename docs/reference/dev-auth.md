---
title: Developing in the Sandbox
description: Muxy provides an off-Twitch environment for development and testing.
slug: dev-auth
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
approved_content_sha256: 787b1a5da01b08c1ac8718b2756446a35ba4ebc3e28690a466e69ba99e13a95d
---

# Developing in the Sandbox

The sandbox lets a local client obtain test Muxy JWTs without running inside Twitch. Sandbox credentials and data are separate from production.

| Environment | REST base URL | Credential source |
| --- | --- | --- |
| Sandbox | `https://sandbox.api.muxy.io/v1/e` | Sandbox-only `POST /authtoken` |
| Production | `https://api.muxy.io/v1/e` | Twitch Extension or trusted-backend flow |

`sandboxy.muxy.io` is not a valid host. A sandbox JWT must not be sent to the production API, and a production credential must not be copied into a local test fixture.

## Obtain one test token

`POST /authtoken` requires no authorization header, but the Twitch Extension Client ID must already be registered with Muxy.

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

A single requested identity returns:

```json
{
  "token": "<sandbox JWT>"
}
```

Use it on sandbox API calls only:

```text
Authorization: your-extension-client-id <sandbox JWT>
```

## Simulate roles and identities

| Field | Meaning |
| --- | --- |
| `extension_id` | Registered Twitch Extension Client ID. Supply this or `app_id`. |
| `app_id` | Registered Muxy app ID; the service resolves its owning extension when available. |
| `channel_id` | Twitch channel to simulate. |
| `user_id` | Optional Twitch user ID. For broadcaster tokens, the service replaces it with `channel_id`. |
| `user_ids` | Optional list of additional Twitch user IDs. The response contains one token per ID. |
| `role` | Role string copied into the test JWT. Use only a role supported by the endpoint under test. |

`user_id` and `user_ids` may be combined. With multiple identities, the response uses `tokens`:

```json
{
  "tokens": [
    "<sandbox JWT>",
    "<sandbox JWT>"
  ]
}
```

The generator copies the role string; it does not prove that a handler will accept that role. In particular, a token whose role says `admin` is not guaranteed to satisfy an endpoint that requires a separately validated admin credential.

## Use MEDKit local simulation

MEDKit 2.4.18 can request sandbox authorization for a simulated user. Configure it before `Muxy.setup()`:

```javascript
const debugging = new Muxy.DebuggingOptions()
  .channelID("12345678")
  .userID("87654321")
  .role("viewer");

Muxy.debug(debugging);
Muxy.setup({ clientID: "your-extension-client-id" });

const medkit = new Muxy.SDK();
await medkit.loaded();
```

Remove `Muxy.debug(...)` from production bundles so Twitch supplies the real authorization context.

## Understand viewer identity

- A shared Twitch User ID is a decimal string such as `27419011`.
- A logged-in viewer who has not shared identity receives an opaque ID beginning with `U`.
- A logged-out viewer receives an opaque ID beginning with `A`.

MEDKit exposes the current values as `medkit.user.twitchID` and `medkit.user.twitchOpaqueID`. Opaque IDs are extension-scoped and must not be used to identify a Twitch account. See [Twitch Extension identity](https://dev.twitch.tv/docs/extensions#identity).

## Security and operational boundaries

- Treat test JWTs as credentials: keep them out of source control, screenshots, logs, and support messages.
- Use synthetic users and non-sensitive payloads. Sandbox data is not durable product storage.
- The sandbox token endpoint does not issue a Twitch Helix Extension token. Use MEDKit's separate debug Helix flow when testing supported Twitch API calls.
- Legacy documentation said sandbox data is regularly wiped and transactions are always approved. Those are deployment behaviors, not guarantees in the pinned OpenAPI contract; verify them with the platform owner before a test depends on them.

For the generated request schema and all response variants, see [`POST /authtoken`](try-sandbox-auth.md).

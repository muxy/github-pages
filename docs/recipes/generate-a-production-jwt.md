---
title: Generate a Production JWT
description: Create a short-lived backend JWT for direct calls to the Muxy REST API.
slug: generate-a-production-jwt
product: REST API
audience: backend developers
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
approved_content_sha256: c32dcffa67ccea8c4d3377580acb8850ec501f412fc8aa2bdcd92330d81cb9a2
---

# Generate a Production JWT

Use this server-side flow when a trusted backend needs to call the Muxy REST API. Never put the extension authentication secret in a browser, Twitch Extension iframe, game client, or source repository.

## Prerequisites

- Your Twitch Extension Client ID
- The Muxy authentication secret associated with that extension
- Node.js 18 or newer

The authentication secret is Base64 encoded. Decode it before using it as the HS256 signing key.

## Create an exchange token

Install [`jose`](https://www.npmjs.com/package/jose) in your backend project:

```bash
npm install jose
```

Create a short-lived exchange token with the extension identifier, target channel, user, and role:

```javascript title="create-muxy-token.mjs"
import { SignJWT } from "jose";

const clientID = process.env.MUXY_CLIENT_ID;
const authSecret = process.env.MUXY_AUTH_SECRET;
const channelID = process.env.TWITCH_CHANNEL_ID;

if (!clientID || !authSecret || !channelID) {
  throw new Error("MUXY_CLIENT_ID, MUXY_AUTH_SECRET, and TWITCH_CHANNEL_ID are required");
}

const signingKey = Uint8Array.from(Buffer.from(authSecret, "base64"));
const exchangeToken = await new SignJWT({
  identifier: clientID,
  channel_id: channelID,
  user_id: channelID,
  role: "backend",
})
  .setProtectedHeader({ alg: "HS256", typ: "JWT" })
  .setIssuedAt()
  .setExpirationTime("5m")
  .sign(signingKey);

const response = await fetch("https://api.muxy.io/v1/e/token", {
  method: "POST",
  headers: { "content-type": "text/plain" },
  body: exchangeToken,
});

if (!response.ok) {
  throw new Error(`Muxy token exchange failed: ${response.status} ${await response.text()}`);
}

const { token } = await response.json();
console.log(token);
```

The returned Muxy JWT expires after 30 minutes. Cache it only on the server and refresh it before expiry.

## Call the REST API

Send the extension Client ID and returned JWT together in the `Authorization` header:

```bash
curl --request GET \
  --url https://api.muxy.io/v1/e/config \
  --header "Authorization: ${MUXY_CLIENT_ID} ${MUXY_JWT}"
```

Use `viewer`, `broadcaster`, or `moderator` instead of `backend` only when the requested endpoint and user context require that role.

## Verify the failure path

Before shipping, verify that the backend rejects missing secrets, does not log either JWT, refreshes expired tokens, and handles non-2xx responses without retrying indefinitely.

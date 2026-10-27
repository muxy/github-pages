---
title: Call the Twitch API from an Extension
description: Call supported Twitch Helix endpoints with the current viewer's Extension
  Helix token.
slug: call-into-the-twitch-api
product: MEDKit
audience: developers
status: current
owner: Developer Experience
source_of_truth: muxy/extensions-js
version: 2.4.18
last_verified: '2026-07-14'
review_state: approved
page_type: task-guide
approved_by: peter-bonanni
approved_at: '2026-07-14T20:34:54Z'
approval_method: user-authorized-codex-assisted-source-review
approved_content_sha256: 064448edf166ecfd45b19592c7c94122553b4644f5c3eee6e7005bdf13dca6b1
---

# Call the Twitch API from an Extension

Twitch supplies an Extension Helix token in the authorization callback. MEDKit exposes it as `medkit.user.helixToken` after `medkit.loaded()` resolves.

Extension Helix tokens work only with endpoints that accept a user access token and require no scopes. See Twitch's [Extension front-end API guide](https://dev.twitch.tv/docs/extensions/frontend-api-usage/) before choosing an endpoint.

## Look up a user

```javascript
import Muxy from "@muxy/extensions-js";
const clientID = import.meta.env.VITE_MUXY_CLIENT_ID;
Muxy.setup({ clientID });

const medkit = new Muxy.SDK();
await medkit.loaded();

const query = new URLSearchParams({ login: "twitch" });
const response = await fetch(`https://api.twitch.tv/helix/users?${query}`, {
  headers: {
    Authorization: `Extension ${medkit.user.helixToken}`,
    "Client-Id": clientID,
  },
});

if (!response.ok) {
  throw new Error(`Twitch API request failed: ${response.status}`);
}

const { data: users } = await response.json();
console.log(users[0]);
```

Do not send `medkit.user.twitchJWT` to Helix; it authenticates extension backend requests, not Twitch front-end API requests.

## 2.4.18 helper limitation

!!! warning "Avoid the user lookup convenience methods"
    Although 2.4.18 declares `TwitchClient.getTwitchUsers()` and `getTwitchUsersByID()`, the published implementation forwards their token argument as request data instead of as the Helix authorization argument. Use `fetch()` as shown above for this release.

For local development, obtain a test Helix token with the [user simulation flow](set-up-user-simulation.md#test-a-helix-request). Never commit or log either token.

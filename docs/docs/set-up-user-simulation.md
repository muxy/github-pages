---
title: Set Up MEDKit User Simulation
description: Simulate channel, user, role, and Helix authorization while testing MEDKit
  locally.
slug: set-up-user-simulation
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
approved_content_sha256: ac7ca53ff78d665ab03a8c003f6d0e3f9156685171923c4e31b06098cbba27b3
---

# Set Up MEDKit User Simulation

`Muxy.DebuggingOptions` supplies local channel, user, and role context before MEDKit starts. Use it only in a local or sandbox build; a call to `Muxy.debug()` is not automatically removed or ignored in production.

## Simulate a viewer

```javascript
import Muxy from "@muxy/extensions-js";
const debugging = new Muxy.DebuggingOptions()
  .channelID("5678")
  .userID("1234")
  .role("viewer");

Muxy.debug(debugging);
Muxy.setup({ clientID: import.meta.env.VITE_MUXY_CLIENT_ID });

const medkit = new Muxy.SDK();
await medkit.loaded();

console.log(medkit.user.channelID, medkit.user.role);
```

Call `Muxy.debug()` before `Muxy.setup()`. Common sandbox roles are `viewer`, `broadcaster`, and `admin`. For broadcaster tests, make `userID` equal the channel owner's Twitch ID when the endpoint requires that identity.

## Debug option reference

| Setter | Purpose |
| --- | --- |
| `channelID(value)` | Simulated Twitch channel ID |
| `userID(value)` | Simulated current Twitch user ID |
| `role(value)` | Simulated role |
| `jwt(value)` | Use an already issued JWT instead of sandbox test auth |
| `environment(value)` | Override MEDKit environment selection |
| `url(value)` | Override the backend base URL |
| `onPubsubListen(callback)` | Observe local subscription setup |
| `onPubsubReceive(callback)` | Observe received messages |
| `onPubsubSend(callback)` | Observe sent messages |

Treat `jwt()`, `environment()`, and `url()` as advanced diagnostics. Never mint a JWT in browser code or expose an extension secret to make local testing easier.

## Test a Helix request

The sandbox authorization response does not provide a Twitch Extension Helix token. In a user-initiated click handler, call `beginDebugHelixTokenFlow()` to open the package's test OAuth flow:

```javascript
const button = document.querySelector("#authorize-helix");
button.addEventListener("click", async () => {
  await medkit.loaded();
  medkit.beginDebugHelixTokenFlow();
});
```

Complete the flow in the opened window, then reload the test page. The 2.4.18 package restores the testing token from local storage and exposes it as `medkit.user.helixToken`.

Clear the local testing token when finished:

```javascript
window.ClearHelixToken?.();
```

Continue with [Call the Twitch API from an Extension](call-into-the-twitch-api.md). Twitch documents the token's endpoint restrictions in its [Extension front-end API guide](https://dev.twitch.tv/docs/extensions/frontend-api-usage/).

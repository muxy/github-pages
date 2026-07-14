---
title: Create the MEDKit Control Object
description: Initialize MEDKit and wait until Twitch authorization is available.
slug: create-the-medkit-control-object
product: MEDKit
audience: Twitch Extension developers
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
approved_content_sha256: 06d6386c0e70f1d592e2fafa03c3e0793160761277d915da33e01dad30485334
---

# Create the MEDKit Control Object

Create one MEDKit SDK instance after configuring your Twitch Extension Client ID. Reuse that instance for state, configuration, PubSub, and signed REST requests.

## Load MEDKit

Install the supported package in your extension project:

```bash
npm install @muxy/extensions-js@2.4.18
```

Import the browser bundle through your build system:

```javascript
import Muxy from "@muxy/extensions-js";
```

## Initialize the SDK

```javascript title="muxy.js"
import Muxy from "@muxy/extensions-js";

Muxy.setup({
  clientID: import.meta.env.VITE_MUXY_CLIENT_ID,
});

export const medkit = new Muxy.SDK();

export async function initializeMuxy() {
  await medkit.loaded();
  return medkit;
}
```

Call `initializeMuxy()` once during application startup. `loaded()` resolves after Twitch authorization and the initial Muxy state/configuration payload are available.

## Read initial data

```javascript
const sdk = await initializeMuxy();
const config = sdk.getConfig();
const state = sdk.getState();

console.log({ config, state });
```

Do not create a new SDK object for every component or request. Pass the shared instance through your application state or dependency-injection layer.

## Next steps

- [Simulate users while testing](simulate-users-while-testing.md)
- [Read and update state](../docs/state-information.md)
- [Store configuration data](../docs/store-configuration-data.md)

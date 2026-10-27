---
title: MEDKit Quick Start
description: Register a Twitch Extension, install MEDKit 2.4.18, and initialize a
  browser page.
slug: quick-start
product: MEDKit
audience: developers
status: current
owner: Developer Experience
source_of_truth: muxy/extensions-js
version: 2.4.18
last_verified: '2026-07-14'
review_state: approved
page_type: quickstart
approved_by: peter-bonanni
approved_at: '2026-07-14T20:34:54Z'
approval_method: user-authorized-codex-assisted-source-review
approved_content_sha256: 6d55aa21545ec3c9270d8fe20c17350deb6152ea77f2180d4543433f808d18ee
---

# MEDKit Quick Start

MEDKit is the `@muxy/extensions-js` browser SDK for custom Twitch Extension pages. This quick start pins the [published 2.4.18 registry record](https://registry.npmjs.org/@muxy%2fextensions-js/2.4.18) instead of relying on an unversioned CDN or an old starter toolchain.

Allow about 10 minutes if your Twitch Extension is already registered with Muxy. At the end, a local page will obtain sandbox authorization and print the current channel state.

## Before you start

You need:

- a Twitch Extension created in the [Twitch developer console](https://dev.twitch.tv/console/extensions);
- its Extension Client ID;
- the extension registered in the [Muxy developer portal](https://dev.muxy.io/landing); and
- a browser project that supports ES modules;
- a test Twitch channel ID and user ID; and
- Node.js 18 or newer.

The Client ID is public configuration. Keep the Twitch Extension secret and every Muxy authentication secret on a trusted backend.

## Install the verified release

```bash
npm create vite@latest muxy-medkit-quickstart -- --template vanilla
cd muxy-medkit-quickstart
npm install
npm install @muxy/extensions-js@2.4.18
```

The published package contains UMD and ES-module bundles plus TypeScript declarations. There is no public Git tag named `2.4.18`, so release-specific API checks must use the 2.4.18 package tarball and its declarations rather than the repository's default branch.

## Configure the local page

Create `.env.local`:

```dotenv
VITE_MUXY_CLIENT_ID=your-extension-client-id
VITE_TWITCH_CHANNEL_ID=12345678
VITE_TWITCH_USER_ID=87654321
```

These values are public test context, not secrets. Never place a Twitch Extension secret, Muxy signing secret, or long-lived token in a `VITE_` variable.

Replace `src/main.js`:

```javascript
import Muxy from "@muxy/extensions-js";

const clientID = import.meta.env.VITE_MUXY_CLIENT_ID;
const channelID = import.meta.env.VITE_TWITCH_CHANNEL_ID;
const userID = import.meta.env.VITE_TWITCH_USER_ID;

if (!clientID || !channelID || !userID) {
  throw new Error("Set all three VITE_ variables in .env.local");
}

const debugging = new Muxy.DebuggingOptions()
  .channelID(channelID)
  .userID(userID)
  .role("viewer");

Muxy.debug(debugging);
Muxy.setup({ clientID });
const medkit = new Muxy.SDK();

try {
  await medkit.loaded();
  const state = await medkit.getChannelState();
  document.querySelector("#app").textContent = JSON.stringify(state, null, 2);
} catch (error) {
  document.querySelector("#app").textContent = "MEDKit did not initialize.";
  console.error("MEDKit failed to initialize", error);
}
```

Call `Muxy.setup()` exactly once per page and wait for `medkit.loaded()` before reading authorization, state, configuration, or user information.

## Run and verify

Start Vite:

```bash
npm run dev
```

Open the local URL it prints. A successful run has all three signals:

1. the page replaces Vite's starter content with a JSON object;
2. the browser console has no MEDKit initialization error; and
3. the Network panel shows sandbox authorization and a channel-state request to `sandbox.api.muxy.io`.

The state may be `{}` on a new test channel; that is a valid result.

## If verification fails

If the page remains on the error message or authorization returns `400`, confirm the Client ID is registered with Muxy and that all three `.env.local` values are present, then stop and restart Vite so it reloads the environment file. If the request returns `401` or `403`, verify that the request is going to the sandbox host and that the simulated role is allowed to perform the operation.

Do not copy a production JWT into the example. Continue with [MEDKit troubleshooting](troubleshooting-tips.md) if initialization still fails.

Before uploading a production Twitch Extension bundle, remove the `Muxy.debug(...)` call. Twitch supplies the real channel, user, and role context in production.

## Continue by goal

| Goal | Guide |
| --- | --- |
| Build a complete local Vite example | [Install MEDKit manually](install-manually.md) |
| Understand the initialization lifecycle | [Get started with MEDKit](getting-started-with-medkit.md) |
| Simulate users in the sandbox | [Set up user simulation](set-up-user-simulation.md) |
| Choose persistent storage | [Choose a MEDKit data store](data-tracking.md) |
| Call Twitch Helix | [Call the Twitch API](call-into-the-twitch-api.md) |
| Collect viewer input | [Aggregate viewer data](data-aggregation-techniques.md) |
| Connect a Unity game | [Unity GameLink tutorial](unity-gamelink-tutorial.md) |

Use the [MEDKit REST API](../reference/medkit-rest-api.md) only when a trusted backend or non-JavaScript client needs the underlying HTTP contract.

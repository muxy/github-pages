---
title: Install MEDKit Manually
description: Add MEDKit to a browser project and verify state access in the Muxy sandbox.
slug: install-manually
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
approved_content_sha256: 2cb6d7feef00c9e92b0e4a80398041e9b42f173ddfa26003c63c3376718310a1
---

# Install MEDKit Manually

This guide creates a minimal browser project with Vite and the published `@muxy/extensions-js` package. It does not depend on placeholder files or global commands.

## Prerequisites

- Node.js 18 or newer
- A Twitch Extension Client ID registered with Muxy
- A test channel ID and user ID

If you do not yet have a Client ID, create a Twitch Extension in the [Twitch developer console](https://dev.twitch.tv/console/extensions) and register it in the [Muxy developer portal](https://dev.muxy.io/landing).

## Create the project

```bash
npm create vite@latest muxy-medkit-example -- --template vanilla
cd muxy-medkit-example
npm install
npm install @muxy/extensions-js@2.4.18
```

Create a local environment file. Vite exposes only variables prefixed with `VITE_` to browser code:

```bash title=".env.local"
VITE_MUXY_CLIENT_ID=your-extension-client-id
VITE_TWITCH_CHANNEL_ID=12345678
VITE_TWITCH_USER_ID=87654321
```

Do not put a Twitch or Muxy secret in this file. Browser extensions use Twitch authorization or sandbox JWTs; extension secrets belong only on a trusted backend.

## Initialize MEDKit

Replace `src/main.js`:

```javascript title="src/main.js"
import Muxy from "@muxy/extensions-js";
import "./style.css";

const clientID = import.meta.env.VITE_MUXY_CLIENT_ID;
const channelID = import.meta.env.VITE_TWITCH_CHANNEL_ID;
const userID = import.meta.env.VITE_TWITCH_USER_ID;

if (!clientID || !channelID || !userID) {
  throw new Error("Set VITE_MUXY_CLIENT_ID, VITE_TWITCH_CHANNEL_ID, and VITE_TWITCH_USER_ID");
}

const debugging = new Muxy.DebuggingOptions();
debugging.role("viewer");
debugging.channelID(channelID);
debugging.userID(userID);
Muxy.debug(debugging);

Muxy.setup({ clientID });

const medkit = new Muxy.SDK();
await medkit.loaded();

const state = await medkit.getChannelState();
document.querySelector("#app").textContent = JSON.stringify(state, null, 2);
```

Replace the contents of the generated `#app` element in `index.html`:

```html
<main>
  <h1>Muxy channel state</h1>
  <pre id="app">Loading…</pre>
</main>
<script type="module" src="/src/main.js"></script>
```

## Run the development server

```bash
npm run dev
```

Open the URL printed by Vite. The page should show the current channel-state object, and the browser network panel should show a request to `sandbox.api.muxy.io` when sandbox debugging is active.

## Write channel state

Writing channel state requires a broadcaster, admin, or backend context. During sandbox-only testing, change the debug role to `broadcaster` and make `userID` equal `channelID`, then run:

```javascript
await medkit.setChannelState({
  message: "Hello, world!",
});
```

Switch back to a viewer context and reload to verify the value with `getChannelState()`.

## Production checklist

- Remove `Muxy.debug(...)` before uploading the Twitch Extension bundle.
- Keep the Client ID in configuration and every secret on a trusted backend.
- Wait for `medkit.loaded()` before reading authorization, state, or configuration.
- Pin and test the MEDKit version before upgrading it.
- Configure Twitch's required CSP and allowed origins for the uploaded extension.

Continue with [Create the MEDKit control object](../recipes/create-the-medkit-control-object.md) or [State information](state-information.md).

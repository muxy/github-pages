---
title: Get Started with MEDKit
description: Choose a MEDKit project path and initialize the published JavaScript
  SDK.
slug: getting-started-with-medkit
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
approved_content_sha256: 3bae26b7b3bd72afc3afa43151e925b7fba587e04712cac276333572a186eb3d
---

# Get Started with MEDKit

MEDKit is the `@muxy/extensions-js` browser SDK for custom Twitch Extension surfaces. It provides authenticated state, configuration, messaging, polling, purchases, and Twitch helpers. Use it when you want to own the viewer or broadcaster UI; use [Gateway](unity-gateway-tutorial.md) when you want game interactions without publishing your own Twitch Extension.

## Choose a starting point

| Goal | Start here |
| --- | --- |
| Create a minimal modern project | [Install MEDKit manually](install-manually.md) |
| Build broadcaster and viewer pages | [Build a simple extension](build-a-simple-extension.md) |
| Understand state and configuration | [Developing with MEDKit](developing-with-medkit.md) |
| Call the backend without JavaScript | [REST API overview](../reference/medkit-rest-api.md) |

The public [Vue starter snapshot](https://github.com/muxy/medkit-starter-vue/tree/7f6bab36bf67ab1f5b78ecf4cf7fff8beb69f675) contains JavaScript and TypeScript examples for `config`, `live`, `panel`, `component`, and `overlay` surfaces. It is not a pinned SDK release fixture: its package manifest requests `@muxy/extensions-js` from the `^2.4.3` range and uses Vue CLI 4. Use it as a structural reference, or update its dependencies before starting a production project.

## MEDKit initialization order

Every page follows the same lifecycle:

1. During local development only, call `Muxy.debug(...)` to simulate a Twitch channel and role.
2. Call `Muxy.setup(...)` exactly once with the Twitch Extension Client ID.
3. Construct `new Muxy.SDK()`.
4. Await `medkit.loaded()` before reading authorization, state, or configuration.

```javascript
import Muxy from "@muxy/extensions-js";
Muxy.setup({ clientID: import.meta.env.VITE_CLIENT_ID });
const medkit = new Muxy.SDK();
await medkit.loaded();
```

Local simulation is not authorization. Test privileged writes with the appropriate broadcaster/admin role, and remove debug overrides from the production bundle so Twitch-provided context controls the user identity.

## Twitch Extension surfaces

- `config`: broadcaster configuration.
- `live`: broadcaster live dashboard.
- `panel`: viewer channel panel.
- `component`: viewer video component.
- `overlay`: viewer video overlay.

Twitch controls the allowed dimensions, lifecycle, CSP, and review requirements for each surface. See [Twitch Extension design guidance](https://dev.twitch.tv/docs/extensions/designing/) before packaging the final bundle.

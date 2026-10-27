---
title: Build a Simple Extension
description: Build a two-page MEDKit extension with a broadcaster dashboard and viewer
  panel.
slug: build-a-simple-extension
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
approved_content_sha256: f7928f1c2bd168675f1f221474a3cc7d30a73aea86322d69ca0a34076bcf208b
---

# Build a Simple Extension

Build a small Twitch Extension with two surfaces:

- `live.html` lets a broadcaster set a message of the day.
- `panel.html` displays the current message to viewers and receives live updates.

## Set up the project

Follow [Install MEDKit manually](install-manually.md), then create these files at the project root:

```text title="live.html"
panel.html
src/live.js
src/panel.js
```

Add both HTML entry points to the production build:

```javascript title="vite.config.js"
import { fileURLToPath } from "node:url";
import { defineConfig } from "vite";

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        live: fileURLToPath(new URL("./live.html", import.meta.url)),
        panel: fileURLToPath(new URL("./panel.html", import.meta.url)),
      },
    },
  },
});
```

Copy the implementation from [Create a broadcaster panel](create-a-broadcaster-panel.md) and [Create a viewer panel](create-a-viewer-panel.md).

## Test the complete flow

1. Run `npm run dev`.
2. Open `/live.html` and `/panel.html` from the same Vite origin.
3. Enter a message in the broadcaster page and select **Save and broadcast**.
4. Confirm the open viewer panel changes immediately.
5. Reload the viewer panel and confirm it still displays the saved channel state.

Run `npm run build` before upload. The output must contain both `live.html` and `panel.html`, with all JavaScript and CSS bundled locally; Twitch Extensions must not depend on an unapproved remote script at runtime.

The older [MEDKit examples repository](https://github.com/muxy/medkit-examples/tree/518bd07ee7b724d4367b0c66af1204a53c95c0e2/hello_world) remains useful as historical source, but this guide uses the published `@muxy/extensions-js@2.4.18` package and a current module build.

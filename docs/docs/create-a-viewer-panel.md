---
title: Create a Viewer Panel
description: Build a Twitch viewer panel that reads channel state and receives live
  MEDKit messages.
slug: create-a-viewer-panel
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
approved_content_sha256: beb92ac7ef960845ce392d374f0865bf526417b15876b5251a7ac47ad6445597
---

# Create a Viewer Panel

This viewer panel displays the broadcaster's current message and updates immediately when MEDKit receives a new `motd` event. Complete [Install MEDKit manually](install-manually.md) first, then add the files below.

## Create the panel HTML

```html title="panel.html"
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Message of the Day</title>
  </head>
  <body>
    <main>
      <h1>Message of the Day</h1>
      <p id="motd" aria-live="polite">Loading…</p>
    </main>
    <script type="module" src="/src/panel.js"></script>
  </body>
</html>
```

## Read state and listen for updates

The initial state read handles viewers who open the panel after the latest message was sent. The listener handles messages sent while the panel is open.

```javascript title="src/panel.js"
import Muxy from "@muxy/extensions-js";

async function main() {
  if (import.meta.env.DEV) {
    const debugging = new Muxy.DebuggingOptions();
    debugging
      .channelID(import.meta.env.VITE_CHANNEL_ID)
      .role("viewer");
    Muxy.debug(debugging);
  }

  Muxy.setup({ clientID: import.meta.env.VITE_CLIENT_ID });
  const medkit = new Muxy.SDK();
  await medkit.loaded();

  const message = document.querySelector("#motd");
  const state = await medkit.getChannelState();
  message.textContent = state.motd ?? "Enjoy the show!";

  medkit.listen("motd", (event) => {
    message.textContent = event.motd;
  });
}

main().catch((error) => {
  console.error(error);
  document.querySelector("#motd").textContent = "Unable to load the message.";
});
```

For local testing, set `VITE_CLIENT_ID` and `VITE_CHANNEL_ID` in `.env.local`, run `npm run dev`, and open the `panel.html` URL printed by Vite. Remove the debug configuration from production bundles; Twitch supplies the authenticated viewer context there.

Continue with [Create a broadcaster panel](create-a-broadcaster-panel.md).

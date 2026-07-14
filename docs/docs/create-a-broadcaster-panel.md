---
title: Create a Broadcaster Panel
description: Build a broadcaster dashboard page that stores and broadcasts a message
  with MEDKit.
slug: create-a-broadcaster-panel
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
approved_content_sha256: c42ac8a98d92c08104c647a88262e339ca781a5e757fec983fb2f73f826fe1d7
---

# Create a Broadcaster Panel

This live-dashboard page lets the broadcaster save a message and notify every open viewer panel. Complete [Install MEDKit manually](install-manually.md) first, then add the files below.

## Create the dashboard HTML

```html title="live.html"
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
      <label for="motd">Message</label>
      <textarea id="motd">Hello, world!</textarea>
      <button id="save" type="button">Save and broadcast</button>
      <p id="status" aria-live="polite"></p>
    </main>
    <script type="module" src="/src/live.js"></script>
  </body>
</html>
```

## Store and broadcast the message

Persisting channel state ensures viewers who open the panel later receive the current message. Sending the event updates panels that are already open.

```javascript title="src/live.js"
import Muxy from "@muxy/extensions-js";

async function main() {
  if (import.meta.env.DEV) {
    const debugging = new Muxy.DebuggingOptions();
    debugging
      .channelID(import.meta.env.VITE_CHANNEL_ID)
      .role("broadcaster");
    Muxy.debug(debugging);
  }

  Muxy.setup({ clientID: import.meta.env.VITE_CLIENT_ID });
  const medkit = new Muxy.SDK();
  await medkit.loaded();

  const input = document.querySelector("#motd");
  const status = document.querySelector("#status");
  document.querySelector("#save").addEventListener("click", async () => {
    const motd = input.value.trim();
    if (!motd) {
      status.textContent = "Enter a message first.";
      return;
    }

    await medkit.setChannelState({ motd });
    medkit.send("motd", { motd });
    status.textContent = "Message saved and broadcast.";
  });
}

main().catch((error) => {
  console.error(error);
  document.querySelector("#status").textContent = "MEDKit failed to initialize.";
});
```

For local testing, set `VITE_CLIENT_ID` and `VITE_CHANNEL_ID` in `.env.local`, run `npm run dev`, and open the `live.html` URL printed by Vite. Remove the debug configuration from production bundles; Twitch supplies the broadcaster context there.

Pair this page with [Create a viewer panel](create-a-viewer-panel.md).

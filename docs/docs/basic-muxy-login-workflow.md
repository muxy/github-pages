---
title: Request a GameLink PIN with MEDKit
description: Request and display a short-lived GameLink PIN from a broadcaster configuration
  page.
slug: basic-muxy-login-workflow
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
approved_content_sha256: 7619b1e6ad38d871a17374a08e6f7169d01cb65b0a94fb754a2ec4a6b7c1dabb
---

# Request a GameLink PIN with MEDKit

A Twitch Extension page does not perform a separate MEDKit login. After `Muxy.setup()`, MEDKit receives the current Twitch authorization context and `medkit.loaded()` resolves when it is ready.

GameLink authentication is a separate flow: a broadcaster requests a short-lived PIN from the extension configuration page, then enters that PIN in the game client.

## Request the PIN

Run this code from a broadcaster configuration surface. The extension must already be registered with Muxy.

```html title="config.html"
<button id="request-pin" type="button">Request GameLink PIN</button>
<output id="pin" aria-live="polite"></output>
<script type="module" src="/src/config.js"></script>
```

```javascript title="src/config.js"
import Muxy from "@muxy/extensions-js";

Muxy.setup({ clientID: import.meta.env.VITE_MUXY_CLIENT_ID });
const medkit = new Muxy.SDK();

const button = document.querySelector("#request-pin");
const output = document.querySelector("#pin");

button.addEventListener("click", async () => {
  button.disabled = true;
  output.textContent = "Requesting…";

  try {
    await medkit.loaded();
    const response = await medkit.signedRequest(
      "POST",
      "gamelink/token",
      {},
    );
    output.textContent = response.token;
  } catch (error) {
    console.error(error);
    output.textContent = "Could not request a GameLink PIN";
  } finally {
    button.disabled = false;
  }
});
```

Pass a JavaScript object. MEDKit 2.4.18 calls `JSON.stringify(data)` inside `signedRequest()`; passing `JSON.stringify({})` would serialize the body twice and send a JSON string instead of an object. The pinned public [`GameAuth.vue`](https://github.com/muxy/gamelink-unity-fps-demo/blob/0c4975d3a670aefe642dff2429af8fc481443a7f/Extension/src/config/components/GameAuth.vue) contains that double-serialization bug, so this corrected example intentionally differs from the demo.

## Complete authentication in the game

Pass only the displayed PIN to the GameLink client. The client exchanges it through its supported `AuthenticateWithPIN` or protocol-equivalent flow and stores the returned refresh credential securely.

- For Unity, continue with the [Unity GameLink tutorial](unity-gamelink-tutorial.md#getting-a-gamelink-pin).
- For the wire contract, see [GameLink WebSocket authentication](../reference/ws-authentication.md).

Never place a Twitch Extension secret, Muxy authentication secret, or long-lived refresh credential in browser code.

---
title: Developing with MEDKit
description: Learn the MEDKit lifecycle and choose the correct state, config, messaging,
  and test APIs.
slug: developing-with-medkit
product: MEDKit
audience: developers
status: current
owner: Developer Experience
source_of_truth: muxy/extensions-js
version: 2.4.18
last_verified: '2026-07-14'
review_state: approved
page_type: concept
approved_by: peter-bonanni
approved_at: '2026-07-14T20:34:54Z'
approval_method: user-authorized-codex-assisted-source-review
approved_content_sha256: e8efb179bc4e157af23d8efb55f756b10b57c1c49957321d323cc1b58dc55128
---

# Developing with MEDKit

After [installing MEDKit](install-manually.md), initialize one SDK instance per extension page and wait for it to load before calling backend methods.

```javascript
import Muxy from "@muxy/extensions-js";
Muxy.setup({ clientID: import.meta.env.VITE_CLIENT_ID });
const medkit = new Muxy.SDK();
await medkit.loaded();

const state = await medkit.getAllState();
console.log(state);
```

## Choose the right API

| Need | API | Guide |
| --- | --- | --- |
| Persistent extension, channel, or viewer data | State methods | [Extension and viewer state](state-information.md) |
| Broadcaster or extension settings | Config methods | [Configuration data](store-configuration-data.md) |
| Live messages between open clients | `send` and `listen` | [Simple extension](build-a-simple-extension.md) |
| Large-audience counters and rankings | Aggregation methods | [Data aggregation](data-aggregation-techniques.md) |
| Local Twitch identity/role simulation | `DebuggingOptions` | [User simulation](set-up-user-simulation.md) |
| Twitch Helix helpers | `TwitchClient` | [Twitch API](call-into-the-twitch-api.md) |

State is durable; a live message is not. For interfaces that must recover after refresh, persist the latest value first and then send a message to active clients.

## Handle failures explicitly

MEDKit methods return promises. Surface initialization and request failures in both logs and the UI, and never assume a write succeeded before its promise resolves.

```javascript
try {
  await medkit.setChannelState({ round: 4 });
  status.textContent = "Saved";
} catch (error) {
  console.error(error);
  status.textContent = "Save failed";
}
```

See [Troubleshooting](troubleshooting-tips.md) for environment, role, and token checks.

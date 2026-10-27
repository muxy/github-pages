---
title: Store Extension and Viewer State
description: Read and write extension, channel, viewer, and extension-viewer state
  with MEDKit.
slug: state-information
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
approved_content_sha256: 1ea0db59c9faf2e7d4ff9d12db704731729584029f45b8d629695f596181b147
---

# Store Extension and Viewer State

Muxy stores developer-defined JSON objects at four scopes. State is intended for live application data; validate every value your application reads.

## Choose a state store

| Store | Scope | Read | Write |
| --- | --- | --- | --- |
| Extension | Shared by every channel using the extension | Any authorized role | Extension owner in broadcaster context |
| Channel | Shared by viewers of one channel | Any authorized role | Broadcaster for that channel |
| Viewer | One viewer on one channel | Current viewer | Current viewer |
| Extension viewer | One identified viewer across channels | Current identified viewer | Current identified viewer |

`getAllState()` returns all four stores as `extension`, `channel`, `viewer`, and `extension_viewer`.

## Initialize one SDK instance

```javascript
Muxy.setup({ clientID: "your-extension-client-id" });
const medkit = new Muxy.SDK();
await medkit.loaded();
```

## Read state

```javascript
const allState = await medkit.getAllState();
const extensionState = await medkit.getExtensionState();
const channelState = await medkit.getChannelState();
const viewerState = await medkit.getViewerState();
const extensionViewerState = await medkit.getExtensionViewerState();

console.log({
  allState,
  extensionState,
  channelState,
  viewerState,
  extensionViewerState,
});
```

Example aggregate response:

```json
{
  "extension": { "featureEnabled": true },
  "channel": { "round": 4 },
  "viewer": { "selectedCharacter": "ada" },
  "extension_viewer": { "lifetimeScore": 1200 }
}
```

## Write state

Each setter replaces the object at that scope. Use the corresponding JSON Patch REST endpoint when you need an atomic partial update.

```javascript
await medkit.setExtensionState({ featureEnabled: true });
await medkit.setChannelState({ round: 4 });
await medkit.setViewerState({ selectedCharacter: "ada" });
await medkit.setExtensionViewerState({ lifetimeScore: 1200 });
```

The extension and channel writes require the roles listed above. A viewer must share identity before using extension-viewer state.

## React to changes

State is also delivered through Muxy PubSub. Subscribe once during application startup and remove listeners during teardown; avoid polling the REST API every frame.

For raw endpoints and role-specific examples, see the [REST state API](../reference/rest-state-api.md).

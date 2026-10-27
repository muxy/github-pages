---
title: Read Arbitrary JSON Stores
description: Read a channel-scoped JSON store and react to its update event with MEDKit.
slug: arbitrary-state
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
approved_content_sha256: f0d38a7853e1f00a1897d1b9c9adddb390e1e75126071e2f709ac2bbf2210ebc
---

# Read Arbitrary JSON Stores

MEDKit JSON stores are named, channel-scoped JSON documents. In `@muxy/extensions-js@2.4.18`, the public SDK exposes `getJSONStore(key)` for reads and emits `json_store_update:<key>` when a store changes.

The package declarations describe each stored value as smaller than 2 KB. Use regular [state](state-information.md) or [configuration](store-configuration-data.md) when those defined scopes fit your data.

## Read a store

Initialize MEDKit and wait for it to load before reading data:

```javascript
import Muxy from "@muxy/extensions-js";
Muxy.setup({ clientID: import.meta.env.VITE_MUXY_CLIENT_ID });
const medkit = new Muxy.SDK();
await medkit.loaded();

try {
  const basecamp = await medkit.getJSONStore("basecamp");
  console.log(basecamp);
} catch (error) {
  console.error("The basecamp store could not be read", error);
}
```

`getJSONStore()` rejects if the request fails or the key has no associated value. Omitting the key reads the `default` store.

## React to updates

`listen()` returns a listener handle immediately; it does not return a promise. The event payload is not typed in 2.4.18, so re-read the store when correctness matters:

```javascript
const handle = medkit.listen("json_store_update:basecamp", async () => {
  const basecamp = await medkit.getJSONStore("basecamp");
  renderBasecamp(basecamp);
});

window.addEventListener(
  "pagehide",
  () => medkit.unlisten(handle),
  { once: true },
);
```

## Write limitation in 2.4.18

!!! warning "No public JSON-store writer"
    The published 2.4.18 `SDK` and `StateClient` types expose only `getJSONStore()`. Do not use the old pseudo-code `set "key" to value` or invent `setJSONStore()`. A writer requires a separately verified REST or trusted-backend contract and remains subject to SME review.

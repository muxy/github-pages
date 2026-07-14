---
title: Get Viewer Information
description: Read the current MEDKit user and enumerate shared Twitch IDs from an
  admin context.
slug: get-viewer-information
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
approved_content_sha256: cd3788e367ec16f92978ba62d06e3aa351b6d9515113440cce7c5e0d47f0fc1a
---

# Get Viewer Information

MEDKit exposes the current extension user after `medkit.loaded()` resolves. A real Twitch ID is present only when the viewer has shared it with the extension.

## Read the current user

```javascript
import Muxy from "@muxy/extensions-js";
Muxy.setup({ clientID: import.meta.env.VITE_MUXY_CLIENT_ID });
const medkit = new Muxy.SDK();
await medkit.loaded();

const user = await medkit.getUser();

console.log({
  channelID: user.channelID,
  role: user.role,
  sharedTwitchID: user.twitchID ?? null,
  opaqueID: user.twitchOpaqueID,
  bufferMilliseconds: user.buffer,
});
```

Useful fields in the 2.4.18 `User` type include:

| Field | Meaning |
| --- | --- |
| `channelID` | Current Twitch channel ID |
| `twitchID` | Shared Twitch ID, or `null` when unavailable |
| `twitchOpaqueID` | Twitch's opaque identifier for the current extension user |
| `role` | Current extension role |
| `buffer`, `latency`, `bitrate` | Current player context when Twitch supplies it |
| `theme`, `volume`, `videoMode` | Current viewer UI/player context |
| `twitchJWT` | Backend authorization JWT; treat as a secret |
| `helixToken` | Token for supported Twitch front-end API calls; treat as a secret |

Use `onUserUpdate(callback)` when a page must react to a refreshed authorization context. Do not log, persist, or send either token to analytics.

## Enumerate users who shared their Twitch ID

`getExtensionUsers(next?)` is admin-only. It returns at most 1,000 entries, may return duplicates across asynchronous pages, and uses `"0"` as the terminal cursor.

```javascript
async function getSharedTwitchIDs(medkit) {
  const ids = new Set();
  let cursor;

  do {
    const page = await medkit.getExtensionUsers(cursor);

    for (const user of page.results) {
      ids.add(user.twitch_id);
    }

    cursor = page.next;
  } while (cursor !== "0");

  return [...ids];
}

await medkit.loaded();
const sharedTwitchIDs = await getSharedTwitchIDs(medkit);
console.log(`Received ${sharedTwitchIDs.length} unique Twitch IDs`);
```

Run bulk enumeration from an approved admin workflow. Add cancellation, backoff, and a page limit before using it against a large extension population.

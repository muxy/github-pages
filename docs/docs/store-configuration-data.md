---
title: Store Configuration Data
description: Read and write long-lived extension and channel configuration with MEDKit.
slug: store-configuration-data
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
approved_content_sha256: 3bdb6f436a7eaf0f9bc07515207c43e1d9c9a5dcf2acfbecb84cf401c0c4f250
---

# Store Configuration Data

Configuration stores long-lived, developer-defined JSON. Use state for frequently changing live data and configuration for settings that should survive sessions.

## Configuration scopes

| Store | Scope | Read | Write |
| --- | --- | --- | --- |
| Extension configuration | Every installation of the extension | Any authorized role | Trusted backend or configured extension owner |
| Channel configuration | One broadcaster's channel | Any authorized role on that channel | Broadcaster for that channel |

## Initialize MEDKit

```javascript
Muxy.setup({ clientID: "your-extension-client-id" });
const medkit = new Muxy.SDK();
await medkit.loaded();
```

## Read configuration

`getConfig()` returns both scopes. Use the scoped methods when you need only one object.

```javascript
const config = await medkit.getConfig();
const extensionConfig = await medkit.getExtensionConfig();
const channelConfig = await medkit.getChannelConfig();

console.log({ config, extensionConfig, channelConfig });
```

Example combined response:

```json
{
  "extension": { "purchasesEnabled": true },
  "channel": { "difficulty": "hard" }
}
```

## Write configuration

```javascript
await medkit.setExtensionConfig({
  purchasesEnabled: true,
});

await medkit.setChannelConfig({
  difficulty: "hard",
});
```

Each setter replaces that scope's complete configuration object. Use the generated JSON Patch endpoints for atomic partial updates.

Never expose an extension secret to make an extension-level write from browser code. Perform secret-authorized operations on a trusted backend using a [production JWT](../recipes/generate-a-production-jwt.md).

For raw endpoints, required roles, and JSON Patch examples, see the [configuration API](../reference/config-api.md).

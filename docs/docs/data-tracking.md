---
title: Choose a MEDKit Data Store
description: Choose state, configuration, or a named JSON store for extension data.
slug: data-tracking
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
approved_content_sha256: 7d7dbdf9315dddee22b4d5580e29475825c265f05dd83cc60247dadfd1400eaa
---

# Choose a MEDKit Data Store

`@muxy/extensions-js@2.4.18` exposes three persistent-data families. Pick the narrowest scope and update pattern that fits the data.

| Data family | Use it for | Verified 2.4.18 methods |
| --- | --- | --- |
| State | Runtime data that must survive refreshes | `getAllState()`, scoped getters, `set*State()`, `patch*State()` |
| Configuration | Settings written infrequently and read on startup | `getConfig()`, scoped getters, `set*Config()`, `patch*Config()` |
| Named JSON store | Reading channel-scoped documents by key | `getJSONStore()` |

## State scopes

`getAllState()` returns four objects:

| Field | Scope |
| --- | --- |
| `extension` | One value shared by the extension across channels |
| `channel` | One value shared by viewers in the current channel |
| `viewer` | One value for the current viewer in the current channel |
| `extension_viewer` | One value for the current identified viewer across channels |

See [State information](state-information.md) for write permissions and replacement-versus-patch behavior.

## Configuration scopes

`getConfig()` returns the combined extension and channel configuration. Use `getExtensionConfig()` or `getChannelConfig()` when only one scope is needed. See [Store configuration data](store-configuration-data.md).

## Named JSON stores

The 2.4.18 package exposes JSON-store reads and update events, but no public writer. See [Read arbitrary JSON stores](arbitrary-state.md) before adopting this store.

## Storage is not messaging

`send()` and `listen()` deliver live events; they do not provide a durable snapshot. For a UI that must recover after a refresh, persist the latest value first and then notify open clients to re-read it.

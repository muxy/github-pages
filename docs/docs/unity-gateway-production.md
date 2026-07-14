---
title: Prepare Gateway for Production
description: Make a Gateway Unity integration resilient, secure, and observable before
  release.
slug: unity-gateway-production
product: Gateway
audience: game developers
status: current
owner: Gateway SDK owner
source_of_truth: muxy/gateway-unity
version: v1.0.0-rc
last_verified: '2026-07-14'
review_state: blocked-release
page_type: task-guide
---

# Prepare Gateway for Production

## Reliability

- Keep exactly one SDK owner and call `SDK.Update()` from Unity's main thread.
- Register callbacks once per authenticated SDK session.
- Bound action inventory and gameplay impact; disable actions when their target system is unavailable.
- Make action fulfillment idempotent by transaction ID and refund effects the game cannot apply.
- Stop the WebSocket transport during teardown and test scene transitions.

## Security and privacy

- Never log PINs, JWTs, refresh tokens, user IDs, or purchase payloads.
- Store refresh tokens with platform-secure storage, not plaintext preferences.
- Validate action IDs, poll result indexes, and all remote strings before using them in game logic or UI.
- Keep sandbox and production configuration separate in the build pipeline.

## Performance

- Do not publish metadata, actions, or game text every frame.
- Keep callbacks short and move expensive work into a bounded game-side queue.
- Use readable RGB24 or RGBA32 logo textures and keep encoded assets below 500 KB.
- Exercise reconnects and long-running sessions in a development build with profiling enabled.

## Release gate

The docs and code fixtures are pinned to `v1.0.0-rc`. Do not approve this page for publication or ship that package until the Gateway SDK owner:

- reconciles tag `v1.0.0-rc` with package version `0.0.1`;
- moves `UnityEditor` imports behind `UNITY_EDITOR` so standalone players compile;
- changes generated sandbox and production connections from `ws://` to `wss://`;
- adds explicit environment selection to the prefab manager instead of always calling `RunInProduction()`; and
- publishes a tested Unity/editor/OS/architecture support matrix.

Bundled Windows, macOS, and Linux native files are implementation evidence, not standalone support claims. The `gateway-testing` game ID is also not a sandbox switch.

Next: [Run the Gateway QA checklist](unity-gateway-qa.md).

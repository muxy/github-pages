---
title: Prepare Gateway for Production
description: Check reliability, credentials, and transactions before shipping a Gateway Unity integration.
slug: unity-gateway-production
product: Gateway
audience: game developers
status: current
owner: Gateway SDK owner
source_of_truth: muxy/gateway-unity
version: v1.1.0-rc.1
last_verified: '2026-10-26'
review_state: needs-sme-review
page_type: task-guide
---

# Prepare Gateway for Production

Before shipping a game with **1.1.0-rc.1**:

- Keep one SDK owner, call `SDK.Update()` on Unity's main thread, and dispose the SDK on teardown.
- Store refresh tokens in platform-secure storage. The authentication prefab uses `PlayerPrefs`, which is for evaluation.
- Keep native debug logging disabled when exchanging credentials; never log PINs or tokens.
- Apply each action once per transaction ID. Refund an action when its effect cannot be applied.
- Validate remote action IDs, text, and poll winner indexes before using them.
- Publish metadata and game text when values change, rather than every frame.
- Test PIN and refresh authentication, disconnect/reconnect, viewer actions, votes, and scene transitions in each player target you plan to ship.

The package includes Windows, macOS, and Linux native libraries. The release candidate's documented player validation covers Windows Mono and IL2CPP; verify other targets in your own builds. The prefab manager connects to production; use a code integration for sandbox testing.

Next: [Run the Gateway QA checklist](unity-gateway-qa.md).

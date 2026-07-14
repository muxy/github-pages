---
title: Unity Gateway Tutorial
description: Add Muxy Gateway actions, polls, game text, and viewer interaction to
  a Unity game.
slug: unity-gateway-tutorial
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

# Unity Gateway Tutorial

Gateway supplies the Twitch Extension experience while your Unity game defines and responds to viewer interactions. Use this tutorial to install the SDK, authenticate a broadcaster, and add actions, polls, and game text.

!!! warning "Release confirmation required"
    These examples are verified against repository tag `v1.0.0-rc`, while its package metadata reports `0.0.1`. The pinned C# transport imports `UnityEditor` for standalone builds and opens Gateway's generated addresses with `ws://`, not `wss://`. Publication and production use remain blocked until the Gateway SDK owner publishes a consistent release with a secure transport and confirmed player-build matrix.

## What you will build

- A Unity component that owns the Gateway SDK lifecycle.
- PIN authentication with refresh-token reuse.
- Game metadata, purchasable actions, audience polls, and game text.
- Production safeguards and a repeatable QA checklist.

## Tutorial sections

1. [Start with the Gateway prefabs](unity-gateway-prefab-quickstart.md) for the fastest low-code path.
2. [Install and initialize Gateway](unity-gateway-installation.md) for a custom code integration.
3. [Authenticate and manage the SDK lifecycle](unity-gateway-authentication.md).
4. [Create and handle game actions](unity-gateway-actions.md).
5. [Add polls and game text](unity-gateway-polls-game-text.md).
6. [Prepare for production](unity-gateway-production.md).
7. [Run the QA checklist](unity-gateway-qa.md).

## Gateway features

| Feature | Use it for |
| --- | --- |
| Actions | Let viewers trigger bounded, priced effects in the game. |
| Polls | Ask the audience to choose an outcome in real time. |
| Game text | Show current game state as label-and-value pairs. |
| Bits | React to Twitch Bits transactions when the game needs less configuration than actions. |

## Before you start

You need Unity 2020.3 or newer and the [Muxy Gateway Twitch Extension](https://www.twitch.tv/ext/i575hs2x9lb3u8hqujtezit03w1740-1.0.0). Use the shared `gateway-testing` game ID only for evaluation. It does not select the sandbox environment.

The prefab manager in `v1.0.0-rc` always calls `SDK.RunInProduction()`; it has no production/sandbox Inspector setting. The code API exposes both modes, but the pinned transport uses insecure `ws://` for each. Treat the tag as source material, not a production-ready Unity package. Before shipping, obtain a corrected owner-approved release and [request a permanent game ID](https://www.muxy.io/gateway).

After installing Gateway on a Twitch channel, open its configuration page to generate the six-character PIN used by the game. A PIN expires after five minutes; request a new one if authentication does not begin promptly.

Next: [Start with the prefab quickstart](unity-gateway-prefab-quickstart.md) or [build a custom code integration](unity-gateway-installation.md).

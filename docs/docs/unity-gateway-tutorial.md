---
title: Unity Gateway Tutorial
description: Add Muxy Gateway actions, polls, game text, and viewer interaction to a Unity game.
slug: unity-gateway-tutorial
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

# Unity Gateway Tutorial

Use Muxy Gateway Unity SDK **1.1.0-rc.1** to connect a game to the Twitch Gateway extension. Start with the [illustrated walkthrough](unity-gateway-prefab-quickstart.md) if you want the SDK to manage authentication and lifecycle through prefabs.

## Guides

1. [Install and initialize from code](unity-gateway-installation.md).
2. [Authenticate a broadcaster](unity-gateway-authentication.md).
3. [Create viewer actions](unity-gateway-actions.md).
4. [Add polls and game text](unity-gateway-polls-game-text.md).
5. [Check production behavior](unity-gateway-production.md) and [run QA](unity-gateway-qa.md).

You need Unity 2020.3 or newer, a broadcaster with the [Muxy Gateway extension](https://www.twitch.tv/ext/i575hs2x9lb3u8hqujtezit03w1740-1.0.0) active, and a Game ID shown under **Configure → Linked Games**. The configuration PIN expires after five minutes. Use a separate viewer session to test actions and votes.

The prefab manager connects to production. Code integrations can call `RunInSandbox()` or `RunInProduction()` explicitly. A testing Game ID does not select the sandbox host.

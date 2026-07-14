---
title: Gateway Prefab Quickstart
description: Add Gateway authentication, actions, notifications, polls, and game text
  to Unity with the packaged prefabs.
slug: unity-gateway-prefab-quickstart
product: Gateway
audience: game developers
status: current
owner: Gateway SDK owner
source_of_truth: muxy/gateway-unity
version: v1.0.0-rc
last_verified: '2026-07-14'
review_state: blocked-release
page_type: quickstart
---

# Gateway Prefab Quickstart

The prefab flow is intended to be the shortest path from a Unity game to Twitch viewer interactions. Gateway supplies the Twitch Extension; you configure supported interactions in the Unity Inspector and connect them to game methods.

Allow about 20 minutes to assemble and inspect the prefab flow after you have an owner-approved package. The pinned `v1.0.0-rc` tag is not safe to run as a production quickstart because of the blockers below.

!!! warning "Release confirmation required"
    The prefab names and fields below are verified against `v1.0.0-rc`, whose package metadata reports `0.0.1`. The transport imports `UnityEditor` into standalone builds and uses `ws://`; the manager prefab always starts production mode. Keep this page blocked until the Gateway owner publishes a consistent release with secure transport, explicit environment selection, and verified player targets.

## 1. Install prerequisites

1. Use Unity 2020.3 or newer for editor inspection. Do not infer standalone support from the included native binaries.
2. Import TextMeshPro essentials from **Window → TextMeshPro → Import TMP Essential Resources**.
3. Install the package from `https://github.com/muxy/gateway-unity.git#v1.0.0-rc`.
4. Install the [Gateway Twitch Extension](https://www.twitch.tv/ext/i575hs2x9lb3u8hqujtezit03w1740-1.0.0) on a test channel.

## 2. Add the manager

Drag `Prefabs/MuxyGatewayManager.prefab` into the first scene that uses Gateway. Keep exactly one manager active.

In the Inspector:

- Set **Game ID** to `gateway-testing` for evaluation.
- Set the game name and optional logo under **Game Metadata**.
- Add game actions with unique IDs, valid `fa-solid` or `mdi` icons, bounded impact, and an `OnGameActionUsed` listener.
- Add initial game text and optional poll settings.
- Connect **On Authentication**, **On Any Game Action Used**, and **On Bits Used** listeners as needed.

Before shipping, [request a permanent game ID](https://www.muxy.io/gateway) and replace `gateway-testing`.

!!! danger "The prefab is not a sandbox client"
    `MuxyGatewayManager.OpenAndRunSDK()` in the pinned tag always invokes `SDK.RunInProduction()`. The `gateway-testing` game ID limits evaluation access but does not switch hosts. Use the prefab only after the SDK owner supplies an explicit, secure stage selector; use the code API to study the intended sandbox/production distinction.

## 3. Add authentication UI

Drag `Prefabs/MuxyGatewayAuthenticateUI.prefab` into the scene and assign its **Gateway Manager** field. In the Gateway Twitch Extension configuration page, generate a six-character PIN and enter it in the game within five minutes.

The prefab stores its refresh token in `PlayerPrefs`. Replace that storage with the platform's secure credential store before production.

## 4. Add optional viewer feedback

- Drag `MuxyGatewayNotifications.prefab` into the scene for scrolling action notifications, then assign its manager.
- Drag `MuxyGatewayPolling.prefab` into the scene for the included poll results display, then assign its manager.

These prefabs use TextMeshPro. Treat them as a starting point: verify fonts, colors, safe areas, input navigation, and localization in your own UI.

## 5. Connect game logic

Create a component with public methods that match the UnityEvents configured on each action:

```csharp title="GameGatewayActions.cs"
using MuxyGateway;
using UnityEngine;

public sealed class GameGatewayActions : MonoBehaviour
{
    [SerializeField] private MuxyGatewayManager gateway;

    public void SpawnBoss(GameActionUsed action)
    {
        if (!TryApplyOnce(action.TransactionID, SpawnBossInGame))
        {
            gateway.RefundGameAction(action, "The action could not be applied");
            return;
        }

        gateway.AcceptGameAction(action, "Boss spawned");
    }

    private bool TryApplyOnce(string transactionID, System.Action effect)
    {
        // Replace with durable transaction-ID storage appropriate for the game.
        effect();
        return true;
    }

    private void SpawnBossInGame() { }
}
```

Make purchase fulfillment idempotent and refund any effect the game cannot safely apply.

## 6. Run and verify

Do not run these steps with `v1.0.0-rc` as a release candidate. First confirm that the package you received fixes the standalone `UnityEditor` import, uses `wss://`, and exposes the intended environment explicitly.

1. Authenticate with a fresh PIN.
2. Confirm from sanitized transport diagnostics that a development build uses the sandbox host; never log the PIN or returned tokens.
3. Confirm metadata and actions appear in the Gateway extension.
4. Trigger every action and verify it applies once.
5. Start a poll and verify live and final results.
6. Restart the game and confirm refresh authentication.
7. Disconnect the network and verify recovery without duplicated listeners or purchases.
8. Build and run every standalone target you plan to support; a successful editor session is not sufficient.

## Recovery

If authentication never starts, check the selected host and secure scheme before requesting another PIN. If a player build fails on `UnityEditor`, stop: the package still contains the pinned source blocker. If the prefab connects to production while you expected sandbox, do not continue testing purchases; replace it with an owner-approved package that exposes stage selection.

Continue with the [custom code installation](unity-gateway-installation.md) for full lifecycle control or run the [Gateway QA checklist](unity-gateway-qa.md).

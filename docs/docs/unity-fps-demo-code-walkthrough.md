---
title: Unity FPS Demo Code Walkthrough
description: Trace authentication, polls, state, datastream events, and purchases
  through the public Unity FPS demo.
slug: unity-fps-demo-code-walkthrough
product: Unity
audience: game developers
status: current
owner: Unity SDK owner
source_of_truth: muxy/gamelink-unity
version: unverified
last_verified: '2026-07-14'
review_state: blocked-release
page_type: task-guide
---

# Trace the Unity FPS GameLink demo

The public FPS demo shows how a Unity game and a Twitch Extension exchange authentication, poll, state, datastream, and purchase events. Use it as a pinned code study, not as a released or drop-in sample.

!!! warning "Source blockers"
    This page is verified against [`muxy/gamelink-unity-fps-demo` commit `0c4975d`](https://github.com/muxy/gamelink-unity-fps-demo/tree/0c4975d3a670aefe642dff2429af8fc481443a7f) and [`muxy/gamelink-unity` commit `d68d60f`](https://github.com/muxy/gamelink-unity/tree/d68d60fee8f7a5615a126e3aa6013b969be4ea03). Neither is a confirmed SDK release. Both the demo runtime and the pinned SDK transport pull `UnityEditor` into standalone compilation; the demo also calls `PrefabUtility`, omits prefab/script `.meta` files, and serializes `GAMELINK_CLIENT_ID` while the script declares `GAMELINK_EXTENSION_ID`. Bundled Windows and macOS native libraries therefore do not establish standalone support. Repair those upstream issues before treating the Unity sample as runnable.

## Check out the exact sources

```bash
git clone https://github.com/muxy/gamelink-unity-fps-demo.git
cd gamelink-unity-fps-demo
git checkout 0c4975d3a670aefe642dff2429af8fc481443a7f
```

The important files are:

| File | Responsibility |
| --- | --- |
| [`GameLinkFPSBehaviour.cs`](https://github.com/muxy/gamelink-unity-fps-demo/blob/0c4975d3a670aefe642dff2429af8fc481443a7f/GameLinkFPSBehaviour.cs) | Unity connection, authentication, polls, state, datastream events, and purchases |
| [`GameAuth.vue`](https://github.com/muxy/gamelink-unity-fps-demo/blob/0c4975d3a670aefe642dff2429af8fc481443a7f/Extension/src/config/components/GameAuth.vue) | Broadcaster PIN request |
| [`App.vue`](https://github.com/muxy/gamelink-unity-fps-demo/blob/0c4975d3a670aefe642dff2429af8fc481443a7f/Extension/src/overlay/App.vue) | Viewer overlay setup and broadcast listeners |
| [`PollVote.vue`](https://github.com/muxy/gamelink-unity-fps-demo/blob/0c4975d3a670aefe642dff2429af8fc481443a7f/Extension/src/overlay/components/PollVote.vue) | Viewer voting |
| [`Actions.vue`](https://github.com/muxy/gamelink-unity-fps-demo/blob/0c4975d3a670aefe642dff2429af8fc481443a7f/Extension/src/overlay/components/Actions.vue) | Datastream actions |
| [`use-state.js`](https://github.com/muxy/gamelink-unity-fps-demo/blob/0c4975d3a670aefe642dff2429af8fc481443a7f/Extension/src/shared/hooks/use-state.js) | Channel-state loading and updates |

## Run the extension

The current demo uses Vite. From `Extension`:

```bash
cp .env.sample .env
npm install
npm run dev
```

Set `VITE_CLIENT_ID` in `.env` to the registered Twitch Extension client ID. The pinned [`vite.config.js`](https://github.com/muxy/gamelink-unity-fps-demo/blob/0c4975d3a670aefe642dff2429af8fc481443a7f/Extension/vite.config.js) serves:

- Broadcaster configuration: `http://localhost:3000/config.html`
- Viewer overlay: `http://localhost:3000/overlay.html`

The source README's port `4000` is stale. `npm run build` currently produces both pages under `dist`; it does not produce the ZIP claimed by the README. The repository has no dependency lockfile, and a 2026-07-14 install reported audit findings, so lock, upgrade, and review the dependency tree before production use.

## Authentication flow

1. The configuration page creates a broadcaster MEDKit instance with `provideMEDKit`.
2. `GameAuth.vue` waits for `medkit.loaded()`, then requests a PIN:

    ```javascript
    async function requestGameLinkPin(medkit) {
      await medkit.loaded();
      const response = await medkit.signedRequest(
        "POST",
        "gamelink/token",
        {}
      );
      return response.token;
    }
    ```

    The pinned `GameAuth.vue` passes `JSON.stringify({})` here, but MEDKit 2.4.18 serializes request data internally. Passing `{}` avoids sending a double-serialized JSON string.

3. The broadcaster enters that PIN in Unity. `GameLinkFPSBehaviour.OnClickAuthWithPIN` calls `GameLink.AuthenticateWithPIN(PINInput.text, AuthCB)`.
4. On success, the game reads `GameLink.User.RefreshToken`, hides the login UI, and subscribes to purchases and datastream events.

The demo stores the refresh token in `PlayerPrefs`. A production game should use its platform's secure credential store.

## Connection lifecycle

`SetupGameLink` constructs `new SDK(clientId)`, creates `new WebsocketTransport(true)`, and opens `Stage.Sandbox`. `Update` calls `Transport.Update(GameLink)` every frame so queued callbacks run on Unity's main thread. `OnApplicationQuit` stops the transport.

For a clean, compilable lifecycle component, use the [basic Unity GameLink tutorial](unity-gamelink-tutorial.md). The demo's `UnityEditor.PrefabUtility` dependency must be replaced with serialized prefab references, or isolated in editor-only code, before a player build can compile.

## Poll flow

The gravity poll crosses both projects:

1. Unity calls `CreatePoll("gravityMode", ...)`, `SubscribeToPoll("gravityMode")`, and `SendBroadcast("start_poll", payload)`.
2. The overlay listens for `start_poll` and displays `PollVote.vue`.
3. A viewer chooses an option; the component calls `medkit.vote("gravityMode", option)`.
4. Unity's `OnPollUpdate` callback receives aggregate results.
5. Unity calls `GetPoll`, applies the winning jump force, broadcasts `stop_poll`, and deletes the poll.

The broadcast payload uses `poll_duration`; the poll ID is the stable join key between Unity and the viewer extension.

## Datastream and purchase flow

`Actions.vue` sends a JSON object to `POST datastream`. Unity subscribes with `SubscribeToDatastream`, then parses each `DatastreamUpdate.Event.Json` into this contract:

```csharp
public struct GameDatastreamEvent
{
    public string spawnMonsterType;
    public string spawnPickupType;
}
```

The overlay's Bits component loads products with `medkit.getProducts()` and starts a purchase with `medkit.purchase(product.sku)`. Unity registers `OnTransaction`, subscribes with `SubscribeToAllPurchases`, and branches on `Transaction.SKU` to spawn the purchased enemy.

Production transaction handling must be idempotent and must validate or refund each transaction after applying the effect. The demo only illustrates event receipt.

## Channel-state flow

Unity counts hoverbot and turret kills in `GameChannelState`. It initializes channel state with `SetState`, batches JSON Patch operations in `SDK.PatchList`, and periodically sends them with `UpdateStateWithPatchList`.

The overlay:

1. Calls `medkit.getChannelState()` for the initial snapshot.
2. Normalizes missing values to zero.
3. Listens for `channel_state_update` and merges later snapshots into Vue reactive state.

See [data tracking](data-tracking.md) before choosing state scope or designing a production schema.

## Make the Unity sample runnable

Before using the sample in a game:

1. Replace `PrefabUtility.LoadPrefabContents` fields with serialized `GameObject` prefab references and remove the `UnityEditor` import from runtime code.
2. Fix the pinned SDK transport so `UnityEditor` is imported only under `UNITY_EDITOR`.
3. Reattach `GameLinkFPSBehaviour` to the prefab, rename or migrate the serialized client-ID field consistently, and commit the generated `.meta` files.
4. Install GameLink from the pinned URL in the [basic tutorial](unity-gamelink-tutorial.md).
5. Rebuild the scene references against the specific FPS Microgame version you support.
6. Verify authentication, poll cleanup, state reset, transaction handling, reconnect behavior, and application shutdown in an actual standalone build.

Keep release publication blocked until the SDK owner publishes a supported GameLink version and the demo repository resolves these source blockers.

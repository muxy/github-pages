---
title: Gateway Unity SDK Walkthrough
description: Install Gateway in Unity, connect a broadcaster, and test actions, game text, and polls.
slug: unity-gateway-prefab-quickstart
product: Gateway
audience: game developers
status: current
owner: Gateway SDK owner
source_of_truth: muxy/gateway-unity
version: v1.0.0-rc
last_verified: '2026-10-26'
review_state: blocked-release
page_type: quickstart
---

# Gateway Unity SDK Walkthrough

Take a new Unity project from package installation to a connected Twitch broadcaster channel. You will add a **Spawn Healthpack** action, publish a **Health** game text value, and run a 30-second viewer poll. The prefab supplies the authentication screen and SDK lifecycle; the [demo component](../assets/unity-gateway/GatewayPrefabDemo.cs) supplies test gameplay and a poll button.

This walkthrough was performed on October 26, 2026, in the Unity **6000.6.6f1 Windows Editor** using a local `muxy/gateway-unity` checkout with compatibility and credential-log changes. The page's version metadata tracks the last public tag, `v1.0.0-rc`; that tag is **not** the checkout used for the hands-on test. The package identified itself as `0.0.1`. Live PIN authentication, return-session authentication, local health changes, and a final poll update with no votes were observed. The broadcaster channel was offline, so a viewer-triggered action and a submitted vote remain to be checked. The images show the actual test session.

The numbered boxes in the screenshots point to the relevant controls and results. Select an image to open it at full resolution.

!!! warning "Unreleased package and player-build limits"
    The public [`v1.0.0-rc` tag](https://github.com/muxy/gateway-unity/tree/v1.0.0-rc) is older than the local checkout used here. Its standalone transport and `ws://` issues are documented in [installation](unity-gateway-installation.md). The prefab currently calls `RunInProduction()`; a testing Game ID does not select a sandbox host. This page remains `blocked-release` until the SDK owner publishes and pins a corrected package and verifies player targets. These Editor results do not establish macOS or other player support.

## Before you start

- A Unity project. The package declares Unity 2020.3 as its minimum; this procedure was tested in Unity 6000.6.6f1 on Windows.
- The SDK checkout or a release ZIP containing `package.json`, `Runtime`, `Prefabs`, and their `.meta` files. Keep an extracted local package folder in place after installing it.
- A Twitch broadcaster account that can install and activate the [Muxy Gateway extension](https://www.twitch.tv/ext/i575hs2x9lb3u8hqujtezit03w1740-1.0.0).
- A **Game ID linked to that broadcaster** in the extension's **Configure → Linked Games** view. This test account listed `gamelink-testing`; the SDK README's `gateway-testing` was not linked to it. Use the exact ID shown for your account.
- A separate viewer session, ideally while the channel is live, for the final action and vote checks.

If your own scripts use an assembly definition, add `Muxy.Gateway` to its Assembly Definition References. SDK types use `using MuxyGateway;`; prefab components such as `MuxyGatewayManager` are in the global namespace.

## 1. Install the local package

1. Extract the SDK to a stable location outside the Unity project's `Assets` folder. Find its `package.json`.
2. In Unity open **Window → Package Manager**. In some newer Editors the menu is **Window → Package Management → Package Manager**.
3. Choose **+ / Add → Add package from disk…** (or **Install package from disk…**) and select `package.json`.
4. Wait for dependency resolution and C# compilation. Import **TMP Essential Resources** from **Window → TextMeshPro** if Unity requests them.
5. Confirm **Muxy Gateway** appears as a **Local** package and **Packages → Muxy Gateway → Prefabs** exists in the Project window. Resolve Console errors before continuing.

<figure class="gateway-shot" markdown="1">
<div class="gateway-shot__image" markdown="1">

[![Unity Package Manager with Muxy Gateway installed as a local package and dependencies visible.](../assets/unity-gateway/01-package-manager.jpg){ width="802" height="604" }](../assets/unity-gateway/01-package-manager.jpg)

<span class="gateway-shot__box" data-step="1" style="left: 34%; top: 12%; width: 34%; height: 41%;" aria-hidden="true"></span>
<span class="gateway-shot__box" data-step="2" style="left: 16%; top: 30%; width: 18%; height: 9%;" aria-hidden="true"></span>
</div>
<figcaption><span class="gateway-shot__key">1</span> Muxy Gateway package details and dependencies. <span class="gateway-shot__key">2</span> The package in the local package list.</figcaption>
</figure>

*The test project showed package version `0.0.1`; Unity resolved a newer uGUI than the package manifest requested. Let the Editor resolve compatible UI versions.*

## 2. Build the scene

1. Create and save a test scene, for example `GatewayDemo`.
2. Drag **`MuxyGatewayManager.prefab`** from the package's `Prefabs` folder into the Hierarchy. Keep one manager active. Set **Game ID** to the exact linked ID, **Game Metadata → Name** to `Gateway Unity Demo`, and **Theme** to `default`. Leave **Logo** empty for this first test.
3. Drag **`MuxyGatewayAuthenticateUI.prefab`** into the scene. In its `MuxyGatewayAuthentication` component, assign the scene's manager to **Gateway Manager**. Set this reference before entering Play mode; the UI subscribes when enabled.
4. Keep one **EventSystem**. The authentication prefab already contains one. Remove an extra scene EventSystem if Unity warns about duplicates.
5. In Unity 6 with the new Input System, select the authentication prefab's **EventSystem**. If **Standalone Input Module** warns that it will not work, select **Replace with InputSystemUIInputModule**. Make this change outside Play mode and save the scene. It made the PIN field clickable in this test.
6. On the manager, add **Game Texts** element 0: **Label** `Health`, **Value** `50`, **Icon** `fa-solid:heart`.
7. Save [GatewayPrefabDemo.cs](../assets/unity-gateway/GatewayPrefabDemo.cs) in your game's `Assets/Scripts` folder. Attach it to a new GameObject named `GatewayDemoController`, then assign its **Gateway Manager** field to the scene manager. Use **Assets → Refresh** if the component does not appear after copying it.
8. The demo uses `OnGUI` buttons. If your project uses only the new Input System, set **Edit → Project Settings → Player → Other Settings → Active Input Handling** to **Both**. Unity may require an Editor restart.

<figure class="gateway-shot" markdown="1">
<div class="gateway-shot__image" markdown="1">

[![Unity Hierarchy with Gateway manager, authentication prefab, and demo controller; authentication Inspector points to the scene manager.](../assets/unity-gateway/02-scene-wiring.jpg){ width="1924" height="1392" }](../assets/unity-gateway/02-scene-wiring.jpg)

<span class="gateway-shot__box" data-step="1" style="left: 3%; top: 11%; width: 10%; height: 8%;" aria-hidden="true"></span>
<span class="gateway-shot__box" data-step="2" style="left: 55%; top: 25%; width: 44%; height: 5%;" aria-hidden="true"></span>
</div>
<figcaption><span class="gateway-shot__key">1</span> Manager, authentication UI, and demo controller in the Hierarchy. <span class="gateway-shot__key">2</span> The authentication prefab's Gateway Manager reference.</figcaption>
</figure>

<figure class="gateway-shot" markdown="1">
<div class="gateway-shot__image" markdown="1">

[![Unity EventSystem Inspector showing Input System UI Input Module on the authentication prefab.](../assets/unity-gateway/02-input-module.png){ width="1924" height="1392" }](../assets/unity-gateway/02-input-module.png)

<span class="gateway-shot__box" data-step="1" style="left: 4%; top: 17%; width: 9%; height: 4%;" aria-hidden="true"></span>
<span class="gateway-shot__box" data-step="2" style="left: 55%; top: 27%; width: 44%; height: 31%;" aria-hidden="true"></span>
</div>
<figcaption><span class="gateway-shot__key">1</span> Select the authentication prefab's EventSystem. <span class="gateway-shot__key">2</span> Confirm Input System UI Input Module replaced the standalone module.</figcaption>
</figure>

**Checkpoint:** The manager, authentication UI, and demo controller have their references set; the scene is saved; the Console has no compilation errors.

## 3. Activate the extension and connect the broadcaster

1. In the Twitch Creator Dashboard, install Gateway under **Extensions** and activate it in a supported overlay or panel slot.
2. Open its **Configure** view. Under **Linked Games**, check the exact Game ID against the manager's **Game ID** field. Select **Get New Code** if the PIN has expired.
3. Enter the six-character PIN into the Unity authentication UI within five minutes and submit it. Keep PINs and returned tokens out of screenshots, source control, and logs.
4. In the Unity Game view, confirm the success state and the demo's **Authenticated** status. Stop and restart Play mode; a successful return-session authentication shows the stored refresh token was reused.

<figure class="gateway-shot" markdown="1">
<div class="gateway-shot__image" markdown="1">

[![Twitch Extensions dashboard showing Gateway active in an overlay slot.](../assets/unity-gateway/03-extension-active.png){ width="460" height="210" }](../assets/unity-gateway/03-extension-active.png)

<span class="gateway-shot__box" data-step="1" style="left: 6%; top: 64%; width: 87%; height: 24%;" aria-hidden="true"></span>
</div>
<figcaption><span class="gateway-shot__key">1</span> Gateway is active in Overlay 1, marked with a green status dot.</figcaption>
</figure>

<figure class="gateway-shot" markdown="1">
<div class="gateway-shot__image" markdown="1">

[![Gateway configuration with a masked PIN and the Linked Games list visible.](../assets/unity-gateway/03-extension-pin.png){ width="1662" height="916" }](../assets/unity-gateway/03-extension-pin.png)

<span class="gateway-shot__box" data-step="1" style="left: 26%; top: 53%; width: 21%; height: 12%;" aria-hidden="true"></span>
<span class="gateway-shot__box" data-step="2" style="left: 56%; top: 40%; width: 18%; height: 11%;" aria-hidden="true"></span>
</div>
<figcaption><span class="gateway-shot__key">1</span> Masked configuration PIN and Get New Code link. <span class="gateway-shot__key">2</span> Linked Games; use the Game ID listed for your broadcaster.</figcaption>
</figure>

<figure class="gateway-shot" markdown="1">
<div class="gateway-shot__image" markdown="1">

[![Unity Game view showing successful Gateway authentication and the demo's authenticated status.](../assets/unity-gateway/04-authenticated.png){ width="1924" height="1392" }](../assets/unity-gateway/04-authenticated.png)

<span class="gateway-shot__box" data-step="1" style="left: 14%; top: 10%; width: 23%; height: 5%;" aria-hidden="true"></span>
<span class="gateway-shot__box" data-step="2" style="left: 25%; top: 35%; width: 17%; height: 4%;" aria-hidden="true"></span>
</div>
<figcaption><span class="gateway-shot__key">1</span> Demo status says Authenticated. <span class="gateway-shot__key">2</span> The prefab confirms authentication succeeded.</figcaption>
</figure>

The packaged prefab stores its refresh token in `PlayerPrefs`. A shipped game needs platform-secure credential storage. The prefab calls `RunInProduction()`; neither the Game ID nor this scene changes its host. See [authentication and lifecycle](unity-gateway-authentication.md) for the code API.

## 4. Add and test a viewer action

Leave Play mode before editing the manager. Under **Game Actions**, add one element:

| Inspector field | Value |
| --- | --- |
| ID | `healthpack` |
| Name | `Spawn Healthpack` |
| Description | `Add up to 10 health to the player.` |
| Category | `Help` |
| State | `Available` |
| Impact | `1` |
| Icon | `fa-solid:heart` |
| Count | `65535` (`GameAction.InfiniteCount`) |

On the action's **On Game Action Used** event, select **+**, drag in `GatewayDemoController`, and choose **GatewayPrefabDemo → OnHealthpack** under **Dynamic GameActionUsed**. The dynamic binding passes the received transaction to the handler.

<figure class="gateway-shot" markdown="1">
<div class="gateway-shot__image" markdown="1">

[![Gateway manager Inspector showing the healthpack action fields and dynamic OnHealthpack event binding.](../assets/unity-gateway/05-action-inspector.jpg){ width="1924" height="1392" }](../assets/unity-gateway/05-action-inspector.jpg)

<span class="gateway-shot__box" data-step="1" style="left: 55%; top: 36%; width: 44%; height: 14%;" aria-hidden="true"></span>
<span class="gateway-shot__box" data-step="2" style="left: 58%; top: 50%; width: 41%; height: 6%;" aria-hidden="true"></span>
<span class="gateway-shot__box" data-step="3" style="left: 55%; top: 60%; width: 44%; height: 8%;" aria-hidden="true"></span>
</div>
<figcaption><span class="gateway-shot__key">1</span> Healthpack action fields. <span class="gateway-shot__key">2</span> Dynamic OnHealthpack event binding. <span class="gateway-shot__key">3</span> Health game text.</figcaption>
</figure>

First use **Local test: add 10 health** in the Game view. Health should change from **50** to **60**. This checks the demo behavior and UI input only. Restart Play mode to reset health to 50.

<figure class="gateway-shot" markdown="1">
<div class="gateway-shot__image" markdown="1">

[![Unity Game view showing Health 60 after the local test button, with no Console errors.](../assets/unity-gateway/04-local-test.jpg){ width="1924" height="1392" }](../assets/unity-gateway/04-local-test.jpg)

<span class="gateway-shot__box" data-step="1" style="left: 14%; top: 10%; width: 23%; height: 8%;" aria-hidden="true"></span>
</div>
<figcaption><span class="gateway-shot__key">1</span> Health is 60 after selecting Local test: add 10 health.</figcaption>
</figure>

Then authenticate, open the active extension as a viewer while the channel is live, and select **Spawn Healthpack**. Verify Unity reports **Viewer action received: healthpack**, health becomes **60**, and the extension's Health value updates to **60**. Review the Twitch confirmation and any purchase cost before submitting. This full viewer round trip was **not observed** in the offline-channel test and still needs its own screenshot. The demo calls `AcceptGameAction` after applying the effect; production handlers should deduplicate transaction IDs and use `RefundGameAction` when the effect cannot be applied.

## 5. Publish game text and run a poll

The demo updates the manager's **Health** game text after authentication and health changes. `SetGameTextAt` publishes the updated list. When adding or clearing entries in your own code, call `SubmitGameTexts` to publish the list; do not resend unchanged values every frame.

While authenticated, select **Start 30-second viewer poll** in the Game view. The demo asks **Where should we go next?** with **Forest**, **Desert**, and **Ice Cave** options. A final callback is expected after 30 seconds. With no votes, the demo reports **Poll ended without a usable winner**; it checks the reported index before using an option. This no-vote path succeeded in the live test.

<figure class="gateway-shot" markdown="1">
<div class="gateway-shot__image" markdown="1">

[![Unity Game view showing the final no-vote poll result after 30 seconds.](../assets/unity-gateway/07-poll-no-votes.png){ width="1924" height="1392" }](../assets/unity-gateway/07-poll-no-votes.png)

<span class="gateway-shot__box" data-step="1" style="left: 14%; top: 10%; width: 23%; height: 5%;" aria-hidden="true"></span>
</div>
<figcaption><span class="gateway-shot__key">1</span> The demo reports that the poll ended without a usable winner after no viewer votes.</figcaption>
</figure>

To verify voting, have a viewer submit one of the options through the live extension and check the final winner in Unity. That path was not observed while the broadcaster was offline. If you add `MuxyGatewayPolling.prefab`, assign its **Gateway Manager** and forward the poll callback to its `OnPollUpdate` event as the demo component does. For further examples, see [polls and game text](unity-gateway-polls-game-text.md).

## 6. Test and troubleshoot

| Check | Expected result | If it fails |
| --- | --- | --- |
| Package import | Local package and prefabs appear; no C# errors | Confirm `package.json` was selected and the package folder still exists. |
| PIN field | Click and type in Play mode | Keep one EventSystem; replace Standalone Input Module with Input System UI Input Module outside Play mode. |
| Authentication | Success UI and authenticated demo status | Use a fresh PIN; match **Game ID** to **Linked Games** exactly; check that Gateway is active. |
| Return session | Restarting Play mode authenticates again | Check that initial authentication succeeded and local `PlayerPrefs` was retained. |
| Local health button | Health changes 50 → 60 | Set **Active Input Handling** to **Both** for the demo's `OnGUI` buttons; assign the manager reference. |
| Viewer action | Health changes after a viewer selects the action | Confirm the channel is live, extension visible, and **Dynamic GameActionUsed** wired to `OnHealthpack`. |
| Poll | Final result arrives after 30 seconds | Confirm authentication, select the poll button once, and wait for the final update. No votes is a valid outcome. |

The walkthrough verified the Windows Editor path. Before release, test a standalone player for each intended platform, disconnect/reconnect behavior, action idempotency, secure token storage, and complete viewer action and vote flows. The [QA checklist](unity-gateway-qa.md) tracks these checks; [production practices](unity-gateway-production.md) covers reliability and security.

## Images still needed

The nine images above were captured from the test session. Two proof images still require a live viewer interaction:

1. **Viewer action round trip:** the extension showing **Spawn Healthpack** and Health changing from 50 to 60, beside Unity showing the received-action status and Health 60.
2. **Voted poll result:** a submitted Forest, Desert, or Ice Cave vote in the extension and Unity's final winner message. A during-poll frame and a final frame are useful if one screenshot cannot show both.

Capture readable application crops. Hide PINs, JWTs, refresh tokens, account details, browser notifications, and unrelated paths. The masked PIN screenshot above illustrates the intended treatment.

Next, review the [custom-code installation](unity-gateway-installation.md) if you need to own the SDK lifecycle instead of using the prefab.

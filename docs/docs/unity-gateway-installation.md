---
title: Install and Initialize Gateway for Unity
description: Install the pinned Gateway Unity package and create a component that
  owns its SDK lifecycle.
slug: unity-gateway-installation
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

# Install and Initialize Gateway for Unity

!!! warning "Pinned source is not a supported player release"
    Tag `v1.0.0-rc` contains native binaries for several desktop targets, but its C# transport imports `UnityEditor` when `UNITY_STANDALONE` is defined. It also prepends `ws://` to production and sandbox addresses. Do not ship or claim standalone support from this tag; wait for an owner-approved package that compiles players and uses `wss://`.

## Editor and binary evidence

| Item | Present in `v1.0.0-rc` | What it proves |
| --- | --- | --- |
| Unity | Package declares Unity 2020.3 | Minimum editor metadata only |
| Windows | `Runtime/x64/cgamelink.dll` | A native artifact is bundled, not that a player compiles or runs |
| macOS | `Runtime/macos/libcgamelink.dylib` | A native artifact is bundled, not an architecture support promise |
| Linux | `Runtime/linux/x64/libcgamelink.so` | A native artifact is bundled, not that importer settings are correct |
| WebGL, iOS, Android, consoles | No matching native library | These targets are not supplied by the tag |

The optional UI prefabs depend on TextMeshPro. In Unity, choose **Window → TextMeshPro → Import TMP Essential Resources** before opening them.

## Install the package

In Unity Package Manager, choose **Add package from Git URL** and use the pinned release tag:

```text
https://github.com/muxy/gateway-unity.git#v1.0.0-rc
```

Pinning the tag prevents a future `main` branch change from silently changing your build.

## Review the intended SDK lifecycle

The code API distinguishes `RunInSandbox()` from `RunInProduction()`. The following component documents that intended lifecycle, but it is not a production recipe until the transport blockers above are fixed. Attach one owner to a persistent GameObject. `gateway-testing` is an evaluation game ID, not an environment selector.

```csharp
using MuxyGateway;
using UnityEngine;

public sealed class GatewayClient : MonoBehaviour
{
    [SerializeField] private string gameId = "gateway-testing";
    [SerializeField] private bool production;

    public SDK Client { get; private set; }

    private void Awake()
    {
        Client = new SDK(gameId);

        if (production)
            Client.RunInProduction();
        else
            Client.RunInSandbox();
    }

    private void Update()
    {
        Client?.Update();
    }

    private void OnDestroy()
    {
        Client?.StopWebsocketTransport();
    }
}
```

`SDK.Update()` dispatches queued Gateway work and must run on Unity's main thread. Keep one SDK owner and avoid creating a client per scene.

## Verify a corrected package

1. Confirm the package imports `UnityEditor` only under `UNITY_EDITOR` and opens generated Gateway hosts with `wss://`.
2. Run the game in sandbox mode and verify the sandbox hostname from sanitized diagnostics.
3. Confirm that Gateway does not report transport initialization errors.
4. Load and unload a scene; confirm the SDK-owning object is not duplicated.
5. Stop Play mode and confirm the transport closes cleanly.
6. Build and run each intended standalone target before recording it as supported.

If the build reports a missing `UnityEditor` namespace or diagnostics show `ws://`, the package still matches the blocked tag. Do not switch to production as a workaround.

Next: [Authenticate and manage the SDK lifecycle](unity-gateway-authentication.md).

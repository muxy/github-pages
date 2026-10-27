---
title: Install and Initialize Gateway for Unity
description: Install Gateway Unity SDK 1.1.0-rc.1 and own its lifecycle in code.
slug: unity-gateway-installation
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

# Install and Initialize Gateway for Unity

Requires Unity 2020.3 or newer and Git on your `PATH`. In **Window → Package Manager**, select **+ / Add → Install package from git URL** and paste:

```text
https://github.com/muxy/gateway-unity.git#v1.1.0-rc.1
```

Wait for compilation, then confirm **Muxy Gateway 1.1.0-rc.1** appears. The package is at the repository root; no `?path=` is needed. For prefabs, import **TMP Essential Resources** from **Window → TextMeshPro** if prompted. If your own scripts use an assembly definition, reference `Muxy.Gateway`.

## Initialize from code

Attach one SDK owner to a GameObject. Use the Game ID linked in your broadcaster's extension configuration. Select sandbox or production explicitly; a testing Game ID does not change the host.

```csharp
using MuxyGateway;
using UnityEngine;

public sealed class GatewayClient : MonoBehaviour
{
    [SerializeField] private string gameId;
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

    private void Update() => Client?.Update();

    private void OnDestroy()
    {
        Client?.Dispose();
        Client = null;
    }
}
```

`SDK.Update()` dispatches callbacks on Unity's main thread. Dispose the client when its owner is destroyed. If you use `MuxyGatewayManager.prefab`, it already owns these lifecycle calls and connects to production; follow the [illustrated prefab walkthrough](unity-gateway-prefab-quickstart.md).

## Check the connection

1. Enter Play mode and check for compilation or connection errors in the Console.
2. Authenticate with a current configuration PIN from the [extension](unity-gateway-authentication.md).
3. Stop Play mode and confirm the transport closes cleanly.
4. Build and run your intended player target before shipping. The release candidate has been validated on Windows Mono and IL2CPP; test other platforms in your own build.

Next: [Authenticate and manage the SDK lifecycle](unity-gateway-authentication.md).

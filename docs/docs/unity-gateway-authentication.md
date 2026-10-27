---
title: Authenticate and Manage the Gateway Lifecycle
description: Authenticate Gateway with a PIN, reuse refresh tokens, and publish game
  metadata safely.
slug: unity-gateway-authentication
product: Gateway
audience: game developers
status: current
owner: Gateway SDK owner
source_of_truth: muxy/gateway-unity
version: v1.1.0-rc.1
last_verified: '2026-10-27'
review_state: needs-sme-review
page_type: task-guide
---

# Authenticate and Manage the Gateway Lifecycle

The broadcaster enters a short-lived PIN once. After successful authentication, store the returned refresh token and use it for later sessions.

## Obtain the PIN

1. Install the [Muxy Gateway Twitch Extension](https://www.twitch.tv/ext/i575hs2x9lb3u8hqujtezit03w1740-1.0.0) on the broadcaster's channel.
2. Open the extension's **Configure** page in the Twitch dashboard.
3. Copy the displayed six-character configuration PIN into the game.
4. Submit it within five minutes. Generate a new PIN if it expires.

Use the exact Game ID shown under **Configure → Linked Games** for your broadcaster. [Request a permanent game ID](https://www.muxy.io/gateway) before distributing the integration.

## Register the callback

Keep the delegate in a field so its lifetime matches the SDK client.

```csharp
using System;
using MuxyGateway;
using UnityEngine;

private SDK.OnAuthenticateDelegate authenticateCallback;

private void ConfigureAuthentication()
{
    authenticateCallback = response =>
    {
        if (response.HasError)
        {
            PlayerPrefs.DeleteKey("MuxyGatewayRefreshToken");
            return;
        }

        PlayerPrefs.SetString("MuxyGatewayRefreshToken", response.RefreshToken);
        PublishGameMetadata();
    };
}

public void AuthenticateWithPin(string pin)
{
    gateway.Client.AuthenticateWithPIN(pin.Trim(), authenticateCallback);
}

private void RestoreSession()
{
    var token = PlayerPrefs.GetString("MuxyGatewayRefreshToken", "");
    if (!String.IsNullOrEmpty(token))
        gateway.Client.AuthenticateWithRefreshToken(token, authenticateCallback);
}
```

Do not log PINs, JWTs, or refresh tokens. `PlayerPrefs` illustrates the flow but is not encrypted storage; use platform-secure storage for a shipped game.

## Production token storage

The **MuxyGatewayManager** prefab in 1.1.0-rc.1 reads, writes, and clears `MuxyGatewayRefreshToken` through `PlayerPrefs`; it has no token-store setting. For a shipped game, use the [code integration](unity-gateway-installation.md) to own authentication and persistence rather than relying on that prefab for refresh-token storage.

1. Add a token-store adapter for each target platform. Store the refresh token in [Apple Keychain](https://developer.apple.com/documentation/security/keychain-services) on macOS/iOS or [Windows Credential Manager](https://learn.microsoft.com/en-us/windows/win32/SecBP/handling-passwords) on Windows. Use an equivalent OS credential store on other targets.
2. On successful `OnAuthenticate`, save `response.RefreshToken`. At startup, load it and call `SDK.AuthenticateWithRefreshToken(token, callback)`; if absent, ask the broadcaster for a PIN and call `SDK.AuthenticateWithPIN(pin, callback)`.
3. On logout or a rejected refresh token, delete the stored token. Never log it or put it in assets, build settings, or source control.

Unity [documents that `PlayerPrefs` is unencrypted](https://docs.unity3d.com/ScriptReference/PlayerPrefs.html). The SDK does not provide a cross-platform secure-store implementation; add one for every player target you support. If you keep the prefab UI, adapt it to call your code integration's authentication method because its default button calls `MuxyGatewayManager.AuthenticateWithPIN`.

## Publish game metadata

```csharp
private void PublishGameMetadata()
{
    var logo = Resources.Load<Texture2D>("Textures/Gateway/GameLogo");
    var metadata = new GameMetadata
    {
        Name = "My Game",
        Logo = SDK.ConvertTextureToBase64(logo),
        Theme = ""
    };

    gateway.Client.SetGameMetadata(metadata);
}
```

The texture must be readable and use a compatible format such as RGB24 or RGBA32. Keep the encoded PNG below 500 KB.

Next: [Create and handle game actions](unity-gateway-actions.md).

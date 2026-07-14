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
version: v1.0.0-rc
last_verified: '2026-07-14'
review_state: blocked-release
page_type: task-guide
---

# Authenticate and Manage the Gateway Lifecycle

The broadcaster enters a short-lived PIN once. After successful authentication, store the returned refresh token and use it for later sessions.

## Obtain the PIN

1. Install the [Muxy Gateway Twitch Extension](https://www.twitch.tv/ext/i575hs2x9lb3u8hqujtezit03w1740-1.0.0) on the broadcaster's channel.
2. Open the extension's **Configure** page in the Twitch dashboard.
3. Copy the displayed six-character configuration PIN into the game.
4. Submit it within five minutes. Generate a new PIN if it expires.

For evaluation, initialize the SDK with `gateway-testing`. [Request a permanent game ID](https://www.muxy.io/gateway) before distributing the integration.

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

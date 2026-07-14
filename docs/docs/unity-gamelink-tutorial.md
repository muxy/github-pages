---
title: Unity GameLink Tutorial
description: Connect a Unity game to GameLink, authenticate with a broadcaster PIN,
  and run a viewer poll.
slug: unity-gamelink-tutorial
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

# Connect a Unity game with GameLink

This tutorial creates one Unity component that connects to the GameLink sandbox, authenticates a broadcaster with a PIN, and runs a two-option viewer poll.

!!! warning "Unpublished SDK"
    This guide is verified against [`muxy/gamelink-unity` commit `d68d60f`](https://github.com/muxy/gamelink-unity/tree/d68d60fee8f7a5615a126e3aa6013b969be4ea03), not a published SDK release. The repository has no release tag and its package metadata reports `0.1.0`. Its transport imports `UnityEditor` whenever `UNITY_STANDALONE` is defined, so the pinned source does not compile as a standalone player without correction. Keep this page blocked until the Unity SDK owner confirms a supported release, distribution path, and player-build matrix.

## Before you start

You need:

- Unity 2020.3 or newer for editor evaluation. The pinned package contains native libraries for macOS and 64-bit Windows, but binary presence is not a support guarantee and the C# transport currently blocks standalone compilation. No Linux library is included.
- A Twitch Extension client ID registered with Muxy. Follow the [developer quick start](quick-start.md) if you do not have one.
- A broadcaster configuration page that can request a GameLink PIN. The pinned FPS demo contains a [minimal PIN component](https://github.com/muxy/gamelink-unity-fps-demo/blob/0c4975d3a670aefe642dff2429af8fc481443a7f/Extension/src/config/components/GameAuth.vue).

## Getting a GameLink PIN

The broadcaster configuration page requests the PIN after MEDKit has loaded. This helper matches the pinned FPS demo:

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

Display the returned token to the broadcaster, who enters it in the Unity UI. Do not put an extension secret in Unity or viewer-facing JavaScript.

MEDKit 2.4.18 serializes the object passed to `signedRequest()`. The pinned FPS demo passes `JSON.stringify({})`, which is then serialized a second time; the object above is the corrected request body.

## 1. Install the pinned package

In Unity, open **Window → Package Manager**, choose **Add package from git URL**, and enter:

```text
https://github.com/muxy/gamelink-unity.git#d68d60fee8f7a5615a126e3aa6013b969be4ea03
```

Pinning the commit prevents an agent or future build from silently using a different API surface.

## 2. Add the GameLink component

Create `GameLinkExample.cs` under `Assets/Scripts` and paste this complete component:

```csharp
using System;
using System.Collections.Generic;
using MuxyGameLink;
using UnityEngine;
using UnityEngine.UI;

public sealed class GameLinkExample : MonoBehaviour
{
    private const string PollId = "tutorial-gravity";

    [SerializeField] private string clientId = "";
    [SerializeField] private InputField pinInput = null;
    [SerializeField] private Text statusText = null;

    private SDK gameLink;
    private WebsocketTransport transport;
    private SDK.AuthenticationCallback authenticationCallback;
    private uint pollUpdateHandle;
    private bool pollUpdateAttached;

    private async void Start()
    {
        if (string.IsNullOrWhiteSpace(clientId))
        {
            SetStatus("Set the Twitch Extension client ID in the Inspector.");
            return;
        }

        gameLink = new SDK(clientId);
        gameLink.OnDebugMessage(message => Debug.Log($"GameLink: {message}"));

        authenticationCallback = response =>
        {
            Error error = response.GetFirstError();
            if (error != null)
            {
                SetStatus($"Authentication failed: {error.Title} — {error.Detail}");
                return;
            }

            SetStatus(gameLink.IsAuthenticated()
                ? "Authenticated. The poll controls are ready."
                : "Authentication did not complete.");
        };

        pollUpdateHandle = gameLink.OnPollUpdate(response =>
        {
            Error error = response.GetFirstError();
            SetStatus(error == null
                ? $"Votes by option: {string.Join(", ", response.Results)}"
                : $"Poll update failed: {error.Title} — {error.Detail}");
        });
        pollUpdateAttached = true;

        transport = new WebsocketTransport(true);
        SetStatus("Connecting to the GameLink sandbox...");
        bool connected = await transport.OpenAndRunInStage(gameLink, Stage.Sandbox);
        SetStatus(connected ? "Connected. Enter the broadcaster PIN." : "Connection failed.");
    }

    public void AuthenticateWithPin()
    {
        if (gameLink == null || pinInput == null)
        {
            return;
        }

        gameLink.AuthenticateWithPIN(pinInput.text.Trim(), authenticationCallback);
    }

    public void StartPoll()
    {
        if (gameLink == null || !gameLink.IsAuthenticated())
        {
            SetStatus("Authenticate before starting a poll.");
            return;
        }

        gameLink.CreatePoll(
            PollId,
            "Choose the gravity mode",
            new List<string> { "Low", "High" });
        gameLink.SubscribeToPoll(PollId);
        SetStatus("Poll started.");
    }

    public void StopPoll()
    {
        if (gameLink == null || !gameLink.IsAuthenticated())
        {
            return;
        }

        gameLink.GetPoll(PollId, response =>
        {
            Error error = response.GetFirstError();
            if (error != null)
            {
                SetStatus($"Could not read the poll: {error.Title} — {error.Detail}");
                return;
            }

            int totalVotes = 0;
            foreach (int votes in response.Results)
            {
                totalVotes += votes;
            }

            if (totalVotes == 0)
            {
                SetStatus("Poll ended with no votes.");
            }
            else
            {
                int winner = response.GetWinnerIndex();
                SetStatus($"Winning option: {response.Options[winner]}");
            }

            gameLink.UnsubscribeFromPoll(PollId);
            gameLink.DeletePoll(PollId);
        });
    }

    private void Update()
    {
        if (transport != null && gameLink != null)
        {
            transport.Update(gameLink);
        }
    }

    private void OnDestroy()
    {
        if (pollUpdateAttached && gameLink != null)
        {
            gameLink.DetachOnPollUpdate(pollUpdateHandle);
        }

        transport?.Dispose();
    }

    private void SetStatus(string message)
    {
        Debug.Log(message);
        if (statusText != null)
        {
            statusText.text = message;
        }
    }
}
```

The constructor and method signatures above match the pinned [`SDK`](https://github.com/muxy/gamelink-unity/blob/d68d60fee8f7a5615a126e3aa6013b969be4ea03/Runtime/MuxySDK.cs), [`WebsocketTransport`](https://github.com/muxy/gamelink-unity/blob/d68d60fee8f7a5615a126e3aa6013b969be4ea03/Runtime/MuxyWebsocketTransport.cs), and [response types](https://github.com/muxy/gamelink-unity/blob/d68d60fee8f7a5615a126e3aa6013b969be4ea03/Runtime/MuxySDK.Types.cs).

## 3. Wire the scene

1. Create an empty GameObject named `GameLink` and attach `GameLinkExample`.
2. Create a Canvas with a legacy UI `InputField`, three `Button` objects, and a `Text` status label.
3. Assign the client ID, input, and status fields in the Inspector.
4. Connect the buttons to `AuthenticateWithPin`, `StartPoll`, and `StopPoll`.
5. Enter Play mode. Generate a PIN in the extension's broadcaster configuration page, enter it in Unity, and authenticate.
6. Start the poll. A viewer extension can vote with `medkit.vote("tutorial-gravity", 0)` or `medkit.vote("tutorial-gravity", 1)`.

`WebsocketTransport(true)` queues callbacks for Unity's main thread. Calling `transport.Update(gameLink)` every frame is therefore required; omitting it makes authentication and poll callbacks appear to hang.

## 4. Prepare a real integration

- Keep `Stage.Sandbox` during development. Use `Stage.Production` only after the SDK owner confirms the production release and your extension is configured for it.
- Do not claim standalone Windows or macOS support from the bundled native libraries alone. First obtain a package that isolates `UnityEditor` imports to editor builds, then compile and run each player target you plan to ship.
- After PIN authentication, `gameLink.User.RefreshToken` can be passed to `AuthenticateWithRefreshToken` on later launches. Store it in the platform's secure credential store, not plain `PlayerPrefs`.
- Treat poll IDs as application-level identifiers and delete polls when they end.
- Dispose the transport when its owning object is destroyed so editor play mode and application shutdown do not leak a websocket thread.

For a larger source walkthrough, continue to the [Unity FPS demo](unity-fps-demo-code-walkthrough.md).

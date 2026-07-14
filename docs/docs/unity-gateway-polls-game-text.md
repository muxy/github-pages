---
title: Add Gateway Polls and Game Text
description: Start an audience poll and publish current game information through Gateway.
slug: unity-gateway-polls-game-text
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

# Add Gateway Polls and Game Text

## Start a poll

```csharp
private void StartNextLevelPoll()
{
    var poll = new PollConfiguration
    {
        Prompt = "Which level should be next?",
        DurationInSeconds = 30,
        Mode = PollMode.Order
    };

    poll.Options.Add("Ice Cave");
    poll.Options.Add("Desert");
    poll.Options.Add("Jungle");
    poll.OnPollUpdate = update =>
    {
        if (!update.IsFinal)
            return;

        LoadLevel(update.Winner);
    };

    gateway.Client.StartPoll(poll);
}
```

Treat `Winner` as an option index and validate it before indexing your own data. Call `StopPoll()` when the game state invalidates an active poll.

## Publish game text

```csharp
private void PublishGameText(string levelName, string difficulty)
{
    var text = new[]
    {
        new GameText { Label = "Current Level", Value = levelName, Icon = "" },
        new GameText { Label = "Difficulty", Value = difficulty, Icon = "" }
    };

    gateway.Client.SetGameTexts(text);
}
```

Publish only when values change. Avoid sending text every frame.

Next: [Prepare Gateway for production](unity-gateway-production.md).

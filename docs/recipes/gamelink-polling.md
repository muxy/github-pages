---
title: GameLink Polling
description: Create an audience poll and process real-time result updates with GameLink
  C++.
slug: gamelink-polling
product: GameLink Native
audience: game developers
status: current
owner: Native SDK owner
source_of_truth: muxy/gamelink-cpp
version: commit-16c6b97
last_verified: '2026-07-14'
review_state: blocked-release
page_type: task-guide
---

# GameLink Polling

!!! warning "Release verification required"
    This example is pinned to commit `16c6b9796ae02105153ac33482d83ac609398d2e`. Publish and confirm a supported GameLink release before approving this page for production.

This recipe assumes you have authenticated a `gamelink::SDK`, connected its payload queue to a WebSocket, and saved the returned refresh token.

## Register the update handler

```cpp
auto onPollUpdate = [](const gamelink::schema::PollUpdateResponse& response) {
    const auto& poll = response.data.poll;
    std::cout << poll.prompt << "\n";

    for (std::size_t index = 0; index < poll.options.size(); ++index) {
        const int votes = index < response.data.results.size()
            ? response.data.results[index]
            : 0;
        std::cout << poll.options[index] << ": " << votes << "\n";
    }
};
```

## Create and subscribe to a poll

```cpp
gamelink::PollConfiguration configuration;
sdk.RunPoll(
    "favorite-character",
    "Who is your favorite character?",
    configuration,
    {"Ada", "Grace", "Margaret"},
    onPollUpdate,
    onPollUpdate
);
```

Poll IDs are scoped to the current channel. Use a stable, URL-safe identifier and no more than 10 options; the SDK enforces that limit before queuing the request.

## Pump network traffic

Every game tick, send queued SDK payloads and pass received WebSocket frames back to the SDK:

```cpp
sdk.ForeachPayload([&](const gamelink::Payload* payload) {
    websocket.send(payload->Data(), payload->Length());
});

websocket.run();
```

Stop or delete polls when they are no longer active. See [GameLink polling protocol](../reference/ws-polling.md) for the canonical wire messages.

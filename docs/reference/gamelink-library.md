---
title: GameLink C++ Library
description: Integrate the native GameLink C++ SDK, provide a WebSocket transport,
  and authenticate with Muxy.
slug: gamelink-library
product: GameLink Native
audience: developers
status: current
owner: Native SDK owner
source_of_truth: muxy/gamelink-cpp
version: commit-16c6b97
last_verified: '2026-07-14'
review_state: blocked-release
page_type: sdk-reference
---

# GameLink C++ Library

GameLink C++ is a native client for the Muxy GameLink protocol. This reference is pinned to public commit [`16c6b9796ae02105153ac33482d83ac609398d2e`](https://github.com/muxy/gamelink-cpp/tree/16c6b9796ae02105153ac33482d83ac609398d2e). The repository has no public release tag for that revision, so this documentation remains blocked from release.

The public API is in the `gamelink` namespace. It is not the Unity C# API, and it is not limited to a specific game engine.

## Requirements and dependencies

- A C++11 compiler. The upstream CMake project sets `CMAKE_CXX_STANDARD` to `11`.
- The pinned [`gamelink_single.hpp`](https://github.com/muxy/gamelink-cpp/blob/16c6b9796ae02105153ac33482d83ac609398d2e/gamelink_single.hpp) amalgamation, or a header regenerated from the same commit with the `amalgam` CMake target.
- A WebSocket implementation supplied by your application. GameLink serializes and parses protocol messages but does not open, poll, reconnect, or close a socket.
- The C++ standard library. The amalgamation includes a copy of `nlohmann::json`; define `MUXY_NO_JSON_INCLUDE` before inclusion only when your project has already made a compatible `nlohmann::json` implementation available.

Define `MUXY_GAMELINK_SINGLE_IMPL` in exactly one translation unit:

```cpp
// gamelink_impl.cpp
#define MUXY_GAMELINK_SINGLE_IMPL
#include "gamelink_single.hpp"
```

Other translation units include the same file without the implementation macro:

```cpp
#include "gamelink_single.hpp"
```

The default aliases are `gamelink::string = std::string` and `gamelink::lock = std::mutex`. Advanced integrations can replace them with `MUXY_GAMELINK_CUSTOM_STRING_TYPE` and `MUXY_GAMELINK_CUSTOM_LOCK_TYPE`; follow the contracts documented at the top of the pinned header.

## Platform support evidence

The public repository does not declare a supported-platform matrix or publish binaries at this commit. Its automated pipeline builds with Clang on Ubuntu. The source also contains Windows symbol-export handling and macOS x86-64/Arm C-library presets, but those are source-level accommodations, not a published support guarantee. Validate the amalgamation and your transport on every platform you ship.

The sample transport is separate from the SDK and uses libcurl WebSocket APIs. Its dependencies are sample dependencies, not requirements of `gamelink_single.hpp`.

## Minimal integration flow

1. Create a `gamelink::SDK`.
2. Generate a socket host and path with `gamelink::WebsocketConnectionURL`.
3. Add the `wss://` scheme in your transport and connect.
4. Attach callbacks before queuing the request that can trigger them.
5. Authenticate with a PIN on first use or a stored refresh token on later runs.
6. Repeatedly drain outbound payloads and copy or send their bytes before the callback returns.
7. Pass complete inbound text-message bytes to `ReceiveMessage`.
8. After reconnecting the socket, call `HandleReconnect`, then continue draining payloads.

```cpp
#include "gamelink_single.hpp"
gamelink::SDK sdk;

const auto hostAndPath = gamelink::WebsocketConnectionURL(
    clientId,
    gamelink::ConnectionStage::Sandbox);

// Your transport must connect to "wss://" + hostAndPath.
socket.onTextMessage([&](const char* bytes, std::uint32_t length) {
    if (!sdk.ReceiveMessage(bytes, length)) {
        // The message was incomplete or could not be parsed.
    }
});

sdk.OnDebugMessage([](const gamelink::string& message) {
    log(message.c_str());
});

sdk.AuthenticateWithPIN(
    clientId,
    pin,
    [](const gamelink::schema::AuthenticateResponse& response) {
        if (const auto* error = gamelink::FirstError(response)) {
            report(error->number, error->title.c_str(), error->detail.c_str());
            return;
        }

        securelyStore(response.data.refresh);
    });

while (socket.isOpen()) {
    sdk.ForeachPayload([&](const gamelink::Payload* payload) {
        // Payload is destroyed after this callback; send synchronously or copy it.
        socket.sendText(payload->Data(), payload->Length());
    });
    socket.poll();
}
```

`WebsocketConnectionURL` returns a host and path without `ws://` or `wss://`. It returns an empty string for invalid input. Use `ConnectionStage::Sandbox` while developing and `ConnectionStage::Production` only with production credentials.

## Continue with the API reference

- [`gamelink::SDK` lifecycle and request model](sdk-class.md)
- [Authentication and network setup](extension-setup-api.md)
- [Callbacks, subscriptions, polls, broadcasts, and transactions](event-handling.md)
- [State and configuration operations](state-config-fns.md)

## Pinned sources

- [Repository README](https://github.com/muxy/gamelink-cpp/blob/16c6b9796ae02105153ac33482d83ac609398d2e/README.md)
- [Build configuration](https://github.com/muxy/gamelink-cpp/blob/16c6b9796ae02105153ac33482d83ac609398d2e/CMakeLists.txt)
- [SDK header](https://github.com/muxy/gamelink-cpp/blob/16c6b9796ae02105153ac33482d83ac609398d2e/include/gamelink.h)
- [Authentication example](https://github.com/muxy/gamelink-cpp/blob/16c6b9796ae02105153ac33482d83ac609398d2e/examples/01-authenticate/main.cpp)

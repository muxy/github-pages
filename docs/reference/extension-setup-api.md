---
title: GameLink C++ Setup and Authentication
description: Connect a native C++ transport, authenticate with a PIN or refresh token,
  and recover after reconnects.
slug: extension-setup-api
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

# GameLink C++ Setup and Authentication

The native SDK queues authentication messages but leaves all socket work to your application. These signatures and behaviors are pinned to public commit [`16c6b97`](https://github.com/muxy/gamelink-cpp/tree/16c6b9796ae02105153ac33482d83ac609398d2e), which has no public release tag.

## Connect the transport

```cpp
gamelink::SDK sdk;
const gamelink::string hostAndPath = gamelink::WebsocketConnectionURL(
    clientId,
    gamelink::ConnectionStage::Sandbox);

if (hostAndPath.size() == 0) {
    fail("Invalid GameLink connection parameters");
}

socket.connect("wss://" + std::string(hostAndPath.c_str()));
socket.onTextMessage([&](const char* bytes, std::uint32_t length) {
    sdk.ReceiveMessage(bytes, length);
});
```

`WebsocketConnectionURL` returns a host and path without a protocol prefix. The pinned implementation selects `gamelink.sandbox.muxy.io` for `ConnectionStage::Sandbox` and `gamelink.muxy.io` for `ConnectionStage::Production`. Use TLS (`wss://`) outside a deliberately local test transport.

Keep pumping both directions for the life of the connection:

```cpp
sdk.ForeachPayload([&](const gamelink::Payload* payload) {
    socket.sendText(payload->Data(), payload->Length());
});

socket.poll();
```

The payload pointer and its data expire when the `ForeachPayload` callback returns. Copy the bytes if `sendText` is asynchronous.

## Authenticate for the first time

Obtain the broadcaster-entered PIN through your extension setup flow, then use a one-shot callback:

```cpp
const gamelink::RequestId request = sdk.AuthenticateWithPIN(
    clientId,
    pin,
    [](const gamelink::schema::AuthenticateResponse& response) {
        if (const auto* error = gamelink::FirstError(response)) {
            report(error->number, error->title.c_str(), error->detail.c_str());
            return;
        }

        securelyStore(response.data.refresh);
        useExpiringJwt(response.data.jwt);
    });
```

The successful `AuthenticateResponse` data contains `jwt`, `refresh`, `twitch_name`, and `twitch_id`. Persist the refresh token as a secret. The JWT expires; do not substitute it for the refresh token on a later run.

If your integration requires a Twitch game ID, use the corresponding `AuthenticateWithGameIDAndPIN` overload.

## Authenticate on later runs

```cpp
sdk.AuthenticateWithRefreshToken(
    clientId,
    storedRefreshToken,
    [](const gamelink::schema::AuthenticateResponse& response) {
        if (response.errors.empty()) {
            securelyStore(response.data.refresh);
        }
    });
```

Use `AuthenticateWithGameIDAndRefreshToken` when the initial flow included a game ID. Each authentication method also has an overload without a callback and a function-pointer-plus-user-data overload.

| C++ API | Result |
| --- | --- |
| `AuthenticateWithPIN(clientId, pin, callback)` | Queue PIN authentication and invoke a one-shot callback for its response. |
| `AuthenticateWithGameIDAndPIN(clientId, gameId, pin, callback)` | Queue PIN authentication scoped with a Twitch game ID. |
| `AuthenticateWithRefreshToken(clientId, refresh, callback)` | Queue repeat authentication with a stored refresh token. |
| `AuthenticateWithGameIDAndRefreshToken(clientId, gameId, refresh, callback)` | Queue repeat authentication with the same game-ID scope. |
| `OnAuthenticate().Add(callback)` | Register a persistent callback for all authentication responses; no subscription call is required. |
| `IsAuthenticated()` | Return `true` after a successful authentication response is processed. |
| `GetUser()` | Return the local `schema::User`, or `nullptr`; its getters expose JWT, refresh token, Twitch name, and Twitch ID. |
| `GetClientId()` | Return the client ID most recently supplied to an authentication call. |

Attach `OnAuthenticate` before calling an overload without a one-shot callback:

```cpp
const auto handle = sdk.OnAuthenticate().Add(
    [](const gamelink::schema::AuthenticateResponse& response) {
        // Handles every authentication response until removed.
    });

sdk.AuthenticateWithPIN(clientId, pin);
// Later: sdk.OnAuthenticate().Remove(handle);
```

## Reconnect safely

After your transport has established a replacement socket, call:

```cpp
sdk.HandleReconnect();
```

When the SDK has a refresh token from an earlier successful authentication, `HandleReconnect` places refresh authentication at the front of the outbound queue and replays subscriptions tracked for SKUs, polls, configuration, state, datastream, and matchmaking. Continue draining `ForeachPayload`; the method itself does not reconnect or send.

If no successful refresh-bearing authentication has occurred, `HandleReconnect` queues nothing. Start a normal authentication flow instead.

## Sign out and errors

At the pinned commit, `Deauthenticate()` deletes the local user and returns `ANY_REQUEST_ID`; it does not notify the server, clear the refresh token retained inside that `SDK` instance, or clear stored credentials in your application. For a complete sign-out, delete your persisted refresh token, close the socket, and destroy the SDK instance instead of reconnecting it.

Always inspect `response.errors`. Each `schema::Error` has `number`, `title`, and `detail`. `OnDebugMessage` can expose protocol send/receive logs and local validation messages, but it is not a server-error callback and may contain sensitive payload data.

## Pinned sources

- [Authentication declarations](https://github.com/muxy/gamelink-cpp/blob/16c6b9796ae02105153ac33482d83ac609398d2e/include/gamelink.h#L709-L877)
- [Authentication response and user schema](https://github.com/muxy/gamelink-cpp/blob/16c6b9796ae02105153ac33482d83ac609398d2e/schema/authentication.h)
- [Connection URL, receive loop, and reconnect behavior](https://github.com/muxy/gamelink-cpp/blob/16c6b9796ae02105153ac33482d83ac609398d2e/src/gamelink.cpp)
- [Upstream authentication example](https://github.com/muxy/gamelink-cpp/blob/16c6b9796ae02105153ac33482d83ac609398d2e/examples/01-authenticate/main.cpp)

---
title: GameLink C++ SDK Class
description: Understand the GameLink C++ request queue, transport lifecycle, callback
  dispatch, and error model.
slug: sdk-class
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

# GameLink C++ SDK Class

`gamelink::SDK` owns GameLink protocol state, queued outbound messages, authentication state, subscriptions, and callbacks. It does not own a network connection. This page describes public commit [`16c6b97`](https://github.com/muxy/gamelink-cpp/tree/16c6b9796ae02105153ac33482d83ac609398d2e), for which no public release tag exists.

## Construction and ownership

```cpp
gamelink::SDK sdk;
```

`SDK()` takes no client ID. Supply the client ID to an authentication method. `SDK` is neither copyable nor movable, and pointers returned by `GetUser()` or callback arguments must not outlive their documented owner or callback.

Most SDK methods are intended to be thread-safe. `ReceiveMessage` is the important exception: call it from one thread only, never recursively. It invokes callbacks synchronously on that same thread.

## Core network API

| C++ signature | Purpose |
| --- | --- |
| `string WebsocketConnectionURL(const string&, ConnectionStage)` | Return the GameLink host and path, without a WebSocket scheme. |
| `bool SDK::ReceiveMessage(const char*, uint32_t)` | Parse inbound bytes and synchronously dispatch matching callbacks. |
| `bool SDK::HasPayloads() const` | Report whether an outbound payload can currently be drained. |
| `void SDK::ForeachPayload(const Callable&)` | Drain all currently sendable payloads. May invoke the callable zero times. |
| `void SDK::HandleReconnect()` | Queue refresh-token authentication first and replay tracked subscriptions after a socket reconnect. |
| `bool SDK::IsAuthenticated() const` | Report whether a successful authentication response has created a local user. |
| `const schema::User* SDK::GetUser() const` | Return the current user, or `nullptr` when unauthenticated. |
| `const char* SDK::GetClientId() const` | Return the client ID last supplied to authentication. |
| `RequestId SDK::Deauthenticate()` | Clear the local user at this commit; it does not send a deauthentication message. |

`ForeachPayload` removes and destroys each `Payload` after invoking your callable. Use `Payload::Data()` and `Payload::Length()` only during that call. A transport that queues work for later must copy the bytes.

`ReceiveMessage` can buffer an incomplete JSON message up to 4 MiB and returns `false` until parsing succeeds. It also returns `false` for malformed or unsupported messages. Frame complete GameLink text messages whenever your transport permits it.

## Request IDs and ordering

Asynchronous methods generally return `gamelink::RequestId`, an unsigned 16-bit request identifier echoed in `response.meta.request_id`.

- `gamelink::ANY_REQUEST_ID` (`UINT16_MAX`) means there is no specific request ID. Some no-op or rejected subscription calls return it.
- `gamelink::REJECTED_REQUEST_ID` (`UINT16_MAX - 1`) is returned by some local validation failures, including invalid poll limits.
- A normal ID means the request was queued, not that the server accepted it.

Use a response callback or event to determine server success. To serialize dependent requests, insert a barrier after the first request:

```cpp
const gamelink::RequestId removed = sdk.DeletePoll("daily-vote");
if (removed != gamelink::ANY_REQUEST_ID &&
    removed != gamelink::REJECTED_REQUEST_ID) {
    sdk.WaitForResponse(removed);
    sdk.CreatePoll("daily-vote", "Choose a route", {"North", "South"});
}
```

`WaitForResponse` blocks later queued payloads until that ID is observed. Never pass an invalid ID: the pinned implementation does not validate it, and the outbound queue can remain blocked indefinitely.

## Responses and errors

Response types derive from `gamelink::schema::ReceiveEnvelope<T>`. They expose:

- `meta.request_id`, `meta.action`, `meta.target`, and `meta.timestamp`;
- `data`, whose type depends on the operation;
- `errors`, a vector of `schema::Error` values with `number`, `title`, and `detail`.

Treat a non-empty `errors` vector as failure before reading operation-specific data:

```cpp
sdk.GetState(
    gamelink::StateTarget::Channel,
    [](const gamelink::schema::GetStateResponse<nlohmann::json>& response) {
        if (const auto* error = gamelink::FirstError(response)) {
            report(error->number, error->title.c_str(), error->detail.c_str());
            return;
        }

        useState(response.data.state);
    });
```

`OnDebugMessage` is diagnostic output, not a replacement for response error handling. Registering it again replaces the previous debug callback; `DetachOnDebugMessage()` removes it.

## Callback lifetime and removal

Persistent SDK events return `Event<Response>&`. `Add` returns a `uint32_t` handle, and `Remove(handle)` must be called on the same event object. `AddUnique(name, callback)` replaces an existing callback with that name; `RemoveByName(name)` removes it.

```cpp
auto& event = sdk.OnPollUpdate();
const std::uint32_t handle = event.Add(
    [](const gamelink::schema::PollUpdateResponse& response) {
        // response is borrowed and valid only for this call.
    });

event.Remove(handle);
```

Callbacks execute inside `ReceiveMessage`. Copy any data needed by another thread or a deferred task before returning. Do not call `ReceiveMessage` recursively from a callback.

## API groups

- [Authentication and socket lifecycle](extension-setup-api.md)
- [Events, datastream, polls, and purchases](event-handling.md)
- [State and configuration](state-config-fns.md)

The header also exposes drops, matchmaking, matches, and game metadata APIs. Those APIs are outside the scope of these migrated native-reference pages; consult the pinned header before use.

## Pinned sources

- [`SDK`, `Event`, `Payload`, and URL declarations](https://github.com/muxy/gamelink-cpp/blob/16c6b9796ae02105153ac33482d83ac609398d2e/include/gamelink.h)
- [Network dispatch and reconnect implementation](https://github.com/muxy/gamelink-cpp/blob/16c6b9796ae02105153ac33482d83ac609398d2e/src/gamelink.cpp)
- [Response envelope and error schema](https://github.com/muxy/gamelink-cpp/blob/16c6b9796ae02105153ac33482d83ac609398d2e/schema/envelope.h)

---
title: GameLink C++ Events and Subscriptions
description: Register C++ callbacks for authentication, state, configuration, datastream,
  polls, and transactions.
slug: event-handling
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

# GameLink C++ Events and Subscriptions

GameLink events are callback collections owned by `gamelink::SDK`. This reference is pinned to public commit [`16c6b97`](https://github.com/muxy/gamelink-cpp/tree/16c6b9796ae02105153ac33482d83ac609398d2e), which has no public release tag.

## Callback model

`Event<T>::Add` registers a persistent `std::function<void(const T&)>` and returns a `uint32_t` handle. Remove the callback through the same event:

```cpp
auto& updates = sdk.OnStateUpdate();
const std::uint32_t handle = updates.Add(
    [](const gamelink::schema::SubscribeStateUpdateResponse<nlohmann::json>& response) {
        if (const auto* error = gamelink::FirstError(response)) {
            report(error->number, error->title.c_str(), error->detail.c_str());
            return;
        }

        useState(response.data.state);
    });

sdk.SubscribeToStateUpdates(gamelink::StateTarget::Channel);

// When the listener is no longer needed:
sdk.UnsubscribeFromStateUpdates(gamelink::StateTarget::Channel);
updates.Remove(handle);
```

`AddUnique(name, callback)` replaces any callback with the same name. `RemoveByName(name)` removes a named callback.

Callbacks run synchronously in the thread calling `SDK::ReceiveMessage`. Response references and their nested data are borrowed and valid only until the callback returns. Copy data before deferring work, and never invoke `ReceiveMessage` recursively.

Most event streams require both a local callback and a server subscription:

| Event accessor and response type | Required request |
| --- | --- |
| `OnAuthenticate()` → `schema::AuthenticateResponse` | None; authentication responses dispatch automatically. |
| `OnStateUpdate()` → `schema::SubscribeStateUpdateResponse<nlohmann::json>` | `SubscribeToStateUpdates(StateTarget)` |
| `OnConfigUpdate()` → `schema::ConfigUpdateResponse` | `SubscribeToConfigurationChanges(ConfigTarget)` |
| `OnDatastreamUpdate()` → `schema::DatastreamUpdate` | `SubscribeToDatastream()` |
| `OnPollUpdate()` → `schema::PollUpdateResponse` | `SubscribeToPoll(pollId)` |
| `OnTransaction()` → `schema::TransactionResponse` | `SubscribeToSKU(sku)` or `SubscribeToAllPurchases()` |

Duplicate subscription calls are suppressed by the pinned SDK and generally return `ANY_REQUEST_ID` while emitting a debug message.

## Debug messages and response errors

`OnDebugMessage` is a single diagnostic callback, not an `Event<T>`:

```cpp
sdk.OnDebugMessage([](const gamelink::string& message) {
    log(message.c_str());
});

// Replaces the existing debug callback if called again.
sdk.DetachOnDebugMessage();
```

With a debug callback attached, the pinned implementation logs complete outbound and inbound protocol payloads. Treat those logs as potentially sensitive. Server failures remain in each response envelope's `errors` vector; check `FirstError(response)` before reading `data`.

## Datastream events

The datastream delivers batches of events. Each `schema::DatastreamEvent` has an arbitrary JSON `event` and a Unix-seconds `timestamp`.

```cpp
sdk.OnDatastreamUpdate().Add(
    [](const gamelink::schema::DatastreamUpdate& response) {
        if (!response.errors.empty()) {
            return;
        }

        for (const auto& item : response.data.events) {
            consume(item.event, item.timestamp);
        }
    });

sdk.SubscribeToDatastream();
```

Broadcasts are outbound messages to viewers on the channel using the extension. `topic` is the frontend filter key.

```cpp
nlohmann::json message = {{"kind", "round-start"}, {"round", 4}};
sdk.SendBroadcast("game-events", message);
```

The overloads are:

```cpp
template<typename T>
gamelink::RequestId SendBroadcast(const gamelink::string& topic, const T& value);

gamelink::RequestId SendBroadcast(
    const gamelink::string& topic,
    const nlohmann::json& object);

gamelink::RequestId SendBroadcast(const gamelink::string& topic);
```

The serialized message must be under 8 KiB. The JSON overload requires an object, not a primitive or array. Stop delivery with `UnsubscribeFromDatastream()`.

## State and configuration updates

Register one event callback for each update family, then subscribe separately for each target you need:

```cpp
sdk.OnConfigUpdate().Add(
    [](const gamelink::schema::ConfigUpdateResponse& response) {
        if (response.errors.empty()) {
            applyConfig(response.data.config, response.data.topicId);
        }
    });

sdk.SubscribeToConfigurationChanges(gamelink::ConfigTarget::Channel);
sdk.SubscribeToConfigurationChanges(gamelink::ConfigTarget::Extension);
```

All callbacks attached to an event receive all updates dispatched to that event. Inspect response metadata and data fields when one callback needs to filter a particular target. See [state and configuration operations](state-config-fns.md) for read and write APIs.

## Polls

The core poll API uses C++ containers and callbacks:

```cpp
gamelink::RequestId CreatePoll(
    const gamelink::string& pollId,
    const gamelink::string& prompt,
    const std::vector<gamelink::string>& options);

gamelink::RequestId GetPoll(
    const gamelink::string& pollId,
    std::function<void(const gamelink::schema::GetPollResponse&)> callback);

gamelink::RequestId SubscribeToPoll(const gamelink::string& pollId);
gamelink::RequestId UnsubscribeFromPoll(const gamelink::string& pollId);
gamelink::RequestId DeletePoll(const gamelink::string& pollId);
```

Attach `OnPollUpdate()` before subscribing. Every callback receives updates for every subscribed poll, so filter on `response.data.poll.pollId` when necessary. `GetPoll` has a one-shot callback overload and returns results in `response.data.results` alongside the poll, mean, sum, and count.

The SDK also provides `CreatePollWithConfiguration`, `RunPoll`, `StopPoll`, and `SetPollDisabled`. `RunPoll` coordinates delete/create/subscribe behavior and accepts update and finish callbacks. Use `StopPoll`, not `DeletePoll`, when you need a `RunPoll` finish callback.

Local validation limits at the pinned commit are 256 characters for the prompt, 10 options, and 128 characters per option. A local limit failure returns `REJECTED_REQUEST_ID` and emits a debug message.

## Purchase transactions

```cpp
auto& purchases = sdk.OnTransaction();
purchases.Add([](const gamelink::schema::TransactionResponse& response) {
    if (const auto* error = gamelink::FirstError(response)) {
        report(error->number, error->title.c_str(), error->detail.c_str());
        return;
    }

    const auto& transaction = response.data;
    grantOnce(transaction.muxyId, transaction.sku, transaction.userId);
});

sdk.SubscribeToSKU("coins-100");
```

`OnTransaction` receives all subscribed SKUs; filter `response.data.sku` inside the callback. Available operations are:

| C++ API | Purpose |
| --- | --- |
| `SubscribeToSKU(sku)` / `UnsubscribeFromSKU(sku)` | Manage one SKU subscription. |
| `SubscribeToAllPurchases()` / `UnsubscribeFromAllPurchases()` | Manage the all-purchases subscription. |
| `GetOutstandingTransactions(sku, callback)` | Return up to 10 unvalidated transactions, oldest first; use `"*"` for all SKUs. |
| `ValidateTransaction(txid, details)` | Mark a Muxy transaction ID as validated. |
| `RefundTransactionByID(txid, userId)` | Refund by Muxy transaction ID and user ID. |
| `RefundTransactionBySKU(sku, userId)` | Refund by SKU and user ID. |

Grant and durably record an entitlement before validation, and make grants idempotent by `muxyId`.

## Pinned sources

- [`Event<T>` and SDK event declarations](https://github.com/muxy/gamelink-cpp/blob/16c6b9796ae02105153ac33482d83ac609398d2e/include/gamelink.h)
- [Datastream schema](https://github.com/muxy/gamelink-cpp/blob/16c6b9796ae02105153ac33482d83ac609398d2e/schema/datastream.h)
- [Poll schema](https://github.com/muxy/gamelink-cpp/blob/16c6b9796ae02105153ac33482d83ac609398d2e/schema/poll.h)
- [Purchase schema](https://github.com/muxy/gamelink-cpp/blob/16c6b9796ae02105153ac33482d83ac609398d2e/schema/purchase.h)
- [Inbound event dispatch](https://github.com/muxy/gamelink-cpp/blob/16c6b9796ae02105153ac33482d83ac609398d2e/src/gamelink.cpp)

---
title: GameLink C++ State and Configuration
description: Read, replace, patch, and subscribe to GameLink state and configuration
  from C++.
slug: state-config-fns
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

# GameLink C++ State and Configuration

GameLink stores state and configuration as JSON objects. The APIs below are pinned to public commit [`16c6b97`](https://github.com/muxy/gamelink-cpp/tree/16c6b9796ae02105153ac33482d83ac609398d2e), which has no public release tag.

## Targets and write scope

Use the strongly typed C++ enums, not C# string constants:

```cpp
enum class gamelink::StateTarget { Channel, Extension };
enum class gamelink::ConfigTarget { Channel, Extension, Combined };
enum class gamelink::Operation { Add, Remove, Replace, Copy, Move, Test };
```

The pinned API is asymmetric:

| Store | Read | Replace or clear | Patch | Subscribe |
| --- | --- | --- | --- | --- |
| Channel state | `GetState(Channel, callback)` | `SetState(Channel, value)`, `ClearState(Channel)` | `UpdateState*(Channel, ...)` | `SubscribeToStateUpdates(Channel)` |
| Extension state | `GetState(Extension, callback)` | `SetState(Extension, value)`, `ClearState(Extension)` | `UpdateState*(Extension, ...)` | `SubscribeToStateUpdates(Extension)` |
| Channel config | `GetConfig(Channel, callback)` | `SetChannelConfig(value)` | `UpdateChannelConfig*(...)` | `SubscribeToConfigurationChanges(Channel)` |
| Extension config | `GetConfig(Extension, callback)` | No public writer | No public patch helper | `SubscribeToConfigurationChanges(Extension)` |
| Combined config | `GetCombinedConfig(callback)` | No public writer | No public patch helper | `SubscribeToConfigurationChanges(Combined)` is representable, but combined is primarily a read target. |

`SetChannelConfig` and every `UpdateChannelConfig*` method write channel configuration only. There is no `SetExtensionConfig` in the pinned public header.

The API permits an extension-state subscription, but the pinned `ReceiveMessage` dispatcher has an explicit state-update branch only for response metadata whose target is `"channel"`. Treat extension-state event delivery as unverified in this revision and validate it against the service before depending on it.

## Read state

Use the callback overload so the response is observable:

```cpp
sdk.GetState(
    gamelink::StateTarget::Channel,
    [](const gamelink::schema::GetStateResponse<nlohmann::json>& response) {
        if (const auto* error = gamelink::FirstError(response)) {
            report(error->number, error->title.c_str(), error->detail.c_str());
            return;
        }

        const nlohmann::json& state = response.data.state;
        useState(state);
    });
```

The header also has `GetState(StateTarget)` without a callback, but the pinned SDK exposes no public `OnGetState` event. Prefer the callback overload.

## Replace or clear state

The complete value must be a JSON object, not an array or primitive:

```cpp
nlohmann::json initialState = {
    {"name", "Judy"},
    {"health", 30},
    {"details", {"val1", "val2", "val3"}}
};

sdk.SetState(gamelink::StateTarget::Channel, initialState);
sdk.ClearState(gamelink::StateTarget::Extension); // Replaces it with {}.
```

Serializable C++ types can be passed to the templated `SetState` overload when they have compatible `nlohmann::json` conversion, including types marked with the SDK's `MUXY_GAMELINK_SERIALIZE*` macros.

## Patch state

Patch paths use JSON Pointer syntax. The typed helpers queue one operation:

```cpp
sdk.UpdateStateWithString(
    gamelink::StateTarget::Channel,
    gamelink::Operation::Replace,
    "/name",
    "Judy B");

sdk.UpdateStateWithInteger(
    gamelink::StateTarget::Channel,
    gamelink::Operation::Replace,
    "/health",
    100);

sdk.UpdateStateWithString(
    gamelink::StateTarget::Channel,
    gamelink::Operation::Replace,
    "/details/0",
    "first-value");
```

State helpers are available for object, array, integer, double, Boolean, string, JSON literal, null, and `nlohmann::json` values. `UpdateState` accepts a contiguous range of `schema::PatchOperation`; `PatchList` builds multiple operations and `UpdateStateWithPatchList` sends them in one request.

```cpp
gamelink::PatchList patches(2);
patches.UpdateStateWithInteger(gamelink::Operation::Replace, "/health", 100);
patches.UpdateStateWithBoolean(gamelink::Operation::Add, "/ready", true);

sdk.UpdateStateWithPatchList(gamelink::StateTarget::Channel, patches);
```

Pass only a valid `Operation` enum value. The typed helper implementation indexes an operation-name array and does not validate a casted out-of-range value.

The enum includes `Copy` and `Move`, but the pinned `schema::PatchOperation` contains only `operation`, `path`, and `value`; it has no standard JSON Patch `from` member. Do not assume this revision can express RFC 6902 copy or move operations without server-specific confirmation.

## Read configuration

```cpp
sdk.GetConfig(
    gamelink::ConfigTarget::Channel,
    [](const gamelink::schema::GetConfigResponse& response) {
        if (response.errors.empty()) {
            useConfig(response.data.config, response.data.configId);
        }
    });

sdk.GetCombinedConfig(
    [](const gamelink::schema::GetCombinedConfigResponse& response) {
        if (response.errors.empty()) {
            useMergedInputs(
                response.data.config.channel,
                response.data.config.extension);
        }
    });
```

`GetConfig` accepts `ConfigTarget::Channel` or `ConfigTarget::Extension`. Use `GetCombinedConfig` for the combined response type.

## Replace or patch channel configuration

`SetChannelConfig` replaces the complete channel configuration object:

```cpp
nlohmann::json config = {
    {"difficulty", "hard"},
    {"roundSeconds", 90}
};

sdk.SetChannelConfig(config);
```

Patch helpers mirror state helpers but omit a target because they always write channel configuration:

```cpp
sdk.UpdateChannelConfigWithInteger(
    gamelink::Operation::Replace,
    "/roundSeconds",
    120);

sdk.UpdateChannelConfigWithJson(
    gamelink::Operation::Add,
    "/allowedMaps",
    nlohmann::json::array({"forest", "desert"}));
```

At this pinned commit, `UpdateChannelConfigWithArray` fails to advance its destination index while building JSON. Use `UpdateChannelConfigWithJson` for arrays until a tagged revision fixes that implementation.

## Subscribe to updates

Callbacks and subscriptions are separate:

```cpp
auto& stateEvent = sdk.OnStateUpdate();
const auto stateHandle = stateEvent.Add(
    [](const gamelink::schema::SubscribeStateUpdateResponse<nlohmann::json>& response) {
        if (response.errors.empty()) {
            useState(response.data.state);
        }
    });

sdk.SubscribeToStateUpdates(gamelink::StateTarget::Channel);

auto& configEvent = sdk.OnConfigUpdate();
const auto configHandle = configEvent.Add(
    [](const gamelink::schema::ConfigUpdateResponse& response) {
        if (response.errors.empty()) {
            useConfig(response.data.config, response.data.topicId);
        }
    });

sdk.SubscribeToConfigurationChanges(gamelink::ConfigTarget::Channel);
```

Call the matching unsubscribe method to update server-side delivery, and remove the local callback handle when the listener is no longer needed. See [events and subscriptions](event-handling.md) for callback lifetime rules.

## Pinned sources

- [State and configuration SDK declarations](https://github.com/muxy/gamelink-cpp/blob/16c6b9796ae02105153ac33482d83ac609398d2e/include/gamelink.h#L1178-L1533)
- [Target and operation enums](https://github.com/muxy/gamelink-cpp/blob/16c6b9796ae02105153ac33482d83ac609398d2e/schema/consts.h)
- [State schema](https://github.com/muxy/gamelink-cpp/blob/16c6b9796ae02105153ac33482d83ac609398d2e/schema/state.h)
- [Configuration schema](https://github.com/muxy/gamelink-cpp/blob/16c6b9796ae02105153ac33482d83ac609398d2e/schema/game_config.h)
- [State implementation](https://github.com/muxy/gamelink-cpp/blob/16c6b9796ae02105153ac33482d83ac609398d2e/src/gamelink_state.cpp)
- [Configuration implementation](https://github.com/muxy/gamelink-cpp/blob/16c6b9796ae02105153ac33482d83ac609398d2e/src/gamelink_config.cpp)

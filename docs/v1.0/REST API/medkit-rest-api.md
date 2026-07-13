---
title: "Using the MEDKit REST API"
slug: "medkit-rest-api"
excerpt: "Overview of available functionality."
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Tue Sep 14 2021 15:42:34 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Feb 01 2022 17:06:05 GMT+0000 (Coordinated Universal Time)"
---
The MEDKit REST API gives users of Twitch extensions direct access to persistent storage and viewer data endpoints. It can be accessed directly via HTTP requests, or by using the [MEDKit JavaScript library](../../v1.0/Getting Started with MEDKit/getting-started-with-medkit.md).

The REST API has two base URLs:

| Base URL              | Description                                                                   |
| :-------------------- | :---------------------------------------------------------------------------- |
| `api.muxy.io`         | Production environment. Your released extension will only work with this API. |
| `sandbox.api.muxy.io` | Sandbox environment with relaxed authentication and limited data persistence. |

These are completely separate environments that don’t share information and have different levels of security. Sandbox is used for development and testing only, but is inaccessible by production viewers.

Sandbox does not check the authentication of users to allow developers to simulate viewer/broadcaster/admin combinations. Similarly it does not verify transactions or store state for very long.

All endpoints are versioned by path; for example `/v1/e/authenticate`.

> 👍 Authentication
> 
> All calls must provide a valid Client ID. This is a Twitch Extension Client ID that has been registered with Muxy.
> 
> See [Register your Twitch extension with Muxy](https://docs.muxy.io/docs/quick-start#register-your-extension-with-muxy).

# Authorization

User authorization is done by passing a [JSON Web Token](https://jwt.io/) in the **`Authorization`** header.

The **`Authorization`** header is required for all API requests except:

- The [`authtoken`](../../v1.0/REST API/dev-auth.md) endpoint,  which you use to obtain a JWT for the `sandbox` development environment. This token is not accepted in the production environment.
- The [`pin`](../../v1.0/REST API/initialization-api/pin-auth.md)  endpoint. This endpoint is an alternative way to authenticate a user by passing a Client ID and 6-character PIN that has been generated previously. The response includes a JWT to use for subsequent API calls.

The value  of the **`Authorization`** header is a space-separated Client ID/JWT pair of the form `Authorization: 12345 eyJhbGciOiJIU...`

For example:

```shell Authorization header
curl -X GET https://sandbox.api.muxy.io/v1/e/viewer_state \
  -H "Authorization: 12345 eyJhbGciOiJIU"
```

# Endpoint summary

> 📘 Endpoint paths
> 
> All endpoints below are on the main `/e/<endpoint>` service unless noted otherwise.

# Data Storage and Retrieval

The REST API allows you to define, store, and retrieve data for general extension configuration and for real-time extension usage.

## [Configuration API](../../v1.0/REST API/config-api.md)

This data store is available in two scopes, extension-wide and channel-wide. 

- Each config store is defined by a single JSON object containing key-value pairs. The keys are developer-defined. Use these endpoints to set, modify, and retrieve configuration keys and values.  
- Use a GET request to `all_config` to retrieve the current content of all configuration stores.
- The individual config-store endpoints support GET, POST, and PATCH operations.

| Configuration Data Endpoint | Usage                                                                                    |
| :-------------------------- | :--------------------------------------------------------------------------------------- |
| `all_config`                | Retrieves all configuration data in a single call.                                       |
| `extension_config`          | Maintains and reports per-extension configuration across channels.                       |
| `channel_config`            | Maintains and reports per-channel configuration for all extensions running in a channel. |

## [State API](../../v1.0/REST API/rest-state-api.md)

This data store is available with  four different scopes.

- Each state store is defined by a single JSON object containing key-value pairs. The keys are developer-defined. Use these endpoints to set, modify, and retrieve state keys and values.  
- Use a GET request to `all_state` to retrieve the current content of all state stores.
- The individual state-store endpoints support GET, POST, and PATCH operations.

| State Data Endpoint      | Usage                                                                                        |
| :----------------------- | :------------------------------------------------------------------------------------------- |
| `all_state`              | Retrieves all four state stores in a single call.                                            |
| `extension_state`        | Maintains and reports per-extension state information.                                       |
| `viewer_state`           | Maintains and reports per-viewer state information.                                          |
| `extension_viewer_state` | Maintains and reports per-viewer state information for each extension.                       |
| `channel_state`          | Maintains and reports per-channel state information for all extensions running in a channel. |

## [Engagement Tools API](../../v1.0/REST API/aggregation-api.md)

The MEDKit REST API supports a variety of tools and techniques for encouraging viewer interaction and engagement, from simple aggregation of viewer data to support for the creation of interactive events. 

- _Accumulating_ data that users provide is the simplest form of aggregation. 
- A _ranking_ service collects answers to open-ended questions, and counts matching responses.
- A _polling_ service helps you create and manage viewer polls, collect viewer votes, and work with voting results.
- The  _trivia_ and _game codes_ services help you implement a sophisticated voting-and-reward system.



| Endpoint | Usage |
| --- | --- |
| `accumulate` | Collect user input for developer-defined data. |
| `rank` | Create open-ended questions, collect user answers, and get statistics on popular answers. |
| `vote`  <br>`vote/vote_logs` | Create and manage polls, cast and collect users' votes, get voting results and logs. |




## Communication API

Additional endpoints support administrative services, including back-channel and server-to-server communication.



| Endpoint | Usage |
| --- | --- |
| [Broadcast Messaging](../../v1.0/REST API/communication-api/broadcast.md)  <br>`broadcast`  <br>`broadcast_extension`  <br>`whisper_self` | Broadcast messages to viewers on a per-channel or per-extension basis.  <br>  <br>This service also enables server-to-server and back-channel communication. |



# Using the MEDKit REST API

Overview of available functionality.

The MEDKit REST API gives users of Twitch extensions direct access to persistent storage and viewer data endpoints. It can be accessed directly via HTTP requests, or by using the [MEDKit JavaScript library](https://docs.muxy.io/docs/getting-started-with-medkit).

The REST API has two base URLs:

[block:parameters]
{
  "data": {
    "h-0": "Base URL",
    "h-1": "Description",
    "0-0": "`api.muxy.io`",
    "0-1": "Production environment. Your released extension will only work with this API.",
    "1-0": "`sandbox.api.muxy.io`",
    "1-1": "Sandbox environment with relaxed authentication and limited data persistence."
  },
  "cols": 2,
  "rows": 2
}
[/block]

These are completely separate environments that don’t share information and have different levels of security. Sandbox is used for development and testing only, but is inaccessible by production viewers.

Sandbox does not check the authentication of users to allow developers to simulate viewer/broadcaster/admin combinations. Similarly it does not verify transactions or store state for very long.

All endpoints are versioned by path; for example `/v1/e/authenticate`.

[block:callout]
{
  "type": "success",
  "body": "All calls must provide a valid Client ID. This is a Twitch Extension Client ID that has been registered with Muxy.\n\nSee [Register your Twitch extension with Muxy](https://docs.muxy.io/docs/quick-start#register-your-extension-with-muxy).",
  "title": "Authentication"
}
[/block]

# Authorization

User authorization is done by passing a [JSON Web Token](https://jwt.io/) in the **`Authorization`** header.

The **`Authorization`** header is required for all API requests except:

* The [`authtoken`](https://docs.muxy.io/reference/dev-auth) endpoint,  which you use to obtain a JWT for the `sandbox` development environment. This token is not accepted in the production environment.
* The [`pin`](https://docs.muxy.io/reference/pin-auth)  endpoint. This endpoint is an alternative way to authenticate a user by passing a Client ID and 6-character PIN that has been generated previously. The response includes a JWT to use for subsequent API calls.

The value  of the **`Authorization`** header is a space-separated Client ID/JWT pair of the form `Authorization: 12345 eyJhbGciOiJIU...`

For example:

[block:code]
{
  "codes": [
    {
      "code": "curl -X GET https://sandbox.api.muxy.io/v1/e/viewer_state \\\n  -H \"Authorization: 12345 eyJhbGciOiJIU\"",
      "language": "shell",
      "name": "Authorization header"
    }
  ]
}
[/block]

# Endpoint summary

[block:callout]
{
  "type": "info",
  "title": "Endpoint paths",
  "body": "All endpoints below are on the main `/e/<endpoint>` service unless noted otherwise."
}
[/block]

# Data Storage and Retrieval

The REST API allows you to define, store, and retrieve data for general extension configuration and for real-time extension usage.

## [Configuration API](https://docs.muxy.io/reference/config-api)

This data store is available in two scopes, extension-wide and channel-wide.

* Each config store is defined by a single JSON object containing key-value pairs. The keys are developer-defined. Use these endpoints to set, modify, and retrieve configuration keys and values.
* Use a GET request to `all_config` to retrieve the current content of all configuration stores.
* The individual config-store endpoints support GET, POST, and PATCH operations.

[block:parameters]
{
  "data": {
    "h-0": "Configuration Data Endpoint",
    "h-1": "Usage",
    "0-0": "`all_config`",
    "1-0": "`extension_config`",
    "2-0": "`channel_config`",
    "0-1": "Retrieves all configuration data in a single call.",
    "1-1": "Maintains and reports per-extension configuration across channels.",
    "2-1": "Maintains and reports per-channel configuration for all extensions running in a channel."
  },
  "cols": 2,
  "rows": 3
}
[/block]

## [State API](https://docs.muxy.io/reference/rest-state-api)

This data store is available with  four different scopes.

* Each state store is defined by a single JSON object containing key-value pairs. The keys are developer-defined. Use these endpoints to set, modify, and retrieve state keys and values.
* Use a GET request to `all_state` to retrieve the current content of all state stores.
* The individual state-store endpoints support GET, POST, and PATCH operations.

[block:parameters]
{
  "data": {
    "h-0": "State Data Endpoint",
    "h-1": "Usage",
    "0-0": "`all_state`",
    "1-0": "`extension_state`",
    "2-0": "`viewer_state`",
    "3-0": "`extension_viewer_state`",
    "4-0": "`channel_state`",
    "0-1": "Retrieves all four state stores in a single call.",
    "1-1": "Maintains and reports per-extension state information.",
    "2-1": "Maintains and reports per-viewer state information.",
    "3-1": "Maintains and reports per-viewer state information for each extension.",
    "4-1": "Maintains and reports per-channel state information for all extensions running in a channel."
  },
  "cols": 2,
  "rows": 5
}
[/block]

## [Engagement Tools API](https://docs.muxy.io/reference/aggregation-api)

The MEDKit REST API supports a variety of tools and techniques for encouraging viewer interaction and engagement, from simple aggregation of viewer data to support for the creation of interactive events.

* *Accumulating* data that users provide is the simplest form of aggregation.
* A *ranking* service collects answers to open-ended questions, and counts matching responses.
* A *polling* service helps you create and manage viewer polls, collect viewer votes, and work with voting results.
* The  *trivia* and *game codes* services help you implement a sophisticated voting-and-reward system.

[block:parameters]
{
  "data": {
    "0-0": "`accumulate`",
    "h-0": "Endpoint",
    "h-1": "Usage",
    "0-1": "Collect user input for developer-defined data.",
    "1-0": "`rank`",
    "1-1": "Create open-ended questions, collect user answers, and get statistics on popular answers.",
    "2-0": "`vote`\n`vote/vote_logs`",
    "2-1": "Create and manage polls, cast and collect users' votes, get voting results and logs."
  },
  "cols": 2,
  "rows": 3
}
[/block]

## Communication API

Additional endpoints support administrative services, including back-channel and server-to-server communication.

[block:parameters]
{
  "data": {
    "h-0": "Endpoint",
    "0-0": "[Broadcast Messaging](https://docs.muxy.io/reference/broadcast) \n`broadcast`\n`broadcast_extension`\n`whisper_self`",
    "0-1": "Broadcast messages to viewers on a per-channel or per-extension basis. \n\nThis service also enables server-to-server and back-channel communication.",
    "h-1": "Usage"
  },
  "cols": 2,
  "rows": 1
}
[/block]
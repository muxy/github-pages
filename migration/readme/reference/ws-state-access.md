# Storing State on the Server

The WebSocket protocol supports read and write of developer-defined game state values.

A client can store state that all users can retrieve on the Muxy servers.

All users can retrieve state values, and users with the "broadcaster" or "admin" role can set values. State update operations should be limited to once every two seconds at most.

# Storing State on the Server

States are stored as JSON-encoded objects containing developer-defined key-value pairs.

* You can replace the entire state data object using the `set` action.
* You can use json-patch commands to update parts of your data object, using the `update` action.

The `target` field for all state operations must be `channel`.

> This method of storing state corresponds with Channel State in the Muxy MEDKit SDK. The state is unique per broadcaster channel. To store state with other scopes, use the Muxy MEDKit SDK.

## Replacing state data

**Request**

The `set` operation replaces any existing state that already exists.

[block:code]
{
  "codes": [
    {
      "code": "{\n    \"action\": \"set\", \n    \"params\": { \n        \"request_id\": 234,\n        \"target\": \"channel\"\n    }, \n    \"data\": {\n        \"state\": { <your-data-blob> }\n    }\n}",
      "language": "json",
      "name": "Set request body format"
    }
  ]
}
[/block]

Note that you can only set state to be a JSON object. Primitives (numbers, strings, booleans) and arrays as root state objects are rejected.

Setting state in this way does not trigger a broadcast.

**Response**

On success, the server respond with a simple confirmation.

[block:code]
{
  "codes": [
    {
      "code": "{\n  \"meta\": {\n    \"request_id\": 234,\n    \"action\": \"set\",\n    \"timestamp\": 1583777221501\n  },\n\n  \"data\": {\n    \"ok\": true,\n    \"state\": { data-blob }\n  }\n}",
      "language": "json",
      "name": "Set response body format"
    }
  ]
}
[/block]

Note that the data-blob received here can be different than what you sent in the original request if there are intervening set or update operations.

## Updating state data

To patch state, use the `update` action, and send an array of patch objects in the "state" field of the "data" object.

[block:code]
{
  "codes": [
    {
      "code": "{\n    \"action\": \"update\", \n    \"params\": { \n        \"request_id\": 235,\n        \"target\": \"channel\"\n    }, \n    \"data\": {\n        \"state\": [\n          { \n            \"op\": \"replace\", \n            \"path\": \"/game_state/player/character/name\", \n            \"value\": \"Guybrush Threepwood\" \n          }\n        ]\n    }\n}",
      "language": "json",
      "name": "Update request body format"
    }
  ]
}
[/block]

# Retrieving State

All users can retrieve state from either the channel-wide state store or the extension-specific state store.

**Request**

To retrieve previously set state, use the `get` action.
You can specify the `target` as `channel` or `extension`, to retrieve either Channel State (as previously set using the `set` or `update` actions), or Extension State, which can only be set through the MEDKit SDK.

[block:code]
{
  "codes": [
    {
      "code": "{\n    \"action\": \"get\", \n    \"params\": { \n        \"request_id\": 145,\n        \"target\": \"channel\"\n    }\n}",
      "language": "json",
      "name": "Get request body format"
    }
  ]
}
[/block]

**Response**

The response to a `get` request is the same as the response to a `set` response,  except that the action field is `get`.

[block:code]
{
  "codes": [
    {
      "code": "{\n  \"meta\": {\n    \"request_id\": 145,\n    \"action\": \"get\",\n    \"timestamp\": 1583777221501\n  },\n\n  \"data\": {\n    \"ok\": true,\n    \"state\": { data-blob }\n  }\n}",
      "language": "json",
      "name": "Get response body format"
    }
  ]
}
[/block]

The retrieval response has no data body or an empty data body.

# Subscribing to State Events

Use the `subscribe` action with a `target` of  `state` to listen for state-update event notifications.
Use the `topic_id` field in `data` to identify the state store of interest,  either `channel` or `extension`.

[block:code]
{
  "codes": [
    {
      "code": "{ \n  \"action\": \"subscribe\", \n  \"params\": { \n    \"request_id\": 11, \n    \"target\": \"state\" \n  }, \n  \"data\" : {\n    \"topic_id\": \"channel\"\n  }\n}",
      "language": "json",
      "name": "State subscription request body format"
    }
  ]
}
[/block]

## State event notifications

State-update notification messages specify the `update` action and the target `channel` or `extension`.
The data `state` field contains the latest JSON-blob value of the targeted state store.

[block:code]
{
  "codes": [
    {
      "code": "{\n  \"meta\": {\n    \"request_id\":65535,\n    \"action\":\"update\",\n    \"target\":\"state\",\n    \"timestamp\":1590011391849472,\n  },\n\n  \"data\": {\n    \"topic_id\": \"channel\",\n    \"state\": {\n      \"game_state\": {\n        \"player\": {\n          \"character\": {\n            \"name\": \"Guybrush Threepwood\"\n          }\n        }\n      }\n    }\n  }\n}",
      "language": "json",
      "name": "State-update notification format"
    }
  ]
}
[/block]
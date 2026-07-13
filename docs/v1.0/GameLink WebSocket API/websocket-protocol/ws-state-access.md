---
title: "Storing State on the Server"
slug: "ws-state-access"
excerpt: "The WebSocket protocol supports read and write of developer-defined game state values."
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Tue Oct 05 2021 16:51:45 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Feb 01 2022 22:55:19 GMT+0000 (Coordinated Universal Time)"
---
A client can store state that all users can retrieve on the Muxy servers. 

All users can retrieve state values, and users with the "broadcaster" or "admin" role can set values. State update operations should be limited to once every two seconds at most. 

# Storing State on the Server

States are stored as JSON-encoded objects containing developer-defined key-value pairs.  

- You can replace the entire state data object using the `set` action.
- You can use json-patch commands to update parts of your data object, using the `update` action.

The `target` field for all state operations must be `channel`.

> This method of storing state corresponds with Channel State in the Muxy MEDKit SDK. The state is unique per broadcaster channel. To store state with other scopes, use the Muxy MEDKit SDK.

## Replacing state data

**Request** 

The `set` operation replaces any existing state that already exists. 

```json Set request body format
{
    "action": "set", 
    "params": { 
        "request_id": 234,
        "target": "channel"
    }, 
    "data": {
        "state": { <your-data-blob> }
    }
}
```

Note that you can only set state to be a JSON object. Primitives (numbers, strings, booleans) and arrays as root state objects are rejected.

Setting state in this way does not trigger a broadcast.

 **Response**

On success, the server respond with a simple confirmation.

```json Set response body format
{
  "meta": {
    "request_id": 234,
    "action": "set",
    "timestamp": 1583777221501
  },

  "data": {
    "ok": true,
    "state": { data-blob }
  }
}
```

Note that the data-blob received here can be different than what you sent in the original request if there are intervening set or update operations.

## Updating state data

 To patch state, use the `update` action, and send an array of patch objects in the "state" field of the "data" object.

```json Update request body format
{
    "action": "update", 
    "params": { 
        "request_id": 235,
        "target": "channel"
    }, 
    "data": {
        "state": [
          { 
            "op": "replace", 
            "path": "/game_state/player/character/name", 
            "value": "Guybrush Threepwood" 
          }
        ]
    }
}
```

# Retrieving State

All users can retrieve state from either the channel-wide state store or the extension-specific state store.

**Request**

To retrieve previously set state, use the `get` action.  
You can specify the `target` as `channel` or `extension`, to retrieve either Channel State (as previously set using the `set` or `update` actions), or Extension State, which can only be set through the MEDKit SDK.

```json Get request body format
{
    "action": "get", 
    "params": { 
        "request_id": 145,
        "target": "channel"
    }
}
```

**Response**

The response to a `get` request is the same as the response to a `set` response,  except that the action field is `get`. 

```json Get response body format
{
  "meta": {
    "request_id": 145,
    "action": "get",
    "timestamp": 1583777221501
  },

  "data": {
    "ok": true,
    "state": { data-blob }
  }
}
```

The retrieval response has no data body or an empty data body. 

# Subscribing to State Events

Use the `subscribe` action with a `target` of  `state` to listen for state-update event notifications.  
Use the `topic_id` field in `data` to identify the state store of interest,  either `channel` or `extension`. 

```json State subscription request body format
{ 
  "action": "subscribe", 
  "params": { 
    "request_id": 11, 
    "target": "state" 
  }, 
  "data" : {
    "topic_id": "channel"
  }
}
```

## State event notifications

State-update notification messages specify the `update` action and the target `channel` or `extension`.  
The data `state` field contains the latest JSON-blob value of the targeted state store.

```json State-update notification format
{
  "meta": {
    "request_id":65535,
    "action":"update",
    "target":"state",
    "timestamp":1590011391849472,
  },

  "data": {
    "topic_id": "channel",
    "state": {
      "game_state": {
        "player": {
          "character": {
            "name": "Guybrush Threepwood"
          }
        }
      }
    }
  }
}
```

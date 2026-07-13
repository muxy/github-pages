---
title: "Client-Server Communication"
slug: "ws-pubsub"
excerpt: ""
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Mon Sep 27 2021 18:45:47 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Feb 01 2022 22:52:49 GMT+0000 (Coordinated Universal Time)"
---
Muxy provides a pub-sub messaging service between clients (or a client server) and the Muxy server, with an option for broadcasting messages to all, or a subset of, the current viewing audience. You can define topics, allowing clients to filter incoming broadcast messages. 

# Message envelope for communication requests

The body of a request to the Muxy server is a JSON-encoded object that uses the following _message envelope_ format.

```json Request body format
{
  // The message "action". one of "subscribe", "unsubscribe", "broadcast"
  "action": String,        

  // An optional mapping of method parameters to values.
  "params"?: {             
    // An optional unique identifier for this message,
    // echoed back as `request_id` in the response
    // An integer between 0 and 65535.
    "request_id"?: Number, 

    // An optional "target" of the action. 
    // One of "accumulate", "vote", "rank", "trivia" ??
    "target"?: String
  },

  // An optional JSON object containing a data payload
  // to be used by the server in processing the request.
  // Format depends on the requested action.
  "data"?: Object          
}
```

# Broadcast action

**Request**  
A message requesting the "broadcast" action contains a `data` object in the following format:

```json Request data-object format
"data": {
    // An optional list of whitelisted user IDs to receive this message.
    // If absent, message is broadcast to all viewers.
    "ids"?: String[],
       // The topic to broadcast on, an arbitrary developer-defined string.
       // Client can use to filter broadcast messages.
    "topic": String

    // The body of the message.
    "message": String
  }
}
```

 **Response**

```json Response body format
{
  "meta": {
    // The request ID if present, or 0xFFFF if absent. 
    // Use to match this response to a specific request.
    "request_id": Number,

    // The action that was requested.
    "action": "broadcast",

    // An empty string.
    "target": String,

    // The server timestamp in milliseconds.
    "timestamp": Number
  },

  // The object { "ok": true } on success
  "data"?: Object,

  // An array of Error objects if the operation did not succeed.
  "errors"?: Array,
}
```

# Subscribe action

**Request**

A message requesting the "subscribe" action must specify the `target` topic, in a `data` object with the following format:

```json Subscription request data-object format
"data": {
       // The topic thread to subscribe to.
    "target": String

    // Optional arbitrary data.
    "message": String
  }
}
```

**Response**

```json Subscription response body format
{
  "meta": {
    // The request ID if present, or 0xFFFF if absent. 
    // Use to match this response to a specific request.
    "request_id": Number,

    // The action that was requested.
    "action": "subscribe",

    // The topic subscribed to.
    "target": String,

    // The server timestamp in milliseconds.
    "timestamp": Number
  },

  // The object { "ok": true } on success
  "data"?: Object,

  // An array of Error objects if the operation did not succeed.
  "errors"?: Array,
}
```

# Unsubscribe action

A message requesting the "unsubscribe" action must specify the `target` topic, in a `data` object with the following format:

**Request**

```json
"data": {
       // The topic thread to unsubscribe from.
    "target": String

    // Optional arbitrary data.
    "message": String
  }
}
```

**Response**

```json Unsubcribe response body format
{
  "meta": {
    // The request ID if present, or 0xFFFF if absent. 
    // Use to match this response to a specific request.
    "request_id": Number,

    // The action that was requested.
    "action": "unsubscribe",

    // The topic unsubscribed from.
    "target": String,

    // The server timestamp in milliseconds.
    "timestamp": Number
  },

  // The object { "ok": true } on success
  "data"?: Object,

  // An array of Error objects if the operation did not succeed.
  "errors"?: Array,
}
```

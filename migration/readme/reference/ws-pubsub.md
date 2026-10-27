# Client-Server Communication

Muxy provides a pub-sub messaging service between clients (or a client server) and the Muxy server, with an option for broadcasting messages to all, or a subset of, the current viewing audience. You can define topics, allowing clients to filter incoming broadcast messages.

# Message envelope for communication requests

The body of a request to the Muxy server is a JSON-encoded object that uses the following *message envelope* format.

[block:code]
{
  "codes": [
    {
      "code": "{\n  // The message \"action\". one of \"subscribe\", \"unsubscribe\", \"broadcast\"\n  \"action\": String,        \n\n  // An optional mapping of method parameters to values.\n  \"params\"?: {             \n    // An optional unique identifier for this message,\n    // echoed back as `request_id` in the response\n    // An integer between 0 and 65535.\n    \"request_id\"?: Number, \n\n    // An optional \"target\" of the action. \n    // One of \"accumulate\", \"vote\", \"rank\", \"trivia\" ??\n    \"target\"?: String\n  },\n\n  // An optional JSON object containing a data payload\n  // to be used by the server in processing the request.\n  // Format depends on the requested action.\n  \"data\"?: Object          \n}\n",
      "language": "json",
      "name": "Request body format"
    }
  ]
}
[/block]

# Broadcast action

**Request**
A message requesting the "broadcast" action contains a `data` object in the following format:

[block:code]
{
  "codes": [
    {
      "code": " \"data\": {\n    // An optional list of whitelisted user IDs to receive this message.\n    // If absent, message is broadcast to all viewers.\n    \"ids\"?: String[],\n       // The topic to broadcast on, an arbitrary developer-defined string.\n       // Client can use to filter broadcast messages.\n    \"topic\": String\n\n    // The body of the message.\n    \"message\": String\n  }\n}",
      "language": "json",
      "name": "Request data-object format"
    }
  ]
}
[/block]

**Response**

[block:code]
{
  "codes": [
    {
      "code": "{\n  \"meta\": {\n    // The request ID if present, or 0xFFFF if absent. \n    // Use to match this response to a specific request.\n    \"request_id\": Number,\n\n    // The action that was requested.\n    \"action\": \"broadcast\",\n\n    // An empty string.\n    \"target\": String,\n\n    // The server timestamp in milliseconds.\n    \"timestamp\": Number\n  },\n\n  // The object { \"ok\": true } on success\n  \"data\"?: Object,\n\n  // An array of Error objects if the operation did not succeed.\n  \"errors\"?: Array,\n}",
      "language": "json",
      "name": "Response body format"
    }
  ]
}
[/block]

# Subscribe action

**Request**

A message requesting the "subscribe" action must specify the `target` topic, in a `data` object with the following format:

[block:code]
{
  "codes": [
    {
      "code": " \"data\": {\n       // The topic thread to subscribe to.\n    \"target\": String\n\n    // Optional arbitrary data.\n    \"message\": String\n  }\n}",
      "language": "json",
      "name": "Subscription request data-object format"
    }
  ]
}
[/block]

**Response**

[block:code]
{
  "codes": [
    {
      "code": "{\n  \"meta\": {\n    // The request ID if present, or 0xFFFF if absent. \n    // Use to match this response to a specific request.\n    \"request_id\": Number,\n\n    // The action that was requested.\n    \"action\": \"subscribe\",\n\n    // The topic subscribed to.\n    \"target\": String,\n\n    // The server timestamp in milliseconds.\n    \"timestamp\": Number\n  },\n\n  // The object { \"ok\": true } on success\n  \"data\"?: Object,\n\n  // An array of Error objects if the operation did not succeed.\n  \"errors\"?: Array,\n}",
      "language": "json",
      "name": "Subscription response body format"
    }
  ]
}
[/block]

# Unsubscribe action

A message requesting the "unsubscribe" action must specify the `target` topic, in a `data` object with the following format:

**Request**

[block:code]
{
  "codes": [
    {
      "code": " \"data\": {\n       // The topic thread to unsubscribe from.\n    \"target\": String\n\n    // Optional arbitrary data.\n    \"message\": String\n  }\n}",
      "language": "json",
      "name": null
    }
  ]
}
[/block]

**Response**

[block:code]
{
  "codes": [
    {
      "code": "{\n  \"meta\": {\n    // The request ID if present, or 0xFFFF if absent. \n    // Use to match this response to a specific request.\n    \"request_id\": Number,\n\n    // The action that was requested.\n    \"action\": \"unsubscribe\",\n\n    // The topic unsubscribed from.\n    \"target\": String,\n\n    // The server timestamp in milliseconds.\n    \"timestamp\": Number\n  },\n\n  // The object { \"ok\": true } on success\n  \"data\"?: Object,\n\n  // An array of Error objects if the operation did not succeed.\n  \"errors\"?: Array,\n}",
      "language": "json",
      "name": "Unsubcribe response body format"
    }
  ]
}
[/block]
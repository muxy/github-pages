# Broadcast Messaging

The broadcast service enables a broadcaster or admin to define and publish messages to subscribers.

Use the broadcast service to create a message thread and publish messages to subscribers.

* A `broadcast` call can target a single viewer, a subset of viewers on a channel, or all viewers on a channel.
* An `extension-broadcast` call targets all viewers that are currently using the extension.
* A `whisper-self` call enables back-channel communication for coordinating and synchronizing  multiple instances of an extension.

The publisher names an *event* stream, which identifies a message thread. Extensions use the GameLink library and WebSocket protocol to subscribe to the named event and register a callback handler for notifications.  See  [Event Handling](https://docs.muxy.io/reference/event-handling#datastream--events) for more information.

**Message format**

The body of an broadcasting request contains the message data as an arbitrary developer-defined JSON object.

[block:callout]
{
  "type": "warning",
  "title": "Message size limit",
  "body": "A message object that is larger than 4kb is automatically compressed, then base64-encoded. If the resulting base64-encoded string is still longer than 4kb, the broadcast call fails. If the call succeeds, the service decodes and decompresses the data transparently. \n\nThis means that the effective maximum size of the JSON object sent by broadcast is not well defined, but 6kb is a safe size."
}
[/block]

**Authorization**

Thread creation and message publishing calls can be made by authenticated users with the `broadcaster` or `admin` role.

The `broadcast` endpoint can also be used for **server-to-server communication**.
Authorization for a call from a backend server to the Muxy server requires a self-signed token with the field `"role": "backend"`. This can be established with a JWT claim by someone who knows the JWT signing secret, generally assumed to be the extension developer.

[block:callout]
{
  "type": "info",
  "body": "Broadcasts sent in the `sandbox` environment do not trigger events in the `production` environment, or vice versa.",
  "title": "Broadcasting during development"
}
[/block]

# Sending a Channel Broadcast

An authorized user with a `backend` or `admin` role can use a GET request to the `broadcast` endpoint to send a message to any channel, or to a specific viewer on the channel.

**Request**

[block:code]
{
  "codes": [
    {
      "code": "GET /v1/e/broadcast",
      "language": "shell"
    }
  ]
}
[/block]

The body of the request contains the following JSON-encoded data.

[block:code]
{
  "codes": [
    {
      "code": "{\n    \"target\": string,\n    \"event\": string,\n    \"user_id\": string,\n    \"data\": object\n}",
      "language": "json"
    }
  ]
}
[/block]

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Value",
    "0-0": "`target`",
    "1-0": "`event`",
    "2-0": "`user_id`",
    "3-0": "`data`",
    "0-1": "String, one of:\n-- `broadcast`: Sends the message to all subscribed viewers \n-- `whisper-${user_id}` : Sends the message to a viewer with the given Twitch ID.",
    "1-1": "String. The developer-defined name of the message thread.  Sends the message to subscribers who have registered a listener for this event.",
    "2-1": "String. The Twitch ID of the channel's broadcaster/owner, which identifies the channel to broadcast to. \n*TBD - change key to \"channel_id\"*",
    "3-1": "JSON object. The body of the message to send."
  },
  "cols": 2,
  "rows": 4
}
[/block]

**Response**

If the call succeeds, the body of the response contains an empty JSON object. If it fails, the body of the response contains error information.

# Sending an Extension-wide Broadcast

The owner or administrator of an extension (an authorized user with a `backend` or `admin` role) can use a GET request to the `extension_broadcast` endpoint to send a message to all viewers on all channels with the extension loaded, or to a specific viewer on any channel.

**Request**

[block:code]
{
  "codes": [
    {
      "code": "GET /v1/e/extension_broadcast",
      "language": "shell"
    }
  ]
}
[/block]

The body of the request contains the following JSON-encoded data.

[block:code]
{
  "codes": [
    {
      "code": "{\n    \"target\": string,\n    \"event\": string,\n    \"data\": object\n}",
      "language": "json"
    }
  ]
}
[/block]

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Value",
    "0-0": "`target`",
    "1-0": "`event`",
    "2-0": "`data`",
    "0-1": "String. Where to send the message. One of:\n-- `broadcast`: Sends the message to all subscribed viewers \n-- `whisper-${user_id}` : Sends the message to a viewer with the given Twitch ID.",
    "1-1": "String. The developer-defined name of the message thread.  Sends the message to subscribers who have registered a listener for this event.",
    "2-1": "JSON object. The body of the message to send."
  },
  "cols": 2,
  "rows": 3
}
[/block]

**Response**

If the call succeeds, the body of the response contains an empty JSON object. If it fails, the body of the response contains error information.

# Sending a Back-channel Message

Use the `whisper_self`  endpoint to synchronize multiple instances of an extension.\
Notifications can be processed on a broadcaster configuration page while the broadcaster is interacting with the viewer extension.

**Request**

A GET request broadcasts a message to all viewing clients that the caller is currently watching, in the same channel that the request was made from.

[block:code]
{
  "codes": [
    {
      "code": "GET /v1/e/whisper_self",
      "language": "shell"
    }
  ]
}
[/block]

The body of the request contains the following JSON-encoded data.

[block:code]
{
  "codes": [
    {
      "code": "{\n    \"event\": string,\n    \"data\": object\n}",
      "language": "json"
    }
  ]
}
[/block]

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Value",
    "0-0": "`event`",
    "1-0": "`data`",
    "0-1": "String. The developer-defined name of the message thread.  Sends the message to subscribers who have registered a listener for this event.",
    "1-1": "JSON object. The body of the message to send."
  },
  "cols": 2,
  "rows": 2
}
[/block]

**Response**

If the call succeeds, the body of the response contains an empty JSON object. If it fails, the body of the response contains error information.
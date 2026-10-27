# Using the WebSocket Protocol

The GameLink connection provides a persistent, publish-subscribe connection for data flow between game clients or servers and a massive live streaming audience.

A scalable server architecture, together with topic/channel communication, enable Muxy to provide real-time game data to viewers. The Muxy Cloud powers new and innovative viewer engagement interactions, with services that maintain developer-defined user and extension state, aggregate viewer input in variety of ways, and facilitate audience monetization actions.

The GameLink library provides these services through a persistent bidirectional connection to the Muxy Cloud. Hundreds of thousands of persistent connections are maintained for hours at a time. During peak events, the Authorizer/Router handles hundreds of thousands of requests per second, with 24/7 availability and low-latency responses, even under peak load.

GameLink services are available through the low-level native-code [Muxy GameLink Library](https://docs.muxy.io/reference/gamelink-library) , and at a higher level through the [MEDKit REST API](https://docs.muxy.io/reference/medkit-rest-api)  and JavaScript.

# GameLink Messaging and State Tracking

Extension data and messages are broadcast through an event system on top of underlying WebSocket connections.

* Game clients can subscribe to events on a named *topic* thread to receive updated information on audience participation.
* Clients can publish events to send information to all or a filtered subset of the live-streaming viewers.
* Clients can get and set developer-defined state values through the event system, and subscribe to state-update events.

The WebSocket protocol defines the following set of actions that a client can request.

[block:parameters]
{
  "data": {
    "h-0": "Action",
    "0-0": "[`authenticate`](https://docs.muxy.io/reference/ws-authentication)",
    "h-1": "Description",
    "h-2": "Data?",
    "h-3": "Filters?",
    "1-0": "[`subscribe`, `unsubscribe`](https://docs.muxy.io/reference/ws-pubsub)",
    "2-0": "[`broadcast`](https://docs.muxy.io/reference/ws-communication)",
    "3-0": "[`get`, `set` state](https://docs.muxy.io/reference/ws-state-access)",
    "2-1": "Targets a named topic, and contains data (the message to broadcast). Can be filtered to a subset of all viewers.",
    "3-1": "Subscriptions target a path to a state key. The `set` call creates and manages developer-defined game-state key-value pairs, the `get` call returns the current value for a given key.",
    "0-1": "Requires a Client ID and authorization (PIN or JWT)",
    "1-1": "Targets a named topic. Can contain developer-defined data."
  },
  "cols": 2,
  "rows": 4
}
[/block]

## GameLink Services

In addition, polling and transaction events are supported through special connection targets `poll` and `transaction_completed`.

[block:parameters]
{
  "data": {
    "h-0": "Event stream",
    "h-1": "Description",
    "0-0": "[Polling and voting events](https://docs.muxy.io/reference/ws-polling)",
    "0-1": "Subscriptions target the `poll` event stream. Create, manage, and delete audience polls, and receive real-time updates on voting results.",
    "1-0": "[Purchasing events](https://docs.muxy.io/reference/ws-purchase-transactions)",
    "1-1": "Subscriptions target the `transaction_completed` event stream. When you offer products for sale through Twitch, respond to completed purchases of those products that are reported from Twitch."
  },
  "cols": 2,
  "rows": 2
}
[/block]
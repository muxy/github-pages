---
title: "Using the WebSocket Protocol"
slug: "websocket-protocol"
excerpt: "The GameLink connection provides a persistent, publish-subscribe connection for data flow between game clients or servers and a massive live streaming audience."
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Tue Sep 14 2021 15:42:55 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Oct 07 2021 16:12:42 GMT+0000 (Coordinated Universal Time)"
---
A scalable server architecture, together with topic/channel communication, enable Muxy to provide real-time game data to viewers. The Muxy Cloud powers new and innovative viewer engagement interactions, with services that maintain developer-defined user and extension state, aggregate viewer input in variety of ways, and facilitate audience monetization actions.

The GameLink library provides these services through a persistent bidirectional connection to the Muxy Cloud. Hundreds of thousands of persistent connections are maintained for hours at a time. During peak events, the Authorizer/Router handles hundreds of thousands of requests per second, with 24/7 availability and low-latency responses, even under peak load.

GameLink services are available through the low-level native-code [Muxy GameLink Library](../../v1.0/GameLink C--C-- Library/gamelink-library.md) , and at a higher level through the [MEDKit REST API](../../v1.0/REST API/medkit-rest-api.md)  and JavaScript.

# GameLink Messaging and State Tracking

Extension data and messages are broadcast through an event system on top of underlying WebSocket connections. 

- Game clients can subscribe to events on a named _topic_ thread to receive updated information on audience participation.
- Clients can publish events to send information to all or a filtered subset of the live-streaming viewers.
- Clients can get and set developer-defined state values through the event system, and subscribe to state-update events. 

The WebSocket protocol defines the following set of actions that a client can request.

| Action                                      | Description                                                                                                                                                                            |
| :------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`authenticate`](../../v1.0/GameLink WebSocket API/websocket-protocol/ws-authentication.md)     | Requires a Client ID and authorization (PIN or JWT)                                                                                                                                    |
| [`subscribe`, `unsubscribe`](../../v1.0/GameLink WebSocket API/websocket-protocol/ws-pubsub.md) | Targets a named topic. Can contain developer-defined data.                                                                                                                             |
| [`broadcast`](ws-communication)         | Targets a named topic, and contains data (the message to broadcast). Can be filtered to a subset of all viewers.                                                                       |
| [`get`, `set` state](../../v1.0/GameLink WebSocket API/websocket-protocol/ws-state-access.md)   | Subscriptions target a path to a state key. The `set` call creates and manages developer-defined game-state key-value pairs, the `get` call returns the current value for a given key. |

## GameLink Services

In addition, polling and transaction events are supported through special connection targets `poll` and `transaction_completed`.

| Event stream                                      | Description                                                                                                                                                                                     |
| :------------------------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Polling and voting events](../../v1.0/GameLink WebSocket API/websocket-protocol/ws-polling.md)       | Subscriptions target the `poll` event stream. Create, manage, and delete audience polls, and receive real-time updates on voting results.                                                       |
| [Purchasing events](../../v1.0/GameLink WebSocket API/websocket-protocol/ws-purchase-transactions.md) | Subscriptions target the `transaction_completed` event stream. When you offer products for sale through Twitch, respond to completed purchases of those products that are reported from Twitch. |

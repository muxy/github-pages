---
title: "SDK Class"
slug: "sdk-class"
excerpt: "Provides primary access to Muxy functionality."
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Tue Sep 28 2021 17:32:07 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Wed Mar 02 2022 18:30:28 GMT+0000 (Coordinated Universal Time)"
---
# Public Member Functions

The `MuxyGameLink.SDK` class provides functionality in the following areas:

- [Extension Setup API](../../v1.0/GameLink C--C-- Library/sdk-class/extension-setup-api.md): Extension authentication and setup.
- [State and Configuration Handling](../../v1.0/GameLink C--C-- Library/sdk-class/state-config-fns.md): Set, retrieve, and update per-channel and per-extension state values and developer-defined configuration values.
- [Event Handling](../../v1.0/GameLink C--C-- Library/sdk-class/event-handling.md): Subscribe to and unsubscribe from event notification in all areas.
  - Get [debugging](../../v1.0/GameLink C--C-- Library/sdk-class/event-handling.md#debugging-events) notifications in the development environment.
  - Use the [datastream service](../../v1.0/GameLink C--C-- Library/sdk-class/event-handling.md#datastream-events) to broadcast messages to subscribers.
  - Respond to changes in the [state and configuration](../../v1.0/GameLink C--C-- Library/sdk-class/event-handling.md#state-and-configuration-events) data.
  - Set up and manage [viewer polls](../../v1.0/GameLink C--C-- Library/sdk-class/event-handling.md#manage-polls-and-polling-events).
  - Handle notifications of [Twitch Bit Transactions](../../v1.0/GameLink C--C-- Library/sdk-class/event-handling.md#twitch-bit-transactions) from viewers.

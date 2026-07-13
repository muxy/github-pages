---
title: "Muxy GameLink Library"
slug: "gamelink-library"
excerpt: "Use this native-code library to integrate Muxy functionality into your game or other Twitch extension."
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Tue Sep 28 2021 16:20:14 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Jul 26 2022 17:10:18 GMT+0000 (Coordinated Universal Time)"
---
The GameLink Library provides direct native-code access to Muxy functionality.  The library is available in two versions:

- GameLink C# for the Unity game engine
- GameLink C++ for the Unreal game engine

The `MuxyGameLink` namespace contains the [`SDK` class](refs:sdk-class), which provides primary access to Muxy functionality, making use of supporting data structures. 

Muxy functionality includes:

- [Authentication of users and extension setup](../../v1.0/GameLink C--C-- Library/sdk-class/extension-setup-api.md) 
- [State and configuration data handling](../../v1.0/GameLink C--C-- Library/sdk-class/state-config-fns.md)  
- [Event Handling](../../v1.0/GameLink C--C-- Library/sdk-class/event-handling.md) 
  - Get [debugging](refs:event-handling#debugging-events) notifications in the development environment.
  - Use the [datastream service](refs:event-handling#datastream-events) to broadcast messages to subscribers.
  - Respond to changes in the [state and configuration](refs:event-handling#state-and-configuration-events) data.
  - Set up and manage [viewer polls](refs:event-handling#manage-polls-and-polling-events).
  - Handle notifications of [Twitch Bit Transactions](refs:event-handling#twitch-bit-transactions) from viewers. 

Calls to retrieve or change data on the Muxy server are asynchronous. These calls require you to supply callback functions to handle the response when it is received.

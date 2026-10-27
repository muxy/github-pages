# Muxy GameLink Library

Use this native-code library to integrate Muxy functionality into your game or other Twitch extension.

The GameLink Library provides direct native-code access to Muxy functionality.  The library is available in two versions:

* GameLink C# for the Unity game engine
* GameLink C++ for the Unreal game engine

The `MuxyGameLink` namespace contains the [`SDK` class](refs:sdk-class), which provides primary access to Muxy functionality, making use of supporting data structures.

Muxy functionality includes:

* [Authentication of users and extension setup](https://docs.muxy.io/reference/extension-setup-api)
* [State and configuration data handling](https://docs.muxy.io/reference/state-config-fns)
* [Event Handling](https://docs.muxy.io/reference/event-handling)
  * Get [debugging](refs:event-handling#debugging-events) notifications in the development environment.
  * Use the [datastream service](refs:event-handling#datastream-events) to broadcast messages to subscribers.
  * Respond to changes in the [state and configuration](refs:event-handling#state-and-configuration-events) data.
  * Set up and manage [viewer polls](refs:event-handling#manage-polls-and-polling-events).
  * Handle notifications of [Twitch Bit Transactions](refs:event-handling#twitch-bit-transactions) from viewers.

Calls to retrieve or change data on the Muxy server are asynchronous. These calls require you to supply callback functions to handle the response when it is received.
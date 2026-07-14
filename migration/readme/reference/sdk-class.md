# SDK Class

Provides primary access to Muxy functionality.

# Public Member Functions

The `MuxyGameLink.SDK` class provides functionality in the following areas:

* [Extension Setup API](https://docs.muxy.io/reference/extension-setup-api): Extension authentication and setup.
* [State and Configuration Handling](https://docs.muxy.io/reference/state-config-fns): Set, retrieve, and update per-channel and per-extension state values and developer-defined configuration values.
* [Event Handling](https://docs.muxy.io/reference/event-handling): Subscribe to and unsubscribe from event notification in all areas.
  * Get [debugging](https://docs.muxy.io/reference/event-handling#debugging-events) notifications in the development environment.
  * Use the [datastream service](https://docs.muxy.io/reference/event-handling#datastream-events) to broadcast messages to subscribers.
  * Respond to changes in the [state and configuration](https://docs.muxy.io/reference/event-handling#state-and-configuration-events) data.
  * Set up and manage [viewer polls](https://docs.muxy.io/reference/event-handling#manage-polls-and-polling-events).
  * Handle notifications of [Twitch Bit Transactions](https://docs.muxy.io/reference/event-handling#twitch-bit-transactions) from viewers.
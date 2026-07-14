# Config API

Muxy provides a storage area for developer-defined configuration data that is specific to either an extension or a channel.

Configuration data, like [state data](https://docs.muxy.io/reference/rest-state-api), is developer defined.  You can define, monitor, and manage whatever configuration data you want to track in real time.

Configuration storage differs from state storage in that it is optimized for long-term storage at the expense of data storage limits. Configuration data is handled in much the same way as state data.

The Muxy server maintains two configuration stores with different scopes.

* **Channel config store**: Keeps configuration data for an extension running on a specific channel.  A user with the `broadcaster` or `admin` role can set and modify configuration values for their own channel. The configuration data can be accessed by all viewers of the associated channel.

* **Extension config store**: Keeps configuration data shared across all instances of an extension on any channel.\
  Extension-wide configuration can only be set by a caller with `admin` role or a `backend`-authenticated request (that is, a JWT created with knowledge of the extension secret, such as a custom server). The data can be accessed by all admins, broadcasters and viewers.

Each configuration store contains a single JSON-encoded object containing developer-defined key-value pairs.

* Use POST to replace the entire data object in any of the data stores. Pass the new data object in the body of the request.
* Use PATCH to modify specific state values. Pass a JSON object, in [JSONPatch](http://jsonpatch.com/) format, containing new key-value pairs in the body of the request.
* Successful GET calls return the stored data in the body of the response.

Use the following  endpoints to create, manage, and access state data.

[block:parameters]
{
  "data": {
    "h-0": "Endpoint",
    "h-1": "Description",
    "0-1": "This endpoint provides read-only access to all of the configuration stores.",
    "0-0": "`config`",
    "1-0": "`config/extension`",
    "2-0": "`config/channel`",
    "1-1": "The **Extension** store keeps configuration data shared across all instances of an extension.",
    "2-1": "The **Channel** store keeps configuration data across all extension instances on a given channel.",
    "h-2": "Commands",
    "0-2": "Use [GET](https://docs.muxy.io/reference/extension-config) to retrieve current values from all configuration stores.",
    "1-2": "Use [POST](https://docs.muxy.io/reference/extension-config-2) to create or replace the entire config object in this store.\n\nUse [GET](https://docs.muxy.io/reference/extension-config-1) to retrieve specific configuration values.\n\nUse [PATCH](https://docs.muxy.io/reference/extension-config-3) to modify specific configuration values.",
    "2-2": "Use [POST](https://docs.muxy.io/reference/channel-config-1) to create or replace the entire config object in this store.\n\nUse [GET](https://docs.muxy.io/reference/channel-config)  to retrieve specific configuration values.\n\nUse [PATCH](https://docs.muxy.io/reference/channel-config-2) to modify specific configuration values."
  },
  "cols": 3,
  "rows": 3
}
[/block]

[block:callout]
{
  "type": "info",
  "title": "Access authorization summary",
  "body": "* A caller with `broadcaster`  role can store, modify, and retrieve state only for their own channel.\n* A caller with `backend` or `admin` role can store, modify, and retrieve state for any channel.\n* A caller with `viewer` role can only retrieve state for the channel they are watching."
}
[/block]
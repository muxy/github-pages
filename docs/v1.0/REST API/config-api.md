---
title: "Config API"
slug: "config-api"
excerpt: "Muxy provides a storage area for developer-defined configuration data that is specific to either an extension or a channel."
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Fri Oct 15 2021 20:48:16 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Jan 11 2022 18:52:16 GMT+0000 (Coordinated Universal Time)"
---
Configuration data, like [state data](../../v1.0/REST API/rest-state-api.md), is developer defined.  You can define, monitor, and manage whatever configuration data you want to track in real time. 

Configuration storage differs from state storage in that it is optimized for long-term storage at the expense of data storage limits. Configuration data is handled in much the same way as state data.

The Muxy server maintains two configuration stores with different scopes. 

- **Channel config store**: Keeps configuration data for an extension running on a specific channel.  A user with the `broadcaster` or `admin` role can set and modify configuration values for their own channel. The configuration data can be accessed by all viewers of the associated channel.

- **Extension config store**: Keeps configuration data shared across all instances of an extension on any channel.  
  Extension-wide configuration can only be set by a caller with `admin` role or a `backend`-authenticated request (that is, a JWT created with knowledge of the extension secret, such as a custom server). The data can be accessed by all admins, broadcasters and viewers.

Each configuration store contains a single JSON-encoded object containing developer-defined key-value pairs. 

- Use POST to replace the entire data object in any of the data stores. Pass the new data object in the body of the request. 
- Use PATCH to modify specific state values. Pass a JSON object, in [JSONPatch](http://jsonpatch.com/) format, containing new key-value pairs in the body of the request. 
- Successful GET calls return the stored data in the body of the response. 

Use the following  endpoints to create, manage, and access state data.



| Endpoint | Description | Commands |
| --- | --- | --- |
| `config` | This endpoint provides read-only access to all of the configuration stores. | Use [GET](../../v1.0/REST API/config-api/extension-config.md) to retrieve current values from all configuration stores. |
| `config/extension` | The **Extension** store keeps configuration data shared across all instances of an extension. | Use [POST](../../v1.0/REST API/config-api/extension-config-2.md) to create or replace the entire config object in this store.  <br>  <br>Use [GET](../../v1.0/REST API/config-api/extension-config-1.md) to retrieve specific configuration values.  <br>  <br>Use [PATCH](../../v1.0/REST API/config-api/extension-config-3.md) to modify specific configuration values. |
| `config/channel` | The **Channel** store keeps configuration data across all extension instances on a given channel. | Use [POST](../../v1.0/REST API/config-api/channel-config-1.md) to create or replace the entire config object in this store.  <br>  <br>Use [GET](../../v1.0/REST API/config-api/channel-config.md)  to retrieve specific configuration values.  <br>  <br>Use [PATCH](../../v1.0/REST API/config-api/channel-config-2.md) to modify specific configuration values. |




> 📘 Access authorization summary
> 
> - A caller with `broadcaster`  role can store, modify, and retrieve state only for their own channel.
> - A caller with `backend` or `admin` role can store, modify, and retrieve state for any channel.
> - A caller with `viewer` role can only retrieve state for the channel they are watching.

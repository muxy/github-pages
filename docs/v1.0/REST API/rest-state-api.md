---
title: "State API"
slug: "rest-state-api"
excerpt: "Use these endpoints to define and manage developer-defined game state."
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Tue Sep 14 2021 22:20:42 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Wed Jan 12 2022 16:38:46 GMT+0000 (Coordinated Universal Time)"
---
You can define, monitor, and manage whatever data you want to track in real time.  
The Muxy server maintains state stores with various scopes. 

- **Extension state store**: Admins can define and store state shared across all instances of an extension on all channels.
- **Channel state store**: Broadcasters can define and store state shared across all extension instances on a given channel..
- **Viewer state store**: Anyone can define and store state for a specific viewer on a specific channel.
- **ExtensionViewer state store**:   Anyone can define and store state for a specific viewer across every instance of the extension on all channels.

All users can access the data, but only users with specific access rights can set and modify state values. The `viewer` role allows callers to set and modify state for themselves. The `broadcaster` role allows callers to set and modify state in their own channel. The `admin` and `backend` roles allow the caller to modify state globally.

Each state store contains a single JSON-encoded object containing developer-defined key-value pairs. Successful GET calls return the stored data in the body of the response. 

- Use POST to replace the entire data object in any of the data stores. Pass the new data object in the body of the request. 
- Use PATCH to add, remove, or modify specific state values. Pass a JSON object containing the changes, using [JSONPatch syntax](http://jsonpatch.com/). 

> 📘 Data Expiration
> 
> State data stored using this API expires automatically 30 days after the last update to a given state store. Expired data is removed and cannot be retrieved. 
> 
> Expiration time for channel state is calculated on a channel-specific basis. That is, updating data for a specific channel extends the expiration time ONLY for that channel.

Use the following  endpoints to create, manage, and access state data.



| Endpoint | Description | Commands |
| --- | --- | --- |
| `all_state` | This endpoint provides read-only access to all of the state stores. | Use [GET](../../v1.0/REST API/rest-state-api/viewer-state.md) to retrieve current state values from all of the state stores. |
| `extension_state` | The **Extension** state store keeps state shared across all instances of an extension on all channels.  <br>  <br>POST and PATCH require `admin` or `backend` authorization. | Use [POST](../../v1.0/REST API/rest-state-api/extension-state.md) to create or replace the entire state object in this store.  <br>  <br>Use [GET](../../v1.0/REST API/rest-state-api/viewer-state-4.md)to retrieve specific state values.  <br>  <br>Use [PATCH](../../v1.0/REST API/rest-state-api/extension-state-1.md) to modify specific state values. |
| `channel_state` | The **Channel** state store keeps per-viewer state across all extension instances on a given channel.  <br>  <br>POST and PATCH require `admin`,  `backend`, or `broadcaster` authorization. | Use [POST](../../v1.0/REST API/rest-state-api/channel-state-1.md) to create or replace the entire state object in this store.  <br>  <br>Use [GET](../../v1.0/REST API/rest-state-api/channel-state.md)to retrieve specific state values.  <br>  <br>Use [PATCH](../../v1.0/REST API/rest-state-api/channel-state-2.md) to modify specific state values. |
| `viewer_state` | The **Viewer** state store keeps state for  as pecific viewer on a specific channel.  <br>  <br>Viewers can set state for themselves. | Use [POST](../../v1.0/REST API/rest-state-api/viewer-state-1.md) to create or replace the entire state object in this store.  <br>  <br>Use [GET](../../v1.0/REST API/rest-state-api/viewer-state-2.md)to retrieve specific state values.  <br>  <br>Use [PATCH](../../v1.0/REST API/rest-state-api/viewer-state-3.md) to modify specific state values. |
| `extension_viewer_state` | The **ExtensionViewer** state store keeps per-viewer state that is accessible across every instance of the extension on Twitch.  <br>  <br>Viewers can set state for themselves. | Use [POST](../../v1.0/REST API/rest-state-api/extension-viewer-state-1.md) to create or replace the entire state object in this store.  <br>  <br>Use [GET](../../v1.0/REST API/rest-state-api/extension-viewer-state.md) to retrieve specific state values.  <br>  <br>Use [PATCH](../../v1.0/REST API/rest-state-api/extension-viewer-state-2.md) to modify specific state values. |



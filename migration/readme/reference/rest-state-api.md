# State API

Use these endpoints to define and manage developer-defined game state.

You can define, monitor, and manage whatever data you want to track in real time.
The Muxy server maintains state stores with various scopes.

* **Extension state store**: Admins can define and store state shared across all instances of an extension on all channels.
* **Channel state store**: Broadcasters can define and store state shared across all extension instances on a given channel..
* **Viewer state store**: Anyone can define and store state for a specific viewer on a specific channel.
* **ExtensionViewer state store**:   Anyone can define and store state for a specific viewer across every instance of the extension on all channels.

All users can access the data, but only users with specific access rights can set and modify state values. The `viewer` role allows callers to set and modify state for themselves. The `broadcaster` role allows callers to set and modify state in their own channel. The `admin` and `backend` roles allow the caller to modify state globally.

Each state store contains a single JSON-encoded object containing developer-defined key-value pairs. Successful GET calls return the stored data in the body of the response.

* Use POST to replace the entire data object in any of the data stores. Pass the new data object in the body of the request.
* Use PATCH to add, remove, or modify specific state values. Pass a JSON object containing the changes, using [JSONPatch syntax](http://jsonpatch.com/).

[block:callout]
{
  "type": "info",
  "title": "Data Expiration",
  "body": "State data stored using this API expires automatically 30 days after the last update to a given state store. Expired data is removed and cannot be retrieved. \n\nExpiration time for channel state is calculated on a channel-specific basis. That is, updating data for a specific channel extends the expiration time ONLY for that channel."
}
[/block]

Use the following  endpoints to create, manage, and access state data.

[block:parameters]
{
  "data": {
    "h-0": "Endpoint",
    "h-1": "Description",
    "0-1": "This endpoint provides read-only access to all of the state stores.",
    "0-0": "`all_state`",
    "1-0": "`extension_state`",
    "2-0": "`channel_state`",
    "1-1": "The **Extension** state store keeps state shared across all instances of an extension on all channels.\n\nPOST and PATCH require `admin` or `backend` authorization.",
    "2-1": "The **Channel** state store keeps per-viewer state across all extension instances on a given channel.\n\nPOST and PATCH require `admin`,  `backend`, or `broadcaster` authorization.",
    "h-2": "Commands",
    "0-2": "Use [GET](https://docs.muxy.io/reference/viewer-state) to retrieve current state values from all of the state stores.",
    "1-2": "Use [POST](https://docs.muxy.io/reference/extension-state) to create or replace the entire state object in this store.\n\nUse [GET](https://docs.muxy.io/reference/viewer-state-4)to retrieve specific state values.\n\nUse [PATCH](https://docs.muxy.io/reference/extension-state-1) to modify specific state values.",
    "2-2": "Use [POST](https://docs.muxy.io/reference/channel-state-1) to create or replace the entire state object in this store.\n\nUse [GET](https://docs.muxy.io/reference/channel-state)to retrieve specific state values.\n\nUse [PATCH](https://docs.muxy.io/reference/channel-state-2) to modify specific state values.",
    "3-0": "`viewer_state`",
    "3-1": "The **Viewer** state store keeps state for  as pecific viewer on a specific channel.\n\nViewers can set state for themselves.",
    "3-2": "Use [POST](https://docs.muxy.io/reference/viewer-state-1) to create or replace the entire state object in this store.\n\nUse [GET](https://docs.muxy.io/reference/viewer-state-2)to retrieve specific state values.\n\nUse [PATCH](https://docs.muxy.io/reference/viewer-state-3) to modify specific state values.",
    "4-0": "`extension_viewer_state`",
    "4-1": "The **ExtensionViewer** state store keeps per-viewer state that is accessible across every instance of the extension on Twitch.\n\nViewers can set state for themselves.",
    "4-2": "Use [POST](https://docs.muxy.io/reference/extension-viewer-state-1) to create or replace the entire state object in this store.\n\nUse [GET](https://docs.muxy.io/reference/extension-viewer-state) to retrieve specific state values.\n\nUse [PATCH](https://docs.muxy.io/reference/extension-viewer-state-2) to modify specific state values."
  },
  "cols": 3,
  "rows": 5
}
[/block]
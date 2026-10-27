# Store Extension and Viewer State

Muxy lets you define your own state data and maintains it in real time.

The Muxy server tracks the state of your extension in real time. You can use MEDKit JavaScript SDK methods to define, store, and retrieve state values. States are stored as JSON blobs, containing developer-defined key-value pairs. There are no predefined keys. You are responsible for defining what data you want to track, and performing any validation of values.

# State Stores

Four state stores vary in scope and accessibility. Read and write access to state values depends on the role of the current user when one of these methods is called.

* **Extension**:  Keeps state as shared across all instances of an extension.
* **Channel**: Keeps state on a per-channel basis.
* **Viewer**:  Keeps state for viewers on a specific channel.
* **ExtensionViewer**:  Keeps per-viewer state that is accessible across every instance of the extension on Twitch.

A user can access each of these stores individually, depending on their role. In addition, any user can retrieve the current content from all four stores at once.

## Access to State Stores

Use MEDKit  methods to retrieve an aggregate of all state information, or to set and get state from each store. Some set methods are only available to users with specific roles.

[block:parameters]
{
  "data": {
    "h-0": "Store",
    "0-0": "AllState",
    "h-1": "Scope and access",
    "0-1": "Aggregates and returns all of the state stores. \n\nRead-only, get available to all users.",
    "h-2": "Get example",
    "0-2": "```js\nsdk.getAllState().then(state => {\n  console.log(state);\n});\n```\n\n**Response**\n```json\n{\n  \"extension\": {},\n  \"channel\": {},\n  \"viewer\": {},\n  \"extension_viewer\": {}\n}\n```",
    "h-3": "Set example",
    "1-0": "ExtensionState",
    "1-1": "Keeps state as shared across all instances of an extension. \n\nGet available to all users.\n\nSet available to `broadcaster` whose user ID matches the extension `owner` or `admin`.",
    "2-0": "ChannelState",
    "2-1": "Keeps state on a per-channel basis. \n\nGet available to all users.\n\nSet available only to `broadcaster`.",
    "1-2": "```js\nsdk.getExtensionState().then(state => {\n  console.log(state);\n});\n```\n\n**Response**\n```json\n{\n  \"sample_field\": \"test\"\n}\n```",
    "0-3": "Read-only",
    "1-3": "```js\nconst newState = {\n  sample_field: 'test'\n};\n\nsdk.setExtensionState(newState).then(state => {\n  console.log(state);\n});\n```\n\n**Response**\n```json\n{}\n```",
    "3-1": "Keeps state on a per-viewer basis. \n\nGet available to all users.\n\nSet available to viewers of a specific channel.",
    "3-0": "ViewerState",
    "4-0": "ExtensionViewerState",
    "4-1": "Keeps per-viewer state across every instance of the extension on Twitch. \n\nGet and set available to viewers across all channels."
  },
  "cols": 2,
  "rows": 5
}
[/block]

# State Access Examples

The following examples show how to access the state stores with `Muxy.SDK` methods, and the format of the response. Developers are responsible for defining keys and expected values in the JSON content.

These examples assume a variable `muxy` set to a  `Muxy.SDK` instance.

## All State

[block:parameters]
{
  "data": {
    "0-0": "```js\nmedkit.getAllState().then(state => {\n  console.log(state);\n});\n```\n\n**Response**\n```json\n{\n  extension: { enable_feature: false },\n  channel: { channel_specific_setting: \"abc\" },\n  viewer: { viewer_specific_setting: 1234 }\n}\n```",
    "h-0": "Get"
  },
  "cols": 1,
  "rows": 1
}
[/block]

## Extension State

Keeps state as shared across all instances of an extension.
Get available to any role. Set available to `broadcaster` whose user ID matches the extension `owner` or `admin`.

[block:parameters]
{
  "data": {
    "h-0": "Get",
    "h-1": "Set",
    "0-0": "```js\nmedkit.getExtensionState().then(state => {\n  console.log(state);\n});\n```\n\n**Response**\n```json\n{\n  \"sample_field\": \"test\"\n}\n```",
    "0-1": "```js\nconst newState = {\n  sample_field: 'test'\n};\n\nsdk.setExtensionState(newState).then(state => {\n  console.log(state);\n});\n```\n\n**Response**\n```json\n{}\n```"
  },
  "cols": 2,
  "rows": 1
}
[/block]

## Channel State

Keeps state on a per-channel basis.  Can be set only by a user with `broadcaster` role. Get available to any role.

[block:parameters]
{
  "data": {
    "h-0": "Get",
    "h-1": "Set",
    "0-0": "```javascript\nmedkit.getChannelState().then(state => {\n  console.log(state);\n});\n```\n\n**Response**\n```json\n{\n  \"sample_field\": \"test\"\n}\n```",
    "0-1": "```js\nconst newState = {\n  sample_field: 'test'\n};\n\nmedkit.setChannelState(newState).then(state => {\n  console.log(state);\n});\n```\n\n**Response**\n```json\n{}\n```"
  },
  "cols": 2,
  "rows": 1
}
[/block]

## Extension Viewer State

Keeps per-viewer state across every instance of the extension on Twitch. Available to any user role for set or get.

[block:parameters]
{
  "data": {
    "h-0": "Get",
    "h-1": "Set",
    "0-0": "```js\nmedkit.getExtensionViewerState().then(state => {\n  console.log(state);\n});\n```\n\n**Response**\n```json\n{\n  \"sample_field\": \"test\"\n}\n```",
    "0-1": "```js\nconst newState = {\n  sample_field: 'test'\n};\n\nmedkit.setExtensionViewerState(newState).then(state => {\n  console.log(state);\n});\n```\n\n**Response**\n```json\n{}\n```"
  },
  "cols": 2,
  "rows": 1
}
[/block]

## Viewer State

Keeps per-viewer state for a specific channel. Available to any user role for set or get.

[block:parameters]
{
  "data": {
    "h-0": "Get",
    "h-1": "Set",
    "0-0": "```js\nmedkit.getViewerState().then(state => {\n  console.log(state);\n});\n```\n\n**Response**\n```json\n{\n  \"sample_field\": \"test\"\n}\n```",
    "0-1": "```js\nmedkit.getViewerState().then(state => {\n  console.log(state);\n});\n```\n\n**Response**\n```json\n{\n  \"sample_field\": \"test\"\n}\n```"
  },
  "cols": 2,
  "rows": 1
}
[/block]
# Store Configuration Data

Muxy provides a storage area for developer-defined configuration data that is specific to either an extension or a channel.

Configuration data, like [state data](docs;state-information), is developer defined.  You can define, monitor, and manage whatever configuration data you want to use for extension configuration. Configuration storage differs from state storage in that it is optimized for long-term storage at the expense of data storage limits.

Configuration data is handled in much the same way as state data. You can use MEDKit JS SDK methods to define, store, and retrieve state values. States are stored as JSON blobs, containing developer-defined key-value pairs. There are no predefined keys. You are responsible for defining what data you want to track, and performing any validation of values.

# Configuration Stores

The Muxy server maintains two configuration stores with different scopes.

* **Extension config store**: Keeps configuration data shared across all instances of an extension.
  The Extension configuration can only be set by a `backend`-authenticated request; that is, one created with knowledge of the extension secret, such as a custom server. The data can be accessed by all broadcasters and viewers.

* **Channel config store**: Keeps configuration data on a per-channel basis.
  A user with the `broadcaster` role can set and modify configuration values for their own channel. The configuration data can be accessed by all viewers of the associated channel.

Each configuration store contains a single JSON-encoded object containing developer-defined key-value pairs.

\#Access to Configuration Stores

Use MEDKit  methods to retrieve an aggregate of all state information, or to set and get state from each store. Some set methods are only available to users with specific roles.

[block:parameters]
{
  "data": {
    "h-0": "Store",
    "0-0": "AllConfig",
    "h-1": "Scope and access",
    "0-1": "Aggregates and returns all of the state stores. \n\nRead-only, get available to all users.",
    "h-2": "Get example",
    "0-2": "```js\nsdk.getAllState().then(state => {\n  console.log(state);\n});\n```\n\n**Response**\n```json\n{\n  \"extension\": {},\n  \"channel\": {},\n  \"viewer\": {},\n  \"extension_viewer\": {}\n}\n```",
    "h-3": "Set example",
    "1-0": "ExtensionConfig",
    "1-1": "Keeps state as shared across all instances of an extension. \n\nGet available to all users.\n\nSet available to `broadcaster` whose user ID matches the extension `owner` or `admin`.",
    "2-0": "ChannelConfig",
    "2-1": "Keeps state on a per-channel basis. \n\nGet available to all users.\n\nSet available only to `broadcaster`.",
    "1-2": "```js\nsdk.getExtensionState().then(state => {\n  console.log(state);\n});\n```\n\n**Response**\n```json\n{\n  \"sample_field\": \"test\"\n}\n```",
    "0-3": "Read-only",
    "1-3": "```js\nconst newState = {\n  sample_field: 'test'\n};\n\nsdk.setExtensionState(newState).then(state => {\n  console.log(state);\n});\n```\n\n**Response**\n```json\n{}\n```"
  },
  "cols": 2,
  "rows": 3
}
[/block]

# Config Access Examples

The following examples show how to access the config stores with `Muxy.SDK` methods, and the format of the response. Developers are responsible for defining keys and expected values in the JSON content.

These examples assume a variable `muxy` set to a  `Muxy.SDK` instance.

## All Config

[block:parameters]
{
  "data": {
    "0-0": "```js\nmedkit.getAllConfig().then(config=> {\n  console.log(state);\n});\n```\n\n**Response**\n```json\n{\n  extension: { enable_feature: false },\n  channel: { channel_specific_setting: \"abc\" },\n}\n```",
    "h-0": "Get"
  },
  "cols": 1,
  "rows": 1
}
[/block]

## Extension Config

Keeps configuration data to be shared across all instances of an extension.
Get available to any role. Set available to `broadcaster` whose user ID matches the extension `owner` or `admin`.

[block:parameters]
{
  "data": {
    "h-0": "Get",
    "h-1": "Set",
    "0-0": "```js\nmedkit.getExtensionConfig().then(config => {\n  console.log(state);\n});\n```\n\n**Response**\n```json\n{\n  \"sample_field\": \"test\"\n}\n```",
    "0-1": "```js\nconst newConfigValue = {\n  sample_field: 'test'\n};\n\nsdk.setExtensionConfig(newConfigValue).then(config => {\n  console.log(state);\n});\n```\n\n**Response**\n```json\n{}\n```"
  },
  "cols": 2,
  "rows": 1
}
[/block]

## Channel Config

Keeps configuration data on a per-channel basis.  Can be set only by a user with `broadcaster` role. Get available to any role.

[block:parameters]
{
  "data": {
    "h-0": "Get",
    "h-1": "Set",
    "0-0": "```javascript\nmedkit.getChannelConfig().then(config => {\n  console.log(state);\n});\n```\n\n**Response**\n```json\n{\n  \"sample_field\": \"test\"\n}\n```",
    "0-1": "```js\nconst newConfigValue = {\n  sample_field: 'test'\n};\n\nmedkit.setChannelConfig(newConfigValue).then(config => {\n  console.log(state);\n});\n```\n\n**Response**\n```json\n{}\n```"
  },
  "cols": 2,
  "rows": 1
}
[/block]
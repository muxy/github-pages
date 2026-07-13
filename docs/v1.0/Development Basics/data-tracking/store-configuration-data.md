---
title: "Store Configuration Data"
slug: "store-configuration-data"
excerpt: "Muxy provides a storage area for developer-defined configuration data that is specific to either an extension or a channel."
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Wed Nov 03 2021 20:21:05 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Feb 01 2022 17:53:39 GMT+0000 (Coordinated Universal Time)"
---
Configuration data, like [state data](docs;state-information), is developer defined.  You can define, monitor, and manage whatever configuration data you want to use for extension configuration. Configuration storage differs from state storage in that it is optimized for long-term storage at the expense of data storage limits. 

Configuration data is handled in much the same way as state data. You can use MEDKit JS SDK methods to define, store, and retrieve state values. States are stored as JSON blobs, containing developer-defined key-value pairs. There are no predefined keys. You are responsible for defining what data you want to track, and performing any validation of values.

# Configuration Stores

The Muxy server maintains two configuration stores with different scopes. 

- **Extension config store**: Keeps configuration data shared across all instances of an extension.  
  The Extension configuration can only be set by a `backend`-authenticated request; that is, one created with knowledge of the extension secret, such as a custom server. The data can be accessed by all broadcasters and viewers.

- **Channel config store**: Keeps configuration data on a per-channel basis.  
  A user with the `broadcaster` role can set and modify configuration values for their own channel. The configuration data can be accessed by all viewers of the associated channel.

Each configuration store contains a single JSON-encoded object containing developer-defined key-value pairs. 

# Access to Configuration Stores

Use MEDKit  methods to retrieve an aggregate of all state information, or to set and get state from each store. Some set methods are only available to users with specific roles.



| Store | Scope and access |
| --- | --- |
| AllConfig | Aggregates and returns all of the state stores.  <br>  <br>Read-only, get available to all users. |
| ExtensionConfig | Keeps state as shared across all instances of an extension.  <br>  <br>Get available to all users.  <br>  <br>Set available to `broadcaster` whose user ID matches the extension `owner` or `admin`. |
| ChannelConfig | Keeps state on a per-channel basis.  <br>  <br>Get available to all users.  <br>  <br>Set available only to `broadcaster`. |




# Config Access Examples

The following examples show how to access the config stores with `Muxy.SDK` methods, and the format of the response. Developers are responsible for defining keys and expected values in the JSON content. 

These examples assume a variable `muxy` set to a  `Muxy.SDK` instance.

## All Config



| Get |
| --- |
| `js<br>medkit.getAllConfig().then(config=> {<br>  console.log(state);<br>});<br>`  <br>  <br>**Response**  <br>`json<br>{<br>  extension: { enable_feature: false },<br>  channel: { channel_specific_setting: "abc" },<br>}<br>` |




## Extension Config

Keeps configuration data to be shared across all instances of an extension.  
Get available to any role. Set available to `broadcaster` whose user ID matches the extension `owner` or `admin`. 



| Get | Set |
| --- | --- |
| `js<br>medkit.getExtensionConfig().then(config => {<br>  console.log(state);<br>});<br>`  <br>  <br>**Response**  <br>`json<br>{<br>  "sample_field": "test"<br>}<br>` | `js<br>const newConfigValue = {<br>  sample_field: 'test'<br>};<br><br>sdk.setExtensionConfig(newConfigValue).then(config => {<br>  console.log(state);<br>});<br>`  <br>  <br>**Response**  <br>`json<br>{}<br>` |




## Channel Config

Keeps configuration data on a per-channel basis.  Can be set only by a user with `broadcaster` role. Get available to any role.



| Get | Set |
| --- | --- |
| `javascript<br>medkit.getChannelConfig().then(config => {<br>  console.log(state);<br>});<br>`  <br>  <br>**Response**  <br>`json<br>{<br>  "sample_field": "test"<br>}<br>` | `js<br>const newConfigValue = {<br>  sample_field: 'test'<br>};<br><br>medkit.setChannelConfig(newConfigValue).then(config => {<br>  console.log(state);<br>});<br>`  <br>  <br>**Response**  <br>`json<br>{}<br>` |



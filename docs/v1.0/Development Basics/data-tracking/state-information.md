---
title: "Store Extension and Viewer State"
slug: "state-information"
excerpt: "Muxy lets you define your own state data and maintains it in real time."
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Wed Sep 15 2021 16:41:11 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Wed Nov 03 2021 22:51:42 GMT+0000 (Coordinated Universal Time)"
---
The Muxy server tracks the state of your extension in real time. You can use MEDKit JavaScript SDK methods to define, store, and retrieve state values. States are stored as JSON blobs, containing developer-defined key-value pairs. There are no predefined keys. You are responsible for defining what data you want to track, and performing any validation of values.

# State Stores

Four state stores vary in scope and accessibility. Read and write access to state values depends on the role of the current user when one of these methods is called. 

- **Extension**:  Keeps state as shared across all instances of an extension.
- **Channel**: Keeps state on a per-channel basis.
- **Viewer**:  Keeps state for viewers on a specific channel.  
- **ExtensionViewer**:  Keeps per-viewer state that is accessible across every instance of the extension on Twitch. 

A user can access each of these stores individually, depending on their role. In addition, any user can retrieve the current content from all four stores at once.

## Access to State Stores

Use MEDKit  methods to retrieve an aggregate of all state information, or to set and get state from each store. Some set methods are only available to users with specific roles.



| Store | Scope and access |
| --- | --- |
| AllState | Aggregates and returns all of the state stores.  <br>  <br>Read-only, get available to all users. |
| ExtensionState | Keeps state as shared across all instances of an extension.  <br>  <br>Get available to all users.  <br>  <br>Set available to `broadcaster` whose user ID matches the extension `owner` or `admin`. |
| ChannelState | Keeps state on a per-channel basis.  <br>  <br>Get available to all users.  <br>  <br>Set available only to `broadcaster`. |
| ViewerState | Keeps state on a per-viewer basis.  <br>  <br>Get available to all users.  <br>  <br>Set available to viewers of a specific channel. |
| ExtensionViewerState | Keeps per-viewer state across every instance of the extension on Twitch.  <br>  <br>Get and set available to viewers across all channels. |




# State Access Examples

The following examples show how to access the state stores with `Muxy.SDK` methods, and the format of the response. Developers are responsible for defining keys and expected values in the JSON content. 

These examples assume a variable `muxy` set to a  `Muxy.SDK` instance.

## All State



| Get |
| --- |
| `js<br>medkit.getAllState().then(state => {<br>  console.log(state);<br>});<br>`  <br>  <br>**Response**  <br>`json<br>{<br>  extension: { enable_feature: false },<br>  channel: { channel_specific_setting: "abc" },<br>  viewer: { viewer_specific_setting: 1234 }<br>}<br>` |




## Extension State

Keeps state as shared across all instances of an extension.  
Get available to any role. Set available to `broadcaster` whose user ID matches the extension `owner` or `admin`. 



| Get | Set |
| --- | --- |
| `js<br>medkit.getExtensionState().then(state => {<br>  console.log(state);<br>});<br>`  <br>  <br>**Response**  <br>`json<br>{<br>  "sample_field": "test"<br>}<br>` | `js<br>const newState = {<br>  sample_field: 'test'<br>};<br><br>sdk.setExtensionState(newState).then(state => {<br>  console.log(state);<br>});<br>`  <br>  <br>**Response**  <br>`json<br>{}<br>` |




## Channel State

Keeps state on a per-channel basis.  Can be set only by a user with `broadcaster` role. Get available to any role.



| Get | Set |
| --- | --- |
| `javascript<br>medkit.getChannelState().then(state => {<br>  console.log(state);<br>});<br>`  <br>  <br>**Response**  <br>`json<br>{<br>  "sample_field": "test"<br>}<br>` | `js<br>const newState = {<br>  sample_field: 'test'<br>};<br><br>medkit.setChannelState(newState).then(state => {<br>  console.log(state);<br>});<br>`  <br>  <br>**Response**  <br>`json<br>{}<br>` |




## Extension Viewer State

 Keeps per-viewer state across every instance of the extension on Twitch. Available to any user role for set or get.



| Get | Set |
| --- | --- |
| `js<br>medkit.getExtensionViewerState().then(state => {<br>  console.log(state);<br>});<br>`  <br>  <br>**Response**  <br>`json<br>{<br>  "sample_field": "test"<br>}<br>` | `js<br>const newState = {<br>  sample_field: 'test'<br>};<br><br>medkit.setExtensionViewerState(newState).then(state => {<br>  console.log(state);<br>});<br>`  <br>  <br>**Response**  <br>`json<br>{}<br>` |




## Viewer State

Keeps per-viewer state for a specific channel. Available to any user role for set or get.



| Get | Set |
| --- | --- |
| `js<br>medkit.getViewerState().then(state => {<br>  console.log(state);<br>});<br>`  <br>  <br>**Response**  <br>`json<br>{<br>  "sample_field": "test"<br>}<br>` | `js<br>medkit.getViewerState().then(state => {<br>  console.log(state);<br>});<br>`  <br>  <br>**Response**  <br>`json<br>{<br>  "sample_field": "test"<br>}<br>` |



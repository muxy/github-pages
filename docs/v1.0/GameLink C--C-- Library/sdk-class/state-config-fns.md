---
title: "State and Configuration Handling"
slug: "state-config-fns"
excerpt: "SDK functions that access Muxy Twitch Extension state and configuration data."
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Tue Sep 28 2021 20:23:05 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Wed Sep 29 2021 14:42:17 GMT+0000 (Coordinated Universal Time)"
---
# Updating State and Configuration Values

All state and configuration options are stored as key-value pairs in a JSON object. Values can be updated using  a specified [JSON patch operation](http://jsonpatch.com/).  Supported operations are “add”, “remove”, “replace”, “move”, “copy”, “test”. The operations are applied to the current state value in order: if any of them fails. the entire operation fails. The "test" operation succeeds if the given value is present, and fails if it is not.

You can perform an update operation on the entire JSON object, or on a given key. Specific value updates have separate functions for each data type.  For these functions, you provide a path within the JSON object to the desired key. For example, suppose you want to replace values in the following JSON object:

```JSON
{
  "name": "Judy",
  "health": "30"
  "details" : ["val1", "val2", "val3"]
}
```

Use calls like this, referencing keys at the top level of the object:

```C#
// replace a string value
UpdateStateWithString(STATE_TARGET_EXTENSION, "replace", "/name", "Judy B");
// replace an integer value
UpdateStateWithInteger(STATE_TARGET_EXTENSION, "replace", "/health", 100);
// replace an array value using zero-based index
UpdateStateWithString(STATE_TARGET_EXTENSION, "replace", "/details/0", "first-value");
```

# Extension and Channel State Handling

Muxy stores extension state on a per-extension or per-channel basis. A  state value is a JSON object.  Each call takes the _target_ state store to be updated and the patch _operation_ to be performed, as well as the new value.

- The _target_ state store is one of: `STATE_TARGET_CHANNEL`, `STATE_TARGET_EXTENSION`
- The update _operation_ is one of:  “add”, “remove”, “replace”, “move”, “copy”, “test”. 

There are separate calls for storing state values of specific data types. These take the path to a key within the current JSON object, and a new value of the given type for that key.

Get and update calls are asynchronous. You must supply a callback to handle the response when the operation has completed. 

You can subscribe to and unsubscribe from events for specific state targets; see [Event Handling](#event-handling).



| Function | Description | C# Signature |
| --- | --- | --- |
| SetState | Set _Target_ state to new JSON value. | `UInt16  SetState`  <br>`   (string` _Target_,  `string` _Json_) |
| GetState | Retrieve the value of  _Target_ state and pass it to the callback. | `UInt16  GetState`  <br>`   (string` _Target_,  <br>`    GetStateCallback` _Callback_) |
| GetStateCallback | Handler signature for response to `GetState()` call. | `delegate void GetStateCallback`  <br>`    (StateUpdate` _Response_) |
| UpdateStateCallback | Handler signature for response to any update-state call. | `delegate void UpdateStateCallback`  <br>`    (StateUpdate` _Response_) |
| UpdateStateWithInteger | Perform the given _Operation_ on the value of the key at the given _Path_. | `UInt16  UpdateStateWithInteger`  <br>`  (string` _Target_, `string` _Operation_,  `string` _Path_, `Int64` _Value_) |
| UpdateStateWithDouble | Perform the given _Operation_ on the value of the key at the given _Path_. | `UInt16  UpdateStateWithDouble`  <br>`  (string` _Target_, `string` _Operation_,  `string` _Path_, `Double` _Value_) |
| UpdateStateWithString | Perform the given _Operation_ on the value of the key at the given _Path_. | `UInt16  UpdateStateWithString`  <br>`  (string` _Target_, `string` _Operation_, ` string` _Path_, `string` _Value_) |
| UpdateStateWithLiteral | Perform the given _Operation_ on the value of the key at the given _Path_. | `UInt16  UpdateStateWithLiteral `  <br>`  (string` _Target_, `string` _Operation_, `string` _Path_, `string` _JsonLiteral_) |
| UpdateStateWithNull | Perform the given _Operation_ on the value of the key at the given _Path_. | `UInt16 UpdateStateWithNull`  <br>`  (string` _Target_, `string` _Operation_, `string` _Path_) |




# Extension and Channel Configuration Handling

An extension can define its own configuration options, on a per-channel or per-extension basis, and store them separately from the standard state store.  Each store contains key-value pairs in a JSON object.   

- For all calls,  the _target_ is one of `CONFIG_TARGET_CHANNEL`, `CONFIG_TARGET_EXTENSION`
- For update calls, the _operation_ is one of:  “add”, “remove”, “replace”, “move”, “copy”, “test”. 

There are separate calls for storing state values of specific data types. These take the path to a key within the current JSON object, and a new value of the given type for that key.

Get and update calls are asynchronous. You must supply a callback to handle the response when the operation has completed. 

You can subscribe to and unsubscribe from events for specific state targets; see [Event Handling](#event-handling).



| Function | Description | C# Signature |
| --- | --- | --- |
| SetChannelConfig | Sets channel or extension configuration. | `UInt16 SetChannelConfig`  <br>`  (string` _JsonLiteral_) |
| GetChannelConfig | Retrieve channel or extension configuration. | `UInt16 GetChannelConfig`  <br>`  (string` _Target_, `GetChannelCallback` _Callback_) |
| GetChannelCallback | Handler signature for response to `GetChannelConfig()` call. | `delegate void GetChannelCallback`  <br>`  (ConfigResponse` _Response_) |
| UpdateConfigWithInteger | Perform the given _Operation_ on the value of the key at the given _Path_. | `UInt16 UpdateConfigWithInteger`  <br>`  (string` _Target_, `string` _Operation_, `string` _Path_, `Int64` _Value_) |
| UpdateConfigWithDouble | Perform the given _Operation_ on the value of the key at the given _Path_. | `UInt16 UpdateConfigWithDouble`  <br>`  (string` _Target_, `string` _Operation_, `string` _Path_, `Double` _Value_) |
| UpdateConfigWithString | Perform the given _Operation_ on the value of the key at the given _Path_. | `UInt16 UpdateConfigWithString` ` <br>`  (string`*Target*,`string`*Operation*,`string`*Path*,`string\` _Value_) |
| UpdateConfigWithLiteral | Perform the given _Operation_ on the value of the key at the given _Path_. | `UInt16 UpdateConfigWithLiteral`  <br>`  (string` _Target_, `string` _Operation_, `string` _Path_, `string` _JsonLiteral_) |
| UpdateConfigWithNull | Perform the given _Operation_ on the value of the key at the given _Path_. | `UInt16 UpdateConfigWithNull`  <br>`  (string` _Target_, `string` _Operation_, `string` _Path_) |



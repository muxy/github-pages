# State and Configuration Handling

SDK functions that access Muxy Twitch Extension state and configuration data.

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

Muxy stores extension state on a per-extension or per-channel basis. A  state value is a JSON object.  Each call takes the *target* state store to be updated and the patch *operation* to be performed, as well as the new value.

* The *target* state store is one of: `STATE_TARGET_CHANNEL`, `STATE_TARGET_EXTENSION`
* The update *operation* is one of:  “add”, “remove”, “replace”, “move”, “copy”, “test”.

There are separate calls for storing state values of specific data types. These take the path to a key within the current JSON object, and a new value of the given type for that key.

Get and update calls are asynchronous. You must supply a callback to handle the response when the operation has completed.

You can subscribe to and unsubscribe from events for specific state targets; see [Event Handling](#event-handling).

[block:parameters]
{
  "data": {
    "h-0": "Function",
    "h-1": "Description",
    "h-2": "C# Signature",
    "0-0": "SetState",
    "0-1": "Set *Target* state to new JSON value.",
    "0-2": "`UInt16  SetState`\n`   (string` *Target*,  `string` *Json*)",
    "1-0": "GetState",
    "1-1": "Retrieve the value of  *Target* state and pass it to the callback.",
    "1-2": "`UInt16  GetState`\n`   (string` *Target*, \n`    GetStateCallback` *Callback*)",
    "2-0": "GetStateCallback",
    "2-1": "Handler signature for response to `GetState()` call.",
    "2-2": "`delegate void GetStateCallback`\n`    (StateUpdate` *Response*)",
    "3-0": "UpdateStateCallback",
    "3-1": "Handler signature for response to any update-state call.",
    "3-2": "`delegate void UpdateStateCallback`\n`    (StateUpdate` *Response*)",
    "4-0": "UpdateStateWithInteger",
    "4-1": "Perform the given *Operation* on the value of the key at the given *Path*.",
    "5-1": "Perform the given *Operation* on the value of the key at the given *Path*.",
    "6-1": "Perform the given *Operation* on the value of the key at the given *Path*.",
    "7-1": "Perform the given *Operation* on the value of the key at the given *Path*.",
    "4-2": "`UInt16  UpdateStateWithInteger`\n`  (string` *Target*, `string` *Operation*,  `string` *Path*, `Int64` *Value*)",
    "5-0": "UpdateStateWithDouble",
    "5-2": "`UInt16  UpdateStateWithDouble`\n`  (string` *Target*, `string` *Operation*,  `string` *Path*, `Double` *Value*)",
    "6-0": "UpdateStateWithString",
    "6-2": "`UInt16  UpdateStateWithString` \n`  (string` *Target*, `string` *Operation*, ` string` *Path*, `string` *Value*)",
    "7-0": "UpdateStateWithLiteral",
    "7-2": "`UInt16  UpdateStateWithLiteral `\n`  (string` *Target*, `string` *Operation*, `string` *Path*, `string` *JsonLiteral*)",
    "8-0": "UpdateStateWithNull",
    "8-1": "Perform the given *Operation* on the value of the key at the given *Path*.",
    "8-2": "`UInt16 UpdateStateWithNull`\n`  (string` *Target*, `string` *Operation*, `string` *Path*)"
  },
  "cols": 3,
  "rows": 9
}
[/block]

# Extension and Channel Configuration Handling

An extension can define its own configuration options, on a per-channel or per-extension basis, and store them separately from the standard state store.  Each store contains key-value pairs in a JSON object.

* For all calls,  the *target* is one of `CONFIG_TARGET_CHANNEL`, `CONFIG_TARGET_EXTENSION`
* For update calls, the *operation* is one of:  “add”, “remove”, “replace”, “move”, “copy”, “test”.

There are separate calls for storing state values of specific data types. These take the path to a key within the current JSON object, and a new value of the given type for that key.

Get and update calls are asynchronous. You must supply a callback to handle the response when the operation has completed.

You can subscribe to and unsubscribe from events for specific state targets; see [Event Handling](#event-handling).

[block:parameters]
{
  "data": {
    "h-0": "Function",
    "h-1": "Description",
    "h-2": "C# Signature",
    "0-2": "`UInt16 SetChannelConfig`\n`  (string` *JsonLiteral*)",
    "0-0": "SetChannelConfig",
    "0-1": "Sets channel or extension configuration.",
    "1-2": "`UInt16 GetChannelConfig`\n`  (string` *Target*, `GetChannelCallback` *Callback*)",
    "2-2": "`delegate void GetChannelCallback`\n`  (ConfigResponse` *Response*)",
    "3-2": "`UInt16 UpdateConfigWithInteger`\n`  (string` *Target*, `string` *Operation*, `string` *Path*, `Int64` *Value*)",
    "1-1": "Retrieve channel or extension configuration.",
    "1-0": "GetChannelConfig",
    "2-0": "GetChannelCallback",
    "2-1": "Handler signature for response to `GetChannelConfig()` call.",
    "3-0": "UpdateConfigWithInteger",
    "3-1": "Perform the given *Operation* on the value of the key at the given *Path*.",
    "4-2": "`UInt16 UpdateConfigWithDouble` \n`  (string` *Target*, `string` *Operation*, `string` *Path*, `Double` *Value*)",
    "4-0": "UpdateConfigWithDouble",
    "4-1": "Perform the given *Operation* on the value of the key at the given *Path*.",
    "5-2": "`UInt16 UpdateConfigWithString` ` \n`  (string` *Target*, `string` *Operation*, `string` *Path*, `string` *Value*)",
    "5-0": "UpdateConfigWithString",
    "5-1": "Perform the given *Operation* on the value of the key at the given *Path*.",
    "6-2": "`UInt16 UpdateConfigWithLiteral`\n`  (string` *Target*, `string` *Operation*, `string` *Path*, `string` *JsonLiteral*)",
    "6-0": "UpdateConfigWithLiteral",
    "7-2": "`UInt16 UpdateConfigWithNull`\n`  (string` *Target*, `string` *Operation*, `string` *Path*)",
    "7-0": "UpdateConfigWithNull",
    "6-1": "Perform the given *Operation* on the value of the key at the given *Path*.",
    "7-1": "Perform the given *Operation* on the value of the key at the given *Path*."
  },
  "cols": 3,
  "rows": 8
}
[/block]
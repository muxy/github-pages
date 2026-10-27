# Event Handling

SDK functions for managing subscriptions and handling of event notification in all areas.

Muxy offers client-server and server-to-server communication through a messaging service. Extensions can publish and subscribe to messages on a named thread, and users with the "admin" role can broadcast messages to all viewers, or to selected sets of viewers.

Event subscriptions and notifications are handled slightly differently in different areas:

* [Debugging events](#debugging-events) report error information in the development environment.
* [Datastream  events](#datastream-events) provide generic pub-sub message broadcasting.
* [State and configuration events](#state-and-configuration-events) report activity that affects stored state and configuration values for an extension.
* [Polling events](#manage-polls-and-polling-events) report activity in a named viewer poll.
* [Transaction events](#transaction-events) report Twitch Bit Transaction activity involving an extension user.

# Debugging events

In the development environment, the server reports errors through these messages. The extension does not need to subscribe, but must supply a handler for the error information contained in the message.

[block:parameters]
{
  "data": {
    "h-0": "Function",
    "h-1": "Description",
    "h-2": "C# Signature",
    "0-2": "`delegate void OnDebugMessageCallback`\n`  (String` *Message*)",
    "0-0": "OnDebugMessageCallback",
    "0-1": "Handler signature for response to error notification.\n\nThe *Message* contains the error number and description in JSON format.",
    "1-2": "`void OnDebugMessage`\n`  (OnDebugMessageCallback` *Callback*)",
    "1-0": "OnDebugMessage",
    "1-1": "Attach callback for debug messages.",
    "2-2": "`void DetachOnDebugMessage ()`",
    "2-0": "DetachOnDebugMessage",
    "2-1": "Detach callback for debug messages."
  },
  "cols": 3,
  "rows": 3
}
[/block]

# Datastream  events

This system provides the ability to broadcast messages to subscribers on a per-channel or per-extension basis. Notification of broadcasts on the datastream contain the arbitrary message content in JSON format.

[block:parameters]
{
  "data": {
    "h-0": "Function",
    "h-1": "Description",
    "h-2": "C# Signature",
    "0-2": "`UInt16 SendBroadcast`\n`  (string` *Target*, `string` *Json*)",
    "0-0": "SendBroadcast",
    "0-1": "Broadcasts a message to subscribers in the *Target* scope, one of \"STATE_TARGET_CHANNEL\" or \"STATE_TARGET_EXTENSION\".\n*Json* contains the message body in JSON format.",
    "1-2": "`delegate void DatastreamCallback (DatastreamUpdate` *Update*`)`",
    "2-2": "`UInt32 OnDatastream (DatastreamCallback` *Callback*`)`",
    "3-2": "`void DetachOnDatastream (UInt32` *Handle*`)`",
    "4-2": "`UInt16 SubscribeToDatastream ()`",
    "5-2": "`UInt16 UnsubscribeFromDatastream ()`",
    "1-0": "DatastreamCallback",
    "2-0": "OnDatastream",
    "3-0": "DetachOnDatastream",
    "4-0": "SubscribeToDatastream",
    "5-0": "UnsubscribeFromDatastream",
    "1-1": "Handler signature for response to a message notification.",
    "2-1": "Attach callback for message notification events. \n\nUse `SubscribeToDatastream()` to begin receiving message notifications.",
    "3-1": "Attach callback for message notification events, passing the *Handle* returned from `OnDatastream()`.",
    "4-1": "Subscribe to message notifications.\n\nUse after defining and attaching a handler with `OnDatastream()`",
    "5-1": "Unsubscribe from message notifications."
  },
  "cols": 3,
  "rows": 6
}
[/block]

# State and Configuration Events

Muxy stores predefined and developer-defined state values on a  per-channel or per-extension basis.
An extension can also define its own configuration options on a per-channel or per-extension basis, and store them separately from the standard state store. Each store contains key-value pairs in a JSON object.

> See [State and Configuration Handling](https://docs.muxy.io/reference/state-config-fns).

Use the following functions to manage subscriptions and define responses to state and configuration update notifications.

* Subscription-management functions must specify the target, one of `CONFIG_TARGET_CHANNEL` or `CONFIG_TARGET_EXTENSION`.
* Update notifications report the type of operation performed. Update operations are: “add”, “remove”, “replace”, “move”, “copy”, “test”.

[block:parameters]
{
  "data": {
    "1-2": "`UInt32 OnStateUpdate`\n`  (UpdateStateCallback` *Callback*)",
    "1-0": "OnStateUpdate",
    "1-1": "Attach callback for state update events. \n\nUse `SubscribeToStateUpdates()` to begin receiving update notifications.",
    "h-0": "Function",
    "h-1": "Description",
    "h-2": "C# Signature",
    "0-0": "UpdateStateCallback",
    "0-1": "Handler signature for response to any update-state event.",
    "0-2": "`delegate void UpdateStateCallback`\n`  (StateUpdate` *Response*)",
    "3-2": "`UInt16 SubscribeToStateUpdates` \n`  (string` *Target*)",
    "3-0": "SubscribeToStateUpdates",
    "3-1": "Subscribe to state update notifications for channel or extension.\n\nUse after defining and attaching a handler with `OnStateUpdate()`.",
    "4-2": "`UInt16 UnsubscribeFromStateUpdates`\n`  (string`  *Target*)",
    "4-1": "Unsubscribe from state update notifications.",
    "4-0": "UnsubscribeFromStateUpdates",
    "2-2": "`void DetachOnStateUpdate`\n`  (UInt32` *Handle*)",
    "2-0": "DetachOnStateUpdate",
    "2-1": "Detach callback for state updates, passing the *Handle* returned from `OnStateUpdate()`.",
    "5-2": "`delegate void \tUpdateConfigCallback` \n`  (ConfigUpdate` *Response*)",
    "8-2": "UInt16 SubscribeToConfigurationChanges (string *Target*)",
    "8-1": "Subscribe to configuration change notifications.\n\nUse after defining and attaching a handler with `OnConfigUpdate()`.",
    "8-0": "SubscribeToConfigurationChanges",
    "9-2": "UInt16 UnsubscribeFromConfigurationChanges (string *Target*)",
    "9-1": "Unsubscribe from configuration change notifications.",
    "9-0": "UnsubscribeFromConfigurationChanges",
    "5-1": "Handler signature for response to any update-configuration event.",
    "6-2": "`UInt32 OnConfigUpdate`\n`  (UpdateConfigCallback` *Callback*)",
    "7-2": "`void DetachOnConfigUpdate`\n`  (UInt32` *Handle*)",
    "5-0": "UpdateConfigCallback",
    "6-0": "OnConfigUpdate",
    "7-0": "DetachOnConfigUpdate",
    "6-1": "Attach callback for configuration update events. \n\nUse `SubscribeToConfigUpdates()` to begin receiving update notifications.",
    "7-1": "Detach callback for configuration updates, passing the *Handle* returned from `OnConfigUpdate()`."
  },
  "cols": 3,
  "rows": 10
}
[/block]

# Manage Polls and Polling Events

Users with administrative privilege can create and manage viewer polls. Use these `SDK` functions manage subscriptions to polling events, and get poll responses.

[block:parameters]
{
  "data": {
    "h-0": "Function",
    "h-1": "Description",
    "h-2": "Signature",
    "0-2": "`UInt16 CreatePoll`\n`  (String` *PollId*, `String` *Prompt*, `List< String >` *Options*)",
    "0-1": "Create and name a poll, with a prompt and list of options.\n\nAvailable only when current user has \"admin\" role.",
    "0-0": "CreatePoll",
    "1-2": "`UInt16 DeletePoll`\n`  (String` *PollId*)",
    "1-1": "Delete the named poll and all its data.\n\nAvailable only when current user has \"admin\" role",
    "7-2": "`UInt16 SubscribeToPoll`\n` (String` *PollId*)",
    "7-1": "Subscribe to a named poll. \n\nBefore subscribing,  use `OnPollUpdate ()` to set the callback that handles polling events.",
    "7-0": "SubscribeToPoll",
    "8-2": "`UInt16 UnsubscribeFromPoll`\n`  (String` *PollId*)",
    "8-0": "UnsubscribeFromPoll",
    "8-1": "Unsubscribe from the named poll.",
    "1-0": "DeletePoll",
    "2-2": "`delegate void GetPollCallback`\n`  (GetPollResponse` *Response*)",
    "2-0": "GetPollCallback",
    "2-1": "Handler signature for response to `GetPoll()` call.",
    "3-2": "`UInt16 GetPoll`\n`  (String` *PollId*, `GetPollCallback` *Callback*)",
    "3-0": "GetPoll",
    "3-1": "Retrieve poll results once, and pass them to the *Callback* handler.",
    "4-2": "`delegate void PollUpdateResponseCallback`\n`  (PollUpdateResponse` *PResp*)",
    "4-0": "PollUpdateResponseCallback",
    "4-1": "Handler signature for response to Poll Update. Pass to `OnPollUpdate()` call.",
    "5-2": "`UInt32 OnPollUpdate`\n`  (PollUpdateResponseCallback` *Callback*)",
    "5-1": "Sets callback to handle Poll Update events. \n\nYou must call to `SubscribeToPoll()` to begin receiving Poll Update events.",
    "5-0": "OnPollUpdate",
    "6-2": "`void DetachOnPollUpdate`\n` (UInt32` *Handle*)",
    "6-0": "DetachOnPollUpdate",
    "6-1": "Detach callback for Poll Update events, using *Handle* returned from  `OnPollUpdate()` call."
  },
  "cols": 3,
  "rows": 9
}
[/block]

# Twitch Bit Transactions

The following `SDK` functions let you manage Twitch Bit Transactions from extension viewers.

[block:parameters]
{
  "data": {
    "h-0": "Function",
    "h-1": "Description",
    "h-2": "C# Signature",
    "0-2": "`UInt16 SubscribeToSKU`\n` (string` *SKU*)",
    "1-2": "`UInt16 UnsubscribeFromSKU`\n`  (string` *SKU*)",
    "2-2": "`UInt16 SubscribeToAllPurchases ()`",
    "3-2": "`UInt16 UnsubscribeFromAllPurchases ()`",
    "0-1": "Subscribe to SKU purchase notifications.",
    "1-1": "Unsubscribe from SKU purchase notifications.",
    "2-1": "Subscribe to all Twitch Bit Purchase notifications.",
    "3-1": "Unsubscribe from all Twitch Bit Purchase notifications.",
    "4-2": "`delegate void \tTransactionCallback`\n` (Transaction` *Purchase*)",
    "5-2": "`UInt32 OnTransaction`\n`  (TransactionCallback` *Callback*)",
    "5-1": "Sets callback for Twitch Bit Purchasing events.\n\nYou must subscribe by calling to `SubscribeToSKU()` or `SubscribeToAllPurchases()` to begin receiving purchase events.",
    "4-0": "TransactionCallback",
    "5-0": "OnTransaction",
    "3-0": "UnsubscribeFromAllPurchases",
    "2-0": "SubscribeToAllPurchases",
    "1-0": "UnsubscribeFromSKU",
    "0-0": "SubscribeToSKU",
    "6-2": "`void DetachOnTransaction`\n`  (UInt32 *Handle*)",
    "6-1": "Detach callback for Twitch Bit Purchases  using *Handle* returned from `OnTransaction()` call.",
    "6-0": "DetachOnTransaction",
    "7-2": "`delegate void \tGetOutstandingTransactionsCallback`\n` (OutstandingTransactions` *Transactions*)",
    "8-2": "`UInt16 GetOutstandingTransactions`\n`  (String` *SKU*, `GetOutstandingTransactionsCallback` *Callback*)",
    "8-1": "Get all outstanding transactions that need validation.",
    "9-2": "`UInt16 RefundTransactionByID`\n` (String` *TxId*, `String` *UserId*)",
    "10-2": "`UInt16 RefundTransactionBySKU`\n`  (String` *SKU*, `String` *UserId*)",
    "11-2": "`UInt16 ValidateTransaction`\n`  (String` *TxId*, `String` *Details*)",
    "9-1": "Refund given transaction for user.",
    "10-1": "Refund given transaction for user.",
    "11-1": "Validate given transaction.",
    "7-0": "GetOutstandingTransactionsCallback",
    "8-0": "GetOutstandingTransactions",
    "9-0": "RefundTransactionByID",
    "10-0": "RefundTransactionBySKU",
    "11-0": "ValidateTransaction",
    "4-1": "Handler signature for response to purchase events. Pass to `OnTransaction()` call.",
    "7-1": "Handler signature for response to `GetOutstandingTransactions()` calls."
  },
  "cols": 3,
  "rows": 12
}
[/block]
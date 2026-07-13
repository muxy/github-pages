---
title: "Event Handling"
slug: "event-handling"
excerpt: "SDK functions for managing subscriptions and handling of event notification in all areas."
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Tue Sep 28 2021 20:26:31 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Jul 26 2022 17:04:07 GMT+0000 (Coordinated Universal Time)"
---
Muxy offers client-server and server-to-server communication through a messaging service. Extensions can publish and subscribe to messages on a named thread, and users with the "admin" role can broadcast messages to all viewers, or to selected sets of viewers.

Event subscriptions and notifications are handled slightly differently in different areas:

- [Debugging events](#debugging-events) report error information in the development environment.
- [Datastream  events](#datastream-events) provide generic pub-sub message broadcasting. 
- [State and configuration events](#state-and-configuration-events) report activity that affects stored state and configuration values for an extension.
- [Polling events](#manage-polls-and-polling-events) report activity in a named viewer poll.
- [Transaction events](#transaction-events) report Twitch Bit Transaction activity involving an extension user.

# Debugging events

In the development environment, the server reports errors through these messages. The extension does not need to subscribe, but must supply a handler for the error information contained in the message.



| Function | Description | C# Signature |
| --- | --- | --- |
| OnDebugMessageCallback | Handler signature for response to error notification.  <br>  <br>The _Message_ contains the error number and description in JSON format. | `delegate void OnDebugMessageCallback`  <br>`  (String` _Message_) |
| OnDebugMessage | Attach callback for debug messages. | `void OnDebugMessage`  <br>`  (OnDebugMessageCallback` _Callback_) |
| DetachOnDebugMessage | Detach callback for debug messages. | `void DetachOnDebugMessage ()` |




# Datastream  events

This system provides the ability to broadcast messages to subscribers on a per-channel or per-extension basis. Notification of broadcasts on the datastream contain the arbitrary message content in JSON format.



| Function | Description | C# Signature |
| --- | --- | --- |
| SendBroadcast | Broadcasts a message to subscribers in the _Target_ scope, one of "STATE_TARGET_CHANNEL" or "STATE_TARGET_EXTENSION".  <br>_Json_ contains the message body in JSON format. | `UInt16 SendBroadcast`  <br>`  (string` _Target_, `string` _Json_) |
| DatastreamCallback | Handler signature for response to a message notification. | `delegate void DatastreamCallback (DatastreamUpdate` _Update_`)` |
| OnDatastream | Attach callback for message notification events.  <br>  <br>Use `SubscribeToDatastream()` to begin receiving message notifications. | `UInt32 OnDatastream (DatastreamCallback` _Callback_`)` |
| DetachOnDatastream | Attach callback for message notification events, passing the _Handle_ returned from `OnDatastream()`. | `void DetachOnDatastream (UInt32` _Handle_`)` |
| SubscribeToDatastream | Subscribe to message notifications.  <br>  <br>Use after defining and attaching a handler with `OnDatastream()` | `UInt16 SubscribeToDatastream ()` |
| UnsubscribeFromDatastream | Unsubscribe from message notifications. | `UInt16 UnsubscribeFromDatastream ()` |




# State and Configuration Events

Muxy stores predefined and developer-defined state values on a  per-channel or per-extension basis.  
An extension can also define its own configuration options on a per-channel or per-extension basis, and store them separately from the standard state store. Each store contains key-value pairs in a JSON object.

> See [State and Configuration Handling](../../../v1.0/GameLink C--C-- Library/sdk-class/state-config-fns.md). 

Use the following functions to manage subscriptions and define responses to state and configuration update notifications.

- Subscription-management functions must specify the target, one of `CONFIG_TARGET_CHANNEL` or `CONFIG_TARGET_EXTENSION`.
- Update notifications report the type of operation performed. Update operations are: “add”, “remove”, “replace”, “move”, “copy”, “test”.



| Function | Description | C# Signature |
| --- | --- | --- |
| UpdateStateCallback | Handler signature for response to any update-state event. | `delegate void UpdateStateCallback`  <br>`  (StateUpdate` _Response_) |
| OnStateUpdate | Attach callback for state update events.  <br>  <br>Use `SubscribeToStateUpdates()` to begin receiving update notifications. | `UInt32 OnStateUpdate`  <br>`  (UpdateStateCallback` _Callback_) |
| DetachOnStateUpdate | Detach callback for state updates, passing the _Handle_ returned from `OnStateUpdate()`. | `void DetachOnStateUpdate`  <br>`  (UInt32` _Handle_) |
| SubscribeToStateUpdates | Subscribe to state update notifications for channel or extension.  <br>  <br>Use after defining and attaching a handler with `OnStateUpdate()`. | `UInt16 SubscribeToStateUpdates`  <br>`  (string` _Target_) |
| UnsubscribeFromStateUpdates | Unsubscribe from state update notifications. | `UInt16 UnsubscribeFromStateUpdates`  <br>`  (string`  _Target_) |
| UpdateConfigCallback | Handler signature for response to any update-configuration event. | `delegate void 	UpdateConfigCallback`  <br>`  (ConfigUpdate` _Response_) |
| OnConfigUpdate | Attach callback for configuration update events.  <br>  <br>Use `SubscribeToConfigUpdates()` to begin receiving update notifications. | `UInt32 OnConfigUpdate`  <br>`  (UpdateConfigCallback` _Callback_) |
| DetachOnConfigUpdate | Detach callback for configuration updates, passing the _Handle_ returned from `OnConfigUpdate()`. | `void DetachOnConfigUpdate`  <br>`  (UInt32` _Handle_) |
| SubscribeToConfigurationChanges | Subscribe to configuration change notifications.  <br>  <br>Use after defining and attaching a handler with `OnConfigUpdate()`. | UInt16 SubscribeToConfigurationChanges (string _Target_) |
| UnsubscribeFromConfigurationChanges | Unsubscribe from configuration change notifications. | UInt16 UnsubscribeFromConfigurationChanges (string _Target_) |




# Manage Polls and Polling Events

Users with administrative privilege can create and manage viewer polls. Use these `SDK` functions manage subscriptions to polling events, and get poll responses.



| Function | Description | Signature |
| --- | --- | --- |
| CreatePoll | Create and name a poll, with a prompt and list of options.  <br>  <br>Available only when current user has "admin" role. | `UInt16 CreatePoll`  <br>`  (String` _PollId_, `String` _Prompt_, `List< String >` _Options_) |
| DeletePoll | Delete the named poll and all its data.  <br>  <br>Available only when current user has "admin" role | `UInt16 DeletePoll`  <br>`  (String` _PollId_) |
| GetPollCallback | Handler signature for response to `GetPoll()` call. | `delegate void GetPollCallback`  <br>`  (GetPollResponse` _Response_) |
| GetPoll | Retrieve poll results once, and pass them to the _Callback_ handler. | `UInt16 GetPoll`  <br>`  (String` _PollId_, `GetPollCallback` _Callback_) |
| PollUpdateResponseCallback | Handler signature for response to Poll Update. Pass to `OnPollUpdate()` call. | `delegate void PollUpdateResponseCallback`  <br>`  (PollUpdateResponse` _PResp_) |
| OnPollUpdate | Sets callback to handle Poll Update events.  <br>  <br>You must call to `SubscribeToPoll()` to begin receiving Poll Update events. | `UInt32 OnPollUpdate`  <br>`  (PollUpdateResponseCallback` _Callback_) |
| DetachOnPollUpdate | Detach callback for Poll Update events, using _Handle_ returned from  `OnPollUpdate()` call. | `void DetachOnPollUpdate`  <br>` (UInt32` _Handle_) |
| SubscribeToPoll | Subscribe to a named poll.  <br>  <br>Before subscribing,  use `OnPollUpdate ()` to set the callback that handles polling events. | `UInt16 SubscribeToPoll`  <br>` (String` _PollId_) |
| UnsubscribeFromPoll | Unsubscribe from the named poll. | `UInt16 UnsubscribeFromPoll`  <br>`  (String` _PollId_) |




# Twitch Bit Transactions

The following `SDK` functions let you manage Twitch Bit Transactions from extension viewers. 



| Function | Description | C# Signature |
| --- | --- | --- |
| SubscribeToSKU | Subscribe to SKU purchase notifications. | `UInt16 SubscribeToSKU`  <br>` (string` _SKU_) |
| UnsubscribeFromSKU | Unsubscribe from SKU purchase notifications. | `UInt16 UnsubscribeFromSKU`  <br>`  (string` _SKU_) |
| SubscribeToAllPurchases | Subscribe to all Twitch Bit Purchase notifications. | `UInt16 SubscribeToAllPurchases ()` |
| UnsubscribeFromAllPurchases | Unsubscribe from all Twitch Bit Purchase notifications. | `UInt16 UnsubscribeFromAllPurchases ()` |
| TransactionCallback | Handler signature for response to purchase events. Pass to `OnTransaction()` call. | `delegate void 	TransactionCallback`  <br>` (Transaction` _Purchase_) |
| OnTransaction | Sets callback for Twitch Bit Purchasing events.  <br>  <br>You must subscribe by calling to `SubscribeToSKU()` or `SubscribeToAllPurchases()` to begin receiving purchase events. | `UInt32 OnTransaction`  <br>`  (TransactionCallback` _Callback_) |
| DetachOnTransaction | Detach callback for Twitch Bit Purchases  using _Handle_ returned from `OnTransaction()` call. | `void DetachOnTransaction`  <br>\`  (UInt32 _Handle_) |
| GetOutstandingTransactionsCallback | Handler signature for response to `GetOutstandingTransactions()` calls. | `delegate void 	GetOutstandingTransactionsCallback`  <br>` (OutstandingTransactions` _Transactions_) |
| GetOutstandingTransactions | Get all outstanding transactions that need validation. | `UInt16 GetOutstandingTransactions`  <br>`  (String` _SKU_, `GetOutstandingTransactionsCallback` _Callback_) |
| RefundTransactionByID | Refund given transaction for user. | `UInt16 RefundTransactionByID`  <br>` (String` _TxId_, `String` _UserId_) |
| RefundTransactionBySKU | Refund given transaction for user. | `UInt16 RefundTransactionBySKU`  <br>`  (String` _SKU_, `String` _UserId_) |
| ValidateTransaction | Validate given transaction. | `UInt16 ValidateTransaction`  <br>`  (String` _TxId_, `String` _Details_) |



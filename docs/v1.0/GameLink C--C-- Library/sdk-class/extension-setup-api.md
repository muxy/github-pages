---
title: "Extension Setup API"
slug: "extension-setup-api"
excerpt: "These functions handle authentication and set up general server communication."
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Wed Sep 29 2021 16:31:25 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Wed Jan 12 2022 18:01:28 GMT+0000 (Coordinated Universal Time)"
---


| Function | Description | C# Signature |
| --- | --- | --- |
| SDK | Constructor. Instantiates the SDK class in the current client. | `MuxyGameLink.SDK.SDK `  <br>`  (String` _ClientId_) |
| ConnectionAddress | Generates connection address for WebSocket.  <br>  <br>_Stage_ is one of `Production` or `Sandbox` (the development/debug environment). | `String ConnectionAddress`  <br>`    (Stage` _Stage_) |
| IsAuthenticated | Checks current authentication status. | `bool  IsAuthenticated ()` |
| AuthenticateWithPIN | Authenticate with a PIN.  <br>  <br>Executes _Callback_ on completion. | `UInt16 AuthenticateWithPIN`  <br>`   (string` _PIN_,  <br>`   AuthenticationCallback` _Callback_) |
| AuthenticateWithRefreshToken | Authenticate with refresh token, which is obtained from initially authenticating with a PIN.  <br>  <br>Executes _Callback_ on completion. | `UInt16 AuthenticateWithRefreshToken`  <br>`  (string` _RefreshToken_,  <br>`   AuthenticationCallback`  _Callback_) |
| AuthenticationCallback | Handler signature for response to any authentication call. | `delegate void AuthenticationCallback`  <br>`  (AuthenticationResponse` _Payload_) |
| ReceiveMessage | Receive a message from a WebSocket for processing.  <br>  <br>Returns true if message was received correctly. | `bool ReceiveMessage`  <br>`  (string` _Message_) |
| ForEachPayload | Executes _Callback_ on each payload waiting to be sent.  <br>  <br>Generally used to send the payload through a WebSocket. | `void  ForEachPayload`  <br>`  (PayloadCallback` _Callback_) |
| PayloadCallback | Handler signature for response to `ForEachPayload()` call. | `delegate void PayloadCallback`  <br>`  (string` _Payload_) |



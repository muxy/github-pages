# Extension Setup API

These functions handle authentication and set up general server communication.

[block:parameters]
{
  "data": {
    "h-0": "Function",
    "h-1": "Description",
    "0-0": "SDK",
    "h-2": "C# Signature",
    "0-1": "Constructor. Instantiates the SDK class in the current client.",
    "0-2": "`MuxyGameLink.SDK.SDK `\n`  (String` *ClientId*)",
    "1-0": "ConnectionAddress",
    "1-1": "Generates connection address for WebSocket. \n\n*Stage* is one of `Production` or `Sandbox` (the development/debug environment).",
    "1-2": "`String ConnectionAddress` \n`    (Stage` *Stage*)",
    "2-2": "`bool  IsAuthenticated ()`",
    "2-0": "IsAuthenticated",
    "2-1": "Checks current authentication status.",
    "4-2": "`UInt16 AuthenticateWithRefreshToken` \n`  (string` *RefreshToken*,\n`   AuthenticationCallback`  *Callback*)",
    "6-2": "`bool ReceiveMessage` \n`  (string` *Message*)",
    "7-2": "`void  ForEachPayload` \n`  (PayloadCallback` *Callback*)",
    "4-0": "AuthenticateWithRefreshToken",
    "4-1": "Authenticate with refresh token, which is obtained from initially authenticating with a PIN.\n\nExecutes *Callback* on completion.",
    "6-0": "ReceiveMessage",
    "6-1": "Receive a message from a WebSocket for processing.\n\nReturns true if message was received correctly.",
    "7-0": "ForEachPayload",
    "7-1": "Executes *Callback* on each payload waiting to be sent. \n\nGenerally used to send the payload through a WebSocket.",
    "5-0": "AuthenticationCallback",
    "5-1": "Handler signature for response to any authentication call.",
    "5-2": "`delegate void AuthenticationCallback` \n`  (AuthenticationResponse` *Payload*)",
    "8-0": "PayloadCallback",
    "8-1": "Handler signature for response to `ForEachPayload()` call.",
    "8-2": "`delegate void PayloadCallback` \n`  (string` *Payload*)",
    "3-0": "AuthenticateWithPIN",
    "3-1": "Authenticate with a PIN.\n\nExecutes *Callback* on completion.",
    "3-2": "`UInt16 AuthenticateWithPIN`\n`   (string` *PIN*,\n`   AuthenticationCallback` *Callback*)"
  },
  "cols": 3,
  "rows": 9
}
[/block]
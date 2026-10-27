# Authentication

The WebSocket protocol supports authorization using PIN or JWT.

Users (game players and Twitch streamers) can authenticate with two-factor authentication, using a server-generated PIN code.
To implement an authentication workflow:

* Request a PIN code from Muxy, based on the broadcaster's Twitch Client ID.
* Display the PIN in the broadcaster-only *config* or *live* Twitch Extension.
* The broadcaster enters the code into the game client to authorize the game to perform actions on their behalf.
* The game client sends the PIN to the server for verification.

# Generating a PIN

The GameLink library uses a PIN to associate the current user with their Twitch account.

An extension running on the Twitch config or live pages can send an unauthorized request to receive a **case-sensitive** PIN. The request is authenticated with the user's Client ID, but does not require an **Authorization** header.

[block:code]
{
  "codes": [
    {
      "code": "const medkit = new Muxy.SDK();\nawait medkit.loaded();\nconst { pin } = medkit.getAuthPin();",
      "language": "javascript",
      "name": "MEDKit SDK"
    },
    {
      "code": "curl --request POST \\\n  --url https://api.muxy.io/v1/e/gamelink/pin \\\n  --header 'authorization: <Client ID> <Broadcaster JWT>' \\\n  --header 'content-type: application/json'\n  \n{ pin: \"\" }",
      "language": "curl",
      "name": "REST"
    }
  ]
}
[/block]

The response is a PIN, not a JWT. You use this PIN to authenticate the user and receive an authorization JWT. You then use that JWT for future authentications. The user never needs to re-enter their PIN.

## Receiving Authentication Updates

There is an "authentication" event topic. A client can subscribe to "authentication" events using the `subscribe` action.

[block:code]
{
  "codes": [
    {
      "code": "{\n  \"action\": \"subscribe\",\n  \"params\": {\n    \"request_id\": 234,\n    \"target\": \"authentication\"\n  }\n}",
      "language": "json",
      "name": "Subscription request"
    }
  ]
}
[/block]

**Response**

If the operation succeeds, the response confirms success and the server begin sending updates messages.

[block:code]
{
  "codes": [
    {
      "code": "{\n  \"meta\": {\n    \"request_id\": 234,\n    \"action\": \"subscribe\",\n    \"target\": \"authentication\",\n    \"timestamp\": 1583777221501\n  },\n\n  \"data\": {\n    \"ok\": true\n  }\n}",
      "language": "json",
      "name": "Response to successful subscription request"
    }
  ]
}
[/block]

If the operation fails, the server responds with an error notification in the following format.

[block:code]
{
  "codes": [
    {
      "code": "{\n  \"meta\": {\n    \"request_id\": 234,\n    \"action\": \"subscribe\",\n    \"target\": \"authentication\",\n    \"timestamp\": 1583777221501\n  },\n\n  \"errors\": [\n    {\n      \"status\": 500,\n      \"title\": \"Internal Service Error\",\n      \"detail\": \n        \"An internal error prevented the server from processing the request\"\n    }\n  ]\n}",
      "language": "json",
      "name": "Response to failed subscription request"
    }
  ]
}
[/block]

# Authenticating a User

Use the `authenticate` action to authorize a user's access to the Muxy server.
You must provide either the user-entered PIN from above or a stored JWT refresh token to authenticate the user and allow access to other actions.

## User-entered PIN authentication

**Request**

If the user has not yet been authenticated, send a user-entered 6-character PIN code that matches one displayed in the extension, along with the Extension Client ID.

[block:code]
{
  "codes": [
    {
      "code": "{\n  \"action\": \"authenticate\",\n  \"params\": {\n    \"request_id\": 333\n  },\n\n  \"data\": {\n    \"pin\": \"pZV4Se\",\n    \"client_id\": \"extension-client-id\"\n  }\n}",
      "language": "json",
      "name": "Request authentication with PIN"
    }
  ]
}
[/block]

**Response**

If the code matches, the server updates the connection's access rights and sends a response that contains a signed JWT access token (`jwt`) for use in future connections. It also returns a refresh token (`refresh`) that can be exchanged in future connections for a valid JWT access token.

[block:code]
{
  "codes": [
    {
      "code": "{\n  \"meta\": {\n    \"request_id\": 333,\n    \"action\": \"authenticate\",\n    \"target\": \"\",\n    \"timestamp\": 1583777666077\n  },\n\n  \"data\": {\n    \"jwt\": \"eyJhbG...\"\n    \"refresh\": \"eyJhbG...\"\n  }\n}",
      "language": "json",
      "name": "Success response"
    }
  ]
}
[/block]

* If the code does not match, the connection's access rights remain unchanged and the server responds with an error message.

[block:code]
{
  "codes": [
    {
      "code": "{\n  \"meta\": {\n    \"request_id\": 333,\n    \"action\": \"authenticate\",\n    \"channel\": \"\",\n    \"timestamp\": 1583777666077\n  },\n\n  \"errors\": [\n    {\n      \"status\": 400,\n      \"title\": \"Bad Request\",\n      \"detail\": \"The provided PIN is invalid or expired\"\n    }\n  ]\n}",
      "language": "json",
      "name": "Failure response"
    }
  ]
}
[/block]

## Returned Tokens

A successful authentication refresh returns two tokens. One authorizes access ;

* 'jwt' is a token you can use to authorize *access* to Muxy functionality
* `refresh` is a different token that you use to obtain a new access token when the current one expires.

The JWT access token returned from the PIN authentication process is issued for the specific channel and user with the 'broadcaster' role. Use this JWT to make calls into the [Muxy REST API](https://docs.muxy.io/reference/medkit-rest-api).
This access token should not be stored on disk and never shared as it is not possible to revoke an access token after it has been issued.

The access token expires after 7 days. Use the returned `refresh` token to generate new one.

The refresh token returned from the PIN authentication process can only be used to authenticate the same user again in the future. It is valid for 365 days after issuance, but may be revoked at any time. You can store this token on disk, but it should not be shared.

To authenticate a user with a refresh token, use the same 'authenticate' method as before, passing the refresh token and Extension Client ID.

[block:code]
{
  "codes": [
    {
      "code": "{\n  \"action\": \"authenticate\",\n  \"params\": {\n    \"request_id\": 444\n  },\n\n  \"data\": {\n    \"refresh\": \"eyJhbG...\",\n    \"client_id\": \"your-client-id\"\n  }\n}",
      "language": "json",
      "name": "Request to authenticate with refresh token"
    }
  ]
}
[/block]

**Refresh response**

If the refresh token is valid and has not been revoked, the response contains a new JWT access token that can be used for future REST calls, as well as a new refresh token. The new refresh token has an updated expiration and should be used for future reconnections.

[block:code]
{
  "codes": [
    {
      "code": "{\n  \"meta\": {\n    \"request_id\": 444,\n    \"action\": \"authenticate\",\n    \"channel\": \"\",\n    \"timestamp\": 1583779685222\n  },\n\n  \"data\": {\n    \"jwt\": \"eyJhbG...\",\n    \"refresh\": \"eyJhbG...\"\n  }\n}",
      "language": "json",
      "name": "Success response"
    }
  ]
}
[/block]

If the refresh token has expired or otherwise cannot be verified, the response contains an error message.

[block:code]
{
  "codes": [
    {
      "code": "{\n  \"meta\": {\n    \"request_id\": 444,\n    \"action\": \"authenticate\",\n    \"channel\": \"\",\n    \"timestamp\": 1583779685222\n  },\n\n  \"errors\": [\n    {\n      \"status\": 400,\n      \"title\": \"Bad Request\",\n      \"detail\": \"Invalid refresh token\"\n    }\n  ]\n}",
      "language": "json",
      "name": "Failure response"
    }
  ]
}
[/block]
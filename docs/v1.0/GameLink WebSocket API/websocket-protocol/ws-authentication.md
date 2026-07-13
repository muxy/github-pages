---
title: "Authentication"
slug: "ws-authentication"
excerpt: "The WebSocket protocol supports authorization using PIN or JWT."
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Tue Oct 05 2021 16:47:44 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Wed Jan 12 2022 18:10:59 GMT+0000 (Coordinated Universal Time)"
---
Users (game players and Twitch streamers) can authenticate with two-factor authentication, using a server-generated PIN code.  
To implement an authentication workflow:

- Request a PIN code from Muxy, based on the broadcaster's Twitch Client ID. 
- Display the PIN in the broadcaster-only _config_ or _live_ Twitch Extension. 
- The broadcaster enters the code into the game client to authorize the game to perform actions on their behalf. 
- The game client sends the PIN to the server for verification.

# Generating a PIN

The GameLink library uses a PIN to associate the current user with their Twitch account.

An extension running on the Twitch config or live pages can send an unauthorized request to receive a **case-sensitive** PIN. The request is authenticated with the user's Client ID, but does not require an **Authorization** header. 

```javascript MEDKit SDK
const medkit = new Muxy.SDK();
await medkit.loaded();
const { pin } = medkit.getAuthPin();
```
```curl REST
curl --request POST \
  --url https://api.muxy.io/v1/e/gamelink/pin \
  --header 'authorization: <Client ID> <Broadcaster JWT>' \
  --header 'content-type: application/json'
  
{ pin: "" }
```

The response is a PIN, not a JWT. You use this PIN to authenticate the user and receive an authorization JWT. You then use that JWT for future authentications. The user never needs to re-enter their PIN.

## Receiving Authentication Updates

There is an "authentication" event topic. A client can subscribe to "authentication" events using the `subscribe` action.

```json Subscription request
{
  "action": "subscribe",
  "params": {
    "request_id": 234,
    "target": "authentication"
  }
}
```

**Response**

If the operation succeeds, the response confirms success and the server begin sending updates messages.

```json Response to successful subscription request
{
  "meta": {
    "request_id": 234,
    "action": "subscribe",
    "target": "authentication",
    "timestamp": 1583777221501
  },

  "data": {
    "ok": true
  }
}
```

If the operation fails, the server responds with an error notification in the following format.

```json Response to failed subscription request
{
  "meta": {
    "request_id": 234,
    "action": "subscribe",
    "target": "authentication",
    "timestamp": 1583777221501
  },

  "errors": [
    {
      "status": 500,
      "title": "Internal Service Error",
      "detail": 
        "An internal error prevented the server from processing the request"
    }
  ]
}
```

# Authenticating a User

Use the `authenticate` action to authorize a user's access to the Muxy server.  
You must provide either the user-entered PIN from above or a stored JWT refresh token to authenticate the user and allow access to other actions.

## User-entered PIN authentication

**Request**

If the user has not yet been authenticated, send a user-entered 6-character PIN code that matches one displayed in the extension, along with the Extension Client ID. 

```json Request authentication with PIN
{
  "action": "authenticate",
  "params": {
    "request_id": 333
  },

  "data": {
    "pin": "pZV4Se",
    "client_id": "extension-client-id"
  }
}
```

**Response**

If the code matches, the server updates the connection's access rights and sends a response that contains a signed JWT access token (`jwt`) for use in future connections. It also returns a refresh token (`refresh`) that can be exchanged in future connections for a valid JWT access token. 

```json Success response
{
  "meta": {
    "request_id": 333,
    "action": "authenticate",
    "target": "",
    "timestamp": 1583777666077
  },

  "data": {
    "jwt": "eyJhbG..."
    "refresh": "eyJhbG..."
  }
}
```

- If the code does not match, the connection's access rights remain unchanged and the server responds with an error message.

```json Failure response
{
  "meta": {
    "request_id": 333,
    "action": "authenticate",
    "channel": "",
    "timestamp": 1583777666077
  },

  "errors": [
    {
      "status": 400,
      "title": "Bad Request",
      "detail": "The provided PIN is invalid or expired"
    }
  ]
}
```

## Returned Tokens

A successful authentication refresh returns two tokens. One authorizes access ; 

- 'jwt' is a token you can use to authorize _access_ to Muxy functionality
- `refresh` is a different token that you use to obtain a new access token when the current one expires.

The JWT access token returned from the PIN authentication process is issued for the specific channel and user with the 'broadcaster' role. Use this JWT to make calls into the [Muxy REST API](../../../v1.0/REST API/medkit-rest-api.md).  
This access token should not be stored on disk and never shared as it is not possible to revoke an access token after it has been issued.

The access token expires after 7 days. Use the returned `refresh` token to generate new one. 

The refresh token returned from the PIN authentication process can only be used to authenticate the same user again in the future. It is valid for 365 days after issuance, but may be revoked at any time. You can store this token on disk, but it should not be shared. 

To authenticate a user with a refresh token, use the same 'authenticate' method as before, passing the refresh token and Extension Client ID.

```json Request to authenticate with refresh token
{
  "action": "authenticate",
  "params": {
    "request_id": 444
  },

  "data": {
    "refresh": "eyJhbG...",
    "client_id": "your-client-id"
  }
}
```

**Refresh response**

If the refresh token is valid and has not been revoked, the response contains a new JWT access token that can be used for future REST calls, as well as a new refresh token. The new refresh token has an updated expiration and should be used for future reconnections.

```json Success response
{
  "meta": {
    "request_id": 444,
    "action": "authenticate",
    "channel": "",
    "timestamp": 1583779685222
  },

  "data": {
    "jwt": "eyJhbG...",
    "refresh": "eyJhbG..."
  }
}
```

If the refresh token has expired or otherwise cannot be verified, the response contains an error message.

```json Failure response
{
  "meta": {
    "request_id": 444,
    "action": "authenticate",
    "channel": "",
    "timestamp": 1583779685222
  },

  "errors": [
    {
      "status": 400,
      "title": "Bad Request",
      "detail": "Invalid refresh token"
    }
  ]
}
```

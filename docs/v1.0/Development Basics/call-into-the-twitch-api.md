---
title: "Call into the Twitch API"
slug: "call-into-the-twitch-api"
excerpt: ""
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Wed Sep 15 2021 16:42:53 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Wed Nov 03 2021 23:36:15 GMT+0000 (Coordinated Universal Time)"
---
Twitch provides a REST API with varying degrees of functionality. You can call into the Twitch API directly from within an extension. The full list of Twitch API endpoints can be found on the official [Twitch API docs site](https://dev.twitch.tv/docs/api/).

MEDKit also provides a convenience wrapper for some of the more common use cases.

# Requesting Directly

You can use any JavaScript library or browser-native method to make a request to the Twitch API endpoints, passing your Extension Client ID as authorization.

For example:

```javascript
window.fetch('https://api.twitch.tv/helix/users?login=twitch', {
  headers: {
    'Client-ID': '<extension client id>'
  }
})
.then((response) => response.json())
.then(({ data }) => {
  console.log(data[0]);
})
.catch(() => {
  console.error('Failed looking up user info');
});
```

## MEDKit Wrapper

MEDKit is initialized with your authorization credentials, so once you've created a Twitch client, you can call certain Twitch functions directly.

```javascript
const client = new Muxy.TwitchClient();
client.getTwitchUsersByID(['126955211'])
  .then((users) => {
    console.log(users[0]);
  });
```

The following functions are available to use through a `TwitchClient` instance.

| Call                                | Description                                                                  | Example                                                                                                                             |
| :---------------------------------- | :--------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------- |
| `TwitchClient.getTwitchUsers()`     | Takes an array of usernames and returns an array of full user objects.       | `js const client = new Muxy.TwitchClient(); client.getTwitchUsers(['liriki', 'muxy']).then(users => {   console.log(users); }); `   |
| `TwitchClient.getTwitchUsersByID()` | Takes an array of Twitch user ids and returns an array of full user objects. | `js const client = new Muxy.TwitchClient(); client.getTwitchUsersByID(['1234', '5678']).then(users => {   console.log(users); }); ` |

### Responses

A request to a Twitch endpoint returns a JSON data object like the following:

```json
{
  "broadcaster_type": "partner",
  "description": "Twitch is the world's leading video platform and community for gamers with more than 100 million visitors per month. Our mission is to connect gamers around the world by allowing them to broadcast, watch, and chat from everywhere they play.",
  "display_name": "Twitch",
  "id": "12826",
  "login": "twitch",
  "offline_image_url": "",
  "profile_image_url": "https://static-cdn.jtvnw.net/jtv_user_pictures/twitch-profile_image-8a8c5be2e3b64a9a-300x300.png",
  "type": "",
  "view_count": 214488775
}
```

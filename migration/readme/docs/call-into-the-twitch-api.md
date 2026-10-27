# Call into the Twitch API

Twitch provides a REST API with varying degrees of functionality. You can call into the Twitch API directly from within an extension. The full list of Twitch API endpoints can be found on the official [Twitch API docs site](https://dev.twitch.tv/docs/api/).

MEDKit also provides a convenience wrapper for some of the more common use cases.

# Requesting Directly

You can use any JavaScript library or browser-native method to make a request to the Twitch API endpoints, passing your Extension Client ID as authorization.

For example:

[block:code]
{
  "codes": [
    {
      "code": "window.fetch('https://api.twitch.tv/helix/users?login=twitch', {\n  headers: {\n    'Client-ID': '<extension client id>'\n  }\n})\n.then((response) => response.json())\n.then(({ data }) => {\n  console.log(data[0]);\n})\n.catch(() => {\n  console.error('Failed looking up user info');\n});",
      "language": "javascript"
    }
  ]
}
[/block]

## MEDKit Wrapper

MEDKit is initialized with your authorization credentials, so once you've created a Twitch client, you can call certain Twitch functions directly.

[block:code]
{
  "codes": [
    {
      "code": "const client = new Muxy.TwitchClient();\nclient.getTwitchUsersByID(['126955211'])\n  .then((users) => {\n    console.log(users[0]);\n  });",
      "language": "javascript"
    }
  ]
}
[/block]

The following functions are available to use through a `TwitchClient` instance.

[block:parameters]
{
  "data": {
    "h-0": "Call",
    "h-1": "Description",
    "h-2": "Example",
    "0-0": "`TwitchClient.getTwitchUsers()`",
    "0-1": "Takes an array of usernames and returns an array of full user objects.",
    "0-2": "```js\nconst client = new Muxy.TwitchClient();\nclient.getTwitchUsers(['liriki', 'muxy']).then(users => {\n  console.log(users);\n});\n```",
    "1-0": "`TwitchClient.getTwitchUsersByID()`",
    "1-1": "Takes an array of Twitch user ids and returns an array of full user objects.",
    "1-2": "```js\nconst client = new Muxy.TwitchClient();\nclient.getTwitchUsersByID(['1234', '5678']).then(users => {\n  console.log(users);\n});\n```"
  },
  "cols": 3,
  "rows": 2
}
[/block]

### Responses

A request to a Twitch endpoint returns a JSON data object like the following:

[block:code]
{
  "codes": [
    {
      "code": "{\n  \"broadcaster_type\": \"partner\",\n  \"description\": \"Twitch is the world's leading video platform and community for gamers with more than 100 million visitors per month. Our mission is to connect gamers around the world by allowing them to broadcast, watch, and chat from everywhere they play.\",\n  \"display_name\": \"Twitch\",\n  \"id\": \"12826\",\n  \"login\": \"twitch\",\n  \"offline_image_url\": \"\",\n  \"profile_image_url\": \"https://static-cdn.jtvnw.net/jtv_user_pictures/twitch-profile_image-8a8c5be2e3b64a9a-300x300.png\",\n  \"type\": \"\",\n  \"view_count\": 214488775\n}",
      "language": "json"
    }
  ]
}
[/block]
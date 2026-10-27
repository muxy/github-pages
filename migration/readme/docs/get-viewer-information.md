# Get Viewer Information

Access information about the current viewer, or all users who have shared their information.

You can always access basic identifying information for the current viewer.

Users of your extension have the option to share their Twitch identity with you.
MEDKit lets an administrator request a list of all users who are currently sharing this information.

> This list is not exposed to users with `viewer` or `broadcaster` role. It is available only to users with the `admin` role for the extension.

# Get Current Viewer Information

Use the JavaScript `SDK.user`  object to access information on the current viewer.
The `user` object has these properties:

[block:parameters]
{
  "data": {
    "0-0": "`channelID`",
    "h-0": "Name",
    "h-1": "Description",
    "0-1": "String. The numeric ID of the channel the user is currently watching.",
    "1-0": "`twitchJWT`",
    "1-1": "Optional. String. The user's JWT as received from the Twitch Extension helper, or \"undefined\" if the viewer has not shared their Twitch ID with the extension.",
    "2-0": "`twitchID`",
    "2-1": "String. The user's Twitch ID if it has been shared with the extension, `null` otherwise.",
    "3-0": "`twitchOpaqueID`",
    "3-1": "String. The user's unique identifier if the Twitch ID has not been shared with the extension, `null` otherwise."
  },
  "cols": 2,
  "rows": 4
}
[/block]

For example:

[block:code]
{
  "codes": [
    {
      "code": "const medkit = new Muxy.SDK();\nawait medkit.loaded();\n\nconsole.log(`Viewer ${  sdk.user.twitchID ? 'has' : 'has not' } shared their Twitch ID with the extension`);\nconsole.log(`They are currently ${sdk.user.buffer}ms behind the stream.`);",
      "language": "javascript"
    }
  ]
}
[/block]

# Get Twitch IDs of Extension Users

To request the current list of shared Twitch IDs, call `sdk.getExtensionUsers()`. The functionality is only available to broadcasters who have the `admin` role, and (in production) only on Muxy's "admin" pages. You cannot make the call from Twitch's Creator Dashboard.

For example:

[block:code]
{
  "codes": [
    {
      "code": "const opts = new Muxy.DebuggingOptions();\nopts.role('admin');\nMuxy.debug(opts);\n\nconst medkit = new Muxy.SDK();\nmedkit.loaded().then(() => {\n  medkit.getExtensionUsers().then((resp) => {\n    resp.results.forEach((u) => {\n      console.log(u.twitch_id);\n    });\n\n    console.log(`There are ${resp.next === '0' ? 'no ' : ''}more results available`);\n  });\n});",
      "language": "javascript",
      "name": "Get users' Twitch IDs"
    }
  ]
}
[/block]

The JSON response from this method has the following structure:

[block:code]
{
  "codes": [
    {
      "code": "{\n  next: '0',\n  results: [\n    { twitch_id: '12345' },\n    { twitch_id: '23456' },\n    { twitch_id: '34567' }\n  ]\n}",
      "language": "json",
      "name": "Print results"
    }
  ]
}
[/block]

## Iterating for large numbers of users

The `getExtensionUsers()` call returns at most 1,000 objects in its response. If more than 1,000 users have shared their identity with your extension, you have to make more calls to iterate through 1000-user pages. Each page is indexed, and the  `getExtensionUsers()`  method takes an optional page index parameter.

The following example demonstrates the basic method for iterating through current users.  The `next` field in the response to each call contains the 0-based page index for the next page, or the value `"0"` if all
results have been returned. Pass the `next` value directly to `getExtensionUsers()` to get the next page of up to 1,000 users. Use a `next` value of 0 to begin the iteration.

[block:code]
{
  "codes": [
    {
      "code": "const opts = new Muxy.DebuggingOptions();\nopts.role('admin');\nMuxy.debug(opts);\n\nconst medkit = new Muxy.SDK();\nmedkit.loaded().then(() => {\n  function getNextUsers(cursor) {\n    medkit.getExtensionUsers(cursor).then((resp) => {\n      resp.results.forEach((u) => {\n        console.log(u.twitch_id);\n      });\n\n      if (resp.next !== '0') {\n       // this example does not limit the number of responses\n        getNextUsers(resp.next);\n      }\n    });\n  }\n\n  getNextUsers('0');\n});",
      "language": "javascript",
      "name": "Iterate through users"
    }
  ]
}
[/block]

[block:callout]
{
  "type": "warning",
  "title": "Be careful!",
  "body": "For very successful extensions, you can easily overload your connection if you do not further limit the number of calls.\nIf a million users have shared their ID with your extension, this code will very quickly make 1,000 API requests."
}
[/block]
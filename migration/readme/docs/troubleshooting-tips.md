# Troubleshooting Tips

Some tips for avoiding common problems.

* [Troubleshoot authorization mismatch](#troubleshoot-authorization-mismatch)
* [Check the channel](#check-the-channel)
* [Troubleshoot data state operations](#troubleshoot-data-state-operations)
* [Troubleshoot user voting](#troubleshoot-user-voting)
* [Ensure correct time settings](#ensure-correct-time-settings)

[block:callout]
{
  "type": "info",
  "title": "",
  "body": "You can also get help from Muxy and the developer community by joining the [Muxy Developer Support Forum](https://discord.gg/ssepDKxXYX) on Discord."
}
[/block]

# Troubleshoot authorization mismatch

A JWT is issued for a specific environment:

* Requests for the production environment are made to `api.muxy.io`
* Requests for the development or staging environment are made to `sandbox.api.muxy.io`

If the token you are using to authorize a request does not match the target environment, the request fails with an error like the following:

[block:callout]
{
  "type": "warning",
  "title": "Request authorization failure",
  "body": "Status: **403 forbidden**\nBody:  `{ \"reason\": \"User was unauthorized to access this resource\", \"info\": \"Allowed stage mismatch\" }`"
}
[/block]

This typically happens when you switch between the staging and production environments using a sandbox-only token. You must obtain a new token for the production environment, using the PIN authorization workflow.

* For a Unity game, see the example in the [Unity GameLink Tutorial](https://docs.muxy.io/docs/unity-gamelink-tutorial#getting-a-gamelink-pin).
* For other development platforms, see one of these recipes:

[block:tutorial-tile]
{
  "title": "GameLink Authentication",
  "emoji": "👤",
  "backgroundColor": "#2c4251",
  "slug": "gamelink-authentication",
  "_id": "617140d21320a601d8232ad9",
  "id": "617140d21320a601d8232ad9",
  "link": "https://docs.muxy.io/v1.0/recipes/gamelink-authentication",
  "align": "default"
}
[/block]

[block:tutorial-tile]
{
  "title": "Generate a Production JWT",
  "emoji": "📼",
  "backgroundColor": "#c1c1c1",
  "slug": "generate-a-production-jwt",
  "_id": "61523714b8f20a0010f16e2d",
  "id": "61523714b8f20a0010f16e2d",
  "link": "https://docs.muxy.io/v1.0/recipes/generate-a-production-jwt",
  "align": "default"
}
[/block]

To check the target environment of a JWT you are using to authorize calls:

1. Look at the token in the **Authorization** header of any request to an authenticated endpoint (that is, any endpoint other than `auth`).  The header contains your client ID (a number) followed by the JWT:
   "Authorization: *extension-id* *jwt*". The JWT is an alphanumeric string that starts with `eyJ`.
2. Copy out the JWT part and enter it into [JWT.IO](https://jwt.io/).
3. Look for the `allowed_stage` field in the payload area. If the value does not match the expected stage, then this is an error.

* In a sandbox-only JWT, the `allowed_stage` value is "sandbox", which causes the "Allowed stage mismatch" in the production environment.
* In a production-stage JWT, the field does not exist, which causes an error in the sandbox environment.

# Check the channel

If you receive data for a channel other than the one you expect, you can check the channel encoded in the JWT you are using to authorize requests.

To check whether a JWT is generated for the wrong channel:

1. Look at the token in the **Authorization** header of any request to an authenticated endpoint (that is, any endpoint other than `auth`).  The header looks like this: "Authorization: <extension-id> <jwt>". The JWT value should start with 'eyJ'.
2. Copy out the JWT part and enter it into [JWT.IO](https://jwt.io/).
3. Check the 'channel\_id' and 'user\_id' fields to make sure they match what is expected.

The `channel_id` value is the same as the `user_id` of the broadcaster of that channel.

# Troubleshoot data state operations

If you are getting unexpected results when accessing stored data values, check that values are actually getting set in the proper store. The different stores for state and configuration data have specific authorization requirements.

* The caller must have the `broadcaster` role to successfully write configuration values, or to set values in the `channel_state` store.
* The broadcaster must be the owner of an extension to set values in the `extension_state` store.

If state values are not found or are incorrect, they might have been set without proper authorization, or they might have been written to the wrong data store.
You can retrieve all state values to make sure that a state value was actually set as expected, and is in the correct state store.

[block:code]
{
  "codes": [
    {
      "code": "js medkit.getAllState().then(state => { console.log(state); });\njs medkit.getAllConfig().then(config=> { console.log(state); });",
      "language": "text",
      "name": "Check all stored data values"
    }
  ]
}
[/block]

[block:callout]
{
  "type": "info",
  "body": "See the [Data Tracking](https://docs.muxy.io/docs/data-tracking) guides for complete details of the scope and authorization requirements for the different data stores."
}
[/block]

# Troubleshoot user voting

A common mismatch with voting occurs when viewers vote using a stale poll ID.

Consider a game that intermittently runs a poll with `poll_id="rps"` to play Rock Paper Scissors against the audience.  Every 5 minutes, the game writes to state and then broadcasts a message, which pops up a poll on the extension interface. After one minute, it gets the results.

This flow will count all of the votes in the `rps` poll, including votes from previous runs, and votes that were cast between runs. Even if you delete the poll after the run, users can still cast votes using that ID, and those votes become "stale" votes in any future run that you create using the same ID.

The poll manager can send a DELETE request to clear data from the log for a given poll ID. (See [Poll Management](https://docs.muxy.io/reference/poll-managment) for details of the REST API.)\
To ensure that each poll begins with a clean slate, the game should do this immediately BEFORE creating a new poll with the same ID.   (It's ok to delete an ID that does not exist.)

The correct sequence of operations is: Delete poll ID -> Create new poll with ID -> Wait for votes -> Get results

# Ensure correct time settings

Sometimes users' system clocks can't be trusted to have the correct time. For
example, users who live near a time-zone border might manually set their time zone
and adjust the system clock by an hour.

To avoid problems, MEDKit provides the function `getOffsetDate()` to get a more accurate date object.
The SDK communicates with the server on load to calculate the time offset without reference to the user's system clock.

The function takes no arguments, and returns a Date object representing the real time.

[block:code]
{
  "codes": [
    {
      "code": "medkit.getOffsetDate();",
      "language": "javascript"
    }
  ]
}
[/block]
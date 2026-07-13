---
title: "Troubleshooting Tips"
slug: "troubleshooting-tips"
excerpt: "Some tips for avoiding common problems."
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Wed Sep 29 2021 21:06:37 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Wed Feb 02 2022 19:37:51 GMT+0000 (Coordinated Universal Time)"
---
- [Troubleshoot authorization mismatch](#troubleshoot-authorization-mismatch)
- [Check the channel](#check-the-channel)
- [Troubleshoot data state operations](#troubleshoot-data-state-operations)
- [Troubleshoot user voting](#troubleshoot-user-voting)
- [Ensure correct time settings](#ensure-correct-time-settings)

> 📘 You can also get help from Muxy and the developer community by joining the [Muxy Developer Support Forum](https://discord.gg/ssepDKxXYX) on Discord.

# Troubleshoot authorization mismatch

A JWT is issued for a specific environment:

- Requests for the production environment are made to `api.muxy.io`
- Requests for the development or staging environment are made to `sandbox.api.muxy.io`

If the token you are using to authorize a request does not match the target environment, the request fails with an error like the following:

> 🚧 Request authorization failure
> 
> Status: **403 forbidden**  
> Body:  `{ "reason": "User was unauthorized to access this resource", "info": "Allowed stage mismatch" }`

This typically happens when you switch between the staging and production environments using a sandbox-only token. You must obtain a new token for the production environment, using the PIN authorization workflow. 

- For a Unity game, see the example in the [Unity GameLink Tutorial](../../v1.0/Integrate with Unity/unity-gamelink-tutorial.md#getting-a-gamelink-pin).
- For other development platforms, see one of these recipes:



> Tutorial: [GameLink Authentication](https://docs.muxy.io/v1.0/recipes/gamelink-authentication)






> Tutorial: [Generate a Production JWT](https://docs.muxy.io/v1.0/recipes/generate-a-production-jwt)




To check the target environment of a JWT you are using to authorize calls:

1. Look at the token in the **Authorization** header of any request to an authenticated endpoint (that is, any endpoint other than `auth`).  The header contains your client ID (a number) followed by the JWT:  
   "Authorization: _extension-id_ _jwt_". The JWT is an alphanumeric string that starts with `eyJ`.
2. Copy out the JWT part and enter it into [JWT.IO](https://jwt.io/).
3. Look for the `allowed_stage` field in the payload area. If the value does not match the expected stage, then this is an error. 

- In a sandbox-only JWT, the `allowed_stage` value is "sandbox", which causes the "Allowed stage mismatch" in the production environment.
- In a production-stage JWT, the field does not exist, which causes an error in the sandbox environment.

# Check the channel

If you receive data for a channel other than the one you expect, you can check the channel encoded in the JWT you are using to authorize requests. 

To check whether a JWT is generated for the wrong channel:

1. Look at the token in the **Authorization** header of any request to an authenticated endpoint (that is, any endpoint other than `auth`).  The header looks like this: "Authorization: <extension-id> <jwt>". The JWT value should start with 'eyJ'.
2. Copy out the JWT part and enter it into [JWT.IO](https://jwt.io/).
3. Check the 'channel_id' and 'user_id' fields to make sure they match what is expected. 

The `channel_id` value is the same as the `user_id` of the broadcaster of that channel.

# Troubleshoot data state operations

If you are getting unexpected results when accessing stored data values, check that values are actually getting set in the proper store. The different stores for state and configuration data have specific authorization requirements. 

- The caller must have the `broadcaster` role to successfully write configuration values, or to set values in the `channel_state` store.
- The broadcaster must be the owner of an extension to set values in the `extension_state` store.

If state values are not found or are incorrect, they might have been set without proper authorization, or they might have been written to the wrong data store.  
You can retrieve all state values to make sure that a state value was actually set as expected, and is in the correct state store. 

```text Check all stored data values
js medkit.getAllState().then(state => { console.log(state); });
js medkit.getAllConfig().then(config=> { console.log(state); });
```

> 📘 See the [Data Tracking](../../v1.0/Development Basics/data-tracking.md) guides for complete details of the scope and authorization requirements for the different data stores.

# Troubleshoot user voting

A common mismatch with voting occurs when viewers vote using a stale poll ID.  

Consider a game that intermittently runs a poll with `poll_id="rps"` to play Rock Paper Scissors against the audience.  Every 5 minutes, the game writes to state and then broadcasts a message, which pops up a poll on the extension interface. After one minute, it gets the results. 

This flow will count all of the votes in the `rps` poll, including votes from previous runs, and votes that were cast between runs. Even if you delete the poll after the run, users can still cast votes using that ID, and those votes become "stale" votes in any future run that you create using the same ID. 

The poll manager can send a DELETE request to clear data from the log for a given poll ID. (See [Poll Management](../../v1.0/REST API/aggregation-api/poll-managment.md) for details of the REST API.)  
To ensure that each poll begins with a clean slate, the game should do this immediately BEFORE creating a new poll with the same ID.   (It's ok to delete an ID that does not exist.) 

The correct sequence of operations is: Delete poll ID -> Create new poll with ID -> Wait for votes -> Get results

# Ensure correct time settings

Sometimes users' system clocks can't be trusted to have the correct time. For  
example, users who live near a time-zone border might manually set their time zone  
and adjust the system clock by an hour.

To avoid problems, MEDKit provides the function `getOffsetDate()` to get a more accurate date object.  
The SDK communicates with the server on load to calculate the time offset without reference to the user's system clock. 

The function takes no arguments, and returns a Date object representing the real time.

```javascript
medkit.getOffsetDate();
```

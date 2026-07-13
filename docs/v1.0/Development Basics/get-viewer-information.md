---
title: "Get Viewer Information"
slug: "get-viewer-information"
excerpt: "Access information about the current viewer, or all users who have shared their information."
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Wed Sep 15 2021 16:42:32 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Wed Jan 19 2022 17:28:45 GMT+0000 (Coordinated Universal Time)"
---
You can always access basic identifying information for the current viewer. 

Users of your extension have the option to share their Twitch identity with you.  
MEDKit lets an administrator request a list of all users who are currently sharing this information.

> This list is not exposed to users with `viewer` or `broadcaster` role. It is available only to users with the `admin` role for the extension.

# Get Current Viewer Information

Use the JavaScript `SDK.user`  object to access information on the current viewer.  
The `user` object has these properties:

| Name             | Description                                                                                                                                                    |
| :--------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `channelID`      | String. The numeric ID of the channel the user is currently watching.                                                                                          |
| `twitchJWT`      | Optional. String. The user's JWT as received from the Twitch Extension helper, or "undefined" if the viewer has not shared their Twitch ID with the extension. |
| `twitchID`       | String. The user's Twitch ID if it has been shared with the extension, `null` otherwise.                                                                       |
| `twitchOpaqueID` | String. The user's unique identifier if the Twitch ID has not been shared with the extension, `null` otherwise.                                                |

For example:

```javascript
const medkit = new Muxy.SDK();
await medkit.loaded();

console.log(`Viewer ${  sdk.user.twitchID ? 'has' : 'has not' } shared their Twitch ID with the extension`);
console.log(`They are currently ${sdk.user.buffer}ms behind the stream.`);
```

# Get Twitch IDs of Extension Users

To request the current list of shared Twitch IDs, call `sdk.getExtensionUsers()`. The functionality is only available to broadcasters who have the `admin` role, and (in production) only on Muxy's "admin" pages. You cannot make the call from Twitch's Creator Dashboard.

For example:

```javascript Get users' Twitch IDs
const opts = new Muxy.DebuggingOptions();
opts.role('admin');
Muxy.debug(opts);

const medkit = new Muxy.SDK();
medkit.loaded().then(() => {
  medkit.getExtensionUsers().then((resp) => {
    resp.results.forEach((u) => {
      console.log(u.twitch_id);
    });

    console.log(`There are ${resp.next === '0' ? 'no ' : ''}more results available`);
  });
});
```

The JSON response from this method has the following structure:

```json Print results
{
  next: '0',
  results: [
    { twitch_id: '12345' },
    { twitch_id: '23456' },
    { twitch_id: '34567' }
  ]
}
```

## Iterating for large numbers of users

The `getExtensionUsers()` call returns at most 1,000 objects in its response. If more than 1,000 users have shared their identity with your extension, you have to make more calls to iterate through 1000-user pages. Each page is indexed, and the  `getExtensionUsers()`  method takes an optional page index parameter. 

The following example demonstrates the basic method for iterating through current users.  The `next` field in the response to each call contains the 0-based page index for the next page, or the value `"0"` if all  
results have been returned. Pass the `next` value directly to `getExtensionUsers()` to get the next page of up to 1,000 users. Use a `next` value of 0 to begin the iteration.

```javascript Iterate through users
const opts = new Muxy.DebuggingOptions();
opts.role('admin');
Muxy.debug(opts);

const medkit = new Muxy.SDK();
medkit.loaded().then(() => {
  function getNextUsers(cursor) {
    medkit.getExtensionUsers(cursor).then((resp) => {
      resp.results.forEach((u) => {
        console.log(u.twitch_id);
      });

      if (resp.next !== '0') {
       // this example does not limit the number of responses
        getNextUsers(resp.next);
      }
    });
  }

  getNextUsers('0');
});
```

> 🚧 Be careful!
> 
> For very successful extensions, you can easily overload your connection if you do not further limit the number of calls.  
> If a million users have shared their ID with your extension, this code will very quickly make 1,000 API requests.

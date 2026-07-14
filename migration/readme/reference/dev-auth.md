# Developing in the Sandbox

Muxy provides an off-Twitch environment for development and testing.

During development, you can make use of the testing "sandbox" environment.

* All data stored on sandbox is regularly wiped.
* Authorization tokens distributed by the sandbox token generator work only in the development environment.
* Transactions are always approved.

All endpoints described as part of the MEDKit REST API are available in this environment, as well as the one "sandbox-only" endpoint for obtaining a testing token. Simply switch the URL of the requests from `api.muxy.io` to `sandboxy.muxy.io` to change environments.

# Sandbox-only Endpoint

[block:parameters]
{
  "data": {
    "h-0": "Endpoint",
    "h-1": "Description",
    "0-0": "`authtoken`",
    "0-1": "Use POST to obtain a JWT to authorize calls  in the development environment, for a specific user with a given role.  \n\nYou can provide a single user ID, or a set of user IDs to authorize several users with the same role."
  },
  "cols": 2,
  "rows": 1
}
[/block]

## User IDs

There are two types of user ID:

* A Twitch User ID is a string-encoded number; for example, "27419011".
* A Twitch Opaque ID (for users who have not granted the extension access to their Twitch User ID) is a string starting with `U`, followed by numbers and letters; for example, "U12X345T6J7". If the user is not currently logged into Twitch, this field will have a string starting with `A<random string>`.

By default, extensions are only given a user's Opaque ID which cannot be used to identify the user's Twitch Account. Users are able to "share" their true Twitch identity with an extension, which will then be made available from within the SDK.

MEDKit can use whichever one is available as a unique identifier for the user, however an extension may want to limit features to only users who have shared their User ID with the extension.

The value for the current user is stored in the JavaScript `SDK` instance, in either the `user.twitchID` or `user.twitchOpaqueID` property.

For more information, see the [Twitch documentation](https://dev.twitch.tv/docs/extensions#identity).
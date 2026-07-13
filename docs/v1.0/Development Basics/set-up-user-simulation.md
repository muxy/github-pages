---
title: "Set up User Simulation"
slug: "set-up-user-simulation"
excerpt: "The Muxy debugging system provides user-simulation for testing and debugging in the development environment."
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Wed Sep 15 2021 16:39:00 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Mon Aug 15 2022 22:46:08 GMT+0000 (Coordinated Universal Time)"
---
In production, the Muxy JS SDK automatically detects specific information about the current user and their role, and uses that information to provide a context for API calls.

In your development environment,  you can provide test values to simulate  these environment-specific values that are normally auto-detected. The simulated values are used only in development mode and are ignored once the extension is released on Twitch, so you can include these calls in both development and production code and still have the correct behavior.

## Setting simulated user values

Provide the simulated values as _options_ to the `debug()` function:

```javascript
const opts = new Muxy.DebuggingOptions();
opts
  .channelID('5678')
  .userID('1234')
  .role('viewer');

Muxy.debug(opts);

const medkit = new Muxy.SDK();
medkit.loaded().then(() => {
  console.log('MEDKit is ready to roll!');
});
```

The following debug options are available:

| Option      | Value                                                                                   |
| :---------- | :-------------------------------------------------------------------------------------- |
| `channelID` | String, Sets the current channel (the Twitch channel the viewer is "watching")          |
| `userID`    | String. Sets the current user's Twitch ID                                               |
| `role`      | String, Sets the current user's role. Valid values are `viewer`, `broadcaster`, `admin` |
| `jwt`       | String,  A self-signed JWT to use for all backend request                               |

## Using a self-signed JWT

One of the more powerful debugging options is the `jwt`. Since, as a developer,  
you have access to the Client ID and Secret for your extension, you can sign a  
JWT that will verify your requests. We do this internally for you when your  
extension is running in sandbox or production environments, but you may want to  
do it yourself if you are running parts of your extension on your own site.

The process is the same as the [Signing the JWT](/examples/js_sdk/server_communication.html#signing-the-jwt-with-jsonwebtokencli) section of Server Communication.

Once you have your encoded JWT (in the form `eyJhbGciOiJIUzI1NiIsInR5cCI6I...`),  
you can pass this as a debugging option when initializing the Muxy SDK. 

This token gives you full access to the broadcaster-only functionality, if the JWT payload  
contains those privileges.

```javascript
const opts = new Muxy.DebuggingOptions();
opts.role('broadcaster').jwt('eyJhbGciOiJIUzI1NiIsInR5cCI6I...');

Muxy.debug(opts);
Muxy.setup({
  clientID: '<extension client id>'
});

// instantiate the SDK control class
const medkit = new Muxy.SDK();
medkit.loaded().then(() => {
  medkit.setChannelState({ broadcasters_age: 24 }); // Normally live-dashboard or config only.
});
```

## Using a testing Helix Token

In production, the Muxy SDK obtains a valid API Twitch.tv Helix token to use in various API calls. Testing endpoints that require a Helix Token requires an OAuth flow.

Starting the OAuth flow can be done by following the instructions that are printed to the Javascript Console in testing modes, or by calling `sdk.beginDebugHelixTokenFlow()`. This will open a new window to go through a Twitch.tv OAuth flow. This function can only be called if `Muxy.debug` has been called with a valid debug options object.

After going through the flow, the User object will have a valid `.helixToken` property, ready to be used in API calls. This token is persisted in localStorage, and can be cleared by either using the chrome UI to clear out localStorage, or by calling window.ClearHelixToken() in a Javascript Console.

There is no API to get a callback or other notification when the OAuth flow has been completed. The expected usage of this API is to use it once and then test the application as if the authorization flow grants a valid helix token.

```javascript
const opts = new Muxy.DebuggingOptions();

Muxy.debug(opts);
Muxy.setup({
  clientID: '<extension client id>'
});

// instantiate the SDK control class
const medkit = new Muxy.SDK();
medkit.loaded().then(() => {
	// Will open a new window.
  medkit.beginDebugHelixTokenFlow();
});

// Later on ...
const client = new Muxy.TwitchClient();
client.signedTwitchHelixRequest("GET", "users", medkit.user.helixToken);
```

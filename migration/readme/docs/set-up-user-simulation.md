# Set up User Simulation

The Muxy debugging system provides user-simulation for testing and debugging in the development environment.

In production, the Muxy JS SDK automatically detects specific information about the current user and their role, and uses that information to provide a context for API calls.

In your development environment,  you can provide test values to simulate  these environment-specific values that are normally auto-detected. The simulated values are used only in development mode and are ignored once the extension is released on Twitch, so you can include these calls in both development and production code and still have the correct behavior.

## Setting simulated user values

Provide the simulated values as *options* to the `debug()` function:

[block:code]
{
  "codes": [
    {
      "code": "const opts = new Muxy.DebuggingOptions();\nopts\n  .channelID('5678')\n  .userID('1234')\n  .role('viewer');\n\nMuxy.debug(opts);\n\nconst medkit = new Muxy.SDK();\nmedkit.loaded().then(() => {\n  console.log('MEDKit is ready to roll!');\n});",
      "language": "javascript"
    }
  ]
}
[/block]

The following debug options are available:

[block:parameters]
{
  "data": {
    "h-0": "Option",
    "h-1": "Value",
    "0-0": "`channelID`",
    "1-0": "`userID`",
    "2-0": "`role`",
    "3-0": "`jwt`",
    "0-1": "String, Sets the current channel (the Twitch channel the viewer is \"watching\")",
    "1-1": "String. Sets the current user's Twitch ID",
    "2-1": "String, Sets the current user's role. Valid values are `viewer`, `broadcaster`, `admin`",
    "3-1": "String,  A self-signed JWT to use for all backend request"
  },
  "cols": 2,
  "rows": 4
}
[/block]

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

[block:code]
{
  "codes": [
    {
      "code": "const opts = new Muxy.DebuggingOptions();\nopts.role('broadcaster').jwt('eyJhbGciOiJIUzI1NiIsInR5cCI6I...');\n\nMuxy.debug(opts);\nMuxy.setup({\n  clientID: '<extension client id>'\n});\n\n// instantiate the SDK control class\nconst medkit = new Muxy.SDK();\nmedkit.loaded().then(() => {\n  medkit.setChannelState({ broadcasters_age: 24 }); // Normally live-dashboard or config only.\n});",
      "language": "javascript"
    }
  ]
}
[/block]

## Using a testing Helix Token

In production, the Muxy SDK obtains a valid API Twitch.tv Helix token to use in various API calls. Testing endpoints that require a Helix Token requires an OAuth flow.

Starting the OAuth flow can be done by following the instructions that are printed to the Javascript Console in testing modes, or by calling `sdk.beginDebugHelixTokenFlow()`. This will open a new window to go through a Twitch.tv OAuth flow. This function can only be called if `Muxy.debug` has been called with a valid debug options object.

After going through the flow, the User object will have a valid `.helixToken` property, ready to be used in API calls. This token is persisted in localStorage, and can be cleared by either using the chrome UI to clear out localStorage, or by calling window\.ClearHelixToken() in a Javascript Console.

There is no API to get a callback or other notification when the OAuth flow has been completed. The expected usage of this API is to use it once and then test the application as if the authorization flow grants a valid helix token.

[block:code]
{
  "codes": [
    {
      "code": "const opts = new Muxy.DebuggingOptions();\n\nMuxy.debug(opts);\nMuxy.setup({\n  clientID: '<extension client id>'\n});\n\n// instantiate the SDK control class\nconst medkit = new Muxy.SDK();\nmedkit.loaded().then(() => {\n\t// Will open a new window.\n  medkit.beginDebugHelixTokenFlow();\n});\n\n// Later on ...\nconst client = new Muxy.TwitchClient();\nclient.signedTwitchHelixRequest(\"GET\", \"users\", medkit.user.helixToken);",
      "language": "javascript"
    }
  ]
}
[/block]
# Basic Muxy Login Workflow

To take advantage of the Muxy SDK, a game must obtain a working JavaScript Web Token (JWT) at login.
This login flow does not involve viewers in any way. The JWT serves to pair the game and the [Muxy extension](#creating-the-extension).

* To obtain a JWT, you need an Authorization Code. This page shows how to retrieve the Authorization Code for your extension.

* The next step is to obtain obtain a working JWT using the Authorization Code.  In a game development environment that uses the Unreal Engine, you do this by incorporating a GameLink call into your game's login flow.
  See [Unreal Engine Integration](#unreal_plugin.md).

Once your game has obtained the JWT, you can use it to authorize the extension on startup and to maintain a connection to the GameLink servers.

## Creating an authorized extension

An extension's configuration contains an Authorization Code based on your Twitch client ID.
You use this code to obtain a JWT from the Muxy server.

> If you are not yet familiar with the directory structure and webpack configuration of Muxy Twitch extensions,
> see the [Quick Start Guide](https://docs.muxy.io/docs/quick-start).  This example assumes [manual installation using npm and webpack](https://docs.muxy.io/docs/install-manually),

1. Create a text field to display the token value that you will retrieve.
   Modify the configuration display page (`src/config.html`) as follows :

**config.html**

```diff
  <body>
    <script src="./dist/main.js"></script>
    <h2>Authorization Code: <span id="code"></span></h2>
  </body>
```

2. In the extension's configuration code, use MEDKit calls to get a JWT from the Muxy server. </br>
   Modify the configuration code file (`config.js`) as follows:

**src/config.js**

```js
import Muxy from "@muxy/extensions-js"

// Set debug options to force a specific channel and user
// even when running from localhost.
const opts = new Muxy.DebuggingOptions();
opts.role("broadcaster");
opts.channelID("89319907");
opts.userID("89319907");

Muxy.debug(opts);

// Setup with a clientId
Muxy.setup({
  clientID: "your_client_id"
});

const sdk = new Muxy.SDK();
sdk
  .loaded()
  .then(() => {
    return sdk.signedRequest("POST", "gamelink/token", {});
  })
  .then(tokenEnvelope => {
    document.getElementById("code").innerText = tokenEnvelope.token;
  });
```

3. Run `npx webpack` and navigate to the config page on localhost.
   After a small delay, the page displays the Authorization Code value.

You will pass the authorization code in a call to `Authenticate With Code` in order to obtain a JWT.
You should save that JWT so that you can use it in further calls to `Authenticate With JWT`.

For an example of how to do this using Unreal Engine, see [Integrating Muxy Login into an Unreal Engine Game](#./unreal_plugin.md).
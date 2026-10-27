# Install Manually

Use npm and webpack to install and configure MEDKit

Although the MEDKit starter project comes with MEDKit already installed and configured,
you can also install and configure MEDKit in a command shell, using npm, node.js, and webpack.
This approach gives you the opportunity to create a more customized development environment.

This page introduces basic installation, configuration, and usage principals.

* [Install the MEDKit package](#install-the-medkit-package)
* [Basic configuration](#basic-configuration)
* [Set and get channel state](#set-and-get-channel-state)

Explore the other [Quickstart guides](https://docs.muxy.io/docs) for how to use MEDKit and gamelink together to create interactive games for your users.

## Install the MEDKit package

1. In a command shell, create and go to a working directory. Initialize the directory by runningthe following command:

```bash
$ npm init -y
```

2. The MEDKit JavaScript library is provided in the `extensions-js` package. Install the package using npm:

```bash
$ npm install @muxy/extensions-js
```

After executing an npm install, you can run your extension in a local development server by executing `npm run serve`, or using the Vue UI.

The package is a ES6 module, so you can use a simple webpack configuration to compile it into a basic JavaScript file.

3. Install webpack using npm:

```bash
$ npm install webpack webpack-cli --save-dev
```

## Basic configuration

You must have a valid Extension ClientID to run a Twitch extension. If you don't have one, create one on Twitch’s developer portal: <https://dev.twitch.tv> Choose the Extension type.

### Load and configure the library

Every extension must import the MEDKit library and configure it with you CLientID. A project's configuration is specified in the `src/config.js` file.

1. Edit the extension's configuration file as follows.

**src/config.js**

```javascript
import Muxy from "@muxy/extensions-js"

/*
 * In your development environment, this file is loaded from `localhost`, not in an extension context on Twitch.tv. 
 * We specify debugging options here to mock the login user context.
 */
// Debugging options
const opts = new Muxy.DebuggingOptions();
opts.role("broadcaster");
opts.channelID("89319907");
opts.userID("89319907");

Muxy.debug(opts);

// Set up with your Twitch client ID
Muxy.setup({
    clientID: "myclientid"
});
```

2. To build, invoke webpack with npm.

```sh
$ npm webpack
```

3. To serve the files, either navigate to the `/config.html` file directly, or start a local webserver:

```
python3 -m http.server
```

4. After navigating to `/config.html`, open the console. You should see the MEDKit version and current environment printed to the console.

### Configure page-building scripts

The default installation contains some empty placeholder files for a basic extension.
These include:

* Two HTML files (`config.html` and `viewer.html`) at the top level
* Corresponding JavaScript files in the `src/` directory (`config.js` and `viewer.js`)

You can configure webpack to build pages to be served by editing these files.

1. Create and edit a webpack configuration file, `webpack.config.js`, at the top level.
2. Add the following code to configure entry points for the two pages:

```javascript
module.exports = {
  entry: {
      config: "./src/config.js",
      viewer: "./src/viewer.js"
  },
  mode: "development"
};
```

3. Modify `src/config.html` and `src/viewer.html` to load the built javascript files:

**config.html**

```html
<!doctype html>
<html>
  <head>
    <title>Config Page</title>
  </head>
  <body>
    <script src="./dist/config.js"></script>
  </body>
</html>
```

**viewer.html**

```html
<!doctype html>
<html>
  <head>
    <title>Viewer Page</title>
  </head>
  <body>
    <script src="./dist/viewer.js"></script>
  </body>
</html>
```

## Set and get channel state

The MEDKit REST API provides access to extensive real-time, persistent state information.
The following examples demonstrates how to set a state value, then retrieve the value and display it to a viewer.

### Set channel state

All state related to your extension is stored in a global `SDK` object.
To create an SDK instance, invoke the SDK constructor. The call is asynchronous.
It returns a Promise when it has completed loading  authorization and user information from the network.
Before using any other methods on the SDK object, wait for the `loaded()` Promise to resolve.

1. Edit the extension's configuration file as follows.

**src/config.js**

```javascript
import Muxy from "@muxy/extensions-js"

// Debugging options
const opts = new Muxy.DebuggingOptions();
opts.role("broadcaster");
opts.channelID("89319907");
opts.userID("89319907");

Muxy.debug(opts);

// Setup
Muxy.setup({
    clientID: "myclientid"
});

// Create an SDK instance to hold state
const sdk = new Muxy.SDK();
sdk
  .loaded()
// When the asynchronous call resolves, use the instance to set the channel state.  
  .then(() => {
    sdk.setChannelState({
      message: "Hello, World!"
    });
  });
```

2. Rebuild the configuration page using npm:

```sh
$ npx webpack
```

3. To test, navigate to `/config.html` and check the network request list. There should be a call to `channel_state`.

### Get and show a state value

1. Modify the JavaScript that builds the viewer page to retrieve the state value you have set.

**viewer.js**

```javascript
import Muxy from "@muxy/extensions-js"

/*
 * Notice that we have changed the debug `role` option from "broadcaster" to "viewer", 
 * to mock the new login user context in the development environment.
 */
 // Debugging options
const opts = new Muxy.DebuggingOptions();
opts.role("viewer");
opts.channelID("89319907");
opts.userID("89368629");

Muxy.debug(opts);

// Setup
Muxy.setup({
    clientID: "myclientid"
});

// State information is stored in an SDK object
const sdk = new Muxy.SDK();
sdk
  .loaded()
  .then(() => {
    return sdk.getChannelState()
  })
  .then(state => {
    document.getElementById("message").innerText = state.message;
  });
```

2. To display the channel state in the viewer page, modify the HTML page source.

**viewer.html**

```diff
<!doctype html>
<html>
  <head>
    <title>Viewer Page</title>
  </head>
  <body>
    <script src="./dist/viewer.js"></script>
+   <h2>Message: <span id="message"></span></h2>
  </body>
</html>
```

3. Build the page again with npm and webpack:

```sh
$ npm webpack
```

4. To test, navigate to `viewer.html`.
   * After a short delay, the message "Hello, World!" should be displayed in unstyled text.
   * If 'undefined' is shown instead, ensure that you have loaded `config.html` before `viewer.html`.
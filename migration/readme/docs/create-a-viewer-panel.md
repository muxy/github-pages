# Create a viewer panel

First up let’s build the Panel Extension that will be shown to each viewer on the broadcaster’s channel page (such as [Muxy Channel Page](https://twitch.tv/muxy)).

## Example Viewer Panel Code

This Viewer Panel will display the message to each viewer.

```html
<html>
  <head>
    <style>
      @import url('//fonts.googleapis.com/css?family=Roboto');

      body {
        font-family: 'Roboto', sans-serif;
      }
    </style>

    <!--
      Twitch only allows loading assets from certain white-listed domains. Above we reference a font from Google's font CDN.

      Here we load the latest version of Muxy's JavaScript SDK, however in production you will have to download this file into your extension's folder and reference the local copy.

      You can download specific versions by replacing `latest` with a version number (e.g. `2.0.0`), or keep this as-is to automatically load the most recent version in development.
    -->
    <script src="//ext-cdn.muxy.io/medkit/latest/medkit.umd.js"></script>

    <!--
      Here is the entire code block needed to power the panel. It uses Muxy's state loading to get the last sent message, and easy event binding to get notified when a new message is comes through.
    -->

    <script type="text/javascript">
      /*
       * Muxy has an optional debug system to ease setting common values when developing, and * more powerful features when building advanced systems! Here we set a debug channel to * fake the viewer's location. This would be replaced with the actual channel when
       * running on Twitch. NOTE: The call to `Muxy.debug` must occur before the call to 
       * `Muxy.setup` for the options to be set correctly.
       */
      const opts = new Muxy.default.DebuggingOptions();
      opts.channelID('126955211').role('viewer');
      Muxy.debug(opts);

      /*
       * All Muxy-powered extensions begin by initializing the SDK. This is done by simply
       * calling `setup()` on the global Muxy object with your extension's Client ID, and then * creating an SDK object.
       */
      Muxy.setup({ clientID: 'replaceme' });
      const sdk = new Muxy.SDK();

      /*
       * The new SDK object has a `loaded` function that returns a Promise which will resolve
       * once communication with the backend has been established. It will fail with an error
       * if something goes wrong.
       */
      sdk.loaded().then(() => {
        /*
         * First we will ask the SDK to load all extension state from the backend. This
         * function returns a Promise that will resolve with an object containing several
         * fields representing state for everything from the extension as a whole, to the 
         * broadcaster-set channel state even down to state stored for the specific viewer.
         */
        sdk.getAllState().then(function(state) {
          /*
           * The `channel` field of the `state` object will contain data set by the
           * broadcaster.
           */
          document.querySelector('#motd').innerText = state.channel.motd || 'Enjoy the show!';
        }).catch(function(err) {
          /*
           * If this request fails, the server will respond with a human-readable error
           * message.
           */
          console.error(err);
        });

        /*
         * Next we will set up an event listener on the SDK that will listen for a named event
         * coming to the extension.
         */
        sdk.listen('motd', function(event) {
          document.querySelector('#motd').innerText = event.motd;
        }).catch(function(err) {
          console.error(err);
        });
      });
    </script>
  </head>

  <!--
    Not much markup is needed.
  -->
  <body>
    <h3>Message of the Day</h3>
    <p id="motd"></p>
  </body>
</html>
```
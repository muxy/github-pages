---
title: "Create a broadcaster panel"
slug: "create-a-broadcaster-panel"
excerpt: ""
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Wed Sep 15 2021 16:29:12 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Wed Sep 15 2021 17:42:19 GMT+0000 (Coordinated Universal Time)"
---
Next let’s put together the Live Dashboard Extension that will only appear on the broadcaster’s live dashboard after they have activated the extension (for example, [Muxy Live Dashboard](https://www.twitch.tv/muxy/dashboard/live)). 

This page displays a text box and button that allows the broadcaster to enter message text and broadcast it to viewers who are running the Viewer Extension.

## Broadcaster Live Dashboard Code

The source code for this extension is in the HelloWorld example, in the file [live.html](https://github.com/muxy/medkit-examples/blob/master/hello_world/live.html).

We'll go through it step by step.

```html
<html>
  <head>
    <!-- This predefined script loads and initializes the Muxy SDK. -->
    <script src="//ext-cdn.muxy.io/medkit/latest/medkit.umd.js"></script>

    <!-- This script defines the functionality. -->
    <script type="text/javascript">
      /*
       * Here we are using the debug system to give the SDK a hint that this will run on the
       * broadcaster's dashboard and have the same rights a broadcaster does. This is only
       * needed and used when developing an extension. Once it is deployed to production, the
       * backend uses the correct rights from the extension system. You can leave these
       * lines in - they are ignored when running in production.
       */
      const opts = new Muxy.default.DebuggingOptions();
      opts.channelID('126955211').role('broadcaster');
      Muxy.debug(opts);

      Muxy.setup({ clientID: 'replaceme' });
      const sdk = new Muxy.SDK();

      /*
       * This function provides the button behavior. It sets the message ID, updates the message text, 
       * and publishes the message to subscribers (viewers).
       */
      function changeMotd() {
        const motd = document.querySelector('#motd').value;

        /*
         * We wait for the SDK to confirm it is loaded each time the button is clicked. In a
         * real extension you may want a more robust solution, although there is no harm in
         * calling this function multiple times.
         */
        sdk.loaded().then(() => {
          /*
           * First we send the updated message state to the backend. This ensures that future
           * requests to get the extension state will have the most recent message.
           */
          sdk.setChannelState({
            motd: motd
          });

          /*
           * Then we broadcast an event to all current viewers with the new message. This
           * allows the panel extension to update its message without continuously polling
           * the backend.
           */
          sdk.send('motd', { motd: motd });
        });
      }
    </script>
  </head>

  <!--
    Not much markup is needed. 
    The component displays a text input box and the button that sends the message.
  -->
  <body>
    <textarea id="motd">Hello, world!</textarea>
    <p>
      <button onclick="changeMotd()">Set MOTD</button>
    </p>
  </body>
</html>
```

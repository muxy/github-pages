# Build a Simple Extension

Add source for a Hello World extension to your basic installation

To get started building simple extensions, we will modify the starter project to create a basic Panel Extension that lets a broadcaster set a “Message of the Day” for their viewers, and another extension for viewers that shows them the message.

This exercise uses two extensions that are part of the [MEDKit Hello World Example](https://github.com/muxy/medkit-examples). The [Broadcast Live Dashboard](https://www.twitch.tv/muxy/dashboard/live) extension is defined by 'src/live.htm', and the extension for viewers is defined by 'src/viewer.htm'.

1. Open the source file for the Broadcast Live Dashboard extension (or create a new Panel Extension).
2. Add a text input box and button to this extension so that a broadcaster will be able to enter some message text, and press the button to publish the message to all current viewers.

**[See the commented Broadcaster Live Dashboard code here](https://docs.muxy.io/docs/create-a-broadcaster-panel)**

3. Open the source file for the Viewer extension (or create a new Panel Extension).
4. Use the example code to modify another extension that viewers will see. This code subscribes to the broadcast stream and displays messages when they arrive. New viewers who visit the channel will see the most recent message the broadcaster sent.

**[See the commented code for the Viewer Panel Extension here](https://docs.muxy.io/docs/create-a-viewer-panel)**
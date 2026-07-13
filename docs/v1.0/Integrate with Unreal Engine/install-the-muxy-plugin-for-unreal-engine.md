---
title: "Install the Muxy Plugin for Unreal Engine"
slug: "install-the-muxy-plugin-for-unreal-engine"
excerpt: ""
hidden: true
metadata: 
  image: []
  robots: "index"
createdAt: "Wed Sep 15 2021 16:30:46 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Mon Jun 12 2023 20:53:56 GMT+0000 (Coordinated Universal Time)"
---
If you have an existing game that you have developed using Unreal Engine, you can add a Muxy-powered experience using the [GameLink Unreal Plugin](https://dl.muxy.io/MuxyUnrealPlugin.zip) for Unreal Engine 4.25.  

## Install the Plugin

1. Download the Muxy plugin from <https://dl.muxy.io/MuxyUnrealPlugin.zip> 
2. Copy the parent directory, `MuxyUnrealPlugin`, into a `Plugins` folder at the root of your Unreal Engine 4.25 project.  
   (Create the folder if necessary.)



![430](https://files.readme.io/f3439f7-layout.png)




3. If the editor is running, restart it to update the contents fo the `Plugins` directory.

4. Scroll to the bottom of the **Edit > Plugins** menu to see **MuxyUnrealPlugin** in the  
   **Other** category. 

5. Check **Enable**.



![1659](https://files.readme.io/a09f782-plugin.png)




## Next Steps

The Muxy UnReal Plugin exposes a set of static blueprint functions and a singleton object, `MuxyEventSource`, with methods for reacting to _authorization_, _polling_, and _transaction_ events.

Before your game can use Muxy functionality, you must allow the broadcaster to log in to the Muxy server, so that you can initialize the plugin by authenticating the user for each login session.

- [Initializing the Muxy Plugin](create-a-muxy-login-flow/initialize-the-extension.md)
- [Integrate the Muxy Login Flow](create-a-muxy-login-flow.md) into your game.

Use the provided blueprints and methods to integrate Muxy functionality into your Unreal Engine game:

- [Retrieve and Use State Information](workflow-examples/basic-usage-examples.md)
- [Broadcast Messages](workflow-examples/basic-usage-examples.md)
- [Accept Bit Transactions](workflow-examples/basic-usage-examples.md)

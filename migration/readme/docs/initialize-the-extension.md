---
title: Initialize the Muxy Plugin
slug: initialize-the-extension
excerpt: Authenticate the user to authorize MEDKit API usage in each session
hidden: true
metadata:
  image: []
  robots: index
createdAt: Wed Sep 15 2021 16:33:44 GMT+0000 (Coordinated Universal Time)
updatedAt: Mon Jun 12 2023 20:53:50 GMT+0000 (Coordinated Universal Time)
---

The Muxy Plugin exposes a set of static blueprint functions and a singleton global source object, `MuxyEventSource`.  
To initialize the plugin, you use a blueprint to authenticate the user, then provide a callback that reacts to an `authorization` event.

## Authenticate the User

Before calling any functions, the game must authenticate the user by calling one of the Authorization blueprints:  `Authenticate with JWT` or `Authenticate with Code`.



![259](https://files.readme.io/cc6f2cf-authblueprints.png)




These blueprints accept two inputs:

- A _Twitch Extension Client ID_, which is obtained from the Twitch Developer Portal.
- Either a JavaScript web token (JWT) or Login Code from the Muxy API. (See the [Login Flow guide] for how to get a Login Code.)

On first use, you will use `Authenticate with Code`. When you make this call, it returns a JWT that you can then use for subsequent calls to `Authenticate with JWT`. The JWT returned from any authorization is valid for 30 days. Using Authenticate with JWT will grant a new JWT that is valid for 30 days.

## Receive Authentication Response

To receive the authorization event use the `Get Event Source` node to get the event source, and assign onto the `MuxyAuth` event.



![542](https://files.readme.io/c93ce04-authevent.png)




When this event fires, the event source will have the updated JWT that should be persisted for logins in the future. This event will fire for both login styles.



![668](https://files.readme.io/7afe9f0-authjwt.png)

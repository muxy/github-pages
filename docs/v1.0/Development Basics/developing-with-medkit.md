---
title: "Developing with MEDKit"
slug: "developing-with-medkit"
excerpt: "Set up your development environment and learn the basics"
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Wed Sep 15 2021 16:38:07 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Wed Sep 29 2021 23:17:39 GMT+0000 (Coordinated Universal Time)"
---
In this section, learn the basics of developing extensions that take full advantage of Muxy functionality through MEDKit, the Muxy JavaScript SDK.

- MEDKit provides the ability to simulate users for testing in the development environment. Learn how to [Set up user simulation](../../v1.0/Development Basics/set-up-user-simulation.md).
- Here are some [troubleshooting tips](troubleshooting-tips.md) for avoiding common mistakes.

Muxy provides _state stores_ with varying scopes, where you can collect data about your extensions and viewers and access it in real time.

- Learn how to access [stored extension and viewer state](../../v1.0/Development Basics/data-tracking/state-information.md) values.
- Learn how take advantage of the Muxy server to store and retrieve your own [developer-defined state information](../../v1.0/Development Basics/data-tracking/state-information.md).
- Learn how to [get viewer information](../../v1.0/Development Basics/get-viewer-information.md).

You can also [call directly into the Twitch API](../../v1.0/Development Basics/call-into-the-twitch-api.md). MEDKit even provides a convenience wrapper for some of the more common use cases.

# Access Muxy Functionality in JavaScript

The `Muxy.SDK` class provides the JavaScript methods you use to access all functionality and services.  Instantiate this class as part of your initialization code for any page script.

```javascript
// create an SDK instance named "medkit"
const medkit = new Muxy.SDK();
// call a method to retrieve data
medkit.getAllState();
```

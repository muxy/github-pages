---
title: "Quick Start for Developers"
slug: "quick-start"
excerpt: "These guides will help you get started with Muxy. You'll be up and running in a jiffy!"
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Mon Sep 13 2021 21:51:49 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Mon Jun 12 2023 20:57:31 GMT+0000 (Coordinated Universal Time)"
---
Here in our Quick Start guides you'll find examples to help you understand the basics of working with our tools to create fully interactive, engaging Twitch Extensions.

# Add Muxy functionality to your Twitch Extension

Whether you are a _game developer_, an _extension writer_, or a _streamer_, you can use Muxy-enabled extensions to improve the gaming and viewing experience, promote viewer engagement with interaction and rewards, and monetize your audience. 

- If you have an existing Twitch Extension, you can use these steps to register it with Muxy to add functionality and use Muxy services. 

- If you don't already have one, **create a new Twitch Extension** in the [Twitch Developer Console](https://dev.twitch.tv).

## Register your extension with Muxy

1. In the [Twitch Developer Console](https://dev.twitch.tv), look at the **Extension Settings** and copy the **Extension Client ID** and **Extension Secret**.  You will use these to register the extension with Muxy.

2. Go to the [Muxy Developer Portal](https://dev.muxy.io) and click **Register New Extension**.

3. Fill in the **Extension Name**, **Client ID**, and **Secret**.

> 🚧 Keep the Client ID
> 
> Store your Client ID where you can find it again-- you will also use it to initialize the MEDKit SDK each time the extension starts up.
> 
> Once you have registered your extension, your _Twitch Extension Client ID_ also serves as your _Muxy Client ID_. Every call into the Muxy SDK is authorized by this `clientId` value

# First Steps

> 👍 Game Developers
> 
> If you use the Unreal Engine or Unity game-development environment, add a Muxy-powered experience using integrated Muxy functionality.   
> 
> - [Integrate with Game-development Environments](#integrate-with-game-development-environments)

> 📘 Muxy Architecture for Extension Writers and Streamers
> 
> If you are creating extensions from the ground up, the following guides will help you to get familiar with the form and structure of a Muxy-powered extension.

| Topic                                                      | Description                                                                         |
| :--------------------------------------------------------- | :---------------------------------------------------------------------------------- |
| [Get Started with MEDKit](../../v1.0/Getting Started with MEDKit/getting-started-with-medkit.md) | Introduction to MEDKit and the Muxy SDK.                                            |
| [Build a Simple Extension](../../v1.0/Getting Started with MEDKit/build-a-simple-extension.md)   | Build a "HelloWorld" Muxy extension with JavaScript                                 |
| [Basic Muxy Login Workflow](../../v1.0/Getting Started with MEDKit/basic-muxy-login-workflow.md) | How your broadcaster logs in to connect to the Muxy server.                         |
| [Install SDK Manually](../../v1.0/Getting Started with MEDKit/install-manually.md)               | Install and configure MEDKit from a command shell, using npm, node.js, and webpack. |

# MEDKit Code Examples

These fully-commented, easy-to-understand code samples showcase how to use the Muxy MEDKit JavaScript SDK for common tasks.

## Development Basics

Learn the basics of developing extensions that take full advantage of Muxy functionality.

| Topic                                                    | Description                                                                                         |
| :------------------------------------------------------- | :-------------------------------------------------------------------------------------------------- |
| [Set up User Simulation](../../v1.0/Development Basics/set-up-user-simulation.md)     | Simulate users with different <<glossary:user roles>> for debugging in the development environment. |
| [Store State Values](../../v1.0/Development Basics/data-tracking/state-information.md)              | How to define, store, and retrieve real-time extension and viewer <<glossary:state>> values.        |
| [Store Configuration Data](../../v1.0/Development Basics/data-tracking/store-configuration-data.md) | How to define, store, and retrieve extension-configuration values.                                  |
| [Store Arbitrary State](sarbitrary-state)            | How to define, store, and retrieve any kind of state data.                                          |
| [Get Viewer Information](../../v1.0/Development Basics/get-viewer-information.md)     | How to retrieve information about your extension viewers.                                           |
| [Call into the Twitch API](../../v1.0/Development Basics/call-into-the-twitch-api.md) | How to make use of Twitch features in an extension.                                                 |
| [Troubleshooting Tips](troubleshooting)              | Some hints and tips for avoiding common problems.                                                   |

## Viewer Engagement Techniques

These guides provide example code and advice for taking advantage of Muxy functionality in your extensions.



| Topic | Description |
| --- | --- |
| [Viewer Data Aggregation](../../v1.0/Viewer Engagement Techniques/data-aggregation-techniques.md) | Introduces techniques and tools for scaling up by aggregating data from many viewers.  <br>  <br>Code examples demonstrate [Accumulating User Data](../../v1.0/Viewer Engagement Techniques/data-aggregation-techniques/accumulation.md) and [Ranking User Data](../../v1.0/Viewer Engagement Techniques/data-aggregation-techniques/ranking.md). |
| [Viewer Engagement Tools](../../v1.0/Viewer Engagement Techniques/viewer-engagement-tools.md) | Tools for creating activities and events that encourage viewer interaction.  <br>  <br>Code examples demonstrate how to set up and manage  [Polls and User Voting](../../v1.0/Viewer Engagement Techniques/viewer-engagement-tools/voting.md). |




# Integrate with Game Development Environments

Muxy functionality is integrated into Unreal Engine through a **Muxy Plugin**, and with Unity through a **C# MEDKit SDK**.  
These guides help you install the integration tools, and get you started with initialization and implementing functionality.

## Integrate Muxy with an Unreal Engine Game

Muxy's GameLink SDK is written in C++ and can be integrated into Unreal. See the [Github repo](https://github.com/muxy/gamelink-cpp) for more information.

## Integrate the C# MEDKit SDK with a Unity Game

For an existing game that uses the Unity engine, add a Muxy-powered experience by installing the [C# MEDKit SDK](docs:integrate-with-unity).

| Topic                                                  | Description                                                                                                             |
| :----------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------- |
| [Unity GameLink Tutorial](../../v1.0/Integrate with Unity/unity-gamelink-tutorial.md) | This tutorial walks through building a small Unity scene that does GameLink authentication and reacts to a viewer poll. |

# Learn more...

- Download a complete MEDKit extension starter project for Vue.js: [MEDKit Starter Vue](https://github.com/muxy/medkit-starter-vue)
- Read up on the Muxy Extension SDK: [Using the MEDKit REST API](../../v1.0/REST API/medkit-rest-api.md) 
- Hit us up with any issues at [support@muxy.io](mailto:support@muxy.io)

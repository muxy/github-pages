# Quick Start for Developers

These guides will help you get started with Muxy. You'll be up and running in a jiffy!

Here in our Quick Start guides you'll find examples to help you understand the basics of working with our tools to create fully interactive, engaging Twitch Extensions.

# Add Muxy functionality to your Twitch Extension

Whether you are a *game developer*, an *extension writer*, or a *streamer*, you can use Muxy-enabled extensions to improve the gaming and viewing experience, promote viewer engagement with interaction and rewards, and monetize your audience.

* If you have an existing Twitch Extension, you can use these steps to register it with Muxy to add functionality and use Muxy services.

* If you don't already have one, **create a new Twitch Extension** in the [Twitch Developer Console](https://dev.twitch.tv).

## Register your extension with Muxy

1. In the [Twitch Developer Console](https://dev.twitch.tv), look at the **Extension Settings** and copy the **Extension Client ID** and **Extension Secret**.  You will use these to register the extension with Muxy.

2. Go to the [Muxy Developer Portal](https://dev.muxy.io) and click **Register New Extension**.

3. Fill in the **Extension Name**, **Client ID**, and **Secret**.

> 🚧 Keep the Client ID
>
> Store your Client ID where you can find it again-- you will also use it to initialize the MEDKit SDK each time the extension starts up.
>
> Once you have registered your extension, your *Twitch Extension Client ID* also serves as your *Muxy Client ID*. Every call into the Muxy SDK is authorized by this `clientId` value

# First Steps

> 👍 Game Developers
>
> If you use the Unreal Engine or Unity game-development environment, add a Muxy-powered experience using integrated Muxy functionality.
>
> * [Integrate with Game-development Environments](#integrate-with-game-development-environments)

> 📘 Muxy Architecture for Extension Writers and Streamers
>
> If you are creating extensions from the ground up, the following guides will help you to get familiar with the form and structure of a Muxy-powered extension.

| Topic                                                      | Description                                                                         |
| :--------------------------------------------------------- | :---------------------------------------------------------------------------------- |
| [Get Started with MEDKit](https://docs.muxy.io/docs/getting-started-with-medkit) | Introduction to MEDKit and the Muxy SDK.                                            |
| [Build a Simple Extension](https://docs.muxy.io/docs/build-a-simple-extension)   | Build a "HelloWorld" Muxy extension with JavaScript                                 |
| [Basic Muxy Login Workflow](https://docs.muxy.io/docs/basic-muxy-login-workflow) | How your broadcaster logs in to connect to the Muxy server.                         |
| [Install SDK Manually](https://docs.muxy.io/docs/install-manually)               | Install and configure MEDKit from a command shell, using npm, node.js, and webpack. |

# MEDKit Code Examples

These fully-commented, easy-to-understand code samples showcase how to use the Muxy MEDKit JavaScript SDK for common tasks.

## Development Basics

Learn the basics of developing extensions that take full advantage of Muxy functionality.

| Topic                                                    | Description                                                                                         |
| :------------------------------------------------------- | :-------------------------------------------------------------------------------------------------- |
| [Set up User Simulation](https://docs.muxy.io/docs/set-up-user-simulation)     | Simulate users with different <<glossary:user roles>> for debugging in the development environment. |
| [Store State Values](https://docs.muxy.io/docs/state-information)              | How to define, store, and retrieve real-time extension and viewer <<glossary:state>> values.        |
| [Store Configuration Data](https://docs.muxy.io/docs/store-configuration-data) | How to define, store, and retrieve extension-configuration values.                                  |
| [Store Arbitrary State](https://docs.muxy.io/docs/sarbitrary-state)            | How to define, store, and retrieve any kind of state data.                                          |
| [Get Viewer Information](https://docs.muxy.io/docs/get-viewer-information)     | How to retrieve information about your extension viewers.                                           |
| [Call into the Twitch API](https://docs.muxy.io/docs/call-into-the-twitch-api) | How to make use of Twitch features in an extension.                                                 |
| [Troubleshooting Tips](https://docs.muxy.io/docs/troubleshooting)              | Some hints and tips for avoiding common problems.                                                   |

## Viewer Engagement Techniques

These guides provide example code and advice for taking advantage of Muxy functionality in your extensions.

[block:parameters]
{
  "data": {
    "h-0": "Topic",
    "h-1": "Description",
    "0-0": "[Viewer Data Aggregation](https://docs.muxy.io/docs/data-aggregation-techniques)",
    "0-1": "Introduces techniques and tools for scaling up by aggregating data from many viewers.  \n  \nCode examples demonstrate [Accumulating User Data](https://docs.muxy.io/docs/accumulation) and [Ranking User Data](https://docs.muxy.io/docs/ranking).",
    "1-0": "[Viewer Engagement Tools](https://docs.muxy.io/docs/viewer-engagement-tools)",
    "1-1": "Tools for creating activities and events that encourage viewer interaction.  \n  \nCode examples demonstrate how to set up and manage  [Polls and User Voting](https://docs.muxy.io/docs/voting)."
  },
  "cols": 2,
  "rows": 2,
  "align": [
    "left",
    "left"
  ]
}
[/block]

# Integrate with Game Development Environments

Muxy functionality is integrated into Unreal Engine through a **Muxy Plugin**, and with Unity through a **C# MEDKit SDK**.\
These guides help you install the integration tools, and get you started with initialization and implementing functionality.

## Integrate Muxy with an Unreal Engine Game

Muxy's GameLink SDK is written in C++ and can be integrated into Unreal. See the [Github repo](https://github.com/muxy/gamelink-cpp) for more information.

## Integrate the C# MEDKit SDK with a Unity Game

For an existing game that uses the Unity engine, add a Muxy-powered experience by installing the [C# MEDKit SDK](docs:integrate-with-unity).

| Topic                                                  | Description                                                                                                             |
| :----------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------- |
| [Unity GameLink Tutorial](https://docs.muxy.io/docs/unity-gamelink-tutorial) | This tutorial walks through building a small Unity scene that does GameLink authentication and reacts to a viewer poll. |

# Learn more...

* Download a complete MEDKit extension starter project for Vue.js: [MEDKit Starter Vue](https://github.com/muxy/medkit-starter-vue)
* Read up on the Muxy Extension SDK: [Using the MEDKit REST API](https://docs.muxy.io/reference/medkit-rest-api)
* Hit us up with any issues at [support@muxy.io](support@muxy.io)
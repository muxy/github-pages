# Developing with MEDKit

Set up your development environment and learn the basics

In this section, learn the basics of developing extensions that take full advantage of Muxy functionality through MEDKit, the Muxy JavaScript SDK.

* MEDKit provides the ability to simulate users for testing in the development environment. Learn how to [Set up user simulation](https://docs.muxy.io/docs/set-up-user-simulation).
* Here are some [troubleshooting tips](troubleshooting-tips.md) for avoiding common mistakes.

Muxy provides *state stores* with varying scopes, where you can collect data about your extensions and viewers and access it in real time.

* Learn how to access [stored extension and viewer state](https://docs.muxy.io/docs/state-information) values.
* Learn how take advantage of the Muxy server to store and retrieve your own [developer-defined state information](https://docs.muxy.io/docs/state-information).
* Learn how to [get viewer information](https://docs.muxy.io/docs/get-viewer-information).

You can also [call directly into the Twitch API](https://docs.muxy.io/docs/call-into-the-twitch-api). MEDKit even provides a convenience wrapper for some of the more common use cases.

# Access Muxy Functionality in JavaScript

The `Muxy.SDK` class provides the JavaScript methods you use to access all functionality and services.  Instantiate this class as part of your initialization code for any page script.

[block:code]
{
  "codes": [
    {
      "code": "// create an SDK instance named \"medkit\"\nconst medkit = new Muxy.SDK();\n// call a method to retrieve data\nmedkit.getAllState();",
      "language": "javascript"
    }
  ]
}
[/block]
---
title: Integrate a Muxy Login Flow
description: Archived Muxy documentation for Integrate a Muxy Login Flow.
slug: create-a-muxy-login-flow
product: Unreal
audience: developers
status: archived
owner: Unreal SDK owner
source_of_truth: muxy/github-pages:migration/readme
version: unverified
last_verified: '2026-07-14'
review_state: needs-sme-review
robots: noindex, nofollow
search:
  exclude: true
page_type: task-guide
---

# Integrate a Muxy Login Flow

!!! warning "Archived documentation"
    This page is retained for URL compatibility. It is not maintained, indexed, or included in agent exports.


> This procedure assumes that you have first followed the installation procedure documented
> at [GameLink Unreal Plugin Install](install-the-muxy-plugin-for-unreal-engine.md).

To integrate your Unreal Engine game with the Muxy server, the game must include
a login flow in which the broadcaster can navigate to the extension's configuration page to
obtain a short Authorization Code, and can then enter this code into a UI element in the game.
The game can then pass the code in a call to `Authenticate With Code` in order to obtain a JWT.

The process has these steps:

1. [Create a Code Field UI Element](#create-a-code-field-ui-element)
2. [Save the Returned JWT](#save-the-returned-jwt)
3. [Use a Saved JWT](#use-a-saved-jwt)

## Create a Code Field UI Element

First, create a simple slate widget blueprint to allow a user to enter a Muxy authorization code.
Right click in the content manager, and select `User Interface > Widget Blueprint`. Call this blueprint
`MuxyUI`.



![463](../assets/readme/9edb3d3-create_widget.png){ width="463" height="187" loading="lazy" }




This widget should have an editable textbox, and a button. An example layout is shown below. Note that
the editable textbox to the left of the Submit button is named `AuthCodeTextBox`.



![842](../assets/readme/6bd6f8d-layout_ui.png){ width="842" height="139" loading="lazy" }




Select the submit button, and scroll the right sidebar to the bottom, and create an event node
on "OnClicked". From this node, drag out the execution pin and add in the Gamelink Node, `Authenticate with Code`.

This node takes in a `Client ID`, which is obtained from the Muxy Dev Portal or Twitch Dev Portal, and an authorization
code. To get this authorization code, drag in the `AuthCodeTextBox`, and use the `Get Text` node to get contents of
the editable textbox. Attach this text to the `Code` input pin of `Authenticate with Code`:



![941](../assets/readme/66268f9-on_clicked.png){ width="941" height="259" loading="lazy" }




To add this widget to the user interface, exit the blueprint editor and open the default level blueprint. There,
find the `BeginPlay` event. From the `BeginPlay` event, create the MuxyUI Widget and add it to the viewport:



![843](../assets/readme/e9df84d-add_to_viewport.png){ width="843" height="309" loading="lazy" }




Now, the user can play the game and see the interface to authorize with Gamelink:



![1567](../assets/readme/26086e3-sample.png){ width="1567" height="783" loading="lazy" }




When a valid authorization code is input to the editable textbox and the Submit button has been
clicked, the console should output something similar to the following:

```
LogTemp: Warning: Attempting to connect: my_client_id:mYcOdE
LogTemp: Warning: Send message: {"action":"authenticate","data":{"client_id":"my_client_id","pin":"mYcOdE"}}
LogTemp: Warning: Got message: {"data":{"jwt":"not.a.jwt"},"meta":{"action":"authenticate","request_id":65535,"target":"","timestamp":1600972000000000}}
```

At this point, the game has authorized and successfully connected to the Muxy Gamelink servers.

## Save the Returned JWT

Requiring the user to enter a code every time they start the game is annoying. For this reason, it is good practice
to save the JWT obtained from authorizing with a code and use that saved JWT to authorize automatically
when the game starts up again.

A easy way to save game configuration like this is to create a new `SaveGame` subclass and place the relevant data in there.
In this sample, right click in the content browser and create a new Blueprint Class, for which the parent class should be
`SaveGame`. Name this class `JWTSave`

Modify this new blueprint class and add in a JWT string variable:

![savegame_variable.png](../assets/readme/ede7ce9-savegame_variable.png){ width="550" height="303" loading="lazy" }

Authorization is done asynchronously, so the UI blueprint cannot directly get the JWT after calling `Authenticate With Code`.
Instead, the UI blueprint must assign to the EventSource's delegate `On Muxy Auth`:



![738](../assets/readme/87783f7-assign_event.png){ width="738" height="304" loading="lazy" }




Link up the exec nodes, and the resulting blueprint should look like this:



![723](../assets/readme/c98fe32-assign_event_result.png){ width="723" height="318" loading="lazy" }




To save data, the blueprint must create an instance of `JWTSave`, set the JWT property as the JWT from
the event source, and then save it to a named save slot. A simple blueprint version of this flow is shown below:



![1081](../assets/readme/70289c7-save_jwt.png){ width="1081" height="212" loading="lazy" }




## Use a Saved JWT

Using a saved JWT to authenticate automatically is the inverse of saving a JWT. Instead of saving a
`SaveGame` instance, you load it and use the saved JWT in a call to `Authenticate With JWT`. This can be done as soon
as OnBeginPlay:



![1709](../assets/readme/5d70d90-load_jwt.png){ width="1709" height="274" loading="lazy" }




This will also invoke the `On Muxy Auth` delegate, with a refreshed JWT, so this Authorization path should update the saved JWT:



![1531](../assets/readme/542578a-refresh_save.png){ width="1531" height="421" loading="lazy" }

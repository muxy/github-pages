---
title: "Unity FPS Demo Code Walkthrough"
slug: "unity-fps-demo-code-walkthrough"
excerpt: "Download and walk through an example project that demonstrates important functionality."
hidden: false
metadata: 
  title: "Unity FPS Demo Code Walkthrough"
  image: []
  robots: "index"
createdAt: "Thu Feb 17 2022 16:32:38 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Mar 12 2024 19:45:58 GMT+0000 (Coordinated Universal Time)"
---
# Get Started

This tutorial walks through a demo based on the Unity FPS Microgame template. The demo integrates  a Muxy extension into the basic first-person-shooter game. You can download the demo from GitHub, and examine and manipulate the code in Unity. 

The demo project, Unity FPS Demo, demonstrates the basic integration of a game with a Muxy extension, and also shows how to take advantage of essential features of **GameLink ** (C#/C++ game-side libraries) and **MEDKit** (JavaScript/TypeScript front-end libraries). We will go over code from both the Unity Game and the Extension.

## Prerequisites

We assume that you have some familiarity with the following concepts and technologies:

- The **Unity game-development platform and ecosystem**.  
   You should have Unity Hub installed, with Unity Editor version 2020.3.12f1 LTS (or any editor version that includes the FPS Microgame template).
- Basic **HTML/CSS**  
   For example, you should understand that HTML statement `<div class="config">` creates a `div` element with the style of "config" specified in the CSS.
- Basic **JavaScript**  
   The demo uses JavaScript. MEDKit also supports TypeScript.
- Basic **Vue.js**  
   You don't have to be a Vue.js expert, but you should understand how an HTML template that presents the user experience is controlled by JS/TS code that provides the game logic and data. For more information, see the [Vue.js guide](https://vuejs.org/guide/introduction.html).

## Get your own Extension ID

You need to have a registered Extension ID to integrate into the demo project.

1. If you don't already have one, **create a new Twitch Extension** in the [Twitch Developer Console](https://dev.twitch.tv). 
2. In the [Twitch Developer Console](https://dev.twitch.tv), look at the **Extension Settings** and copy the **Extension Client ID** and **Extension Secret**.  You will use these to register the extension with Muxy.
3. Go to the [Muxy Developer Portal](https://dev.muxy.io) and click **Register New Extension**.
4. Fill in the **Extension Name**, **Client ID**, and **Secret**. 

For more information, see [Quick Start for Developers](../../v1.0/Documentation/quick-start.md) .

## Download and set up the example Unity project

To get started, [download the Unity FPS Demo from GitHub](https://github.com/muxy/gamelink-unity-fps-demo). The demo includes two Unity files (a script and prefab), that you can drag and drop into a project based on the Unity FPS Microgame template.  
Use the following steps to get the example project running in Unity:

1. In the Unity Hub, start a new project using the **FPS Microgame** template.
2. Install the [GameLink Library](https://github.com/muxy/gamelink-unity) into the packages folder.
3. Drag and drop `GameLink.prefab` into `Assets\FPS\Prefabs`.
4. Drag and drop `GameLinkFPSBehaviour.cs` into `Assets\FPS\Scripts`.
5. Open `Assets\FPS\Scenes\IntroMenu.unity` and drag `GameLink.prefab` into the hierarchy scene root.
6. Enter your extension ID into the component field `GAMELINK_EXTENSION_ID` on the GameLink prefab.

## Set up the example extension

The download also includes a folder containing a complete Muxy extension. The sample extension code includes source files for two pages, a configuration page for the broadcaster and an overlay for the viewer. Each page has a Vue.js HTML template that defines the UI, and a JavaScript file that defines the logic and data. 

> 📘 For more information about the different types of extensions and broadcaster pages, see [Get Started with MEDKit](../../v1.0/Getting Started with MEDKit/getting-started-with-medkit.md).

To set up  and run the sample extension: 

1. Copy `.env.sample` to `.env`. This file could contain secrets, so `.env` is in our `.gitignore` file.
2. Edit the variable `VUE_APP_CLIENT_ID` to match the Twitch Extension Client ID you created on the [Twitch Dev Console](https://dev.twitch.tv).
3. To install dependencies, run the following command in a command shell: 

```shell Install dependencies
npm install
```

4. To run the extension locally during development, enter the following command:

```shell Start hot-reloading
npm run dev
```

5. Access the two extension pages on your localhost port (we use port 4000 as a typical example): 

| Page                           | Access on localhost                  |
| :----------------------------- | :----------------------------------- |
| Broadcaster configuration page | `http://localhost:4000/config.html`  |
| Viewer overlay extension       | `http://localhost:4000/overlay.html` |

The rest of this tutorial walks through the extension code, so that you can see how it works.

> 📘 Developing your own extension
> 
> You can copy, customize, and extend any of this code, to learn more and to suit your needs.
> 
>  When you are ready to release your extension, run `npm run build`. This creates a `dist/` folder with compiled versions of the pages, as well as a ZIP file containing all HTML, JS and other assets bundled together. You can upload this ZIP directly to Twitch's upload page.

# Authentication

Each broadcaster who uses the extension will need to authenticate with a PIN, which they must acquire and enter inside the game. They will get this PIN from the extension's configuration page when they install it to their channel. That page is defined by the Vue.js component file `Extension/src/config/App.vue`.  

You can give the broadcaster all sorts of customization options in the configuration page, but for now what we care about is displaying a PIN to use. The sample code just provides a  basic way to obtain and display a PIN for your broadcaster to enter. To see how the PIN is displayed, open the sample configuration page at \<localhost:4000/config.html> (or whatever port you are serving it from). 

## Initialization

The `App.vue` component file, like all Vue component files, has two parts; the top part is the HTML template, and the rest is the JS script that controls the behavior.

> 📘 [Learn more about Vue component basics](https://vuejs.org/guide/essentials/component-basics.html)

 Vue components allow you to separate out blocks of functionality into reusable pieces.  `App.vue` is a controller component that performs initialization and defines the basic framework of the page UI. The HTML code for the config page template displays another component called `GameAuth`, which performs the authentication operation.  Before trying do that, it checks to see that the MEDKit library has been fully initialized.

```html Config component template
<template>
  <div class="config">
    <h1>Configuration PIN</h1>
    <GameAuth v-if="loaded" />
  </div>
</template>
```

The value of `loaded` comes from the  `setup()` initialization function that is defined in the script portion of the file.

```javascript Initializing the config component
setup() {
  // MEDKit is initialized and provided to the Vue provide/inject system
  const medkit = provideMEDKit({
    channelId: globals.TESTING_CHANNEL_ID,
    clientId: globals.CLIENT_ID,
    role: "broadcaster",
    uaString: globals.UA_STRING,
    userId: globals.TESTING_USER_ID,
  });
  const loaded = ref(false);
  medkit.loaded().then(() => {
    loaded.value = true;
  });
  return {
    loaded,
  }
}
```

You can see here that `loaded` is set to true when the MEDKit library has finished loading. 

```javascript Report load status with a referenceable variable
const loaded = ref(false);
  medkit.loaded().then(() => {
    loaded.value = true;
```

The ```ref`` part of ```const loaded = ref(false);`allows us to use the variable in a template. Checking for that value in the template ensures that the`GameAuth\` component is only displayed after MEDKit is fully initialized. 

## PIN authentication

The `GameAuth` component is defined in the component file `Extension/src/config/components/GameAuth.vue`.  The top part is the HTML template that defines the authentication UI, and the bottom part is the JS script that provides the behavior.

```html GameAuth component template
<template>
  <div class="game-auth-container">
    <template v-if="pin">
      <div class="pin">
        PIN:
        <span>{{ pin || "No PIN found" }}</span>
      </div>
    </template>
  </div>
</template>
```

We use another ```v-if`` to ensure that ```GameAuth`component is only shown when we have obtained the PIN data. . That happens in the script's`setup()\` initialization function:

```javascript Initialize authentication by getting a PIN
setup() {
  const { medkit } = useMEDKit();
  const loaded = ref(false);
  const pin = ref("");
  const configErr = ref("");
  async function requestPIN() {
    if (!medkit) {
      configErr.value = "MEDKit could not be initialized correctly.";
    }
    try {
      await medkit.loaded();
      const resp = await medkit.signedRequest(
        "POST",
        "gamelink/token",
        JSON.stringify({})
      );
      pin.value = resp.token;
    } catch (err) {
      configErr.value = "Could not get PIN from server";
    }
  }
  onMounted(() => {
    requestPIN();
    loaded.value = true;
  });
  return {
    loaded,
    pin,
    requestPIN
  };
}
```

Here we send a `POST` request to the `gamelink/token` endpoint, setting a `pin` variable to the value of the token received in the response. 

The `onMounted()` callback function runs when the component first starts up, so `requestPIN()` is called as soon as the component starts.

## GameLink setup

The two components we have looked at perform extension-side  setup. When the extension-side setup is complete we have obtained a PIN, the broadcaster has entered it in the config page, and we have received a refresh token in the response, 

Now we have to run game-side code to initialize the GameLink connection. 

- All of the game-side code is in the C# file `GameLinkFPSBehaviour.cs`. 
- Game-side initialization is defined in the `SetupGameLinkCallbacks()` function. 

```csharp GameLink game-side setup
private void SetupGameLinkCallbacks()
{
  AuthCB = (AuthResp) =>
  {
    Error Err = AuthResp.GetFirstError();
    if (Err == null)
    {
      if (GameLink.IsAuthenticated())
      {
        String RefreshToken = GameLink.User?.RefreshToken;
        if (RefreshToken != null)
        {
          if (PlayerPrefs.GetString(GAMELINK_PLAYERPREF_RT, "") == "") PlayerPrefs.SetString(GAMELINK_PLAYERPREF_RT, RefreshToken);
        }

        GameLinkLoginUI.SetActive(false);
        GameLinkPollUI.SetActive(true);
        GameLink.SubscribeToAllPurchases();
        GameLink.SubscribeToDatastream();
      }
    }
    else
    {
      PINInput.text = "";
      PINInput.placeholder.GetComponent<Text>().text = "Authentication failed... invalid PIN!";
      PlayerPrefs.SetString(GAMELINK_PLAYERPREF_RT, "");
    }
  };
  
  ...
}
```

The authentication callback, `AuthCB()`, first checks that there is no error and that the client has authenticated successfully. If so, it stores the refresh token in the player's preferences.  The refresh token is used for automatically authenticating without needing to enter in a new PIN every time. 

This function also calls some other setup functions needed for the features that we will discuss later.

The game-side file also defines an on-click callback that defines the behavior of the "Authenticate" button in the broadcaster's config page.

```csharp Retrieve the entered PIN
public void OnClickAuthWithPIN()
{
  GameLink.AuthenticateWithPIN(PINInput.text, AuthCB);
}
```

This `AuthenticateWithPIN()` function is a GameLink API call that receives the PIN the broadcaster has submitted, and passes it to an authentication callback (in this case, the one we just defined).

# Tracking Game State

One of the core GameLink features for any project that uses a Muxy-powered extension is the ability to store and retrieve game state in real time. State information is stored as a JSON object, with key-value pairs that you define to track whatever information you need. There are different state stores with different scopes; for a complete discussion, see the [Data Tracking](../../v1.0/Development Basics/data-tracking.md) section of the documentation.

In this demo, we demonstrate basic usage by using the `ViewerState` store to keep track of how many of each type of enemy the viewer has killed. To see how the results are displayed in the overlay extension, open `localhost:4000/overlay.html` (or whatever port your npm is running on).

## Game-side setup

The code that defines and tracks state values is in the game-side C# source file, `GameLinkFPSBehaviour.cs`.

Let's look at the  `GameChannelState` struct that defines the state keys, and the `ClearState()` function that initializes the state store for the current viewer:

```csharp Initialize state
public struct GameChannelState
{
    public int hoverBotsKilled;
    public int turretsKilled;
}

private GameChannelState State;

private void ClearState()
{
  State.hoverBotsKilled = 0;
  State.turretsKilled = 0;
  GameLink.SetState(SDK.STATE_TARGET_CHANNEL, JsonUtility.ToJson(State));
}
```

`ClearState()` resets all state values, then calls `GameLink.SetState()`. It's important to make the `SetState()` call the first time you set up state, before you start manipulating it. You might also want to clear state between levels or when the game starts or closes. If there is any state you want to persist throughout levels you need another function to clear only the values you want to reset, but in our demo we just clear the state at the start of the game. 

We are setting the state of the target state store `SDK.STATE_TARGET_CHANNEL`. The target constants identify  state stores with particular scopes. This one stores per-viewer data only for the broadcaster's channel that is currently running the extension, which is the most common usage. You could also use `SDK.STATE_TARGET_EXTENSION`, which stores extension-wide state across channels. 

## Game-side state handling

To update values, we need to collect the new kill events from the client, write them to the state store, and send the new state back to the client. For this small, simple demo, we could just call `SetState()` again to update the state store, but once you start having larger data sets, it can be very slow to copy over tons of data that hasn't changed. Instead, we use a [JSON patch operation](http://jsonpatch.com/) that changes only the values that have actually changed.  

Here, the `OnEnemyKilled()` callback function collects state changes from an `EnemyKillEvent` notification, and builds a `PatchList`. This patch list efficiently batches the operations together so we won't have to send lots of individual messages.

```csharp Collecting changes
private void OnEnemyKilled(EnemyKillEvent Evt)
{
  if (Evt.Enemy.name.ToLower().Contains("hoverbot"))
  {
    State.hoverBotsKilled++;
  }
  else if (Evt.Enemy.name.ToLower().Contains("turret"))
  {
    State.turretsKilled++;
  }

  PatchList.UpdateStateWithInteger("add", "/" + nameof(State.hoverBotsKilled), State.hoverBotsKilled);
  PatchList.UpdateStateWithInteger("add", "/" + nameof(State.turretsKilled), State.turretsKilled);
}
```

 `HandlePatchListSend()` runs a timer to periodically check for updates and perform the updates using the patch list. It then clears the list and resets the timer. 

```csharp Updating the state store
private void HandlePatchListSend()
{
  PatchListSendTimer -= Time.deltaTime;
  if (PatchListSendTimer <= 0)
  {
    if (!PatchList.Empty())
    {
      GameLink.UpdateStateWithPatchList(SDK.STATE_TARGET_CHANNEL, PatchList);
      PatchList.Clear();
    }
    PatchListSendTimer = PatchListSendTime;
  }
}    

public void Update()
{
	...
  HandlePatchListSend();
}
```

The public `Update()` function will call this helper function (among other things we'll be discussing in later sections).

## Extension-side state handling

On the extension side, state handling is defined in a another component, with source code in `Extension/src/overlay/components/State.vue`, and in a support file `Extension/src/shared/hooks/use-state.js`. The support file defines how to process the data values sent from the game, so that they can be displayed in the extension.

The `channelStateFromNetwork()` function sets the new state value for each key if it exists; otherwise it initializes the value to 0.

```javascript Receive state data on the extension side
export function channelStateFromNetwork(data) {
  return {
    hoverBotsKilled: data?.hoverBotsKilled || 0,
    turretsKilled: data?.turretsKilled || 0
  };
}
```

The script in the component file (`Extension/src/overlay/components/State.vue`) defines a `setup()` function that provides the received data in a referenceable state variable, so that we can use it in the template.

```javascript Make the data available to the template
import { defineComponent, toRefs } from "vue";
import { useState } from "@/shared/hooks/use-state";

setup() {
  const { state } = useState();
  return {
  ...toRefs(state),
  };
},
```

Here we use the Vue.js `toRefs()` function as a convenience, so that anything we add to `channelStateFromNetwork`  will automatically be reflected in the template, without having to enter the same names in multiple places.

The template portion refers to the state-key variables in order to display their values:

```html Display state values
<template>
  <div class="stats">
    <hr />
    <div>
      <div>
        Hoverbots Killed:
        <span class="negative">{{ hoverBotsKilled }}</span>
      </div>
      <div>
        Turrets Killed:
        <span class="negative">{{ turretsKilled }}</span>
      </div>
    </div>
    <hr />
  </div>
</template>
```

# Polling and Voting

The polling feature allows viewers to vote on a topic, selecting from provided options. The demo shows basic usage by setting up a poll that lets the viewers choose the gravity mode, either low or high. 

## Game-side poll setup

Let's look at the game side code for polling. The game is responsible for naming a poll, defining the poll options, starting the poll, collecting and counting votes, and stopping the poll after some period of time.

```csharp
private void CleanupPoll()
{
  PollIsRunning = false;
  GameLink.SendBroadcast("stop_poll", "{}");
  GameLink.DeletePoll("gravityMode");
}

public void OnClickStartPoll()
{
  TotalVotesCountText.SetActive(true);
  PollTimerText.SetActive(true);
  List<string> PollOptions = new List<string> { "Low", "High" };
  GameLink.CreatePoll("gravityMode", "Vote for the gravity mode!", PollOptions);
  GameLink.SubscribeToPoll("gravityMode");
  GameLink.SendBroadcast("start_poll", "{\"poll_duration\":\"" + PollDuration + "\"}");
  TotalVotesCountText.GetComponent<Text>().text = "Total Votes: 0";
  PollTimer = PollDuration;
  PollIsRunning = true;
}

public void OnClickStopPoll()
{
  TotalVotesCountText.SetActive(false);
  PollTimerText.SetActive(false);

  GameLink.GetPoll("gravityMode", (Poll) =>
                   {
                     PlayerCharacterController Controller = Player.GetComponent<PlayerCharacterController>();
                     int Winner = Poll.GetWinnerIndex();
                     if (Winner != -1) // As long as there is a winner set the timer
                     {
                       GravityModeTimer = GravityModeDuration;
                     }
                     if (Winner == 0) // Low
                     {
                       GravityModeType = "Low";
                       Controller.JumpForce = 20;
                     }
                     else if (Winner == 1) // High
                     {
                       GravityModeType = "High";
                       Controller.JumpForce = 4;
                     }
                   });

  CleanupPoll();
}
```

The `OnClickStartPoll()` function creates a poll, subscribes to it, and then broadcasts the `start_poll` event with the poll's duration. It initializes the vote counter and the starts the poll timer. 

The `OnClickStopPoll()` function chooses the winning poll option and applies it, then cleans up the poll by broadcasting the `stop_poll` event and deleting the poll ID with all its data.  There's a fair amount of code here, but it's pretty straightforward.

## Extension-side poll setup

On the extension side, we need to show viewers their choices and give them a chance to submit votes. 

The top-level template in the main component file `Extension/src/overlay/App.vue` displays a  `PollVote` component only if a poll is currently active.

```html Main component template
<template>
  <div class="overlay">
    <h1>Unity FPS Demo Extension</h1>

    <div v-if="loaded">
      <Stats />

      <div>
        <Actions />
      </div>
    </div>

    <div v-else>
      Loading...
    </div>
  </div>

  <PollVote v-if="isVoting" :eventDuration="eventDuration" />
</template>
```

The script for this page initializes the variables `isVoting` and `eventDuration`, and then subscribes to the event topics that will tell the extension when a new poll starts with a given duration, and when it stops.

```javascript Main component script
// Initialize variables used in HTML
const eventDuration = ref(0);
const isVoting = ref(false);
const loaded = ref(false);

// MEDKit is initialized and provided to the Vue provide/inject system
const medkit = provideMEDKit({
  channelId: globals.TESTING_CHANNEL_ID,
  clientId: globals.CLIENT_ID,
  role: "viewer",
  uaString: globals.UA_STRING,
  userId: globals.TESTING_USER_ID,
  transactionsEnabled: true,
});

provideState(medkit);

// MEDKit must fully load before it is available
medkit.loaded().then(() => {
  loaded.value = true;

  medkit.listen("start_poll", (data) => {
    if (data) {
      eventDuration.value = data.poll_duration;
    }
    isVoting.value = true;
  });

  medkit.listen("stop_poll", () => {
    isVoting.value = false;
  });

  medkit.listen("game_over", () => {
    isVoting.value = false; 
  });
});
```

These listeners receive the messages we sent from GameLink, We listen for the `start_poll`  event, providing a handler that sets `isVoting` to true and sets `eventDuration` to the value received from GameLink. 

## Extension-side voting

Now lets look at the actual polling component `PollVote`, defined in the component file `Extension/src/overlay/components/PollVote.vue`. 

The template portion defines the voting UI.

```html PollVote component template
<template>
  <div class="voting" :class="{ voted: countdownTimer === 0 }">
    <div v-if="!voted" class="instructions">
      Vote to change the gravity!

      <div class="timer">
        Time Left To Vote:
        <div class="clock">{{ countdownTimer }}</div>
      </div>
    </div>

    <div v-else class="instructions">
      Your vote has been counted!
    </div>

    <div class="actions" v-if="!voted">
      <button :disabled="countdownTimer <= 0" @click="voteForOption(0)">
        Low Gravity
      </button>

      <button :disabled="countdownTimer <= 0" @click="voteForOption(1)">
        High Gravity
      </button>
    </div>
  </div>
</template>
```

Here we display the countdown timer, instructions, and choice buttons for voting. 

To end the poll, the first element changes the `<div>` class from `voting` to `voted` when `countdownTimer` reaches 0:

```javascript Using a CS class to control visibility
<div class="voting" :class="{ voted: countdownTimer === 0 }">
```

In the corresponding CSS file, we see that the `voted` class stops displaying this `<div>` , which contains this entire template.

```css CSS class definition
&.voted {
	display: none;
}
```

The script for the `PollVote` component collects and processes votes.

```javascript PollVote component script
export default defineComponent({
  props: {
    eventDuration: {
      default: 25,
      type: Number,
    },
  },
  setup(props) {
    const { medkit } = useMEDKit();
    const voted = ref(false);
    const countdownTimer = ref(props.eventDuration);
    const voteForOption = (option) => {
      medkit.vote("gravityMode", option).then(() => {
        voted.value = true;
        countdownTimer.value = 3;
      });
    };
    const startCountdown = () => {
      if (countdownTimer.value > 0) {
        setTimeout(() => {
          countdownTimer.value -= 1;
          startCountdown();
        }, 1000);
      }
    };
    onMounted(() => {
      startCountdown();
    });
    return {
      voteForOption,
      countdownTimer,
    };
  },
});
```

The `voteForOption()` function calls `medkit.vote()` with the poll-id `"gravityMode"` and the option the viewer selected. It also records the fact that this viewer has voted in this poll, and when. This is because a viewer can change their vote will the poll is still running. Only the latest vote is counted in the results. 

If you recall, the  `onMounted()` callback runs when a component has completed loading. For this component, the callback starts the countdown timer, using the `eventDuration` we passed in from the main component.

# Datastream Events

The GameLink Datastream service is the basis for communication between the game and an extension. An extension uses the datastream to publish events, and the game listens for those events and responds using a callback. 

Your game must subscribe to the service as part of initialization, using the GameLink `SubscribeToDatastream()` method. You can only subscribe after authentication is successful. In the sample code, we did this in the setup code as part of the authentication callback:

```text Initializing game-extension communication
private void SetupGameLinkCallbacks()
{
  AuthCB = (AuthResp) =>
  {
    Error Err = AuthResp.GetFirstError();
    if (Err == null)
    {
      if (GameLink.IsAuthenticated())
      {
        ...
        GameLinkLoginUI.SetActive(false);
        GameLinkPollUI.SetActive(true);
        GameLink.SubscribeToAllPurchases();
        GameLink.SubscribeToDatastream();
      }
    }
  ...
}
```

## Game-side event definition callbacks

Your game defines the event types that your extension needs, and the event-handler callbacks that define the game behavior for when the event occurs. 

To show how it works, the sample game code defines events that spawn pick-ups and monsters.  A callback loops through event notifications, extracts the type of pickup or monster requested, and creates the requested object.

```csharp Define events and respond to notifications
public struct GameDatastreamEvent
{
    public string spawnMonsterType;
    public string spawnPickupType;
}

private void SetupGameLinkCallbacks()
{
  DatastreamCB = (Data) =>
  {
    foreach(DatastreamUpdate.Event Event in Data.Events)
    {
      GameDatastreamEvent GameEvent = JsonUtility.FromJson<GameDatastreamEvent>(Event.Json);
      System.Random R = new System.Random();

      if (GameEvent.spawnMonsterType == "hoverbot")
      {
        GameObject Hoverbot = Instantiate(HoverbotPrefab, RandomSpawnPositionNearby(R.Next(6, 18), R.Next(-5, 5)), Quaternion.identity);
      }
      if (GameEvent.spawnMonsterType == "turret")
      {
        GameObject Hoverbot = Instantiate(TurretPrefab, RandomSpawnPositionNearby(R.Next(6, 18), R.Next(-5, 5)), Quaternion.identity);
      }


      if (GameEvent.spawnPickupType == "healthpack")
      {
        Instantiate(HealthpackPrefab, RandomSpawnPositionNearby(R.Next(4, 8), R.Next(-5, 5)), Quaternion.identity);
      }
      else if (GameEvent.spawnPickupType == "shotgun")
      {
        Instantiate(ShotgunPrefab, RandomSpawnPositionNearby(R.Next(4, 8), R.Next(-5, 5)), Quaternion.identity);
      }
      else if (GameEvent.spawnPickupType == "jetpack")
      {
        Instantiate(JetpackPrefab, RandomSpawnPositionNearby(R.Next(4, 8), R.Next(-5, 5)), Quaternion.identity);
      }
      else if (GameEvent.spawnPickupType == "launcher")
      {
        Instantiate(LauncherPrefab, RandomSpawnPositionNearby(R.Next(4, 8), R.Next(-5, 5)), Quaternion.identity);
      }
    }
	};
}
```

> 📘 We've kept the code minimal here to illustrate the technique, but in a real game you also want to make a cooldown check for spawning, so that someone can't spam events from the extension.

## Extension-side event generation

The extension code that sends these events out is located at `Extension/src/overlay/components/Actions.vue`.  
The template portion defines buttons for for spawning monsters and pickups.

```html Connect buttons to event-generation
<template>
  <div class="actions">
    <h4 class="positive">Help The Player!</h4>

    <button @click="spawnPickup('healthpack')">Spawn Healthpack</button>
    <button @click="spawnPickup('shotgun')">Spawn Shotgun</button>
    <button @click="spawnPickup('jetpack')">Spawn Jetpack</button>
    <button @click="spawnPickup('launcher')">Spawn Launcher</button>

    <h4 class="negative">Sabotage The Player!</h4>

    <button @click="spawnMonster('hoverbot')">Spawn Hoverbot</button>
    <button @click="spawnMonster('turret')">Spawn Turret</button>

    <BitsInterface />

    <button v-if="bitsEnabled" @click="spawnWithBits('turret')">
      Spawn Turret for Bits
    </button>
  </div>
</template>
```

The  `setup()` function in the page's script defines the click callbacks that generate events:

```javascript Generate events
setup() {
  const { medkit } = useMEDKit();
  // Initialize convenience wrapper for Twitch interactions.
  const { bitsEnabled } = useTwitchContext();
  const sendDatastream = (event) => {
    medkit.signedRequest("POST", "datastream", event);
  };
  const spawnMonster = (monsterType) => {
    var event = {
      spawnMonsterType: monsterType,
      spawnPickupType: "",
    };
    sendDatastream(event);
  };
  const spawnPickup = (pickupType) => {
    var event = {
      spawnMonsterType: "",
      spawnPickupType: pickupType,
    };
    sendDatastream(event);
  };
  return {
    bitsEnabled,
    spawnMonster,
    spawnPickup,
  };
},
```

The MEDKit `signedRequest()` method sends  a `POST` request to the `datastream` endpoint with our event data.  
The event data includes a field that tells the game which type of monster or pickup was requested.

# Bits Transactions

Monetization of your extension is important, so handling bits transactions is relatively painless. Transaction events report Twitch Bit Transaction activity involving an extension user; as part of the setup code, we subscribed to this service (along with the Datastream service), using the `SubscribeToAllPurchases()` Gamelink  function.

In the demo a player can use bits to spawn more powerful hoverbots and turrets. 

## Game-side transaction handling

The game code defines a callback to handle purchase transactions. 

```csharp Receive and handle transaction notifications
private void SetupGameLinkCallbacks()
{
  TransactionCB = (Purchase) =>
  {
    System.Random R = new System.Random();
    if (Purchase.SKU == "spawn-turret")
    {
      GameObject Turret = Instantiate(TurretPrefab, RandomSpawnPositionNearby(R.Next(6, 18), R.Next(-5, 5)), Quaternion.identity);
      Turret.GetComponent<Health>().MaxHealth += 200;
    }
    else if(Purchase.SKU == "spawn-hoverbot")
    {
      GameObject Hoverbot = Instantiate(HoverbotPrefab, RandomSpawnPositionNearby(R.Next(6, 18), R.Next(-5, 5)), Quaternion.identity);
      Hoverbot.GetComponent<Health>().MaxHealth += 50;
    }
  };
}
```

In response to a bit-transaction notification, the game checks the SKU passed in the event data and spawns an object of the appropriate type with an increased Health value.  

## Extension-side transaction handling

The extension's main file,  `Extension\src\overlay\main.js`, defines some products that the extension offers for purchase. Each product is a JavaScript object.

```javascript Define purchasable products
window.MEDKIT_PURCHASABLE_ITEMS = [
{
  sku: "spawn-hoverbot",
  displayName: "Spawn Extra HP Hoverbot",
  cost: {
    amount: 50,
    type: "test-cost"
  }
  },
  {
  sku: "spawn-turret",
  displayName: "Spawn Extra HP Turret",
  cost: {
    amount: 100,
    type: "test-cost"
  }
}
```

On the extension side, the `BitsInterface` component defines a UI that allows players purchase products, in  the file `Extension/src/overlay/components/BitsInterface.vue`. 

In the script portion of the component, the `setup()` function does two things:

- `getProducts()` creates a list of the products we offer, so that the template can create a button for each one. Each item in the list is one of the JS objects that describes a purchasable item. 
- `confirmSpendWithTwitch()` defines the button behavior that sends the requested purchase to Twitch. 

```javascript Make a list of products
setup() {
  const { medkit } = useMEDKit();
  const productList = ref([]);

  const confirmSpendWithTwitch = (product) => {
    medkit.purchase(product.sku);
  };

  medkit.getProducts().then((products) => {
    productList.value = products;
  });

  return {
    confirmSpendWithTwitch,
    productList,
  };
}
```

The template portion of the code defines the buttons. A loop makes a button for each product we offer, using the product fields to populate the button labels. 

```html Connect purchase buttons to purchase behavior
<template>
  <div class="bits-interface">
    <transition name="fade">
      <div v-if="productList.length > 0">
        <template v-for="product in productList" :key="product.SKU">
          <button @click="confirmSpendWithTwitch(product)">
            {{ product.displayName }}:
            <strong>{{ product.cost.amount }}</strong> Bits!
          </button>
        </template>
      </div>
    </transition>
  </div>
</template>
```

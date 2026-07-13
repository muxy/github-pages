---
title: "Polling"
slug: "ws-polling"
excerpt: "A game client can create and update audience polls, and receive real-time updates on voting results using the `poll` topic."
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Tue Oct 05 2021 20:57:57 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Feb 01 2022 22:47:45 GMT+0000 (Coordinated Universal Time)"
---
# Create a Poll

To create a new poll, send a message with the `create` action with the `poll` target.  
The `data` payload is a JSON-encoded object with the following format:

```json Poll data format
{
  // A unique identifer for this poll.
  "poll_id": String,

  // The prompt displayed to viewers.
  "prompt": String,

  // An array of options that viewers can select to vote for. This is limited to 64 entries.
  "options": String[],

  // An optional data object that is passed to the viewer extension along with the poll.
  // Content and usage is developer-defined.
  "user_data"?: Object
}
```

The new poll is stored as a state value in the channel-wide state store. You can access it using the `poll_id` value as the key. The value of this key is a JSON object that contains the `prompt`, `options`, and `user_data` fields.

The following example creates a poll to gauge the favorite color of the audience.

```json Poll-creation example data
{
  "action": "create",
  "params": {
    "request_id": 100,
    "target": "poll"
  },

  "data": {
    "poll_id": "favorite-color",
    "prompt": "What is your favorite color?",
    "options": ["Blue", "Red", "Orange"],
    "user_data": {
      "has_mystery_prize": true
    }
  }
}
```

## Send votes to a poll

Creating a poll through GameLink is equivalent to creating a poll through the REST API.  
Any user can send a vote to the server by calling `POST vote?id=`_vote_id_. 

## Get poll logs

A user with `admin` role can obtain the full vote logs by calling `GET vote_logs` with an administrator JWT.

# Receive Poll Results

Any client can subscribe to poll update events. The server sends update notifications containing the latest poll results, at most once per second.

> Polls that are not actively receiving votes from the audience are considered "dead", and are not included in update notifications. 

**Request** 

To subscribe, use `subscribe` action and provide  poll ID in `topic_id`.  
You can use the special character `*` to receive updates for all polls created by the caller.

```json Poll event subscription-request body
{
  "action": "subscribe",
  "params": {
    "request_id": 200,
    "target": "poll"
  },

  "data": {
    "topic_id": "favorite-color"
  }
}
```

## Poll event notifications

Polls periodically emit an event with the `update` action whose `target` is `poll`.  
The server automatically stops sending update messages for a poll 5 minutes after the last vote is received.

The `data` contains a  `results` field containing an array of votes for each option. The `results` array is the same length as the `options` array, with a one-to-one mapping between the values.  
The `poll` details as specified on creation, are also included.

In the following example, the option `Blue` has 50 votes, `Red` has two votes, and `Orange` has 13 votes.  

```json Poll update response example data
{
  "action": "update",
  "params": {
    "request_id": 0xffff,
    "target": "poll",
  },

  "data": {
    "topic_id": "favorite-color",
    "results": [50, 2, 13],
    "poll": {
      "prompt": "What is your favorite color?",
      "options": ["Blue", "Red", "Orange"],
      "user_data": {
        "has_mystery_prize": true
      }
    }
  }
}
```

## Request poll results

Anyone can request the results for a poll at any time until the poll is manually deleted. 

**Request**

Use the `get` action with a `target` of `poll`, and specify the `poll_id` in the `data`.

```json Poll result request body
{
  "action": "get",
  "params": {
    "request_id": 300,
    "target": "poll"
  },

  "data": {
    "poll_id": "favorite-color"
  }
}
```

**Response**

The response from the server matches the form of the poll-update event notification.

```json Poll result response data example
{
  "action": "get",
  "params": {
    "request_id": 300,
    "target": "poll"
  },

  "data": {
    "topic_id": "favorite-color",
    "results": [50, 2, 13],
    "poll" : {
      "prompt": "What is your favorite color?",
      "options": ["Blue", "Red", "Orange"],
      "user_data": {
        "has_mystery_prize": true
      }
    }
  }
}
```

# Delete a Poll

There is a limit to the number of polls that can be active for a given user account.  
It is up to the game client to remove polls when they are no longer needed.

A deleted poll is no longer be accessible by viewers, and no further poll result updates are sent.

**Request**

Use the `delete` action with a `target` of `poll`, and specify the `poll_id` in the `data`.

```json Poll deletion request body
{
  "action": "delete",
  "params": {
    "request_id": 300,
    "target": "poll"
  },

  "data": {
    "poll_id": "favorite-color"
  }
}
```

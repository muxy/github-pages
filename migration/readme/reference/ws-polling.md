# Polling

A game client can create and update audience polls, and receive real-time updates on voting results using the `poll` topic.

# Create a Poll

To create a new poll, send a message with the `create` action with the `poll` target.
The `data` payload is a JSON-encoded object with the following format:

[block:code]
{
  "codes": [
    {
      "code": "{\n  // A unique identifer for this poll.\n  \"poll_id\": String,\n\n  // The prompt displayed to viewers.\n  \"prompt\": String,\n\n  // An array of options that viewers can select to vote for. This is limited to 64 entries.\n  \"options\": String[],\n\n  // An optional data object that is passed to the viewer extension along with the poll.\n  // Content and usage is developer-defined.\n  \"user_data\"?: Object\n}",
      "language": "json",
      "name": "Poll data format"
    }
  ]
}
[/block]

The new poll is stored as a state value in the channel-wide state store. You can access it using the `poll_id` value as the key. The value of this key is a JSON object that contains the `prompt`, `options`, and `user_data` fields.

The following example creates a poll to gauge the favorite color of the audience.

[block:code]
{
  "codes": [
    {
      "code": "{\n  \"action\": \"create\",\n  \"params\": {\n    \"request_id\": 100,\n    \"target\": \"poll\"\n  },\n\n  \"data\": {\n    \"poll_id\": \"favorite-color\",\n    \"prompt\": \"What is your favorite color?\",\n    \"options\": [\"Blue\", \"Red\", \"Orange\"],\n    \"user_data\": {\n      \"has_mystery_prize\": true\n    }\n  }\n}",
      "language": "json",
      "name": "Poll-creation example data"
    }
  ]
}
[/block]

## Send votes to a poll

Creating a poll through GameLink is equivalent to creating a poll through the REST API.
Any user can send a vote to the server by calling `POST vote?id=`*vote\_id*.

## Get poll logs

A user with `admin` role can obtain the full vote logs by calling `GET vote_logs` with an administrator JWT.

# Receive Poll Results

Any client can subscribe to poll update events. The server sends update notifications containing the latest poll results, at most once per second.

> Polls that are not actively receiving votes from the audience are considered "dead", and are not included in update notifications.

**Request**

To subscribe, use `subscribe` action and provide  poll ID in `topic_id`.
You can use the special character `*` to receive updates for all polls created by the caller.

[block:code]
{
  "codes": [
    {
      "code": "{\n  \"action\": \"subscribe\",\n  \"params\": {\n    \"request_id\": 200,\n    \"target\": \"poll\"\n  },\n\n  \"data\": {\n    \"topic_id\": \"favorite-color\"\n  }\n}",
      "language": "json",
      "name": "Poll event subscription-request body"
    }
  ]
}
[/block]

## Poll event notifications

Polls periodically emit an event with the `update` action whose `target` is `poll`.
The server automatically stops sending update messages for a poll 5 minutes after the last vote is received.

The `data` contains a  `results` field containing an array of votes for each option. The `results` array is the same length as the `options` array, with a one-to-one mapping between the values.
The `poll` details as specified on creation, are also included.

In the following example, the option `Blue` has 50 votes, `Red` has two votes, and `Orange` has 13 votes.

[block:code]
{
  "codes": [
    {
      "code": "{\n  \"action\": \"update\",\n  \"params\": {\n    \"request_id\": 0xffff,\n    \"target\": \"poll\",\n  },\n\n  \"data\": {\n    \"topic_id\": \"favorite-color\",\n    \"results\": [50, 2, 13],\n    \"poll\": {\n      \"prompt\": \"What is your favorite color?\",\n      \"options\": [\"Blue\", \"Red\", \"Orange\"],\n      \"user_data\": {\n        \"has_mystery_prize\": true\n      }\n    }\n  }\n}",
      "language": "json",
      "name": "Poll update response example data"
    }
  ]
}
[/block]

## Request poll results

Anyone can request the results for a poll at any time until the poll is manually deleted.

**Request**

Use the `get` action with a `target` of `poll`, and specify the `poll_id` in the `data`.

[block:code]
{
  "codes": [
    {
      "code": "{\n  \"action\": \"get\",\n  \"params\": {\n    \"request_id\": 300,\n    \"target\": \"poll\"\n  },\n\n  \"data\": {\n    \"poll_id\": \"favorite-color\"\n  }\n}",
      "language": "json",
      "name": "Poll result request body"
    }
  ]
}
[/block]

**Response**

The response from the server matches the form of the poll-update event notification.

[block:code]
{
  "codes": [
    {
      "code": "{\n  \"action\": \"get\",\n  \"params\": {\n    \"request_id\": 300,\n    \"target\": \"poll\"\n  },\n\n  \"data\": {\n    \"topic_id\": \"favorite-color\",\n    \"results\": [50, 2, 13],\n    \"poll\" : {\n      \"prompt\": \"What is your favorite color?\",\n      \"options\": [\"Blue\", \"Red\", \"Orange\"],\n      \"user_data\": {\n        \"has_mystery_prize\": true\n      }\n    }\n  }\n}",
      "language": "json",
      "name": "Poll result response data example"
    }
  ]
}
[/block]

# Delete a Poll

There is a limit to the number of polls that can be active for a given user account.
It is up to the game client to remove polls when they are no longer needed.

A deleted poll is no longer be accessible by viewers, and no further poll result updates are sent.

**Request**

Use the `delete` action with a `target` of `poll`, and specify the `poll_id` in the `data`.

[block:code]
{
  "codes": [
    {
      "code": "{\n  \"action\": \"delete\",\n  \"params\": {\n    \"request_id\": 300,\n    \"target\": \"poll\"\n  },\n\n  \"data\": {\n    \"poll_id\": \"favorite-color\"\n  }\n}",
      "language": "json",
      "name": "Poll deletion request body"
    }
  ]
}
[/block]
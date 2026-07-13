---
title: "Polls and User Voting"
slug: "voting"
excerpt: "An broadcaster or administrator can create and manage a named poll, and collect users' votes."
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Wed Sep 15 2021 16:44:59 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Feb 01 2022 22:29:05 GMT+0000 (Coordinated Universal Time)"
---
Voting is a form of data aggregation that collects user choices in a poll that you offer. To elicit viewer responses, you must set up a poll that offers a set of choices, display the choices to viewers, and give viewers a way to submit their votes.

- Your game or extension is responsible for setting up a poll with a unique ID, defining and presenting a numbered list of choices to viewers, and giving user a means to submit their vote.

- Polls expire automatically 1 day after the last vote is cast. After that point, all vote values are removed. If you then send data using the same `poll_name` value, the server starts a new accumulation.

- Votes are unique per user; that is, a given poll retains only one vote value for a given user. If a user sends additional requests to the `vote` endpoint, giving the same poll name,  that user's vote changes  to the latest value.

> 👍 Ensuring unique votes
> 
> The result includes the viewer's real ID if it is known at the time the vote is cast, but falls back to using their opaque ID. If your extension depends on absolutely correct voting behavior, you should only allow viewers who have shared their ID to vote. Otherwise, it is possible for viewers to vote multiple times by repeatedly sharing and unsharing their ID, which gives them new opaque ID each time.

# Sending Votes

For basic voting behavior, Muxy provides a `vote` endpoint, accessed in JavaScript through the `SDK.vote()` method.  
Call the `SDK.vote()` method to send and add a viewer's vote to a named poll.

`SDK.vote(poll_name, value);`

- _poll_name_  is a developer-defined string that identifies the poll. By convention, this is a lower-case, hyphen-separated alphanumeric string.  All votes sent to this poll are counted towards the results. Prefix the name with "global" to create an [extension-wide](#extension-wide-votes) poll.
- _value_ is an integer in the range [-1000, 1000] that indicates which choice the user prefers. 

The following example submits a vote for choice number 1 in a poll with the ID "my-poll". If the poll does not yet exist, it is created and this vote is recorded.

```javascript Submit a vote in a new or existing poll
const medkit= new Muxy.SDK();
medkit.vote('my-poll', 1);
```

# Getting Votes

A viewer or broadcaster can get the current status of a running poll using the `SDK.getVoteData(poll_name)` method.

```javascript Check poll status
const opts = new Muxy.DebuggingOptions();
opts.role('viewer');
Muxy.debug(opts);

const medkit = new Muxy.SDK();
medkit.getVoteData('my-poll').then(voteData => {
  console.log(voteData.sum);
});
```

This method returns a Promise that resolves to a JSON blob containing information about the poll. This example shows the status of a poll that has received exactly one vote, for choice 1. 

```json Voting statistics
{
    mean: 1,
    sum: 1,
    stddev: 0,
    specific: [0, 1, 0, 0, 0, 0],
    count: 1
    vote: 1
}
```

The JSON object has the following fields:



| Field | Meaning |
| --- | --- |
| `mean` | The average of all the votes cast in this poll. A floating-point number. |
| `sum` | The sum of all the values cast in this poll. |
| `stddev` | An approximate standard deviation of all the votes cast in this poll. A floating-point number. |
| `specific` | Captures the number of votes cast with the integer values between 0 and 31, inclusive.  <br>The number of votes cast for such a value is stored in the array at the index of that value. That is, the number of votes cast for the integer value `12` can be found in `specific[12]`. |
| `count` | The number of users who have voted. |
| `vote` | The value of the vote that the current user cast. Absent if the user has not yet cast a vote. |




# Automatic Vote Updates

While votes are being sent to the voting system, the server sends periodic update events to  
all viewers. Update events are sent at most every 5 seconds, and so can include data for  
multiple votes. We suggest using the vote update events to refresh your interface in real time; however, if no update events have been seen in more than 5 seconds, you can request the vote data directly to obtain most recent data.

The following example sets up the viewer to listen for automatic update events for the poll we named "my-poll". It provides a callback function to handle the data contained in the event .

```javascript Listen for poll updates
const opts = new Muxy.DebuggingOptions();
opts.role('viewer');
Muxy.debug(opts);

const medkit= new Muxy.SDK();
// listen for updates to "my-poll', and provide a callback handler
medkit.listen('vote_update:my-poll', voteData => {
// The handler extracts and displays a value from the event data
  console.log(voteData.sum);
});
```

The callback handler (`voteData` in this example) receives the event ID and a value parameter containing a JSON object has the same structure and fields as the  `getVoteData()` response:

```json Poll update event data
{
    "id": "my-poll",
    "stats": {
        "stddev": 0,
        "mean": 0,
        "sum": 0,
        "specific": [0, 1, 0, 0, 0, 0],
        "count": 1,
    }
}
```

# Extension-Wide Votes

If a poll name is prefixed with "global",  the vote is shared across all instances of the extension. This is useful if multiple broadcasters are co-streaming an event with an extension, so that every viewer's vote counts for the entire event.

```javascript Submit a vote to a new or existing global poll
const opts = new Muxy.DebuggingOptions();
opts.role('viewer');
Muxy.debug(opts);

const medkit= new Muxy.SDK();
medkit.vote('global-12345', 1);
```

# Voting Logs

Voting logs are maintained per poll. For a caller with an admin-tier JWT, you can use the `SDK.getFullVoteLogs()` method to obtain a log of all votes cast by users. 

```javascript Get voting logs
const opts = new Muxy.DebuggingOptions();
opts.role('admin');
Muxy.debug(opts);

const medkit= new Muxy.SDK();
// ...get the log for a global poll...
medkit.getFullVoteLogs('global-12345').then(logs => {
  const audit = logs.result;

  // ... process the audit logs ...
  const valueToUsersMapping = {};
  for (const i = 0; i < audit.length; ++i) {
    const value = audit[i].value;
    const identifier = audit[i].identifier;

    const list = valueToUsersMapping[value] || [];
    list.append(identifier);

    valueToUsersMapping[value] = list;
  }
});
```

**Response**

The log is returned as a JSON object in the following form:

```json Voting log format
{
  "result": [
    { "identifier": "U1235161", "value": 1 }
  ]
}
```

The objects in the result array are ordered from oldest to most recent. Each object shows the voter's user ID and their vote value.  
If your extension allows users to change their vote by voting more than once, a given identifier can have more than one entry in the result list.

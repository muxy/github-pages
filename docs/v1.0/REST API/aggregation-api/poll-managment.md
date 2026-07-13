---
title: "Poll Management"
slug: "poll-managment"
excerpt: "The voting endpoints allow for high-volume polling activity."
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Mon Sep 27 2021 18:48:22 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Wed Feb 02 2022 19:14:00 GMT+0000 (Coordinated Universal Time)"
---
Poll administrators can create, manage, and end polls, track votes and voting statistics, and get a log with the combined results from all voters. A poll administrator must have one of  `broadcaster`, `admin` , or `backend` role.

Any viewer can cast a vote in an existing poll, which you send to the server using a POST request to the `vote` endpoint.

# Poll naming and scope

Collections of votes are grouped by a poll identifier that is unique to your Extension Client ID.  
Poll administrators name a poll on creation. 

A poll name is a case-sensitive alphanumeric string, which can contain the special character `$`, and the optional prefix `global-`.   Polls IDs without this prefix must be unique within the channel, and the poll is available for voting within the channel. A global poll is available to all instances of an extension running on Twitch.

A poll and its voting data persist for up to a week after the last vote cast on it, but a poll administrator can end the poll at any time.  

## Option values and voting statistics

On creation, the poll admin creates a set of options and defines the appearance of each option. Each option is associated with an integer value. 

When a viewer selects an option, the extension casts a vote for that option using a POST call to the `vote` endpoint, containing the value of the selected option. Each vote is associated with the user who cast that vote. A user cannot cast multiple votes in the same poll. The POST endpoint does accept multiple requests for a user. Each request after the initial vote changes the user's vote value, rather than casting an additional vote.

The GET and POST calls both return a statistical summary of the current voting status for the given poll.  Votes can be cast for for any integer value between -99 and 99, inclusive. Votes outside  
of the range [0, 63] do not appear in the `stats.specific` array in the response, but  
are  used to compute the `stddev` (standard deviation), `mean`, `sum`, and `count` fields. 

# Retrieving Vote Information

Use a GET call to retrieve vote information for a given poll. The call returns both the current vote for the current user (if any) and a statistical summary of all votes received for the poll.

**Request**

Any caller can make this request.

```shell Request voting information
GET /v1/e/vote?id=${poll_id}
```

| Parameter | Description                                                                    |
| :-------- | :----------------------------------------------------------------------------- |
| _poll_id_ | Optional. A valid poll ID string. If not present, the value `default` is used. |

**Response**

If the call succeeds, the body of the response contains a JSON-encoded object with the following format.

```json Voting information snapshot
{
    "stats": {
        "stddev": number, 
        "mean": number, 
        "sum": number, 
        "specific": number[64], 
        "count": number
    },
    "vote': number?
}
```

The value of each individual vote is an integer. The statistical values are floating-point numbers.



| Field | Description |
| --- | --- |
| `vote` | The vote cast by the current user, if one exists.  <br>If no such vote exists, this field does not appear in the response. |
| `stats.stddev` | The standard deviation of all votes cast on this poll. |
| `stats.mean` | The numerical average of all votes cast on this poll. |
| `stats.sum` | The numerical sum of all votes cast on this poll. |
| `stats.specific` | An array containing the count of votes cast for the index-value option. That is, the first value in the array is the number of votes cast for option 0. |
| `stats.count` | The number of votes cast on this poll. |




If the call fails, the body of the response contains error information.

# Casting Votes

Use a POST call to cast a vote in a poll. 

**Request**

Any caller can make this request.

```shell Cast a vote
POST /v1/e/vote?id=${poll_id}
```

| Parameter | Description                                                                    |
| :-------- | :----------------------------------------------------------------------------- |
| _poll_id_ | Optional. A valid poll ID string. If not present, the value `default` is used. |

The body of the request contains the integer value of the option the viewer is voting for, in JSON format. 

```json
{
    "value": number
}
```

**Response**

If the call succeeds, the POST call returns the same response as the GET call, with both this new vote value and a statistical summary of the current voting status for this poll.

If the call fails, the body of the response contains error information.

# Clearing Poll Data

Polls are automatically deleted a week after the last vote is cast. 

A poll administrator can use the DELETE call to end a poll at any time, but if a client submits a vote using the same ID, the poll is recreated and the new vote is logged. 

> 📘 Clear stale votes
> 
> If you re-use a poll ID, send a DELETE request immediately _before_ running it again, to clear any accumulated votes that might have been posted earlier. It is not an error to delete a poll that does not exist, so it's good practice to do this any time you start a new poll.

**Request**

The caller must have one of  `broadcaster`, `admin` , or `backend` role,

```shell Request poll deletion
DELETE /v1/e/vote?id=${poll_id}
```

**Response**

If the call succeeds, it deletes all votes and logs for the given poll, and the response contains an empty JSON object. 

If the call fails, the body of the response contains error information.

# Getting Vote Logs

A poll administrator can use a GET call to the `vote_logs` endpoint to retrieve a log of individual votes cast in a given poll.  

**Request**

The caller must have the `admin`, or `backend` role.

```shell Request poll results
GET /v1/e/vote_logs?id=${poll_id}
```

| Parameter | Description                                                                    |
| :-------- | :----------------------------------------------------------------------------- |
| _poll_id_ | Optional. A valid poll ID string. If not present, the value `default` is used. |

**Response**

If the call succeeds, the body of the response contains a JSON-encoded array of results in the following format:

> 🚧 This endpoint's response can be very large if many votes have been cast.  
> Only vote-processing backends should call this endpoint.

```json Poll results
{
    "result": [{
        "identifier": string, 
        "opaque": string, 
        "value": number, 
        "timestamp": number
    }]
}
```



| Field | Description |
| --- | --- |
| `identifier` | String. The Twitch UserID of vote caster, if the user was shared; if not, contains the OpaqueID.  <br>UserIDs start with the letter `U`. |
| `opaque` | String. The OpaqueID of a vote caster. Always exists |
| `value` | Integer. The option value the user's latest vote was cast for. |
| `timestamp` | Number. The Unix millisecond timestamp when the server received this user's latest vote. |




If the call fails, the body of the response contains error information.

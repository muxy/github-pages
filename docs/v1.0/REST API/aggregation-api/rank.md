---
title: "Basic Ranking"
slug: "rank"
excerpt: "The REST API provides a ranking service that collects user input and counts matching values."
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Mon Sep 27 2021 18:48:33 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Jan 11 2022 17:26:17 GMT+0000 (Coordinated Universal Time)"
---
A broadcaster or administrator can present viewers with open-ended questions, such as "Who is your favorite player?" or "Where do you live?". The ranking service collects user responses and sorts matching responses by frequency.  

The service counts the number of users who send matching response strings for a given key. It does not evaluate or manipulate responses in any way.  You can query the key to determine the most popular responses. 

- Use a [POST](../../../v1.0/REST API/aggregation-api/rank-1.md) call to submit viewer responses to a question that you present.

- Use a [GET](../../../v1.0/REST API/aggregation-api/rank-2.md) call to retrieve ranked responses to a given question.

- You can use a [DELETE](../../../v1.0/REST API/aggregation-api/rank-3.md) call to remove a ranking buffer and its data at any time. If it is not deleted, ranking data expires automatically 1 day after the last entry is added. At that point, all data for the ranking ID is removed. If you then send data using the same ranking ID value, the server starts a new accumulation. 

# Setting Rankable Questions

A developer-defined ranking ID string identifies an accumulation buffer. The developer is responsible for associating a ranking ID with a question, and presenting the question to viewers. All responses that are submitted with the same ID are aggregated and ranked. 

# Submitting Answers

When a user responds to a question, send their response to the ranking service with a POST request to the `rank` endpoint, using the developer-defined rankable-question ID. If the named buffer does not yet exist, it is created with the current data. If it already exists, the current data is appended to any existing data in the buffer. 

**Request**

```shell Submit a value to a ranking buffer
POST /v1/e/rank?id=${id}
```

| Parameter | Description                                                              |
| :-------- | :----------------------------------------------------------------------- |
| _id_      | String. The name of the accumulation buffer to create or append data to. |

The body of the POST request contains a user's response to the question, as a JSON object. The string the user entered is the value of the `key` field.

```json Rankable data format
{
  key: "DOTA"
}
```

The data is stored along with collection data, including the user information of the poster and the time the post was received. 

**Response**

Ranking data is unique per user; that is, the service retains only one value for a given user for a given ranking ID. If a user sends additional responses to the same question, only the latest value is counted. In this case, the response to the successful POST request returns the user's previous answer.

```json Voting status and history data
{
  "accepted": true,         // Whether the entry has been added to the rankings
  "original": "Serious Sam" // Optional. The previous value submitted by this viewer, if any. 
}
```

# Retrieving Ranking Results

To retrieve results for a given question, send a GET request  to the `rank` endpoint with the ranking ID.  The GET call must be authorized by a JWT with `broadcaster`, `admin`, or `backend` role.  
The call reports all response strings that have been received, and the number of users who have submitted each response, in order of popularity.

**Request**

```shell Retrieve ranking results
GET /v1/e/rank?id=${id}
```

| Parameter | Description                                                   |
| :-------- | :------------------------------------------------------------ |
| _id_      | String. The name of the ranking accumulation buffer to query. |

**Response**

If the call succeeds, the body of the response contains a JSON-encoded array. Each response value becomes a `key` value in this array, up to the top 100 responses. Any response value that matches another value increments a `score` for that value. The response array is sorted by score to show how many people submitted the given response.

```json Ranking result data
{
  "data": [
    {
      "key": "DOTA",
      "score": 12
    },
    {
      "key": "FIFA 2014",
      "score": 8
    }
  ]
}
```

If the call fails, the body of the response contains error information.

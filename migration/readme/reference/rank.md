# Basic Ranking

The REST API provides a ranking service that collects user input and counts matching values.

A broadcaster or administrator can present viewers with open-ended questions, such as "Who is your favorite player?" or "Where do you live?". The ranking service collects user responses and sorts matching responses by frequency.

The service counts the number of users who send matching response strings for a given key. It does not evaluate or manipulate responses in any way.  You can query the key to determine the most popular responses.

* Use a [POST](https://docs.muxy.io/reference/rank-1) call to submit viewer responses to a question that you present.

* Use a [GET](https://docs.muxy.io/reference/rank-2) call to retrieve ranked responses to a given question.

* You can use a [DELETE](https://docs.muxy.io/reference/rank-3) call to remove a ranking buffer and its data at any time. If it is not deleted, ranking data expires automatically 1 day after the last entry is added. At that point, all data for the ranking ID is removed. If you then send data using the same ranking ID value, the server starts a new accumulation.

# Setting Rankable Questions

A developer-defined ranking ID string identifies an accumulation buffer. The developer is responsible for associating a ranking ID with a question, and presenting the question to viewers. All responses that are submitted with the same ID are aggregated and ranked.

# Submitting Answers

When a user responds to a question, send their response to the ranking service with a POST request to the `rank` endpoint, using the developer-defined rankable-question ID. If the named buffer does not yet exist, it is created with the current data. If it already exists, the current data is appended to any existing data in the buffer.

**Request**

[block:code]
{
  "codes": [
    {
      "code": "POST /v1/e/rank?id=${id}",
      "language": "shell",
      "name": "Submit a value to a ranking buffer"
    }
  ]
}
[/block]

[block:parameters]
{
  "data": {
    "h-0": "Parameter",
    "h-1": "Description",
    "0-0": "*id*",
    "0-1": "String. The name of the accumulation buffer to create or append data to."
  },
  "cols": 2,
  "rows": 1
}
[/block]

The body of the POST request contains a user's response to the question, as a JSON object. The string the user entered is the value of the `key` field.

[block:code]
{
  "codes": [
    {
      "code": "{\n  key: \"DOTA\"\n}",
      "language": "json",
      "name": "Rankable data format"
    }
  ]
}
[/block]

The data is stored along with collection data, including the user information of the poster and the time the post was received.

**Response**

Ranking data is unique per user; that is, the service retains only one value for a given user for a given ranking ID. If a user sends additional responses to the same question, only the latest value is counted. In this case, the response to the successful POST request returns the user's previous answer.

[block:code]
{
  "codes": [
    {
      "code": "{\n  \"accepted\": true,         // Whether the entry has been added to the rankings\n  \"original\": \"Serious Sam\" // Optional. The previous value submitted by this viewer, if any. \n}",
      "language": "json",
      "name": "Voting status and history data"
    }
  ]
}
[/block]

# Retrieving Ranking Results

To retrieve results for a given question, send a GET request  to the `rank` endpoint with the ranking ID.  The GET call must be authorized by a JWT with `broadcaster`, `admin`, or `backend` role.
The call reports all response strings that have been received, and the number of users who have submitted each response, in order of popularity.

**Request**

[block:code]
{
  "codes": [
    {
      "code": "GET /v1/e/rank?id=${id}",
      "language": "shell",
      "name": "Retrieve ranking results"
    }
  ]
}
[/block]

[block:parameters]
{
  "data": {
    "h-0": "Parameter",
    "h-1": "Description",
    "0-0": "*id*",
    "0-1": "String. The name of the ranking accumulation buffer to query."
  },
  "cols": 2,
  "rows": 1
}
[/block]

**Response**

If the call succeeds, the body of the response contains a JSON-encoded array. Each response value becomes a `key` value in this array, up to the top 100 responses. Any response value that matches another value increments a `score` for that value. The response array is sorted by score to show how many people submitted the given response.

[block:code]
{
  "codes": [
    {
      "code": "{\n  \"data\": [\n    {\n      \"key\": \"DOTA\",\n      \"score\": 12\n    },\n    {\n      \"key\": \"FIFA 2014\",\n      \"score\": 8\n    }\n  ]\n}",
      "language": "json",
      "name": "Ranking result data"
    }
  ]
}
[/block]

If the call fails, the body of the response contains error information.
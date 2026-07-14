# Basic Accumulation

Basic accumulation allows you to collect large amounts of user input
into a list for consumption by a backend.

Any user can store data using a POST call to the `accumulate` endpoint, but only users with `broadcaster`, `admin`, or `backend` role can retrieve the data using a GET call.

Each POST call appends a timestamp to the stored data blob, and a GET call can retrieve data collected since a given timestamp.

[block:callout]
{
  "type": "info",
  "title": "Accumulation retrieval scope",
  "body": "If the call is authorized by a JWT with the `broadcaster` role, the response contains data for that broadcaster's channel; that is, the `channel_id` value is the caller's Twitch ID.\n\nIf the call is authorized by an extension-level JWT with the `backend` or `admin` role, the response contains all data points for the entire extension across all channels."
}
[/block]

# Collecting Data

Use a [POST](https://docs.muxy.io/reference/accumulate-1) call to add any JSON-encoded data that you collect into a named *accumulation buffer*.

[block:code]
{
  "codes": [
    {
      "code": "POST /v1/e/accumulate?id=${id}",
      "language": "shell"
    }
  ]
}
[/block]

If the named buffer does not yet exist, it is created with the current data. If it already exists, the current data is appended to any existing data in the buffer.

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

**Request**
The body of the POST request contains any developer-defined data you wish to store, in JSON-encoded format. The marshalled JSON size must be under 256 bytes.

[block:code]
{
  "codes": [
    {
      "code": "{\n  arbitrary-json-blob\n}",
      "language": "json"
    }
  ]
}
[/block]

The data blob is stored along with collection data, including the user information of the poster and the time the post was received.

**Response**

The POST call returns an empty JSON object.

# Accessing the Accumulation Buffer

Use a [GET](https://docs.muxy.io/reference/accumulate-2) call to retrieve data from a named buffer. Requires an authorized user with `broadcaster` or `admin` role.

[block:code]
{
  "codes": [
    {
      "code": "GET /v1/e/accumulate?id=${accumulation_name}&start=${start}&",
      "language": "shell"
    }
  ]
}
[/block]

[block:parameters]
{
  "data": {
    "h-0": "Parameter",
    "0-0": "*accumulation_name* ",
    "1-0": "*start* ",
    "0-1": "String. The buffer from which to retrieve data.",
    "1-1": "Unix millisecond timestamp of the earliest collection time to retrieve."
  },
  "cols": 2,
  "rows": 2
}
[/block]

**Response**

The body of the response contains a list of all accumulation values sent to the buffer since the given start time. The JSON-encoded value as an array of stored data blobs, along with their collection information. Each user is identified by either their Twitch ID or Opaque Twitch ID; see [User IDs](https://docs.muxy.io/reference/dev-auth#user-ids).

[block:code]
{
  "codes": [
    {
      "code": "{\n    \"data\": [{\n        \"observed\": number,\n        \"channel_id\": string,\n        \"opaque_id\": string,\n        \"user_id\": string,\n        \"data\": object\n    }],\n    \"latest\": number\n}",
      "language": "json",
      "name": "Accumulation retrieval response"
    }
  ]
}
[/block]

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Description",
    "0-0": "`latest`",
    "0-1": "Millisecond Unix Timestamp. The time of the latest addition to this buffer.",
    "1-0": "`data`",
    "1-1": "Array containing a JSON element for each returned data blob. The data values are ordered from most recent to least recent.",
    "2-0": "`data.observed`",
    "2-1": "Millisecond Unix Timestamp. The time when this element was inserted into the accumulation buffer.",
    "3-0": "`data.channel_id`",
    "4-0": "`data.opaque_id`",
    "3-1": "Twitch Channel ID where this accumulation value was inserted.",
    "5-0": "`data.user_id`",
    "6-0": "`data.data`",
    "4-1": "Twitch Opaque ID of the user who inserted this value, or an empty string if the `user_id` is available.",
    "5-1": "Twitch User ID of the user who inserted this value, if it exists.",
    "6-1": "The data object inserted."
  },
  "cols": 2,
  "rows": 7
}
[/block]

[block:callout]
{
  "type": "success",
  "body": "The larger the request size, the slower this endpoint becomes. Try to keep the timespan queried by this endpoint less than five to ten minutes.",
  "title": "Performance Tip"
}
[/block]
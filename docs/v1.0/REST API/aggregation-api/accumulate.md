---
title: "Basic Accumulation"
slug: "accumulate"
excerpt: "Basic accumulation allows you to collect large amounts of user input\ninto a list for consumption by a backend."
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Mon Sep 27 2021 18:48:13 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Jan 11 2022 17:15:21 GMT+0000 (Coordinated Universal Time)"
---
Any user can store data using a POST call to the `accumulate` endpoint, but only users with `broadcaster`, `admin`, or `backend` role can retrieve the data using a GET call. 

Each POST call appends a timestamp to the stored data blob, and a GET call can retrieve data collected since a given timestamp.

> 📘 Accumulation retrieval scope
> 
> If the call is authorized by a JWT with the `broadcaster` role, the response contains data for that broadcaster's channel; that is, the `channel_id` value is the caller's Twitch ID.
> 
> If the call is authorized by an extension-level JWT with the `backend` or `admin` role, the response contains all data points for the entire extension across all channels.

# Collecting Data

Use a [POST](../../../v1.0/REST API/aggregation-api/accumulate-1.md) call to add any JSON-encoded data that you collect into a named _accumulation buffer_. 

```shell
POST /v1/e/accumulate?id=${id}
```

 If the named buffer does not yet exist, it is created with the current data. If it already exists, the current data is appended to any existing data in the buffer. 

| Parameter | Description                                                              |
| :-------- | :----------------------------------------------------------------------- |
| _id_      | String. The name of the accumulation buffer to create or append data to. |

**Request**  
The body of the POST request contains any developer-defined data you wish to store, in JSON-encoded format. The marshalled JSON size must be under 256 bytes.

```json
{
  arbitrary-json-blob
}
```

The data blob is stored along with collection data, including the user information of the poster and the time the post was received. 

**Response**

The POST call returns an empty JSON object.

# Accessing the Accumulation Buffer

Use a [GET](../../../v1.0/REST API/aggregation-api/accumulate-2.md) call to retrieve data from a named buffer. Requires an authorized user with `broadcaster` or `admin` role. 

```shell
GET /v1/e/accumulate?id=${accumulation_name}&start=${start}&
```

| Parameter            |                                                                         |
| :------------------- | :---------------------------------------------------------------------- |
| _accumulation_name_  | String. The buffer from which to retrieve data.                         |
| _start_              | Unix millisecond timestamp of the earliest collection time to retrieve. |

**Response**

The body of the response contains a list of all accumulation values sent to the buffer since the given start time. The JSON-encoded value as an array of stored data blobs, along with their collection information. Each user is identified by either their Twitch ID or Opaque Twitch ID; see [User IDs](../../../v1.0/REST API/dev-auth.md#user-ids).

```json Accumulation retrieval response
{
    "data": [{
        "observed": number,
        "channel_id": string,
        "opaque_id": string,
        "user_id": string,
        "data": object
    }],
    "latest": number
}
```

| Field             | Description                                                                                                                |
| :---------------- | :------------------------------------------------------------------------------------------------------------------------- |
| `latest`          | Millisecond Unix Timestamp. The time of the latest addition to this buffer.                                                |
| `data`            | Array containing a JSON element for each returned data blob. The data values are ordered from most recent to least recent. |
| `data.observed`   | Millisecond Unix Timestamp. The time when this element was inserted into the accumulation buffer.                          |
| `data.channel_id` | Twitch Channel ID where this accumulation value was inserted.                                                              |
| `data.opaque_id`  | Twitch Opaque ID of the user who inserted this value, or an empty string if the `user_id` is available.                    |
| `data.user_id`    | Twitch User ID of the user who inserted this value, if it exists.                                                          |
| `data.data`       | The data object inserted.                                                                                                  |

> 👍 Performance Tip
> 
> The larger the request size, the slower this endpoint becomes. Try to keep the timespan queried by this endpoint less than five to ten minutes.

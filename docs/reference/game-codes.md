---
title: Game Codes
description: Archived Muxy documentation for Game Codes.
slug: game-codes
product: REST API
audience: developers
status: archived
owner: API Platform
source_of_truth: muxy/github-pages:openapi/rest-v1.yaml
version: v1
last_verified: '2026-07-14'
review_state: needs-sme-review
robots: noindex, nofollow
search:
  exclude: true
page_type: protocol-reference
---

> ❗️ Under Construction
>
> - need authorization info
> - need info on defining prizes, relationship of codes to prizes
> - how are codes distributed to users?
> - is a code removed from the list when it is distributed? Or can you give the same code to many users?
>   What does "distributed linearly" mean?

Use the `codes` endpoints in server-to-server communication to create and manage named sets of game codes, which  viewers can redeem for prizes.

Using the built-in [Poll Management](../reference/poll-managment.md) system you can automatically download reward codes to viewers who guess the correct answer. Another option is to collect and store Twitch user IDs for certain actions of viewing time, like the Twitch VHS system, and make those viewers eligible for reward codes.



| Endpoint | Description | Commands |
| --- | --- | --- |
| `codes` | Define and manage game codes. | Use `PUT` to define and name code sets  <br>Use `GET` to query for active codes sets  <br>Use `DELETE` to remove code sets and report distribution |
| `codes/mark_from_poll` | Mark all users who have voted correctly in a given poll as eligible for a given prize. | Use `POST` to specify eligibility details |
| `codes/mark_from_list` | Mark all users in a list as eligible for a given prize. | Use `POST` to specify eligibility details |
| `codes/eligibility` | Viewers can query whether the they are _eligible_ to receive a game code. | Use `GET` to query eligibility |
| `codes/redeem` | A user can redeem a code they have received for a specific prize. | Use `POST` to redeem a code for a prize |




# Game Codes

!!! warning "Archived documentation"
    This page is retained for URL compatibility. It is not maintained, indexed, or included in agent exports.


Game codes are available to your extension across channels. Use the `codes` endpoint to define and name game-code sets, modify the names of active code sets, and query for the current names.

The developer is responsible for mapping codes to actual prizes.

The list of code sets expires automatically after 90 days, but you can delete the codes at any time. When you delete the codes, the call reports the total number of codes that have been distributed from each set.

## Defining codes sets

**Request**

Use a PUT request to the `codes` endpoint to define and name sets of game codes.

```shell title="Uploading codes"
PUT https://api.muxy.io/v1/e/codes
```

The body of the request is a JSON blob that contains named sets of codes.

```json title="Defining codes"
{
  "codes": [
    ["3c21-256d-6c", "306e-223a-25", "445e-7676-75"],
    ["555f-4e21-55", "476e-7e76-31", "2d31-5850-7a"]
  ],
  "names": ["Pistol skin", "Fancy Hat"],
  "indices": [0, 1]
}
```



| Field | Value |
| --- | --- |
| `codes ` | Required. A two-dimensional array of codes.  <br> _ You can have up to 10 active rewards (uniquely named code sets) at any given time.  <br> _ Each code must be fewer than 64 characters.  <br> \* Each array must be under 1 million entries. |
| `names` | Required. A parallel array of unique names for each a `codes` array.  <br>\* You can rename code sets with a new PUT request. |
| `indices` | Optional.  A parallel array of specific indices for each named code set. All indices must be in the range [0, 9].  <br>  <br>Default is a 0-based index matching the order of the `codes` and `names` arrays. |




## Querying Active Code Sets

Use a GET request to discover the current names of active code sets.

**Request**

```shell title="Query active code sets"
GET /v1/e/codes
```

**Response**

The call returns the array of current code-set names in a JSON object.

```json title="Names of active code sets"
{
  "names": ["Pistol Skin", "Fancy Hat"]
}
```

## Removing Code Sets

Deleting a set of codes deactivates the code list, and returns the number of codes distributed.

**Request**

Use a DELETE call to deactivate all currently defined codes.

```shell title="Deactivate code sets"
DELETE /v1/e/codes
```

**Response**

If the call succeeds, the body of the response contains a JSON object with the number of codes that have been distributed from each deactivated `codes` set.

```json title="Number of codes distributed from each set"
{
  "distributed": [15612, 42]
}
```

## Marking Code Eligibility

Use these endpoints to specify who can redeem which codes.

## Marking from Poll

This endpoint marks all the users who have voted correctly in the given poll as eligible for a given prize.

**Request**

Use a POST request to specify eligibility details.

```shell title="Make poll winners eligible"
POST /v1/e/codes/mark_from_poll
```

The body of the request is a JSON object that specifies eligibility parameters.

```javascript title="Eligibility parameters"
{
  "prize_limits" : [1, 1], // max number of prizes the user can have
  "prizes": [3, 4], // prizes to award
  "correct": 3, // the poll index that was correct
  "cutoff_timestamp": 1538621638 // what time the users should have voted by
}
```

| Field              | Value                                                                                                                 |
| :----------------- | :-------------------------------------------------------------------------------------------------------------------- |
| `prize_limits`     | An array where each entry is maximum number of prizes a winner can receive from the code set at the same array index. |
| `prizes`           | _How do you define prizes? how do you match codes to prizes?_                                                         |
| `correct`          | _is this the number of the correct option? where is the poll ID?_                                                     |
| `cutoff_timestamp` | The cut-off time for correct votes. Votes received after this time are not marked as eligible.                        |

## Marking from list

Use this endpoint to provide a list of users to be made eligible for a given prize.

**Request**

Use a POST request to specify eligibility details.

```shell title="Make a list of users eligible"
POST /v1/e/codes/mark_from_list
```

The body of the request is a JSON object that specifies eligibility parameters.

```jsonc
{
  "prize_limits": [1, 1], // max number of prizes the user can have
  "prizes": [3, 4], // prizes to award
  "users": ["123456", "65432"] // A list of user IDs
}
```

| Field          | Value                                                                                                                 |
| :------------- | :-------------------------------------------------------------------------------------------------------------------- |
| `prize_limits` | An array where each entry is maximum number of prizes a winner can receive from the code set at the same array index. |
| `prizes`       | _How do you define prizes? how do you match codes to prizes?_                                                         |
| `users`        | An array of Twitch user IDs for users to be marked as eligible.                                                       |

## Querying eligibility

Any user can query whether they are eligible to receive game codes.

**Request**

Use a GET request to find out if the current user is eligible for any prizes.

```shell title="Query user eligibility"
GET /v1/e/codes/eligibility
```

## Redeeming Codes

A user who has received a game code can redeem it for a specific prize.

**Request**

Use a POST request to redeem a code for a specific prize.

```shell title="Redeem game codes"
POST  /v1/e/codes/redeem
```

_do you submit a game code?_

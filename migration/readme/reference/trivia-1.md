---
title: Trivia Contest Management
slug: trivia-1
excerpt: For a more advanced voting and reward system, Muxy provides a trivia contest
  service.
hidden: true
metadata:
  image: []
  robots: index
createdAt: Mon Sep 27 2021 18:48:43 GMT+0000 (Coordinated Universal Time)
updatedAt: Wed Dec 15 2021 17:23:22 GMT+0000 (Coordinated Universal Time)
---

> ❗️ Under construction

A trivia contest is made up of a series of multiple-choice questions. The extension administrator sets the questions and answer options, designates correct answers, and decides when to declare a winner. A contest is identified by at unique `quiz_id`, and only one contest can be active at a time. 

Viewers submit their choice for the winning option for a question, and can be given points for correct choices. A typical application asks viewers to make a prediction about which player of a game will win. Each user is allowed only one choice, but can change that choice. Each choice submitted replaces any previous choice for that user. 

The service updates an extension-wide leaderboard. You can present multiple questions in sequence. The leaderboard displays a sum of correct answers from each viewer.

# Creating and Managing a Trivia Contest

The extension administrator (a user with the `broadcaster` or `admin` role) sets up the questions and answers, identifies the correct answer, and is responsible for any updates. Questions have an optional numerical order field for organizing question display and a state field that an administrator can set to show or hide a question and to enable or disable voting.

Use POST requests to the `trivia` endpoint to set up and manage a trivia contest. 

## Creating questions and options

## Updating questions and options

## Setting question status

# Choosing an Option

Any user can choose an option for a given question as long as voting for that question is open.  
Votes are unique per user; that is, a given question retains only one vote value for a given user. If a user sends additional votes giving the same question ID, that user's vote changes to the latest value.

**Request**  
Make a POST request to send a user's vote to the server.

```shell Vote for an option
POST /v1/e/trivia?id=${quiz_id}
```

The body of the request contains the question ID and the integer value of the option the viewer is voting for, in JSON format. 

```json Voting data
{
  
)
```

**Response**

If the call succeeds, the body of the response contains an empty JSON object. If it fails, the body of the response contains error information.

# Examining Results

Any user can request the list of current questions at any time. The response varies according to the caller's access rights and the question status. 

- Viewers do not see trivia questions that are listed as `inactive`, but admins do. 

**Request**

Use a GET request to the `trivia` endpoint to get the current event status.

```shell Get event status
GET /v1/e/trivia?id=${quiz_id}
```

**Response**

If the call succeeds, the body of the response contains a JSON-encoded array with an entry for each question ID.  The `results` field of each question contain the latest vote chosen by the calling user, and winner information if a winner has been chosen by the administrator.

```json Example response body
{[
  
])
```

 If the call fails, the body of the response contains error information.

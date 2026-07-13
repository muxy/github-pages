---
title: "Ranking User Data"
slug: "ranking"
excerpt: ""
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Wed Sep 15 2021 16:45:10 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Wed Oct 06 2021 21:37:05 GMT+0000 (Coordinated Universal Time)"
---
Muxy provides a ranking service that collects user input and counts matching values. The input is expected to be a response to an open-ended question, such as "What is your favorite color?" or "Where do you live?". The service counts the number of users who send matching response strings -- it does not evaluate or manipulate responses in any way.

When you ask such a question, send responses to the ranking service using a developer-defined key. The service collects and counts responses for that key. You can then query the key to determine the most popular responses.

Ranking responses are timestamped.  Ranking data expires automatically 1 day after the last entry is added. At that point, all data for the ranking key are removed. If you then send data using the same `ranking_key` value, the server starts a new accumulation. 

Like voting data, ranking data is unique per user; that is, the service retains only one value for a given user for a given ranking key. If a user sends additional responses to the same question, only the latest value is counted.

> 👍 Ensuring unique responses
> 
> The result includes the viewer's real ID if it is known at the time the response is sent, but falls back to using their opaque ID. If your extension depends on absolutely correct ranking behavior, you should only allow viewers who have shared their ID to respond. Otherwise, it is possible for viewers to respond multiple times by repeatedly sharing and unsharing their ID, which gives them new opaque ID each time.

# Sending Ranks

Use the `SDK.rank()` method to send viewer responses to a ranking question.

`rank(ranking_key, value);`

- _ranking_key_ is a developer-defined string that identifies the question being answered. By convention, this is a lower-case, hyphen-separated alphanumeric string.  All responses sent to this key are counted toward the result. 

> 👍 Extension-wide ranking
> 
> Prefix the ranking key string with "global" to create an extension-wide ranking key. This is useful if multiple broadcasters are co-streaming an event with an extension, so that every viewer's response counts for the entire event.

- _value_ is the string value entered by the viewer in response the question.

The following example sends a ranking response for a user who has been asked to enter their favorite color:

```javascript
const usersFavoriteColor = 'rebeccapurple';

const opts = new Muxy.DebuggingOptions();
opts.role('viewer');
Muxy.debug(opts);

const medkit= new Muxy.SDK();
// ...the ranking key is "favorite-color"...
medkit.rank('favorite_color', usersFavoriteColor).then(resp => {
  if (!resp.accepted) {
    console.error('Could not send this color');
  }
});
```

The response is a JSON object:

```json
{
  "accepted": true
}
```

# Getting Ranking Data

A broadcaster can use 'SDK.getRankingData`to request the current user rankings for a given ranking key.
The following example returns a set of user responses to the`favorite-color\` ranking question.

```javascript
const opts = new Muxy.DebuggingOptions();
opts.role('broadcaster');
Muxy.debug(opts);

const medkit = new Muxy.SDK();
medkit.getRankingData('favorite-color').then(colors => {
  if (colors.data.length > 0) {
    colors.data.forEach(color => {
      console.log(`${color.key}: ${color.score}`);
    });
  }
});
```

The response is a JSON object that contains an array of key-value pairs:

```json
{
  "data": [
    { "key": "rebeccapurple", "score": 5 },
    { "key": "arcticblue", "score": 2 },
    { "key": "olivedrab", "score": 1 }
  ]
}
```

Each response value becomes a key value in this array, up to the top 100 responses. Any response value that matches another value increments a _score_ for that value. The response array is than sorted by score to show how many people submitted the given response.

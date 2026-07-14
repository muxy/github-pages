# Ranking User Data

Muxy provides a ranking service that collects user input and counts matching values. The input is expected to be a response to an open-ended question, such as "What is your favorite color?" or "Where do you live?". The service counts the number of users who send matching response strings -- it does not evaluate or manipulate responses in any way.

When you ask such a question, send responses to the ranking service using a developer-defined key. The service collects and counts responses for that key. You can then query the key to determine the most popular responses.

Ranking responses are timestamped.  Ranking data expires automatically 1 day after the last entry is added. At that point, all data for the ranking key are removed. If you then send data using the same `ranking_key` value, the server starts a new accumulation.

Like voting data, ranking data is unique per user; that is, the service retains only one value for a given user for a given ranking key. If a user sends additional responses to the same question, only the latest value is counted.

[block:callout]
{
  "type": "success",
  "body": "The result includes the viewer's real ID if it is known at the time the response is sent, but falls back to using their opaque ID. If your extension depends on absolutely correct ranking behavior, you should only allow viewers who have shared their ID to respond. Otherwise, it is possible for viewers to respond multiple times by repeatedly sharing and unsharing their ID, which gives them new opaque ID each time.",
  "title": "Ensuring unique responses"
}
[/block]

# Sending Ranks

Use the `SDK.rank()` method to send viewer responses to a ranking question.

`rank(ranking_key, value);`

* *ranking\_key* is a developer-defined string that identifies the question being answered. By convention, this is a lower-case, hyphen-separated alphanumeric string.  All responses sent to this key are counted toward the result.

[block:callout]
{
  "type": "success",
  "title": "Extension-wide ranking",
  "body": "Prefix the ranking key string with \"global\" to create an extension-wide ranking key. This is useful if multiple broadcasters are co-streaming an event with an extension, so that every viewer's response counts for the entire event."
}
[/block]

* *value* is the string value entered by the viewer in response the question.

The following example sends a ranking response for a user who has been asked to enter their favorite color:

[block:code]
{
  "codes": [
    {
      "code": "const usersFavoriteColor = 'rebeccapurple';\n\nconst opts = new Muxy.DebuggingOptions();\nopts.role('viewer');\nMuxy.debug(opts);\n\nconst medkit= new Muxy.SDK();\n// ...the ranking key is \"favorite-color\"...\nmedkit.rank('favorite_color', usersFavoriteColor).then(resp => {\n  if (!resp.accepted) {\n    console.error('Could not send this color');\n  }\n});",
      "language": "javascript"
    }
  ]
}
[/block]

The response is a JSON object:

[block:code]
{
  "codes": [
    {
      "code": "{\n  \"accepted\": true\n}",
      "language": "json"
    }
  ]
}
[/block]

# Getting Ranking Data

A broadcaster can use 'SDK.getRankingData`to request the current user rankings for a given ranking key.
The following example returns a set of user responses to the`favorite-color\` ranking question.

[block:code]
{
  "codes": [
    {
      "code": "const opts = new Muxy.DebuggingOptions();\nopts.role('broadcaster');\nMuxy.debug(opts);\n\nconst medkit = new Muxy.SDK();\nmedkit.getRankingData('favorite-color').then(colors => {\n  if (colors.data.length > 0) {\n    colors.data.forEach(color => {\n      console.log(`${color.key}: ${color.score}`);\n    });\n  }\n});",
      "language": "javascript"
    }
  ]
}
[/block]

The response is a JSON object that contains an array of key-value pairs:

[block:code]
{
  "codes": [
    {
      "code": "{\n  \"data\": [\n    { \"key\": \"rebeccapurple\", \"score\": 5 },\n    { \"key\": \"arcticblue\", \"score\": 2 },\n    { \"key\": \"olivedrab\", \"score\": 1 }\n  ]\n}",
      "language": "json"
    }
  ]
}
[/block]

Each response value becomes a key value in this array, up to the top 100 responses. Any response value that matches another value increments a *score* for that value. The response array is than sorted by score to show how many people submitted the given response.
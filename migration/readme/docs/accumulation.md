# Accumulating User Data

Accumulation is the simplest form of aggregation.  Using this method, the server simply timestamps and concatenates all JSON blobs sent to a data store with a given name. It does not combine or process the data in any way, or provide automatic broadcasting.

* Your game or extension collects data viewers and sends it to a named data store in the form of a valid JSON object, using a schema that you define.

* The broadcaster live app is responsible for retrieving the data using an accessor method. It can then transform the data and send the information out to viewers as needed. Viewers cannot request the data themselves,

Each entry is accompanied by a timestamp for when it was sent, and you can retrieve data entries received after a given time.  Accumulation data expires automatically 1 day after the last entry is added. After that point, all
accumulation values are removed. If you then send data using the same `name` value, the server starts a new accumulation.

# Sending Data

Use MEDKit's `accumulate()` method to send data from a viewer to a named accumulation store.

`medkit.accumulate(name, blob);`

* *name* is the identifier for this data store.
* *blob* is a data to add to the store. A data blob must be a valid JSON object. You can include any data, such as timestamp or user id info.

The following example sends a data blob from a viewer (simulated in the development environment), using the `accumulate()` method. The name of the data store is 'awesomeness\_level'. The data includes a key of the same name, whose value is a set of three key-value pairs.

[block:code]
{
  "codes": [
    {
      "code": "const opts = new Muxy.DebuggingOptions();\nopts.role('viewer');\nMuxy.debug(opts);\n\nconst medkit= new Muxy.SDK();\nmedkit.accumulate('awesomeness_level', {\n  awesomeness_level: {\n    great: 10,\n    good: 2.5,\n    poor: 'dank'\n  }\n});",
      "language": "javascript"
    }
  ]
}
[/block]

# Accessing Data

The broadcaster can request the accumulated data at any point, using the `getAccumulation()` method.

`getAccumulation(name, max_age)`

* *name* identifies the data store.
* *max\_age* is a timestamp identifies the oldest entry to retrieve.

The following example retrieves all entries from the `awesomeness_level` store that were sent in the minute previous to the call.

[block:code]
{
  "codes": [
    {
      "code": "const oneMinuteAgo = new Date().getTime() - 1000 * 60; // Timestamp in seconds of the oldest entry.\n\nconst opts = new Muxy.DebuggingOptions();\nopts.role('broadcaster');\nMuxy.debug(opts);\n\nconst medkit= new Muxy.SDK();\nmedkit.getAccumulation('awesomeness_level', oneMinuteAgo).then(resp => {\n  console.log(resp.latest); // An epoch timestamp of the most recent accumulate entry.\n  console.log(resp.data); // A list of all accumulate values since oneMinuteAgo.\n});",
      "language": "javascript"
    }
  ]
}
[/block]

**Response**

The call returns a JSON object that includes the single entry that the viewer just sent. If additional entries were sent by other viewers, the "data" blob would included additional JSON objects.

[block:code]
{
  "codes": [
    {
      "code": "{\n  \"data\":[\n    {\n      \"observed\": 1503939418480,    // The timestamp of when this accumulate entry was sent.\n      \"channel_id\": \"23161357\",     // The id of the channel the entry was sent from.\n      \"opaque_user_id\": \"A1954218\", // The opaque id of the viewer that sent the event.\n      \"user_id\": \"\",                // The user id of the viewer (if shared).\n      \"data\": {                     // The JSON object that was sent in the request.\n        \"awesomeness_level\": {\n          \"good\": 2.5,\n          \"great\": 10,\n          \"poor\": \"dank\"\n        }\n      }\n    }\n  ],\n  \"latest\": 1503939418480             // The timestamp of the last entry from the server.\n}",
      "language": "json"
    }
  ]
}
[/block]
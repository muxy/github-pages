# Store Arbitrary JSON Data

Define and store your own data values for users to retrieve.

In addition to storing the extension and viewer state, a developer can define and store any arbitrary JSON data that any user can retrieve at any time.  This data goes into a JSON store, and is available on a per-channel basis.

[block:callout]
{
  "type": "warning",
  "body": "The JSON store allows for more flexibility than the standard state stores, but it does come with some limitations.\n* Data stored using this method is automatically removed 14 days after it is inserted.\n* Data stored in JSON store is charged at a higher rate when accessed by viewers using an extension.",
  "title": "Arbitrary Storage vs. State Storage"
}
[/block]

# JSON Stores

A JSON store is like Channel state, in that a broadcaster can use it to store arbitrary JSON data that is accessible to all viewers. The stored data is specific to a particular channel and cannot be accessed by viewers of a different channel.

Unlike Channel state however, each channel can have several JSON stores, accessed by different keys. The data associated with each key must be under 2KB, but there is no limit to the number of keys in use.

When you push new data to the JSON store, a messenger event is automatically sent to all active viewers of the associated channel, and to the broadcaster's live and config pages. This event has the following format:

`json_store_update:${key}`

## Code examples

Create a JSON store by setting a variable to a JSON value:

[block:code]
{
  "codes": [
    {
      "code": "set \"basecamp\" to { tanks: [\"tank1\", \"tank2\"] }",
      "language": "javascript"
    }
  ]
}
[/block]

This creates a JSON store named "basecamp", which contains a key `tanks`. Access by passing the name to the MEDKit function \`getJSONStore(), as in the following example.

[block:code]
{
  "codes": [
    {
      "code": "const medkit = new Muxy.SDK();\nmedkit.getJSONStore('basecamp').then(basecamp => {\n  // check that the key you want exists\n  if (basecamp && basecamp.tanks) {\n    deploy(basecamp.tanks);\n  }\n});",
      "language": "javascript"
    }
  ]
}
[/block]

The following example listens for automatic updates to the "basecamp" JSON store:

[block:code]
{
  "codes": [
    {
      "code": "medkit.listen('json_store_update:basecamp').then(data => {\n  // data.id will equal 'basecamp'\n  console.log(data.value);\n});",
      "language": "javascript"
    }
  ]
}
[/block]
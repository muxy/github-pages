---
title: "Store Arbitrary JSON Data"
slug: "arbitrary-state"
excerpt: "Define and store your own data values for users to retrieve."
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Wed Sep 15 2021 16:41:32 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Wed Nov 03 2021 16:10:15 GMT+0000 (Coordinated Universal Time)"
---
In addition to storing the extension and viewer state, a developer can define and store any arbitrary JSON data that any user can retrieve at any time.  This data goes into a JSON store, and is available on a per-channel basis.

> 🚧 Arbitrary Storage vs. State Storage
> 
> The JSON store allows for more flexibility than the standard state stores, but it does come with some limitations.
> 
> - Data stored using this method is automatically removed 14 days after it is inserted.
> - Data stored in JSON store is charged at a higher rate when accessed by viewers using an extension.

# JSON Stores

A JSON store is like Channel state, in that a broadcaster can use it to store arbitrary JSON data that is accessible to all viewers. The stored data is specific to a particular channel and cannot be accessed by viewers of a different channel.

Unlike Channel state however, each channel can have several JSON stores, accessed by different keys. The data associated with each key must be under 2KB, but there is no limit to the number of keys in use.

When you push new data to the JSON store, a messenger event is automatically sent to all active viewers of the associated channel, and to the broadcaster's live and config pages. This event has the following format:

`json_store_update:${key}`

## Code examples

Create a JSON store by setting a variable to a JSON value:

```javascript
set "basecamp" to { tanks: ["tank1", "tank2"] }
```

This creates a JSON store named "basecamp", which contains a key `tanks`. Access by passing the name to the MEDKit function \`getJSONStore(), as in the following example.

```javascript
const medkit = new Muxy.SDK();
medkit.getJSONStore('basecamp').then(basecamp => {
  // check that the key you want exists
  if (basecamp && basecamp.tanks) {
    deploy(basecamp.tanks);
  }
});
```

 The following example listens for automatic updates to the "basecamp" JSON store:

```javascript
medkit.listen('json_store_update:basecamp').then(data => {
  // data.id will equal 'basecamp'
  console.log(data.value);
});
```

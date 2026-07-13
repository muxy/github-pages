---
title: "Data Tracking"
slug: "data-tracking"
excerpt: "MEDKit offers three different ways to track any kind of extension and viewer data that you want to use."
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Wed Nov 03 2021 20:19:29 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Wed Nov 03 2021 23:22:21 GMT+0000 (Coordinated Universal Time)"
---
The Muxy server can store and provide access to any data that you need to track.  
Tracked data is stored as JSON blobs containing developer-defined key-value pairs. There are no predefined keys. You are responsible for defining what data you want to track, and performing any validation of values.

There are three kinds of data storage:

- [**State**](../../v1.0/Development Basics/data-tracking/state-information.md)  storage keeps data that you expect to set and retrieve often in real time. Four different stores maintain data with different scopes: per channel, per viewer of a channel, per extension across channels,  and per viewer of an extension running in any channel.

- [**Configuration**](../../v1.0/Development Basics/data-tracking/store-configuration-data.md) storage keeps data the you expect to set infrequently, and access only on extension startup. There are two configuration stores with different scopes:  one per channel, and one for an extension running in any channel.

- [**Arbitrary**](../../v1.0/Development Basics/data-tracking/arbitrary-state.md) storage keeps any kind of JSON-encoded data you want on a per-channel basis. This store is more flexible in usage, but the data expires more quickly and costs more to access.

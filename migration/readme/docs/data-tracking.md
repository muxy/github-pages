# Data Tracking

MEDKit offers three different ways to track any kind of extension and viewer data that you want to use.

The Muxy server can store and provide access to any data that you need to track.
Tracked data is stored as JSON blobs containing developer-defined key-value pairs. There are no predefined keys. You are responsible for defining what data you want to track, and performing any validation of values.

There are three kinds of data storage:

* [**State**](https://docs.muxy.io/docs/state-information)  storage keeps data that you expect to set and retrieve often in real time. Four different stores maintain data with different scopes: per channel, per viewer of a channel, per extension across channels,  and per viewer of an extension running in any channel.

* [**Configuration**](https://docs.muxy.io/docs/store-configuration-data) storage keeps data the you expect to set infrequently, and access only on extension startup. There are two configuration stores with different scopes:  one per channel, and one for an extension running in any channel.

* [**Arbitrary**](https://docs.muxy.io/docs/arbitrary-state) storage keeps any kind of JSON-encoded data you want on a per-channel basis. This store is more flexible in usage, but the data expires more quickly and costs more to access.
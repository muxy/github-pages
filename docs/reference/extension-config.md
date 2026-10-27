---
title: All Config
description: Retrieve the combined channel and extension configuration documents.
slug: extension-config
product: REST API
audience: developers
status: current
owner: API Platform
source_of_truth: muxy/github-pages:openapi/rest-v1.yaml
version: v1
last_verified: '2026-07-14'
review_state: approved
page_type: protocol-reference
approved_by: peter-bonanni
approved_at: '2026-07-14T20:34:54Z'
approval_method: user-authorized-codex-assisted-source-review
approved_content_sha256: 82684ad22e6bea7a37fd41fb0ba2b495d0bcc7591dcdfc6bec806b51bbf26211
---

# All Config

## `GET /config`

All Config

### Authorization

Send `Authorization: <Twitch Extension Client ID> <Muxy JWT>`. The JWT role must satisfy the endpoint requirements shown in the examples.

### Responses

#### 200 Response

200

Content type: `application/json`

##### Schema

```json
{
  "type": "object",
  "properties": {
    "channel": {
      "type": "object",
      "properties": {}
    },
    "extension": {
      "type": "object",
      "properties": {}
    }
  }
}
```

##### Example

```json
{
  "channel": {},
  "extension": {}
}
```

#### 400 Error

400

Content type: `application/json`

##### Schema

```json
{
  "type": "object",
  "properties": {
    "reason": {
      "type": "string"
    }
  }
}
```

##### Example

```json
{
  "reason": "400"
}
```

### Examples

#### Curl

```curl
curl --request GET \
  --url https://api.muxy.io/v1/e/config \
  --header 'authorization: <Client ID> <any JWT>' \
  --header 'content-type: application/json'
```

#### Javascript

```javascript
const medkit = new Muxy.SDK();
await medkit.loaded();

const config = medkit.getConfig();
```

#### Node

```node
type ExtensionConfig = {
  enablePurchases?: Boolean;
};
type ChannelConfig = {
  itemAmount?: Number;
};
type Config = {
  channel: ChannelConfig;
  extension: ExtensionConfig;
};

const medkit = new Muxy.SDK();
await medkit.loaded();

const config = medkit.getConfig<Config>();
console.log(config.channel.itemAmount || 100);
```

!!! info "Generated API reference"
    This endpoint is generated from [`rest-v1.yaml`](https://docs.muxy.io/openapi/rest-v1.yaml).

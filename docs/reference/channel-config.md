---
title: Channel Config
description: Retrieve the current channel configuration document.
slug: channel-config
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
approved_content_sha256: 813567cf8702a6147521bea3cf0aab41279f37d482d5c8d0f94c7db58f672dea
---

# Channel Config

## `GET /config/channel`

Channel Config

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
  "properties": {}
}
```

##### Example

```json
{
  "broadcaster_birthday": "2000-01-01"
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
  --url https://api.muxy.io/v1/e/config/channel \
  --header 'authorization: <Client ID> <any JWT>' \
  --header 'content-type: application/json'
```

#### Javascript

```javascript
const medkit = new Muxy.SDK();
await medkit.loaded();

const config = medkit.getChannelConfig();
```

!!! info "Generated API reference"
    This endpoint is generated from [`rest-v1.yaml`](https://docs.muxy.io/openapi/rest-v1.yaml).

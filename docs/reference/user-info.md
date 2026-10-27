---
title: User Information
description: Archived Muxy documentation for User Information.
slug: user-info
product: REST API
audience: developers
status: archived
owner: API Platform
source_of_truth: muxy/github-pages:openapi/rest-v1.yaml
version: v1
last_verified: '2026-07-14'
review_state: needs-sme-review
robots: noindex, nofollow
search:
  exclude: true
page_type: protocol-reference
---

# User Information

!!! warning "Archived documentation"
    This page is retained for URL compatibility. It is not maintained, indexed, or included in agent exports.


> ❗️ Under construction

The `user_info` endpoint provides read-only access to information about the user making the call.

> 📘 Checking Token Validity
>
> A call for [PIN authorization](refs:pin-auth) returns a JWT. To check the validity of this JWT, use it to poll this endpoint until it returns a 200 response.

**Request**
Send a GET request to the `user_info` endpoint to retrieve information associated with the user making the call.

```shell title="user-info endpoint"
GET /v1/e/user_info
```

**Response**
If the call succeeds, the user's JWT is valid, and the response body contains a JSON-encoded object with the user's account data.

```json title="Response body"
{
  "??": "<??>"
}
```

---
title: User Information
slug: user-info
excerpt: Retrieve information about the calling user,
hidden: true
metadata:
  image: []
  robots: index
createdAt: Tue Oct 26 2021 19:43:00 GMT+0000 (Coordinated Universal Time)
updatedAt: Mon Jan 10 2022 18:38:54 GMT+0000 (Coordinated Universal Time)
---

> ❗️ Under construction

The `user_info` endpoint provides read-only access to information about the user making the call.

> 📘 Checking Token Validity
> 
> A call for [PIN authorization](refs:pin-auth) returns a JWT. To check the validity of this JWT, use it to poll this endpoint until it returns a 200 response.

**Request**  
Send a GET request to the `user_info` endpoint to retrieve information associated with the user making the call.

```shell user-info endpoint
GET /v1/e/user_info
```

**Response**  
If the call succeeds, the user's JWT is valid, and the response body contains a JSON-encoded object with the user's account data.

```json Response body
{
  "??": "<??>"
}
```

---
title: "Initialization API"
slug: "initialization-api"
excerpt: "These endpoints support the initialization process for authorized communication with the Muxy server."
hidden: true
metadata: 
  image: []
  robots: "index"
createdAt: "Tue Oct 26 2021 19:45:36 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Wed Feb 02 2022 16:55:04 GMT+0000 (Coordinated Universal Time)"
---
All calls into the MEDKit REST API are authenticated with a valid Client ID. This is a Twitch Extension Client ID that has been registered with Muxy. See [Quick Start for Developers](../../v1.0/Documentation/quick-start.md) for details.

> ❗️ Under construction
> 
> Implementation is changing

Calls to all resources except 'authtoken' and 'pin' require the **Authorization** header.  The value of the **Authorization** header is a space-separated Client ID/JWT pair of the form 'Authorization: 12345 eyJhbGciOiJIU...'.



| Endpoint | Usage |
| --- | --- |
| [`authtoken`](refs:dev-auth) | Used internally. Available only on `sandbox`.  <br>  <br>An unauthorized [POST](../../v1.0/REST API/dev-auth/try-sandbox-auth.md) call generates and returns a JavaScript Web Token (JWT), valid only in the `sandbox` testing environment. |
| [`pin`](refs:pin-auth) | An unauthorized POST call by a broadcaster returns credentials (a PIN and JWT) to use in subsequent calls to the MedKit REST API. |
| [`user-info`](refs:user-info) |  |



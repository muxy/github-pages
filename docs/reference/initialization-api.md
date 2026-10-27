---
title: Initialization API
description: Archived Muxy documentation for Initialization API.
slug: initialization-api
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

# Initialization API

!!! warning "Archived documentation"
    This page is retained for URL compatibility. It is not maintained, indexed, or included in agent exports.


All calls into the MEDKit REST API are authenticated with a valid Client ID. This is a Twitch Extension Client ID that has been registered with Muxy. See [Quick Start for Developers](../docs/quick-start.md) for details.

> ❗️ Under construction
>
> Implementation is changing

Calls to all resources except 'authtoken' and 'pin' require the **Authorization** header.  The value of the **Authorization** header is a space-separated Client ID/JWT pair of the form 'Authorization: 12345 eyJhbGciOiJIU...'.



| Endpoint | Usage |
| --- | --- |
| [`authtoken`](refs:dev-auth) | Used internally. Available only on `sandbox`.  <br>  <br>An unauthorized [POST](../reference/try-sandbox-auth.md) call generates and returns a JavaScript Web Token (JWT), valid only in the `sandbox` testing environment. |
| [`pin`](refs:pin-auth) | An unauthorized POST call by a broadcaster returns credentials (a PIN and JWT) to use in subsequent calls to the MedKit REST API. |
| [`user-info`](refs:user-info) |  |

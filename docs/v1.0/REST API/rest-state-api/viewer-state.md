---
title: "All State"
slug: "viewer-state"
excerpt: ""
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Tue Sep 14 2021 22:21:42 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Jan 11 2022 22:17:28 GMT+0000 (Coordinated Universal Time)"
---
All users can make this GET request to retrieve all types of developer-defined state data.  
The response body is a JSON object with three keys; `extension`, `channel`, and `viewer`. The value of each key is a JSON object containing the state data defined with the given scope,  
The `viewer` data includes both extension-wide and channel-wide viewer data.

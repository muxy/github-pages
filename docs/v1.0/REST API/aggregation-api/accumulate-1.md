---
title: "Accumulate"
slug: "accumulate-1"
excerpt: ""
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Sat Oct 16 2021 16:22:08 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Jan 11 2022 17:19:30 GMT+0000 (Coordinated Universal Time)"
---
Retrieves a snapshot of accumulated data from an existing accumulation buffer.  

> 📘 Single-channel or extension-wide data accumulation
> 
> If the JWT used to access this endpoint has the `broadcaster` role, the response contains data for that broadcaster's channel; that is, the `channel_id` value is the broadcaster's Twitch ID.
> 
> If the JWT used is  extension-level, with the `admin` or `backend` role, the response contains all data points for the entire extension across all channels.

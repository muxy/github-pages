---
title: "Basic Usage"
slug: "basic-usage-examples"
excerpt: ""
hidden: true
metadata: 
  image: []
  robots: "index"
createdAt: "Wed Sep 15 2021 16:35:48 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Mon Jun 12 2023 20:54:03 GMT+0000 (Coordinated Universal Time)"
---
Here's how you implement some basic operations, which include:

- Using Muxy's extension and viewer state information
- Broadcasting messages to your viewers
- Accepting bit transactions in your game

## Retrieve and Use State Information

To maintain state, use the `Set Channel State` node.



![232](https://files.readme.io/00e7f7a-state.png)




- **Path** is a dot-delimited path string that points to the state object
- **Info** is a JSON object string to be placed at that path.

To clear out existing state use the `Clear Channel State` node.



![202](https://files.readme.io/8fe9b7b-clearstate.png)




## Broadcast Message to Viewers

A common requirement is to have the client extension update instantly in response to creating a poll or other  
game action. The broadcast API pushes a notification to all viewers.



![211](https://files.readme.io/359c7ca-broadcast.png)




- **Topic** is a string is used on the client as a discriminator
- **Data** is JSON object. (Note that the Muxy API does not provide a way to manipulate JSON strings, so you need a third-party plugin to construct the data object.)

## Accept Bit Transactions

Bit transactions are exposed as events on the Event Source.



![662](https://files.readme.io/f561f9d-transaction.png)




- **SKU** is the product that was purchased
- **User ID** is the Twitch user ID of the user who purchased the product. 
- **Display Name** is the display name of the product that was purchased. 
- **Username** is the user-facing display name of the user who purchased the product.

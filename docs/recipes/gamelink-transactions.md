---
title: GameLink Transactions
description: Subscribe to purchases and validate completed transactions with GameLink
  C++.
slug: gamelink-transactions
product: GameLink Native
audience: game developers
status: current
owner: Native SDK owner
source_of_truth: muxy/gamelink-cpp
version: commit-16c6b97
last_verified: '2026-07-14'
review_state: blocked-release
page_type: task-guide
---

# GameLink Transactions

!!! warning "Release verification required"
    This example is pinned to commit `16c6b9796ae02105153ac33482d83ac609398d2e`. Publish and confirm a supported GameLink release before approving this page for production.

Subscribe before authentication so the SDK can restore the subscription after reconnecting.

## Subscribe to purchases

```cpp
sdk.OnTransaction().Add([&](const gamelink::schema::TransactionResponse& response) {
    const auto& purchase = response.data;

    std::cout
        << "Purchase " << purchase.muxyId
        << " for " << purchase.sku
        << " from " << purchase.userName
        << "\n";

    // Grant the item exactly once before validating the transaction.
    GrantEntitlement(purchase.userId, purchase.sku, purchase.muxyId);
    sdk.ValidateTransaction(purchase.muxyId, purchase.userId);
});

sdk.SubscribeToAllPurchases();
sdk.AuthenticateWithPIN(clientID, pin);
```

To listen for one SKU instead, use the SDK's SKU-specific purchase subscription. Persist the Muxy transaction ID with the entitlement so reconnects and retries cannot grant the item twice.

## Pump network traffic

```cpp
sdk.ForeachPayload([&](const gamelink::Payload* payload) {
    websocket.send(payload->Data(), payload->Length());
});

websocket.run();
```

Do not validate a transaction until the game has durably granted or recorded the entitlement. See [purchase transaction protocol](../reference/ws-purchase-transactions.md) for the canonical wire events.

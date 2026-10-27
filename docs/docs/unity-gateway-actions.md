---
title: Create Gateway Game Actions
description: Define viewer actions, handle purchases, and bound their gameplay impact.
slug: unity-gateway-actions
product: Gateway
audience: game developers
status: current
owner: Gateway SDK owner
source_of_truth: muxy/gateway-unity
version: v1.1.0-rc.1
last_verified: '2026-10-26'
review_state: needs-sme-review
page_type: task-guide
---

# Create Gateway Game Actions

Actions let viewers trigger game effects. Give every action a stable ID, an explicit state, a bounded impact score, and a count appropriate to the effect.

## Define actions

```csharp
using MuxyGateway;
private readonly GameAction[] actions =
{
    new GameAction
    {
        ID = "spawn-healthpack",
        Name = "Spawn Healthpack",
        Description = "Spawn a healthpack near the player.",
        Icon = "fa-solid:heart",
        Category = GameActionCategory.Help,
        State = GameActionState.Available,
        Impact = 2,
        Count = GameAction.InfiniteCount,
        OnGameActionUsed = new MuxyGatewayGameActionUsedEvent()
    },
    new GameAction
    {
        ID = "restart-level",
        Name = "Restart Level",
        Description = "Restart the current level.",
        Icon = "fa-solid:skull-crossbones",
        Category = GameActionCategory.Hinder,
        State = GameActionState.Available,
        Impact = 5,
        Count = 1,
        OnGameActionUsed = new MuxyGatewayGameActionUsedEvent()
    }
};
```

## Register one handler

```csharp
private SDK.OnGameActionUsedDelegate actionUsedCallback;
private void RegisterActions()
{
    actionUsedCallback = used =>
    {
        switch (used.ActionID)
        {
            case "spawn-healthpack":
                SpawnHealthpack();
                gateway.Client.AcceptGameAction(used, "Healthpack spawned");
                break;
            case "restart-level":
                RestartLevel();
                gateway.Client.AcceptGameAction(used, "Level restarted");
                break;
            default:
                gateway.Client.RefundGameAction(used, "Unknown action");
                break;
        }
    };

    gateway.Client.OnGameActionUsed(actionUsedCallback);
    gateway.Client.SetGameActions(actions);
}
```

Register callbacks once after authentication. Make handlers idempotent by transaction ID so reconnects cannot apply an effect twice.

Initialize each action's `OnGameActionUsed` UnityEvent in code even when handling actions through the global callback. Inspector-created actions receive it automatically.

## Handle Bits conversions

Register the Bits callback once after authentication:

```csharp
private SDK.OnBitsUsedDelegate bitsUsedCallback;
private void RegisterBits()
{
    bitsUsedCallback = used =>
    {
        Debug.Log($"Received {used.Bits} Bits for SKU {used.SKU}");
        RecordBitsTransactionOnce(used.TransactionID, used.UserID, used.SKU, used.Bits);
    };

    gateway.Client.OnBitsUsed(bitsUsedCallback);
}
```

Treat `TransactionID` as the idempotency key and never grant the same conversion twice.

Next: [Add polls and game text](unity-gateway-polls-game-text.md).

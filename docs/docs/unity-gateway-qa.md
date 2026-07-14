---
title: Gateway Unity QA Checklist
description: Verify authentication, actions, polls, metadata, game text, reconnects,
  and production configuration.
slug: unity-gateway-qa
product: Gateway
audience: game developers and QA
status: current
owner: Gateway SDK owner
source_of_truth: muxy/gateway-unity
version: v1.0.0-rc
last_verified: '2026-07-14'
review_state: blocked-release
page_type: task-guide
---

# Gateway Unity QA Checklist

Run this checklist in a development build before enabling production mode.

## Authentication

- [ ] A valid PIN authenticates once and returns a refresh token.
- [ ] An invalid or expired PIN shows a recoverable error without exposing credentials.
- [ ] A stored refresh token restores the session after restart.
- [ ] Deauthentication removes local credentials and requires a new PIN.

## Viewer features

- [ ] Metadata displays the expected game name, logo, and theme.
- [ ] Each action appears with the correct state, count, category, impact, and icon.
- [ ] Every accepted action applies exactly once; rejected actions are refunded.
- [ ] Poll options display in order, updates arrive, and the final winner maps to a valid option.
- [ ] Game text updates after state changes and is not republished every frame.

## Lifecycle and resilience

- [ ] The SDK persists or is recreated intentionally across scene transitions, never duplicated.
- [ ] Temporary network loss reconnects without duplicate callback registration or action fulfillment.
- [ ] A 60-minute session shows no unbounded queue, handle, or memory growth.
- [ ] Exiting Play mode or the game stops the transport cleanly.
- [ ] Production builds use production mode; local and QA builds use sandbox mode.

Return to the [Gateway tutorial overview](unity-gateway-tutorial.md).

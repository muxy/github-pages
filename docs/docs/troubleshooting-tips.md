---
title: Troubleshoot MEDKit 2.4.18
description: Diagnose MEDKit initialization, authorization, state, voting, and clock
  problems.
slug: troubleshooting-tips
product: MEDKit
audience: developers
status: current
owner: Developer Experience
source_of_truth: muxy/extensions-js
version: 2.4.18
last_verified: '2026-07-14'
review_state: approved
page_type: troubleshooting
approved_by: peter-bonanni
approved_at: '2026-07-14T20:34:54Z'
approval_method: user-authorized-codex-assisted-source-review
approved_content_sha256: 982181d88d010917b2155bf4d3189f81809e6336226681f8abfd2e3c3b755290
---

# Troubleshoot MEDKit 2.4.18

Start with the first failed boundary: initialization, authorization, request scope, or application data. Do not work around a `401` or `403` by exposing an extension secret in browser code.

## Diagnosis

### Initialization does not complete

Confirm that the page follows the required order and calls setup only once:

```javascript
Muxy.debug(debugging); // Local and sandbox builds only.
Muxy.setup({ clientID }); // Exactly once per page.

const medkit = new Muxy.SDK();
await medkit.loaded();
```

Inspect the rejection from `loaded()`, the first failed Network request, and the value of `clientID`. A missing Client ID throws synchronously; a second `Muxy.setup()` call also throws. Request and event methods used before `loaded()` resolves can fail or appear to hang.

### A request returns 401 or 403

MEDKit 2.4.18 uses separate environments:

| Context | API origin |
| --- | --- |
| Local or sandbox testing | `https://sandbox.api.muxy.io` |
| Twitch production | `https://api.muxy.io` |

In the failed request, verify locally that:

- `Authorization` has the shape `<client-id> <jwt>`;
- the Client ID matches `Muxy.setup({ clientID })`;
- the JWT is unexpired and was issued for the target environment;
- `channel_id`, `user_id`, and `role` match the operation; and
- privileged writes run as a supported broadcaster, admin, or trusted backend role.

Do not paste a live token into a third-party decoder or support message.

### State or configuration appears missing

Read all verified scopes before changing write code:

```javascript
const [state, config] = await Promise.all([
  medkit.getAllState(),
  medkit.getConfig(),
]);

console.log({ state, config });
```

`getAllConfig()` is not a MEDKit 2.4.18 method. Compare the channel, viewer, extension, and extension-viewer scope with the scope used by the writer.

### Vote totals contain an earlier round

`vote(id, value)` groups submissions by the identifier supplied by the application. Reusing an ID reuses the existing poll. MEDKit 2.4.18 does not expose a public JavaScript method to delete a vote buffer.

### Time-sensitive UI drifts

Compare the operating-system time with MEDKit's server-adjusted value after initialization:

```javascript
await medkit.loaded();
const now = medkit.getOffsetDate();
console.log(now.toISOString());
```

`getOffsetDate()` returns a `Date`; it does not schedule timers or correct the operating-system clock.

### An example method is missing or behaves differently

Confirm the installed release:

```bash
npm ls @muxy/extensions-js
```

MEDKit 2.4.18 has known source-specific boundaries: use `fetch()` for Twitch user lookups, JSON stores have no public SDK writer, and `signedRequest()` serializes object bodies itself.

## Resolution

### Initialization does not complete

Move debug setup before `Muxy.setup()`, create one SDK instance for the page, and gate MEDKit-dependent UI on `await medkit.loaded()`. Restart the development server after changing environment files.

### A request returns 401 or 403

Use a fresh token from the same environment as the API host. In local tests, set the intended `DebuggingOptions` role before setup; for broadcaster tests, use the channel owner's Twitch ID when the operation requires it. Keep backend-only credentials on a trusted server.

### State or configuration appears missing

Use the getter and setter for the same scope and confirm the current channel and viewer identity. Review [state scopes](state-information.md) and [configuration scopes](store-configuration-data.md) before migrating data between stores.

### Vote totals contain an earlier round

Use a unique identifier for every round:

```javascript
const pollID = `show-${showID}-round-${roundNumber}`;
await medkit.vote(pollID, selectedOption);
```

Only use an administrative REST deletion flow after its authorization and production contract have been reviewed separately.

### Time-sensitive UI drifts

Calculate MEDKit deadlines from `getOffsetDate()` and use one application timer to update the UI. Recalculate after page resume or network recovery instead of assuming a timer remained exact in the background.

### An example method is missing or behaves differently

Match code to the 2.4.18 declarations and pass JavaScript objects—not pre-serialized JSON strings—to `signedRequest()`. See [Call the Twitch API](call-into-the-twitch-api.md#2418-helper-limitation) and [Read arbitrary JSON stores](arbitrary-state.md#write-limitation-in-2418).

## Escalation

Remove authorization headers, credentials, and unnecessary user data before sharing diagnostics. Collect the row for the symptom you reproduced:

| Symptom | Evidence to collect |
| --- | --- |
| Initialization does not complete | Installed SDK version, page URL and Twitch surface, browser version, sanitized console error, failed request URL and status, and local-versus-Twitch context. |
| Request returns `401` or `403` | API host, method and path, status, sanitized response, expected role, Client ID suffix, and JWT expiry time. Never include the complete JWT, PIN, refresh token, or extension secret. |
| State or configuration appears missing | Read and write method names, sanitized payload, expected scope, channel ID, shared-identity state, API host, and timestamps for one reproduction. |
| Vote totals contain an earlier round | Poll ID, round start time, submit/read roles, one sanitized result, and whether an earlier client could still be open. |
| Time-sensitive UI drifts | System time, `getOffsetDate()` value, browser visibility state, timezone, elapsed background duration, and relevant server timestamp. |
| Example method is missing or differs | Exact package version, method signature, minimal call site, sanitized arguments, observed result, and documentation URL. |

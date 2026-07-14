---
title: Accumulating User Data
description: Append viewer JSON events and consume them safely with a durable timestamp
  cursor.
slug: accumulation
product: MEDKit
audience: developers
status: current
owner: Developer Experience
source_of_truth: muxy/extensions-js
version: 2.4.18
last_verified: '2026-07-14'
review_state: approved
page_type: concept
approved_by: peter-bonanni
approved_at: '2026-07-14T20:34:54Z'
approval_method: user-authorized-codex-assisted-source-review
approved_content_sha256: a7fd5169844d5d4fdfd7ee3604e6c66f149ea44a447ff025036964b41a1e7c4f
---

# Accumulating User Data

Use accumulation when every submission matters and your broadcaster or backend will process the raw events later. MEDKit appends each authenticated caller's JSON object to a named buffer; it does not merge values, calculate totals, or broadcast updates.

Choose a different API when you need a current value or a server-calculated result:

| Requirement | Use |
| --- | --- |
| Preserve each timestamped submission | Accumulation |
| Count matching text answers once per user | [Ranking](ranking.md) |
| Maintain one current object | [State](state-information.md) |
| Aggregate numeric poll choices | [Voting](voting.md) |

## Design the buffer

Treat the accumulation ID as part of your data contract. Include the feature and round in the ID, such as `post-match-feedback-2026-07-14`, so a later run cannot accidentally consume older entries.

Keep each payload small and version its schema when consumers may outlive producers:

```javascript
const feedback = {
  schemaVersion: 1,
  rating: 5,
  tags: ["fast", "fun"],
};
```

Do not include secrets or data you do not need. Read responses include channel and viewer identity fields supplied by the service.

## Append viewer data

After MEDKit is ready, call `accumulate(id, data)` from any authenticated role. Pass a JavaScript object; MEDKit 2.4.18 serializes it for the request.

```javascript
import Muxy from "@muxy/extensions-js";

Muxy.setup({ clientID: import.meta.env.VITE_MUXY_CLIENT_ID });
const medkit = new Muxy.SDK();
await medkit.loaded();

await medkit.accumulate("post-match-feedback-2026-07-14", {
  schemaVersion: 1,
  rating: 5,
  tags: ["fast", "fun"],
});
```

A resolved promise means the append request was accepted. It does not mean a consumer has processed the entry.

## Read new entries

`getAccumulateData(id, start)` requires a `broadcaster`, `admin`, or `backend` context. `start` is a Unix timestamp in milliseconds, and the response contains `{ data, latest }`.

```javascript
let cursor = 0;

async function readNextBatch() {
  const response = await medkit.getAccumulateData(
    "post-match-feedback-2026-07-14",
    cursor,
  );

  for (const entry of response.data) {
    console.log({
      receivedAt: new Date(entry.observed),
      channelID: entry.channel_id,
      opaqueUserID: entry.opaque_user_id,
      sharedUserID: entry.user_id || null,
      feedback: entry.data,
    });
  }

  if (response.latest > cursor) {
    cursor = response.latest;
  }
}
```

The REST contract treats `start` as an exclusive lower bound, so feeding `latest` into the next read avoids replaying the final entry. Persist the cursor only after all returned entries have been handled successfully; otherwise retry from the previous cursor and make your consumer idempotent.

## Operational constraints

- A broadcaster reads only its channel's entries; admin and backend roles can read across the extension.
- `opaque_user_id` is always suitable only as the identity supplied for that extension context. `user_id` can be empty when the viewer has not shared a Twitch ID.
- Accumulation is pull-based. Poll at a bounded interval, back off after failures, and stop when the owning page or job shuts down.
- The pinned MEDKit declarations and OpenAPI contract do not specify a retention guarantee or a delete operation. Do not depend on the legacy one-day retention claim for correctness; use round-specific IDs and move durable data to storage you control.
- Query short windows. Large time spans return more raw entries and take longer to transfer and process.

For the HTTP request and role contract, see [Basic Accumulation](../reference/accumulate.md).

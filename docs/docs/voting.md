---
title: Collect Votes with MEDKit
description: Submit numeric votes, read aggregate results, react to updates, and retrieve
  admin logs.
slug: voting
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
approved_content_sha256: bda9b89d75fd4f4f1f74fe1d682791041a278763268e1e886e27df8470191545
---

# Collect Votes with MEDKit

MEDKit groups numeric viewer choices by a developer-defined vote ID. Use one ID per logical round so earlier submissions cannot be mistaken for current results.

## Submit a vote

```javascript
import Muxy from "@muxy/extensions-js";
Muxy.setup({ clientID: import.meta.env.VITE_MUXY_CLIENT_ID });
const medkit = new Muxy.SDK();
await medkit.loaded();

const pollID = "round-42-map-choice";
const result = await medkit.vote(pollID, 1);

console.log(`Accepted vote ${result.vote}; total votes: ${result.count}`);
```

`vote(id, value)` requires a string ID and numeric value. The resolved `VoteData` is the current aggregate plus the current user's vote when available.

Prefix an ID with `global-` only when votes should be shared across all channels using the extension. Otherwise, results are channel-scoped.

## Read results

```javascript
const voteData = await medkit.getVoteData(pollID);
console.log({
  count: voteData.count,
  sum: voteData.sum,
  mean: voteData.mean,
  stddev: voteData.stddev,
  optionOneVotes: voteData.specific[1] ?? 0,
  currentViewerVote: voteData.vote,
});
```

The 2.4.18 type is flat:

```json
{
  "count": 1,
  "mean": 1,
  "specific": [0, 1, 0, 0, 0, 0],
  "stddev": 0,
  "sum": 1,
  "vote": 1
}
```

| Field | Meaning |
| --- | --- |
| `count` | Number of counted votes |
| `mean` | Average numeric value |
| `specific` | Counts indexed by supported non-negative vote values |
| `stddev` | Approximate standard deviation |
| `sum` | Sum of numeric values |
| `vote` | Current user's value when one exists |

The package comments disagree about the exact indexed range represented by `specific`. Keep application choices in the displayed indices you have tested and rely on `count`, `sum`, `mean`, and `stddev` for other numeric values.

## React to updates

`listen()` returns a handle, not a promise. The vote-update event payload is not strongly typed, so re-read the aggregate in the callback:

```javascript
const handle = medkit.listen(`vote_update:${pollID}`, async () => {
  renderResults(await medkit.getVoteData(pollID));
});

window.addEventListener(
  "pagehide",
  () => medkit.unlisten(handle),
  { once: true },
);
```

Debounce rendering or requests if your interface can receive bursts of updates.

## Retrieve vote logs

`getFullVoteLogs(id)` is admin-only and can return a large result. Each entry contains an `identifier` and numeric `value`.

```javascript
const { result: entries } = await medkit.getFullVoteLogs(pollID);
const identifiersByValue = new Map();

for (const { identifier, value } of entries) {
  const identifiers = identifiersByValue.get(value) ?? [];
  identifiers.push(identifier);
  identifiersByValue.set(value, identifiers);
}
```

Do not expose vote logs to viewers or analytics. Prefer aggregate results unless an approved administrative workflow needs individual entries.

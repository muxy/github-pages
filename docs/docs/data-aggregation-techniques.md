---
title: Aggregate Viewer Data
description: Choose MEDKit accumulation, ranking, or voting APIs for large-audience
  input.
slug: data-aggregation-techniques
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
approved_content_sha256: c0bb1ef20d7eb5b21354b46e10ba0de06a3815d1877c93484eac11b249d45f36
---

# Aggregate Viewer Data

MEDKit aggregation APIs collect many viewer submissions without storing a custom object for every viewer in channel state.

| Need | Submit | Read | Guide |
| --- | --- | --- | --- |
| Preserve arbitrary timestamped payloads | `accumulate(id, data)` | `getAccumulateData(id, start)` | [Accumulation](accumulation.md) |
| Count matching text choices | `rank(id, value)` | `getRankData(id)` | [Ranking](ranking.md) |
| Collect numeric choices and statistics | `vote(id, value)` | `getVoteData(id)` | [Voting](voting.md) |

## Accumulate viewer input

Any authorized viewer can submit JSON-serializable data. Reading the accumulated records is broadcaster-only.

```javascript
await medkit.accumulate("round-feedback", {
  round: 4,
  reaction: "excited",
});

const oneMinuteAgo = Date.now() - 60_000;
const result = await medkit.getAccumulateData(
  "round-feedback",
  oneMinuteAgo,
);

for (const entry of result.data) {
  console.log(entry.observed, entry.data);
}
```

Use stable identifiers for a continuous stream and include a round or schema version in each payload. Validate payload size and shape before submission; the SDK's generic types do not enforce your application schema.

## Choose the smallest result shape

- Use ranking when the useful result is a text value plus its score.
- Use voting when choices are numeric and you need count, mean, sum, or standard deviation.
- Use accumulation only when you need each submitted payload and its observation metadata.

Do not put aggregate results into state on every viewer submission. If viewers need a durable snapshot, update state at a bounded interval and use events only to prompt open clients to refresh.

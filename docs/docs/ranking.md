---
title: Ranking User Data
description: Count normalized open-ended viewer answers and manage each ranking round
  safely.
slug: ranking
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
approved_content_sha256: bd16099f30be5020d075331a1212147df9a776eab66a928ffac136ac1c28f51e
---

# Ranking User Data

Use ranking for an open-ended question whose result is the frequency of each exact text response. For a given ranking ID, the service keeps one current answer per viewer identity and returns matching strings with a numeric score.

Ranking does not normalize spelling, capitalization, whitespace, aliases, or unsafe text. Your application owns input rules and display safety.

## Define one round

Give every question run a distinct ID. A stable pattern such as `next-game-2026-07-14-round-3` prevents late requests from one round changing another round's results.

Normalize only the differences your product wants to collapse:

```javascript
function normalizeAnswer(value) {
  return value.trim().replace(/\s+/g, " ").toLocaleLowerCase("en-US");
}
```

If `DOTA`, `dota`, and `Dota` should be separate answers, submit the original string instead. Apply a length limit and reject empty input before making the request.

## Submit an answer

After MEDKit is ready, call `rank(rankID, value)` from the viewer context:

```javascript
const rankID = "next-game-2026-07-14-round-3";
const answer = normalizeAnswer(answerInput.value);

if (!answer || answer.length > 80) {
  throw new Error("Enter an answer between 1 and 80 characters.");
}

const result = await medkit.rank(rankID, answer);
if (!result.accepted) {
  throw new Error("The ranking service did not accept the answer.");
}

if (result.original !== undefined) {
  console.log(`Previous answer replaced: ${result.original}`);
}
```

`original` is optional and contains the viewer's previous value when the new submission replaces it. Do not treat a repeated submission as an extra vote.

## Read and display results

`getRankData(rankID)` requires a privileged broadcaster, admin, or backend context. MEDKit 2.4.18 resolves with an object whose `data` property contains the scored values:

```javascript
const { data } = await medkit.getRankData(rankID);

const results = data.map(({ key, score }) => ({
  label: key,
  responses: score,
}));

renderRanking(results);
```

Treat every `key` as untrusted viewer text. Render it with `textContent` or your framework's escaped text binding, not `innerHTML`. The API returns scores in service order; preserve that order unless your product defines and documents its own tie-break.

## End or recover a round

A broadcaster can clear the selected buffer with `clearRankData(rankID)`:

```javascript
await medkit.clearRankData(rankID);
```

Clearing is destructive. Prefer a new round ID when you need an audit trail or when late clients may still submit to the previous question. If a read fails, keep the last known result on screen, show that it is stale, and retry with backoff instead of clearing the buffer.

## Identity and retention constraints

- Ranking uniqueness follows the identity in the caller's JWT. A shared Twitch ID and an opaque ID are different identifiers, so identity changes can affect one-response-per-viewer behavior.
- Require shared identity only when your product needs stronger cross-session identity, and explain that requirement to viewers.
- The service compares submitted strings; moderation, normalization, profanity handling, and localization are application responsibilities.
- The pinned MEDKit declarations and OpenAPI contract do not guarantee a top-N size or automatic retention period. Do not build correctness around legacy claims of 100 results or one-day expiry.
- The pinned sources do not define an extension-wide `global` ID prefix. Treat IDs as ordinary buffer names unless the API owner confirms additional deployment behavior.

For raw HTTP requests and role requirements, see [Basic Ranking](../reference/rank.md).

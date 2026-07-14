---
title: Choose a Viewer Engagement API
description: Choose a verified MEDKit 2.4.18 API for votes, rankings, accumulated
  input, or trivia.
slug: viewer-engagement-tools
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
approved_content_sha256: a96f3f33bfe174913bb11eb619b04d6bbeedca1d9484f6b4b9cf6fa831d7f4af
---

# Choose a Viewer Engagement API

MEDKit 2.4.18 provides several server-backed ways to collect viewer input. Choose by the result shape your application needs.

| Experience | Submit API | Read API | Result |
| --- | --- | --- | --- |
| Numeric poll | `vote(id, value)` | `getVoteData(id)` | Count, mean, sum, standard deviation, and indexed counts |
| Open-ended popularity | `rank(id, value)` | `getRankData(id)` | Text values ranked by score |
| Raw viewer payloads | `accumulate(id, data)` | `getAccumulateData(id, start)` | Timestamped submissions with user/channel metadata |
| Structured trivia | Trivia question, option, vote, and leaderboard methods | Trivia getters | Questions, teams, votes, and leaderboard data |

Start with [polls and user voting](voting.md) for fixed choices, or [data aggregation](data-aggregation-techniques.md) for ranking and accumulation.

## Production design rules

- Use a stable schema and version it in each payload.
- Bound retries, pagination, and refresh frequency.
- Treat opaque and shared Twitch identifiers as personal data.
- Persist any state needed after refresh; live events are notifications, not storage.
- Enforce privileged operations with broadcaster, admin, or backend authorization rather than UI visibility alone.

The package types verify method signatures, not your product's poll lifecycle, retention policy, abuse limits, or reward rules. Keep those policies explicit in application code and have them reviewed before launch.

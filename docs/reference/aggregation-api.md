---
title: Aggregation API
description: Navigate the accumulation and ranking operations in the Muxy REST API.
slug: aggregation-api
product: REST API
audience: developers
status: current
owner: API Platform
source_of_truth: muxy/github-pages:openapi/rest-v1.yaml
version: v1
last_verified: '2026-07-14'
review_state: approved
page_type: protocol-reference
approved_by: peter-bonanni
approved_at: '2026-07-14T20:34:54Z'
approval_method: user-authorized-codex-assisted-source-review
approved_content_sha256: ccdbe3d53427c67e232ed38379398e5a21dd5d8a8c7bdb6fc05c65fe1356c432
---

# Aggregation API

The canonical v1 REST contract exposes two aggregation route groups: accumulation for collecting and retrieving entries, and ranking for collecting, retrieving, and clearing ranked responses.

All paths below are relative to `https://api.muxy.io/v1/e` and require the standard [`Authorization` header](medkit-rest-api.md#authorization).

| Group | Method and path | Generated operation reference |
| --- | --- | --- |
| Accumulation | `GET /accumulate` | [Get accumulated entries](accumulate-1.md) |
| Accumulation | `POST /accumulate` | [Submit an accumulation entry](accumulate-2.md) |
| Ranking | `GET /rank` | [Get ranked responses](rank-1.md) |
| Ranking | `POST /rank` | [Submit a ranked response](rank-2.md) |
| Ranking | `DELETE /rank` | [Clear ranked responses](rank-3.md) |

For concepts and lifecycle guidance, see [Basic Accumulation](accumulate.md) and [Basic Ranking](rank.md). Request bodies, query parameters, and responses remain canonical in the generated operation pages and OpenAPI; they are not duplicated here.

## Canonical OpenAPI

See the [raw `rest-v1.yaml` specification](https://docs.muxy.io/openapi/rest-v1.yaml). Sandbox token creation is defined separately in [raw `sandbox-v1.yaml`](https://docs.muxy.io/openapi/sandbox-v1.yaml).

---
type: persona
title: "OEE Chat Assistant — Tech view"
persona: tech
status: current
tags: [knowledge-base, tech, oee]
sources: [knowledge-base-adr, knowledge-base-cdf-assets, knowledge-base-cdf-timeseries, knowledge-base-cdf-activities, knowledge-base-cdf-files]
created: 2026-10-02
updated: 2026-10-04
---

# OEE Chat Assistant — Tech view

This is Tech's reading of `knowledge-base`, drawn from [[knowledge-base-adr]] (what Tech has
committed to and ruled out) plus the CDF project — [[knowledge-base-cdf-assets]],
[[knowledge-base-cdf-timeseries]], [[knowledge-base-cdf-activities]], and
[[knowledge-base-cdf-files]] (what the tools actually query against). The ADR and the CDF
project are both Tech's exclusive sources — Business and Product may reference them but never
own them. This page does not reflect what Business has promised the customer — see
[[knowledge-base-conflicts]] for where this view disagrees with the other personas.

## What Tech has committed to build (v1)

Exactly three read-only tools, registered against the Veridion mock CDF project's Core Data
Model instances:

1. **OEE snapshot** — resolve a line asset (e.g. `asset_line3`, see [[knowledge-base-cdf-assets]])
   and return its most recent OEE plus the Availability / Performance / Quality breakdown
   (`ts_line3_oee_pct`, `ts_line3_availability_pct`, `ts_line3_performance_pct`,
   `ts_line3_quality_pct`, see [[knowledge-base-cdf-timeseries]]).
2. **OEE trend** — query any OEE-related `CogniteTimeSeries` over a date range (see
   [[knowledge-base-cdf-timeseries]]).
3. **Downtime history** — list `CogniteActivity` instances behind Availability loss (e.g.
   `activity_line3_unplanned_stop_valve_fault`, see [[knowledge-base-cdf-activities]]).

## The CDF project Tech owns and maintains

Tech (Data Engineer, Data Scientist, Solutions Architect) owns the mock CDF project these tools
query against — one space, `sp_veridion_demo`: an asset hierarchy
([[knowledge-base-cdf-assets]]), six time series ([[knowledge-base-cdf-timeseries]]), two
downtime activities ([[knowledge-base-cdf-activities]]), and one SOP file
([[knowledge-base-cdf-files]]). It is static and fictional — no deployed tenant, no cluster, no
credentials — but every `externalId` cited above resolves against it, so the "no invented
`externalId`" rule is checkable, not just asserted.

## What Tech has explicitly ruled out

**No write tool is registered.** There is no tool capable of creating, updating, or deleting
any CDF resource. ADR 001 explicitly rejected a "generate work order" tool for v1, because no
work-order resource, schema, or agreed OEE threshold policy exists anywhere in the CDF
project.

## Other constraints Tech has committed to

- **Cluster boundary** — reads are confined to the one CDF project/space, `sp_veridion_demo`.
- **No invented `externalId`** — if a lookup finds nothing, the agent says so; it never
  fabricates an identifier to produce an answer.
- **Citation required** — every factual claim must cite the specific `(space, externalId)`
  it came from.

## Open conflicts involving this view

See [[knowledge-base-conflicts]] — the "no write tool" decision above directly contradicts the
auto-work-order promise in [[knowledge-base-business]]. [[knowledge-base-product]] independently
scoped the same read-only boundary, so this is Business against both Product and Tech, not
Tech alone.

See [[tech-glossary]] for the vocabulary used above, written for Business and Product.

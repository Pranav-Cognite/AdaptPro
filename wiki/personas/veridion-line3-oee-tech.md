---
type: persona
title: "Veridion Line 3 OEE — Tech view"
persona: tech
status: current
tags: [veridion-line3-oee, tech, oee]
sources: [veridion-line3-oee-adr, veridion-line3-oee-cdf-assets, veridion-line3-oee-cdf-timeseries, veridion-line3-oee-cdf-activities, veridion-line3-oee-cdf-files, veridion-line3-oee-cdf-model-and-pipelines]
created: 2026-10-02
updated: 2026-10-16
---

# Veridion Line 3 OEE — Tech view

Line 3 is the polymer production line at Calder Valley (`asset_line3`): Reactor R-301, then
Extruder EX-302. This page is only what Tech will build for that line in v1: a read-only
lookup of OEE and downtime. Creating a work order is refused here.

This is Tech's reading of `veridion-line3-oee`, drawn from [[veridion-line3-oee-adr]] (what Tech has
committed to and ruled out) plus the CDF project — [[veridion-line3-oee-cdf-assets]],
[[veridion-line3-oee-cdf-timeseries]], [[veridion-line3-oee-cdf-activities]], and
[[veridion-line3-oee-cdf-files]] (what the tools actually query against). The ADR and the CDF
project are both Tech's exclusive sources — Business and Product may reference them but never
own them. This page does not reflect what Business has promised the customer — see
[[veridion-line3-oee-open-topics]] for where this view disagrees with the other personas.

## What Tech has committed to build (v1)

Exactly three read-only capabilities, registered against the Veridion mock CDF project's Core
Data Model instances:

1. **OEE snapshot** — resolve a line asset (e.g. `asset_line3`, see [[veridion-line3-oee-cdf-assets]])
   and return its most recent OEE plus the Availability / Performance / Quality breakdown
   (`ts_line3_oee_pct`, `ts_line3_availability_pct`, `ts_line3_performance_pct`,
   `ts_line3_quality_pct`, see [[veridion-line3-oee-cdf-timeseries]]).
2. **OEE trend** — query any OEE-related `CogniteTimeSeries` over a date range (see
   [[veridion-line3-oee-cdf-timeseries]]).
3. **Downtime history** — list `CogniteActivity` instances behind Availability loss (e.g.
   `activity_line3_unplanned_stop_valve_fault`, see [[veridion-line3-oee-cdf-activities]]).

## The CDF project Tech owns and maintains

Tech (Data Engineer, Data Scientist, Solutions Architect) owns the mock CDF project these tools
query against. Instances are all in one space, `sp_veridion_demo`: 40 assets
([[veridion-line3-oee-cdf-assets]]), 21 time series with 30 days of datapoints
([[veridion-line3-oee-cdf-timeseries]]), 11 downtime activities
([[veridion-line3-oee-cdf-activities]]), and 10 file records including the OEE calculation SOP
([[veridion-line3-oee-cdf-files]]). A custom data model, three extractors, a transformation, an OEE
function and the access groups sit behind them ([[veridion-line3-oee-cdf-model-and-pipelines]]).
It is static and fictional — no deployed tenant, no cluster, no credentials — but every
`externalId` cited above resolves against it, so the "no invented `externalId`" rule is checkable,
not just asserted.

The data is deliberately not clean: two OEE definitions coexist (SOP and legacy MES), one stop is
logged twice, one has no end time, some stops are never logged, one gap and one frozen sensor sit
in the process data, and R-301 exists as a live and a decommissioned asset. Those are in the
source pages above, not hidden.

## What Tech has explicitly ruled out

**No write capability is registered.** There is no path capable of creating, updating, or
deleting any CDF resource. ADR 001 explicitly rejected a "generate work order" path for v1,
because no work-order resource, schema, or agreed OEE threshold policy exists anywhere in the
CDF project.

## Other constraints Tech has committed to

- **Cluster boundary** — reads are confined to the one CDF project/space, `sp_veridion_demo`.
- **No invented `externalId`** — if a lookup finds nothing, say so; never fabricate an
  identifier to produce an answer.
- **Citation required** — every factual claim must cite the specific `(space, externalId)`
  it came from.

## Open conflicts involving this view

See [[veridion-line3-oee-open-topics]] — the "no write tool" decision above directly contradicts the
auto-work-order promise in [[veridion-line3-oee-business]]. [[veridion-line3-oee-product]] independently
scoped the same read-only boundary, so this is Business against both Product and Tech, not
Tech alone.

See [[tech-glossary]] for the vocabulary used above, written for Business and Product.

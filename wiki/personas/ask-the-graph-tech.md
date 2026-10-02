---
type: persona
title: "Ask the Graph — Tech view"
persona: tech
epic: ask-the-graph
status: current
tags: [ask-the-graph, tech, oee]
sources: [ask-the-graph-adr]
created: 2026-10-02
updated: 2026-10-02
---

# Ask the Graph — Tech view

This is Tech's reading of the `ask-the-graph` epic, drawn only from [[ask-the-graph-adr]]. It
does not reflect what Business has promised the customer — see [[ask-the-graph-conflicts]]
for where this view disagrees with the other personas.

## What Tech has committed to build (v1)

Exactly three read-only tools, registered against the Veridion mock CDF project's Core Data
Model instances:

1. **OEE snapshot** — resolve a line asset (e.g. `asset_line3`) and return its most recent
   OEE plus the Availability / Performance / Quality breakdown (`ts_line3_oee_pct`,
   `ts_line3_availability_pct`, `ts_line3_performance_pct`, `ts_line3_quality_pct`).
2. **OEE trend** — query any OEE-related `CogniteTimeSeries` over a date range.
3. **Downtime history** — list `CogniteActivity` instances behind Availability loss (e.g.
   `activity_line3_unplanned_stop_valve_fault`).

## What Tech has explicitly ruled out

**No write tool is registered.** There is no tool capable of creating, updating, or deleting
any CDF resource. ADR 001 explicitly rejected a "generate work order" tool for v1, because no
work-order resource, schema, or agreed OEE threshold policy exists anywhere in the CDF
project.

## Other constraints Tech has committed to

- **Cluster boundary** — reads are confined to the one CDF project/space for this epic
  (`sp_veridion_demo`).
- **No invented `externalId`** — if a lookup finds nothing, the agent says so; it never
  fabricates an identifier to produce an answer.
- **Citation required** — every factual claim must cite the specific `(space, externalId)`
  it came from.

## Open conflicts involving this view

See [[ask-the-graph-conflicts]] — the "no write tool" decision above directly contradicts the
auto-work-order promise in [[ask-the-graph-business]]. [[ask-the-graph-product]] independently
scoped the same read-only boundary, so this is Business against both Product and Tech, not
Tech alone.

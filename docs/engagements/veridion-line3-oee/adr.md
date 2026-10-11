# ADR 001 — Veridion Line 3 OEE engagement: read-only tool set for v1

**Status:** Accepted  
**Owner:** Tech / Architecture  
**Engagement:** Veridion Line 3 OEE (`veridion-line3-oee`) — Veridion Chemicals, Calder Valley Plant

## Context

The Veridion Line 3 OEE engagement needs natural-language questions about OEE (Overall
Equipment Effectiveness) for a production line, grounded in the Veridion CDF project's Core
Data Model instances (`CogniteAsset`, `CogniteTimeSeries`, `CogniteActivity`, `CogniteFile` —
see `mock-cdf-project/`). We need to decide what the delivery is allowed to do: read OEE data
only, or also write back (e.g. generate a corrective work order).

## Decision

For v1, the delivery registers exactly three capabilities, all read-only:

1. **OEE snapshot** — resolve a `CogniteAsset` (e.g. `asset_line3`) and return its most
   recent OEE value plus the Availability / Performance / Quality breakdown from
   `ts_line3_oee_pct`, `ts_line3_availability_pct`, `ts_line3_performance_pct`, and
   `ts_line3_quality_pct`.
2. **OEE trend** — query any of the four OEE-related `CogniteTimeSeries` over a date range
   and summarize the trend.
3. **Downtime history** — list `CogniteActivity` instances linked to a line (e.g.
   `activity_line3_unplanned_stop_valve_fault`) within a date range, to explain Availability
   loss.

**No write capability is registered.** There is no path capable of creating, updating, or
deleting any CDF resource — no work order, no activity, nothing. v1 is read-only.

Additional constraints:

- **Cluster boundary.** Reads only from the single CDF project/space defined for this
  engagement (`sp_veridion_demo`). No cross-project or cross-cluster access.
- **No invented `externalId`.** If a lookup returns no match, report that nothing was found.
  Never fabricate an `externalId` to produce an answer.
- **Citation required.** Every factual claim must cite the specific `(space, externalId)` of
  the instance it came from.

## Alternatives considered

- **Register a "generate work order" path now, gated behind a confirmation step.** Rejected.
  There is no work order resource defined anywhere in the Veridion CDF project, no schema for
  what a work order instance would contain, no agreed OEE threshold that should trigger one,
  and no agreement on who is liable if one is created incorrectly. A confirmation UI around a
  capability with no backing resource hides the gap instead of closing it.
- **Allow writes only to a sandboxed "draft" space, never the real one.** Rejected for v1.
  Still requires a work-order schema and a review workflow that does not yet exist; adds
  scope without changing what the customer can actually do with the result.

## Consequences

- v1 **cannot** fulfill the "automatically generate a corrective work order" promise in the
  business use case. It can report that OEE dropped and explain why (e.g. an unplanned stop
  on Reactor R-301), but it cannot act on it.
- Any ticket or feature request that assumes write capability (e.g. auto-generating a work
  order on an OEE threshold breach) is out of scope for this ADR and requires a new decision,
  including a work order schema and a defined threshold policy, before it can be built.
- This decision holds until superseded by a new ADR.

## How this document is used in AdaptPro

This ADR (plus the mock CDF project) is **Tech's exclusive source** for the
`veridion-line3-oee` knowledge base. AdaptPro ingests it into the Tech persona view so
Business and Product can query what is actually buildable in v1.

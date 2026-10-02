# ADR 001 — OEE Chat Assistant: read-only tool set for v1

**Status:** Accepted
**Owner:** Tech / Architecture
**Epic:** OEE Chat Assistant (Veridion Chemicals, Calder Valley Plant)

## Context

"OEE Chat Assistant" lets a user ask natural-language questions about OEE (Overall Equipment
Effectiveness) for a production line, grounded in the Veridion CDF project's Core Data Model
instances (`CogniteAsset`, `CogniteTimeSeries`, `CogniteActivity`, `CogniteFile` — see
`mock-cdf-project/`). We need to decide what the agent is allowed to do: read OEE data only,
or also write back to CDF (e.g. generate a corrective work order).

## Decision

For v1, the agent registers exactly three tools, all read-only:

1. **OEE snapshot** — resolve a `CogniteAsset` (e.g. `asset_line3`) and return its most
   recent OEE value plus the Availability / Performance / Quality breakdown from
   `ts_line3_oee_pct`, `ts_line3_availability_pct`, `ts_line3_performance_pct`, and
   `ts_line3_quality_pct`.
2. **OEE trend** — query any of the four OEE-related `CogniteTimeSeries` over a date range
   and summarize the trend.
3. **Downtime history** — list `CogniteActivity` instances linked to a line (e.g.
   `activity_line3_unplanned_stop_valve_fault`) within a date range, to explain Availability
   loss.

**No write tool is registered.** There is no tool capable of creating, updating, or deleting
any CDF resource — no work order, no activity, nothing. The agent is a reader.

Additional constraints registered alongside these tools:

- **Cluster boundary.** The agent only reads from the single CDF project/space defined for
  this epic (`sp_veridion_demo`). It does not reach across projects or clusters.
- **No invented `externalId`.** If a lookup returns no match, the agent reports that nothing
  was found. It must never fabricate an `externalId` to produce an answer.
- **Citation required.** Every factual claim in an answer must cite the specific
  `(space, externalId)` of the instance it came from.

## Alternatives considered

- **Register a "generate work order" tool now, gated behind a confirmation step.** Rejected.
  There is no work order resource defined anywhere in the Veridion CDF project, no schema for
  what a work order instance would contain, no agreed OEE threshold that should trigger one,
  and no agreement on who is liable if the agent creates one incorrectly. Building a
  confirmation UI around a tool with no backing resource just hides the gap instead of
  closing it.
- **Allow writes only to a sandboxed "draft" space, never the real one.** Rejected for v1.
  Still requires a work-order schema and a review workflow that does not yet exist; adds
  scope without changing what the customer can actually do with the result.

## Consequences

- The agent **cannot** fulfill the "automatically generate a corrective work order" promise
  in the business use case. It can report that OEE dropped and explain why (e.g. an
  unplanned stop on Reactor R-301), but it cannot act on it.
- Any ticket or feature request that assumes write capability (e.g. auto-generating a work
  order on an OEE threshold breach) is out of scope for this ADR and requires a new decision,
  including a work order schema and a defined threshold policy, before it can be built.
- This decision holds until superseded by a new ADR.

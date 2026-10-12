# PRD — Veridion Line 3 OEE engagement: OEE for Production Line 3

**Status:** Draft, v1 scope  
**Owner:** Product  
**Engagement:** Veridion Line 3 OEE (`veridion-line3-oee`) — Veridion Chemicals, Calder Valley Plant

## In plain language

Line 3 is the polymer production line at Calder Valley (`asset_line3`), from Reactor R-301
through Extruder EX-302. This document is what Product will actually ship in v1: three
read-only questions about that line's OEE and downtime. It does not include the automatic
work order Business promised.

## Problem

Production supervisors at Calder Valley pull OEE numbers from a separate reporting tool,
after a shift ends, with no easy way to see what drove a drop — downtime, slow running, or
scrap. This engagement scopes a **CDF-grounded OEE capability for Production Line 3**: read
OEE and explain loss drivers from real CDF data, with every answer citing the instances used.

## Data architecture — how OEE data gets into CDF

Three Cognite extractors feed the Core Data Model instances this engagement queries
(`mock-cdf-project/`):

| Extractor | Source system | Feeds |
| --- | --- | --- |
| **Cognite OPC UA Extractor** | Plant OPC UA servers (PLCs/DCS on Line 3) | Process time series: `ts_reactor_r301_temperature_degc`, `ts_line3_output_rate_kg_per_hr` — the raw signals behind the Performance component. |
| **Cognite SAP Extractor** | SAP PM (Plant Maintenance) | Equipment master data enriching `CogniteAsset` records, and downtime/maintenance records landing as `CogniteActivity` instances (`activity_line3_changeover`, `activity_line3_unplanned_stop_valve_fault`) — the Availability component. |
| **Cognite DB Extractor** | Plant MES / batch quality database | Good-unit and reject-unit counts, rolled up into `ts_line3_quality_pct` — the Quality component. |

The composite `ts_line3_oee_pct` and the three component series
(`ts_line3_availability_pct`, `ts_line3_performance_pct`, `ts_line3_quality_pct`) are
calculated from these three feeds per the OEE Calculation SOP (`file_line3_oee_calculation_sop`).
This PRD scopes what the product queries once that data is in CDF — it does not scope the
extractor pipelines or transformations themselves.

## In scope for v1

Three read-only query templates — **identical to what Tech has committed to build** (see
`adr.md`):

1. **OEE snapshot** — current OEE and its Availability/Performance/Quality breakdown for a
   line.
2. **OEE trend** — any OEE or component time series over a date range.
3. **Downtime history** — `CogniteActivity` records behind Availability loss for a line and
   date range.

Every answer cites the specific `(space, externalId)` instances it used.

## Explicitly out of scope for v1

- **Creating, updating, or triggering any SAP work order, or any other write action.** The
  SAP Extractor referenced above is inbound only (SAP → CDF); this PRD does not scope a path
  back from CDF into SAP, and does not scope any new work-order resource in CDF either.
  "Automatically generate a corrective work order on OEE drop" — the promise Business has made
  to Veridion — is not in this PRD. See `adr.md` for why, and see
  `../../../wiki/synthesis/veridion-line3-oee-conflicts.md` for the open conflict this creates
  with Business's commitment.
- Any OEE threshold/alerting policy (what counts as "OEE dropped below target") — not defined
  anywhere yet, and a prerequisite for any future write capability.

## Acceptance criteria

- A user can ask for Line 3's current OEE and get Availability/Performance/Quality with
  citations.
- A user can ask for an OEE trend over a date range and get a correct summary with citations.
- A user can ask what drove an Availability loss and get the relevant downtime activity with
  citations.
- The system never returns a fabricated `externalId`; it says "not found" instead.
- No tool in this engagement can write to CDF or to any source system.

## How this document is used in AdaptPro

This PRD is **Product's exclusive source** for the `veridion-line3-oee` knowledge base.
AdaptPro ingests it into the Product persona view so Business and Tech can query what was
actually scoped for v1.

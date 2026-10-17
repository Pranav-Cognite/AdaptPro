---
type: source
title: "Veridion Line 3 OEE — CDF activities (mock-cdf-project)"
tags: [veridion-line3-oee, tech, cdf, cdm, activities, downtime]
authors: [Tech/Architecture]
url: null
raw: mock-cdf-project/modules/veridion_line3_oee/data_modeling/activities.node.yaml
ingested: 2026-10-16
created: 2026-10-04
updated: 2026-10-16
---

# Veridion Line 3 OEE — CDF activities (mock-cdf-project)

The downtime records for Production Line 3 in the fake plant data. Some stops are planned and do
not count as a loss. Others are unplanned and do. A few records are messy in the way real SAP
records are.

11 `CogniteActivity` node instances over 2026-09-17 to 2026-10-14. The two the ADR cites are
unchanged: `activity_line3_changeover` (planned, excluded from loss) and
`activity_line3_unplanned_stop_valve_fault` (unplanned, FV-301 on Reactor R-301, counted as loss).
Around them: three more planned records (two changeovers, a screen pack change, an agitator seal
inspection), a die-pressure trip, a feed-pump trip, a repeat FV-301 stop on 2026-10-09, a
pelletizer jam, and a second notification for the 09-30 valve fault.
`CogniteActivity` is the Core Data Model's equivalent of a legacy "event" — there is no
`CogniteEvent` view. Each record is also classed through `VeridionDowntimeActivity` (planned or
unplanned, SAP notification id, cause code, shift).

Messy on purpose:

- **Logged twice:** the 09-30 stop appears as an operator notification and as a maintenance
  notification (`..._maint_notification`). Adding both durations double-counts.
- **No end time:** the 10-14 pelletizer jam (`..._pelletizer_20261014`) was never closed in SAP. OEE
  availability ignores it, so the loss appears in Performance instead.
- **Repeat failure:** FV-301 stuck on 09-30 and again on 10-09. The draft RCA for the first
  (`file_rca_2026_09_30_fv301_valve_fault`) was still open when it recurred.
- **Not here at all:** micro-stops under about 10 minutes are not in SAP.
- **No work order.** SAP work orders exist only in SAP. Nothing in CDF creates or tracks one.

Full text: `mock-cdf-project/modules/veridion_line3_oee/data_modeling/activities.node.yaml`

## Where this fits

- [[veridion-line3-oee-tech]] — Tech's "Downtime history" tool lists these activity instances;
  Tech owns and maintains this CDF project.
- [[veridion-line3-oee-cdf-assets]] — the assets and equipment each activity is linked to.
- [[veridion-line3-oee-cdf-timeseries]] — the unplanned valve stops cross-link to
  `ts_reactor_r301_temperature_degc` and the FV-301 position series via `timeSeries`.
- [[veridion-line3-oee-cdf-model-and-pipelines]] — the SAP extractor and transformation that produce these.

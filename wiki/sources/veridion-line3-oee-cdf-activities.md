---
type: source
title: "Veridion Line 3 OEE — CDF activities (mock-cdf-project)"
tags: [veridion-line3-oee, tech, cdf, cdm, activities, downtime]
authors: [Tech/Architecture]
url: null
raw: mock-cdf-project/modules/veridion_line3_oee/data_modeling/activities.node.yaml
ingested: 2026-10-04
created: 2026-10-04
updated: 2026-10-04
---

# Veridion Line 3 OEE — CDF activities (mock-cdf-project)

The downtime records for Production Line 3 in the fake plant data. One stop is planned and
does not count as a loss. One stop is an unplanned valve fault and does count.

The two `CogniteActivity` node instances driving the Availability component of Line 3's OEE:
`activity_line3_changeover` (a planned grade changeover, excluded from loss) and
`activity_line3_unplanned_stop_valve_fault` (an unplanned stop on Reactor R-301, counted as
loss). `CogniteActivity` is the Core Data Model's equivalent of a legacy "event" — there is no
`CogniteEvent` view — so this is the correct concept, and it carries scheduling fields instead
of a single timestamp.

Full text: `mock-cdf-project/modules/veridion_line3_oee/data_modeling/activities.node.yaml`

## Where this fits

- [[veridion-line3-oee-tech]] — Tech's "Downtime history" tool lists exactly these activity
  instances; Tech owns and maintains this CDF project.
- [[veridion-line3-oee-cdf-assets]] — the assets each activity is linked to via `assets`.
- [[veridion-line3-oee-cdf-timeseries]] — `activity_line3_unplanned_stop_valve_fault` cross-links to
  `ts_reactor_r301_temperature_degc` via `timeSeries`.

---
type: glossary
title: "Tech glossary — for Business and Product"
persona: tech
tags: [glossary, tech, oee, cdf]
sources: [veridion-line3-oee-adr, veridion-line3-oee-cdf-assets, veridion-line3-oee-cdf-timeseries, veridion-line3-oee-cdf-activities, veridion-line3-oee-cdf-files, veridion-line3-oee-cdf-model-and-pipelines]
created: 2026-10-03
updated: 2026-10-16
---

# Tech glossary

Terms Tech (architect/engineer) uses day-to-day. Written for Business and Product to read when
they need to understand what Tech means, not for Tech's own reference. `asset_line3` is
Production Line 3, the polymer line at Calder Valley (Reactor R-301, then Extruder EX-302).

- **ADR (Architecture Decision Record)** — a specific technical decision, with the alternatives
  considered and rejected. `veridion-line3-oee-adr` here. Different from a PRD: a PRD says *what*,
  an ADR says *how* and locks in a *why not*.
- **CogniteAsset / CogniteTimeSeries / CogniteActivity / CogniteFile** — the Core Data Model
  (CDM) types this project's data is stored as. `CogniteActivity` is the modern equivalent of a
  legacy "event" — there is no `CogniteEvent` type.
- **externalId / space** — every piece of data is identified by an `(space, externalId)` pair.
  "No invented `externalId`" means the agent must say "not found" rather than guess one.
- **Contextualization** — linking a raw data point (a sensor tag, a SAP record) to the
  `CogniteAsset` it belongs to, via the `assets` relation. Without this, a query template has
  nothing to traverse — see the glossary note under Data Engineering's work if more detail is
  needed.
- **Cluster boundary** — the agent only reads instances from the one CDF project/space defined here
  (`sp_veridion_demo`); it does not reach across projects or clusters. To resolve views it also
  needs to read the schema space `sp_veridion_dm` and the Core Data Model space `cdf_cdm`, which
  hold definitions and no plant data. The ADR's wording does not mention this.
- **Tool** — a specific, registered capability the agent can call (e.g. "OEE snapshot"). "No
  write tool" means literally no registered capability can create/update/delete anything — not
  a permissions setting, a missing capability.
- **Citation** — every factual claim in an answer must name the exact `(space, externalId)` it
  came from. This is an honesty guarantee, not a proof the underlying data is correct or
  complete.

## Data-model and pipeline terms (from the CDF project)

- **Space (schema space vs instance space)** — a namespace in CDF. Here the definitions of the data
  (`sp_veridion_dm`) are kept apart from the plant data itself (`sp_veridion_demo`), so who may change
  the model and who may read the data can be set separately.
- **View / data model** — a named shape for data. The Veridion views extend the standard Core Data
  Model types with plant-specific fields (SAP functional location, loss class, known issues, document
  revision). The `VeridionOEE` data model bundles them.
- **Extractor / RAW / transformation / function / workflow** — the path data takes in: an extractor
  copies from a source system (OPC UA servers, SAP PM, the MES database); RAW holds the untouched copy;
  a transformation (SQL) reshapes it into CDF instances; a function (Python) computes derived series
  such as OEE; a workflow runs them in order every hour.
- **Functional location vs equipment** — SAP PM's split. A functional location is a place in the plant
  (`CV-P-L3-R301`, "the reactor position on Line 3"); equipment is the physical item installed there.
  Here a functional location is a `CogniteAsset` and the item is a `CogniteEquipment`.
- **SAP notification** — a maintenance record raised for a fault or planned task. Becomes a
  `CogniteActivity`. It can be raised twice for the same stop, and can be left open with no end time.
  SAP work orders are different and are not copied into CDF.
- **Planned vs unplanned downtime** — planned (changeover, scheduled maintenance) is removed from the time
  the line was supposed to run; unplanned (breakdown, trip) counts against Availability.
- **Ideal rate** — the throughput Performance is measured against. 3,800 kg/h under SOP rev B; 4,200 kg/h
  in the legacy MES report. It is the main reason the two OEE numbers differ.
- **Legacy MES OEE** — the shift-end OEE number the plant already uses, defined differently from the SOP.
  Not comparable with the SOP-based series.
- **Micro-stop** — a stop too short (here 3 to 8 minutes) to be logged in SAP. It only shows up as lost
  output, so it lands in Performance, not Availability.
- **Data gap vs zero** — a missing reading means no data, not no production. A tool must not treat it as 0.
- **MOC / RCA** — Management of Change (the approval record for a change to a procedure or equipment);
  Root Cause Analysis (the write-up of why a failure happened). Both exist here as file records.

---
type: source
title: "Veridion Line 3 OEE — CDF asset hierarchy (mock-cdf-project)"
tags: [veridion-line3-oee, tech, cdf, cdm, assets]
authors: [Tech/Architecture]
url: null
raw: mock-cdf-project/modules/veridion_line3_oee/data_modeling/assets.node.yaml
ingested: 2026-10-04
created: 2026-10-04
updated: 2026-10-04
---

# Veridion Line 3 OEE — CDF asset hierarchy (mock-cdf-project)

Where Line 3 sits in the fake plant. Calder Valley Plant contains the Polymer Production Unit,
which contains Production Line 3 (`asset_line3`), which contains Reactor R-301 and Extruder
EX-302. These names exist so the other documents are not inventing equipment.

The `CogniteAsset` node instances backing the Veridion Line 3 OEE engagement, in space `sp_veridion_demo`:
`plant_caldervalley` → `area_polymer_unit` → `asset_line3` → `asset_reactor_r301` /
`asset_extruder_ex302`. This is fixture data maintained by Tech (Data Engineer, Data Scientist,
Solutions Architect) — not a claim any persona makes, but the asset hierarchy every other CDM
resource (time series, activities, files) links back to via the `assets` relation.

Full text: `mock-cdf-project/modules/veridion_line3_oee/data_modeling/assets.node.yaml`

## Where this fits

- [[veridion-line3-oee-tech]] — Tech's own page; Tech owns and maintains this CDF project.
- [[veridion-line3-oee-cdf-timeseries]], [[veridion-line3-oee-cdf-activities]],
  [[veridion-line3-oee-cdf-files]] — the other CDM resource types in this same mock project, all
  linked back to these assets.
- This is **not** a deployed CDF tenant — see `mock-cdf-project/README.md`. It exists so every
  `externalId` the business use case, PRD, and ADR reference resolves to something real.

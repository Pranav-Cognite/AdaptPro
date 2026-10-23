---
type: source
title: "Veridion Line 3 OEE — CDF asset hierarchy (mock-cdf-project)"
tags: [veridion-line3-oee, tech, cdf, cdm, assets]
authors: [Tech/Architecture]
url: null
raw: mock-cdf-project/modules/veridion_line3_oee/data_modeling/assets.node.yaml
ingested: 2026-10-16
created: 2026-10-04
updated: 2026-10-16
---

# Veridion Line 3 OEE — CDF asset hierarchy (mock-cdf-project)

Where Line 3 sits in the fake plant. Calder Valley Plant contains the Polymer Production Unit,
which contains Production Line 3 (`asset_line3`), which contains Reactor R-301 and Extruder
EX-302 and the equipment on them. These names exist so the other documents are not inventing equipment.

40 `CogniteAsset` node instances in space `sp_veridion_demo`, five levels deep: plant
(`plant_caldervalley`) → areas (`area_polymer_unit`, utilities, packaging and warehouse, quality
lab) → lines 1 to 4 → units → components. Line 3 is described in full: `asset_reactor_r301` (feed
valve FV-301, agitator M-301, feed pumps P-301A/B, jacket cooler HX-301, temperature transmitters
TT-301A/B, pressure transmitter PT-301), `asset_extruder_ex302` (screw drive M-302, gearbox,
die head, screen changer, die pressure transmitter), then pelletizer PL-303, dryer DR-304 and
packaging PK-305. Lines 1, 2 and 4 are reactor and extruder only.

Each asset is also populated through the `VeridionAsset` view, which adds its SAP functional
location, OPC UA tag path, lifecycle status, criticality and commissioning year. The same
physical equipment is a separate `CogniteEquipment` node (17 for Line 3), as in SAP PM.

**Duplicate to be aware of:** Reactor R-301 exists twice. `asset_reactor_r301` is the live one;
`asset_reactor_r301_dcs_legacy` is the decommissioned pre-migration DCS representation, kept
because old historian series still attach to it. Both carry the SAP functional location
`CV-P-L3-R301`. A lookup that matches on functional location alone can return either.

This is fixture data maintained by Tech (Data Engineer, Data Scientist, Solutions Architect) — not
a claim any persona makes, but the hierarchy every other CDM resource links back to via `assets`.

Full text: `mock-cdf-project/modules/veridion_line3_oee/data_modeling/assets.node.yaml` (also `equipment.node.yaml`)

## Where this fits

- [[veridion-line3-oee-tech]] — Tech's own page; Tech owns and maintains this CDF project.
- [[veridion-line3-oee-cdf-timeseries]], [[veridion-line3-oee-cdf-activities]],
  [[veridion-line3-oee-cdf-files]] — the other CDM resource types in this same mock project, all
  linked back to these assets.
- [[veridion-line3-oee-cdf-model-and-pipelines]] — the custom views and the ingestion that populate these nodes.
- This is **not** a deployed CDF tenant — see `mock-cdf-project/README.md`. It exists so every
  `externalId` the business use case, PRD, and ADR reference resolves to something real.

---
type: source
title: "Veridion Line 3 OEE — CDF time series (mock-cdf-project)"
tags: [veridion-line3-oee, tech, cdf, cdm, timeseries, oee]
authors: [Tech/Architecture]
url: null
raw: mock-cdf-project/modules/veridion_line3_oee/data_modeling/timeseries.node.yaml
ingested: 2026-10-04
created: 2026-10-04
updated: 2026-10-04
---

# Veridion Line 3 OEE — CDF time series (mock-cdf-project)

The six `CogniteTimeSeries` node instances behind Line 3's OEE: the composite
(`ts_line3_oee_pct`) and its three components (`ts_line3_availability_pct`,
`ts_line3_performance_pct`, `ts_line3_quality_pct`), plus two feeder series
(`ts_line3_output_rate_kg_per_hr` on the extruder, `ts_reactor_r301_temperature_degc` on the
reactor). Each links back to its asset via the `assets` relation. Data points themselves are
not included — this is a static fixture, not a running time series store; only the series
definitions exist, which is enough to make every `externalId` the ADR and PRD reference
resolvable and checkable.

Full text: `mock-cdf-project/modules/veridion_line3_oee/data_modeling/timeseries.node.yaml`

## Where this fits

- [[veridion-line3-oee-tech]] — Tech's "OEE snapshot" and "OEE trend" tools query exactly these
  series; Tech owns and maintains this CDF project.
- [[veridion-line3-oee-product]] — the PRD's three extractors (OPC UA, SAP, DB) each feed one of
  these series or their inputs; Product scopes what's queryable, not how the data gets here.
- [[veridion-line3-oee-cdf-assets]] — the asset hierarchy these series are linked to.

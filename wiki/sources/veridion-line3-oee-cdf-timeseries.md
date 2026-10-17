---
type: source
title: "Veridion Line 3 OEE — CDF time series (mock-cdf-project)"
tags: [veridion-line3-oee, tech, cdf, cdm, timeseries, oee]
authors: [Tech/Architecture]
url: null
raw: mock-cdf-project/modules/veridion_line3_oee/data_modeling/timeseries.node.yaml
ingested: 2026-10-16
created: 2026-10-04
updated: 2026-10-16
---

# Veridion Line 3 OEE — CDF time series (mock-cdf-project)

The numbers for Production Line 3's OEE in the fake plant data. The composite is how well the
line ran. The three components are time up, speed, and good output. There are also 30 days of
datapoints, with the flaws a real plant has.

21 `CogniteTimeSeries` node instances. The six the ADR and PRD cite are unchanged: the composite
(`ts_line3_oee_pct`) and its three components (`ts_line3_availability_pct`,
`ts_line3_performance_pct`, `ts_line3_quality_pct`), plus `ts_line3_output_rate_kg_per_hr`
(extruder) and `ts_reactor_r301_temperature_degc` (reactor). Added around them: nine more Line 3
process signals (pressure, agitator current, FV-301 position, coolant flow, screw speed, motor
load, melt temperature, die pressure, and a redundant temperature in degF), two MES hourly count
series (good and reject kg), and four **legacy MES OEE** series (Line 3 plus Lines 1, 2 and 4).
Each carries its source system, SAP/OPC UA identifier, calculation method and a plain-language
`knownIssues` note through the `VeridionTimeSeries` view.

**Datapoints** are in `mock-cdf-project/modules/veridion_line3_oee/timeseries/`: 2,880 rows at 15
minutes for the process signals and 720 hourly rows for OEE and counts, 2026-09-15 to
2026-10-14 UTC. The OEE series are computed from the other series and the downtime records by the
SOP calculation, so OEE = Availability x Performance x Quality in every row.

Things a reader must not trip over:

- **Two OEE numbers.** `ts_line3_oee_pct` follows the SOP (3,800 kg/h ideal rate; planned downtime
  excluded). `ts_line3_oee_pct_mes_legacy` is what supervisors see today (4,200 kg/h; planned downtime
  counted as loss). Over the window they average about 85 % and 76 %. Neither is wrong.
- **A gap is not a zero.** The OPC UA extractor lost 2026-10-03 02:10 to 05:50 UTC; those hours have no OEE.
- **A frozen sensor** (PT-301 pressure flat for six hours on 10-08), **a unit mismatch**
  (TT-301B in degF), and **one bad reading** (melt temperature 9999.0 on 09-24).
- **Unlogged stops.** Ten micro-stops (3 to 8 minutes) have no SAP record and show only as output-rate dips.

Full list with locations: `mock-cdf-project/README.md`, "Known data characteristics".

Full text: `mock-cdf-project/modules/veridion_line3_oee/data_modeling/timeseries.node.yaml`

## Where this fits

- [[veridion-line3-oee-tech]] — Tech's "OEE snapshot" and "OEE trend" tools query exactly these
  series; Tech owns and maintains this CDF project.
- [[veridion-line3-oee-product]] — the PRD's three extractors (OPC UA, SAP, DB) each feed one of
  these series or their inputs; Product scopes what's queryable, not how the data gets here.
- [[veridion-line3-oee-cdf-assets]] — the asset hierarchy these series are linked to.
- [[veridion-line3-oee-cdf-activities]] — the downtime records that drive Availability.
- [[veridion-line3-oee-cdf-model-and-pipelines]] — how the series are produced and who may read them.

# Mock CDF project — Veridion Chemicals

**What these files are:** fake plant data and a fake CDF project setup for the Calder Valley plant,
so the engagement documents can name real assets, time series and downtime records. The focus is
Production Line 3 (`asset_line3`): Reactor R-301, then Extruder EX-302, in the Polymer Production
Unit. Nothing here is deployed.

This is a **fictional, static** Cognite Data Fusion project. It exists to ground the
`veridion-line3-oee` engagement (see `../docs/engagements/veridion-line3-oee/`) so that:

- every `externalId` the business use case, PRD and ADR cite resolves to something that exists here
- the ADR's "no invented `externalId`" rule is checkable
- OEE (Availability x Performance x Quality) has real, decomposable series, downtime records and
  datapoints behind it, including the messy parts a real project has

It is **not** a deployed CDF tenant. There is no cluster, project or credentials, and nothing here is
meant to run. The files follow Cognite Toolkit conventions (`space` / `externalId` per node,
`sources: [{ source: {space, externalId, version, type: view}, properties }]`, one module per concern)
but have **not** been run through `cdf build` or `cdf deploy`; see "Known limitations" below.

## Layout

```
mock-cdf-project/
├── config.dev.yaml                              fictional environment, four modules, placeholder variables
├── fixtures/generate_datapoints.py              regenerates the datapoint CSVs (deterministic)
└── modules/
    ├── veridion_platform/                       data sets and access groups
    │   ├── data_sets/veridion.DataSet.yaml      4 data sets: OPC UA, SAP PM, MES, derived OEE
    │   └── auth/*.Group.yaml                    4 groups: oee_readers (read only), extractors, pipeline_runner, data_engineers
    ├── veridion_oee_model/data_modeling/        the custom data model, schema space sp_veridion_dm
    │   ├── containers/                          4 containers (asset, downtime, time series, document extensions)
    │   ├── views/                               4 views implementing CogniteAsset / Activity / TimeSeries / File
    │   └── VeridionOEE.DataModel.yaml           the data model
    ├── veridion_line3_oee/                      the instances, in space sp_veridion_demo
    │   ├── data_modeling/                       source systems, asset classes, equipment types,
    │   │                                        assets, equipment, time series, activities, files
    │   └── timeseries/*.csv                     30 days of datapoints (see below)
    └── veridion_ingestion/                      how the data gets in
        ├── extraction_pipelines/                OPC UA, SAP PM and DB (MES) extractor pipelines and configs
        ├── raw/                                 RAW database, tables and sample rows (SAP notifications etc.)
        ├── transformations/                     SAP notifications -> downtime activities (SQL)
        ├── functions/fn_line3_oee_calc/         the OEE calculation (oee.py), CDF Function handler
        └── workflows/                           hourly workflow: load activities, then compute OEE
```

## Size

| Resource | Count |
| --- | --- |
| Assets (functional locations) | 40, five levels deep (plant, area, line, unit, component) |
| Equipment | 17 (Line 3 reactor and extruder trains) |
| Time series | 21 (5 OEE-family, 11 process, 2 MES counts, 3 other-line OEE) |
| Activities (downtime records) | 11 over 30 days |
| Files (metadata only) | 10 |
| Datapoints | 2,880 process rows (15 min) and 720 hourly rows, 2026-09-15 to 2026-10-14 UTC |

Lines 1, 2 and 4 are reactor and extruder only, with a legacy-MES OEE series each. Line 3 is the
fully described line.

## How the data model is built

All instances use the Core Data Model (CDM) views (`CogniteAsset`, `CogniteEquipment`,
`CogniteTimeSeries`, `CogniteActivity`, `CogniteFile`, `CogniteSourceSystem`, `CogniteAssetClass`,
`CogniteEquipmentType`) and are also populated through four Veridion views that extend CDM:

| View | Adds |
| --- | --- |
| `VeridionAsset` | SAP functional location, OPC UA tag path, lifecycle status, criticality, commissioning year |
| `VeridionDowntimeActivity` | downtime category, loss class (planned or unplanned), SAP notification id, cause code, shift |
| `VeridionTimeSeries` | signal role, calculation method, sampling interval, definition basis, known issues, definition document |
| `VeridionDocument` | document type, revision, status, the revision it supersedes |

The real core model's equivalent of a legacy "event" is **`CogniteActivity`**; there is no
`CogniteEvent` view. Schema lives in `sp_veridion_dm` and instances in `sp_veridion_demo`, so write
access to the model and read access to the data can be granted separately. Every instance stays in
the one space the ADR names; the schema space contains no instances. `gp_veridion_oee_readers` has
read access only, which is the ADR's "no write capability" decision enforced in CDF as well.

## The engagement example: OEE for Production Line 3

OEE = Availability x Performance x Quality, per clock hour, as the OEE Calculation SOP (rev B,
`file_line3_oee_calculation_sop`) defines it:

- `ts_line3_availability_pct`: run time over planned time. Planned downtime (changeovers, planned
  maintenance) is removed from planned time. Unplanned downtime is loss.
- `ts_line3_performance_pct`: produced kg over (3,800 kg/h ideal rate x run time).
- `ts_line3_quality_pct`: good kg over (good + reject kg), from MES counts.
- `ts_line3_oee_pct`: the product of the three.

The OEE series are **computed**, not invented: `fixtures/generate_datapoints.py` simulates process
signals, MES counts and downtime windows, then calls the same `oee.py` the CDF Function uses.
`oee = availability x performance x quality` holds in every row. Over the window the SOP OEE
averages about 85 %, and the legacy MES OEE about 76 %.

## Known data characteristics (deliberate)

These are what a real plant project looks like. They are in the data so that questions about
Line 3 hit real ambiguity instead of a clean story.

| # | Characteristic | Where it lives | What it affects |
| --- | --- | --- | --- |
| 1 | **Two OEE definitions.** The SOP counts 3,800 kg/h ideal and excludes planned downtime. The legacy MES report the supervisors read uses 4,200 kg/h and counts planned downtime as loss. | `ts_line3_oee_pct` vs `ts_line3_oee_pct_mes_legacy`; `file_line3_oee_calculation_sop` (rev B), `..._rev_a` (superseded), `file_mes_legacy_oee_report_spec`, `file_moc_2025_014_line3_ideal_rate` | The two numbers differ by about 9 points on average with nothing wrong in either. Which one counts as "the OEE" is a Business decision (`wiki/SCHEMA.md`); this project holds both. Lines 1, 2 and 4 only have the legacy definition, so they are not comparable with Line 3. |
| 2 | **A stop logged twice.** On 2026-09-30 the operator and maintenance each raised a notification for the same valve fault. | `activity_line3_unplanned_stop_valve_fault` and `..._maint_notification` | Adding the two durations double-counts. `oee.py` merges overlapping windows. |
| 3 | **A stop with no end time.** SAP notification for the 2026-10-14 pelletizer jam was never closed. | `activity_line3_unplanned_stop_pelletizer_20261014` | Availability ignores it. The lost output shows up as Performance loss for that hour (Availability 100 %, Performance 53 %). |
| 4 | **Stops that are never logged.** Ten micro-stops of 3 to 8 minutes appear only as output-rate dips. | `ts_line3_output_rate_kg_per_hr` | They are Performance loss with no activity to point at. |
| 5 | **A data gap, not a zero.** The OPC UA extractor lost data 2026-10-03 02:10 to 05:50 UTC. | `line3_process_15min.csv` (blank cells), hours 02 to 05 have no OEE | A tool that treats "no value" as 0 reports a false outage. |
| 6 | **A frozen sensor.** PT-301 pressure reads a flat 14.2 bar for six hours on 2026-10-08. | `ts_reactor_r301_pressure_bar` | Looks healthy, is not live. |
| 7 | **A unit mismatch.** TT-301B is published in degF next to a degC twin; the `unit` relation is not mapped. | `ts_reactor_r301_temperature_b_degf` | Anything that assumes degC misreads it by about 180. |
| 8 | **A bad reading.** One melt-temperature value of 9999.0. | `ts_extruder_ex302_melt_temperature_degc` at 2026-09-24 11:15 UTC | Skews any min, max or average. |
| 9 | **A duplicate asset.** R-301 exists as `asset_reactor_r301` and as the decommissioned `asset_reactor_r301_dcs_legacy` with the same SAP functional location. | `assets.node.yaml`, `raw/asset_tag_map.csv`, `raw/pm_functional_locations.csv` | Joining on functional location fans out unless filtered on status. The transformation filters on `ACTIVE`. |
| 10 | **A repeat failure with a visible precursor.** FV-301 stuck on 09-30 and again on 10-09. In the hours before each, its position reads a flat 55.0 and reactor temperature drifts up. | `activity_line3_unplanned_stop_valve_fault`, `..._valve_sticking_20261009`, `ts_reactor_r301_feed_valve_fv301_position_pct`, `ts_reactor_r301_temperature_degc` | The draft RCA (`file_rca_2026_09_30_fv301_valve_fault`) was still open when it recurred. The die-pressure trip has its own precursor (rising die pressure); the pump trip and the pelletizer jam have none, so none of this is a general predictor. |
| 11 | **Local times in SAP.** SAP stores date and time with no zone. | `raw/pm_notifications.csv`, `transformations/sap_notifications_to_activities.sql` | Converted from Europe/London (UTC+1 for this window). Wrong by an hour if that assumption fails. |
| 12 | **No work-order resource.** SAP work orders exist only in SAP. CDF holds notifications as activities and nothing that creates or tracks a work order. | by absence; `ep_veridion_sap_pm` is inbound only | Matches the ADR: there is no resource, schema or threshold to build the automatic work order on. |

## Regenerating the datapoints

```
python3 mock-cdf-project/fixtures/generate_datapoints.py
```

Stdlib only, fixed seed, reads `raw/pm_notifications.csv` for the downtime windows. Re-running
reproduces the CSVs byte for byte. If you change a downtime record, change the matching SAP row in
`raw/pm_notifications.csv` and the activity in `activities.node.yaml` together; the generator reads
the CSV, not the YAML.

## What has been checked

| Check | Result |
| --- | --- |
| `cdf build` (Toolkit 0.9.6, offline) | 169 resources of 16 types, **0 errors**. 147 warnings, all "unverified reference" to Core Data Model views, which cannot be checked without a CDF connection. Building found and fixed: a function and workflow with no data set, extraction-pipeline configs in the wrong shape, a space file Toolkit silently ignored, a too-long space description, and two wrong field or capability names. |
| Referential integrity | Every `sp_veridion_demo` relation resolves; one asset root; every series has datapoints and every datapoint column has a series. |
| Datapoint generator | Reproducible byte for byte; OEE = Availability x Performance x Quality in every row. |
| OEE function | `functions/fn_line3_oee_calc/test_handler.py` runs `handler.handle()` against a fake client over the CSVs and reproduces 748 OEE datapoints with 0 mismatches. It shares `oee.py` with the generator, so it checks the handler's plumbing, not the formula independently. |
| Handler against the SDK | Imports and call signatures match `cognite-sdk` 8.22. |
| Transformation SQL | Parses as Spark SQL (sqlglot). Not executed, so CDF-specific functions such as `node_reference` are unchecked. |

## Known limitations

- **Not deployed.** There is no CDF project to deploy to. The offline build is the strongest check available.
- **Datapoints are not loaded by `cdf build`.** Toolkit 0.9.6 builds nothing from `timeseries/*.csv`;
  datapoints would be uploaded as a separate step. The CSV shape (`timestamp` plus one column per
  series `externalId`) is this project's own convention.
- **Extractor configs are illustrative.** They are carried as pipeline config in the right Toolkit shape
  but were not validated against the OPC UA, SAP or DB extractors' own schemas.
- **The function ran only against a fake client**, not the CDF API.
- **No transformation for assets or equipment.** Only SAP notifications have one. The asset and equipment
  hierarchy is fixture data, although the PRD says the SAP extractor enriches asset records.
- **The `unit` relation is unmapped.** `sourceUnit` is set on every series; the relation to the
  CDM unit catalogue is not, so no unit externalIds are asserted.
- **One simplification of SAP.** `raw/pm_notifications.csv` has the handful of QMEL-style fields the
  transformation uses, not the full notification record.
- **Read access is wider than the ADR's wording.** The lookup's group reads `sp_veridion_dm` and `cdf_cdm`
  (definitions, no plant data) as well as `sp_veridion_demo`, because views live there.
- **No 3D, no annotations, no relationships beyond direct relations.** Not needed for this engagement.

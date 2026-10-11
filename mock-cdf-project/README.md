# Mock CDF project — Veridion Chemicals

This is a **fictional, static** Cognite Data Fusion project. It exists only to ground the
`veridion-line3-oee` engagement (see `../docs/engagements/veridion-line3-oee/`) in real Core Data Model (CDM)
shapes, so that:

- every `externalId` referenced by the business use case and the ADR resolves to something
  that actually exists here, instead of being invented in prose
- the "no invented `externalId`" constraint in the ADR is checkable, not just asserted
- the OEE metric (Availability x Performance x Quality) has real, decomposable time series
  and activity instances behind it, not a single invented number

It is **not** a deployed CDF tenant. There is no cluster, no project, no credentials, and
nothing here is meant to run. The resource files follow the real
[Cognite Toolkit](https://docs.cognite.com/cdf/deploy/cdf_toolkit) node-instance schema —
`space` / `externalId` per node, `sources: [{ source: {space, externalId, version, type: view},
properties: {...} }]`, `*.node.yaml` file naming, placed under `data_modeling/` — so it reads
as a real module to anyone who has built one. It is still not meant to be deployed with
`cdf deploy`: there's no backing CDF project for `config.dev.yaml` to point at.

All resources use the Core Data Model (CDM) views — `CogniteAsset`, `CogniteTimeSeries`,
`CogniteActivity`, `CogniteFile` — not the legacy `/assets`, `/timeseries`, `/events` APIs.
Note that the real core model's equivalent of a legacy "event" is **`CogniteActivity`**;
there is no `CogniteEvent` view.

## Layout

```
mock-cdf-project/
├── config.dev.yaml                              fictional project/cluster name
└── modules/veridion_line3_oee/
    └── data_modeling/
        ├── 01_space.yaml                         the one space used for this demo
        ├── assets.node.yaml                      plant -> polymer unit -> Line 3 -> reactor/extruder
        ├── timeseries.node.yaml                  OEE + its 3 components, output rate, reactor temp
        ├── activities.node.yaml                  a planned changeover, an unplanned valve-fault stop
        └── files.node.yaml                       Line 3's OEE calculation SOP
```

## The engagement example: OEE for Production Line 3

**Veridion Chemicals**, Calder Valley Plant, runs **Production Line 3** (Reactor R-301 →
Extruder EX-302) in its Polymer Production Unit. OEE = Availability x Performance x Quality:

- `ts_line3_oee_pct` — the composite metric.
- `ts_line3_availability_pct` — driven down by downtime activities on `asset_line3`
  (`activity_line3_changeover` is planned and excluded from loss; `activity_line3_unplanned_stop_valve_fault`
  is unplanned and counted as loss).
- `ts_line3_performance_pct` — driven by `ts_line3_output_rate_kg_per_hr` on `asset_extruder_ex302`
  versus theoretical max throughput.
- `ts_line3_quality_pct` — good units over total units produced.

"What's driving the OEE loss on Line 3?" is answerable by decomposing the composite into its
three components and cross-referencing the activity history — all of it real, fixture-backed
data, not invented numbers.

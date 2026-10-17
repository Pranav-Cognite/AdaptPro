---
type: source
title: "Veridion Line 3 OEE — CDF data model and ingestion (mock-cdf-project)"
tags: [veridion-line3-oee, tech, cdf, data-model, ingestion, access]
authors: [Tech/Architecture]
url: null
raw: mock-cdf-project/modules/
ingested: 2026-10-16
created: 2026-10-16
updated: 2026-10-16
---

# Veridion Line 3 OEE — CDF data model and ingestion (mock-cdf-project)

How the fake plant data is shaped, how it gets into CDF, and who may touch it. This is the
plumbing behind the OEE numbers, described as the project is configured. None of it is deployed.

**Data model** (`veridion_oee_model`, schema space `sp_veridion_dm`): four views extending the Core
Data Model — `VeridionAsset`, `VeridionDowntimeActivity`, `VeridionTimeSeries`, `VeridionDocument` —
collected in the `VeridionOEE` data model. Schema is in its own space; every instance is in
`sp_veridion_demo`, the single space the ADR names.

**Ingestion** (`veridion_ingestion`): three extractors feed it, matching the PRD. The OPC UA
extractor writes the process series. The SAP extractor reads maintenance notifications into RAW
(one way, SAP to CDF; SAP work orders are not extracted). The DB extractor reads hourly good and
reject counts from MES. A SQL transformation turns SAP notifications into downtime activities,
converting SAP's zone-less local times to UTC. A CDF Function (`fn_line3_oee_calc`, with the
calculation in `oee.py`) computes OEE per the SOP, and an hourly workflow runs both.

**Access** (`veridion_platform`): four data sets and four groups. `gp_veridion_oee_readers` can
only read — this is how the ADR's "no write capability" decision is also enforced in CDF. Extractors,
pipeline runner and data engineers each get only the writes they need; only data engineers can
write the schema space.

**Where it differs from the documents:** (1) The ADR says reads come only from `sp_veridion_demo`. The
lookup's read access also covers the schema space and `cdf_cdm`, because views live there; those spaces
hold no plant data. (2) The PRD says the DB extractor feeds `ts_line3_quality_pct`; here it feeds the
hourly good and reject counts, and the function derives quality. (3) The PRD says the SAP extractor
enriches asset records; here only notifications have a transformation, and the asset and equipment
hierarchy is fixture data with no transformation behind it.

**Not in the data:** no work-order resource, no OEE threshold or alert policy. That absence is what
the ADR rests on.

**Limits:** the project builds offline with Toolkit 0.9.6 with no errors, but has not been deployed. The
SQL parses but has not run, extractor configs are illustrative, and the function was exercised only against a
fake client. `mock-cdf-project/README.md` lists them.

Full text: `mock-cdf-project/modules/veridion_oee_model/`, `veridion_ingestion/`, `veridion_platform/`

## Where this fits

- [[veridion-line3-oee-tech]] — Tech owns this plumbing and the permissions boundary behind the read-only decision.
- [[veridion-line3-oee-product]] — the PRD's extractor table describes the same three feeds.
- [[veridion-line3-oee-cdf-timeseries]], [[veridion-line3-oee-cdf-activities]],
  [[veridion-line3-oee-cdf-assets]], [[veridion-line3-oee-cdf-files]] — the instances this model describes.

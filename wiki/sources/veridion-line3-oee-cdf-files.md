---
type: source
title: "Veridion Line 3 OEE — CDF files (mock-cdf-project)"
tags: [veridion-line3-oee, tech, cdf, cdm, files]
authors: [Tech/Architecture]
url: null
raw: mock-cdf-project/modules/veridion_line3_oee/data_modeling/files.node.yaml
ingested: 2026-10-16
created: 2026-10-04
updated: 2026-10-16
---

# Veridion Line 3 OEE — CDF files (mock-cdf-project)

The written procedures and records around Production Line 3's OEE, stored as file metadata in the
fake plant data. They define the formula and the history of how it changed. They are not the
customer promise.

10 `CogniteFile` node instances, metadata only (no file content). `file_line3_oee_calculation_sop`,
the SOP defining how Availability, Performance and Quality are calculated for Line 3 (linked to
`asset_line3`), is unchanged and is now marked rev B, effective. Around it:

- `file_line3_oee_calculation_sop_rev_a` — the superseded rev A (4,200 kg/h ideal rate).
- `file_moc_2025_014_line3_ideal_rate` — the change record moving the ideal rate to 3,800 kg/h. It
  records that the legacy MES report was not in the change's scope.
- `file_mes_legacy_oee_report_spec` — the legacy shift-end report supervisors read today.
- Two P&IDs (reactor and extruder sections), the FV-301 vendor manual, the EX-302 screen pack
  change procedure, the SAP downtime cause code guide, and a **draft** RCA for the 09-30 valve fault.

Each file is also classed through `VeridionDocument` (type, revision, status, what it supersedes).
The cause code guide does not say who reconciles a stop logged by both Production and Maintenance.

Full text: `mock-cdf-project/modules/veridion_line3_oee/data_modeling/files.node.yaml`

## Where this fits

- [[veridion-line3-oee-tech]] — Tech owns and maintains this CDF project; these files exist so a
  citation to "the OEE calculation SOP" (or to why two OEE numbers exist) resolves to something real.
- [[veridion-line3-oee-cdf-assets]] — the assets these files are linked to.
- [[veridion-line3-oee-cdf-timeseries]] — the series whose definition each SOP revision governs.

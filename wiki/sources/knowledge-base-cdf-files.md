---
type: source
title: "OEE Chat Assistant — CDF files (mock-cdf-project)"
tags: [knowledge-base, tech, cdf, cdm, files]
authors: [Tech/Architecture]
url: null
raw: mock-cdf-project/modules/knowledge_base/data_modeling/files.node.yaml
ingested: 2026-10-04
created: 2026-10-04
updated: 2026-10-04
---

# OEE Chat Assistant — CDF files (mock-cdf-project)

One `CogniteFile` node instance: `file_line3_oee_calculation_sop`, the standard operating
procedure defining how Availability, Performance, and Quality are calculated for Line 3, linked
to `asset_line3`. File content itself is not included — this is a static fixture, not a running
File service — only the metadata needed for citation exists.

Full text: `mock-cdf-project/modules/knowledge_base/data_modeling/files.node.yaml`

## Where this fits

- [[knowledge-base-tech]] — Tech owns and maintains this CDF project; this file exists so a
  citation to "the OEE calculation SOP" resolves to something real rather than being asserted.
- [[knowledge-base-cdf-assets]] — the asset (`asset_line3`) this file is linked to.

---
type: source
title: "OEE Chat Assistant — PRD (OEE for Line 3)"
tags: [knowledge-base, product, oee, prd]
authors: [Product]
url: null
raw: docs/epics/01-knowledge-base/prd.md
ingested: 2026-10-03
created: 2026-10-03
updated: 2026-10-03
---

# OEE Chat Assistant — PRD (OEE for Line 3)

The product-scoping artifact for the `knowledge-base` epic. Defines the data architecture —
Cognite OPC UA Extractor (process time series), Cognite SAP Extractor (equipment master +
downtime/maintenance activities), and Cognite DB Extractor (quality/reject data) — feeding the
OEE composite and its three components for Production Line 3. Scopes the same three
read-only query templates as the ADR, and explicitly puts "automatically generate a
corrective work order" and any OEE threshold/alerting policy out of scope for v1.

Full text: `docs/epics/01-knowledge-base/prd.md`

## Where this fits

- [[knowledge-base-product]] — the product persona page drawn from this source.
- [[knowledge-base-conflicts]] — this source scopes the same read-only templates as
  [[knowledge-base-adr]], so it does not introduce a new conflict with Tech — it confirms
  Tech's position against Business's promise in [[knowledge-base-business-use-case]].

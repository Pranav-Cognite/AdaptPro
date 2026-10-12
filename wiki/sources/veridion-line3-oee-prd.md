---
type: source
title: "Veridion Line 3 OEE — PRD (OEE for Line 3)"
tags: [veridion-line3-oee, product, oee, prd]
authors: [Product]
url: null
raw: docs/engagements/veridion-line3-oee/prd.md
ingested: 2026-10-03
created: 2026-10-03
updated: 2026-10-11
---

# Veridion Line 3 OEE — PRD (OEE for Line 3)

Summary of Product's source document. It scopes a read-only lookup of Production Line 3's OEE.
Line 3 is the polymer line at Calder Valley. The automatic work order is out of this document.

The Product scoping artifact for `veridion-line3-oee`. Defines the data architecture —
Cognite OPC UA Extractor (process time series), Cognite SAP Extractor (equipment master +
downtime/maintenance activities), and Cognite DB Extractor (quality/reject data) — feeding the
OEE composite and its three components for Production Line 3. Scopes the same three
read-only query templates as the ADR, and explicitly puts "automatically generate a
corrective work order" and any OEE threshold/alerting policy out of scope for v1.

Full text: `docs/engagements/veridion-line3-oee/prd.md`

## Where this fits

- [[veridion-line3-oee-product]] — the product persona page drawn from this source.
- [[veridion-line3-oee-conflicts]] — this source scopes the same read-only templates as
  [[veridion-line3-oee-adr]], so it does not introduce a new conflict with Tech — it confirms
  Tech's position against Business's promise in [[veridion-line3-oee-business-use-case]].

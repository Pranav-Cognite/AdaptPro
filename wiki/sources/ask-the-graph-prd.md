---
type: source
title: "Ask the Graph — PRD (OEE for Line 3)"
tags: [ask-the-graph, product, oee, prd]
authors: [Product]
url: null
raw: docs/epics/01-ask-the-graph/prd.md
ingested: 2026-10-03
created: 2026-10-03
updated: 2026-10-03
---

# Ask the Graph — PRD (OEE for Line 3)

The product-scoping artifact for the `ask-the-graph` epic. Defines the data architecture —
Cognite OPC UA Extractor (process time series), Cognite SAP Extractor (equipment master +
downtime/maintenance activities), and Cognite DB Extractor (quality/reject data) — feeding the
OEE composite and its three components for Production Line 3. Scopes the same three
read-only query templates as the ADR, and explicitly puts "automatically generate a
corrective work order" and any OEE threshold/alerting policy out of scope for v1.

Full text: `docs/epics/01-ask-the-graph/prd.md`

## Where this fits

- [[ask-the-graph-product]] — the product persona page drawn from this source.
- [[ask-the-graph-conflicts]] — this source scopes the same read-only templates as
  [[ask-the-graph-adr]], so it does not introduce a new conflict with Tech — it confirms
  Tech's position against Business's promise in [[ask-the-graph-business-use-case]].

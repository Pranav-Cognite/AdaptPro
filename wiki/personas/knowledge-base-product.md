---
type: persona
title: "OEE Chat Assistant — Product view"
persona: product
epic: knowledge-base
status: current
tags: [knowledge-base, product, oee]
sources: [knowledge-base-prd]
created: 2026-10-02
updated: 2026-10-03
---

# OEE Chat Assistant — Product view

This is Product's reading of the `knowledge-base` epic, drawn only from [[knowledge-base-prd]].
It does not reflect what Business has promised the customer or how Tech phrases its
constraints — see [[knowledge-base-conflicts]] for where this view disagrees with the other
personas.

## How the data gets into CDF

Three Cognite extractors feed the OEE data this product queries:

- **OPC UA Extractor** — reactor temperature and Line 3 output rate, straight from plant
  PLCs/DCS. Feeds the Performance component.
- **SAP Extractor** — equipment master data and downtime/maintenance records from SAP PM.
  Feeds the Availability component (`CogniteActivity` instances).
- **DB Extractor** — good/reject counts from the plant MES/quality database. Feeds the
  Quality component.

## What Product has scoped for v1

The same three read-only query templates Tech has committed to: OEE snapshot, OEE trend, and
downtime history — all with citations. Product scoped this deliberately read-only.

## What Product has explicitly scoped out

- **Any write action** — creating or triggering a SAP work order, or any other write, from
  the chat. The SAP Extractor is inbound-only (SAP → CDF); there is no path back out scoped
  here.
- **Any OEE threshold/alerting policy** — nothing defines what "OEE dropped below target"
  means yet, which is a prerequisite for any future write capability Business might want.

## Open conflicts involving this view

See [[knowledge-base-conflicts]] — Product's read-only scope here **matches** Tech's ADR, not
Business's promise. The auto-work-order promise in [[knowledge-base-business]] is therefore in
conflict with both Product and Tech, not just Tech alone.

See [[knowledge-base-briefing-product]] for Product's homework on Business and Tech before a
cross-functional meeting on this epic.

See [[product-glossary]] for the vocabulary used above, written for Business and Tech.

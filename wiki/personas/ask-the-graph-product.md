---
type: persona
title: "Ask the Graph — Product view"
persona: product
epic: ask-the-graph
status: current
tags: [ask-the-graph, product, oee]
sources: [ask-the-graph-prd]
created: 2026-10-02
updated: 2026-10-03
---

# Ask the Graph — Product view

This is Product's reading of the `ask-the-graph` epic, drawn only from [[ask-the-graph-prd]].
It does not reflect what Business has promised the customer or how Tech phrases its
constraints — see [[ask-the-graph-conflicts]] for where this view disagrees with the other
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

See [[ask-the-graph-conflicts]] — Product's read-only scope here **matches** Tech's ADR, not
Business's promise. The auto-work-order promise in [[ask-the-graph-business]] is therefore in
conflict with both Product and Tech, not just Tech alone.

See [[ask-the-graph-briefing-product]] for Product's homework on Business and Tech before a
cross-functional meeting on this epic.

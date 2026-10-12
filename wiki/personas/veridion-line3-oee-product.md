---
type: persona
title: "Veridion Line 3 OEE — Product view"
persona: product
status: current
tags: [veridion-line3-oee, product, oee]
sources: [veridion-line3-oee-prd]
created: 2026-10-02
updated: 2026-10-11
---

# Veridion Line 3 OEE — Product view

Line 3 is the polymer production line at Calder Valley (`asset_line3`): Reactor R-301, then
Extruder EX-302. This page is only what Product scoped for that line in v1: three read-only
questions. The automatic work order is not in this scope.

This is Product's reading of `veridion-line3-oee`, drawn only from [[veridion-line3-oee-prd]] — the PRD
is Product's exclusive source; Business and Tech may reference it but never own it. This page
does not reflect what Business has promised the customer or how Tech phrases its constraints —
see [[veridion-line3-oee-conflicts]] for where this view disagrees with the other personas.

## How the data gets into CDF

Three Cognite extractors feed the OEE data this product queries:

- **OPC UA Extractor** — reactor temperature and Line 3 output rate, straight from plant
  PLCs/DCS. Feeds the Performance component.
- **SAP Extractor** — equipment master data and downtime/maintenance records from SAP PM.
  Feeds the Availability component (`CogniteActivity` instances).
- **DB Extractor** — good/reject counts from the plant MES/quality database. Feeds the
  Quality component.

The actual CDM resources these extractors feed are owned and maintained by Tech — see
[[veridion-line3-oee-cdf-timeseries]] and [[veridion-line3-oee-cdf-activities]] for the specific time
series and activities this maps onto. Product scopes which questions are queryable; Tech owns
what's actually there to query.

## What Product has scoped for v1

The same three read-only query templates Tech has committed to: OEE snapshot, OEE trend, and
downtime history — all with citations. Product scoped this deliberately read-only.

## What Product has explicitly scoped out

- **Any write action** — creating or triggering a SAP work order, or any other write. The
  SAP Extractor is inbound-only (SAP → CDF); there is no path back out scoped here.
- **Any OEE threshold/alerting policy** — nothing defines what "OEE dropped below target"
  means yet, which is a prerequisite for any future write capability Business might want.

## Open conflicts involving this view

See [[veridion-line3-oee-conflicts]] — Product's read-only scope here **matches** Tech's ADR, not
Business's promise. The auto-work-order promise in [[veridion-line3-oee-business]] is therefore in
conflict with both Product and Tech, not just Tech alone.

See [[veridion-line3-oee-briefing-product]] for Product's homework on Business and Tech before a
cross-functional meeting.

See [[product-glossary]] for the vocabulary used above, written for Business and Tech.

# Wiki Index

The catalog of all pages in this wiki. Each entry: a wikilink to the page and a one-line summary. The LLM reads this first when answering queries to identify candidate pages.

Keep summaries tight — one line each. The index is engineered to be cheap to read; a fat index defeats its purpose.

When this file exceeds ~300 lines or the wiki passes ~150 pages, shard into `wiki/indexes/<type>.md` and replace this file with a directory of shards. See the `scaling-playbook.md` reference in the `llm-wiki` skill for the migration procedure.

---

## Sources

- [[knowledge-base-business-use-case]] — Business's OEE promise for Line 3: real-time OEE + auto-generated work order on drop.
- [[knowledge-base-prd]] — Product's PRD: 3 extractors (OPC UA/SAP/DB) feed OEE; same read-only scope as the ADR.
- [[knowledge-base-adr]] — ADR 001, Tech's read-only OEE tool set for Line 3; no write tool.
- [[knowledge-base-cdf-assets]] — Tech's mock CDF asset hierarchy: plant → polymer unit → Line 3 → reactor/extruder.
- [[knowledge-base-cdf-timeseries]] — Tech's mock CDF time series: OEE composite + 3 components + 2 feeder series.
- [[knowledge-base-cdf-activities]] — Tech's mock CDF activities: one planned changeover, one unplanned valve-fault stop.
- [[knowledge-base-cdf-files]] — Tech's mock CDF file: the Line 3 OEE calculation SOP.

## Entities

(populated as entity pages are created)

## Concepts

(populated as concept pages are created)

## Personas

- [[knowledge-base-business]] — Business's view: real-time OEE + auto-generated work order on drop.
- [[knowledge-base-product]] — Product's view: same read-only scope as Tech; no PRD write path.
- [[knowledge-base-tech]] — Tech's view: read-only OEE snapshot/trend/downtime tools, no write tool, cluster-bound.

## Glossaries

- [[business-glossary]] — Business's day-to-day vocabulary (OEE, GTM, renewal, plant-floor terms), for Product and Tech.
- [[product-glossary]] — Product's day-to-day vocabulary (PRD, scope, query templates), for Business and Tech.
- [[tech-glossary]] — Tech's day-to-day vocabulary (ADR, CDM types, externalId, contextualization), for Business and Product.

## Synthesis

- [[knowledge-base-conflicts]] — RED: Business's auto-work-order promise vs. Product + Tech's read-only scope.
- [[knowledge-base-briefing-product]] — worked example of a cross-persona briefing: Product's homework on Business and Tech before a meeting.

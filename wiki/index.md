# Wiki Index

**Subject of this wiki:** Production Line 3 at Calder Valley, a polymer line (Reactor R-301,
then Extruder EX-302). Business promised a live OEE number and an automatic work order when
OEE drops. Product and Tech scoped a read-only lookup. The pages below keep those three
views separate. The red conflict is the work order.

The catalog of all pages in this wiki. Each entry: a wikilink to the page and a one-line summary. The LLM reads this first when answering queries to identify candidate pages.

Keep summaries tight — one line each. The index is engineered to be cheap to read; a fat index defeats its purpose.

When this file exceeds ~300 lines or the wiki passes ~150 pages, shard into `wiki/indexes/<type>.md` and replace this file with a directory of shards. See the `scaling-playbook.md` reference in the `llm-wiki` skill for the migration procedure.

---

## Sources

- [[veridion-line3-oee-business-use-case]] — Business's Line 3 OEE promise: real-time OEE + auto-generated work order on drop.
- [[veridion-line3-oee-prd]] — Product's PRD: 3 extractors (OPC UA/SAP/DB) feed OEE; same read-only scope as the ADR.
- [[veridion-line3-oee-adr]] — ADR 001, Tech's read-only OEE capability set for Line 3; no write path.
- [[veridion-line3-oee-cdf-assets]] — Tech's mock CDF asset hierarchy: plant → polymer unit → Line 3 → reactor/extruder.
- [[veridion-line3-oee-cdf-timeseries]] — Tech's mock CDF time series: OEE composite + 3 components + 2 feeder series.
- [[veridion-line3-oee-cdf-activities]] — Tech's mock CDF activities: one planned changeover, one unplanned valve-fault stop.
- [[veridion-line3-oee-cdf-files]] — Tech's mock CDF file: the Line 3 OEE calculation SOP.

## Entities

(populated as entity pages are created)

## Concepts

(populated as concept pages are created)

## Personas

- [[veridion-line3-oee-business]] — Business's view: real-time OEE + auto-generated work order on drop.
- [[veridion-line3-oee-product]] — Product's view: same read-only scope as Tech; no write path in the PRD.
- [[veridion-line3-oee-tech]] — Tech's view: read-only OEE snapshot/trend/downtime capabilities, no write path, cluster-bound.

## Glossaries

- [[business-glossary]] — Business's day-to-day vocabulary (OEE, GTM, renewal, plant-floor terms), for Product and Tech.
- [[product-glossary]] — Product's day-to-day vocabulary (PRD, scope, query templates), for Business and Tech.
- [[tech-glossary]] — Tech's day-to-day vocabulary (ADR, CDM types, externalId, contextualization), for Business and Product.

## Synthesis

- [[veridion-line3-oee-conflicts]] — RED: Business's auto-work-order promise vs. Product + Tech's read-only scope.
- [[veridion-line3-oee-briefing-product]] — worked example of a cross-persona briefing: Product's homework on Business and Tech before a meeting.

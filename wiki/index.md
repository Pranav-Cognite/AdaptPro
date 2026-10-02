# Wiki Index

The catalog of all pages in this wiki. Each entry: a wikilink to the page and a one-line summary. The LLM reads this first when answering queries to identify candidate pages.

Keep summaries tight — one line each. The index is engineered to be cheap to read; a fat index defeats its purpose.

When this file exceeds ~300 lines or the wiki passes ~150 pages, shard into `wiki/indexes/<type>.md` and replace this file with a directory of shards. See the `scaling-playbook.md` reference in the `llm-wiki` skill for the migration procedure.

---

## Sources

- [[ask-the-graph-business-use-case]] — Business's OEE promise for Line 3: real-time OEE + auto-generated work order on drop.
- [[ask-the-graph-prd]] — Product's PRD: 3 extractors (OPC UA/SAP/DB) feed OEE; same read-only scope as the ADR.
- [[ask-the-graph-adr]] — ADR 001, Tech's read-only OEE tool set for Line 3; no write tool.

## Entities

(populated as entity pages are created)

## Concepts

(populated as concept pages are created)

## Personas

- [[ask-the-graph-business]] — Business's view: real-time OEE + auto-generated work order on drop.
- [[ask-the-graph-product]] — Product's view: same read-only scope as Tech; no PRD write path.
- [[ask-the-graph-tech]] — Tech's view: read-only OEE snapshot/trend/downtime tools, no write tool, cluster-bound.

## Synthesis

- [[ask-the-graph-conflicts]] — RED: Business's auto-work-order promise vs. Product + Tech's read-only scope.
- [[ask-the-graph-briefing-product]] — worked example of a cross-persona briefing: Product's homework on Business and Tech before a meeting.

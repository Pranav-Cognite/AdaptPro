---
type: source
title: "Ask the Graph — ADR 001 (read-only tool set)"
tags: [ask-the-graph, tech, adr, oee]
authors: [Tech/Architecture]
url: null
raw: docs/epics/01-ask-the-graph/adr.md
ingested: 2026-10-02
created: 2026-10-02
updated: 2026-10-02
---

# Ask the Graph — ADR 001 (read-only tool set)

The architecture decision record for the `ask-the-graph` epic. Registers exactly three
read-only tools (OEE snapshot, OEE trend, downtime history) against the Veridion mock CDF
project's Core Data Model instances, and explicitly **does not register a write tool**. Names
the cluster-boundary and no-invented-`externalId` constraints. Explicitly rejects a "generate
work order" tool for v1, citing the absence of any work-order resource, schema, or agreed OEE
threshold policy in the CDF project.

Full text: `docs/epics/01-ask-the-graph/adr.md`

## Where this fits

- [[ask-the-graph-tech]] — the tech persona page drawn from this source.
- [[ask-the-graph-conflicts]] — this source's "no write tool" decision is the other half of
  the epic's primary conflict with [[ask-the-graph-business-use-case]].

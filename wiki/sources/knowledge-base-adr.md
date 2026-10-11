---
type: source
title: "OEE Chat Assistant — ADR 001 (read-only tool set)"
tags: [knowledge-base, tech, adr, oee]
authors: [Tech/Architecture]
url: null
raw: docs/epics/01-knowledge-base/adr.md
ingested: 2026-10-02
created: 2026-10-02
updated: 2026-10-02
---

# OEE Chat Assistant — ADR 001 (read-only tool set)

The architecture decision record for `knowledge-base`. Registers exactly three
read-only tools (OEE snapshot, OEE trend, downtime history) against the Veridion mock CDF
project's Core Data Model instances, and explicitly **does not register a write tool**. Names
the cluster-boundary and no-invented-`externalId` constraints. Explicitly rejects a "generate
work order" tool for v1, citing the absence of any work-order resource, schema, or agreed OEE
threshold policy in the CDF project.

Full text: `docs/epics/01-knowledge-base/adr.md`

## Where this fits

- [[knowledge-base-tech]] — the tech persona page drawn from this source.
- [[knowledge-base-conflicts]] — this source's "no write tool" decision is the other half of
  the primary conflict with [[knowledge-base-business-use-case]].

---
type: source
title: "Veridion Line 3 OEE — ADR 001 (read-only tool set)"
tags: [veridion-line3-oee, tech, adr, oee]
authors: [Tech/Architecture]
url: null
raw: docs/engagements/veridion-line3-oee/adr.md
ingested: 2026-10-02
created: 2026-10-02
updated: 2026-10-11
---

# Veridion Line 3 OEE — ADR 001 (read-only tool set)

Summary of Tech's decision. For Production Line 3 (the polymer line at Calder Valley), v1 may
read OEE and downtime. It may not create a work order.

The architecture decision record for `veridion-line3-oee`. Registers exactly three
read-only tools (OEE snapshot, OEE trend, downtime history) against the Veridion mock CDF
project's Core Data Model instances, and explicitly **does not register a write tool**. Names
the cluster-boundary and no-invented-`externalId` constraints. Explicitly rejects a "generate
work order" tool for v1, citing the absence of any work-order resource, schema, or agreed OEE
threshold policy in the CDF project.

Full text: `docs/engagements/veridion-line3-oee/adr.md`

## Where this fits

- [[veridion-line3-oee-tech]] — the tech persona page drawn from this source.
- [[veridion-line3-oee-open-topics]] — this source's "no write tool" decision is the other half of
  the primary conflict with [[veridion-line3-oee-business-use-case]].

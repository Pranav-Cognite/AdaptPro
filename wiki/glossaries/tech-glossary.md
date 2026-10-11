---
type: glossary
title: "Tech glossary — for Business and Product"
persona: tech
tags: [glossary, tech, oee, cdf]
sources: [knowledge-base-adr]
created: 2026-10-03
updated: 2026-10-03
---

# Tech glossary

Terms Tech (architect/engineer) uses day-to-day. Written for Business and Product to read when
they need to understand what Tech means, not for Tech's own reference.

- **ADR (Architecture Decision Record)** — a specific technical decision, with the alternatives
  considered and rejected. `knowledge-base-adr` here. Different from a PRD: a PRD says *what*,
  an ADR says *how* and locks in a *why not*.
- **CogniteAsset / CogniteTimeSeries / CogniteActivity / CogniteFile** — the Core Data Model
  (CDM) types this project's data is stored as. `CogniteActivity` is the modern equivalent of a
  legacy "event" — there is no `CogniteEvent` type.
- **externalId / space** — every piece of data is identified by an `(space, externalId)` pair.
  "No invented `externalId`" means the agent must say "not found" rather than guess one.
- **Contextualization** — linking a raw data point (a sensor tag, a SAP record) to the
  `CogniteAsset` it belongs to, via the `assets` relation. Without this, a query template has
  nothing to traverse — see the glossary note under Data Engineering's work if more detail is
  needed.
- **Cluster boundary** — the agent only reads from the one CDF project/space defined here
  (`sp_veridion_demo`); it does not reach across projects or clusters.
- **Tool** — a specific, registered capability the agent can call (e.g. "OEE snapshot"). "No
  write tool" means literally no registered capability can create/update/delete anything — not
  a permissions setting, a missing capability.
- **Citation** — every factual claim in an answer must name the exact `(space, externalId)` it
  came from. This is an honesty guarantee, not a proof the underlying data is correct or
  complete.

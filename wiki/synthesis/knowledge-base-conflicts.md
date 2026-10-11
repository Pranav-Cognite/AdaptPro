---
type: synthesis
title: "OEE Chat Assistant — open conflicts"
tags: [knowledge-base, conflict, lint, oee]
sources: [knowledge-base-business-use-case, knowledge-base-prd, knowledge-base-adr]
created: 2026-10-02
updated: 2026-10-03
---

# OEE Chat Assistant — open conflicts

Status: **RED**. One open conflict, two personas on one side of it.

## Conflict 1 — auto-work-order promise vs. Product + Tech's read-only scope

- **Business** ([[knowledge-base-business]]): promises to "automatically generate a
  corrective work order the moment OEE drops below target."
- **Product** ([[knowledge-base-product]]): scopes the same three read-only query templates as
  Tech; explicitly puts any write action and any OEE threshold/alerting policy out of scope
  for v1.
- **Tech** ([[knowledge-base-tech]]): registers exactly three read-only tools; explicitly
  rejected a "generate work order" tool for v1 in ADR 001, because no work-order resource,
  schema, or agreed OEE threshold policy exists.
- **Owner:** unassigned.
- **Resolution options:** (a) Business removes or qualifies the auto-work-order line in
  customer-facing materials, or (b) Product and Tech take on new scope — an OEE threshold
  policy, a work-order schema, and a write tool — which is a new PRD and a new ADR, not a v1
  fix.
- **Status:** open, unsigned.

## Resolved — Product source was missing, now ingested

As of 2026-10-02, Product had no PRD, which was itself flagged as a gap (see
wiki log). As of 2026-10-03, [[knowledge-base-prd]] was ingested. It independently scoped the
same read-only boundary Tech had already committed to — so the missing-source gap closes, and
it does **not** introduce a second, separate conflict: it reinforces Conflict 1 rather than
adding a new one. Two personas now agree; one does not.

## What would turn this green

Someone needs to either resolve Conflict 1 (align the business promise with what Product and
Tech have scoped) or sign a waiver that names the gap, assigns an owner, and accepts it.
Until then, any persona asking "are we aligned?" should get: no — Business is
promising something neither Product nor Tech has scoped or built.

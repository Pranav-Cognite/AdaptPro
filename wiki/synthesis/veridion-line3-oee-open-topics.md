---
type: synthesis
title: "Veridion Line 3 OEE — open topics"
tags: [veridion-line3-oee, open-topics, lint, oee]
sources: [veridion-line3-oee-business-use-case, veridion-line3-oee-prd, veridion-line3-oee-adr, veridion-line3-oee-cdf-timeseries, veridion-line3-oee-cdf-files]
created: 2026-10-02
updated: 2026-10-17
---

# Veridion Line 3 OEE — open topics

This page lists what the three personas have not yet settled, so each persona knows what is worth
asking about. Most items are things nobody has written down yet. One is a real mismatch between a
promise and the scope, and the decision check uses that one to give a verdict.

Line 3 is the polymer production line at Calder Valley (Reactor R-301, then Extruder EX-302).
The first topic is not about how to calculate OEE (see the second topic below, which the CDF
data raised). Business promised an automatic work order when
that line's OEE drops. Product and Tech scoped a read-only lookup and will not create the
work order in v1.

Decision-check status: **RED** (used only by `check-decision-alignment`). One open mismatch, two personas on one side of it.

## Topic 1 — the auto-work-order promise and Product + Tech's read-only scope (the one recorded conflict)

- **Business** ([[veridion-line3-oee-business]]): promises to "automatically generate a
  corrective work order the moment OEE drops below target."
- **Product** ([[veridion-line3-oee-product]]): scopes the same three read-only query templates
  as Tech; explicitly puts any write action and any OEE threshold/alerting policy out of scope
  for v1.
- **Tech** ([[veridion-line3-oee-tech]]): registers exactly three read-only capabilities;
  explicitly rejected a "generate work order" path for v1 in ADR 001, because no work-order
  resource, schema, or agreed OEE threshold policy exists.
- **Owner:** unassigned.
- **Resolution options:** (a) Business removes or qualifies the auto-work-order line in
  customer-facing materials, or (b) Product and Tech take on new scope — an OEE threshold
  policy, a work-order schema, and a write path — which is a new PRD and a new ADR, not a v1
  fix.
- **Status:** open, unsigned.

## Topic 2 — which OEE number is "the" OEE? (an open question, not a conflict)

Raised by the CDF project ([[veridion-line3-oee-cdf-timeseries]], [[veridion-line3-oee-cdf-files]]),
not by any of the three persona documents. No persona has taken a position on it.

- The PRD says supervisors today read OEE from "a separate reporting tool" after each shift. The
  CDF project shows that tool is the legacy MES report: ideal rate 4,200 kg/h, and changeovers and
  planned maintenance counted as loss.
- The OEE Calculation SOP (rev B) and the v1 lookup use an ideal rate of 3,800 kg/h and exclude
  planned downtime. Over 2026-09-15 to 2026-10-14 the two average about 85 % (SOP) and 76 %
  (legacy MES) for Line 3. Neither is wrong; they are defined differently.
- So Business's "real-time OEE" may land as a number about nine points higher than the one the
  customer's supervisors already trust, with nothing in the three documents saying which one the
  promise means. Lines 1, 2 and 4 only have the legacy definition.
- **Verdict if asked today:** undetermined. Business's document does not say which definition;
  the PRD names the SOP's components but not the legacy report's; the ADR is silent.
- **Owner:** **Business**, solely. Under the wiki's decision-ownership rule (see `wiki/SCHEMA.md`, "Decision
  ownership: OEE") which OEE definition counts is Business's call; Product and Tech follow it.
- **What is needed:** Business states which definition the promise and the customer's "target" mean, and
  how the other number is labelled. Product then adds a PRD line and Tech an ADR entry to match.
- **Not counted in the RED status above** until Business's document takes a side. Until then, a proposal from
  Product or Tech to report a different definition is not aligned, because it is not theirs to choose.

## Resolved — Product source was missing, now ingested

As of 2026-10-02, Product had no PRD, which was itself flagged as a gap (see wiki log). As of
2026-10-03, [[veridion-line3-oee-prd]] was ingested. It independently scoped the same
read-only boundary Tech had already committed to — so the missing-source gap closes, and it
does **not** introduce a second, separate mismatch: it reinforces Topic 1 rather than
adding a new one. Two personas now agree; one does not.

## What would turn the decision check green

Someone needs to either resolve Topic 1 (align the business promise with what Product and
Tech have scoped) or sign a waiver that names the gap, assigns an owner, and accepts it.
Until then, any persona asking "are we aligned?" should get: no — Business is promising
something neither Product nor Tech has scoped or built.

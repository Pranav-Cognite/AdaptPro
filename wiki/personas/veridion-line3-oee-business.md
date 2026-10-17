---
type: persona
title: "Veridion Line 3 OEE — Business view"
persona: business
status: current
tags: [veridion-line3-oee, business, oee]
sources: [veridion-line3-oee-business-use-case]
created: 2026-10-02
updated: 2026-10-11
---

# Veridion Line 3 OEE — Business view

Line 3 is the polymer production line at Calder Valley (`asset_line3`): Reactor R-301, then
Extruder EX-302. This page is only what Business promised about that line. It is not what
Product scoped or what Tech will build.

This is Business's reading of `veridion-line3-oee`, drawn only from
[[veridion-line3-oee-business-use-case]] — the business use case is Business's exclusive
source; Product and Tech may reference it but never own it. This page does not reflect what
Product has scoped or what Tech has committed to build — see [[veridion-line3-oee-open-topics]]
for where this view disagrees with the other two personas.

## What Business is promising the customer

> "See real-time OEE for any line, and automatically generate a corrective work order the
> moment OEE drops below target."

This is the line used in the Veridion account conversation and the customer one-pager. It has
two parts: (1) real-time OEE visibility, grounded in plant data, and (2) **automatically
generate a corrective work order** when OEE drops below target.

## Why Business wants this

- Differentiator against competitors who only offer OEE dashboards: Veridion is buying
  visibility that leads to **action on an OEE drop**, not a slower way to see the same chart.
- "Auto-generate a work order on OEE drop" specifically came up in the Veridion renewal
  conversation and is expected to be referenced again in the Q4 business review.

## Example scenario Business expects to work

A production supervisor needs Line 3's OEE and what's driving the loss, and — if OEE has
dropped below the shift target — a corrective work order is generated automatically, without
a separate tooling chase.

## Open conflicts involving this view

See [[veridion-line3-oee-open-topics]] — the auto-work-order promise above has no backing
capability, no threshold policy, and no work-order schema in either
[[veridion-line3-oee-product]] or [[veridion-line3-oee-tech]].

See [[business-glossary]] for the vocabulary used above, written for Product and Tech.

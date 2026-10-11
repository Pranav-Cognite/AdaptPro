# Business use case — Veridion Line 3 OEE engagement

**Customer:** Veridion Chemicals, specialty polymers manufacturer, Calder Valley Plant.  
**Owner:** Business / Solutions.  
**Engagement slug:** `veridion-line3-oee`

## Customer pain (plain language)

Production supervisors at Calder Valley pull OEE (Overall Equipment Effectiveness) numbers
from a separate reporting tool, hours after a shift ends. When OEE drops, they still cannot
tell whether the loss came from downtime, slow running, or scrap — and turning that insight
into a corrective work order means jumping tools and waiting on someone else.

## What Business has committed to Veridion

> **See real-time OEE for any line, and automatically generate a corrective work order the
> moment OEE drops below target.**

This is the line Sales has used in the Veridion account conversation and in the customer
one-pager. It has two parts:

1. **Visibility** — real-time OEE, grounded in plant data in CDF.
2. **Action** — automatically generate a corrective work order when OEE drops below target.

## Example scenario Business expects

A production supervisor at Calder Valley needs:

> "What's OEE for Line 3 this shift, and what's driving the loss?"

The answer should use the plant's actual CDF data — the OEE composite and its Availability /
Performance / Quality components on `asset_line3`, plus the downtime activities behind any
Availability loss (e.g. the unplanned stop on Reactor R-301) — and cite what it used.

If OEE has dropped below the shift target, Business's commitment is that a corrective work
order follows without a separate tooling chase.

## Why this matters to the business

- Differentiator against competitors who only offer OEE dashboards: Veridion is buying
  **visibility that leads to action on an OEE drop**, not a slower way to see the same chart.
- "Automatically generate a work order on OEE drop" came up in the Veridion renewal
  conversation and is expected again in the Q4 business review.

## How this engagement is used in AdaptPro

This document is **Business's exclusive source** for the `veridion-line3-oee` knowledge base.
AdaptPro ingests it into the Business persona view so Product and Tech can query what was
actually promised — and so conflicts with PRD/ADR scope stay visible instead of getting
smoothed away.

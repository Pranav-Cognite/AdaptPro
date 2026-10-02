---
type: persona
title: "Ask the Graph — Business view"
persona: business
epic: ask-the-graph
status: current
tags: [ask-the-graph, business, oee]
sources: [ask-the-graph-business-use-case]
created: 2026-10-02
updated: 2026-10-02
---

# Ask the Graph — Business view

This is Business's reading of the `ask-the-graph` epic, drawn only from
[[ask-the-graph-business-use-case]]. It does not reflect what Product has scoped or what Tech
has committed to build — see [[ask-the-graph-conflicts]] for where this view disagrees with
the other two personas.

## What Business is promising the customer

> "See real-time OEE for any line, and automatically generate a corrective work order the
> moment OEE drops below target."

This is the line used in the Veridion account conversation and the generic one-pager shown to
prospects. It has two parts: (1) real-time OEE visibility, grounded in plant data, and (2)
**automatically generate a corrective work order** when OEE drops below target.

## Why Business wants this

- Differentiator against competitors who only offer OEE dashboards: Veridion is buying an
  assistant that acts on an OEE drop, not just a slower way to see the same chart.
- "Auto-generate a work order on OEE drop" specifically came up in the Veridion renewal
  conversation and is expected to be referenced again in the Q4 business review.

## Example scenario Business expects to work

A production supervisor asks about Line 3's OEE and what's driving the loss, and — if OEE has
dropped below the shift target — a corrective work order is generated automatically, without
anyone leaving the chat.

## Open conflicts involving this view

See [[ask-the-graph-conflicts]] — the auto-work-order promise above has no backing tool, no
threshold policy, and no work-order schema in either [[ask-the-graph-product]] or
[[ask-the-graph-tech]].

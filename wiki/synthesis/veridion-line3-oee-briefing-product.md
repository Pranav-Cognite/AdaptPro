---
type: synthesis
title: "Veridion Line 3 OEE — Product's briefing on Business and Tech"
tags: [veridion-line3-oee, briefing, oee]
sources: [veridion-line3-oee-business-use-case, veridion-line3-oee-prd, veridion-line3-oee-adr]
created: 2026-10-03
updated: 2026-10-03
---

# Veridion Line 3 OEE — Product's briefing on Business and Tech

Generated for: **Product**, before a cross-functional meeting on `veridion-line3-oee`. Reads
[[veridion-line3-oee-product]], [[veridion-line3-oee-business]], [[veridion-line3-oee-tech]], and
[[veridion-line3-oee-conflicts]].

## What Business is telling the customer that you should know

Business has promised Veridion: "see real-time OEE for any line, and **automatically generate
a corrective work order** the moment OEE drops below target." You scoped the first half (real
-time OEE, via the three read-only templates) but not the second half. If you walk in only
knowing your own PRD, you will be surprised that the customer already expects the work-order
part to exist.

## Where your own commitments have no source in the other two pages

Nothing — your PRD's read-only scope is independently confirmed by Tech's ADR. You and Tech
agree with each other; neither of you agrees with what Business has told the customer.

## What Tech has ruled out that you should also be saying out loud

Tech didn't just fail to build the work-order feature — ADR 001 explicitly rejected it for
v1, citing no work-order schema, no CDF write path, and no OEE threshold policy. That's a
stronger statement than "not done yet." If you only say "it's not in this PRD," the room may
assume it's coming next sprint. It is not scoped anywhere, and building it requires a new PRD
and a new ADR, not a bug fix.

## The question to expect in the room

"Sales already told the customer this works — why does the PRD say it doesn't?" Have an
answer ready: either Business needs to walk back or qualify the promise, or someone needs to
scope an OEE threshold policy and a work-order write path as new work — which is a decision
for this meeting, not something Product can resolve alone.

## One thing to walk in already knowing

You are not the one who is wrong here. Point to [[veridion-line3-oee-conflicts]]: it's Business's
promise against both Product and Tech, not a three-way disagreement where you need to pick a
side.

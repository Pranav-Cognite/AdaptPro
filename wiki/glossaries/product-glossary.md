---
type: glossary
title: "Product glossary — for Business and Tech"
persona: product
tags: [glossary, product, oee]
sources: [knowledge-base-prd]
created: 2026-10-03
updated: 2026-10-03
---

# Product glossary

Terms Product (PM/BA) uses day-to-day. Written for Business and Tech to read when they need to
understand what Product means, not for Product's own reference.

- **PRD (Product Requirements Document)** — the scoping document: what's actually planned to
  ship, with explicit acceptance criteria. `knowledge-base-prd` here.
- **In scope / out of scope** — explicit boundaries in the PRD. "Out of scope" means "not
  decided or built yet," not "never" — that distinction is exactly where the conflict with
  Business's promise lives.
- **Query template** — one of the three fixed question-shapes the product answers: OEE
  snapshot, OEE trend, downtime history. Product scopes the templates; Tech builds the tools
  behind them.
- **v1** — the first shippable version. Constraints written "for v1" are deliberately
  temporary, not permanent architecture.
- **Acceptance criteria** — the specific, testable conditions a feature has to meet before
  Product considers it done (e.g. "every answer cites the externalId it used").
- **Extractor (as Product scopes it)** — Product doesn't build extractors, but the PRD names
  which one feeds which OEE component: OPC UA → Performance, SAP → Availability, DB → Quality.
  Product's job is deciding what's queryable, not how the data gets there.
- **Threshold/alerting policy** — a rule for what counts as "OEE dropped below target." Does
  not exist yet — a named prerequisite before any write capability could be scoped.

# AdaptPro

LLMs and Agentic AI at the intersection of Business, Product, and Tech.

The business use case is in [`BUSINESS_USE_CASE.md`](BUSINESS_USE_CASE.md).

## Slice 1 — contract (no UI, no LLM)

Canonical epic schema, planted *Ask the graph* corpus, gold-set of the five failure modes, and deterministic evals.

Evals **must fail** a fake `ALIGNED` brief. They **must fail** if a planted contradiction is removed. They **must pass** an honest `BLOCKED` brief and a legal post-waiver `ALIGNED` brief.

```bash
poetry install
poetry run pytest
```

## Skip-level demo — LLM wiki (7 Oct 2026)

Offline ingest, query, and lint for the *Ask the graph* epic. No model is called. The wiki is compiled the way a helpful LLM wiki writes: a smooth overview and three persona pages that still disagree. The overview marks the epic Ready. That status is the thing to critique, not a successful alignment.

```bash
poetry run python -m adaptpro.wiki.server
```

Open http://127.0.0.1:8765 for the wiki and `demo/slides.html` for the deck. In the deck, arrow keys move slides and `S` toggles speaker notes. The notes on the Demo slide are the click path.

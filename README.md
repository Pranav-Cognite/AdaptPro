# AdaptPro

**Start here.** AdaptPro is a self-maintaining knowledge base shared by Business, Product, and Tech. The base is an LLM wiki: pages compiled from source documents, linked so a claim can be followed back to the page and the source it came from. Three steps keep it: **ingest** adds a document and updates the pages, **query** answers from those pages in the persona of the person asking, and **lint** checks the pages for disagreement and stale claims as the base grows. Every use case in this repo is a question asked of that base. The Veridion write-up below is one example stored in it, not the product itself.

**AdaptPro** is a persona-based, AI-native system that helps cross-functional teams stay
aligned on decisions by building a continuously updated knowledge base — a shared source of
truth that Business, Product, and Tech (and roles across the delivery stack) can query before
decisions get made.

> Build the knowledge base. Query it as your persona. Align on the decision — before you ship
> different products.

Beachhead: **Cognite delivery teams** first. The Veridion engagement below is a synthetic
example used to demonstrate the knowledge base, not a customer-facing AdaptPro product.

https://github.com/praneybehl/llm-wiki-plugin

## Prerequisites

To actually use this repo (not just read it), you need:

- **Claude Code**, with this repo open as the working directory.
- **The `llm-wiki` skill installed** at `~/.claude/skills/llm-wiki` — this repo's `wiki/`
  directory was bootstrapped with it (`scripts/init_wiki.py`) and its scripts
  (`wiki_lint.py`, `wiki_search.py`, etc.) are referenced throughout this README and
  `wiki/SCHEMA.md` by that path. Without it, the wiki's markdown is still fully readable, but
  the lint/search tooling won't resolve.
- **Python 3 and [`uv`](https://docs.astral.sh/uv/)** — the `llm-wiki` skill's scripts are
  run via `uv run --script ...` or plain `python3`, and `uv` is what installs their pinned
  dependencies (FastEmbed, sqlite-vec, PyYAML) on first use.
- **A fresh Claude Code session** the first time you use the three persona agents under
  `.claude/agents/` — see Known gaps below for why.

Nothing here requires a real Cognite Data Fusion project, tenant, or credentials —
`mock-cdf-project/` is static and fictional (see that section below).

## What this is

A working demo of one idea: **build a knowledge base from engagement sources**, keep Business /
Product / Tech claims in separate persona views, let each persona **query** that knowledge
base, and **surface whether a proposed decision is aligned** — before kickoff pretends everyone
agreed.

This repo implements the simplest version of that idea:

1. **Ingest** source documents into an LLM wiki
2. **Persona pages** (exclusive ownership — no blending)
3. **Conflict record** when promise / scope / buildable disagree
4. **Four read-only agents** that query the knowledge base (briefing + decision alignment)

Persona queries may look like a conversation. That is how someone **asks the knowledge base** —
AdaptPro is not a plant chat product.

## The example engagement: Veridion Line 3 OEE

**Veridion Chemicals** (fictional specialty-polymers manufacturer) has a delivery engagement
around OEE for Production Line 3 at Calder Valley Plant, grounded in CDF data.

Production Line 3 (`asset_line3`) sits in the Polymer Production Unit. Material passes through
Reactor R-301 and Extruder EX-302. OEE multiplies three things: time the line was up
(Availability), how fast it ran (Performance), and how much output was good (Quality).

**Customer pain (plain language):** supervisors learn OEE dropped too late, cannot tell whether
the loss was downtime, slow running, or scrap, and cannot turn that insight into action without
tool-hopping.

- **Business** has promised: see real-time OEE for any line, **and** automatically generate a
  corrective work order when OEE drops below target.
- **Product's PRD** and **Tech's ADR** both independently scope exactly three **read-only**
  query capabilities (OEE snapshot, OEE trend, downtime history) and explicitly rule out any
  write path for v1 — no work-order schema, no threshold policy, no write capability.

That's the conflict the knowledge base is built to surface, not hide: Business is promising
something neither Product nor Tech has scoped or built. Left unresolved, this is the shape of
**delivery reversal / mis-scoped AI** risk.

## Design rationale — why this approach, and why it's not the end state

Thesis: **kickoff is a lie when a GTM line, a PRD, and an ADR can each be correct and still
describe different products.**

**The maturity ladder considered, in order:**

1. **An LLM wiki** (what this repo currently implements) — one wiki, three persona pages per
   engagement, a human or agent reads them and compares. Good enough for one engagement and a
   handful of documents. Known failure mode: a wiki that re-reads and rewrites its whole corpus
   on every ingest will eventually smooth a real disagreement into one fluent, falsely "aligned"
   page — and a full-corpus lint does not scale.
2. **Agentic patterns** (partially implemented here, via the three persona-briefing agents) —
   give each persona its own voice so no single model pass can blend them, and add a critic
   that compares projections instead of merging them. Helps, but does not by itself solve
   accuracy or scale.
3. **A claim store with a deterministic check and delta ingest** (not yet built) — every
   promise, scope line, and constraint becomes a record with a source and an owner persona;
   persona pages become views rendered from those records; alignment is a pass/fail check on
   the records, not a model grading its own answer; each change only ingests and re-checks the
   one source that changed.

This repo deliberately stops at step 1, plus a slice of step 2. See
`docs/architecture/for-scale.md`.

**Where RAG fits, and where it doesn't:** retrieval is useful for fetching exact passages, but
it is a bad fit for deciding alignment. Similar passages get blended by a model into one fluent
answer — exactly how a real fork disappears.

**Critical risks this design has to guard against:**

- **Missing sources look like agreement.** A conflict check can only compare what was
  ingested. Gaps must be flagged red, not left blank.
- **Ingest will try to clean up the conflict.** Ingest must preserve both claims with their
  sources; only a separate check reports the clash.
- **A waiver can become a rubber stamp.** A sign-off with no name, no date, and no later
  visibility is a decision nobody will defend. (Not yet built — see Known gaps.)
- **Noisy output gets ignored.** Vague conflict spam trains teams to ignore the one real fork.
- **A copied wiki rots.** If the real documents still live elsewhere and this wiki is a second
  copy, it goes stale. It has to read the real sources, or the team has to work here.
- **Over-reliance on LLMs for decisions.** Agents inform and surface misalignment; humans own
  the decision.
- **Sensitive engagement data in AI systems.** Enterprise willingness to expose SoWs, Slack,
  and customer docs is a real adoption constraint.

## Repository layout

```
AdaptPro/
├── docs/engagements/veridion-line3-oee/   Business use case, PRD, ADR — source documents
│   ├── business-use-case.md
│   ├── prd.md
│   └── adr.md
├── docs/architecture/                     Current vs for-scale architecture notes
├── mock-cdf-project/                      Fictional CDF project grounding externalIds
│   └── modules/veridion_line3_oee/
├── wiki/                                  The LLM knowledge base
│   ├── SCHEMA.md                          Conventions — read this first
│   ├── sources/                           One summary page per ingested document
│   ├── personas/                          Business / Product / Tech views
│   ├── glossaries/                        Per-persona vocabulary for the other two
│   └── synthesis/                         Conflict record + filed briefs
└── .claude/agents/                        Four read-only agents that query the wiki
```

`mock-cdf-project/` is static and fictional — no deployed CDF tenant, cluster, or credentials.
It exists so every `externalId` the documents reference resolves to something real.

## How the knowledge base is built (this demo)

For `veridion-line3-oee`:

| Source | Owner persona | Lands in |
| --- | --- | --- |
| `docs/engagements/veridion-line3-oee/business-use-case.md` | Business | persona + source pages |
| `docs/engagements/veridion-line3-oee/prd.md` | Product | persona + source pages |
| `docs/engagements/veridion-line3-oee/adr.md` + `mock-cdf-project/` | Tech | persona + source pages |
| Cross-check of the three | — | `wiki/synthesis/veridion-line3-oee-conflicts.md` |

Ingest is a **team action**, not an automated pipeline: edit a source under
`docs/engagements/<slug>/`, then ask for re-ingest (see `wiki/SCHEMA.md`). Ask-before-answering
applies to ingest and to every agent query — it is never bypassed.

**Future source types** (not in this repo's clean three docs yet): Zoom summaries, Slack,
Google Drive, Jira, Confluence, customer KT, Teams, shared folders, pre-sales decks. See
`docs/architecture/for-scale.md`.

## How to use it

### Prompting scenarios

**1. Query the knowledge base as one persona (get briefed on the other two).**

- **Business** → `brief-business-on-product-and-tech.md`  
  e.g. "I am a business guy, explain product and tech to me."
- **Product** → `brief-product-on-business-and-tech.md`  
  e.g. "I am a product guy, explain business and tech to me."
- **Tech** → `brief-tech-on-business-and-product.md`  
  e.g. "I am a tech guy, explain business and product to me."

Known designations route to personas — Business → Plant Operator, Maintenance Manager, Plant
Supervisor; Product → Technical Product Manager; Tech → Data Engineer, Data Scientist,
Solutions Architect. Unrecognized designations get asked which persona they are closer to,
never guessed.

**Every agent asks before answering — hard gate, never bypassed.** First response is clarifying
questions only (grounded in wiki content where possible), then:

1. **Homework (Phase 1)** — fixed-format brief; may be filed under `wiki/synthesis/` on request
2. **Exploration (Phase 2)** — open-ended follow-up; never filed
3. **Impact of work (Phase 3)** — fixed-format impact analysis; filable on request

Other personas' claims are spoken in first-person voice. Glossary terms and technical
identifiers are defined inline on first use.

**2. Check a proposed decision against all three personas.**

> "If we added a work-order-draft path that only suggests text, would everyone be fine with it?"  
> "Check this decision against all three personas: scoping a 4th query template for shift-level summaries."

Invokes `.claude/agents/check-decision-alignment.md`. Same ask-before-answering gate. Verdicts:
**Aligned**, **Not aligned**, or **Undetermined** (silence never rounds up to Aligned). Drafts
conflict-entry text for a human to add — never writes the conflicts file itself.

**Check wiki structural health:**

```bash
python3 ~/.claude/skills/llm-wiki/scripts/wiki_lint.py wiki/
```

**Update a source document.** Edit under `docs/engagements/veridion-line3-oee/`, then ask for
re-ingest.

## Product jobs (what people hire AdaptPro for)

1. Homework before a cross-functional meeting
2. Explore what another persona claims — without blending it into yours
3. See how your work fits the bigger picture (impact)
4. Check whether a proposed decision is aligned across personas before you commit

## Known gaps

- **No sign-off mechanism.** Conflicts are recorded and explained; resolution still happens
  outside this repo.
- **Git is the only version record.** No link yet between a sign-off and a specific commit.
- **New agents need a fresh session.** Claude Code only picks up the first agent added to a new
  `.claude/agents/` directory after a restart; edits to existing agent files are picked up live.
- **Exploration doesn't use the wiki's own search tooling.** Agents use `Read`/`Grep`/`Glob`,
  not semantic search. Fine at current size; revisit past ~300 pages.
- **One engagement, agents hardcoded to it.** Adding a second engagement means deciding then
  whether to extend or duplicate agents.
- **Not production-grade.** Built on Claude Code + llm-wiki; synthetic sources; mock CDF; will
  not scale as a full-corpus reread on every ingest (see for-scale architecture).
- **Token efficiency.** Agents are not yet optimized for cost at corpus growth.

## Cognite ecosystem opportunities (later)

- Deeper integration with CDF as industrial evidence
- Atlas AI (richer context for agents / investigations)
- Flows apps (surfaces where delivery teams act)

## Architecture

- Current implementation: `docs/architecture/current-implementation.md`
- For scale (not built): `docs/architecture/for-scale.md`

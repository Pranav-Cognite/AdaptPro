# AdaptPro

**Start here.** AdaptPro is a knowledge base shared by Business, Product, and Tech. The base is an LLM wiki: pages compiled from source documents, linked so a claim can be followed back to the page and the source it came from. Three steps keep it. **Ingest** adds a document and updates the pages. **Query** answers from those pages in the persona of the person asking. **Lint** is a health check of the wiki: pages that disagree, claims a newer source has replaced, orphan pages, and missing links. It is not the decision check. Checking one proposed decision against the three personas is a separate agent, `check-decision-alignment`. In this demo a person maintains the wiki after ingest or lint. A self-maintaining loop, and a Capture phase that stores the signed decision, come later. The Veridion write-up below is one example stored in the base, not the product itself.

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
Product / Tech claims in separate persona views, and let each persona **query** that knowledge
base to understand the other two sides, prepare for meetings with good questions, and, when a
decision is coming, check whether it is aligned.

This repo implements the simplest version of that idea:

1. **Ingest** source documents into an LLM wiki
2. **Persona pages** — three pages for one engagement, under `wiki/personas/`. Business, Product, and Tech each have their own page, written only from that side's documents. They are not mixed into one summary.
3. **Open topics** record of what the personas have not yet settled (including any promise / scope / buildable mismatch)
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

That is one of the open topics the knowledge base keeps visible: Business has promised
something neither Product nor Tech has scoped or built yet. Surfacing it early, along with the
questions it raises, is what keeps it from turning into **delivery reversal / mis-scoped AI** risk.
It is an example topic, not what AdaptPro is for.

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
│   └── modules/ (platform, oee_model, line3_oee, ingestion)
├── wiki/                                  The LLM knowledge base
│   ├── SCHEMA.md                          Conventions — read this first
│   ├── sources/                           One summary page per ingested document
│   ├── personas/                          Business / Product / Tech views
│   ├── glossaries/                        Per-persona vocabulary for the other two
│   └── synthesis/                         Open topics + filed briefs
└── .claude/agents/                        Four read-only agents that query the wiki
```

`mock-cdf-project/` is static and fictional — no deployed CDF tenant, cluster, or credentials.
It exists so every `externalId` the documents reference resolves to something real. It is a
full Toolkit-shaped project (data model, extractors, transformation, OEE function, access groups,
30 days of datapoints with deliberate data-quality flaws); see its README.

## How the knowledge base is built (this demo)

For `veridion-line3-oee`:

| Source | Owner persona | Lands in |
| --- | --- | --- |
| `docs/engagements/veridion-line3-oee/business-use-case.md` | Business | persona + source pages |
| `docs/engagements/veridion-line3-oee/prd.md` | Product | persona + source pages |
| `docs/engagements/veridion-line3-oee/adr.md` + `mock-cdf-project/` | Tech | persona + source pages |
| Open topics across the three | — | `wiki/synthesis/veridion-line3-oee-open-topics.md` |

Ingest is a **team action**, not an automated pipeline: edit a source under
`docs/engagements/<slug>/`, then ask for re-ingest (see `wiki/SCHEMA.md`).

**Future source types** (not in this repo's clean three docs yet): Zoom summaries, Slack,
Google Drive, Jira, Confluence, customer KT, Teams, shared folders, pre-sales decks. See
`docs/architecture/for-scale.md`.

## How to use it

### Prompting scenarios

**1. Query the knowledge base as one persona (get briefed on the other two).**

- **Business** → `brief-business-on-product-and-tech.md`  
  e.g. "I am a business guy. We promised an automatic work order when Line 3 OEE drops. What have Product and Tech actually scoped?"
- **Product** → `brief-product-on-business-and-tech.md`  
  e.g. "I am a product guy. Business promised an automatic work order on an OEE drop. Does my read-only scope cover that, and what has Tech ruled out?"
- **Tech** → `brief-tech-on-business-and-product.md`  
  e.g. "I am a tech guy. Business promised an automatic work order when Line 3 OEE drops. Does our read-only decision cover that promise?"

Known designations route to personas — Business → Plant Operator, Maintenance Manager, Plant
Supervisor; Product → Technical Product Manager; Tech → Data Engineer, Data Scientist,
Solutions Architect. Unrecognized designations get asked which persona they are closer to,
never guessed.

**2. Check a proposed decision against all three personas.**

> "We will ship v1 as a read-only OEE lookup and leave the automatic work-order promise in the customer conversation. Are Business, Product, and Tech aligned?"

This is not lint. It invokes `.claude/agents/check-decision-alignment.md`. Verdicts:
**Aligned**, **Not aligned**, or **Undetermined** (silence never rounds up to Aligned).
Drafts open-topic text for a human to add — never writes the open-topics file itself.

**Lint the wiki structure** (broken links, missing pages, frontmatter — not a verdict on one decision, and not the cross-persona disagreement check):

```bash
python3 ~/.claude/skills/llm-wiki/scripts/wiki_lint.py wiki/
```

**Update a source document.** Edit under `docs/engagements/veridion-line3-oee/`, then ask for
re-ingest.

## Use cases

1. **Explore beyond your role** — read what the other personas in the engagement have actually committed to.
2. **Homework before a cross-functional meeting** — walk in knowing the other sides' documents and the bigger picture, with the sharp questions to ask them, each grounded in what their pages leave open.
3. **Check a decision** — for each decision, see whether Business, Product, and Tech are aligned and ready.
4. **Impact of your work** — see how your contribution sits in the engagement and what it does to the business.
5. **Slack** — an agent joins a long cross-persona thread and bridges the people in it. Not in this demo.
6. **Jira** — when a ticket is created, flag dependencies between personas and other concerns, and help align priorities. Not in this demo.
7. **Teams** — an agent joins a long cross-persona thread and bridges the people in it. Not in this demo.
8. **Look ahead** — compare the current plan with historical failure patterns, see dependencies early, and suggest what to change. Not in this demo.
9. **History plus now** — use what the engagement already decided together with what just changed. Not in this demo.

## Demo use case: check a decision

This repo demos use case 3, on one engagement: Veridion Line 3 OEE.

Production Line 3 is the polymer line at Calder Valley (Reactor R-301, then Extruder EX-302). Business promised a live OEE number and an automatic corrective work order when OEE drops. The PRD and the ADR scope three read-only queries — OEE snapshot, OEE trend, downtime history — and no write path. The knowledge base holds those as three persona pages. The conflict page records that the work-order promise is not what Product or Tech will build.

In the chat, ask whether a decision is aligned, for example: "If we added a work-order path, would everyone be fine with it?" The `check-decision-alignment` agent reads the three persona pages and answers per persona: aligned, not aligned, or undetermined. Silence is not treated as agreement. It can draft a conflict entry. A person files that entry. The agent does not write the wiki.

## Known gaps

- **Maintenance is human, on purpose, for this demo.** A person re-ingests a changed source and acts on a lint report. A self-maintaining loop is the later idea.
- **No Capture phase.** The signed decision is not stored as its own object. That phase comes after this chat demo.
- **No sign-off mechanism.** Open topics are recorded and explained; resolution still happens
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

### Integration with CDF

The CDF project is one of the sources ingested into the knowledge base. In this demo that source is `mock-cdf-project/`. A real delivery ingests the real CDF project the same way. CDF is part of the base, not a separate system AdaptPro has to be wired onto afterwards.

### Integration with Flows apps

Three shapes:

- AdaptPro itself is a Flows custom app.
- An AdaptPro tab or panel inside a Flows app.
- AdaptPro is a service, and Flows apps call its API.

### Integration with Atlas AI

AdaptPro is a plugin, skill, or subagent for Atlas AI. It gives Atlas the engagement's persona pages and open topics, so a root-cause analysis has that context instead of only the incident in front of it.

## Architecture

- Current implementation: `docs/architecture/current-implementation.md`
- For scale (not built): `docs/architecture/for-scale.md`

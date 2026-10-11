# AdaptPro
LLMs and Agentic AI at the intersection of Business, product and tech

AdaptPro (Agentic AI and LLMs for the intersection of Business, tech and Product):

More often than not you would find a product manager, a business analyst and an Architect speaking their own language and each one of them end up wondering why is it so difficult to put across such a simple idea.

An AI native product with 3 personas to start with (Business, Product and tech) where LLMs and Gen AI helps understand the nitty gritty details of the other domains. This product serves a purpose across levels from intern to CXOs in boardrooms.



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

A working demo of one specific idea: instead of Business, Product, and Tech each keeping
their own documents and discovering they disagree in a meeting, put all three in one wiki,
let an LLM read what each one actually claims, and surface the disagreement before anyone
walks into the room.

This repo currently implements the simplest version of that idea — an LLM wiki with three
persona pages per use case and a conflict record — plus four agents that turn "read the wiki"
into "get briefed in plain language" or "check whether a proposed decision actually holds up
against all three."

## The use case

**Veridion Chemicals**, a fictional specialty-polymers manufacturer, wants an "OEE Chat
Assistant": a chat interface where plant staff ask about OEE (Overall Equipment
Effectiveness) for Production Line 3 at the Calder Valley Plant, grounded in real CDF data.

- **Business** has promised the customer: "see real-time OEE for any line, and automatically
  generate a corrective work order the moment OEE drops below target."
- **Product's PRD** and **Tech's ADR** both independently scope exactly three read-only query
  tools (OEE snapshot, OEE trend, downtime history) and explicitly rule out any write
  capability for v1 — no work-order schema, no threshold policy, no write tool.

That's the conflict the rest of this repo is built to surface, not hide: Business is
promising something neither Product nor Tech has scoped or built.

## Design rationale — why this approach, and why it's not the end state

This grew out of a DevCon-talk-prep conversation built around one thesis: **kickoff is a lie
when a GTM line, a PRD, and an ADR can each be correct and still describe different
products.** The original demo use case for that conversation was "Ask the Graph" (a plant-chat
assistant for a hydropower customer); it's since been replaced by the OEE/Veridion use case
above, but the underlying design argument is unchanged.

**The maturity ladder considered, in order:**

1. **An LLM wiki** (what this repo currently implements) — one wiki, three persona pages per
   use case, a human or agent reads them and compares. Good enough for one use case and a handful
   of documents. The known failure mode: a wiki that re-reads and rewrites its whole corpus on
   every ingest will eventually smooth a real disagreement into one fluent, falsely "aligned"
   page — and a sprint-by-sprint lint that re-reads everything doesn't scale as the product
   grows.
2. **Agentic patterns** (partially implemented here, via the three persona-briefing agents) —
   give each persona its own voice so no single model pass can blend them, and add a critic
   that compares projections instead of merging them. This helps, but doesn't by itself solve
   accuracy (agents can still talk themselves into "aligned") or scale (they can still re-read
   the whole corpus every time).
3. **A claim store with a deterministic check and delta ingest** (not yet built) — every
   promise, scope line, and constraint becomes a record with a source and an owner persona;
   persona pages become views rendered from those records; alignment is a pass/fail check on
   the records (opposite claims, a promise wider than scope, a constraint missing from another
   view), not a model grading its own answer; and each change only ingests and re-checks the
   one source that changed, against the already-signed set — so the check stays cheap as the
   product grows, even though the corpus doesn't.

This repo deliberately stops at step 1, plus a slice of step 2. The claim store is the part
that would actually hold up at scale, and the main reason it isn't built yet.

**Where RAG fits, and where it doesn't:** retrieval is useful for fetching exact passages — a
citation behind a conflict, or an answer to "what did Business actually say about X" — but it
is a bad fit for deciding alignment. Similar passages get blended by a model into one fluent
answer, which is exactly how a real fork disappears.

**Critical risks this design has to guard against, regardless of stage:**

- **Missing sources look like agreement.** A conflict check can only compare what was
  ingested. If Product never writes a PRD, that's a gap, not evidence of agreement with
  Business and Tech — it has to be flagged red, not left blank. (This is why `knowledge-base-product.md`
  explicitly carried a `status: missing-source` state before the PRD existed.)
- **Ingest will try to clean up the conflict.** An LLM's instinct is to merge "ask anything"
  and "read-only" into one sensible-sounding page. If ingest does that, the fork is deleted
  before anyone can see it. Ingest has to preserve both claims with their sources; only a
  separate check gets to report the clash.
- **A waiver can become a rubber stamp.** A sign-off with no name, no date, and no later
  visibility is a decision nobody will defend. (Not yet built here — see Known gaps.)
- **Noisy output gets ignored.** If every check produces ten vague conflicts, the team stops
  reading it, and the one real fork gets missed along with the noise.
- **A copied wiki rots.** If the real documents still live in Confluence/Jira/Slack and this
  wiki is a second copy, it goes stale by the next sprint. It has to read the real sources, or
  the team has to actually look here instead.

## Repository layout

```
AdaptPro/
├── docs/epics/01-knowledge-base/     Business use case, PRD, and ADR — the 3 source documents
│   ├── business-use-case.md
│   ├── prd.md
│   └── adr.md
├── mock-cdf-project/                 Fictional CDF project the use case is grounded in
│   └── modules/knowledge_base/       Toolkit-spec-accurate CDM fixtures (assets, time
│       data_modeling/                series, activities, files) for Line 3's OEE data
├── wiki/                             The LLM wiki — personas, conflicts, conventions
│   ├── SCHEMA.md                     Conventions: persona pages, query/ingest workflow,
│   │                                 the briefing-agent convention — read this first
│   ├── sources/                      One summary page per ingested document
│   ├── personas/                     Business / Product / Tech views, each from only
│   │                                 their own source document
│   └── synthesis/                    The conflict record, plus any filed briefs
└── .claude/agents/                   Four subagents: three persona-briefing agents, plus a
                                     decision-alignment checker (see below)
```

`mock-cdf-project/` is static and fictional — there is no deployed CDF tenant, no cluster, no
credentials. It exists so every `externalId` the documents reference resolves to something
real, instead of being invented in prose.

## How to use it

### Prompting scenarios

**1. Get briefed on the other two personas.** Three separate scenarios, one per persona, each
invoking its own agent under `.claude/agents/`:

- **Business understanding Product and Tech** — invokes `brief-business-on-product-and-tech.md`.

  > "I am a business guy, explain product and tech to me."
  > "I am a plant operator, help me understand how this CDF product is going to help me with
  > my day-to-day job."
  > "I am a maintenance manager — how does my promise to the customer affect the other two?"

- **Product understanding Business and Tech** — invokes `brief-product-on-business-and-tech.md`.

  > "I am a product guy, explain business and tech to me."
  > "As a technical product manager, how does my work affect the other two?"
  > "How exactly will a data engineer be involved in this project?" (asked as Product)

- **Tech understanding Business and Product** — invokes `brief-tech-on-business-and-product.md`.

  > "I am a tech guy, explain business and product to me."
  > "I am a data engineer, help me understand the exact business use case I'm trying to solve
  > here."
  > "How does my work impact the business?"

Known designations route each prompt to the right persona automatically — Business → Plant
Operator, Maintenance Manager, Plant Supervisor; Product → Technical Product Manager; Tech →
Data Engineer, Data Scientist, Solutions Architect. An unrecognized designation (e.g. "I'm a
Reliability Engineer") gets asked which of the three personas it's closer to, never guessed.

**Every one of these agents asks before answering, as a hard gate.** The first response to
any prompt above is one or more clarifying questions, not a brief — grounded in the actual
wiki content where possible (the open conflict, a specific ADR rejection) and anchored to a
concrete task (a shift handover, sprint planning, debugging a pipeline, etc.), presented as a
short set of selectable options plus "something else." The agent only proceeds once that
exchange has happened — including on a single-shot invocation, where it returns just the
question(s) and waits to be re-invoked with the answer.

Once answered, each agent runs up to three phases in the same conversation:

1. **Homework (Phase 1)** — a fixed-format brief: what the other two personas claim, where
   your own commitments are unsupported, the sharpest question to expect, one thing to walk in
   already knowing. Runs first by default. Can be filed as a permanent record under
   `wiki/synthesis/`, but only if you ask.
2. **Exploration (Phase 2)** — anything else, about anything in the repo, not just this one
   use case. Answered live from whatever files are relevant. Never filed, even on request —
   it's intentionally ephemeral.
3. **Impact of work (Phase 3)** — triggered by a question like "how does my promise/work
   affect the other two" or "what's downstream of what I build/commit to." A fixed-format
   impact analysis. Like Phase 1, can be filed on request.

Throughout all three phases, the other two personas' claims are narrated in their own
first-person voice ("my ADR rejected this because...") rather than third-person summary — this
applies inside the fixed-format Phase 1/3 sections too, not just free-form answers. Any
glossary term or technical identifier (`CogniteActivity`, `externalId`, an ADR reference, etc.)
is defined briefly inline the first time it's used, since each glossary is written for the
*other two* personas to read, not the persona itself.

**2. Check a proposed decision against all three personas.** In the same kind of session:

> "If we added a work-order-draft tool that only suggests text, would everyone be fine with
> it?"
> "Check this decision against all three personas: scoping a 4th query template for
> shift-level summaries."

This invokes `.claude/agents/check-decision-alignment.md`. The same ask-before-answering gate
applies first. The agent then reports a per-persona verdict — **Aligned**, **Not aligned**, or
**Undetermined** (silence from any persona never rounds up to Aligned) — and, if not aligned,
offers to draft (but never write) new conflict-entry text for you to add yourself. A vague
decision ("should we improve the product") gets rejected and a more concrete one requested,
rather than guessed at.

**Check the wiki's structural health:**

```bash
python3 ~/.claude/skills/llm-wiki/scripts/wiki_lint.py wiki/
```

**Update a source document.** Edit the file under `docs/epics/01-knowledge-base/`, then ask
for it to be re-ingested — there is no automated pipeline that does this on file save; it's a
deliberate team action (see `wiki/SCHEMA.md`).

## Known gaps

- **No sign-off mechanism.** Conflicts are recorded and explained, but nobody can yet mark one
  "accepted" with a name and a date — resolution still happens outside this repo.
- **Git is the only version record.** There's no versioning scheme beyond commit history, and
  no link yet between a sign-off and a specific commit.
- **New agents need a fresh session.** Claude Code only picks up the first agent added to a new
  `.claude/agents/` directory after a restart; edits to existing agent files are picked up
  live.
- **Exploration doesn't use the wiki's own search tooling.** The agents read files directly
  (`Read`/`Grep`/`Glob`), not through the llm-wiki skill's semantic search layer. Fine at 8
  pages; will need to change if the wiki grows past roughly 300 pages.
- **One use case, agents hardcoded to it.** All four agents (three briefing agents plus
  decision-alignment) are specific to this OEE use case by design, not parameterized — adding a
  second use case means deciding then whether to extend or duplicate them.
- **Persona designations deferred.** Sub-roles within each persona (e.g. which kind of
  Business role is asking) aren't modeled yet.



Sources for building the knoweledge base using LLM Wiki:
1. Zoom meeting summaries
2. Slack threads
3. Google drive with all the relevant files and/or folders
4. JIRA tickets
5. Confluence documentation
6. Any KTs sessions taken and/or given by the customer (In the form of recordings, pdfs etc)
7. Teams chat
8. Shared folders with customers on MS teams
9. PPTs and documents from Pre-sales


Current implementation limitations:
1. Built out of off the self plugins from claude code so this is not really production grade
2. A very simple use case which lacks a lot of the chaotic real world implementation details
3. Mock CDF project so lacks a solid real use case
4. Wiki built is very simple and does not really include a lot of real sources.
5. Fails on scale. Even though this is the theme of this year's DevCon this current implementation is not going to scale
6. Agents are not optimized to use tokens efficiently
7. Personas are not very rigidly implemented at the moment. Needs a more mature implementation.


Opportunities for this to integrate into CDF:
1. Integration with CDF
2. Integration with Atlas AI
3. Integration with Flows Apps


Product use cases as of now:
1. Homework for a cross-functional team meeting
2. Exploration of what the other line of business does
3. Get an understanding of the bigger picture by understanding how the work integrates into the grand scheme of things
4. Intelligent decision aligning assisant to see if there are any gaps withing cross-functional teams before decisions are made.


Things to consider:
1. The agent is as good as the questions that are going to be asked by the user across personas. Makes it a product of great use across levels
2. 



TODO:
1. Make an architecture diagram for the current implementation. Give the code for the architecture diagram in mermaid. Make sure to use various colors to make sure it is readable and understandable
2. Make an architecture diagram for scale using mermaid. Make sure to use various colors to make sure it is readable and understandable
3. Set the tone here by showing some real life stats saying how and what the gap currently is not being addressed.


Improvements:
1. Understand what are the current shortcomings of the wiki or the knoweldge base that is present at the moment.
2. Increase the efficiency of the wiki and make it more robust. This wiki or the knoweldge base should be in such a way that the agents can easily reference this or read this and interact efficiently.
3. How exactly is this idea going to scale? 

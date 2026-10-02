# AdaptPro
LLMs and Agentic AI at the intersection of Business, product and tech


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
persona pages per use case and a conflict record — plus three agents that turn "read the
wiki" into "get briefed in plain language."

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
products.** The original demo epic for that conversation was "Ask the Graph" (a plant-chat
assistant for a hydropower customer); it's since been replaced by the OEE/Veridion use case
above, but the underlying design argument is unchanged.

**The maturity ladder considered, in order:**

1. **An LLM wiki** (what this repo currently implements) — one wiki, three persona pages per
   use case, a human or agent reads them and compares. Good enough for one epic and a handful
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
└── .claude/agents/                   Three persona-briefing subagents (see below)
```

`mock-cdf-project/` is static and fictional — there is no deployed CDF tenant, no cluster, no
credentials. It exists so every `externalId` the documents reference resolves to something
real, instead of being invented in prose.

## How to use it

**Get briefed before a cross-functional meeting.** Declare which persona you are and ask to
be briefed — in a fresh Claude Code session in this repo:

> "I am a product guy, explain business and tech to me......"

This invokes one of `.claude/agents/brief-{business,product,tech}-on-....md`. Each one runs
two phases in the same conversation:

1. **Homework** — a fixed-format brief: what the other two personas claim, where your own
   commitments are unsupported, the sharpest question to expect, one thing to walk in already
   knowing. Can be filed as a permanent record under `wiki/synthesis/`, but only if you ask.
2. **Exploration** — anything else, about anything in the repo, not just this one use case.
   Answered live from whatever files are relevant. Never filed, even on request — it's
   intentionally ephemeral.

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
- **One use case, agents hardcoded to it.** The three briefing agents are specific to this OEE
  epic by design, not parameterized — adding a second epic means deciding then whether to
  extend or duplicate them.
- **Persona designations deferred.** Sub-roles within each persona (e.g. which kind of
  Business role is asking) aren't modeled yet.

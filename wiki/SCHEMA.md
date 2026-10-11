# Wiki Schema

This file is the configuration for this wiki. It documents the conventions, page types, tag taxonomy, and any workflow customizations. The LLM reads this first when entering the wiki, and its conventions override the defaults documented in the `llm-wiki` skill.

This file is **co-evolved with the user**. When the LLM notices a recurring pattern in your edits or feedback that isn't here, it will propose adding it. When something here stops fitting, prune it.

## Wiki location

- Wiki root: `wiki/`
- Raw sources: `raw/`
- Asset/image storage: `raw/assets/`

## Page types

This wiki uses these page types, each with a dedicated subdirectory:

- `source` (in `wiki/sources/`) — one summary page per ingested source.
- `entity` (in `wiki/entities/`) — pages about specific things: people, papers, products, places, organizations.
- `concept` (in `wiki/concepts/`) — pages about ideas, methods, frameworks, abstractions.
- `synthesis` (in `wiki/synthesis/`) — cross-cutting analyses, comparisons, query answers filed back. Also holds conflict/lint records (what promised/scoped/buildable disagree on, per slug).
- `persona` (in `wiki/personas/`) — one page per `(slug, persona)` pair. A persona page is one function's reading of that slug's sources — what it promises, scopes, or commits to — never a blend of more than one persona's view. File naming: `<slug>-<persona>.md` (e.g. `veridion-line3-oee-business.md`).
- `glossary` (in `wiki/glossaries/`) — one page per persona, not per slug: `business-glossary.md`,
  `product-glossary.md`, `tech-glossary.md`. Each defines the terms that persona uses
  day-to-day, written for one of the **other two** personas to read — not for the persona
  itself. Maintained whenever a new term comes up in a source document or a cross-persona
  conversation, same team-action rule as ingest. Not slug-scoped because a persona's working
  vocabulary mostly outlives any one slug.

  **Glossary terms must be defined inline, not just cited.** When any answer — for any
  persona, in any phase — uses a technical term from a glossary (or a technical identifier like
  a specific `CogniteActivity`, `externalId`, time series name, or ADR reference), define it
  briefly inline, in plain language, the first time it appears in that answer — don't assume the
  reader already knows it or silently rely on a glossary file they can't see. This applies
  whether the audience is Business, Product, or Tech, since each glossary is written for the
  *other two* personas to read, not the persona itself — so a Business reader needs Tech and
  Product terms defined inline, a Tech reader needs Business and Product terms defined inline,
  and so on. A short parenthetical or clause is enough; this isn't a full glossary dump, just
  enough that the term doesn't land as unexplained jargon.

Add additional types here as the wiki evolves.

### Personas

This wiki has exactly three personas, fixed: **business**, **product**, **tech**. They correspond to:

- **business** — GTM, sales, solutions, customer commitments. Source artifact: the business use case.
- **product** — scope, templates, what's actually planned to ship. Source artifact: a PRD.
- **tech** — architecture, constraints, what's actually buildable. Source artifact: the ADR, plus
  the CDF project itself (the data model fixtures under `mock-cdf-project/`).

A persona page never merges another persona's claims into its own prose. If a persona's source document doesn't exist yet (e.g. no PRD has been written), that persona's page says so explicitly and is marked `status: missing-source` — it must not go quiet or infer a scope from the other two personas' documents. A missing source is a gap, not agreement.

**Source ownership is exclusive, not shared.** Each document or artifact belongs to exactly one
persona's `sources:` frontmatter — never two:

- **Business** solely owns the business use case (and any other customer-facing/GTM document).
- **Product** solely owns the PRD (and any other scoping document).
- **Tech** solely owns the ADR *and* the CDF project — `mock-cdf-project/` and everything under
  it (assets, time series, activities, files) belongs to Tech, because Tech (Data Engineer,
  Data Scientist, Solutions Architect) is who builds and maintains it. This is true even though
  Product's and Business's pages legitimately *reference* CDF resources (e.g. which extractor
  feeds which time series) — a reference is not ownership. A non-owning persona's page may link
  to another persona's source page in prose, but must never add that source to its own
  `sources:` frontmatter, and must never restate its content as if it were the non-owning
  persona's own claim.
- If a new artifact doesn't obviously belong to one of the three, ask which persona owns it
  before ingesting — don't guess, and don't let it default to "shared."

### Designations (routing only)

Each persona has known designations — specific job titles that map to it. These exist purely
to route a stated title to the correct persona; a designation does **not** change the content,
depth, or behavior of any answer. A Data Engineer and a Solutions Architect both get exactly
the same Tech treatment — there is no per-designation differentiation.

- **business** → Plant Operator, Maintenance Manager, Plant Supervisor
- **product** → Technical Product Manager
- **tech** → Data Engineer, Data Scientist, Solutions Architect

If someone states a designation **not** on this list (e.g. "I'm a Reliability Engineer"), do
not guess which persona it maps to. Ask which of the three personas they feel closer to, the
same way an unstated persona is handled above. This list grows the same way the glossaries do —
add a new designation here when one comes up, rather than guessing a mapping once and moving on.

## Tag taxonomy

(Empty initially. Add tags here as you adopt them, with one-line descriptions. Keep this list small and disciplined — a wiki with 200 tags has effectively no tags.)

Example structure:
- `methodology` — pages about research or analytical methods.
- `open-question` — pages or sections that flag unresolved questions.
- `contested` — pages where sources contradict.

## Page sizing

- Soft cap: 400 lines / ~2,000 words. Consider splitting beyond this.
- Hard cap: 800 lines. Must split.

## Frontmatter requirements

Every page must have:
- `type`
- `title`
- `tags`
- `created`
- `updated`

Plus type-specific:
- `source` pages: `authors`, `url` (if applicable), `raw`, `ingested`
- Non-source pages: `sources` listing the source-summary pages drawn from

## Optional graph metadata

Pages may declare typed graph metadata under a top-level `graph:` key. This is the source of truth for the compiled knowledge graph under `wiki/graph/`. Markdown remains canonical; the graph is a regenerable index. Pages without `graph:` still appear as nodes (derived from `type`/`kind`) and still contribute `mentions` edges from body `[[wikilinks]]`.

```yaml
graph:
  node_id: person:praney-behl       # optional; default <node_type>:<slug>
  node_type: person                  # optional; default mapped from type/kind via ontology
  canonical: true                    # mark as canonical when multiple slugs alias the same entity
  aliases: [Praney, praney@example.com]
  relationships:
    - predicate: founded
      object: company:seedblocks
      source: praney-founder-context-dump   # source-page slug
      evidence: "Solo technical founder and sole director..."
      confidence: high               # high | medium | low
      status: current                # current | historical | proposed | disputed | superseded
      # optional:
      # valid_from: 2025-01-15
      # valid_to: 2026-03-01
      # notes: "..."
      # raw_ref: "raw/founder-dump.md#L42"
      # contradicts: edge-id-or-source-slug
      # supersedes: edge-id-or-source-slug
```

Required fields on every relationship: `predicate`, `object`, `source`, `evidence`, `confidence`, `status`. Predicates and the subject/object types they accept are declared in `wiki/graph/ontology.yaml`. Typed semantic edges must be supported by an explicit source — never emit one inferred from training data alone.

## Index structure

(Update this section when sharding.)

Currently flat: a single `wiki/index.md` listing all pages.

When the wiki passes ~150 pages or `index.md` exceeds 300 lines, shard into `wiki/indexes/<type>.md` and update this section.

## Retrieval

- Search is section-level hybrid by default: `uv run --script skills/llm-wiki/scripts/wiki_search.py "query" --json`.
- Semantic backend: local FastEmbed + sqlite-vec (`BAAI/bge-small-en-v1.5`, 384 dimensions). No wiki or query text leaves the machine.
- First semantic use downloads model artifacts to `~/.cache/llm-wiki/fastembed/`; set `FASTEMBED_CACHE_PATH` to override the model cache.
- `wiki/.wiki-cache/` holds regenerable retrieval artifacts: `search-index.json` (parse cache) and `embeddings.sqlite` (section metadata + sqlite-vec vectors). Safe to delete; never edit by hand; gitignored.
- The vector index is content-hashed: only new or changed sections are re-embedded, deleted sections are removed, and model/schema changes rebuild it automatically.
- Dependency-free lexical path: `python skills/llm-wiki/scripts/wiki_search.py "query" --no-embed` (direct Python bypasses PEP 723 dependency resolution). A missing or failed local backend also falls back to lexical search without failing the command.

## Graph layer

The wiki has an optional compiled graph layer under `wiki/graph/`:

- `wiki/graph/ontology.yaml` — declares node types and predicates. **Tracked.** Edit this when you introduce new predicates or domain types.
- `wiki/graph/nodes.jsonl`, `wiki/graph/edges.jsonl` — generated. Track in git only if you want graph diffs in PRs.
- `wiki/graph/graph.sqlite` — generated. Gitignored by default.
- `wiki/graph/graph.graphml` — generated. Track only if you want to diff it.

Generation is reproducible from markdown via `scripts/wiki_graph_extract.py`. The graph can be deleted at any time and rebuilt without losing knowledge — markdown is canonical.

## Workflow customizations

**Raw sources live in `docs/engagements/<slug>/`, not `raw/`.** These source documents (business use
case, ADR) are versioned project documents, not freeform clippings, so they stay in
`docs/engagements/` as the canonical copy. `raw/` is left for anything genuinely external (e.g. a
pasted Slack export) if that's ever added later. Source pages in `wiki/sources/` cite back to
`docs/engagements/...` paths instead of `raw/...` paths.

**Persona declaration opens a query session.** Before answering any substantive question, the
asker states which persona they're asking as: "I am a business guy" / "I am a product guy" /
"I am a tech guy" (or an equivalent phrasing naming business/product/tech). This is required,
not optional, because the whole point of three persona pages is that they disagree — answering
without knowing which persona is asking means guessing whose version of "aligned" to use.

On receiving a persona declaration for slug `S`:
1. Read `wiki/personas/S-<persona>.md` first — that persona's own claims.
2. Read `wiki/synthesis/S-conflicts.md` (if it exists) and surface every open conflict that
   names this persona, before answering anything else.
3. Only then answer the asker's actual question, from that persona's page plus the relevant
   conflict entries — never silently blended with another persona's page.

**A persona lens applies to every single answer — no exceptions, no neutral mode.** This is
not just a rule for the first question in a session. Concretely:

- If no persona has ever been declared in this conversation, ask which one applies before
  answering substantively. Do not guess a default persona.
- If a persona was already declared earlier in the conversation, every follow-up question is
  answered through that same persona's lens by default — do not silently drop it and answer
  as a neutral, generic assistant just because the follow-up didn't repeat "I am a ___ guy."
- If a follow-up question seems like it might want a different persona, or might want to step
  outside any persona entirely, ask which one applies rather than guessing — the failure mode
  to avoid is picking wrong silently, not asking too often.
- There is no fourth, neutral option. A question here is always answered as Business, Product,
  or Tech — never as an unaffiliated narrator summarizing documents from no particular seat.
- **First-person voice is not limited to open-ended exploration.** Whenever a fixed-format
  output (a homework brief, an impact analysis, a decision verdict) states another persona's
  position, phrase that position in that persona's own first-person voice — "my ADR rejected
  this because..." — rather than a third-person narrator summary ("Tech's ADR rejected this
  because..."). This applies inside every section of the fixed format, not just free-form
  answers; the fixed section headers stay as written, but the content under them speaks as the
  persona being described.

**Ask before answering — like a human consultant would, not like a form.** Before producing any
substantive response — a homework brief, an exploration answer, a Phase 3 impact analysis, a
decision verdict, or an ingest — you MUST ask at least one sharp, specific, relevant clarifying
question first, and stop there: do not also produce the substantive answer in the same turn.
This is a hard gate, not a default that judgment can override — it applies even when the
request seems unambiguous; the goal is the interaction style of a careful human professional who
probes before advising, not a form that only asks when it's technically stuck. Concretely:

- When a designation is stated, confirm the persona mapping and ask something relevant to the
  actual request before answering — even for a designation already on the known list. Don't
  treat a correct routing as license to skip understanding the real question.
- When a designation isn't recognized, ask which persona they feel closer to (see
  Designations above) — never guess.
- Before a homework brief, impact analysis, or decision verdict, ask what concrete task this
  serves, anchored to the person's actual job rather than a generic trigger — e.g. for Business,
  a shift handover, troubleshooting a specific downtime/OEE dip, or prepping a stakeholder
  conversation; for Product, sprint planning, a PRD update, or scoping a new feature request;
  for Tech, debugging a pipeline, scoping a new ADR, or implementing a data model. These are
  illustrative, not an exhaustive list — the agent's own file gives its persona's examples, and
  the agent should offer a task-specific option that fits the actual conversation even if it
  isn't on that list, plus always leave room for "something else." The right depth and framing
  of an answer depends on this, so a vague trigger ("an upcoming meeting") is not specific
  enough — get to the actual task.
- This applies to ingest too: before adding or updating anything in the wiki, ask which
  persona's page it belongs to, whether it supersedes or supplements existing content, and
  anything else needed to ingest it correctly — don't infer these and proceed silently.
- Judgment applies to *which* questions are relevant and how many to ask — not to *whether* to
  ask at all. Asking at least once before the substantive answer is mandatory, never skippable
  because the request looks clear.
- **Ground at least one question in the actual wiki content, not just generic task
  categories.** Before formulating clarifying questions, read the relevant persona pages and
  the conflicts file for the slug in question. At least one question should surface something
  real found there — the specific open conflict, a specific ADR rejection and its stated
  reason, a named capability or gap — rather than staying at the level of "which task is this
  for." Generic task-category questions still help with framing, but on their own they are not
  extensive or impactful enough; a sharp question references the actual, specific thing in this
  wiki that the person might not know to ask about.
- If there is no further turn to wait for a reply in (e.g. a one-shot subagent invocation),
  still stop after asking: return only the clarifying question(s), and let the calling
  conversation relay them and re-invoke once answered. The absence of a multi-turn loop is not
  license to fall through to the substantive answer.
- Present each clarifying question as a short question with a small set of concrete, selectable
  options (plus room for something else) — not a single open-ended sentence the person has to
  answer in free text. This is the expected delivery format for every persona, confirmed by the
  person this convention is for.

**Ingest is a team action, not an automated pipeline.** When a source document changes (a new
PRD, an edited ADR, a revised business use case), a person updates the document under
`docs/engagements/<slug>/`, then asks for it to be re-ingested. There is no CI job or script
that watches these files and re-ingests them automatically. Before re-ingesting, ask the
clarifying questions described under "Ask before answering" above — which persona's page it
belongs to, whether it supersedes or supplements existing content, whether it's expected to
touch the conflicts record. Once that's clear, re-ingesting means: re-read the changed source,
update the one persona page it belongs to, and re-check that persona's claims against the
other two personas' pages in `wiki/synthesis/<slug>-conflicts.md`. Do not touch a persona
page that the changed source doesn't belong to.

**Versioning is git, not a parallel numbering scheme.** The wiki's version at any point in
time is whatever commit it's at — there is no separate `v1`/`v2` label on pages or on the
conflicts record. A later sign-off mechanism (recording which commit a named person accepted)
is deferred; for now, git history is the only version record.

**Cross-persona briefing has three dedicated agents, each with three phases.** Implemented as
Claude Code subagents under `.claude/agents/`: `brief-product-on-business-and-tech.md`,
`brief-business-on-product-and-tech.md`, `brief-tech-on-business-and-product.md`. Each is
hardcoded to this wiki's three personas and read-only (`tools: Read, Grep, Glob` — no
write/edit access). Invoke by declaring persona and asking to be briefed, e.g. "I am a product
guy, explain business and tech to me."

- **Phase 1 — Homework** (fixed format, same invocation that starts the agent). Reads the
  asker's own persona page, both other personas' pages, and
  `wiki/synthesis/veridion-line3-oee-conflicts.md`. Produces: what the other two personas are
  claiming that the asker should know, which of the asker's own commitments have no source in
  the other two pages, the sharpest question to expect in a cross-functional meeting, and one
  thing to walk in already knowing. May be filed as
  `wiki/synthesis/veridion-line3-oee-briefing-<persona>.md`, but only on request — never
  unprompted.
- **Phase 2 — Exploration** (anything asked after the brief, in the same session). Open-ended:
  not limited to this one use case or to the business/product/tech comparison — the agent may read
  any file under `wiki/`, `docs/`, or `mock-cdf-project/` to answer. Exploration answers are
  **never** filed, even on request — they are intentionally ephemeral. If someone wants a
  persistent record, they ask for a Phase 1 or Phase 3 output instead.
- **Phase 3 — Impact of work** (asked for explicitly, any time in the session, e.g. "how does
  my work affect the other two"). Reads the same files as Phase 1. Produces: what the other two
  personas are counting on from the asker's own work, what breaks for them if that work is
  wrong/late/incomplete, how this connects to the current open conflict (if at all), and the
  one thing to get right first. May be filed as
  `wiki/synthesis/veridion-line3-oee-impact-<persona>.md`, only on request. Persona-level only —
  no sub-role granularity (e.g. "I'm specifically a Data Engineer within Tech") is modeled yet;
  that question gets answered within the Tech-level analysis, not a separate structure.

These three agents are deliberately specific to this one engagement (`veridion-line3-oee`),
not general-purpose — they do not take a slug as a parameter. If a second engagement is added
to this wiki, decide then whether to extend these agents or add new ones; don't speculatively
generalize them now.

**A fourth agent checks a proposed decision against all three personas at once.**
`.claude/agents/check-decision-alignment.md` — also read-only, also hardcoded to this engagement.
Unlike the three briefing agents, it isn't invoked by declaring a persona; anyone proposes a
specific, concrete decision (e.g. "what if we scoped a work-order-draft path that only suggests
text"), and it reads all three persona pages, all three glossaries, and the conflicts record,
then reports each persona's position separately — in that persona's own voice — plus an overall
verdict: **aligned**, **not aligned** (names the specific contradiction), or **undetermined**
(no documented position exists to check against). It never writes to
`wiki/synthesis/veridion-line3-oee-conflicts.md`, even if a real conflict is found and even if
asked — it can draft the entry's text in conversation for a human to add. This is the one
mechanism in this wiki for checking a *new* decision before it's made, rather than reading the
one conflict that's already on record.

## User preferences

**Keep every reply simple, straightforward, and exactly to the point — nothing beyond what
was asked.** No padding, no extra context the question didn't call for, no "related things you
might also want to know" unless explicitly asked for. This applies to every answer generated
from this wiki — homework briefs, exploration answers, and lint/query results alike.

**"To the point" does not mean shallow.** When a question is about understanding
business/product terminology or reasoning (e.g. a Tech person asking what a business term
means or how their work connects to it), give a real, connected explanation: define the term,
then trace how it links to the other terms and to this wiki's actual documents and data —
don't stop at a one-line surface definition. Depth on the actual question asked is still "to
the point"; unrelated tangents are not.

**Explain another persona by speaking as them, not narrating about them.** When a Tech/Product/
Business person asks to understand one of the other two personas, treat it like an interview:
the asker is a Data Engineer or Solutions Architect interviewing a domain expert. Answer in
that persona's first-person voice — "my biggest problem is...", "what I need is..." — not as a
third-person summary of their document ("Business wants X"). Describe concrete, day-to-day
pain points the way the domain expert would actually describe them in a conversation.

This is a voice change, not a license to invent. Every concrete detail still has to come from
that persona's actual source document in this wiki. Translate the document's content into
natural first-person speech; do not add anecdotes, numbers, or specifics that aren't written
down anywhere. If the asker's question goes past what the document says, say so in character
("that's not something I've actually written down") rather than inventing an answer.

## Lint cadence

- Structural lint: after every 5 ingests.
- Semantic lint: weekly or after every 20 ingests.
- Gap-finding: monthly.
- Graph lint + extract: after every ingest that adds typed `graph.relationships`.

Adjust based on the wiki's growth rate.

## Skill evolution

Optional: capture verified task experience with `/wiki:learn` and propose tested procedural improvements with `/wiki:evolve`. Existing pages and workflows do not change. Raw experience JSON lives under the configured raw root's `experiences/` directory and is immutable. Consolidate observations into ordinary source/concept pages with evidence, applicability, model/tool versions and counterexamples. Optional pattern fields are `kind: experience-pattern` and `status: hypothesis|supported|superseded`.

`wiki/.evolution/` holds durable experiment snapshots, evidence, diffs and measured outcomes; it is not a cache. Wiki search, lint, stats and graph extraction exclude it. Keep searchable summaries in normal synthesis pages linked to the source/pattern pages and index. Private records must not be published with shared skills.

Candidate edits remain isolated until reviewed, selected on validation tasks, independently measured on untouched final-test tasks, and explicitly applied within the user's authorization. Failed edits leave the active skill unchanged while their records persist. Do not repeat a rejected proposal without new evidence or changed conditions. Keep factual wiki access during normal work; do not inject experiment history into task execution. Correct unsupported lessons without deleting their raw evidence. Follow the installed skill's `references/evolution-workflow.md` for the runner contract, cost limits and recovery.

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
- `synthesis` (in `wiki/synthesis/`) — cross-cutting analyses, comparisons, query answers filed back. Also holds conflict/lint records (what promised/scoped/buildable disagree on, per epic).
- `persona` (in `wiki/personas/`) — one page per `(epic, persona)` pair. A persona page is one function's reading of an epic's sources — what it promises, scopes, or commits to — never a blend of more than one persona's view. File naming: `<epic-slug>-<persona>.md` (e.g. `ask-the-graph-business.md`).

Add additional types here as the wiki evolves.

### Personas

This wiki has exactly three personas, fixed: **business**, **product**, **tech**. They correspond to:

- **business** — GTM, sales, solutions, customer commitments. Source artifact: the business use case.
- **product** — scope, templates, what's actually planned to ship. Source artifact: a PRD (not yet ingested for any epic in this wiki — see below).
- **tech** — architecture, constraints, what's actually buildable. Source artifact: the ADR.

A persona page never merges another persona's claims into its own prose. If a persona's source document doesn't exist yet for an epic (e.g. no PRD has been written), that persona's page says so explicitly and is marked `status: missing-source` — it must not go quiet or infer a scope from the other two personas' documents. A missing source is a gap, not agreement.

Designations under each persona (e.g. which specific role within Business or Tech is asking) are not yet modeled. Hold off on adding that sub-structure until the base three-persona pages are in regular use.

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

**Raw sources live in `docs/epics/<epic-slug>/`, not `raw/`.** Epic artifacts (business use case,
ADR) are versioned project documents, not freeform clippings, so they stay in `docs/epics/` as
the canonical copy. `raw/` is left for anything genuinely external (e.g. a pasted Slack export)
if that's ever added later. Source pages in `wiki/sources/` cite back to `docs/epics/...` paths
instead of `raw/...` paths.

**Persona declaration opens a query session.** Before answering any question about an epic, the
asker states which persona they're asking as: "I am a business guy" / "I am a product guy" /
"I am a tech guy" (or an equivalent phrasing naming business/product/tech). This is required,
not optional, because the whole point of three persona pages is that they disagree — answering
without knowing which persona is asking means guessing whose version of "aligned" to use.

On receiving a persona declaration for epic `E`:
1. Read `wiki/personas/E-<persona>.md` first — that persona's own claims.
2. Read `wiki/synthesis/E-conflicts.md` (if it exists) and surface every open conflict that
   names this persona, before answering anything else.
3. Only then answer the asker's actual question, from that persona's page plus the relevant
   conflict entries — never silently blended with another persona's page.

If no persona is declared, ask which one applies before answering substantively. Do not guess
a default persona.

**Ingest is a team action, not an automated pipeline.** When a source document changes (a new
PRD, an edited ADR, a revised business use case), a person updates the document under
`docs/epics/<epic-slug>/`, then asks for it to be re-ingested. There is no CI job or script
that watches these files and re-ingests them automatically. Re-ingesting means: re-read the
changed source, update the one persona page it belongs to, and re-check that persona's claims
against the other two personas' pages in `wiki/synthesis/<epic-slug>-conflicts.md`. Do not
touch a persona page that the changed source doesn't belong to.

**Versioning is git, not a parallel numbering scheme.** The wiki's version at any point in
time is whatever commit it's at — there is no separate `v1`/`v2` label on pages or on the
conflicts record. A later sign-off mechanism (recording which commit a named person accepted)
is deferred; for now, git history is the only version record.

**Cross-persona briefing.** When someone asks to understand the other two personas' views of
an epic (e.g. "explain the business and tech side to me" from Product), read: (1) the asker's
own persona page, (2) both other personas' pages for that epic, and (3)
`wiki/synthesis/<epic-slug>-conflicts.md`. Produce a short, plain-language brief covering, for
the asker's persona: what the other two personas are claiming that the asker should know,
which of the asker's own commitments have no source in the other two personas' pages, and
which open conflicts the asker should expect to be asked about in a cross-functional meeting.
File the brief as `wiki/synthesis/<epic-slug>-briefing-<persona>.md`. This is the "homework"
artifact — the thing a person reads before walking into a meeting, not a new document type;
it is a synthesis page like any other.

## User preferences

(Empty initially. As the user expresses style preferences — "always include a 'Why this matters' section on concept pages", "never use bullet lists in summaries", "prefer comparative tables for synthesis pages" — capture them here so they persist across sessions.)

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

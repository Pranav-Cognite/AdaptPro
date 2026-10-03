# Wiki Log

Append-only chronological record of operations on the wiki. Each entry begins with `## [YYYY-MM-DD] <op> | <description>` so it's parseable with `grep "^## \[" log.md | tail -N`.

Operations:
- `ingest` — a source was processed into the wiki.
- `query` — a question was answered against the wiki (typically only logged when the answer was filed back as synthesis).
- `lint` — a health check was run.
- `schema` — the schema was modified.
- `shard` — an index was sharded.

---

## [2026-10-02] schema | Added `persona` page type and the "I am a business/tech/product guy" query-session convention; documented `docs/epics/` as the raw-source location instead of `raw/`.

## [2026-10-02] ingest | Ingested `docs/epics/01-knowledge-base/business-use-case.md` and `docs/epics/01-knowledge-base/adr.md`. Created persona pages `knowledge-base-business`, `knowledge-base-tech`, and `knowledge-base-product` (missing-source, no PRD). Filed `knowledge-base-conflicts` (RED): write-promise vs. no-write-tool, plus the missing Product source.

## [2026-10-03] ingest | Revamped the `knowledge-base` epic around OEE for a chemical plant: company changed to Veridion Chemicals (Calder Valley Plant), use case changed to OEE (Availability x Performance x Quality) for Production Line 3, replacing the prior Fjordline Energy / pump-vibration use case. Rebuilt `mock-cdf-project` fixtures (asset hierarchy, OEE + component time series, downtime activities, OEE SOP file) and re-ingested `business-use-case.md` / `adr.md`. Updated all three persona pages and `knowledge-base-conflicts` accordingly; the two open conflicts (auto-work-order promise vs. no write tool; missing Product source) are unchanged in structure, only in subject matter.

## [2026-10-03] ingest | Wrote `docs/epics/01-knowledge-base/prd.md`: data architecture (Cognite OPC UA/SAP/DB Extractors feeding OEE), scoped to the same 3 read-only templates as the ADR, write actions and threshold policy explicitly out of scope. Ingested as `knowledge-base-prd`; replaced the `missing-source` Product persona page with real content. This closes the "missing Product source" gap and collapses the epic's two open conflicts into one: Business's auto-work-order promise against both Product and Tech, who independently agree on read-only scope.

## [2026-10-03] schema | Documented three workflow conventions in SCHEMA.md: ingest is a team action (no automated pipeline), versioning is git commit history (no parallel numbering, sign-off-to-version linkage deferred), and cross-persona briefings (a persona's homework on the other two, filed as `wiki/synthesis/<epic>-briefing-<persona>.md`). Filed a worked example, `knowledge-base-briefing-product`.

## [2026-10-03] schema | Renamed the epic slug from `ask-the-graph` to `knowledge-base` everywhere (directories, file slugs, wikilinks, the product name in prose, now "OEE Chat Assistant") — the prior name was confusing against the actual use case. No content or conflict logic changed, only naming.

## [2026-10-03] schema | Implemented cross-persona briefing as three read-only Claude Code subagents (`.claude/agents/brief-<persona>-on-...md`), replacing the earlier plan of a purely conversational convention. Each agent runs two phases in one invocation: Phase 1 (homework) is the fixed-format brief, filed only on request; Phase 2 (exploration) is open-ended follow-up Q&A, not limited to this epic, and is never filed even on request. Agents are hardcoded to this one use case, not parameterized by epic. Documented in SCHEMA.md.

## [2026-10-03] schema | Added two user preferences: replies stay simple and to-the-point but still go deep on the actual question (not shallow), and agents explain another persona in first-person interview voice rather than narrating about them.

## [2026-10-03] ingest | Added a new `glossary` page type (`wiki/glossaries/`, not epic-scoped): `business-glossary.md`, `product-glossary.md`, `tech-glossary.md`. Each defines one persona's day-to-day vocabulary for the other two personas to read. Wired into all 3 briefing agents' reading list so the interview-voice translation draws on the right terminology.

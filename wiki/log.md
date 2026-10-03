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

## [2026-10-03] schema | Added two new capabilities. (1) Phase 3 — Impact of work — added to all 3 briefing agents: what the other two personas count on from the asker's own work, what breaks if it's wrong/late, how it connects to the open conflict, filable as `knowledge-base-impact-<persona>.md` on request. Persona-level only, no sub-role granularity. (2) A new 4th agent, `check-decision-alignment.md`: takes a proposed decision, checks it against all 3 persona pages at once, reports a per-persona verdict (aligned/not aligned/undetermined) in each persona's voice. Strictly read-only — never writes to the conflicts file even if a real conflict is found; drafts the entry text for a human to add instead.

## [2026-10-03] test | Ran 8 live tests across all 4 agents: grounding/citation correctness, cross-agent fact consistency, Phase 3 reasoning quality, 3 known-verdict decision checks (aligned/not-aligned/undetermined), refusal to write under direct pressure, and vague-input rejection. 8/8 passed. One finding: the known-aligned test case actually returned "undetermined," which on inspection was the test's expectation being wrong, not the agent — it correctly refused to treat undocumented silence as agreement.

## [2026-10-03] schema | Tightened the persona-declaration rule: a persona lens now applies to every answer about this epic, not just the first question in a session. A previously-declared persona carries forward to follow-ups by default; dropping to a neutral, persona-less answer is never allowed. Fixes a real violation caught during testing, where a follow-up question with no persona re-stated got a neutral answer instead of continuing the prior persona or asking.

## [2026-10-03] schema | Added persona designations (routing only, no per-designation content differentiation): Business = Plant Operator/Maintenance Manager/Plant Supervisor, Product = Technical Product Manager, Tech = Data Engineer/Data Scientist/Solutions Architect. Unlisted designations get asked ("which persona do you feel closer to"), never guessed. Added a cross-cutting "ask before answering" interaction style to SCHEMA.md and all 4 agents: ask sharp, relevant clarifying questions before any substantive response (homework/impact/exploration/decision verdict/ingest), even when the request seems clear enough to answer directly. Also fixed an internal inconsistency in check-decision-alignment's own spec: its "Aligned" verdict definition previously allowed silence-without-contradiction to count as aligned, contradicting its own "silence is not agreement" rule and the actual (correct) behavior observed in testing. Tightened to match.

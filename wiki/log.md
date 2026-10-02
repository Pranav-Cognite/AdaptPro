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

## [2026-10-02] ingest | Ingested `docs/epics/01-ask-the-graph/business-use-case.md` and `docs/epics/01-ask-the-graph/adr.md`. Created persona pages `ask-the-graph-business`, `ask-the-graph-tech`, and `ask-the-graph-product` (missing-source, no PRD). Filed `ask-the-graph-conflicts` (RED): write-promise vs. no-write-tool, plus the missing Product source.

## [2026-10-03] ingest | Revamped the `ask-the-graph` epic around OEE for a chemical plant: company changed to Veridion Chemicals (Calder Valley Plant), use case changed to OEE (Availability x Performance x Quality) for Production Line 3, replacing the prior Fjordline Energy / pump-vibration use case. Rebuilt `mock-cdf-project` fixtures (asset hierarchy, OEE + component time series, downtime activities, OEE SOP file) and re-ingested `business-use-case.md` / `adr.md`. Updated all three persona pages and `ask-the-graph-conflicts` accordingly; the two open conflicts (auto-work-order promise vs. no write tool; missing Product source) are unchanged in structure, only in subject matter.

## [2026-10-03] ingest | Wrote `docs/epics/01-ask-the-graph/prd.md`: data architecture (Cognite OPC UA/SAP/DB Extractors feeding OEE), scoped to the same 3 read-only templates as the ADR, write actions and threshold policy explicitly out of scope. Ingested as `ask-the-graph-prd`; replaced the `missing-source` Product persona page with real content. This closes the "missing Product source" gap and collapses the epic's two open conflicts into one: Business's auto-work-order promise against both Product and Tech, who independently agree on read-only scope.

## [2026-10-03] schema | Documented three workflow conventions in SCHEMA.md: ingest is a team action (no automated pipeline), versioning is git commit history (no parallel numbering, sign-off-to-version linkage deferred), and cross-persona briefings (a persona's homework on the other two, filed as `wiki/synthesis/<epic>-briefing-<persona>.md`). Filed a worked example, `ask-the-graph-briefing-product`.

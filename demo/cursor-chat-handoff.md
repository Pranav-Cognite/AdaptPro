# Cursor chat handoff for Claude Code

This is the settled thread from the Cursor conversation about AdaptPro, DevCon 2026, and the 7 October skip-level demo. Continue from these decisions. Do not reopen them unless asked.

## Product

One versioned wiki for the product. Each epic is ingested into that same wiki. Business, Product, and Tech are pages in it, not three knowledge bases.

Lint compares those pages with what was already signed and writes down the conflicts. That list is what people read before a meeting or sprint planning. A human resolves a conflict or signs it. Query is only for opening a conflict, or for reading another side with those conflicts attached.

A source change creates a new version. The old sign-off stays on the old version and does not cover the new one. Which changes void the sign-off must be an explicit rule.

The first epic starts from an empty wiki. Every later epic is ingest, then lint against what is already signed. Query only when someone opens a conflict lint already found. A sprint with no new epic still gets a lint if a document changed.

## What does not hold

- Three self-updating persona wikis, plus “ask the right question,” do not solve the problem. A human already closes gaps in the meeting. The product only helps if it shows the gap before they walk in.
- RAG is not the product. Use it only to fetch passages: related signed claims when the corpus no longer fits in one prompt, evidence attached to a filed conflict, and citations for a question. RAG does not decide alignment.
- Agentic patterns alone are not what makes this accurate or scalable. Agents extract claims from the changed source and draft the three persona pages. A deterministic check on the records decides whether the version is blocked. Each lint looks at the change plus a short list of signed claims, not the whole wiki.

## Story order, for the talk

Tell it in this order. Step 2 is the attempt that fails, not a better product.

1. LLM wiki. Readable. The overview smooths the conflict, and a later sprint cannot reread the whole product.
2. Agentic patterns. Three voices, and they can still declare “aligned” and still reread everything.
3. Claim store, plus a deterministic check on the delta. That is the step that holds accuracy and scale. The store alone is only a database. It is the part not to replace. Retrieval and the sign-off rule can sit around it later.

## DevCon

Theme: Scalability. The claim is that a meeting does not scale across epics, and a check on the delta does. A 25-minute slot is about 20 minutes of talk and 5 minutes of questions. One lesson, on *Ask the graph*. Success is a specific question, not “nice overview.”

## Skip-level demo, 7 October 2026

LLM wiki only. Discuss the downsides. No live model. The wiki is compiled so the failure is repeatable.

- Slides: `demo/slides.html` (arrow keys, `S` for speaker notes)
- Demo code: `src/adaptpro/wiki/`
- Run: `poetry run python -m adaptpro.wiki.server` then http://127.0.0.1:8765
- Compiled files after ingest: `demo/run/wiki`

Click path: Ingest, read Overview (status Ready), ask “Are we ready to kick this off?” on Overview only, ask the work-order question, switch to Every page and ask again, ask about demo tenants with missing file links both ways, Lint (status stays Ready), Ingest again and show the log.

## Fundamental risks still open

- People who benefit from a fuzzy promise will keep the real sentence out of the wiki. Discipline does not fix that.
- A live product changes faster than anyone can re-sign. The void-on-change rule is the design problem.
- One trusted compiled page can shut the argument down when it is subtly wrong.

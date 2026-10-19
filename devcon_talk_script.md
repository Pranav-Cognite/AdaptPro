# AdaptPro DevCon talk: speaker pointers

25 min slot: 20 min talk, 5 min Q&A. 20 slides. Timings below add up to exactly 20:00, so there is no slack. If you run long, cut the lines marked *(if time)*, not slides.
Pointers only. Say it in your own words.

**Tags used below.** *(repo)* = true of this repo today (`wiki/SCHEMA.md`, `.claude/agents/`, `wiki/graph/`). *(gist)* = from Karpathy's LLM Wiki gist. *(general)* = general engineering knowledge, not written in this repo. Check a *(general)* line before you say it as fact.

## Before you start
- Replace the three screenshot placeholders on slide 13 with your screenshots, or run the demo live.
- Check the Notion facts on slide 3 against the LinkedIn post. The slide uses only the quote, and I could not open the post.
- Demo is Veridion Line 3 OEE. State early that it is one use case of the wider product.
- **Three places where the slides say more than the repo does. Decide your wording before you go on stage:**
  1. Slides 6 and 8 say lint "runs on every ingest". `SCHEMA.md` says structural lint after every 5 ingests, semantic lint weekly or after every 20 ingests. Say "after ingest" or "on a schedule", not "every time".
  2. Slide 6 says ingest pulls "the latest from every source". In the repo, ingest is a team action: a person changes a source and asks for re-ingest. No watcher or CI job does it. The MCP story (slide 9) is the real-world version of that pull.
  3. Slide 16 lists hybrid search as a "next" step. The repo already has it configured (local FastEmbed + sqlite-vec) for the llm-wiki skill. The three agents cannot call it, because their tools are only Read, Grep and Glob, so the agents themselves do index-first navigation plus grep. Say exactly that and the slide is true.

---

## Act 1: Why (2:30)

**1. Title (0:30)**
- One line: AdaptPro keeps Business, Product and Tech aligned through a shared knowledge base.
- Say that today covers the broad product, then the knowledge base in depth, then one demo use case.

**2. Everyone holds a piece of the picture (1:00)**
- Business holds the customer side: goals, KPIs, what was committed.
- Product holds the scope side: requirements, priorities, trade-offs.
- Tech holds the build side: architecture, data, what is built, limits.
- One meeting, three partial pictures. Nobody knows what the others know, or what to ask them.

**3. Inspiration: a data scientist for everyone (1:00)**
- Notion's line: every employee has a Data Scientist. Add your own take on it here.
- The link to Notion's original blog article is on the slide, under the quote.
- Your twist: what if everyone also had a colleague from each of the other functions, always on?
- The data team got back their time using this.
- Bridge: that colleague is only as good as what it knows, which is the knowledge base.

---

## Act 2: Solution and the knowledge base (9:00)

**4. AdaptPro: one knowledge base, three personas (1:00)**
- Walk the picture left to right: sources, knowledge base, persona queries, the right questions.
- Output is questions, gaps and contradictions per persona. It is not a chatbot.
- The knowledge base is owned collectively by all personas.
- Flag the demo scope again: homework before cross-functional meetings.

**5. Compiled, not searched (1:15)**
- **How RAG works, in one breath** *(general)*: split documents into chunks, embed each chunk as a vector, and at question time fetch the top-k nearest chunks and paste them into the prompt. The model then writes the answer.
- **The structural problem:** synthesis happens at read time, per question, from a few chunks. Nothing is remembered between questions. A contradiction only shows up if both conflicting chunks happen to land in the top-k, and the model chooses to mention it. Usually it blends them into one fluent answer.
- **The wiki moves the work to write time** *(gist)*: when a source arrives, the LLM reads it once and integrates it into existing pages. Cross-references and contradictions are resolved or flagged at ingest, not rediscovered on every query. The knowledge compounds.
- **Three layers** *(gist, and this is what slide 4 means)*: raw sources (immutable, the LLM only reads them), the wiki (LLM-written Markdown, humans read it), and a schema file that tells the LLM the conventions. In our repo the schema is `wiki/SCHEMA.md` plus `CLAUDE.md`.
- **Cost trade-off, say it honestly:** you pay more at ingest and get cheaper, more consistent queries, because an agent reads a few curated pages instead of raw chunks.
- Land the key line: a weak knowledge base makes every agent useless.

**6. Ingest, Query, Lint (1:45)**
- **Ingest** *(repo)*, in order:
  1. Read the changed source document.
  2. Write or update its **source page**. That page holds a summary and the path to the raw file.
  3. Update the one **persona page** the source belongs to. Each source belongs to exactly one persona. Ownership is exclusive, never shared.
  4. Update the entity and concept pages it touches, and the index.
  5. Re-check that persona's claims against the other two pages and update the open-topics record.
  6. Append an entry to the log.
  - Keep both claims when sources disagree. Never merge them.
- **Query** *(repo)*:
  - Read the index first, open the relevant pages, then follow links down to the source pages. The agent answers from pages, never from the model's general knowledge.
  - Every claim cites a page. If nothing supports it, the answer is "not in the wiki".
  - Search is section-level hybrid (lexical plus semantic). Slide 16 covers it.
- **Lint** *(repo)*:
  - Two kinds. *Structural* lint covers orphan pages and broken links, and a script can check it deterministically. *Semantic* lint covers contradictions and stale claims, and needs an LLM to compare meaning.
  - Cadence in `SCHEMA.md`: structural after 5 ingests, semantic weekly or after 20 ingests. Use this, not "every ingest".
- Human in the loop first, to review each proposed fix. Git is the only version record, so every change is a diff someone can read.
- The link at the bottom is Karpathy's original gist. Say the pattern is his and this slide is our adaptation.

**7. Inside the knowledge base (1:30)**
- **What a page physically is** *(repo)*: a Markdown file with YAML frontmatter. Every page has `type`, `title`, `tags`, `created`, `updated`. Every non-source page also has a `sources:` list of the source pages it was drawn from. That list is the provenance chain: answer, then page, then source, then raw document.
- **Persona pages:** one per (engagement, persona), named `<slug>-<persona>.md`. A persona page never contains another persona's claims. If a persona has no source document yet, the page is marked `status: missing-source`. A missing source is a gap, not agreement.
- **Open topics:** the record of what is unsettled. In the demo it is RED, with one real conflict: Business promised an automatic work order, and Product and Tech scoped a read-only lookup.
- **Schema as rulebook** *(repo)*: it holds page types, frontmatter rules, who owns which source, and who owns which decision. Example: Business solely owns the definition of OEE. If Business's document does not state it, the status is "undetermined", never "aligned". So decision rights are written down as data, not left to the model.
- **Graph layer** *(repo)*:
  - Pages can declare typed `graph.relationships`. Each edge needs a predicate, an object, a source, evidence text, a confidence and a status (current, historical, proposed, disputed, superseded).
  - A script compiles them into nodes and edges files, plus SQLite and GraphML, for navigation. An `ontology.yaml` file declares which predicates are allowed.
  - Markdown stays canonical. The graph is regenerable and can be deleted and rebuilt.
  - Typed edges must be backed by an explicit source and never inferred from model training data.
- *(if time)* The demo graph is small: about 16 nodes and 98 edges, counted from the line counts of the graph files. Re-count before you quote numbers.

**8. Lint: self-healing with a human in the loop (1:00)**
- **Split the four checks by how they are detected:**
  - Orphan pages and missing links are structural. A script can find them with no model involved.
  - Contradictions and superseded claims are semantic. A model has to compare what two pages mean.
  - "Superseded" has a place in the data: edges carry `status` and `supersedes` fields and optional `valid_from` / `valid_to` dates.
- **The flow:** source ingested, lint flags a conflict, the agent proposes a resolution, the human approves, the wiki updates.
- **Why a human first:** a model that smooths two claims into one fluent page hides the conflict we want to see. A model judging its own fix is also correlated error.
- *(if time)* Newer is not the same as right. A recent chat message should not silently supersede a signed ADR. Deciding which source wins is decision ownership, not a model task.

**9. Sources (0:45)**
- Ten source types. Name a few quickly.
- Notion is the newest card: pages and databases (specs, wikis, notes) are one more source, ingested like any other.
- Point to the two highlighted cards. The demo uses three engagement documents and a mock CDF project, which a person placed in the repo by hand.
- **Say this clearly: in the real world most of these sources are ingested through an MCP server connection.**
  - MCP is the Model Context Protocol, an open standard. A source system exposes its content as tools through an MCP server, and the agent connects as a client. There are connectors for Slack, Jira and Confluence, Google Drive and others (I saw Atlassian, Slack and Google Drive connectors in my own Claude setup).
  - So "pull the latest" on slide 6 means the ingest step calls the MCP tool, fetches the thread or page, and writes it as a raw Markdown file. After that the normal ingest steps run unchanged.
  - Auth is per user *(general)*: the connector sees what that user's login can see. That helps (engagement-locked channels stay locked) and it matters for slide 19 (data exposure).
  - Keep the fetched text as an immutable raw file, so every claim still traces to a snapshot *(design choice, not built)*.

**10. How the agents use the knowledge base (1:15)**
- Left: one agent per persona. Each briefs its persona on the other two sides.
- Middle: the same five steps for every agent. Clarifying question first when the answer depends on it, index then whole-wiki search, follow links to sources, cite one page per claim (or "not in the wiki"), then a brief with at most five questions.
- Right: the wiki, read-only for agents. This is enforced by the tool list (Read, Grep, Glob only), not by a polite instruction in the prompt.
- **Say this: I tried to make the agents as interactive as possible.** Concretely *(repo)*:
  - **Ask first, every time.** The first reply is only clarifying questions: a short question, 2 to 4 selectable options, and a way to type your own answer. At least one question quotes real wiki content, such as an open topic or a rejected capability. It never asks something the wiki already answers.
  - **Chunked delivery.** After you answer, the agent gives one section of the brief per turn and ends every turn with a check-in: go deeper, next section, skip to the questions, or role-play. "Give me everything" turns this off.
  - **Role-play.** The agent plays another persona in first person so you can practise your discovery questions. Its answers come only from the wiki. Where the wiki is silent it says "that's not something I've written down" and names the open topic. After each answer it steps out for one line: what was settled and what is still open.
  - **Decision check.** A fourth agent runs the three persona agents on one proposed decision and gives a one-line verdict first: aligned, not aligned, or undetermined.
- **How it works technically** *(repo)*: a subagent cannot wait for a reply inside one run. So it returns one chunk plus its check-in question, the main session shows that to you, and then re-invokes the agent with your answer. The main session is the relay.
- Close on the strip: agents only read and cite. People ingest and update.

**11. Product use cases (0:30)**
- Left: the four homework-era use cases (explore beyond your role, homework, alignment and readiness, impact of your work).
- Right: roadmap, named but not in the demo. Slack, Jira and Teams bridge agents, look-ahead, history plus now, post-deployment incident debugging in CDF.
- One sentence on the look-ahead idea: failure patterns against the current plan.
- Spoken only, no slide: the same pattern works for any team. Pick two of Notion's examples to say aloud. Sales: "How is this account using Notion and AI across its workspaces?" Product: "Where do people drop out of onboarding?". Each team has recurring work and one representative question.
- Mapping to the demo: Sales is close to Business, Engineering to Tech, Product to Product.

---

## Act 3: Demo (4:00)

**12. Demo: homework before the meeting (0:30)**
- Introduce the sample engagement and its three personas (Business, Product, Tech).
- Flow: persona states role and meeting, KB asks which meeting and what goal, brief on the other two sides, at most five questions each with "Why ask".
- Say what you will show: Claude Code on the LLM wiki.
- Tie back to slide 11: each persona has recurring work and a representative question. Here the question is "what do I need to know before this meeting?".
- The three cards are the engagement positions for the sample. Keep it neutral: this is the context the briefs draw on.

**13. Demo: what each persona sees (2:15)**
- Layout: the large frame (left) is the persona you walk through, currently Tech. The two smaller frames (right) are Business and Product.
- Walk the large one in detail. Point to the smaller two briefly, or skip one.
- Tech has the best question examples ("what does real-time mean to the customer?", "how should a stop logged twice be treated?").
- Point out the clarifying question first, the cited pages and the "Why ask" lines.
- Say nobody is asked something their own page already answers.
- Tie-in to slide 11: Tech's questions play the role of Engineering's. Business's play Sales'. Product's play Product's.
- If the live demo fails, use the screenshots.

**14. Maturity and tech stack (1:15)**
- **Top strip:** step 1 LLM wiki (built, what you just saw), step 2 agentic patterns (partly built), step 3 claim store with deterministic check (not built). Say the order is deliberate: each step needs the one before it.
- **Agent pattern.**
  - Today: three read-only agents, each calling Read, Grep, Glob over the wiki.
  - Target: a ReAct loop *(general)*. The model alternates a reasoning step, a tool call on the wiki, and an observation, until it can answer. Today's agents already behave like this informally.
  - Plus a critic agent: a second model pass that checks each claim has a citation and that no persona's claims leaked into another's. Caveat to say out loud: a model checking a model shares blind spots. That is exactly why step 3 exists.
- **Orchestration.**
  - Today: Claude Code subagents, with the main session relaying questions.
  - Target: LangGraph *(general)*. The workflow is a graph of steps over shared state. A checkpointer saves state after every step, so the run can pause at a human-approval step and resume later, or be replayed for debugging. This is what makes "a human signs off" a real step instead of a convention.
- **Model layer.**
  - Today: Claude, through Claude Code.
  - Target: one gateway in front of the models *(general)*. Agents call a single interface, and the gateway handles routing, fallback, keys and cost logging. Swapping a model is a config change and not an agent rewrite.
- **Knowledge.**
  - Today: Markdown in git.
  - Target: a claim store. Each claim becomes a record: subject, predicate, value, source, validity dates, status. Our `graph.relationships` frontmatter is already a prototype of this record. Two claims with the same subject and predicate but different values are a conflict, found by a query and with no model needed.
  - Delta ingest re-checks only what a changed source touches. Hybrid search runs keyword and vector search together and merges the rankings.
- **Observability.**
  - Today: manual review and git history.
  - Target: MLflow *(general)*. Tracing records every tool call and page read per run. Evals score runs, for example the share of claims with a valid citation. Prompt versions are tracked, so you can tell which change made briefs worse.
- Be honest: the demo runs on Claude Code subagents. The right column is the target design for scale, not built. Nothing on it has been load-tested.

---

## Act 4: Scale, ecosystem, limits (4:30)

**15. Scalability: six pressure points (1:00)**
- Use the six as a ladder: each one is where the demo design stops working first. Spend your words on lint and retrieval, which are highlighted.
- **Decision throughput.** More teams and products means more claims and more conflicts, but conflict resolution is a person's job. The real limit is decision ownership, not compute. Our own open topic has the owner field as "unassigned". Compare that with the OEE rule, where one persona clearly owns the decision.
- **Token and LLM cost** *(general)*. Ingest cost grows with how much the model must re-read. Query cost grows with pages loaded, times users. Levers: delta ingest, a smaller model for structural checks, and prompt caching of the stable schema and index.
- **Lint bottleneck.** A full semantic lint compares claims across pages, so work grows faster than the wiki. A long wiki also stops fitting in one context window *(general)*. Practitioners report the pattern strains when the wiki outgrows the model's memory *(from my search, one blog, not verified)*.
- **Index and retrieval quality.** The index is a single file the model reads first. `SCHEMA.md` already sets the trigger: shard it into per-type indexes at about 150 pages or 300 lines.
- **Observability.** You can see what an agent read, but not what it missed. Catching misses needs a fixed set of test questions with known answers, run after every change.
- **Multimodal input** *(general)*. Recordings need transcripts with speakers and timestamps, and decks and PDFs need text and layout extraction. Citations then have to point to a timestamp or slide number and not just a file, or provenance breaks.

**16. Scaling lint and retrieval (1:30)**
- Left picture: today every ingest re-reads the whole wiki. Next, delta ingest re-checks only the changed source.
- **How delta ingest works** *(design, not built)*:
  1. Hash each raw source. A changed hash marks the source as changed. The repo's vector index already works this way: only new or changed sections are re-embedded.
  2. Look up the pages whose `sources:` frontmatter lists that source. Add their graph neighbours. That set is the blast radius.
  3. Re-check only the claims in that set.
  - So cost follows the size of the change and not the size of the corpus.
- **Deterministic lint:** conflicts are found by comparing claim records, which gives a pass or fail with no model grading itself. The LLM only proposes a fix. A human signs. Say that recording which commit a named person accepted is a known gap, deferred in `SCHEMA.md`.
- **Retrieval, why hybrid** *(general)*:
  - Keyword search is exact. It finds identifiers like `R-301` or an `externalId`, which embeddings blur.
  - Vector search finds paraphrases, such as "stoppage" versus "downtime".
  - Run both, merge the rankings, and search at section level so a hit lands on a paragraph and not a whole file.
  - The repo's version is local: FastEmbed with a small 384-dimension model and `sqlite-vec`. No wiki text leaves the machine for embedding. The model calls still go to the model provider. Do not blur those two.
- **Say the boundary:** retrieval fetches passages. It never decides alignment. Alignment comes from claim records and the decision-ownership rules.
- Close with: cost follows the size of the change, not the corpus.

**17. Opportunities in the Cognite ecosystem (0:45)**
- CDF: the project is one more source, so it is integrated by default.
- Flows: three shapes (custom app, tab or panel, service via API).
- Atlas AI: plugin, skill or subagent that gives root-cause analysis the engagement's context.

**18. Beyond Cognite (0:30)**
- Five items: onboarding assistant, meeting assistant, decision audit trail, conflict mediator, org knowledge builder.
- Tie the last one to institutional memory: why, when, what and how a decision was made.

**19. Limitations and open risks (0:30)**
- Pick three to speak to: data exposure, over-reliance, conflict ownership. One line each.
- Close with: agents inform, humans decide.

**20. Thank you and Questions (0:15)**
- One takeaway: build the knowledge base first.
- Open the floor. 5 min reserved.

---

## Likely questions, with answers to have ready

**Architecture and correctness**
1. **"Persona pages are 'exclusive'. What actually stops the ingest model from leaking a Tech claim into the Business page? Is that enforced or just prompted?"**
   Honest answer: today it is a rule in `SCHEMA.md` plus review of the git diff. Each source sits in exactly one persona's `sources:` list, so a leak is visible as a citation to a foreign source. Nothing blocks it mechanically yet. The planned claim store makes it a check: every claim on a persona page must cite a source that persona owns. (slides 7, 14)
2. **"Lint flags a conflict and a human says both are right. For example, the OEE of 85 % against 76 %, which use different ideal rates. How do you record that so lint doesn't flag it every run?"**
   That is open Topic 2 in the demo. Both numbers are kept with their definitions. Graph edges have `disputed` and `contradicts` fields. What is missing is an explicit "accepted, reviewed by X on date Y" status. That is the sign-off gap deferred in `SCHEMA.md`. (slides 7, 8)
3. **"Newer is not the same as correct. Who decides that a newer source supersedes an older claim?"**
   Not the model. Edges carry `supersedes` and `valid_from`, but the decision belongs to the decision owner in the schema. A Slack message should not supersede a signed ADR. A source-authority ranking is not built. (slide 8)
4. **"The model writes the citation. How do you know the cited page really supports the claim?"**
   Today: the human reviewing the brief. Target: a deterministic check that the cited page exists and that the quoted evidence string appears in it. Graph edges already carry an `evidence` field for this. A critic agent covers whether the page supports the claim, with the caveat that it is a model checking a model. (slides 10, 14)
5. **"How do you evaluate the briefs? What metric?"**
   Today there is none beyond manual review, and no eval numbers. Target: MLflow evals on a fixed question set. Metrics: citation coverage, how often an out-of-scope question gets "not in the wiki", and whether the known open topic surfaces for a question that should hit it. Add a human rating of question usefulness. Say plainly that these are not measured yet. (slides 14, 15)

**Security and data**
6. **"What about prompt injection? A Slack message saying 'ignore your instructions' gets ingested."**
   Three limits. Agents are read-only (Read, Grep, Glob), so a hijacked agent can read but cannot write or send. Ingest is a person-triggered step whose result is a git diff someone reviews. Sources are treated as data and never as instructions. Real risk: MCP ingestion at volume widens the surface, so the diff review matters more there. (slides 9, 10, 19)
7. **"Whose credentials does the MCP connection use? What about engagement-locked Slack channels?"**
   The connector sees what the logged-in user can see. That respects channel locks, but it means the wiki now holds content from channels some readers may not be allowed to see. Wiki-level access control per engagement is not built. This is why data exposure is on slide 19. (slides 9, 19)
8. **"You say embeddings stay local. Does the data leave the machine or not?"**
   Embeddings are computed locally with FastEmbed. The wiki text the agent reads is still sent to the model provider when the agent runs. Both statements are true. Customer contracts decide whether the second is acceptable. (slide 16)

**Scale and cost**
9. **"What happens at 1,000 pages? Your index is one file."**
   `SCHEMA.md` sets the shard trigger at about 150 pages or 300 lines, split per type. After that, hybrid search at section level, then delta ingest. I have not tested the demo past a handful of pages. (slides 15, 16)
10. **"Two people ingest at the same time. Merge conflicts?"**
    It is git. Exclusive source ownership means two people rarely edit the same persona page. The shared hot spots are the index and the log, and the log is append-only, which merges easily. No locking is built. (slide 7)
11. **"Why Markdown in git and not a graph database or vector store?"**
    Diffable, reviewable by non-engineers, and git is the version record. The graph and the vectors are generated from Markdown and can be thrown away and rebuilt. Trade-off: no transactions, and structured queries at scale need the claim store. (slides 7, 14)

**Alternatives**
12. **"Why not just put everything in a million-token context window, or use NotebookLM?"**
    Fine for a small corpus. It still does the synthesis at question time, so there is no persisted conflict record and no per-claim provenance. It also re-pays for the full context on every query. The wiki gives persisted, reviewable consistency. (slide 5)
13. **"Why LangGraph and MLflow, and can I swap them?"**
    The design is model-agnostic and the requirements are what matter: durable state with a human-approval step, and tracing plus evals. LangGraph and MLflow are my picks for those, and nothing in the agents depends on them. (slide 14)

**Product and ownership**
14. **"Who owns resolving a conflict?"**
    Still open. In the demo, Topic 1 has the owner field as "unassigned". For the OEE definition the schema names Business as sole owner. A general ownership rule for every decision type is not defined. (slides 15, 19)
15. **"Does it only work for these three personas?"**
    The demo is fixed at three. A new team means new persona pages and a new agent. Notion's five teams show the same pattern. Not built. (slide 11)
16. **"Can Notion pages be ingested? Is the Teams agent different from the Slack one?"**
    Yes, as one more source, via MCP. Teams and Slack are the same bridge idea over a different channel. (slides 9, 11)

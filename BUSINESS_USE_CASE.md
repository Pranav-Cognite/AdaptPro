# AdaptPro — Business Use Case

**Product:** AdaptPro  
**Working subtitle:** Agentic AI at the intersection of Business, Product, and Tech  
**Document type:** Business use case (reference for anyone: intern, hiring manager, DevCon reviewer, future teammate)  
**Status:** Domain 1 locked for MVP; later domains are intentional, not in scope yet  
**Setting for Domain 1:** Cognite-internal product delivery (not a Cognite-branded product for customers)

---

## 1. Why this document exists

This is the source of truth for *what problem AdaptPro is for*, *who it serves*, and *what “done” looks like* for the first slice.

It is not a pitch deck, not an architecture spec, and not a sprint plan. Those come later. If a sentence in this file does not help someone understand the job AdaptPro does in a real cross-functional fight, it does not belong here.

---

## 2. The problem AdaptPro exists to solve

A product manager, a business analyst, and an architect can sit in the same meeting, use the same English words, and still not be talking about the same product.

That is not a communication skills problem. It is a **shared-meaning** problem.

- Business hears *outcomes, commitments, and risk to revenue or reputation*.
- Product hears *scope, user journeys, acceptance, and what ships in this cut*.
- Tech hears *constraints, interfaces, data, latency, failure modes, and what will actually break*.

Each persona is usually right *inside their own language*. The damage happens in the gaps:

| What people think happened | What actually happened |
| --- | --- |
| “We agreed.” | Three people agreed to three different things that share a label. |
| “It’s a simple idea.” | The idea is simple only after someone else’s constraints have been deleted. |
| “Tech is overcomplicating it.” | Tech is pricing a promise nobody wrote down. |
| “Business keeps moving the goalposts.” | Business is translating a customer sentence that never became a requirement. |
| “The docs are fine.” | The business case, PRD, and HLD are each internally consistent and mutually contradictory. |

This happens from intern to CXO. An intern loses the thread because they only see a ticket. A CXO loses the thread because they only see a slide. Both are lossy compression of the same object: **one change to the product**.

AdaptPro’s job is to make that object *one thing* again — and to refuse to pretend alignment exists when it does not.

---

## 3. What AdaptPro is (and is not)

### Is

An **AI-native alignment product** for a single unit of work: **one epic / feature**, taken from a fuzzy idea to an **implementation-ready shared brief**.

It gives three first-class personas — **Business, Product, Tech** — a way to:

1. See the *same* epic in *their* language.
2. See how the other two languages map onto theirs (the “nitty-gritty” of the other domains).
3. Surface contradictions, unpriced promises, and orphaned constraints *before* kickoff.
4. Produce artifacts a human must sign, not a chat they can screenshot.

The same epic is readable at intern altitude (tickets, examples, edge cases) and CXO altitude (decision, risk, investment, what we will not promise).

### Is not

- A generic chatbot with three system prompts and a dropdown for “persona.”
- A replacement for Jira, Confluence, GitHub, or architecture review.
- A Cognite customer product in Domain 1 (it is a tool *Cognite teams* would use on *Cognite work*).
- A promise that AI will “align people.” People still decide. AdaptPro makes disagreement expensive to hide.

---

## 4. Domain strategy

AdaptPro is **not Cognite-specific as a product category**. The durable idea is: *any domain where three languages collide on one piece of work*.

The build strategy is the opposite of a horizontal toy:

| Phase | Domain | Why this order |
| --- | --- | --- |
| **Domain 1 (now)** | **Cognite-internal product delivery** — how a CDF / Fusion / Atlas-adjacent epic is shaped by GTM, PM/BA, and architecture | Real stakes, real vocabulary, demoable to DevCon and to anyone who has shipped software with customers in the loop |
| **Later domains** | Other collision zones (for example: Legal × Product × Security; CS × Product × Support; Finance × Product × Infra) | Same engine, new ontologies and tools. Do not start here. |

“One domain end-to-end” means: **one epic type, full loop, all failure modes, all agentic patterns that that loop actually needs** — not a thin demo of ten industries.

---

## 5. Who it is for

Three **personas** (languages) × a **seniority ladder** (how much of the epic they are allowed to see, and what they are allowed to commit).

### Personas (Domain 1 mapping)

| Persona | Cognite-internal stand-ins | They optimize for | They get punished when |
| --- | --- | --- | --- |
| **Business** | Solutions, Sales, Customer Success, Industry principal, GTM, finance partner | Commitments, differentiation, deal risk, narrative that survives a customer meeting | The company promised a sentence Tech cannot defend |
| **Product** | PM, BA, PMM, design | Scope of *this* cut, UX, acceptance, sequencing, what is out | The PRD is “clear” and still not buildable, or ships something nobody can sell |
| **Tech** | Software architect, applied AI, data modeling, platform | Constraints, interfaces, data reality, operability, failure | They are asked to absorb an unpriced promise as “just engineering” |

A **business analyst** in the original idea sits on the Product side in this mapping (scope, acceptance, traceability) but is a first-class *translator* — AdaptPro treats BA work as the glue, not as a lesser PM.

### Seniority (same epic, different contract)

| Altitude | Example role | What they owe AdaptPro | What AdaptPro owes them |
| --- | --- | --- | --- |
| Intern / new grad | Intern on the epic | Concrete examples, open questions, ticket-level detail | A path *up*: why this ticket exists in the CXO sentence |
| IC | PM, BA, architect, engineer | Precise claims, sources, dissent | A path *sideways*: the other personas’ non-negotiables in their language |
| Lead / manager | EM, PM lead, solutions lead | Tradeoffs and staffing implications | A path *down*: what will hit the floor this sprint |
| Director / VP | Head of product, engineering, or a GTM region | Portfolio fit, sequencing vs other epics | What this epic crowds out |
| CXO | CPO, CTO, CRO, CEO | A decision: fund, cut, re-scope, or explicitly accept risk | A one-page object that cannot hide unresolved contradictions |

**Human-in-the-loop rule:** AdaptPro may *draft* at every altitude. It may not *commit* a customer-facing sentence, a scope cut, or an architectural non-negotiable without a named human in the matching persona.

---

## 6. Flagship use case (Domain 1)

### Name

**Align one epic before kickoff.**

### Working epic (the story we implement against)

**Epic title:** *Ask the graph*  
**One-line intent:** Let a user ask a natural-language question over a customer’s Cognite Data Fusion (CDF) project and get an answer **grounded** in assets, time series, and files — with citations — and **without inventing tag names or asset IDs**.

This epic is fictional enough to ship as a portfolio scenario, and real enough that anyone who has worked near industrial software will recognize the fight.

Cognite Data Fusion (CDF) is Cognite’s industrial data platform: it connects operational and IT data and exposes it as a queryable industrial knowledge graph (assets, time series, files, and the links between them). AdaptPro users in Domain 1 are **Cognite employees shaping a feature**, not plant operators using CDF.

### Why this epic (not a generic “add a button”)

It is a **simple sentence** that detonates all five failure modes at once. That is the point. If AdaptPro cannot hold *this* epic, it cannot claim the original idea.

---

## 7. The five failure modes, instantiated

AdaptPro is not “for miscommunication.” It is for these five, **all of them**, on the same epic. If the product only catches one, it is incomplete.

### 7.1 False-friend language

Same words, forked work.

| Phrase | Business often means | Product often means | Tech often means |
| --- | --- | --- | --- |
| “Real-time” | Fresh enough for a live customer conversation | Feels instant in the UI | Streaming ingest + sub-second queries |
| “Understands the plant” | Fluent, trustworthy answers | A copilot with templates and empty states | Entity resolution, views, access, and retrieval that cannot hallucinate IDs |
| “MVP” | Something we can show in a sales cycle | Three starter questions, English, read-only | A narrow tool surface with an SLO and an eval harness |
| “Source of truth” | “It’s in Cognite” | The user never has to leave the product | A specific view in a specific space — not RAW, not last week’s export |

**AdaptPro’s job:** Detect false friends, force a disambiguation, and write the chosen meaning into the shared brief in all three languages.

### 7.2 Unpriced promise

A commitment that has not been converted into cost, time, data, or operational risk.

In this epic: a GTM one-pager already says *“ask anything about your operations.”* Product has scoped three templates. Architecture has a read-only, citation-required, cluster-local design. Nobody has priced the gap between *anything* and *three templates* as a **promise**.

**AdaptPro’s job:** Lift that gap into an explicit object: *promised vs scoped vs buildable*, with an owner.

### 7.3 Orphaned constraint

A non-negotiable that lives in an architect’s head (or a Slack thread) and never becomes a PRD line or a business-risk line.

In this epic, typical orphans:

- Answers must not leave the customer’s CDF cluster / region.
- Inventing an `externalId` is worse than saying “I don’t know.”
- No writes from the copilot in v1 (a hallucinated write is an incident, not a UX bug).
- p95 latency and citation coverage are launch blockers, not polish.

**AdaptPro’s job:** Promote constraints into the shared brief and into the Business view as *risk language*, not only as engineering preference.

### 7.4 Artifact silos

Three “correct” documents that disagree.

| Artifact | Hidden contradiction on *Ask the graph* |
| --- | --- |
| GTM one-pager | Implies write actions (“create a work order from the answer”) |
| PRD | Read-only, English, three templates, citations required |
| HLD | Tool-calling over the Instances API + file RAG; no write tools registered |

Each document can pass its own review. The epic still cannot ship.

**AdaptPro’s job:** Treat contradiction as a first-class record, not a comment in a meeting. The system does not get to “smooth” it away.

### 7.5 Seniority lossy-compression

- **Downward loss:** CXO says “AI that understands the plant.” By the time it is an intern ticket it is “add a text box on Search.” The *grounding* requirement died on the stairs.
- **Upward loss:** An intern finds that 40% of demo tenants have no file links to assets. That fact never reaches the board slide, which still shows a happy path.

**AdaptPro’s job:** Keep a vertical thread: every CXO sentence maps to evidence and tickets; every blocking intern-level finding can be raised without being “too detailed.”

---

## 8. The job, end to end

One loop. This is what Domain 1 implements.

```text
Idea / customer sentence / slide
        ↓
Ingest context (decks, PRD draft, ADRs, Slack-export, tickets, code pointers)
        ↓
Canonical epic object (claims, scope, constraints, open questions, owners)
        ↓
Persona projections (Business / Product / Tech)
        ↓
Adversarial critique (agents argue; humans see the argument)
        ↓
Contradiction & risk board (nothing unresolved is marked “aligned”)
        ↓
Altitude views (intern ↔ CXO) of the *same* object
        ↓
Human gates (named sign-off per persona / altitude)
        ↓
Implementation-ready brief (and explicitly: what we will not promise)
```

### Entry triggers (any one is enough)

- A PM drops a one-pager and asks “can we kick this off next sprint?”
- A solutions engineer pastes a customer sentence from a call.
- An architect dumps three ADRs and says “this is what v1 can actually be.”
- A CXO forwards a slide: “Make this real.”

### Exit criteria (the epic is allowed to start)

All of the following are true, or explicitly waived by a named human:

1. **One canonical intent** in language all three personas accept.
2. **False friends** in this epic are defined (not left as slogans).
3. **Promised vs scoped vs buildable** is written down.
4. **Constraints** have owners and appear in Business and Product views, not only Tech.
5. **Contradictions** are resolved or listed as accepted risk.
6. **Intern-level** acceptance examples exist; **CXO-level** “will / will not promise” exists.
7. **Sign-offs** from Business, Product, and Tech on the same version of the brief.

If AdaptPro prints “Looks aligned!” while any of (3)–(6) are red, the product has failed its own use case.

---

## 9. Why this must be agentic (not a chat UI)

A single LLM answering “explain this PRD to an architect” is a **translator**. Useful. Not AdaptPro.

AdaptPro is agentic because the *job* is a multi-step, multi-party process with memory, tools, disagreement, and permission. Patterns are used **when the step requires them**, not as a checklist on a slide.

### 9.1 Orchestrated planning (when the work is a process)

An orchestrator turns “align this epic” into a plan: ingest → extract claims → project personas → critique → score → wait for humans → freeze a version.

Without a planner, the user is the workflow engine. That does not survive a board meeting or a messy Confluence dump.

### 9.2 Tools + memory (when claims need evidence)

Agents do not get to invent the estate. They retrieve and write structured objects:

- Read: PRD drafts, ADRs, GTM copy, ticket text, (later) repo paths, design notes.
- Write: canonical epic, persona views, contradiction records, decision log.
- Remember: the last signed version, waived risks, defined false friends.

If it is not in context or in a tool result, it is a **proposal**, labeled as such.

### 9.3 Adversarial persona agents (when the risk is false agreement)

Three specialist agents, plus a critic that is *not* allowed to be “helpful”:

| Agent | Allowed to do | Forbidden to do |
| --- | --- | --- |
| Business agent | Translate to commitments, deal/reputation risk, what Sales will say tomorrow | Quietly shrink a customer-facing sentence to match engineering |
| Product agent | Cut scope, write acceptance, name the user and the non-user | Call a missing constraint “v2” without putting it on the risk board |
| Tech agent | Bind claims to data, APIs, SLOs, failure modes | Accept an unpriced promise as “we’ll figure it out in the sprint” |
| Alignment critic | Fail the run if contradictions are unresolved | Rewrite history so the critique looks clean |

The valuable output is often **the argument**, not a blended paragraph.

### 9.4 Human-in-the-loop gates (when a sentence becomes a commitment)

| Gate | Who | What cannot proceed without them |
| --- | --- | --- |
| Business commit | Named GTM / solutions / CXO delegate | Customer-facing claims, “ask anything,” write-from-chat, timeline in a sales cycle |
| Product commit | Named PM / BA | Scope of the cut, acceptance, explicit non-goals |
| Tech commit | Named architect | Constraints, SLO, eval gates, “what happens if retrieval misses” |
| Altitude publish | Matching seniority | CXO view cannot ship a slogan the intern view contradicts |

Interns can *annotate* and *escalate*. They cannot *sign* a CXO sentence.

### 9.5 Eval / guardrail loop (when “sounds right” is the failure mode)

AdaptPro scores the *state of the epic*, not the eloquence of the prose.

Minimum scores for Domain 1:

| Check | Pass means |
| --- | --- |
| Claim traceability | Every material claim points at a source or is marked `UNSOURCED` |
| Cross-persona consistency | Business / Product / Tech views do not assert opposite facts |
| Promise accounting | Promised ⊇ scoped is false unless a human accepted the gap |
| Constraint promotion | Tech non-negotiables appear in Product acceptance and Business risk |
| Grounding for this epic | “I don’t know” and citation rules are testable, not vibes |
| No false green | Status is not `ALIGNED` while the contradiction board is non-empty |

Refusal is a feature: the system should **decline to declare alignment**.

---

## 10. Artifacts AdaptPro produces

The product is the artifacts (and the argument that produced them). Chat is a view.

| Artifact | Owner persona | Purpose |
| --- | --- | --- |
| **Canonical epic object** | Shared | The one object. Versioned. |
| **Business projection** | Business | Commitments, risks, what we will not say in a room |
| **Product projection** | Product | Scope, journeys, acceptance, non-goals |
| **Tech projection** | Tech | Constraints, interfaces, failure modes, eval gates |
| **Contradiction board** | Critic + humans | Unresolved or accepted-with-owner |
| **False-friend glossary (epic-local)** | Shared | What *this* epic means by contested words |
| **Altitude views** | Shared | Intern packet ↔ CXO one-pager, same version id |
| **Decision / waiver log** | Humans | Who accepted which risk, on which version |
| **Implementation-ready brief** | All three signed | Kickoff packet: build this, do not promise that |

---

## 11. Value

### For the company (Cognite-internal, Domain 1)

- Fewer epics that enter build already forked.
- Fewer customer sentences that outlive the PRD.
- Architect constraints visible while scope can still move.
- CXO and intern looking at the same version, not a game of telephone.

### For a person in the fight

| Person | What they stop wasting |
| --- | --- |
| BA | Rewriting the same acceptance criteria after every “quick sync” |
| PM | Discovering in week 4 that “MVP” meant three different products |
| Architect | Being the person who “says no” without a paper trail |
| Solutions / CS | Finding out on a customer call that v1 cannot do the demo they were handed |
| Intern | Implementing a ticket whose purpose they are not allowed to see |
| CXO | Deciding on a slide that has already shed its constraints |

### What we will measure (even on an MVP)

Qualitative is allowed. Vanity “hours saved” is not the north star.

| Metric | Why it is honest |
| --- | --- |
| **Time-to-signed-brief** for one epic | Did kickoff get a real object, or another meeting? |
| **Contradiction yield** | How many material conflicts were found *before* sprint 1 vs after? |
| **Promise gap count** | Promised vs scoped vs buildable, still open at sign-off |
| **Constraint promotion rate** | % of Tech non-negotiables that appear in Product + Business views |
| **False-green rate** | Times a human had to override `ALIGNED` because the system was wrong *or* times the system was green and kickoff still exploded (both are bugs) |
| **Altitude fidelity** | Can an intern find the CXO sentence that justifies their ticket, and vice versa? |

---

## 12. MVP vs later (no end state)

There is no “finished” AdaptPro. There is a **first honest loop**, then additions.

### MVP (Domain 1, one epic type)

Must be demoable as a *product*, not a notebook:

- One flagship epic: *Ask the graph* (synthetic but realistic corpus: one-pager, PRD draft, two ADRs, a handful of tickets, a GTM snippet that over-promises).
- Canonical object + three persona projections + contradiction board + intern/CXO views.
- Orchestrator + persona agents + critic.
- Tools over a **local knowledge base** (files), not live Jira.
- Human sign-off simulated in the UI (named role, version pin).
- Eval loop that can **fail the run** (claim traceability + no false green).

If the MVP cannot show a **red contradiction board** turning into a **signed brief with an explicit “we will not promise X”**, it is not AdaptPro yet.

### Next (still Domain 1)

- Real connectors (tickets, docs, repo).
- Multi-version diff (“what changed between v3 and v4 of the brief”).
- Stronger evals (held-out contradiction fixtures, regression on false friends).
- Role-based views in a real auth model.

### Later (new domains)

Same loop, new collision: different personas, different false friends, different tools. Do not dilute Domain 1 to look horizontal early.

---

## 13. Non-goals (Domain 1)

- Auto-writing production code or deploying CDF configuration.
- Replacing architecture review, legal review, or security review.
- Unattended customer-facing answers about a real plant (that is a different product; this epic is *about* that class of feature, not a live copilot on customer data).
- “Alignment score” as a vanity dashboard with no contradiction board.
- Supporting ten industries in the MVP.

---

## 14. Why this is the right story to build in public

**Cross-functional reality:** The hard part is not generating text. It is stopping three competent people from shipping three products under one name.

**Agentic substance:** The loop *requires* planning, tools, memory, adversarial specialists, human gates, and evals. If you remove any of those, a specific failure mode in §7 comes back.

**Intern → CXO:** The same object, different contracts. That is rare in both internal tools and portfolio demos.

**DevCon and portfolio, same file:** Domain 1 is Cognite-internal, so the vocabulary is native. The category is not Cognite-shaped forever — Domain 2+ is how the idea generalizes.

---

## 15. The one-sentence contract

> **AdaptPro takes one epic that three languages think they already agree on, makes the disagreement impossible to ignore, and will not call it aligned until Business, Product, and Tech have signed the same version — including what the company will not promise.**

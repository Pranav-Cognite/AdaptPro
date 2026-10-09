# Product Improvement: Capture (Decision Ledger)

> **Status:** Future product improvement — **not planned for implementation now**.  
> **Purpose:** Capture the AdaptPro “Capture” concept as a documented improvement to the core knowledge-base loop, for later prioritization (e.g. post-MVP / DevCon follow-up).

---

## Context

AdaptPro is a persona-based, AI-native product that helps cross-functional teams stay aligned on decisions. The underlying knowledge base follows:

**Ingest → Lint → Query → Capture**

| Stage | Role |
| --- | --- |
| **Ingest** | Pull latest data from sources (docs, Slack, Jira, Confluence, email, meetings, etc.) |
| **Lint** | Detect self-contradictions and keep the knowledge base healthy as it grows |
| **Query** | Let each persona ask questions against the knowledge base |
| **Capture** | Record human decisions and agreements as durable, structured truth |

Without Capture, the loop is incomplete: Ingest/Lint/Query reflect *what was written*, while today’s real alignment often lives only in a Slack “LGTM”, a meeting outcome, or a Jira priority change.

**Talk-friendly one-liner:**  
*Ingest keeps the world in sync; Capture keeps the team’s decisions in sync.*

---

## Problem Capture solves

| Today | Gap |
| --- | --- |
| SoWs, Confluence, Jira, Slack are ingested | Good coverage of *evidence* |
| People decide in chats and meetings | Those outcomes rarely become queryable truth |
| Lint can clean ingested text | New contradictions re-enter via undocumented decisions |
| Personas query the KB | They cannot reliably ask “what did we agree?” or “who still needs to sign off?” |

Capture turns **decision-grade human outcomes** into first-class knowledge — separate from raw evidence, but linted and queryable together with it.

---

## What Capture is (and is not)

### Is
- A **decision ledger**: structured records of what the team agreed
- **High-signal, low-volume** writes (not a dump of every message)
- **Persona-aware**: shared decision, persona-based stance/sign-off
- **Propose → confirm** by default (human accountability)
- Linked to **evidence**, not a replacement for ingest

### Is not
- A second copy of Slack/Confluence/Jira
- Silent auto-write of every heated thread (surveillance risk)
- Opinions treated as decisions
- Implementation work in the current roadmap

---

## Placement in the cycle

```text
Ingest  →  Lint  →  Query  →  Capture
   ↑                               │
   └──── next ingest may re-pull ──┘
         systems updated after capture
```

Practical flow:

1. Stakeholders **query** / discuss (“Are we aligned to ship?”).
2. They reach an outcome.
3. **Capture** drafts a decision object.
4. **Lint** checks it against the existing KB (prior decisions + evidence).
5. Humans confirm → committed as truth.
6. Later **ingest** may mirror the same fact from Jira/Confluence; Capture made it usable immediately.

Lint should run on Capture commits as well as on Ingest — otherwise contradictions re-enter through the write path.

---

## Maintain captures separately

Captures should be maintained as their **own store/layer**, not mixed into the raw ingest corpus.

| Layer | Holds | Updates via |
| --- | --- | --- |
| **Evidence / Ingest store** | Docs, Slack, Jira, Confluence, email, meeting summaries | Automated ingest |
| **Decision / Capture store** | Confirmed decisions, assumptions, owners, status | Human-confirmed capture |

Users still experience **one AdaptPro** (unified Query). Answers can cite both:  
*“Per captured decision D-42… supported by SoW §3 / Jira X.”*

### Why separate
- **Different trust** — ingest is “what was said/written”; capture is “what we agreed”
- **Different lifecycle** — docs re-sync; decisions supersede / amend / retire
- **Different lint rules** — text contradictions vs decision-vs-decision / decision-vs-evidence conflicts
- **Governance** — who can capture ≠ who can ingest
- **Ops** — rebuild ingest indexes without wiping the decision log

### Maintenance principles
1. Separate collection / table / graph space (`evidence_*` vs `decisions_*`).
2. Separate IDs and APIs (`DecisionCapture` CRUD + audit trail).
3. **Link, don’t duplicate** — point at evidence IDs; don’t paste entire threads.
4. Append-oriented history — amend = new version; old decision marked `superseded_by`.
5. **Unified lint** across both stores before commit.

```text
┌─────────────────────┐     ┌──────────────────────┐
│  Ingest store       │     │  Capture store       │
│  (evidence)         │◄────┤  (decisions)         │
│  docs, jira, slack… │ link│  D-1, D-2, …         │
└──────────┬──────────┘     └──────────┬───────────┘
           │                           │
           └──────────► Lint ◄─────────┘
                         │
                      Query
```

**One-liner:**  
*Evidence is discovered; decisions are declared — lint keeps them honest together.*

---

## Persona-aware Capture

Capture should be **persona-aware**, not split into one KB per persona.

- **Evidence is shared**
- **Decisions are shared**
- **Sign-off is persona-based**

Each capture should record how each persona relates to it:

| Field | Example |
| --- | --- |
| Proposed by | Product |
| Needs sign-off from | Business, Tech |
| Status per persona | Business: approved · Product: approved · Tech: pending |
| Persona-specific notes | Business: KPI impact · Tech: API risk · Product: scope tradeoff |

Suggested persona states: `pending` | `approved` | `rejected` | `abstain`

**v1 persona set (product framing):** Business · Product · Tech  
Industrial personas (plant operators, maintenance engineers, etc.) can extend the same model later.

Avoid:
- Three disconnected capture stores that drift apart
- Only one persona allowed to capture (recreates silos)

---

## What else Capture should be aware of

Beyond personas, each capture should carry:

### 1. Decision identity
- Clear statement of what was decided
- Type: `decision` | `assumption` | `dependency` | `risk` | `constraint`
- Lifecycle status: `proposed` → `confirmed` → `active` → `superseded` / `retired`

### 2. Context and scope
- Engagement / project / customer / plant / product area
- Scope boundaries (“applies to Plant X only”)
- Related OKRs, KPIs, SoW clauses

### 3. Evidence links
- Supporting sources (doc, Slack, Jira, meeting summary)
- Conflicting sources (if any)
- Rationale / “why we believe this”

### 4. Ownership and accountability
- Persona sign-off (above)
- Named humans / roles (DRI, approver)
- Expiry or review date (“revisit if historian access slips past Q2”)

### 5. Dependencies and impact
- Blocked by / blocks what
- Downstream impact (timeline, cost, architecture, ops)
- Blast radius if reversed

### 6. Confidence and certainty
- Confirmed fact vs working assumption
- Confidence level
- Open questions still unresolved

### 7. Time
- When proposed / confirmed
- Effective from / until
- `supersedes` / `superseded_by` links

### 8. Permissions and sensitivity
- Internal vs customer-visible
- Confidentiality / need-to-know
- Who can query vs who can amend

### 9. Lint state
- `clean` | `conflict` | `needs_review`
- Which rules failed
- Resolution path (including human-confirmed override)

### 10. Consumption
- Which personas have not yet acknowledged
- Where it should surface next (Slack align check, Jira ticket, board pack)

**Slide-sized summary (five pillars):**  
Capture is aware of **persona · scope · evidence · dependencies · time** (plus trust: permissions + lint).

**One-liner:**  
*Personas answer who must align; the rest answers what is true, for where, until when, based on what, and what breaks if we’re wrong.*

---

## What gets captured

Not every message — **decision-grade artifacts** only:

| Captured | Example |
| --- | --- |
| Decision | “Use OPC-UA for Plant X ingestion” |
| Assumption | “Customer will provide historian access by Q2” |
| Ownership | Business owns KPI definition; Tech owns API contract |
| Dependency | Blocked on security review before go-live |
| Status change | Option A rejected; Option B approved |
| Rationale + evidence | Links to SoW §3.2, Slack thread, Jira CDF-1234 |

---

## Where Capture happens (future surfaces)

Same collaboration surfaces AdaptPro already targets:

- **Slack / Teams** — explicit “capture this” or agent-proposed draft after a long thread (prefer inviteable / designated channels over silent eavesdropping)
- **Meetings** — extract proposed decisions from AI summaries → human confirm
- **Jira** — status/priority/dependency changes that affect cross-persona alignment
- **Explicit UI** — “Record decision” after an Align check

Default UX: **propose → confirm**, not silent commit.

---

## Capture vs Ingest

| | Ingest | Capture |
| --- | --- | --- |
| Source | Systems of record | Live human outcomes |
| Shape | Often messy, long-form | Structured decision objects |
| Trigger | Scheduled / event sync | End of discussion, meeting, ticket change |
| Trust | “What was written” | “What we agreed” (after confirmation) |
| Volume | Broad coverage | High-signal, low-volume |
| Lint role | Lint ingested content | Lint new decision vs KB before commit |

---

## Conflict model (lint on Capture)

Detecting contradictions is not enough; resolution must be explicit:

1. **Flag** — new capture conflicts with Decision D-17 and/or SoW §3  
2. **Propose** — AdaptPro suggests resolution options  
3. **Human owner confirms** — accept, amend, or override with rationale  
4. **Write back** — commit to Capture store with audit trail  

Humans stay accountable; the KB stays coherent.

---

## Illustrative decision object (non-normative)

Future schema sketch only — not an implementation contract:

```json
{
  "id": "D-42",
  "type": "decision",
  "statement": "Use OPC-UA for Plant X ingestion",
  "status": "confirmed",
  "scope": {
    "engagement": "Plant X CDF rollout",
    "appliesTo": ["Plant X"]
  },
  "personas": {
    "business": { "state": "approved", "notes": "Supports uptime KPI" },
    "product": { "state": "approved", "notes": "In scope for MVP" },
    "tech": { "state": "pending", "notes": "Pending security review" }
  },
  "owners": {
    "dri": "tech-lead@example.com",
    "approvers": ["pm@example.com"]
  },
  "evidence": ["sow://§3.2", "jira://CDF-1234", "slack://C123/p456"],
  "dependencies": {
    "blockedBy": ["security-review"],
    "blocks": ["go-live"]
  },
  "confidence": "high",
  "effectiveFrom": "2026-10-09",
  "reviewBy": "2026-12-01",
  "supersedes": null,
  "lint": { "state": "needs_review", "conflicts": ["D-17"] },
  "sensitivity": "internal",
  "audit": {
    "proposedAt": "2026-10-09T12:00:00Z",
    "confirmedAt": null,
    "confirmedBy": null
  }
}
```

---

## Success criteria (when this is eventually prioritized)

Capture is working if teams can reliably answer:

- What did we decide, and why?
- Which personas have signed off / are still pending?
- What evidence supports this, and what conflicts?
- What does this block or get blocked by?
- What happens if this decision is reversed?
- Is this still valid, or has it been superseded?

---

## Non-goals (for now)

- Implementing Capture in the current AdaptPro build
- Auto-joining every chat to scrape decisions without consent
- Replacing Ingest, Lint, or Query
- Fully autonomous resolution of contradictions without human confirmation

---

## Relation to DevCon narrative

For storytelling / roadmap slides, Capture can be positioned as the **fourth stage** that makes AdaptPro a living source of truth for decisions — not only documents — while remaining explicitly **out of current implementation scope**.

Suggested roadmap framing:

1. **Now:** Ingest → Lint → Query (persona-aware Q&A over evidence)  
2. **Later:** Capture (decision ledger + persona sign-off + lint-on-write)

---

## Open questions (parked)

- Minimum viable decision types for a first Capture slice?
- Default persona set per engagement type (software delivery vs plant ops)?
- How Capture interacts with customer-boundary / data residency rules?
- Which surface ships first later: Slack, meeting summary, or explicit UI?
- How aggressively should AdaptPro *suggest* captures vs wait for explicit user action?

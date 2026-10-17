# DevCon demo: homework before the meeting

Hero use case: **homework before a cross-functional meeting** (README use case 2). It is a brainstorm,
not a risk report. The persona first answers two clarifying questions (what meeting, what they want out
of it), then gets a short brief and up to five discovery questions to ask the other two personas, each
tied to something the wiki leaves open. 25 minutes: 20 on stage, 5 for Q&A.

The scenarios use the Veridion Line 3 OEE engagement. The idea does not depend on OEE: swap in any
engagement whose documents are in the wiki.

## Run of show (20 minutes)

| Min | Beat |
| --- | --- |
| 0–3 | The problem: walking into a cross-functional meeting without knowing what the other side knows, and without the right questions. |
| 3–6 | How it is built: three documents plus a CDF project become one wiki per persona. Show the tree and the mock project (`cdf build` passes). Do not build live. |
| 6–16 | Scenarios, one persona at a time (below). Each starts with the agent asking its two clarifying questions, which you answer from the audience or the options list. Narrate while each runs (about 30–45 seconds). |
| 16–19 | The use-case map: nine use cases, two or three live today, the rest next (Slack, Teams, Jira, look-ahead, history-plus-now). Queries in `use-case-queries.md`. |
| 19–20 | Close. |
| 20–25 | Q&A. |

Suggested: run **Tech fully live** (clarifying questions, then brief), and run Business and Product
from the first prompt with the answers already given, or show them as captured output.

## The three scenarios

### Step 1, every persona: the vague opener (shows the clarifying questions)

Use this on stage for at least one persona. The agent replies with only a question, three options and
"Or type your own answer". Then a second question about what you want out of it.

> **Business:** I'm the account lead on Veridion Line 3 OEE (persona: Business). I have a cross-functional meeting coming up and I want to do my homework first.
> **Product:** I'm the Technical Product Manager on Veridion Line 3 OEE (persona: Product). I have a cross-functional meeting coming up and I want to do my homework first.
> **Tech:** I'm a Solutions Architect on Veridion Line 3 OEE (persona: Tech). I have a cross-functional meeting coming up and I want to do my homework first.

Verified 2026-10-17 for all three personas: the reply is only "What kind of meeting are you preparing for?"
with three options and "Or type your own answer", and no brief.

### Step 2: the answers, then the brief

If you want to skip the questions (or save time), use the one-shot versions. These state the meeting and the goal.

| Persona | Agent | One-shot prompt |
| --- | --- | --- |
| Business | `brief-business-on-product-and-tech` | I'm the account lead (Business). I'm preparing for a discovery session with Product and Tech tomorrow. I want to find the right questions to ask. Give me the homework brief and the questions to ask. |
| Product | `brief-product-on-business-and-tech` | I'm the Technical Product Manager (Product). I'm preparing for a scoping session with Business and Tech. I want to find the right questions to ask. Give me the homework brief and the questions to ask. |
| Tech | `brief-tech-on-business-and-product` | I'm a Solutions Architect (Tech). I'm preparing for a customer technical discovery call. I want to find the right questions to ask. Give me the homework brief and the questions. |

What to point at, for Tech: the questions are curious and open ("What does 'real-time' mean to the
customer?", "Which lines at launch?", "How should a stop logged twice be treated?"). The "real-time" and
data-quality questions come from the agent reading the CDF pipeline and source files, not from a document
that already names them as a problem.

## What good looks like (check on stage)

- With a vague request, the first reply is only a clarifying question with options and a type-your-own line.
- At most five questions, each with **Why ask** (a file and the specific gap) and **A good answer settles**.
- The tone is exploratory. No "Conflict 1", "RED" or "mismatch" in the brief. At most one question on the work-order item.
- Nobody asks Product or Tech something their page already states.
- "Which OEE" is asked of Business, never settled by Product or Tech (`wiki/SCHEMA.md`).
- Technical terms are defined inline.
- Nothing is written to the wiki.

## Fallback: captured output

Captured from live runs on 2026-10-17 (questions sections only), one per persona, using the one-shot prompts
above. Model output varies, so treat these as examples of a good run, not fixed text.

<details><summary>Business: questions to ask (discovery session with Product and Tech)</summary>

> **1. To Tech:** When I say "real-time OEE" to the customer, what is the actual freshness of the number your lookup returns? I know there's an hourly workflow that runs the OEE calculation, but what would you be comfortable letting me say?
> **Why ask:** `veridion-line3-oee-cdf-model-and-pipelines` says a workflow runs the extraction and calculation hourly. Neither the tech page nor the ADR states a freshness commitment, and the business page promises "real-time" without defining it.
> **A good answer settles:** The wording I can safely use about how current the OEE figure is.

> **2. To Product:** The customer heard "any line". Your v1 covers Line 3 only. What's your plan for Lines 1, 2 and 4, and in what order? Those lines only have the legacy MES definition (the existing shift-end report) today.
> **Why ask:** The `veridion-line3-oee-cdf-assets` and open-topics pages say Lines 1, 2 and 4 are reactor and extruder only and carry only the legacy definition. The product page scopes only Line 3 and names no rollout for other lines.
> **A good answer settles:** Whether "any line" is a later phase, who owns it, and what I tell the customer in the meantime.

> **3. To Product:** You've said a threshold policy ("what counts as OEE below target") is a prerequisite for any future write capability. What would you need from me and the customer to write that down, and who would own it?
> **Why ask:** The product page and glossary say the policy "does not exist yet". The open-topics Topic 1 records no owner for the work-order item and no next step. This is the one work-order question I'm asking.
> **A good answer settles:** The first concrete input Business has to provide, and whether this becomes a new scoping document or stays out for v1.

> **4. To Tech:** The data has a stop logged twice, a stop with no end time, and short stops (micro-stops of 3 to 8 minutes) that never get logged in SAP. When my customer's supervisor looks at downtime history, what will they actually see, and how should I describe the gaps?
> **Why ask:** The tech page and the glossary say the data is deliberately not clean. The glossary says micro-stops show up only as lost output in Performance, not Availability. Nothing says how the lookup presents these cases to a supervisor.
> **A good answer settles:** What I can honestly promise about downtime history accuracy, and which caveats to raise with the customer first.

> **5. To Tech:** The project is mock data and hasn't been deployed. What has to happen before this runs against Veridion's real Calder Valley data, and how long might it take?
> **Why ask:** The model-and-pipelines page says it is "not deployed" and the SQL "has not run". The tech page says there is no tenant, cluster or credentials. No timeline or deployment step is written anywhere.
> **A good answer settles:** What a realistic first customer demo can show, and what date commitments I should avoid.

</details>

<details><summary>Product: questions to ask (scoping session with Business and Tech)</summary>

> **1. To Business:** When you tell Veridion "OEE", do you mean the SOP number (3,800 kg/h ideal rate, planned downtime excluded, about 85% on Line 3) or the legacy MES report supervisors read today (4,200 kg/h, planned downtime counted as loss, about 76%)? And how should the other number be labelled?
> **Why ask:** `wiki/synthesis/veridion-line3-oee-open-topics.md`, Topic 2, says your use case does not state a definition. SCHEMA.md makes Business the sole owner of that decision.
> **A good answer settles:** The definition I put in the PRD and Tech puts in an ADR entry. It also settles whether the customer sees a nine-point difference from the number they trust.

> **2. To Business:** What does "real-time" mean to a Veridion supervisor: the latest hour, the current shift, or something faster? And is "any line" a v1 expectation, given that only Line 3 has the SOP definition?
> **Why ask:** `veridion-line3-oee-business.md` uses both phrases without defining them. The pipeline page shows an hourly workflow, and the open-topics page says Lines 1, 2 and 4 only have the legacy definition.
> **A good answer settles:** The freshness requirement and the line coverage I write into v1 scope.

> **3. To Business:** The Q4 business review will reference the work-order promise. What do you need to be able to show there for it to count as working? Would a visible threshold with a suggested follow-up satisfy you, or does it have to be an actual SAP work order?
> **Why ask:** `veridion-line3-oee-business.md` names the Q4 review and the shift target but gives no success criterion or target value. `veridion-line3-oee-product.md` says no threshold policy is defined. This is the one question on the open work-order item.
> **A good answer settles:** Whether there is a smaller first step worth scoping, and who owns the target value.

> **4. To Tech:** My PRD says the DB extractor feeds `ts_line3_quality_pct`, but your pipeline has it feed hourly good and reject counts, and a function derives quality. Should I update the PRD's extractor table to match what you built, or is the table the intended design?
> **Why ask:** `wiki/sources/veridion-line3-oee-cdf-model-and-pipelines.md` ("Where it differs from the documents") lists this and two other differences. Neither the PRD nor the ADR names an owner for reconciling them.
> **A good answer settles:** Which of the PRD and the pipeline is the reference for the extractor-to-series mapping, and who updates the other.

> **5. To Tech:** When the downtime history tool returns a stop logged twice (the 09-30 valve fault), a stop with no end time (the 10-14 pelletizer jam) or nothing at all (micro-stops under about 10 minutes), what should it show? Do you want Product to put a rule in the PRD?
> **Why ask:** `wiki/sources/veridion-line3-oee-cdf-activities.md` describes all three cases. The ADR's no-invented-`externalId` and citation rules don't say how to present them.
> **A good answer settles:** The wording and rules for the downtime template, and what Product can promise supervisors about completeness.

</details>

<details><summary>Tech: questions to ask (customer technical discovery call)</summary>

> **1. To Business:** "When the customer says 'OEE target', is that the SOP number (ideal rate 3,800 kg/h, planned downtime excluded) or the legacy MES number their supervisors read after each shift? How should we label the other one?"
> **Why ask:** `veridion-line3-oee-open-topics.md` (open question section). Business's page does not state a definition, and the two numbers differ by about nine points on Line 3.
> **A good answer settles:** Which definition the promise and the target mean. Product can then add a PRD line and Tech an ADR entry.

> **2. To Business:** "What does 'real-time' mean to the customer? Is it fresh within the shift, within minutes, or on demand?"
> **Why ask:** `veridion-line3-oee-business.md` promises "real-time OEE", and the Business glossary says OEE is mostly reported per shift. No page defines freshness.
> **A good answer settles:** The latency expectation the pipelines need to meet, and whether "real-time" needs its own ADR entry.

> **3. To Business:** "The one-pager says 'any line'. Which lines does the customer expect at launch? Lines 1, 2 and 4 only have the legacy definition."
> **Why ask:** `veridion-line3-oee-business.md` says "any line", while the open-topics page says Lines 1, 2 and 4 only have the legacy definition. No page names the launch lines.
> **A good answer settles:** The line coverage, and so how much of the OEE definition question Tech has to resolve per line.

> **4. To Product:** "Your page says a threshold policy is a prerequisite for any write capability. Who defines 'below target', and is it the shift target Business mentions? If a work-order PRD came next, what would it need first?"
> **Why ask:** `veridion-line3-oee-product.md` says the policy "does not exist yet". Neither persona page names an owner or a timeline for it.
> **A good answer settles:** The first concrete input for any later write scope, and who supplies it.

> **5. To Product:** "For downtime history, how should the answer treat a stop logged twice, a stop with no end time, and stops never logged? What would count as a correct answer in your acceptance criteria?"
> **Why ask:** `veridion-line3-oee-tech.md` lists these data quirks. `veridion-line3-oee-product.md` states acceptance criteria only as citations and says nothing about them.
> **A good answer settles:** The rules Tech builds the downtime tool to, and what "correct" means for the Availability breakdown.

</details>

## Known issues to watch for

- Agent definitions may be read at session start. After editing `.claude/agents/*.md`, start a fresh Claude Code session before the talk and test once.
- In one earlier run the Tech agent said the process signals are sampled every minute. They are every 15 minutes (hourly for OEE). Correct it out loud if it happens.
- The "real-time versus hourly" point is the agent's reading of the CDF pipeline files, not something the wiki records. Say so if asked.
- The mock CDF project is not deployed. The demo reads the wiki, not live CDF.
- Rehearse once on the stage machine: each run takes about 30–45 seconds, and the first run after a long idle may be slower.
- The decision check (`check-decision-alignment`) was re-run on 2026-10-17 on a write-path proposal and returned "Not aligned" with sources per persona. Its closing offer still says "draft a new conflict entry"; ignore it or skip the offer.
- `wiki/synthesis/veridion-line3-oee-briefing-product.md` is an old (2026-10-03) filed brief. The agents may read it as a prior example and call it out of date. Do not file new briefs during the demo.
- The PRD's "supervisors read OEE from a separate reporting tool" sentence is only in the open-topics page, not on the PRD source page, so agents cite it second-hand.

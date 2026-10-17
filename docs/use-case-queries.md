# AdaptPro use-case query bank

Generic, engagement-agnostic queries for each AdaptPro use case. They are phrased the way a person asks the knowledge base: first person, in their own role. None of them depend on the Veridion Line 3 OEE sample. Swap in any engagement, customer, or project.

Personas: **B** = Business, **P** = Product, **T** = Tech.

Status: use cases 1 to 3 are covered by the demo agents. Use cases 4 to 7 (Slack, Teams, Jira, look-ahead, history) are named in the README and are not in the demo. Their queries describe the intended behaviour.

---

## 1. Explore work beyond one's role

Understand the parts of an engagement outside your own function, and how your contribution fits the whole.

- **B:** I'm a sales lead and the customer keeps asking "how will this actually be built?" Explain the delivery approach in terms I can repeat without overpromising.
- **B:** What does Tech have to do before the thing I just sold can go live, and which of those steps usually take longest?
- **P:** I own the roadmap. What are the data and infrastructure assumptions Tech is making that could silently invalidate my scope?
- **T:** I'm a data engineer. What does the business actually earn or lose from the feature I'm building, and who on the customer side feels it first?
- **T:** Which of my technical decisions are visible to the customer, and which are invisible to everyone but me?
- **P:** What commitments has Business already made to the customer that I haven't seen written down?

## 2. Understanding impact and the bigger picture

See how your own contribution fits the grand scheme, and what it does to the business and to the other personas.

- **B:** The deal I'm closing has a clause I added. Trace what it changes for Product's scope and Tech's work, down to the first task.
- **P:** I'm cutting a feature to hit a date. Who loses something because of that, and what is the business cost of it?
- **T:** I'm choosing a data model for speed of delivery. How does that choice affect what the business can sell or report in a year?
- **B:** Where does my part of the engagement sit in the end-to-end value chain, and which handoffs depend on me?
- **P:** If my requirements slip by a week, what is the ripple across Business commitments and Tech milestones?
- **T:** What business outcome is my current task ultimately in service of, and how would anyone know if I got it wrong?

## 3. Homework before a meeting, and decision alignment

Prepare for cross-functional meetings, and check whether Business, Product and Tech are all ready and aligned on a decision before it is made.

**Homework before the meeting**

- **B:** I'm meeting the customer's engineering team tomorrow. What will they ask me that I can't answer without Tech, and what is the safe answer today?
- **P:** I'm walking into a design review with architects. Which terms, constraints, and past decisions do I need to know so I don't derail it?
- **T:** I'm joining a steering call with executives. What does each of them care about, and which of my technical risks need translating into business impact?
- **B:** Summarise where Product and Tech currently disagree, so I don't take a side by accident.
- **P:** What open questions from the last meeting are still unresolved, and who owns each one?

**Alignment and readiness on a decision**

- **P:** We're about to change scope by adding a capability. Would Business and Tech both consider that aligned, and what would each push back on?
- **B:** I want to promise the customer an earlier date. Is Product ready, is Tech ready, and who would have to give something up?
- **T:** I plan to swap one core technology for another. What does that do to the commitments Business and Product have already made?
- **P:** Before we sign off, show me where each persona's understanding of "done" differs.
- **B:** If this decision goes wrong, which persona is the first to find out, and how?

**Readiness of each persona behind a decision**

- **B:** Before we commit, is each persona actually ready? Show me what Product still needs, what Tech still needs, and what I still owe them.
- **P:** For this decision, list what each persona must have in hand (data, approvals, capacity, context) to say yes confidently, and which are missing.
- **T:** Which persona is least ready for this decision, and what would it take to get them ready before the meeting?
- **B:** If I asked each persona "are you ready?" today, who would say yes while meaning no?
- **P:** Score the readiness of Business, Product and Tech for this decision, and name the single blocker for each.

## 4. Chat-assistant integrations

### 4a. Slack: a bridge between real people

An agent that joins long cross-persona discussions in a Slack channel, summarises, and keeps the personas aligned.

- **B:** This thread has 60 messages between Product and Tech. Tell me what has been decided, what hasn't, and what I need to do.
- **P:** Tech and Business are talking past each other in this channel. Find the terms they're using differently and restate each side in the other's words.
- **T:** Someone in this chat just agreed to something that has a hidden technical cost. Flag it before it becomes a commitment.
- **B:** Catch me up on this channel after a week away. Only tell me what changes my promises to the customer.
- **P:** The discussion has circled for 30 minutes. Propose the decision that needs to be made, who needs to make it, and what each persona needs to hear first.
- **T:** Which messages in this chat are assumptions someone stated as facts?

### 4b. Teams: bridging personas in meetings and chats

The same bridging role on Microsoft Teams, in channels, group chats and meeting chats.

- **B:** I missed the Teams call between Product and Tech. Give me the decisions, the open disagreements, and the actions assigned to me.
- **P:** Join this meeting chat and warn me when Business and Tech start using the same word to mean different things.
- **T:** During this call someone just committed us to a delivery date. Post a note on what it depends on from my side.
- **B:** After each cross-team meeting, send each persona a short summary written for their own concerns.
- **P:** Which action items from this channel have no owner, and which persona should own each one?

### 4c. Jira: dependency flagging and priority alignment

An agent that reads new and changing tickets, flags cross-persona dependencies and concerns, and aligns priorities.

- **P:** I just created this ticket. Which other tickets, teams or personas does it depend on or block?
- **T:** This ticket looks small to me. What does Business or Product know that makes it more urgent or riskier than it looks?
- **B:** Two tickets I care about are both marked highest priority by different personas. Which one should go first, and what does it cost to reorder?
- **P:** Flag tickets in this sprint whose acceptance criteria depend on a decision no one has made yet.
- **T:** Which tickets are waiting on data, access, or an environment that nobody has requested?
- **B:** Which tickets, if they slip, put a customer promise at risk?

## 5. Foresight and dependency look-ahead

Connect the personas and think many steps ahead to foresee problems and suggest ways to avoid them.

**Foresight and dependency look-ahead**

- **B:** If I agree to this change, what are the next ten things that follow across Product and Tech?
- **P:** Walk the current plan forward. Where does it first break, and which persona notices?
- **T:** Of the dependencies in this plan, which are on the critical path and have no fallback?
- **B:** What's the earliest warning sign that this engagement is heading for a missed expectation?
- **P:** Suggest the cheapest change we could make today that avoids the largest future problem.

## 6. Historical failure patterns versus the current plan

Compare what has gone wrong before with what is planned now.

- **P:** Which past engagements had a plan like ours and ran into trouble? What did they have in common?
- **T:** Which technical failure patterns from previous projects match what we're about to build?
- **B:** Have we made a promise like this one before? What happened, and what did we wish we had said?
- **P:** Which dependencies failed most often in earlier projects, and are any of them in this plan?
- **B:** Which of the lessons we recorded earlier are we about to ignore again?

## 7. Historical knowledge combined with current events

Use accumulated knowledge together with what is happening right now.

- **T:** A new event just occurred (an outage, a requirement change, a staff change). Which historical lessons apply right now, and what should we do differently?
- **P:** Compare this week's status with what the same project looked like at this stage in earlier engagements.
- **B:** The customer just raised a new concern. Has anything similar come up before, and how was it resolved?
- **T:** This week's incident looks familiar. What was the root cause last time, and does it apply here?
- **P:** Given what happened last time a scope change landed this late, what should we do with the one landing now?

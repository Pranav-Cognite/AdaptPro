# Cursor conversation transcript

Every question and every answer from the AdaptPro / DevCon thread, in order. Wording is the conversation as it happened.

---

## 1

**You:** Do you know what is DevCon in Cognite?

**Assistant:**

**DevCon** is Cognite’s annual internal developers conference. It is run by Cogniters, for Cogniters: engineers, product managers, solution architects, and anyone who is “code-curious.”

The day is set aside for technical talks, sharing work, and learning together. The program is built and presented by Cognite employees. It has run for years, including a fully virtual edition in 2021 and an in-person DevCon 2025 in Oslo on 18 September 2025.

It is a company event, not a Cognite Data Fusion feature or API. Cognite Docs do not document it.

A separate, external event is the **Cognite Developer Summit**. The first one was in Oslo on 27 August 2025 and was aimed at customers, partners, and outside developers building on Cognite Data Fusion.

---

## 2

**You:** Ok so I am one of the speakers at DevCon for 2026. And below is my topic and a brief about the same. I have been given a 25 min slot for my talk:

AdaptPro (Agentic AI and LLMs for the intersection of Business, tech and Product)

More often than not you would find a product manager, a business analyst and an Architect speaking their own language and each one of them end up wondering why is it so difficult to put across such a simple idea.

An AI native product with 3 personas to start with (Business, Product and tech) where LLMs and Gen AI helps understand the nitty gritty details of the other domains. This product serves a purpose across levels from intern to CXOs in boardrooms.

I want you to give a constructive critisim of the above idea about being a DevCon talk topic.

**Assistant:**

The pain is worth a DevCon slot. The abstract, as written, will not survive 25 minutes in that room.

DevCon is engineers, architects, and code-curious product people who have already sat through a year of “agentic AI at the intersection of X.” They will grant you the premise in the first minute: a PM, a business analyst, and an architect can share a sentence and still mean three different products. What they will not grant is a product that “helps each persona understand the other domain.” That sentence describes a translator. A translator is three system prompts and a dropdown. Someone in the room will say that out loud.

### What is already strong

The audience is the user. Domain 1 of AdaptPro is Cognite-internal delivery, and this room has lived the fight: a GTM sentence, a PRD, and an ADR that each pass their own review and still cannot ship together.

The deeper claim in your use case is the talk. Alignment is a shared object with contradictions still visible, and the system is forbidden to print “aligned” while those contradictions are open. That is an engineering opinion. “People speak different languages” is a culture observation. DevCon rewards the first and nods through the second.

You also already have the right demo epic. *Ask the graph* is a simple customer sentence that breaks on words this audience knows: real-time, MVP, source of truth, “ask anything,” write-from-chat, citations, cluster boundary. You do not need to teach Cognite Data Fusion. You need to show three internally consistent artifacts disagreeing about it.

### Where the abstract loses the room

**The title is a category, not a claim.** “AdaptPro (Agentic AI and LLMs for the intersection of Business, tech and Product)” tells the agenda reader which buzzwords you will use. It does not tell them what they will be able to do, judge, or steal afterward. A DevCon title should be a sentence they could argue with in the hallway.

**The opening teaches the wrong lesson.** “Why is it so hard to put across such a simple idea?” treats the idea as simple and the people as the bug. Your own failure modes say the opposite: the idea is simple only after someone else’s constraints have been deleted. If you open on communication skills, you will spend the slot defending a chatbot. If you open on three correct documents that contradict each other, the slot becomes a design talk.

**“Intern to CXO” is a second product.** The seniority ladder is real, and it is the fifth failure mode (a CXO slogan that dies on the way to a ticket, and an intern finding that never reaches the slide). In a 25-minute talk it reads as “this is for everyone,” which this audience hears as “this is for no one.” Pick one altitude pair and show the thread. Do not tour the org chart.

**The cast list does not match the product.** The abstract names a product manager, a business analyst, and an architect, then names personas Business, Product, and Tech. In the locked model the business analyst sits on the Product side as the translator, and Business is GTM, solutions, and customer commitments. An architect in row three will notice the slip and start discounting the rest.

**There is no technical spine in the pitch.** Nothing in the abstract says what the system reads, what object it writes, who is allowed to smooth a contradiction, or how you know a green status is a lie. DevCon will forgive an early product. It will not forgive a vision with no artifact. The thing you can already stand behind is narrower and better: a canonical epic, persona projections, a contradiction board, and evals that must fail a fake `ALIGNED` brief.

### What fits in 25 minutes

One epic. One loop. Two failure modes, shown, not listed.

A shape that fits the slot:

1. **Two minutes.** One customer sentence: ask anything about the plant, grounded, no invented tag names.
2. **Six minutes.** Put the GTM line, the PRD, and the ADR on screen. Let the room find the fork themselves: “ask anything” and “create a work order” against a read-only, three-template, citation-required design.
3. **Ten minutes.** Walk the object, not the agents-as-magic. Claims, promised vs scoped vs buildable, an orphaned constraint (no writes, no invented `externalId`, answers stay in-cluster), and a critic that is not allowed to blend the disagreement into a helpful paragraph.
4. **Five minutes.** The eval. Show a polished brief that sounds aligned and fails, then an honest blocked brief that passes. That is the moment the talk stops being a product pitch.
5. **Two minutes.** What a Cogniter can reuse on Monday even if they never open AdaptPro: treat contradiction as a record, and refuse a kickoff while promised, scoped, and buildable are different sets.

Leave the other domains, the full agent taxonomy, and the boardroom altitude for a question or a follow-up doc. If someone asks “does this work for Legal × Security?”, the answer is “same engine, later ontology.” Do not spend the slot there.

### A tighter thesis

Something you can say in one breath, and that an engineer can disagree with:

**Kickoff is a lie when the GTM sentence, the PRD, and the ADR can each be correct and still describe different products. AdaptPro’s job is to keep that disagreement on the record until a named human accepts it.**

Title options in that spirit:

- *Your epic is three products that share a name*
- *Refuse the green check: aligning Business, Product, and Tech before kickoff*
- *Ask anything about the plant: how one sentence forks a PRD, a slide, and an ADR*

The first is the best DevCon title. It is specific, slightly rude, and true.

The idea belongs on the agenda. The version that belongs in the 25 minutes is the contradiction you will not let the model smooth over, demonstrated on one CDF epic this room already understands.

---

## 3

**You:** So I need to put in some effort on how I am going to present this right?

**Assistant:**

Yes. The idea is already strong enough. The work is deciding what the 25 minutes are allowed to contain, and then presenting only that.

Right now the abstract tries to introduce a product category: agentic AI, three personas, intern through CXO. A DevCon audience will treat that as a vision pitch and wait for the part where something breaks. Your job in the talk is to make one disagreement impossible to miss, then show that AdaptPro refuses to smooth it over.

Put the effort into four choices:

1. **One sentence you will defend.** Kickoff is a lie when the GTM line, the PRD, and the ADR can each be correct and still describe different products. Everything else in the talk has to serve that sentence.
2. **One epic on screen.** *Ask the graph.* Show the slide that says “ask anything,” the PRD that scopes three read-only templates, and the ADR that registers no write tools. Let the room see the fork before you explain the product.
3. **One proof.** A brief that sounds aligned and still fails your check, next to an honest blocked brief that passes. That is the moment it becomes an engineering talk.
4. **One thing they can reuse Monday.** Treat an unresolved contradiction as a record with an owner. Do not start the epic while “promised,” “scoped,” and “buildable” are different sets.

Cut the tour. Other industries, the full agent roster, and the boardroom altitude can wait for questions. If you only have time to rehearse one path, rehearse the three documents and the failed green check. That path is the talk.

---

## 4

**You:** What exactly is the expectation of a Decon talk of 25 min?

**Assistant:**

A 25-minute DevCon talk is a peer lesson, not a product launch. Cognite has not published a formal speaker rubric for it, so this is the bar that event actually sets: an internal conference, built and presented by Cogniters, for people who code and people who are code-curious. Organizers have historically coached speakers on storytelling. Confirm with them whether your 25 minutes include questions. Plan on about 20 minutes of talk and 5 of questions unless they say otherwise.

The room is giving you one working session of attention. They expect to leave able to retell one idea and reuse one piece of it on their own epic. They do not expect a tour of AdaptPro, a roadmap, or a definition of agentic AI.

What “good” looks like in that slot:

- **One claim they can argue with.** Yours is that kickoff is false when the GTM line, the PRD, and the ADR can each be correct and still describe different products.
- **One concrete case from Cognite work.** *Ask the graph* is enough. The audience already knows the vocabulary, so you spend the time on the fork, not on what Cognite Data Fusion is.
- **Something on screen that is not a metaphor.** Three artifacts that disagree, then a brief that sounds aligned and still fails the check. A talk that only describes the product will feel like a pitch. A talk that shows the disagreement will feel like engineering.
- **An honest boundary.** Say what exists and what is still a design. This audience trusts a narrow, true demo more than a wide, future one.
- **A Monday action.** One practice they can use without installing anything: keep the contradiction on the record, and do not start while “promised,” “scoped,” and “buildable” are different sets.

What wastes the slot:

- Defining LLMs, agents, or the three personas in the abstract.
- Covering intern through CXO, or later domains.
- A live demo you have not rehearsed to the minute. If the demo can fail, use screenshots or a recorded path and narrate it.
- Ending on “and we are building a platform.” End on the check that refuses to go green.

A 25-minute shape that matches the expectation:

| Minutes | Job |
| --- | --- |
| 0–2 | The customer sentence, and why it feels simple |
| 2–8 | The slide, the PRD, and the ADR, side by side, until the fork is obvious |
| 8–16 | The shared object and the critic that is not allowed to smooth it |
| 16–20 | The fake green brief that fails, and the blocked brief that passes |
| 20–25 | The one practice to steal, then questions |

Success is a sharp question, not applause. Someone asking “where do you store the waiver?” or “what if Sales has already said it to the customer?” means the talk did its job. Silence and “cool product” means it stayed a pitch.

---

## 5

**You:** Ok so I want to keep the last 5 min open for questions

**Assistant:**

Then the talk itself is 20 minutes. Minute 20 is a hard stop, even if a slide is still up.

Use the time like this:

| Minutes | What you do |
| --- | --- |
| 0–2 | One customer sentence: ask the graph, grounded, no invented tags. It sounds simple. |
| 2–7 | Three artifacts side by side. The GTM line says “ask anything” and implies a write. The PRD is read-only, three templates, citations required. The ADR registers no write tools. Stop talking long enough for the room to see the fork. |
| 7–14 | The shared object: promised, scoped, and buildable as three different sets. One orphaned constraint, such as “inventing an `externalId` is worse than saying I don’t know.” The critic is not allowed to blend that into a helpful paragraph. |
| 14–18 | The proof. A brief that sounds aligned and fails the check. An honest blocked brief that passes. |
| 18–20 | One sentence to leave with: do not kick off while those three sets disagree, unless a named person has accepted the gap. Then stop and take questions. |

Hold these back on purpose. They make better questions than slides:

- What if Sales has already said “ask anything” to the customer?
- How does an intern finding reach the CXO slide?
- Why is this agents and not three prompts?

If nobody asks, use one of those yourself: “The question I usually get next is what happens when the sentence is already in a customer meeting.” That keeps the last five minutes a conversation, which is what you saved them for.

---

## 6

**You:** Another thing to consider is that the theme for this year's DevCon is Scalability

**Assistant:**

Scalability is the reason this talk belongs on this year’s agenda. It is the cost of catching a forked epic by hand, not how many tokens the agents use.

One architect, one PM, and one solutions lead can sit in a room and catch “ask anything” against a read-only ADR. That meeting does not survive the next forty epics. The same false friends show up every time: real-time, MVP, source of truth, “the model understands the plant.” The constraint dies on the way from a CXO sentence to a ticket, and nobody reruns the meeting. Manual alignment is a hero process. Hero processes do not scale.

The line that ties AdaptPro to the theme:

**You can scale teams, epics, and customer promises. You cannot scale a meeting that is the only place the three documents get compared. The thing that scales is a check that refuses to go green while “promised,” “scoped,” and “buildable” still disagree.**

Put that in two places, and nowhere else:

- **Minute 0.** After the customer sentence, one beat: “We already know how to catch this once. We do not know how to catch it on every epic in flight. That is the scaling problem.” Then go straight to the three artifacts.
- **Minute 18.** Close on the same beat. The Monday practice is the scalable object: a contradiction with an owner, and no kickoff until a named person accepts the gap. The agents are how the check runs without booking the same three people again. The sign-off stays human, because a commitment that nobody owns does not scale either.

Leave throughput, multi-agent diagrams, and “AI at scale” off the slides. If the room wants architecture, it will ask in the last five minutes. The honest answer is that the scale you are claiming is organizational: one canonical epic, many readers, and a critic that is not allowed to smooth the fork.

---

## 7

**You:** So basically my idea is to for cross-functional teams to come in prepared by doing their home work on how to present their work to with cross-fucntional teams. For this I basically want to build a self-updating and self-maintainable knoweledge base for 3 which powers 3 personas (Business, tech and product).

**Assistant:**

The useful part is the homework. The knowledge base is the shelf the homework is built from. If the knowledge base becomes the product, the talk slides back into “three personas chatting with a wiki.”

What you want people to do is real: before a cross-functional meeting, Business, Product, and Tech each show up having already seen how their work lands in the other two languages. That is a better behavior than discovering the fork live in the room. It also fits the scalability theme. You cannot put those three people in a prep meeting for every epic. You can hand each of them a briefing generated from the same sources.

A self-updating knowledge base does not do that job by itself. A knowledge base stores what was written. Your failure mode is that the GTM page, the PRD, and the ADR are all stored, all current, and all in conflict. A base that maintains itself will keep all three and, when someone asks “are we aligned?”, blend them into a fluent answer. Fluency is how false agreement scales.

Keep one corpus, not three. The sources are the GTM note, the PRD, the ADR, the tickets, the Slack thread. Business, Product, and Tech are three readings of that corpus. The moment each persona has its own knowledge base, you have rebuilt the silo and given it a refresh job.

“Self-updating” should mean one specific thing: a source changed, so the claims are extracted again, the contradiction board is rebuilt, and a previous `ALIGNED` status is revoked until a named person re-signs. It should not mean the wiki rewrites itself and stays green. Someone still owns a customer sentence, a scope cut, and a constraint. Maintenance without an owner is how a knowledge base rots at scale.

The homework, then, is a generated brief for each persona, from that one object:

- What the other two will hear you promising.
- Which of your claims have no source.
- Which of your constraints never appeared in their document.
- The question you should expect in the room.

For *Ask the graph*, Tech’s homework is not “here is the ADR in simpler words.” It is: “GTM still says ask anything and create a work order. Your ADR registers no write tools. If you walk in with only the ADR, Sales will leave believing the work order is in v1.”

That is the 20-minute talk. Minute 0 is the meeting people walk into unprepared. Minutes 2–18 are one epic, one corpus, three briefs, and a check that drops from green when the one-pager changes. The close is the scale claim: the prep meeting does not scale; a brief that goes stale on purpose does.

---

## 8

**You:** Can you just tell me in a straight forward manner if what I am telling makes sense?

**Assistant:**

The homework part makes sense. The self-updating knowledge base, as the product, does not.

People showing up already knowing how their work sounds to the other two functions is a real problem, and it scales better than another prep meeting. That part is sound.

A knowledge base that updates itself and “powers” Business, Tech, and Product does not solve it. The documents are already the knowledge base. They stay wrong together because they disagree, not because they are hard to find. A base that maintains itself will store the disagreement and answer it smoothly.

What makes sense is one set of sources, three briefs generated from it, and a status that turns red when a source changes. The briefs are the homework. The knowledge base is just where the sources live.

---

## 9

**You:** Actually my idea was to build the self-updating and self-maintaing knowledge bases using LLM wiki. I want to implement the ingest-query-lint process. End of the day, I need the user to be able to ask right questions to each of these knowledge bases to get the best out of it.

**Assistant:**

Ingest, query, and lint make sense. Three knowledge bases whose purpose is “ask the right question” do not.

Karpathy’s LLM wiki is a real loop: ingest a source, compile it into wiki pages, query those pages, and lint for contradictions, stale claims, and gaps. Lint is the part that matches your problem. Ingest is what makes it keep up when the PRD or the one-pager changes.

Split that into a Business wiki, a Tech wiki, and a Product wiki, and lint only cleans each one. Each wiki will read as coherent. “Ask anything” and “no write tools” will both look healthy, because they never land on the same page. The fork you care about is between the wikis, so the lint that matters is a cross-check. One wiki, three sections, and a lint that fails when those sections disagree.

The last requirement undoes the homework. If the user has to already know the right question, they are back to walking into the meeting unprepared. Query is how they drill in after lint has handed them the question. Lint produces “GTM promises a work order; the ADR has no write tool.” Query is them asking what that means for their own doc.

---

## 10

**You:** Can you please tell me in a striaght forward way. You are beating around the bush way too much. Please be straight forward

**Assistant:**

No. That idea does not hold.

Ingest-query-lint is a fine way to maintain a wiki. It is the wrong product. Three wikis will each look clean while disagreeing with each other, and "ask the right question" assumes the user already knows what they are missing. That is the original problem.

---

## 11

**You:** Ok but there is always going to be a human in the loop right? That is how ultimately if there still exists a gap it is going to be bridged

**Assistant:**

Yes, a human has to close the gap. That does not fix the idea.

A human already closes it today, in the meeting. The product only helps if it shows them the gap before they walk in. If they still have to ask the right question, the human is doing the same job as before, with a wiki open.

---

## 12

**You:** Ok then what do you suggest?

**Assistant:**

Build one wiki per epic. Ingest the GTM note, the PRD, and the ADR into it. Business, Product, and Tech are three pages in that same wiki.

Lint compares those three pages and writes down the gaps: what conflicts, who owns it, and what question each person must answer before the meeting. That list is the homework. They open it and already see the gap.

Query is only for drilling into a gap that is already on the list. A human then changes a source or signs the gap. When a source changes, ingest runs again and the old sign-off is void.

---

## 13

**You:** Tell me in a straight forward manner

**Assistant:**

Build one wiki for the epic. Lint it, and hand the person the conflicts before the meeting. Let a human resolve them.

---

## 14

**You:** Ok so how exactly is this going to help. Please explain

**Assistant:**

It helps by showing the conflict before the meeting, while there is still time to change a document or explicitly accept the risk.

Take *Ask the graph*. The GTM note says a user can ask anything and create a work order. The PRD says three read-only templates. The ADR has no write tool. Today those three documents sit in three places. People read their own, meet, and leave thinking they agreed. The work order promise shows up later, in a customer conversation or in a sprint, when changing it is expensive.

With one wiki, all three documents are on the same epic. Lint writes the conflict down: GTM promises a write, Product scoped read-only, Tech has no write tool. Business walks in already seeing that their sentence cannot be built. Product walks in already seeing that "read-only" never reached the customer-facing page. Tech walks in already seeing that they are about to be asked to absorb an unpriced promise.

The meeting then starts from that list. Someone cuts the work-order sentence, or someone signs that the gap is accepted and names an owner. Either way, the decision is made before kickoff.

If the GTM note changes again next week, ingest runs, the old sign-off drops, and the conflict is back on the list. The agreement does not silently survive a later edit.

---

## 15

**You:** ok so it can be done sprint wise is also right?

**Assistant:**

Yes. Run it at the start of each sprint, on the same epic.

A new wiki every sprint would throw away the sign-off. The sprint check is a fresh lint of what changed: new tickets, an edited PRD, a decision in Slack. If nothing conflicts, the previous sign-off stands. If something conflicts, the sign-off drops and the team resolves it before the sprint starts.

---

## 16

**You:** Ok but I want this for a product that is being developed. So a product would typically be developed across multiple sprints and epics. And addtionally in all the areas i.e business,tech and product every epic would require the context of the previous epic and we would be creating a lot of epic wikis right?

**Assistant:**

No. One wiki for the product, not a new wiki per epic.

A product is developed across many epics and sprints, and each epic depends on decisions already made. Those decisions have to stay in one place. Epic 2 needs to see what Epic 1 already promised, scoped, and signed.

Each epic is a set of pages inside that product wiki. A sprint is a fresh lint of the pages that changed. When a new epic is ingested, lint checks it against the earlier epics. If the new epic breaks a signed promise or constraint, that conflict goes on the list before the sprint starts.

---

## 17

**You:** Ok so the for the every 1st epic we will have an empty wiki. And this is will be the very first ingest. So basically what you are saying is ingest-query-lint should be followed for every epic right?

**Assistant:**

Yes. The first epic starts with an empty wiki, and that ingest is the first one.

Every epic after that follows the same loop. Ingest the new sources, then lint them against what is already in the wiki. Query only when someone needs to open a conflict the lint already found. A sprint with no new epic still gets a lint, because a document may have changed.

---

## 18

**You:** Ok so can you help me understand how and what problems does this solve compared to my approach which I had suggested?

**Assistant:**

Your approach stores each side’s documents and waits for someone to ask a good question. This approach compares the sides and hands over the conflict before anyone has to ask.

| Problem | Your approach | This approach |
| --- | --- | --- |
| Business, Product, and Tech disagree | Three knowledge bases each stay internally clean. “Ask anything” and “no write tool” never meet, so both look fine. | One wiki holds all three. Lint compares them and writes the conflict down. |
| People walk into the meeting unprepared | They still have to think of the right question. If they don’t, the gap stays hidden. | The lint list is the homework. The gap is already on it. |
| A human closes the gap | The human does the same job as today: notice the gap, then resolve it. | The human only resolves a gap that is already named, or signs it and owns it. |
| The next epic contradicts the last one | A new epic wiki cannot see the previous epic’s signed promise. | The new epic is ingested into the same product wiki and linted against earlier epics. |
| A document changes after you agreed | Each base updates itself and still looks healthy. | Ingest runs again, lint runs again, and the old sign-off drops. |

The ingest-query-lint tooling can be the same. The difference is what lint is required to compare, and what the person receives before the meeting.

---

## 19

**You:** Ok so if a techie is curious to understand the busines or the product side of things are you saying even in that case your approach makes more sense?

**Assistant:**

Yes. A techie who wants to understand the business or product side queries those pages in the same wiki. A separate knowledge base is unnecessary for that.

The answer they get is the business page plus any conflict lint already found with Tech. So “the business wants a work order created from the answer” arrives with “your ADR has no write tool.” They learn the other side, and they learn where it breaks. A Business-only wiki would teach them the promise and leave out the break.

---

## 20

**You:** Ok so what are the other opportunities you see in this product being a real hit?

**Assistant:**

The meeting list is the start. It becomes a hit when the same wiki is the place a product’s promises, scope, and constraints stay tied together across epics.

Four opportunities matter.

**A new person can learn the product without inheriting a lie.** A techie, a new PM, or an intern asks what the business wants. They get that page and every place it already conflicts with Product or Tech. That replaces the oral history that walks out when someone leaves.

**A signed gap stays signed.** “We will not promise a work order in this version” is a record with a name and a date. The next sales conversation and the next epic both see it. Most of the damage happens because that decision lived in a meeting and then disappeared.

**A lead can see alignment debt.** Across every epic in the product, which conflicts are still unsigned? That is the scalability story. One red epic is a meeting. Twenty red epics are a portfolio problem, and today nobody can see the list.

**People trust it because it will not say “aligned” to be helpful.** The first time it waves through a forked epic, the team stops opening it. The hit is a lint result the team believes enough to block a sprint on.

It sticks only if a red lint has a consequence. If the team can ignore the list and start the sprint anyway, it is another wiki.

---

## 21

**You:** What are some downsides or areas of improvement you can think of which can turn out to be critical?

**Assistant:**

The critical risks are the ones that make a green result a lie, or make people stop looking at a red one.

**Missing sources look like agreement.** Lint can only compare what was ingested. If the real promise was said on a call and never written down, the wiki goes green. An empty conflict list has to mean “these sources do not conflict,” and any missing PRD, ADR, or GTM note has to stay red. A blank wiki is not an aligned product.

**Ingest will try to clean up the conflict.** The model’s instinct is to merge “ask anything” and “read-only” into one sensible page. If ingest does that, the fork is deleted before lint runs. Ingest has to keep both claims, with their sources. Lint reports the clash. It must not rewrite the pages to make the clash go away.

**A waiver can become a rubber stamp.** A human can sign every gap and the team continues. If a signature has no name, no date, and no later visibility, the product is a log of decisions nobody will defend. A signed gap has to remain visible on the next epic and on the lead’s list.

**Noisy lint gets ignored.** If every sprint produces ten vague conflicts, the team will skip it. Miss one real fork and they will never trust it again. The lint has to be tested on planted contradictions, including a polished brief that sounds aligned and must still fail.

**A copied wiki rots.** If Confluence, Jira, and Slack remain the real documents, this wiki is a second copy and it will be stale by the next sprint. It has to read those sources, or sprint planning has to look at this wiki. A parallel copy will lose.

---

## 22

**You:** Does this help with Sprint planning for all the 3 personas?

**Assistant:**

Yes, at the start of planning. It does not plan the sprint. It tells each persona whether the sprint they are about to commit still matches what was signed.

**Product** sees which stories conflict with the GTM promise or the ADR, and which promised behavior is simply not in this sprint.

**Tech** sees which tickets carry an unpriced promise or a constraint that never made it into the story, before those tickets are accepted.

**Business** sees what this sprint will actually deliver against the customer sentence, including what was dropped. Business does not have to attend planning to see that. The list is the update.

If the lint is red, planning starts by resolving or signing those items. If it is green, planning proceeds as usual.

---

## 23

**You:** So this entire thing is going to be version controlled right?

**Assistant:**

Yes. The wiki has to be versioned, and a sign-off has to point at one exact version.

That version includes the sources, the Business, Product, and Tech pages, and the lint result. When any of those change, the version changes and the previous sign-off no longer applies. The old version stays, so you can still see who signed it and what the documents said then.

---

## 24

**You:** The critical limitations that you mentioned above are something I can and I will take care of. Do you think there is anything that can go wrong fundamentally?

**Assistant:**

Yes. Three things can still break it after you handle those limitations.

**People often need the gap to stay fuzzy.** A deal, a commit, or a roadmap is easier while “ask anything” has not been pinned down. The product exists to pin it down. If the team’s incentive is to keep it vague, they will route around the wiki even when the lint is right.

**A live product changes faster than anyone can re-sign.** Every real edit voids the sign-off. Tickets and PRDs change all week, so the wiki stays red, or you decide some edits do not count. That choice is the product. There is no setting where the wiki is both current and signed.

**One trusted wiki can shut the conversation down.** Three conflicting documents at least force people to argue. One current version that reads well will be treated as the decision. When that version is subtly wrong, the team stops arguing, and the wrong page is what they build.

---

## 25

**You:** 1. Need people to build discipline here other wise it would be difficult
2. How are the changes ingested is something that would need to be worked upon

**Assistant:**

Your first point is right, with one limit. Discipline gets people to write things down and to look at the lint. It does not help when someone is better off if the promise stays vague. Those people will keep the real sentence out of the wiki.

Your second point is the real design problem. Getting changes into the wiki is buildable. The hard part is which changes void the sign-off. If every ticket edit voids it, the wiki stays red. If too few edits void it, a real change slips through while the old signature still stands. That rule has to be explicit.

---

## 26

**You:** Ok so I actually want to stick to your approach this makes more sense as a whole thing

**Assistant:**

Stick to this: one versioned wiki for the product. Each epic is ingested into that same wiki, and Business, Product, and Tech are pages in it.

Lint compares those pages with what was already signed and writes down the conflicts. That list is what people read before the meeting or sprint planning. A human resolves a conflict or signs it. Query is only for opening a conflict, or for reading another side with those conflicts attached.

A source change creates a new version. The old sign-off stays on the old version and does not cover the new one. Which changes void the sign-off has to be an explicit rule, or the wiki is either always red or quietly wrong.

---

## 27

**You:** So coming to the theme of Devcon this year i.e Scalability, how scalable is LLM wiki implementation and what other alternatives can I consider to build a consolidated knoweledge base of business, product and tech?

**Assistant:**

An LLM wiki scales to one product team and a modest set of documents. It does not scale to a product that keeps growing sprint after sprint if every lint re-reads the whole wiki.

Karpathy’s pattern works by reading an index, opening a handful of pages, and occasionally asking the model to health-check the corpus. One ingest already rewrites many pages. That is fine for the first epic, where the sources are a slide, a PRD, and an ADR. It gets worse as tickets, Slack threads, and later epics accumulate. A full-wiki lint then costs more, misses more, and starts summarizing away the exact sentence that conflicted. Git scales the history of the markdown. It does not scale the model pass.

The version that scales is the one already in your schema. Store claims, promise gaps, constraints, contradictions, and sign-offs as records, each tied to a source and a version. Business, Product, and Tech pages are views rendered from those records. The LLM only extracts claims when a source is ingested. Lint is a check on the records: promised versus scoped versus buildable, a constraint that never appears in the other two views, two claims that assert opposite facts. A sprint lints what changed against the signed set. It does not re-read the product.

Two other options lose the actual job:

- **Search over the documents** scales questions. It does not notice that two documents disagree.
- **Three maintained wikis** scale writing. They hide the cross-persona conflict.

Use the LLM wiki as the reading surface for the demo. Keep the records as the thing that is versioned, signed, and linted. That is the scalability claim for DevCon: the corpus can grow, and the check stays on the delta.

---

## 28

**You:** Does it make sense to have a RAG based approach for this?

**Assistant:**

As the product, no. As the way a query finds the source text, yes.

RAG retrieves similar passages and the model writes one answer. That is useful when a techie asks what the GTM note actually says. It is a bad fit for the check. Similar passages get blended, so “ask anything” and “no write tool” come back as one fluent paragraph. The conflict disappears in the answer.

Keep retrieval behind query, pointed at a specific claim or conflict that lint already stored. Do not use it to decide whether the epic is aligned. That decision stays on the records.

---

## 29

**You:** Can you help me understand what other agentic design pattern can be used to address the shortcomings of LLM wiki approach?

**Assistant:**

The LLM wiki fails because one model rewrites the whole corpus and then answers in one voice. These five patterns split that job so the model cannot do that.

**Planning, on the delta.** An orchestrator reads only what changed since the signed version and builds a short plan: extract claims from those sources, compare them to the signed set, stop. It does not health-check the whole wiki. That is what makes a sprint lint scale.

**Tool use with a write rule.** The extractor may append a claim and attach its source. It may not edit a claim owned by another persona, and it may not delete a conflict to make the page cleaner. The wiki text is rendered from those records afterward. Ingest stops being a rewrite.

**Multi-agent, with no shared pen.** A Business agent, a Product agent, and a Tech agent each write only their own projection. A critic compares the three and files conflicts. None of them is allowed to merge the projections into one story. The argument stays on the record, which is the failure of a single compiled wiki.

**A separate evaluator.** The writer can draft a brief that sounds aligned. A different step runs the checks you already defined: promised versus scoped versus buildable, orphaned constraints, opposite claims. The writer cannot override a failed check. That is what stops a fluent page from going green.

**Retrieval only as evidence.** When the critic files a conflict, a retrieval tool pulls the exact passages. Query uses the same tool to show those passages. Retrieval is not asked “are we aligned?”

Human sign-off stays the last step, on that version, after the evaluator passes or a named person waives a specific conflict.

---

## 30

**You:** Ok so can you help me understand where exactly can I use the RAG??

**Assistant:**

Use RAG only to fetch passages. Something else decides what those passages mean.

**When a new source is ingested into a wiki that no longer fits in one prompt.** RAG pulls the signed claims and passages that might relate to it, such as earlier text about work orders or writes. The extractor still writes new claims only. The critic compares the shortlist. RAG does not decide that they conflict.

**When a conflict is filed.** RAG attaches the exact lines from the GTM note, the PRD, and the ADR to that conflict. The person opens the conflict and sees the sentences, not a summary.

**When someone asks a question.** “What did Business say about creating a work order?” retrieves those passages and answers from them, with the source named. If a conflict record already points at those passages, the answer includes it.

Do not use RAG to mark the epic aligned, to merge the three persona pages, or to rewrite the wiki on ingest. The index holds source passages and claim text. The records hold the conflict and the sign-off.

---

## 31

**You:** So basically there are 3 approaches I can think of right now as follows:

1. Only LLM wiki implementation
2. LLM wiki + RAG
3. Using agentic patterns

Is this the right order for the maturity of the product?

**Assistant:**

No. RAG is not the step after the wiki, and the agentic patterns are not a later product.

**LLM wiki alone** is a valid first demo for one epic. **Adding RAG next** makes search better and the check worse, because retrieved passages get blended into one answer. **Agentic patterns** are how the wiki stays honest once more than one epic exists. They are not a third architecture you swap in at the end.

The order that matches the product is:

1. **Records and a deterministic lint** on one epic. Claims, conflicts, and a sign-off on a version. The LLM wiki can be the way those records are read.
2. **The agentic loop** once a second epic or a later sprint appears. Plan over the delta, append claims, three persona projections, a critic, and an evaluator the writer cannot override.
3. **RAG last**, when that corpus no longer fits in one prompt. It fetches candidate passages for the critic and citations for a question. It still does not decide alignment.

---

## 32

**You:** So you are saying using agentic design patterns is the best way out for this idea to scale right?

**Assistant:**

No. Agentic patterns are what keep it honest as it grows. They are not what makes it scale.

What scales is linting the change against the signed records. An agent that re-reads the whole wiki on every sprint scales no better than the LLM wiki.

Use agents for a narrow job: plan over the delta, append claims, let the three personas write only their own pages, and run an evaluator they cannot override. That is the scalable use. A general multi-agent discussion of the corpus is not.

---

## 33

**You:** So how would you suggest it to make it scalable?

**Assistant:**

Scale the check, not the reading.

Store sources, claims, conflicts, and sign-offs as records. A sign-off points at a version of those records. The wiki pages are rendered from the records. Nothing in the product rewrites the whole corpus.

On each change, do only this:

1. Ingest the one source that changed.
2. Append the claims from that source. Leave every other persona’s claims untouched.
3. Pull a short list of signed claims that could conflict with the new ones. Use the records for this while the product is small. Add retrieval only when that list no longer fits in one prompt.
4. Run the evaluator on the new claims plus that short list. It can open a conflict. It cannot declare the product aligned by rewriting prose.
5. If it opens a conflict, this version is blocked. The previous sign-off remains on the previous version only.

A sprint then reads the open conflict list. The corpus can grow to every epic in the product. Each lint still looks at one change and a handful of signed claims.

---

## 34

**You:** Is using the Agentic Design patterns the best way forward in terms of accuracy and scale?

**Assistant:**

No. Agentic patterns alone are not the best way forward for either accuracy or scale.

Accuracy comes from the evaluator on the records. A group of agents will still smooth a conflict or miss one. Scale comes from checking only the change against the signed claims. Agents that re-read the product do not scale.

Use agents to extract claims from the changed source and to draft the three persona pages. Let the deterministic check decide whether this version is blocked. That split is what holds up on both.

---

## 35

**You:** Then which approach or methods can ensure both?

**Assistant:**

Use a claim store, a deterministic check, and a delta ingest. Together those two properties hold. Neither agents nor an LLM wiki does both.

**Claim store.** Every promise, scope line, and constraint is a record with a source and an owner persona. The three pages are views of those records. This is what your schema already models.

**Deterministic check.** Alignment is a pass or fail on those records: opposite claims, a promise wider than scope, a constraint missing from the other two views. The model does not grade its own answer. That is the accuracy.

**Delta ingest.** Only the changed source is extracted. The check compares those new claims to the signed set. Each sprint stays the same size as the product grows. That is the scale.

The model’s only jobs are to extract claims into that schema and to draft the persona pages. If its output fails the schema or the check, it is rejected. Retrieval, when you need it, only supplies the short list of signed claims to compare. It does not vote.

---

## 36

**You:** Ok so I need to tell a story here I cannot tell the most efficient method directly or immedately. So this is the correct order with increasing maturity of the product right?

1. LLM Wiki
2. Making use of Agentic AI patterns
3. Building claim store

Is this the correct order? Also is the last one the best approach to ever exists?

**Assistant:**

As the story, that order is right. As a ladder where each step is a better product, it is only right if step 2 is the attempt that fails.

**LLM wiki** is where you start. One epic, three documents, a readable wiki. Then show the break: ingest smooths the conflict, and a later sprint cannot re-read the whole product.

**Agentic patterns** are the next thing a team tries. Three personas and a critic stop the single voice. They still do not give you accuracy or scale, because the agents can talk themselves into “aligned,” and they still reread the corpus.

**Claim store** is the step that addresses both, but only together with the deterministic check on the delta. The store alone is a database. The maturity is: claims are records, the check decides, and only the changed source is examined.

It is not the best approach that will ever exist. It is the part you should not replace. Retrieval, better extraction, and the sign-off rule can sit around it later. A later design still has to store claims as records and refuse to let the model grade itself.

---

## 37

**You:** So this is going in the right direction right?

**Assistant:**

Yes. Tell it in that order, and make the point of the story that the agents are not the arrival.

The wiki is the start. The agents are what you try next, and they do not secure accuracy or scale. The claim store, the deterministic check, and the delta are where the product actually holds.

---

## 38

**You:** What is that people actually expect in a 25 min devcon style talk?

**Assistant:**

They expect one lesson they can repeat on Monday, shown on a real epic, with the last five minutes left for questions. They do not expect a survey of wiki, agents, and claim stores.

The lesson is this: a readable wiki does not scale, and more agents do not fix it. What scales is checking the change against signed claims.

Use the twenty minutes as a story with one example, *Ask the graph*:

- **Minutes 0–5.** The three documents disagree. An LLM wiki makes them readable, then smooths the disagreement or cannot reread the product next sprint.
- **Minutes 5–12.** Agents give Business, Product, and Tech each a voice. They still declare “aligned,” and they still reread everything. Scalability fails here. Say so.
- **Minutes 12–18.** The same epic as claims. The check fails a brief that sounds aligned. A later change lints only the delta.
- **Minutes 18–20.** The Monday practice: do not treat a green page as agreement. Then stop.

A successful talk ends with someone asking how a sign-off survives a ticket edit. That question means they followed the story. A comment of “nice overview of agent patterns” means the talk stayed a tour.

---

## 39

**You:** I am asking in a more general not just my topic

**Assistant:**

A 25-minute DevCon talk is a peer lesson. The room expects to learn one thing from work you actually did, and to have time to ask about it.

What they expect:

- **One idea.** They can retell it after they leave. A tour of a topic feels like an overview, and overviews are forgettable.
- **Something real.** A system, a failure, a change you shipped or tried. Slides that only define terms waste the slot.
- **A point of view.** You tried something, it broke or it held, and you say which. A neutral summary of options is a blog post, not a talk.
- **Respect for the clock.** About 20 minutes of talk and 5 for questions. Running over is the fastest way to lose the room.
- **Something they can reuse** on their own work, even if they never touch your project.

What they do not expect is a product launch, a glossary, or every branch of the subject. Success is a specific question. Polite silence means they could not find the one idea.

---

## 40

**You:** Ok so I need to show a quick start demo on 7th of Oct to my skip-level manager on this. I need a slide deck and a working demo for this. As of now for this demo I want to stick to the LLM wiki approach. I will however discuss about the downsides of this approach quite extensively

**Assistant:**

The demo and the deck are ready for 7 October. The wiki is compiled, not a live model call, so the same failure shows up every time you run it.

Start the demo:

```bash
poetry run python -m adaptpro.wiki.server
```

Open http://127.0.0.1:8765. Open `demo/slides.html` for the deck. Arrow keys move slides. `S` shows speaker notes. The notes on the Demo slide are the click path.

In the demo, ingest the eight *Ask the graph* documents, then:

1. Read the overview. It says **Ready**, and it turns “create a work order” into “a path to close the loop.”
2. Ask “Are we ready to kick this off?” with **Overview only**. The answer is yes, and it only read the overview.
3. Ask “Can the user create a work order from the answer?” the same way, then switch to **Every page** and ask again. Business, Product, and Tech disagree.
4. Ask about demo tenants with missing file links. Overview only does not see the intern note. Every page does.
5. Run **Lint**. It lists wording issues and leaves the status on Ready.
6. Ingest again. The log shows the wiki being rewritten. The badge stays Ready.

The deck spends the rest of the meeting on those failures: the false green, the default answer hiding the other pages, lint that does not block, the dropped intern finding, and why rereading that wiki does not scale. It does not present the claim-store design unless someone asks.

---

## 41

**Assistant follow-up** (after the demo server and tests finished; you had not asked a new question):

The wiki demo tests passed. The local demo server is not running now, so start it again when you want to rehearse:

```bash
poetry run python -m adaptpro.wiki.server
```

Then open http://127.0.0.1:8765 and `demo/slides.html`.

---

## 42

**You:** Give me the path to the LLM wiki setup and the slides on this computer

**Assistant:**

The slide deck is at `/Users/pranav.kalwad@cognite.com/Desktop/AdaptPro/demo/slides.html`.

The LLM wiki demo lives in `/Users/pranav.kalwad@cognite.com/Desktop/AdaptPro/src/adaptpro/wiki/`. The page you click through is `/Users/pranav.kalwad@cognite.com/Desktop/AdaptPro/src/adaptpro/wiki/static/index.html`. Start it from the repo with `poetry run python -m adaptpro.wiki.server`, then open http://127.0.0.1:8765. After you ingest, the compiled wiki files are written to `/Users/pranav.kalwad@cognite.com/Desktop/AdaptPro/demo/run/wiki`.

---

## 43

**You:** Help me export this chat to claude code CLI

**Assistant:**

Claude Code cannot resume a Cursor chat. Its `--resume` flag only opens sessions Claude Code itself saved, and `claude import` only brings in Codex or Gemini settings.

The settled thread is in `demo/cursor-chat-handoff.md`. On this machine that is `/workspace/demo/cursor-chat-handoff.md`. It is also on the branch, in pull request https://github.com/Pranav-Cognite/AdaptPro/pull/1.

From the AdaptPro repo on your computer, after you pull this branch:

```bash
claude "Read demo/cursor-chat-handoff.md and continue from those decisions."
```

That starts a normal Claude Code session with the decisions already loaded. After that, `claude --continue` in the same directory resumes that session.

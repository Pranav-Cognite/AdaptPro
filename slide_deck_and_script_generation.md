Dumps:

The implementation of this solution aims towards building a self maintainable knowledge base which keeps updating frequently and becomes a source of truth for data engineers, product and/or project managers, plant operators, maintenance engineers etc. 

The core idea behind implementing lies in the development of the underlying knowledge base. Knowledge base follows the fundamental rule of ingest->query->lint.

Ingest process basically triggers all the latest data to be pulled from their respective sources

Query is the process where each and every persona uses the underlying knowledge base to query and get answers

Linting is the process where the self-healing capabilities of the knowledge base is going to be leveraged. As the knowledge base keeps growing it becomes more and more difficult to maintain it. It becomes important for the knowledge base to not have any kind of self-contradictory statements. The linting process should be ideally run each and every time the sources are being ingested. To start off with I would want to have a Human-in-the-loop to understand the conflict being raised here and the proposed resolution to fix the problem.

The way this assistant or solution is supposed to work is by asking a lot of questions. And by questions I mean really sharp and specific clarifying questions. Some of these questions are interview-style questions to try and make sure to understand the question before making any assumptions.

Ultimately the effectiveness of this solution lies in bringing up the right questions, gaps, and contradictions per persona including what people don’t know what/how to address. The ownership of this knowledge base is a collective responsibility of the stakeholders across all personas

I also want to add an example of the below use case at Notion where the article says every employee at Notion has a Data Scientist:

https://www.linkedin.com/posts/billie-moffat-716668198_notions-favourite-custom-agent-got-the-full-share-7515244757128785920-fGTo/?utm_source=share&utm_medium=member_android&rcm=ACoAADej3Y0Bjf62_e-G1nXdeI4lVMJROWMRmxs


I need to explicitly state that the demo that I have built is around a particular use case (home work for each persona for cross functional team meetings). The talk itself needs to start with a more broader view of the overall product that is being built. The LLM wiki implementation needs to be spoken in quite a bit of detail. Knowledge base is the foundation for the agentic personas to run. 

If the knowledge base itself is not good the agentic personas will be rendered useless. So I will need to basically focus a bit on the internal working of how the knowledge base is built and how the agents are going to use it. The core is the knowledge base itself.


This use cases for this product are as follows: 

Exploration of work beyond one's role in an engagement, 
Do a thorough homework before jumping into meetings with cross-functional stakeholders, understanding the bigger picture and/or
Check alignment and readiness of each of the personas behind each and every decision that is being made
Understanding how one’s contribution fits into the grand scheme of things / understanding the impact of one’s work on the business
Intelligent chat assistant Integration with Slack:
An agent on Slack that automatically enters the chat when there are extensive discussions going on between different personas and acts as a bridge between the personas of real life
Intelligent chat assistant Integration with Jira:
Automatically flag down dependencies between personas and other areas of concern for a JIRA ticket that is created and intelligently align priorities within personas.
Intelligent chat assistant Integration with Teams:
An agent on Slack that automatically enters the chat when there are extensive discussions going on between different personas and acts as a bridge between the personas of real life
Connecting the dots between personas and having the intelligence to think 10 steps ahead and foresee problems and suggest solutions to avoid them => Historical failure patterns vs current plan, dependency foresight.
Making use of historical knowledge and combine it with current events
Use case for Value Delivery teams post deployment of CDF to debug and analyze incidents.

Use cases across teams (examples from Notion; spoken only, not a slide; tie to the demo personas in the script):
Sales | Account usage, AI adoption, seats, ARR, pipeline, and ownership | How is this account using Notion and AI across its workspaces?
Engineering | Product and AI behavior, identity lookups, and data validation | Which agents or workspaces stayed active, and where did behaviour change?
Customer Experience | Ticket volume, first-response time, CSAT, and customer context | What's driving this support queue's volume and response time?
Product | Feature adoption, onboarding, activation, and conversion | Where do people drop out of onboarding, and how does that vary by cohort?
Marketing | Account targeting, customer adoption, campaigns, and pipeline | Which target accounts already use Notion AI, and where should we focus outreach?


The use case which I need to present in DevCon is homework for each and every persona before jumping into meetings with Cross-functional meetings and discovery sessions with Customers.

Sources for the knowledge base:

Google docs (pre-sales documents, SoWs, business glossaries, Business KPIs, OKRs etc)
Email threads (Communications with internal and external stakeholders)
Slack threads (From relevant open channels and engagement specific locked channels)
JIRA tickets (Closed,open,pending and anything else that is relevant)
MS Teams chat
Confluence documentation
zoom/google meet AI generated summaries
Customer KT sessions and recordings
CDF project / codebase
Notion (pages and databases: specs, wikis, notes)

Product use cases beyond Cognite:

Onboarding assistant for new stakeholders (Getting up to speed on the current business requirement)
Meeting (Before,During and After) assistant
Intelligent assistant for audit trail of decisions (Why, what, where, how, when)
Conflict mediator (Conflict of decisions between personas)
Org knowledge base builder (To address the institutional memory problem where you want to understand why, when, what and how was a decision was arrived at for doing a particular thing)


Opportunities within Cognite:

Integration with CDF
Technically the entire CDF project will be a part of the sources which are being ingested into the knowledge base. So the CDF project is by default integrated with AdaptPro.
Integration with Flows apps 
Two ways in which this can be thought of:
AdaptPro by itself is a Flows custom app
AdaptPro tab/panel inside a Flows app
AdaptPro as a service to which Flows app make API calls
Integration with Atlas AI
AdaptPro as a plugin/skill/subagent with Atlas AI which provides a richer context to carry out a more effective RCA.



Aligning with the theme of this year’s DevCon (Scalability):
Decision throughput and consistency needs to scale with the product, processes and cross-functional teams
Token/LLM cost explosion
Lint is an intellectual exercise so this could a bottleneck if not handled properly
Index/ Retrieval quality at scale
Observability at scale
Multimodal and unstructured input at scale


Limitations/Shortcomings/gaps:

How many customers would be ok to expose their data to AI systems to build a knowledge graph?
 If not used correctly there can be over reliance on LLMs in decision making decisions
Cyber risks about bringing in data from various sources
Surveillance threat
Ambiguity in conflict resolution ownership
Source-of-truth fights
Cost at scale


Implementation approaches to consider  (Build from POC to a production grade enterprise product):

Basic LLM wiki implementation with a rudimentary chat based interface for each of the personas.
NotebookLM
Integration of LLM Wiki with Obsidian
Using LLM agnostic agentic AI design patterns:
I very much prefer running these queries using claude since it gives this easy to use interface while asking clarifying questions which seems very user friendly.




Things to cover in the talk and the slide deck:
What is the problem being faced by cross-functional teams today?
Give example of Notion’s paper “Every employee at Notion has a Data Scientist"
The solution you are proposing
The internal working of your solution (Internal working of Knowledge base. A brief intro to knowledge bases can also help)
Product use cases
Talk briefly about the knowledge base and the ingest->query->lint process
Talk about data sources as well
Architecture diagrams
Demo with Claude Code => LLM Wiki (A slide discussing the implementation maturity)
Aligning with the theme of this year’s DevCon: Scalability
Opportunities within Cognite Ecosystem
Product use cases beyond Cognite
Limitations / shortcomings
Q&A
Thank you

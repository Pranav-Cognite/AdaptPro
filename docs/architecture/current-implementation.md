# Architecture — current implementation

**What is being addressed:** teams on a cross-functional engagement (Business, Product, Tech) each
hold part of the picture and meet without knowing what the others know or what to ask them. AdaptPro
builds one knowledge base from the engagement's documents, keeps each persona's claims separate, and
lets each persona query it to understand the others, prepare for meetings and, when a decision is
coming, check whether it is aligned.

The sample engagement is Veridion Line 3 OEE. Line 3 is the polymer line at Calder Valley (Reactor
R-301, then Extruder EX-302), not a software version. Business promised an automatic work order when
its OEE drops; Product and Tech scoped a read-only lookup. The diagram below is how this repo stores
and uses that engagement. It is not the plant system.

## What is built

- **Sources.** Three engagement documents (business use case, PRD, ADR) under
  `docs/engagements/veridion-line3-oee/`, plus a fictional Cognite Data Fusion (CDF) project under
  `mock-cdf-project/`.
- **Mock CDF project.** A Cognite Toolkit project with four modules: `veridion_platform` (data sets,
  access groups), `veridion_oee_model` (a custom data model on top of the Core Data Model),
  `veridion_line3_oee` (about 40 assets, equipment, 21 time series, 11 downtime activities, files) and
  `veridion_ingestion` (extractor and pipeline configs, RAW tables, a SQL transformation, an OEE
  calculation function and an hourly workflow). `fixtures/` generates 30 days of datapoints
  reproducibly, with deliberate data flaws. `cdf build` passes offline; nothing is deployed.
- **LLM wiki** (`wiki/`). Three exclusive persona pages (Business, Product, Tech), source pages for
  each document and for the CDF project, three glossaries, an **open-topics** page, and a generated
  graph layer. `SCHEMA.md` holds the conventions, including who owns which decision (Business owns the
  definition of OEE).
- **Four read-only agents** (`.claude/agents/`): three briefing agents (one per persona) and
  `check-decision-alignment`.
  - **Briefing agents** cover explore beyond your role, homework before a cross-functional meeting,
    and impact. A homework request without the meeting type and goal gets two selectable clarifying
    questions first. The brief is then written as preparation for a brainstorm, and ends with at
    most five questions to ask the other personas, each with a *Why ask* (file and gap) and *A good
    answer settles*. Slack, Teams, Jira, look-ahead and history-plus-now are named in the README but
    not built.
  - **`check-decision-alignment`** runs the three briefing agents on a proposed decision and waits
    for all three before giving one verdict (Aligned, Not aligned, Undetermined). It is the only
    place that uses the "RED" status on the open-topics page.
  - **Every agent queries the wiki for every request**: index first, then a search of the whole wiki, following links and source pages, citing a page per claim, and saying "not in the wiki" when it is absent. They never read the raw `docs/` or `mock-cdf-project/` files.
  - Every agent asks a clarifying question only when a missing fact would change the answer, with
    selectable options and a place to type another answer; homework requests are the exception and
    always ask first when the meeting is unstated.

```mermaid
flowchart TD
    subgraph Sources["Source documents (docs/engagements/veridion-line3-oee/)"]
        BU["Business use case"]
        PRD["Product plan"]
        ADR["Engineering decision"]
    end

    subgraph CDFProj["mock-cdf-project/ (fictional, Toolkit-shaped, not deployed)"]
        Plat["veridion_platform\n(data sets, groups)"]
        Model["veridion_oee_model\n(custom data model)"]
        L3["veridion_line3_oee\n(assets, series, activities, files)"]
        Ingest["veridion_ingestion\n(extractors, RAW, SQL, function, workflow)"]
        Fix["fixtures/\n(30 days of datapoints)"]
    end

    subgraph WikiBox["LLM wiki (wiki/)"]
        Schema["SCHEMA.md\n(conventions, decision ownership)"]
        BizP["Business persona page"]
        ProdP["Product persona page"]
        TechP["Tech persona page"]
        SrcP["Source pages\n(3 documents + CDF project)"]
        Gloss["3 glossaries"]
        Topics["Open topics\n(veridion-line3-oee-open-topics.md)"]
        Graph["Generated graph layer"]
    end

    subgraph AgentsBox[".claude/agents/ (strictly read-only)"]
        A1["brief-business-on-product-and-tech"]
        A2["brief-product-on-business-and-tech"]
        A3["brief-tech-on-business-and-product"]
        A4["check-decision-alignment"]
    end

    Humans(["Business / Product / Tech people\n+ known designations"])

    BU --> BizP
    PRD --> ProdP
    ADR --> TechP
    Plat & Model & L3 & Ingest --> SrcP
    Fix --> L3
    SrcP --> TechP

    BizP --> Topics
    ProdP --> Topics
    TechP --> Topics
    WikiBox -.generates.-> Graph

    Schema --> A1 & A2 & A3 & A4
    Gloss --> A1 & A2 & A3 & A4
    Topics --> A1 & A2 & A3 & A4
    BizP --> A1
    ProdP --> A2
    TechP --> A3
    A4 -->|"runs and waits for"| A1 & A2 & A3

    Humans -->|"homework: clarifying questions first;\nother use cases: ask only if a fact would change the answer"| A1 & A2 & A3
    Humans -->|"proposed decision"| A4

    classDef source fill:#CADCFC,stroke:#1E2761,color:#1E2761,stroke-width:2px
    classDef wiki fill:#1E2761,stroke:#1E2761,color:#ffffff,stroke-width:2px
    classDef agent fill:#1F8A70,stroke:#1F8A70,color:#ffffff,stroke-width:2px
    classDef human fill:#B8862B,stroke:#B8862B,color:#ffffff,stroke-width:2px

    class BU,PRD,ADR,Plat,Model,L3,Ingest,Fix source
    class Schema,BizP,ProdP,TechP,SrcP,Gloss,Topics,Graph wiki
    class A1,A2,A3,A4 agent
    class Humans human
```

**Reading it:** blue = source documents and the mock CDF project, navy = the wiki, green = the four
agents, gold = the humans asking questions. The agents search the wiki (index, persona, source, glossary and
open-topics pages) before answering; that is what keeps the question rule
and the first-person voice convention consistent. The agents do not read live CDF: the mock project
reaches them only through the wiki's source pages.

## Not built or not verified

- No deployment of the mock CDF project; extractor configs are not validated against the extractors'
  own schemas, and the SQL transformation has not been executed.
- Datapoint CSVs are not loaded by `cdf build`.
- Slack, Teams, Jira, look-ahead and history-plus-now are not implemented.
- The clarifying-question gate and brainstorm tone were verified on the Tech briefing agent only;
  `check-decision-alignment` has not been re-tested since the OEE ownership rule and the rename.
- The graph layer is generated from the wiki and is not read by the agents.

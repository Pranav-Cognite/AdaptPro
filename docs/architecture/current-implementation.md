# Architecture — current implementation

**What is being addressed:** Business promised Veridion an automatic work order when Production
Line 3's OEE drops. Product and Tech scoped a read-only lookup of that line. Line 3 is the
polymer line at Calder Valley (Reactor R-301, then Extruder EX-302), not a software version.
The diagram below is how this repo stores that disagreement today. It is not the plant system.

What's actually built in this repo today: engagement source documents are ingested into an
LLM knowledge base as three exclusive persona pages plus one conflict record; four read-only
agents query that knowledge base so Business, Product, and Tech can brief each other and check
decision alignment. Ask-before-answering is a hard gate on every agent — never bypassed.

```mermaid
flowchart TD
    subgraph Sources["Source documents (docs/engagements/veridion-line3-oee/)"]
        BU["Business use case"]
        PRD["Product plan"]
        ADR["Engineering decision"]
    end

    subgraph CDFProj["mock-cdf-project/ (fictional, static)"]
        Fixtures["CDM fixtures:\nAssets, TimeSeries, Activities, Files"]
    end

    subgraph WikiBox["LLM wiki (wiki/)"]
        Schema["SCHEMA.md\n(conventions)"]
        BizP["Business persona page"]
        ProdP["Product persona page"]
        TechP["Tech persona page"]
        Gloss["3 glossaries"]
        Conflicts["Conflict record\n(veridion-line3-oee-conflicts.md)"]
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
    Fixtures -.grounds externalIds.-> BU
    Fixtures -.grounds externalIds.-> ADR

    BizP --> Conflicts
    ProdP --> Conflicts
    TechP --> Conflicts

    Schema --> A1 & A2 & A3 & A4
    Gloss --> A1 & A2 & A3 & A4
    Conflicts --> A1 & A2 & A3 & A4
    BizP --> A1
    ProdP --> A2
    TechP --> A3

    Humans -->|"ask-before-answering gate"| A1 & A2 & A3 & A4

    classDef source fill:#CADCFC,stroke:#1E2761,color:#1E2761,stroke-width:2px
    classDef wiki fill:#1E2761,stroke:#1E2761,color:#ffffff,stroke-width:2px
    classDef agent fill:#1F8A70,stroke:#1F8A70,color:#ffffff,stroke-width:2px
    classDef human fill:#B8862B,stroke:#B8862B,color:#ffffff,stroke-width:2px

    class BU,PRD,ADR,Fixtures source
    class Schema,BizP,ProdP,TechP,Gloss,Conflicts wiki
    class A1,A2,A3,A4 agent
    class Humans human
```

**Reading it:** blue = source documents, navy = the wiki, green = the four agents, gold = the
humans asking questions. Every agent reads `SCHEMA.md`, the glossaries, and the conflict
record before answering anything — that's what makes the ask-before-answering gate and the
first-person voice convention consistent across all four.

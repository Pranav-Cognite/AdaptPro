# Architecture — current implementation

What's actually built in this repo today: three source documents become three persona pages
and one conflict record in the wiki; four read-only agents read that wiki to answer people.

```mermaid
flowchart TD
    subgraph Sources["Source documents (docs/epics/01-knowledge-base/)"]
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
        Conflicts["Conflict record\n(knowledge-base-conflicts.md)"]
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

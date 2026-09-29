from adaptpro.corpus.loader import load_corpus
from adaptpro.corpus.models import AskTheGraphCorpus, LoadedSource
from adaptpro.wiki.models import CompiledWiki, WikiPage


def compile_wiki(
    corpus: AskTheGraphCorpus | None = None,
    *,
    ingest_count: int = 1,
) -> CompiledWiki:
    """Compile sources into an LLM-wiki: persona pages plus one smoothed overview.

    The overview is the failure this demo exists to show. It reads as agreement.
    """
    loaded = corpus if corpus is not None else load_corpus()
    by_id = loaded.by_id()
    pages: dict[str, WikiPage] = {}

    pages["overview"] = _overview()
    pages["business"] = _business(by_id)
    pages["product"] = _product(by_id)
    pages["tech"] = _tech(by_id)
    for source in loaded.sources:
        pages[f"sources/{source.id}"] = _source_page(source)

    ordered = _ordered_slugs(pages)
    pages["index"] = _index(pages, ordered)
    log_line = (
        f"ingest #{ingest_count} | {len(loaded.sources)} sources | "
        f"wrote {len(pages) + 1} pages | query reads overview first"
    )
    pages["log"] = _log(log_line, ingest_count)
    return CompiledWiki(
        epic_title=loaded.manifest.title,
        kickoff_status="Ready",
        ingest_count=ingest_count,
        pages=pages,
        log=[log_line],
    )


def _quote(source: LoadedSource, snippet: str) -> str:
    if snippet not in source.text:
        raise ValueError(f"{source.id} does not contain {snippet!r}")
    return snippet


def _overview() -> WikiPage:
    body = """# Ask the graph

Kickoff status: Ready

Ask the graph lets a customer ask about their operations in Fusion and get an answer with citations. The first version is an MVP we can show in a sales cycle: a small set of questions, a fast UI, and a path to close the loop after the answer.

Business, Product, and Tech are describing the same epic. Open points are wording, not scope.

- Customers ask about operations without leaving Fusion.
- Answers are grounded and cited.
- v1 stays focused enough to demo next month.
- Follow-up work tracks how the answer connects to the customer's process.

This is the page a query reads first.
"""
    return WikiPage(
        slug="overview",
        title="Overview",
        summary="Kickoff status: Ready. Wording, not scope.",
        body=body,
    )


def _business(by_id: dict[str, LoadedSource]) -> WikiPage:
    ask = _quote(by_id["gtm-one-pager"], "Ask anything about your operations")
    realtime = _quote(
        by_id["gtm-one-pager"],
        "in real-time, while you are still on the call",
    )
    work_order = _quote(by_id["gtm-one-pager"], "create a work order from the answer")
    truth = _quote(by_id["gtm-one-pager"], "Cognite is the source of truth")
    mvp = _quote(
        by_id["gtm-one-pager"],
        "something we can show in a sales cycle next month",
    )
    headline = _quote(by_id["cxo-slide"], "AI that understands the plant.")
    board = _quote(by_id["cxo-slide"], "ask anything about your operations.")
    happy = _quote(by_id["cxo-slide"], "Happy path only")
    body = f"""# Business

What GTM and the board slide commit to.

- {headline}
- Customers should be able to {board}
- {ask} — {realtime}.
- {truth}; the user should not leave Fusion.
- After the answer, {work_order} so the loop closes in the customer's CMMS.
- MVP: {mvp}, not a science project.
- {happy}: a reliability engineer asks a question and gets an answer in the room.
- We will not slow the sales cycle for engineering polish.
"""
    return WikiPage(
        slug="business",
        title="Business",
        summary="Ask anything, on the call, then create a work order.",
        body=body,
    )


def _product(by_id: dict[str, LoadedSource]) -> WikiPage:
    templates = _quote(by_id["prd-v1"], "Three starter question templates")
    readonly = _quote(by_id["prd-v1"], "Read-only")
    writes = _quote(by_id["prd-v1"], "Write actions (no CMMS, no work orders)")
    realtime = _quote(by_id["prd-v1"], "Real-time means the UI feels instant")
    mvp = _quote(by_id["prd-v1"], "MVP means these three templates, not an open-ended assistant")
    ticket = _quote(by_id["tickets"], "Add a text box on Search.")
    body = f"""# Product

What v1 actually contains.

## In scope

- English only
- {templates}
- {readonly}
- Citations required on every answer
- {realtime} (p95 target: snappy), not a new ingest pipeline
- {mvp}
- The user never has to leave Fusion

## Out of scope

- {writes}
- Languages other than English

## Tickets

- {ticket} No link to the CXO sentence, grounding rules, or citations.
- Wire the three starter templates.
"""
    return WikiPage(
        slug="product",
        title="Product",
        summary="Three templates, read-only, no work orders.",
        body=body,
    )


def _tech(by_id: dict[str, LoadedSource]) -> WikiPage:
    ids = _quote(
        by_id["adr-014-grounding"],
        'Inventing an `externalId` is worse than saying "I don\'t know."',
    )
    cluster = _quote(
        by_id["adr-014-grounding"],
        "Answers must not leave the customer's CDF cluster / region",
    )
    citations = _quote(
        by_id["adr-014-grounding"],
        "Citation coverage is a launch blocker, not polish.",
    )
    writes = _quote(by_id["adr-015-tools"], "No write tools registered.")
    latency = _quote(by_id["adr-015-tools"], "p95 latency < 8s is a launch blocker.")
    realtime = _quote(
        by_id["adr-015-tools"],
        '"Real-time" as streaming ingest is out of scope',
    )
    truth = _quote(
        by_id["adr-015-tools"],
        "Source of truth is a specific view in a specific space — not RAW",
    )
    files = _quote(
        by_id["intern-file-coverage"],
        "~40% of demo tenants have no file links to assets.",
    )
    slack = _quote(by_id["slack-architect"], "Cluster-local stays non-negotiable.")
    body = f"""# Tech

What architecture has already accepted.

- {ids}
- {cluster} (cluster-local; no cross-region model calls).
- {citations}
- Tool-calling over the Instances API + file RAG.
- {writes}
- {latency}
- {realtime}; we query data already in CDF.
- {truth}, not last week's export.
- {slack} Don't register write tools even if GTM asks.
- Field note, not on the board slide: {files}
"""
    return WikiPage(
        slug="tech",
        title="Tech",
        summary="No write tools, cluster-local, p95 under 8s.",
        body=body,
    )


def _source_page(source: LoadedSource) -> WikiPage:
    body = f"""# {source.title}

Owner: {source.persona_owner.value}

{source.text.strip()}
"""
    first_line = next(
        (line.strip() for line in source.text.splitlines() if line.strip() and not line.startswith("#")),
        source.title,
    )
    return WikiPage(
        slug=f"sources/{source.id}",
        title=source.title,
        summary=first_line,
        body=body,
    )


def _ordered_slugs(pages: dict[str, WikiPage]) -> list[str]:
    head = ["overview", "business", "product", "tech"]
    sources = sorted(slug for slug in pages if slug.startswith("sources/"))
    return head + sources


def _index(pages: dict[str, WikiPage], ordered: list[str]) -> WikiPage:
    lines = [
        "# Index",
        "",
        "Query reads Overview first.",
        "",
    ]
    for slug in ordered:
        page = pages[slug]
        lines.append(f"- [{page.title}]({slug}) — {page.summary}")
    body = "\n".join(lines) + "\n"
    return WikiPage(
        slug="index",
        title="Index",
        summary="Catalog. Query reads the overview first.",
        body=body,
    )


def _log(line: str, ingest_count: int) -> WikiPage:
    entries = [
        f"## ingest #{number} | sources compiled | pages rewritten | query reads overview first"
        for number in range(1, ingest_count)
    ]
    entries.append(f"## {line}")
    body = "# Log\n\n" + "\n\n".join(entries) + "\n"
    return WikiPage(
        slug="log",
        title="Log",
        summary=f"{ingest_count} ingest(s). Each one rewrites the wiki.",
        body=body,
    )

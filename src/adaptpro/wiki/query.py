from adaptpro.wiki.models import CompiledWiki, Excerpt, QueryAnswer


def answer_question(wiki: CompiledWiki, question: str, scope: str = "overview") -> QueryAnswer:
    """Answer from the compiled wiki.

    ``overview`` is the LLM-wiki default: index, then the overview. ``all`` opens
    every persona page. The two scopes disagree on purpose.
    """
    if scope not in {"overview", "all"}:
        raise ValueError(f"Unknown scope: {scope}")
    kind = _classify(question)
    if scope == "overview":
        return _from_overview(wiki, question, kind)
    return _from_all(wiki, question, kind)


def _classify(question: str) -> str:
    text = question.lower()
    if any(token in text for token in ("40%", "file link", "demo tenant")):
        return "files"
    if any(token in text for token in ("work order", "cmms", "write tool", "write")):
        return "write"
    if "real-time" in text or "realtime" in text or "real time" in text:
        return "realtime"
    if any(token in text for token in ("source of truth", "raw")):
        return "truth"
    if any(token in text for token in ("ask anything", "template", "open-ended")):
        return "scope"
    if any(token in text for token in ("kick", "align", "ready", "agree", "same epic")):
        return "kickoff"
    return "search"


def _from_overview(wiki: CompiledWiki, question: str, kind: str) -> QueryAnswer:
    overview = wiki.page("overview")
    pages = ["index", "overview"]
    answers = {
        "kickoff": (
            "Yes. Kickoff status is Ready. Business, Product, and Tech are describing "
            "the same epic. Open points are wording, not scope."
        ),
        "write": (
            "Yes, as a follow-up. v1 includes a path to close the loop after the answer, "
            "so the result can connect to the customer's process."
        ),
        "realtime": (
            "Real-time here means a fast UI, quick enough to show in a sales conversation."
        ),
        "scope": (
            "The customer can ask about their operations. v1 is a small set of questions, "
            "focused enough to demo next month."
        ),
        "truth": "Cognite, inside Fusion. The user does not leave the product.",
        "files": (
            "The overview does not mention file coverage. Nothing on this page changes "
            "the happy path."
        ),
    }
    answer = answers.get(kind) or _search_answer(wiki, question, pages)
    excerpts = [Excerpt(slug="overview", title=overview.title, text=_paragraph(overview.body))]
    if kind == "search":
        excerpts = _search_excerpts(wiki, question, pages)
    return QueryAnswer(
        question=question,
        scope="overview",
        pages_read=pages,
        answer=answer,
        excerpts=excerpts,
    )


def _from_all(wiki: CompiledWiki, question: str, kind: str) -> QueryAnswer:
    pages = ["index", "overview", "business", "product", "tech"]
    answers = {
        "kickoff": (
            "No. The overview says Ready, and that the open points are wording. "
            "Business promises a work order and open-ended questions. "
            "Product scopes three read-only templates. "
            "Tech has registered no write tools."
        ),
        "write": (
            "Business says create a work order from the answer. "
            "Product says write actions are out of scope. "
            "Tech says no write tools are registered."
        ),
        "realtime": (
            "Business means while you are still on the call. "
            "Product means the UI feels instant. "
            "Tech says streaming ingest is out of scope, and p95 under 8 seconds is a launch blocker."
        ),
        "scope": (
            "Business says ask anything. "
            "Product says three starter templates, not an open-ended assistant. "
            "The intern ticket is a text box on Search, with no link to grounding or citations."
        ),
        "truth": (
            "Business says Cognite is the source of truth. "
            "Product says the user never leaves Fusion. "
            "Tech says a specific view in a specific space, not RAW."
        ),
        "files": (
            "Tech has a field note: about 40% of demo tenants have no file links to assets. "
            "The overview and the board slide do not mention it."
        ),
    }
    answer = answers.get(kind) or _search_answer(wiki, question, pages)
    excerpts = _search_excerpts(wiki, question, pages) if kind == "search" else _kind_excerpts(wiki, kind)
    return QueryAnswer(
        question=question,
        scope="all",
        pages_read=pages,
        answer=answer,
        excerpts=excerpts,
    )


def _kind_excerpts(wiki: CompiledWiki, kind: str) -> list[Excerpt]:
    wanted = {
        "kickoff": ("overview", "business", "product", "tech"),
        "write": ("business", "product", "tech"),
        "realtime": ("business", "product", "tech"),
        "scope": ("business", "product"),
        "truth": ("business", "product", "tech"),
        "files": ("tech", "overview"),
    }[kind]
    return [
        Excerpt(slug=slug, title=wiki.page(slug).title, text=_relevant_line(wiki.page(slug).body, kind))
        for slug in wanted
    ]


def _relevant_line(body: str, kind: str) -> str:
    needles = {
        "kickoff": ("Kickoff status", "create a work order", "Read-only", "No write tools"),
        "write": ("create a work order", "no work orders", "No write tools"),
        "realtime": ("on the call", "feels instant", "streaming ingest", "p95 latency"),
        "scope": ("Ask anything", "three templates", "text box"),
        "truth": ("source of truth", "leave Fusion", "not RAW"),
        "files": ("40%", "Kickoff status", "happy path"),
    }[kind]
    for line in body.splitlines():
        if any(needle.lower() in line.lower() for needle in needles):
            return line.lstrip("- ").strip()
    paragraph = _paragraph(body)
    return paragraph


def _paragraph(body: str) -> str:
    chunks = [chunk.strip() for chunk in body.split("\n\n") if chunk.strip() and not chunk.startswith("#")]
    return chunks[0] if chunks else body.strip()


def _search_answer(wiki: CompiledWiki, question: str, slugs: list[str]) -> str:
    excerpts = _search_excerpts(wiki, question, slugs)
    if not excerpts:
        return "No compiled page in this scope contains those words."
    titles = ", ".join(excerpt.title for excerpt in excerpts)
    return f"The closest compiled text is on {titles}."


def _search_excerpts(wiki: CompiledWiki, question: str, slugs: list[str]) -> list[Excerpt]:
    terms = [term for term in question.lower().split() if len(term) > 3]
    scored: list[tuple[int, Excerpt]] = []
    for slug in slugs:
        page = wiki.page(slug)
        haystack = page.body.lower()
        score = sum(haystack.count(term) for term in terms)
        if score == 0:
            continue
        line = next(
            (item.strip() for item in page.body.splitlines() if any(term in item.lower() for term in terms)),
            page.summary,
        )
        scored.append((score, Excerpt(slug=slug, title=page.title, text=line.lstrip("- ").strip())))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [excerpt for _, excerpt in scored[:3]]

from adaptpro.wiki.compile import compile_wiki
from adaptpro.wiki.lint import lint_wiki, with_lint_page
from adaptpro.wiki.query import answer_question


def test_overview_declares_ready_and_smooths_the_work_order() -> None:
    wiki = compile_wiki()
    overview = wiki.markdown("overview")
    assert wiki.kickoff_status == "Ready"
    assert "Kickoff status: Ready" in overview
    assert "wording, not scope" in overview
    assert "path to close the loop" in overview
    assert "No write tools registered" not in overview
    assert "40%" not in overview
    assert "create a work order from the answer" in wiki.markdown("business")
    assert "no work orders" in wiki.markdown("product")
    assert "No write tools registered." in wiki.markdown("tech")


def test_default_query_reads_the_overview_and_misses_the_conflict() -> None:
    wiki = compile_wiki()
    ready = answer_question(wiki, "Are we ready to kick this off?")
    write = answer_question(wiki, "Can the user create a work order from the answer?")
    files = answer_question(wiki, "Did anyone flag demo tenants with missing file links?")

    assert ready.pages_read == ["index", "overview"]
    assert "Yes" in ready.answer
    assert "Ready" in ready.answer
    assert "work order" not in ready.answer.lower()

    assert write.scope == "overview"
    assert "path to close the loop" in write.answer
    assert "No write tools" not in write.answer

    assert "does not mention" in files.answer
    assert "40%" not in files.answer


def test_opening_every_page_shows_the_disagreement() -> None:
    wiki = compile_wiki()
    write = answer_question(wiki, "Can the user create a work order from the answer?", "all")
    files = answer_question(wiki, "Did anyone flag demo tenants with missing file links?", "all")

    assert "create a work order" in write.answer
    assert "out of scope" in write.answer
    assert "no write tools" in write.answer.lower()
    assert "40%" in files.answer
    assert "overview" in files.answer.lower()


def test_lint_lists_wording_and_does_not_block_or_see_the_file_gap() -> None:
    wiki = compile_wiki()
    report = lint_wiki(wiki)
    updated = with_lint_page(wiki, report)
    text = report.markdown()

    assert report.health == "usable"
    assert report.kickoff_status_changed is False
    assert updated.kickoff_status == "Ready"
    assert "Kickoff status remains Ready" in text
    assert "Work orders" in text
    assert "40%" not in text
    assert "file link" not in text.lower()


def test_reingest_rewrites_and_stays_ready() -> None:
    first = compile_wiki(ingest_count=1)
    second = compile_wiki(ingest_count=2)
    assert first.kickoff_status == second.kickoff_status == "Ready"
    assert second.ingest_count == 2
    assert "ingest #2" in second.markdown("log")
    assert len(second.pages) > 8

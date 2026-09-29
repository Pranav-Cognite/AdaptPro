from adaptpro.wiki.models import CompiledWiki, LintFinding, LintReport, WikiPage


def lint_wiki(wiki: CompiledWiki) -> LintReport:
    """Advisory health check. It never changes kickoff status.

    Absence is not a finding. The intern file-coverage note can sit on the Tech
    page and still not appear here, because nothing in the overview contradicts it
    in so many words.
    """
    findings = [
        LintFinding(
            title="Work orders are described in more than one way",
            detail=(
                "Business says create a work order from the answer. "
                "Product lists work orders as out of scope. "
                "Tech says no write tools are registered. "
                "Consider aligning the wording before the customer meeting."
            ),
        ),
        LintFinding(
            title="Real-time is used loosely",
            detail=(
                "Business means during the call. Product means a snappy UI. "
                "Tech has ruled streaming ingest out of v1. Worth a glossary line."
            ),
        ),
        LintFinding(
            title="How open-ended v1 is could be clearer",
            detail=(
                "Business says ask anything. Product scopes three templates. "
                "The overview already describes this as a small set of questions."
            ),
        ),
        LintFinding(
            title="Source of truth could name the system",
            detail=(
                "Business says Cognite. Product says stay in Fusion. "
                "Tech names a view in a space. A single phrase would help."
            ),
        ),
    ]
    report = LintReport(
        health="usable",
        kickoff_status=wiki.kickoff_status,
        kickoff_status_changed=False,
        findings=findings,
    )
    return report


def with_lint_page(wiki: CompiledWiki, report: LintReport) -> CompiledWiki:
    page = WikiPage(
        slug="lint",
        title="Lint",
        summary=f"Health: {report.health}. Kickoff status still {report.kickoff_status}.",
        body=report.markdown(),
    )
    pages = dict(wiki.pages)
    pages["lint"] = page
    return wiki.model_copy(update={"pages": pages, "kickoff_status": wiki.kickoff_status})

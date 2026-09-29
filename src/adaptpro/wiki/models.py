from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class WikiPage(StrictModel):
    slug: str
    title: str
    summary: str
    body: str


class CompiledWiki(StrictModel):
    epic_title: str
    kickoff_status: Literal["Ready"]
    ingest_count: int
    pages: dict[str, WikiPage]
    log: list[str] = Field(default_factory=list)

    def page(self, slug: str) -> WikiPage:
        return self.pages[slug]

    def markdown(self, slug: str) -> str:
        return self.pages[slug].body


class Excerpt(StrictModel):
    slug: str
    title: str
    text: str


class QueryAnswer(StrictModel):
    question: str
    scope: Literal["overview", "all"]
    pages_read: list[str]
    answer: str
    excerpts: list[Excerpt]


class LintFinding(StrictModel):
    title: str
    detail: str


class LintReport(StrictModel):
    health: Literal["usable"]
    kickoff_status: Literal["Ready"]
    kickoff_status_changed: bool
    findings: list[LintFinding]

    def markdown(self) -> str:
        lines = [
            "# Lint",
            "",
            f"Health: {self.health}",
            "",
            (
                f"{len(self.findings)} wording items to tidy when convenient. "
                f"Kickoff status remains {self.kickoff_status}. Lint did not change it."
            ),
            "",
        ]
        for index, finding in enumerate(self.findings, start=1):
            lines.append(f"## {index}. {finding.title}")
            lines.append("")
            lines.append(finding.detail)
            lines.append("")
        return "\n".join(lines).rstrip() + "\n"

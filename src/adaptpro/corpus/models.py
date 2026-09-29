from pydantic import BaseModel, ConfigDict, Field

from adaptpro.schema.enums import FailureMode, Persona, SourceKind


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ManifestSource(StrictModel):
    id: str
    title: str
    kind: SourceKind
    filename: str
    persona_owner: Persona


class CorpusManifest(StrictModel):
    epic_id: str
    title: str
    intent: str
    sources: list[ManifestSource]


class LoadedSource(StrictModel):
    id: str
    title: str
    kind: SourceKind
    filename: str
    persona_owner: Persona
    text: str


class AskTheGraphCorpus(StrictModel):
    manifest: CorpusManifest
    sources: list[LoadedSource]

    def by_id(self) -> dict[str, LoadedSource]:
        return {source.id: source for source in self.sources}


class EvidenceAnchor(StrictModel):
    source_id: str
    must_contain: str


class GoldFinding(StrictModel):
    id: str
    failure_mode: FailureMode
    title: str
    summary: str
    evidence: list[EvidenceAnchor] = Field(min_length=1)


class GoldSet(StrictModel):
    epic_id: str
    findings: list[GoldFinding]

    def ids(self) -> set[str]:
        return {finding.id for finding in self.findings}

    def modes(self) -> set[FailureMode]:
        return {finding.failure_mode for finding in self.findings}

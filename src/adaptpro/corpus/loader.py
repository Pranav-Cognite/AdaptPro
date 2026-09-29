import json

from adaptpro.corpus.models import AskTheGraphCorpus, CorpusManifest, GoldSet, LoadedSource
from adaptpro.paths import ask_the_graph_dir


def load_manifest() -> CorpusManifest:
    path = ask_the_graph_dir() / "manifest.json"
    return CorpusManifest.model_validate_json(path.read_text(encoding="utf-8"))


def load_corpus() -> AskTheGraphCorpus:
    manifest = load_manifest()
    sources: list[LoadedSource] = []
    root = ask_the_graph_dir() / "sources"
    for item in manifest.sources:
        text = (root / item.filename).read_text(encoding="utf-8")
        sources.append(
            LoadedSource(
                id=item.id,
                title=item.title,
                kind=item.kind,
                filename=item.filename,
                persona_owner=item.persona_owner,
                text=text,
            )
        )
    return AskTheGraphCorpus(manifest=manifest, sources=sources)


def load_goldset() -> GoldSet:
    path = ask_the_graph_dir() / "goldset.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    return GoldSet.model_validate(payload)

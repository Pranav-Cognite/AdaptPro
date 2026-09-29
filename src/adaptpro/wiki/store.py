from pathlib import Path

from adaptpro.wiki.models import CompiledWiki


def write_wiki(root: Path, wiki: CompiledWiki) -> None:
    root.mkdir(parents=True, exist_ok=True)
    for page in wiki.pages.values():
        path = root / f"{page.slug}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(page.body, encoding="utf-8")

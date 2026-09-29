"""LLM-wiki demo: ingest, query, and lint over one epic."""

from adaptpro.wiki.compile import compile_wiki
from adaptpro.wiki.lint import lint_wiki
from adaptpro.wiki.query import answer_question

__all__ = ["answer_question", "compile_wiki", "lint_wiki"]

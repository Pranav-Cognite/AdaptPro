import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from adaptpro.paths import repo_root
from adaptpro.wiki.compile import compile_wiki
from adaptpro.wiki.lint import lint_wiki, with_lint_page
from adaptpro.wiki.models import CompiledWiki
from adaptpro.wiki.query import answer_question
from adaptpro.wiki.store import write_wiki

STATIC = Path(__file__).resolve().parent / "static"
RUN_DIR = repo_root() / "demo" / "run" / "wiki"

_wiki: CompiledWiki | None = None


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8765), Handler)
    print("AdaptPro LLM wiki demo: http://127.0.0.1:8765", flush=True)
    print("Slides: open demo/slides.html", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/":
            self._bytes(200, "text/html; charset=utf-8", (STATIC / "index.html").read_bytes())
            return
        if path == "/api/state":
            self._json(200, _state())
            return
        self._json(404, {"error": "not found"})

    def do_POST(self) -> None:
        global _wiki
        path = urlparse(self.path).path
        if path == "/api/ingest":
            count = 1 if _wiki is None else _wiki.ingest_count + 1
            _wiki = compile_wiki(ingest_count=count)
            write_wiki(RUN_DIR, _wiki)
            self._json(200, _state())
            return
        if path == "/api/lint":
            if _wiki is None:
                self._json(400, {"error": "Ingest the corpus first."})
                return
            report = lint_wiki(_wiki)
            _wiki = with_lint_page(_wiki, report)
            write_wiki(RUN_DIR, _wiki)
            self._json(200, {"state": _state(), "report": report.model_dump()})
            return
        if path == "/api/query":
            if _wiki is None:
                self._json(400, {"error": "Ingest the corpus first."})
                return
            payload = json.loads(self.rfile.read(int(self.headers.get("Content-Length", "0"))) or b"{}")
            question = str(payload.get("question", "")).strip()
            scope = str(payload.get("scope", "overview"))
            if not question:
                self._json(400, {"error": "Ask a question."})
                return
            try:
                result = answer_question(_wiki, question, scope)
            except ValueError as exc:
                self._json(400, {"error": str(exc)})
                return
            self._json(200, result.model_dump())
            return
        self._json(404, {"error": "not found"})

    def log_message(self, format: str, *args: object) -> None:
        return

    def _json(self, status: int, payload: object) -> None:
        body = json.dumps(payload).encode("utf-8")
        self._bytes(status, "application/json; charset=utf-8", body)

    def _bytes(self, status: int, content_type: str, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def _state() -> dict[str, object]:
    if _wiki is None:
        return {"ingested": False, "pages": []}
    order = ["overview", "business", "product", "tech", "lint", "index", "log"]
    slugs = [slug for slug in order if slug in _wiki.pages]
    slugs.extend(sorted(slug for slug in _wiki.pages if slug.startswith("sources/")))
    return {
        "ingested": True,
        "epic_title": _wiki.epic_title,
        "kickoff_status": _wiki.kickoff_status,
        "ingest_count": _wiki.ingest_count,
        "page_count": len(_wiki.pages),
        "log": _wiki.log,
        "pages": [
            {
                "slug": slug,
                "title": _wiki.page(slug).title,
                "summary": _wiki.page(slug).summary,
                "body": _wiki.page(slug).body,
            }
            for slug in slugs
        ],
    }


if __name__ == "__main__":
    main()

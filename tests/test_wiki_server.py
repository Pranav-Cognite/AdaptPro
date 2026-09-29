import json
import threading
from http.server import ThreadingHTTPServer
from urllib.request import Request, urlopen

import adaptpro.wiki.server as server


def test_ingest_query_and_lint_over_http() -> None:
    server._wiki = None
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=lambda: httpd.serve_forever(poll_interval=0.05), daemon=True)
    thread.start()
    try:
        home = urlopen(f"http://127.0.0.1:{port}/")
        assert home.status == 200
        assert b"LLM wiki" in home.read()

        ingested = _post(port, "/api/ingest", {})
        assert ingested["kickoff_status"] == "Ready"
        assert ingested["page_count"] > 8

        answer = _post(
            port,
            "/api/query",
            {"question": "Can the user create a work order from the answer?", "scope": "overview"},
        )
        assert answer["pages_read"] == ["index", "overview"]
        assert "No write tools" not in answer["answer"]

        linted = _post(port, "/api/lint", {})
        assert linted["report"]["health"] == "usable"
        assert linted["state"]["kickoff_status"] == "Ready"
    finally:
        httpd.shutdown()
        server._wiki = None


def _post(port: int, path: str, payload: dict[str, object]) -> dict[str, object]:
    request = Request(
        f"http://127.0.0.1:{port}{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request) as response:
        body = json.loads(response.read().decode("utf-8"))
    assert isinstance(body, dict)
    return body

# ADR-015: Tool surface for v1

Status: accepted (architecture).

Tool-calling over the Instances API + file RAG.

No write tools registered.

p95 latency < 8s is a launch blocker.

"Real-time" as streaming ingest is out of scope; we query data already in CDF.

Source of truth is a specific view in a specific space — not RAW, not last week's export.

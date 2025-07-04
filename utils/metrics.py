"""Optional Prometheus metrics for monitoring agent workflows."""

from __future__ import annotations

try:
    from prometheus_client import Counter, Histogram, start_http_server
except ImportError:  # pragma: no cover - optional dependency
    Counter = Histogram = None
    start_http_server = None

# Counters for agent executions and ingested documents
AGENT_RUNS = Counter("agent_runs_total", "Number of times an agent was executed", ["agent"]) if Counter else None
DOCUMENTS_INGESTED = Counter("documents_ingested_total", "Total documents ingested") if Counter else None

# Histogram to measure workflow runtime
WORKFLOW_SECONDS = Histogram("workflow_run_seconds", "Time spent running a workflow") if Histogram else None


def start_metrics_server(port: int = 8001) -> None:
    """Expose metrics on an HTTP endpoint if prometheus_client is available."""
    if start_http_server is not None:
        start_http_server(port)

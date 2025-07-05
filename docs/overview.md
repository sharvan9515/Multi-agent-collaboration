# Project Overview

RAG_HEITAA is a Retrieval-Augmented Generation (RAG) system designed for
automating health insurance claims questions.  It follows a **multi-agent
workflow** paradigm where each agent performs a single step such as
redacting PHI, summarising context or generating an answer.

## How It Works
1. **User Query** – a question is submitted via the `ChatEngine` or API.
2. **Workflow Execution** – the `Workflow` or `MultiAgentCoordinator` runs a
   list of agents in sequence. Shared state is passed via a `context`
   dictionary.
3. **Document Retrieval** – the `RAGAgent` queries the vector store for
   relevant documents and assembles a prompt with chat history.
4. **LLM Response** – the language model produces the final answer which is
   returned to the user.
5. **Observability** – an `EventBus` emits events for every step. Prometheus
   metrics and an audit log can be enabled for monitoring.

The design embraces the _workflow pattern_ where agents are arranged in a
pipeline. Optional hooks allow custom code to run before and after each agent.

## Theory
- **Retrieval Augmented Generation** combines search (vector retrieval) with
  language model reasoning. It grounds answers in the indexed knowledge base.
- **Agents** encapsulate discrete behaviours. Chaining them promotes
  modularity and reuse.
- **Workflow Hooks** let developers inject validation, filtering or logging
  around each agent without modifying core logic.
- **Event Bus** decouples components by allowing subscribers to react to
  `workflow_start`, `agent_end`, etc.
- **Metrics & Auditing** provide enterprise-grade visibility into each
  conversation and ingestion event.

## Flowchart
```text
 User Query
     |
     v
+-----------+
| Workflow  |
| (agents)  |
+-----------+
  |  |  |
  |  |  +--> SummaryAgent
  |  +-----> DeidAgent
  +--------> RAGAgent -> Vector DB
     |
     v
 Response
```

This flow shows a typical run: the workflow sends the message through each
agent, retrieves documents, and returns an answer while emitting events and
collecting metrics.

## Recommended Video Tutorials

To dive deeper into each subsystem, consider the following YouTube resources:

- [Retrieval Augmented Generation Explained](https://www.youtube.com/watch?v=pYhB4YwbCLE)
- [Building Python Agents with LangChain](https://www.youtube.com/watch?v=9n1HUsvK3PY)
- [Celery Task Queues Tutorial](https://www.youtube.com/watch?v=Z00rs1F8VZM)
- [FastAPI Crash Course](https://www.youtube.com/watch?v=0sOvCWFmrtA)
- [Prometheus & Grafana Basics](https://www.youtube.com/watch?v=h4Sl21AKiDg)

## Security Utilities

Several modules help secure the application:

- `cybersecurity.encryption` provides symmetric encryption helpers.
- `cybersecurity.integrity` offers SHA‑256 hashing for data verification.
- `cybersecurity.monitor` checks the health of Qdrant and the message broker.
- `agents.security_agent.SecurityAgent` combines these utilities to validate
  messages within a workflow.
- `storage.audit_log` writes JSON audit events with optional data hashes.
